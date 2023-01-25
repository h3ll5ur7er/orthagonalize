# Orthagonalize

The goal of this tool is to detect the perspective distortion of a image of a planar surface using aruco markers and then correct it.

## Setup

### Prerequisites

- Python 3.9
- Poetry

### Installation

```bash
git clone http://github.com/h3ll5ur7er/orthagonalize
cd orthagonalize
poetry install
```

## Usage

### Generate Aruco Markers

the default marker dictionary has 7x7 bits with a 1 bit border and 1000 entries. This can be adjusted inside the config.py file.
the default number of pixels per bit is 254.

```bash
poetry run python -m orthagonalize generate <id> [<pixels_per_bit>]
```

for example to get a marker with the id 42 and a resulting image size of 900x900 pixels ((7 bits + 2*1 bit border)*100 pixels per bit):

```bash
poetry run python -m orthagonalize generate 42 100
```

print the marker at a known absolute size (e.g. insert the image into a word document and set the size to 50mm x 50mm)

### Orthagonalize image

```bash
poetry run python -m orthagonalize image <path> <marker_size_mm>
```

The following steps are performed:

- the marker will be detected within the image.
- a homography matrix will be calculated to align and center the marker within a 15360x8640 image.
- the input image is then warped using the homography matrix.
- the corners of the input image are projected using the homography matrix.
- the projected corners are clamped to the 15360x8640 image.
- the image is cropped to the clamped corner bounds.
- the cropped image is displayed and saved to the same directory as the input image.

### Orthagonalize stream

```bash
poetry run python -m orthagonalize stream <source> <marker_size_mm>
```

the stream source can be a camera index or a video file path.
