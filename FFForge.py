import os
import subprocess
from pathlib import Path
import argparse
# From click import command


# SETTINGS
INPUT_DIR = "./test"
OUTPUT_DIR = "./output"

INPUT_FILE = None
OUTPUT_FILE = None

EXTENSIONS = {}
IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}

os.makedirs(OUTPUT_DIR, exist_ok=True)


# PARSE ARGS
parser = argparse.ArgumentParser()

parser.add_argument("input_file")
parser.add_argument("output_file")

parser.add_argument("-i", "--input", type=str)                                    # Arguments: [input-dir]
parser.add_argument("-o", "--output", type=str)                                   # Arguments: [output-dir]

ex_args = parser.add_mutually_exclusive_group()

ex_args.add_argument("-cP", "--compress", nargs=2)                                 # Arguments: [max-width] [compression-level]
ex_args.add_argument("-cV", "--convert", type=str)                                 # Arguments: [target-extension]
ex_args.add_argument("-r", "--resize", type=str)                                   # Arguments: [width:height] "AUTO" can be used for automatic aspect ratio in either width or height
ex_args.add_argument("-f", "--fps", type=int)                                      # Arguments: [fps]
ex_args.add_argument("-eF", "--extract-frames", action="store_true")               # Arguments: (True/False)

parser.add_argument("-tE", "--target-extension", type=str)                        # Arguments: [target-extension]

args = parser.parse_args()                                                        # Parse all arguments


def RUN():
    for file in Path(INPUT_DIR).iterdir():

        if args.target_extension is not None:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{args.target_extension}"
        elif args.target_extension is None:
            OutputFile = Path(OUTPUT_DIR) / f"{file.stem}{file.suffix.lower()}"


        if INPUT_FILE is not None and ((Path(INPUT_FILE)).is_file()) is True:
            file = Path(INPUT_FILE)

        if OUTPUT_FILE is not None and ((Path(OUTPUT_FILE)).is_file()) is True:
            OutputFile = Path(OUTPUT_FILE)
            custom_output_file = True


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
                if custom_output_file:
                    OutputFile = Path(OUTPUT_FILE)
                else:
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
                    "ffmpeg",
                    "-i", str(file),
                    "-r", str(args.fps),
                    str(OutputFile)
                ]

            elif args.extract_frames is not None:
                if custom_output_file:
                    OutputFile = Path(OUTPUT_FILE)
                else:
                    OutputFile = Path(OUTPUT_DIR) / f"{file.stem}.%04d.png"

                command = [
                    "ffmpeg",
                    "-i", str(file),
                    str(OutputFile)
                    ]

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
    global INPUT_DIR, INPUT_FILE, OUTPUT_DIR, OUTPUT_FILE

    if args.input is not None and parser.input_file is not None:
        print("Error: Both input file and input directory cannot be specified at the same time.")
        return

    if args.output is not None and parser.output_file is not None:
        print("Error: Both output file and output directory cannot be specified at the same time.")
        return
    

    if args.input is not None:
        INPUT_DIR = args.input
        print(f"Input path set to: {INPUT_DIR}")

    elif parser.input_file is not None:
        tmp_path = Path(parser.input_file)

        INPUT_DIR = None
        INPUT_FILE = tmp_path.resolve()

        print(f"Input file set to: {INPUT_FILE}")

    else:
        print("Using default input path.")


    if args.output is not None:
        OUTPUT_DIR = args.output
        print(f"Output path set to: {OUTPUT_DIR}")

    elif parser.output_file is not None:
        tmp_path = Path(parser.output_file)

        OUTPUT_DIR = None
        OUTPUT_FILE = tmp_path.resolve()

        print(f"Output file set to: {OUTPUT_FILE}")

    else:
        print("Using default output path.")

    RUN()


if __name__ == "__main__":
    main()