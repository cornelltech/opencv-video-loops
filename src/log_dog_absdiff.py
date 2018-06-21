#!/usr/bin/env python3
"""log_dog_absdiff.py"""

import sys
import cv2
from log_dog import LogDog
import absdiff


class LogDogAbsDiff(LogDog):
    """Log-Dog then AbsDiff"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.absdiff = absdiff.AbsDiff(None)

    def process_frame(self, frame):
        """Log-Dog then AbsDiff"""
        log_dog = super().process_frame(frame)
        return self.absdiff.process_frame(log_dog)


if __name__ == '__main__':
    LogDogAbsDiff(cv2.VideoCapture(sys.argv[1])).start()
