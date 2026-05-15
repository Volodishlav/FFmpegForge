import os
import subprocess
from pathlib import Path

# SETTINGS
INPUT_DIR = "./test"
OUTPUT_DIR = "./output"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    global INPUT_DIR, OUTPUT_DIR, EXTENSIONS

    # ask user for custom parameters (added fallback)
    INPUT_DIR = input(f"Enter input directory (Default: {INPUT_DIR}): ") or INPUT_DIR
    OUTPUT_DIR = input(f"Enter output directory (Default: {OUTPUT_DIR}): ") or OUTPUT_DIR

    extensions_input = input(f"Enter file extensions to process (comma-separated, Default: {(EXTENSIONS)}): ") or ", ".join(EXTENSIONS)
    EXTENSIONS = {ext.strip().lower() for ext in extensions_input.split(",")}

    customwidth = int(input("Enter width (Default: 1920): ") or 1920)
    compression = int(input("Enter compression level (1-31 | Lower = better quality | Default: 4): ") or 4)

    RUN(customwidth, compression)

def setCommand(file: str, customwidth: int, compression: int, OutputFile: str) -> list[str]:

    if file.suffix.lower() == ".gif":
        vf = (
            f"fps=10,scale={customwidth}:-2:flags=lanczos,"
            "split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
        )

        command = [
            "ffmpeg", "-y", "-i", str(file),
            "-vf", vf,
            str(OutputFile)
        ]

    else:
        command = [
            "ffmpeg", "-y", "-i", str(file),
            # resize if exceeds 1920px in width
            # "-vf", "scale='min(3840,iw)':-2",
            "-vf", f"scale={customwidth}:-2",
            # quality / compression level
            "-q:v", str(compression),
            str(OutputFile)
        ]

    return command

def RUN(customwidth, compression):
    for file in Path(INPUT_DIR).iterdir():
        if file.suffix.lower() not in EXTENSIONS:
            continue
        
        OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{file.suffix.lower()}"
        command = setCommand(file, customwidth, compression, OutputFile)

        print(f"Compressing: {file.name}")

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

print("Done.")

if __name__ == "__main__":
    main()