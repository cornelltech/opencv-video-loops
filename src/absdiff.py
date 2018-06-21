#!/usr/bin/env python3
"""absdiff.py"""

import sys
import cv2
from gray import Gray


class AbsDiff(Gray):
    """absolute value of (current_frame - previous_frame)"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.prev_frame = None

    def process_frame(self, frame):
        """returns diff"""
        gray = super().process_frame(frame)
        if self.prev_frame is None:
            result = gray
        else:
            result = cv2.absdiff(gray, self.prev_frame)
        self.prev_frame = gray
        return result


if __name__ == '__main__':
    AbsDiff(cv2.VideoCapture(sys.argv[1])).start()
