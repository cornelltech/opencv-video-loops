#!/usr/bin/env python3
"""feat.py - video streaming SIFT-like feature detection"""

import sys
import cv2
from gray import Gray


class Feat(Gray):
    """Feat: class for video streaming SIFT-like feature detection"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        if 'method' in kwargs:
            print('method: ', method)

    def process_frame(self, frame):
        """KNN background subtraction"""
        return frame


if __name__ == '__main__':
    Feat(sys.argv[1]).start()
