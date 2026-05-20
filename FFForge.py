import os
import subprocess
from pathlib import Path
import argparse

from click import command


# SETTINGS
INPUT_DIR = "./test"
OUTPUT_DIR = "./output"
EXTENSIONS = {}
IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}

os.makedirs(OUTPUT_DIR, exist_ok=True)


# PARSE ARGS
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str)                                      # Arguments: [input-dir]
parser.add_argument("-o", "--output", type=str)                                     # Arguments: [output-dir]

parser.add_argument("-cP", "--compress", nargs=2)                                   # Arguments: [max-width] [compression-level]
parser.add_argument("-cV", "--convert", type=str)                                   # Arguments: [target-extension]
parser.add_argument("-r", "--resize", type=str)                                     # Arguments: [width:height]
parser.add_argument("-f", "--fps", type=int)                                        # Arguments: [fps]

parser.add_argument("-tE", "--target-extension", type=str)                          # Arguments: [target-extension]

args = parser.parse_args()

def RUN():
    for file in Path(INPUT_DIR).iterdir():

        if args.target_extension is not None:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{args.target_extension}"
        elif args.target_extension is None:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{file.suffix.lower()}"

        try:
            if args.compress is not None:
                max_width, compression_level = args.compress
                command = ["ffmpeg", "-i", str(file), "-vf", f"scale='min({max_width},iw)':-2", "-q:v", compression_level, str(OutputFile)]

            elif args.convert is not None:
                OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{args.convert}"
                command = ["ffmpeg", "-i", str(file), str(OutputFile)]

            elif args.resize is not None:
                width, height = args.resize.split(":")
                command = ["ffmpeg", "-i", str(file), "-vf", f"scale={width}:{height}", str(OutputFile)]

            elif args.fps is not None:
                command = ["ffmpeg", "-i", str(file), "-r", str(args.fps), str(OutputFile)]

        except Exception as e:
            print(f"Error processing {file.name}: {e}")
            return


        print(f"Processing: {file.name}")

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def main():
    global INPUT_DIR, OUTPUT_DIR

    if args.input is None:
        print("Using default input path.")

    if args.output is None:
        print("Using default output path.")

    else:
        INPUT_DIR = args.input
        OUTPUT_DIR = args.output

    RUN()


if __name__ == "__main__":
    main()