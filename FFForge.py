import os
import subprocess
from pathlib import Path
import argparse
# From click import command


# SETTINGS
INPUT_DIR = "./test"
OUTPUT_DIR = "./output"
EXTENSIONS = {}
IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}

os.makedirs(OUTPUT_DIR, exist_ok=True)


# PARSE ARGS
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str)                                    # Arguments: [input-dir]
parser.add_argument("-o", "--output", type=str)                                   # Arguments: [output-dir]

parser.add_argument("-cP", "--compress", nargs=2)                                 # Arguments: [max-width] [compression-level]
parser.add_argument("-cV", "--convert", type=str)                                 # Arguments: [target-extension]
parser.add_argument("-r", "--resize", type=str)                                   # Arguments: [width:height] "AUTO" can be used for automatic aspect ratio in either width or height
parser.add_argument("-f", "--fps", type=int)                                      # Arguments: [fps]
parser.add_argument("-eF", "--extract-frames", action="store_true")               # Arguments: (True/False)

parser.add_argument("-tE", "--target-extension", type=str)                        # Arguments: [target-extension]

args = parser.parse_args()                                                        # Parse all arguments


def RUN():
    for file in Path(INPUT_DIR).iterdir():

        if args.target_extension is not None:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{args.target_extension}"
        elif args.target_extension is None:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{file.suffix.lower()}"

        try:
            if args.compress is not None:
                max_width, compression_level = args.compress

                command = ["ffmpeg",
                    "-i", str(file),
                    "-vf", f"scale='min({max_width},iw)':-2",
                    "-q:v", compression_level,
                    str(OutputFile)
                ]

            elif args.convert is not None:
                OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{args.convert}"

                if args.convert.lower() == ".jpg":
                    command = [
                        "ffmpeg",
                        "-i", str(file),
                        "-vf", "format=yuv420p",
                        "-q:v", "2",
                        str(OutputFile)
                    ]

                if file.suffix.lower() == ".webp":
                    command = [
                        "ffmpeg",
                        "-i", str(file),
                        "-vf", "fps=15,scale=640:-1:flags=lanczos",
                        "-gifflags", "-transdiff",
                        "-y",
                        str(OutputFile)
                    ]

                    # command = [
                    #     "ffmpeg",
                    #     "-i", str(file), "-filter_complex",
                    #     "[0:v] palettegen[p]; [0:v][p] paletteuse",
                    #     str(OutputFile)
                    # ]

                    # command = [
                    #   "ffmpeg", "-c:v","libwebp",
                    #   "-i", str(file), "-filter_complex",
                    #   "[0:v] palettegen[p]; [0:v][p] paletteuse",
                    #   str(OutputFile)
                    # ]

                if file.suffix.lower() == ".gif":
                     command = [
                        "ffmpeg",
                        "-i", str(file),
                        "-movflags", "+faststart",
                        "-pix_fmt", "yuv420p",
                        str(OutputFile)
                    ]
                     
                else:
                    command = [
                        "ffmpeg", "-i",
                        str(file),
                        str(OutputFile)
                    ]

            elif args.resize is not None:
                width, height = args.resize.split(":")

                width = "-1" if width.upper() == "AUTO" else width
                height = "-1" if height.upper() == "AUTO" else height

                if width == "-1" and height == "-1":
                    raise ValueError("Both width and height cannot be set to AUTO at the same time.")

                command = [
                    "ffmpeg",
                    "-i", str(file),
                    "-vf", f"scale={width}:{height}",
                    str(OutputFile)
                ]

            elif args.fps is not None:
                command = [
                    "ffmpeg", "-i", str(file),
                    "-r", str(args.fps),
                    str(OutputFile)
                ]

            elif args.extract_frames is not None:
                OutputFile = Path(OUTPUT_DIR) / f"{file.stem}.%04d.png"
                command = ["ffmpeg", "-i", str(file), str(OutputFile)]

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

    if args.input is not None:
        INPUT_DIR = args.input
        print(f"Input path set to: {INPUT_DIR}")
    else:
        print("Using default input path.")

    if args.output is not None:
        OUTPUT_DIR = args.output
        print(f"Output path set to: {OUTPUT_DIR}")
    else:
        print("Using default output path.")

    RUN()


if __name__ == "__main__":
    main()