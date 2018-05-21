#!/usr/bin/env python3
"""knn.py"""

import sys
import cv2
from gray import Gray
from video_stream_common import get_stream


class KNN(Gray):
    """KNN background subtraction"""

    def __init__(self, stream):
        """constructor"""
        self.fgbg = cv2.createBackgroundSubtractorKNN(10, 500.0, False)
        super().__init__(stream)

    def process_frame(self, frame):
        """KNN background subtraction"""
        gray = super().process_frame(frame)
        return self.fgbg.apply(gray)


if __name__ == '__main__':
    KNN(get_stream(sys.argv[1])).start()
