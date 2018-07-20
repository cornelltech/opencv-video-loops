#!/usr/bin/env python3
"""calib.py - camera calibration from checkerboard"""

import sys
import cv2
import numpy as np
from gray import Gray


N_CORNERS = (9, 7)
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
CALIB_RESULTS_FILENAME = 'calib'
OBJP = np.zeros((N_CORNERS[0] * N_CORNERS[1], 3), np.float32)
OBJP[:, :2] = np.mgrid[0:N_CORNERS[0], 0:N_CORNERS[1]].T.reshape(-1, 2)

class Canny(Gray):
    """Calib"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.accum_obj_pts = []
        self.accum_img_pts = []
        self.gray_shape = 0

    def process_frame(self, frame):
        """Calib"""
        gray = super().process_frame(frame)

        if self.processed_frame_num() == 0:
            self.gray_shape = gray.shape[::-1]

        ret, corners = cv2.findChessboardCorners(gray, N_CORNERS, None)

        # if found corners, overlay them on the image
        if ret == True:
            self.accum_obj_pts.append(OBJP)
            corners_subpix = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), CRITERIA)
            self.accum_img_pts.append(corners_subpix)
            cv2.drawChessboardCorners(frame, N_CORNERS, corners, ret)

        return frame

    def stop(self):
        print('Computing camera calibration using %d measurements ...' %
              len(self.accum_obj_pts))
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            self.accum_obj_pts, self.accum_img_pts, self.gray_shape, None, None)

        np.savez(CALIB_RESULTS_FILENAME,
                 mtx = mtx, dist = dist, rvecs = rvecs, tvecs = tvecs)

        super().stop()

if __name__ == '__main__':
    Canny(sys.argv[1]).start()
