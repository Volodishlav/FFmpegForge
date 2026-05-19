import os
import subprocess
from pathlib import Path
import argparse

# SETTINGS
INPUT_DIR = "./test"
OUTPUT_DIR = "./output"
EXTENSIONS = {}
IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}

os.makedirs(OUTPUT_DIR, exist_ok=True)


# PARSE ARGS
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str)
parser.add_argument("-o", "--output", type=str)

ext_group = parser.add_mutually_exclusive_group()
ext_group.add_argument("-e", "--extensions", type=str)
ext_group.add_argument("-eV", "--video-extensions", action="store_true")
ext_group.add_argument("-eI", "--image-extensions", action="store_true")

parser.add_argument("-cP", "--compress", action="store_true")
parser.add_argument("-cV", "--convert", action="store_true")

parser.add_argument("-w", "--max-width", type=int)
parser.add_argument("-l", "--compression-level", type=int)
parser.add_argument("-tE", "--target-extension", type=str)

args = parser.parse_args()

# COMPATIBILITY CHECKS
if args.compress:
    if args.convert:
        parser.error("-cP/--compress cannot be used with -cV/--convert")

    if args.target_extension is not None:
        parser.error("-cP/--compress cannot be used with -tE/--target-extension")

if args.convert:
    if args.compress:
        parser.error("-cV/--convert cannot be used with -cP/--compress")

    if args.max_width is not None:
        parser.error("-cV/--convert cannot be used with -w/--max-width")

    if args.compression_level is not None:
        parser.error("-cV/--convert cannot be used with -l/--compression-level")

# INPUT
def set_input_dir():
    global INPUT_DIR
    # ask user for input directory (added fallback)
    try:
        INPUT_DIR = input(f"Enter input directory (Default: {INPUT_DIR}): ") or INPUT_DIR
        os.makedirs(INPUT_DIR, exist_ok=True)
    except Exception as e:
        INPUT_DIR = "./"
        print(f"Error occurred while setting input directory: {e} | (new input directory set to {INPUT_DIR})")

def arg_input():
    if args.input is not None:
        return args.input
    else:
        set_input_dir()

# OUTPUT
def set_output_dir():
    global OUTPUT_DIR
    # ask user for output directory (added fallback)
    try:
        OUTPUT_DIR = input(f"Enter output directory (Default: {OUTPUT_DIR}): ") or OUTPUT_DIR
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except Exception as e:
        OUTPUT_DIR = "./output"
        print(f"Error occurred while setting output directory: {e} | (new output directory set to {OUTPUT_DIR})")
    
def arg_output():
    if args.output is not None:
        return args.output
    else:
        set_output_dir()

# EXTENSIONS
def set_extensions():
    global EXTENSIONS
    # ask user if they want to process images or videos (added fallback)
    imgORvid = input("Process images or videos? (i/v, Default: i): ") or "i"

    if imgORvid.lower() == "v":
        extensions_input = input(f"Enter file extensions to process or press Enter for defaults (comma-separated, Default: {(VIDEO_EXTENSIONS)}): ") or ", ".join(VIDEO_EXTENSIONS)
        try:
            for ext in extensions_input.split(","):
                if not ext.strip().startswith("."):
                    print(f"Invalid extension: {ext}")
                    print("Extensions set to default video extensions.")
                    EXTENSIONS = VIDEO_EXTENSIONS
                    break

            if EXTENSIONS != VIDEO_EXTENSIONS:
                EXTENSIONS = {ext.strip().lower() for ext in extensions_input.split(",")}
            
        except ValueError as e:
            print("Error:", e)
            print("Extensions set to default video extensions.")
            EXTENSIONS = VIDEO_EXTENSIONS

    elif imgORvid.lower() == "i":
        extensions_input = input(f"Enter file extensions to process or press Enter for defaults (comma-separated, Default: {(IMG_EXTENSIONS)}): ") or ", ".join(IMG_EXTENSIONS)
        try:
            for ext in extensions_input.split(","):
                if not ext.strip().startswith("."):
                    print(f"Invalid extension: {ext}")
                    print("Extensions set to default image extensions.")
                    EXTENSIONS = IMG_EXTENSIONS
                    break

            if EXTENSIONS != IMG_EXTENSIONS:
                EXTENSIONS = {ext.strip().lower() for ext in extensions_input.split(",")}

        except ValueError as e:
            print("Error:", e)
            print("Extensions set to default image extensions.")
            EXTENSIONS = IMG_EXTENSIONS

    else:
        print("Invalid choice. Try again.")
        set_extensions()

def arg_extensions():
    global EXTENSIONS

    if args.image_extensions == True:
        EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

    elif args.video_extensions == True:
        EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}
    
    else:
        if args.extensions is not None:
            try:
                for ext in args.extensions.split(","):
                    ext = ext.strip().lower()

                    if not ext.startswith("."):
                        ext = "." + ext

                    EXTENSIONS.add(ext)

            except Exception as e:
                print("Error:", e)
                set_extensions()
        else:
            set_extensions()

# COMPRESSION OR CONVERSION
def set_compression_or_conversion():

    compressionORconversion = input("Compress/resize (c) or convert (v)? (Default: c): ") or "c"

    if compressionORconversion.lower() == "c":
        while True:
            tmp_customwidth = input("Enter maximum width (Default: 1920): ")

            if tmp_customwidth == "":
                customwidth = 1920
                break

            try:
                customwidth = int(tmp_customwidth)
                break

            except ValueError:
                print("Please enter a valid integer")

        while True:
            tmp_compression = input("Enter compression level (1-31 | Lower = better quality | Default: 4): ")

            if tmp_compression == "":
                compression = 4
                break

            try:
                compression = int(tmp_compression)
                break

            except ValueError:
                print("Please enter a valid integer")
        
        target_extension = None

    elif compressionORconversion.lower() == "v":
        while True:
            target_extension = input("Enter target file extension for conversion (e.g., .jpg, .mp4): ").strip().lower()

            if target_extension == "":
                print("Error: extension cannot be empty")
                continue

            if not target_extension.startswith("."):
                target_extension = "." + target_extension

            break

        customwidth = None
        compression = None

    else:
        print("Invalid choice. Try again.")
        set_compression_or_conversion()

    RUN(customwidth, compression, target_extension if compressionORconversion.lower() == "v" else None)

def arg_compress_or_convert():
    if args.compress:
        if args.max_width is not None and type(args.max_width) == int:
            customwidth = int(args.max_width)

        else:
            while True:
                tmp_customwidth = input("Enter maximum width (Default: 1920): ")

                if tmp_customwidth == "":
                    customwidth = 1920
                    break

                try:
                    customwidth = int(tmp_customwidth)
                    break

                except ValueError:
                    print("Please enter a valid integer")

        if args.compression_level is not None and type(args.compression_level) == int:
            compression = int(args.compression_level)
        
        else:
            while True:
                tmp_compression = input("Enter compression level (1-31 | Lower = better quality | Default: 4): ")

                if tmp_compression == "":
                    compression = 4
                    break

                try:
                    compression = int(tmp_compression)
                    break

                except ValueError:
                    print("Please enter a valid integer")

        target_extension = None
    
    elif args.convert:
        if args.target_extension is not None and type(args.target_extension) == str:
            target_extension = args.target_extension.strip().lower()

        else:
            while True:
                target_extension = input("Enter target file extension for conversion (e.g., .jpg, .mp4): ").strip().lower()

                if target_extension == "":
                    print("Error: extension cannot be empty")
                    continue

                if not target_extension.startswith("."):
                    target_extension = "." + target_extension

                break
        
        customwidth = None
        compression = None

    else:
        set_compression_or_conversion()

    RUN(customwidth, compression, target_extension)


def set_command(file: str, customwidth: int, compression: int, OutputFile: str, target_extension: str = None) -> list[str]:

    if target_extension is not None:
        if target_extension.lower() not in EXTENSIONS:
            raise ValueError(f"Unsupported target extension: {target_extension}")
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


def RUN(customwidth, compression, target_extension=None):

    for file in Path(INPUT_DIR).iterdir():
        if file.suffix.lower() not in EXTENSIONS:
            continue

        print(f"Processing: {file.name}")

        if target_extension is not None:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{target_extension}"
        else:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{file.suffix.lower()}"

            command = set_command(file, customwidth, compression, OutputFile, target_extension)

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )


def main():
    # SET GLOBAL VARIABLES FROM ARGS
    arg_input()
    arg_output()
    arg_extensions()
    arg_compress_or_convert()

print("Done.")

if __name__ == "__main__":
    main()