# FFmpegForge
A lightweight Python CLI tool for batch media processing powered by FFmpeg.

Supports:

* Batch compression, conversion and resizing
* FPS modification
* Custom output extensions

---

## Features

* Batch process entire directories
* Simple CLI interface
* FFmpeg-powered media operations
* Supports both image and video workflows
* Silent FFmpeg execution
* Automatic output directory creation

---

## Requirements

* Python 3.9+

* Python dependencies

```bash
pip install click
```

* FFmpeg installed

[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

> [!IMPORTANT]
> FFmpeg must be installed and **available in your system PATH**.

---

## Installation

```bash
git clone https://github.com/yourname/mediabatch.git
cd mediabatch
```

---

## Usage

```bash
python FFForge.py [ARGS]
```

> [!WARNING]
> Existing files in the output directory **will be overwritten**.

---

## Args

| Argument                    | Description                                        |
| --------------------------- | -------------------------------------------------- |
| `-i`, `--input`             | Input directory                                    |
| `-o`, `--output`            | Output directory                                   |
| `-cP`, `--compress`         | Compress media using max width + compression level |
| `-cV`, `--convert`          | Convert media to another extension                 |
| `-r`, `--resize`            | Resize media using WIDTH:HEIGHT                    |
| `-f`, `--fps`               | Change FPS                                         |
| `-tE`, `--target-extension` | Force output extension                             |

---

## Examples

### Compress media

```bash
python main.py -cP 1920 28
# 1920 --> maximum width; height is calculated automatically
# 28   --> compression level
```

> [!TIP]
> Use lower compression values for higher quality.

Compresses media while preserving aspect ratio.

---

### Convert media format

```bash
python main.py -cV .mp4
```

Converts all compatible files to MP4.

---

### Resize media

```bash
python main.py -r 1280:720
```

Resizes media to 1280x720.

---

### Change FPS

```bash
python main.py -f 60
```

Changes output FPS to 60.

---

### Custom input/output directories

```bash
python main.py -i ./media -o ./processed -cV .webm
```

---

## Supported Extensions

```python
IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}
```

---

# Future Improvements

* More options
* Extension filtering
* Recursive directory traversal
* Progress bars
* Much more
