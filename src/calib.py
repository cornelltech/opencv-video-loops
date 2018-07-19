#!/usr/bin/env python3
"""calib.py - camera calibration from checkerboard"""

import sys
import cv2
import numpy as np
from gray import Gray


N_CORNERS = (7, 7)
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((N_CORNERS[0] * N_CORNERS[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:N_CORNERS[0], 0:N_CORNERS[1]].T.reshape(-1, 2)

obj_pts = []
img_pts = []

class Canny(Gray):
    """Calib"""

    def process_frame(self, frame):
        """Calib"""
        gray = super().process_frame(frame)

        ret, corners = cv2.findChessboardCorners(gray, N_CORNERS, None)

        # if found corners, overlay them on the image
        if ret == True:
            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), CRITERIA)

            cv2.drawChessboardCorners(frame, N_CORNERS, corners, ret)

        return frame


if __name__ == '__main__':
    Canny(sys.argv[1]).start()
