#!/usr/bin/env python3
"""knn.py"""

import sys
import cv2
from gray import Gray


class KNN(Gray):
    """KNN background subtraction"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.fgbg = cv2.createBackgroundSubtractorKNN(10, 500.0, False)

    def process_frame(self, frame):
        """KNN background subtraction"""
        gray = super().process_frame(frame)
        return self.fgbg.apply(gray)


if __name__ == '__main__':
    KNN(sys.argv[1]).start()
