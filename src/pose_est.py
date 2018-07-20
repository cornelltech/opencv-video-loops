#!/usr/bin/env python3

import sys
import cv2
import numpy as np
from gray import Gray
from calib import N_CORNERS, CRITERIA, CALIB_RESULTS_FILENAME, OBJP


AXIS = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

def draw_axes(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img

class CheckerboardPoseEst(Gray):
    """CheckerboardPoseEst(Gray)"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        with np.load(CALIB_RESULTS_FILENAME + '.npz') as X:
            mtx, dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
            self.mtx = mtx
            self.dist = dist
        print('Done loading calibration results...')

    def process_frame(self, frame):
        """Calib"""
        gray = super().process_frame(frame)

        ret, corners = cv2.findChessboardCorners(gray, N_CORNERS, None)

        # if found corners, overlay them on the image
        if ret == True:
            corners_subpix = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), CRITERIA)

            # find the rotation and translation vectors
            res =cv2.solvePnPRansac(OBJP, corners_subpix, self.mtx, self.dist)

            ret, rvecs, tvecs, inliers = cv2.solvePnPRansac(
                OBJP, corners_subpix, self.mtx, self.dist)

            # project 3D points to image plane
            imgpts, jac = cv2.projectPoints(AXIS, rvecs, tvecs,
                                            self.mtx, self.dist)

            frame = draw_axes(frame, corners_subpix, imgpts)

        return frame


if __name__ == "__main__":
    CheckerboardPoseEst(sys.argv[1]).start()
