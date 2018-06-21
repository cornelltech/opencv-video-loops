#!/usr/bin/env python3
"""mog2.py"""

import sys
import cv2
from gray import Gray


class Mog2(Gray):
    """Mog2 background subtraction"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.fgbg = cv2.createBackgroundSubtractorMOG2()

    def process_frame(self, frame):
        """Mog2 background subtraction"""
        gray = super().process_frame(frame)
        return self.fgbg.apply(gray)


if __name__ == '__main__':
    Mog2(cv2.VideoCapture(sys.argv[1])).start()
