#!/usr/bin/env python3
"""canny.py - video streaming SIFT-like cannyure detection"""

import sys
import cv2
from gray import Gray


class Canny(Gray):
    """Canny: class for video streaming SIFT-like cannyure detection"""

    def process_frame(self, frame):
        """Cannyure detection per frame"""
        gray = super().process_frame(frame)
        return cv2.Canny(gray, 50, 150)


if __name__ == '__main__':
    Canny(sys.argv[1]).start()
