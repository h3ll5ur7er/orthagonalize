""" use aruco markers to orthagonalize images """

# pylint: disable=no-member

from typing import Tuple
import numpy as np
import cv2

from orthagonalize.config import ARUCO_PARAMS, MARKER_DICT, OUTPUT_IMAGE_SIZE, OUTPUT_IMAGE_CENTER

ARUCO_DETECTOR = cv2.aruco.ArucoDetector(MARKER_DICT, ARUCO_PARAMS)

def stream(source: str, marker_size_mm: str) -> None:
    """ stream video from source (camera index or video path) """
    if source.isdigit():
        source = int(source)
    cam = cv2.VideoCapture(source)
    running = True
    while running:
        ret, image = cam.read()
        if not ret:
            break
        image, min_x, max_x, min_y, max_y = orthagonalize(image, marker_size_mm)
        image = image[min_y:max_y, min_x:max_x]
        cv2.imshow("image", image)
        key = cv2.waitKey(100)
        if key == ord(" "):
            cv2.imwrite("capture.png", image)
        if key == ord("q"):
            running = False
    cam.release()

def detect_single_marker_corners(img: np.ndarray) -> np.ndarray:
    """ detect marker in image """
    corners, ids, _rejected = ARUCO_DETECTOR.detectMarkers(img)
    if ids is not None and len(ids) > 0:
        return corners[0]
    return None

def project_image_bounds(image: np.ndarray, homography: np.ndarray) -> Tuple[int, int, int, int]:
    """ project corners of image onto plane defined by homography and return clamped bounds """

    height, width, _ = image.shape
    bounds = np.array([[[0., 0.], [width-1., 0.], [width-1., height-1.], [0., height-1.]]])
    projected_bounds = cv2.perspectiveTransform(bounds, homography)

    min_x, max_x = OUTPUT_IMAGE_SIZE[0], 0
    min_y, max_y = OUTPUT_IMAGE_SIZE[1], 0
    for [_x, _y] in projected_bounds[0]:
        min_x = min(min_x, _x)
        min_y = min(min_y, _y)
        max_x = max(max_x, _x)
        max_y = max(max_y, _y)
    min_x = max(int(np.floor(min_x)), 0)
    min_y = max(int(np.floor(min_y)), 0)
    max_x = min(int(np.ceil(max_x)), OUTPUT_IMAGE_SIZE[0]-1)
    max_y = min(int(np.ceil(max_y)), OUTPUT_IMAGE_SIZE[1]-1)


    return int(min_x), int(max_x), int(min_y), int(max_y)

def orthagonalize(image: np.ndarray, marker_size_mm: str) -> None:
    """ orthagonalize image """
    marker_size_mm = int(marker_size_mm)
    marker_size_px = marker_size_mm / 25.4 * 96 # 96 dpi
    marker_offset = marker_size_px / 2
    ortho_points = np.array(
        [[
            [OUTPUT_IMAGE_CENTER[0] - marker_offset, OUTPUT_IMAGE_CENTER[1] - marker_offset],
            [OUTPUT_IMAGE_CENTER[0] + marker_offset, OUTPUT_IMAGE_CENTER[1] - marker_offset],
            [OUTPUT_IMAGE_CENTER[0] + marker_offset, OUTPUT_IMAGE_CENTER[1] + marker_offset],
            [OUTPUT_IMAGE_CENTER[0] - marker_offset, OUTPUT_IMAGE_CENTER[1] + marker_offset]
        ]],
        dtype=np.float32)

    corners = detect_single_marker_corners(image)
    if corners is not None:
        homography, _ = cv2.findHomography(corners, ortho_points)
        min_x, max_x, min_y, max_y = project_image_bounds(image, homography)
        image = cv2.warpPerspective(image, homography, OUTPUT_IMAGE_SIZE)
        return image, min_x, max_x, min_y, max_y
    return image, 0, image.shape[1], 0, image.shape[0]
