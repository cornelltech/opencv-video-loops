#!/usr/bin/env python3
"""feat.py - video streaming SIFT-like feature detection"""

import sys
import cv2
# from gray import Gray
from log_dog import LogDog

class Feat(LogDog):
    """Feat: class for video streaming SIFT-like feature detection"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.orb = cv2.ORB_create(
            nfeatures = 500,
            nlevels = 8,
            scaleFactor = 1.2
        )

    def process_frame(self, frame):
        """Feature detection per frame"""
        (keypoints, descs) = self.orb.detectAndCompute(frame, None)
        res = cv2.drawKeypoints(frame, keypoints, None)
        return res


if __name__ == '__main__':
    Feat(sys.argv[1]).start()
