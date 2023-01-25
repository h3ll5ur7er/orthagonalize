""" global config """

# pylint: disable=no-member
# pylint: disable=bad-whitespace

import cv2

## Use this to use custom dictionary. Takes a long time to load..
# BITS_PER_SIDE, MAX_ID = 10, 1000
# NAME = f"Custom{BITS_PER_SIDE}x{BITS_PER_SIDE}x{MAX_ID}"
# MARKER_DICT = cv2.aruco.extendDictionary(MAX_ID, BITS_PER_SIDE)

MARKER_DICTIONARIES = {
    cv2.aruco.DICT_7X7_1000:       (f"Aruco7x7x1000", 7, 1000),
    cv2.aruco.DICT_7X7_250:        (f"Aruco7x7x250",  7, 250),
    cv2.aruco.DICT_7X7_100:        (f"Aruco7x7x100",  7, 100),
    cv2.aruco.DICT_7X7_50:         (f"Aruco7x7x50",   7, 50),
    cv2.aruco.DICT_6X6_1000:       (f"Aruco6x6x1000", 6, 1000),
    cv2.aruco.DICT_6X6_250:        (f"Aruco6x6x250",  6, 250),
    cv2.aruco.DICT_6X6_100:        (f"Aruco6x6x100",  6, 100),
    cv2.aruco.DICT_6X6_50:         (f"Aruco6x6x50",   6, 50),
    cv2.aruco.DICT_5X5_1000:       (f"Aruco5x5x1000", 5, 1000),
    cv2.aruco.DICT_5X5_250:        (f"Aruco5x5x250",  5, 250),
    cv2.aruco.DICT_5X5_100:        (f"Aruco5x5x100",  5, 100),
    cv2.aruco.DICT_5X5_50:         (f"Aruco5x5x50",   5, 50),
    cv2.aruco.DICT_4X4_1000:       (f"Aruco4x4x1000", 4, 1000),
    cv2.aruco.DICT_4X4_250:        (f"Aruco4x4x250",  4, 250),
    cv2.aruco.DICT_4X4_100:        (f"Aruco4x4x100",  4, 100),
    cv2.aruco.DICT_4X4_50:         (f"Aruco4x4x50",   4, 50),
    cv2.aruco.DICT_ARUCO_ORIGINAL: (f"ArucoOriginal", 5, 1024),
}
DICT = cv2.aruco.DICT_7X7_1000
DICTIONARY_NAME, BITS_PER_SIDE, MAX_ID = MARKER_DICTIONARIES[DICT]
MARKER_DICT = cv2.aruco.getPredefinedDictionary(DICT)

ARUCO_PARAMS = cv2.aruco.DetectorParameters()
ARUCO_PARAMS.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX

OUTPUT_IMAGE_SIZE = (3840*4, 2160*4)
OUTPUT_IMAGE_CENTER = (OUTPUT_IMAGE_SIZE[0] / 2, OUTPUT_IMAGE_SIZE[1] / 2)
