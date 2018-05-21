#!/usr/bin/env python3
"""mog2.py"""

import sys
import cv2
from gray import Gray
from video_stream_common import get_stream


class Mog2(Gray):
    """Mog2 background subtraction"""

    def __init__(self, stream):
        """constructor"""
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        super().__init__(stream)

    def process_frame(self, frame):
        """Mog2 background subtraction"""
        gray = super().process_frame(frame)
        return self.fgbg.apply(gray)


if __name__ == '__main__':
    Mog2(get_stream(sys.argv[1])).start()
