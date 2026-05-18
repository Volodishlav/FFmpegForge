import os
import subprocess
from pathlib import Path
import argparse
import arg_verification

# SETTINGS
INPUT_DIR = "./test"
OUTPUT_DIR = "./output"
EXTENSIONS = {}
IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}

os.makedirs(OUTPUT_DIR, exist_ok=True)

# parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str)
parser.add_argument("-o", "--output", type=str)
parser.add_argument("-e", "--extensions", type=str)
parser.add_argument("-eV", "--video-extensions", action="store_true")
parser.add_argument("-eI", "--image-extensions", action="store_true")

args = parser.parse_args()

# set global variables based on arguments
INPUT_DIR = arg_verification.arg_input() or INPUT_DIR
OUTPUT_DIR = arg_verification.arg_output() or OUTPUT_DIR
EXTENSIONS = arg_verification.arg_extensions() or #########################


def main():
    
    global INPUT_DIR, OUTPUT_DIR, EXTENSIONS, IMG_EXTENSIONS, VIDEO_EXTENSIONS

    # ask user for custom parameters (added fallback)
    INPUT_DIR = input(f"Enter input directory (Default: {INPUT_DIR}): ") or INPUT_DIR
    OUTPUT_DIR = input(f"Enter output directory (Default: {OUTPUT_DIR}): ") or OUTPUT_DIR

    imgORvid = input("Process images or videos? (i/v, Default: i): ") or "i"

    if imgORvid.lower() == "v":
        extensions_input = input(f"Enter file extensions to process or press Enter for defaults (comma-separated, Default: {(VIDEO_EXTENSIONS)}): ") or ", ".join(VIDEO_EXTENSIONS)
        try:
            for ext in extensions_input.split(","):
                if not ext.strip().startswith("."):
                    print(f"Invalid extension: {ext}")
                    EXTENSIONS = VIDEO_EXTENSIONS
                    break

            if EXTENSIONS != VIDEO_EXTENSIONS:
                EXTENSIONS = {ext.strip().lower() for ext in extensions_input.split(",")}
            
        except ValueError as e:
            print("Error:", e)
            EXTENSIONS = VIDEO_EXTENSIONS

    elif imgORvid.lower() == "i":
        extensions_input = input(f"Enter file extensions to process or press Enter for defaults (comma-separated, Default: {(IMG_EXTENSIONS)}): ") or ", ".join(IMG_EXTENSIONS)
        try:
            for ext in extensions_input.split(","):
                if not ext.strip().startswith("."):
                    print(f"Invalid extension: {ext}")
                    EXTENSIONS = IMG_EXTENSIONS
                    break

            if EXTENSIONS != IMG_EXTENSIONS:
                EXTENSIONS = {ext.strip().lower() for ext in extensions_input.split(",")}

        except ValueError as e:
            print("Error:", e)
            EXTENSIONS = IMG_EXTENSIONS

    else:
        print("Invalid choice. Setting to default image extensions...")
        EXTENSIONS = IMG_EXTENSIONS


    compressionORconversion = input("Compress/resize (c) or convert (v)? (Default: c): ") or "c"

    if compressionORconversion.lower() == "c":
        customwidth = int(input("Enter maximum width (Default: 1920): ") or 1920)
        compression = int(input("Enter compression level (1-31 | Lower = better quality | Default: 4): ") or 4)

    elif compressionORconversion.lower() == "v":
        targetExtension = input("Enter target file extension for conversion (e.g., .jpg, .mp4): ").strip().lower()
        if not targetExtension.startswith("."):
            targetExtension = "." + targetExtension
            customwidth = None
            compression = None
    else:
        print("Invalid choice. Setting to default compression settings...")
        customwidth = 1920
        compression = 4

    RUN(customwidth, compression, targetExtension if compressionORconversion.lower() == "v" else None)

def setCommand(file: str, customwidth: int, compression: int, OutputFile: str, targetExtension: str = None) -> list[str]:

    if targetExtension is not None:
        if targetExtension.lower() not in EXTENSIONS:
            raise ValueError(f"Unsupported target extension: {targetExtension}")
        command = [
            "ffmpeg", "-i", str(file), str(OutputFile)
        ]

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

def RUN(customwidth, compression, targetExtension=None):

    for file in Path(INPUT_DIR).iterdir():
        if file.suffix.lower() not in EXTENSIONS:
            continue

        print(f"Processing: {file.name}")

        if targetExtension is not None:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{targetExtension}"
        else:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{file.suffix.lower()}"

            command = setCommand(file, customwidth, compression, OutputFile, targetExtension)

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

print("Done.")

if __name__ == "__main__":
    main()