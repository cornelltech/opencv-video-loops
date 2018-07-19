#!/usr/bin/env python3
"""canny.py - video streaming SIFT-like cannyure detection"""

import sys
import cv2
import numpy as np
from gray import Gray

# distance resolution of accumulator, in pixels
HOUGH_RHO = 1
# angle resolution of accumulator, in radians
HOUGH_THETA = np.pi/180
# min number of votes required in accumulator
HOUGH_THRESH = 10
# min line length allowed
MIN_LINE_LENGTH = 5
# max gap between lines
MAX_LINE_GAP = 20


class Canny(Gray):
    """Canny: class for video streaming SIFT-like cannyure detection"""

    def process_frame(self, frame):
        """Cannyure detection per frame"""
        result = np.zeros(frame.shape)
        edges = cv2.Canny(frame, 50, 150)
        lines = cv2.HoughLinesP(edges, HOUGH_RHO, HOUGH_THETA, HOUGH_THRESH,
                                MIN_LINE_LENGTH, MAX_LINE_GAP)

        if lines is None:
            return result

        for x1, y1, x2, y2 in lines[0]:
            i += 1
            cv2.line(result, (x1, y1), (x2, y2), (255, 0, 0), 1)

        return result


if __name__ == '__main__':
    Canny(sys.argv[1]).start()
