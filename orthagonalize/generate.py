""" generate aruco marker image """

# pylint: disable=no-member

import cv2

from orthagonalize.config import ARUCO_PARAMS, MARKER_DICT, BITS_PER_SIDE, DICTIONARY_NAME

def generate_marker(marker_id: str = "923", pixel_per_bit: str = "254") -> None:
    """ generate marker image and save to file """
    marker_id = int(marker_id)
    pixel_per_bit = int(pixel_per_bit)
    size = (ARUCO_PARAMS.markerBorderBits * 2 + BITS_PER_SIDE) * pixel_per_bit
    marker = cv2.aruco.generateImageMarker(MARKER_DICT, marker_id, size)
    cv2.imwrite(f"{DICTIONARY_NAME}_{marker_id}.png", marker)
    cv2.imshow("marker", marker)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
