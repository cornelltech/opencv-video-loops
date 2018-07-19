#!/usr/bin/env python3
"""log_dog.py"""

import sys
import cv2
from log import Log


ON_SIZE = 3
OFF_SIZE = 155

class LogDog(Log):
    """log-dog a frame"""

    def process_frame(self, frame):
        """log-dog a frame"""
        log_scaled = super().process_frame(frame)
        blur_on = cv2.GaussianBlur(log_scaled, (ON_SIZE, ON_SIZE), 0)
        blur_off = cv2.GaussianBlur(log_scaled, (OFF_SIZE, OFF_SIZE), 0)
        return blur_on-blur_off


if __name__ == '__main__':
    LogDog(sys.argv[1]).start()
