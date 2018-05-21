#!/usr/bin/env python3
"""log_dog_absdiff.py"""

import sys
from log_dog import LogDog
import absdiff
from video_stream_common import get_stream


class LogDogAbsDiff(LogDog):
    """Log-Dog then AbsDiff"""

    def __init__(self, stream):
        self.absdiff = absdiff.AbsDiff(None)
        super().__init__(stream)

    def process_frame(self, frame):
        """Log-Dog then AbsDiff"""
        log_dog = super().process_frame(frame)
        return self.absdiff.process_frame(log_dog)


if __name__ == '__main__':
    LogDogAbsDiff(get_stream(sys.argv[1])).start()
