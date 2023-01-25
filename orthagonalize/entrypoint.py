# pylint: disable=unnecessary-lambda
""" main entry point for the cli """

# pylint: disable=no-member
# pylint: disable=bad-whitespace

import sys
import cv2

from orthagonalize.generate import generate_marker
from orthagonalize.marker_detector import stream, orthagonalize

OUTPUT_IMAGE_SIZE = (3840*4, 2160*4)
OUTPUT_IMAGE_CENTER = (OUTPUT_IMAGE_SIZE[0] / 2, OUTPUT_IMAGE_SIZE[1] / 2)

def print_usage_and_exit(exit_code: int = -1):
    """ print usage """
    print('''usage: <mandatory> [optional]
    poetry run python -m orthagonalize generate <id> [pixel_per_bit=254]
    poetry run python -m orthagonalize stream <video_source> <marker_width_mm>
    poetry run python -m orthagonalize image <input_image_path> <marker_width_mm>
''')
    sys.exit(exit_code)

def invoke_for_single_image(*args) -> None:
    """ invoke orthagonalization for a single image and save the result to disk"""
    if len(args) != 2:
        print_usage_and_exit()
    path, marker_width_mm = args
    img = cv2.imread(path)
    img, min_x, max_x, min_y, max_y = orthagonalize(img, marker_width_mm)
    img = img[min_y:max_y, min_x:max_x]
    cv2.imshow("orthagonalized", img)
    cv2.imwrite(path + ".orthagonalized.png", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main(*args) -> None:
    """ parse user input to switch between marker generation and image orthagonalization """

    if len(args) == 0:
        print_usage_and_exit()

    subcmd, *args = args

    action = {
        'generate': lambda *args: generate_marker(*args),
        'stream':   lambda *args: stream(*args),
        'image':    lambda *args: invoke_for_single_image(*args),
        'help':     lambda *args: print_usage_and_exit(0),
        '--help':   lambda *args: print_usage_and_exit(0),
    }.get(subcmd,   lambda *args: print_usage_and_exit())

    action(*args)
