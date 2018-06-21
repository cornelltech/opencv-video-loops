#!/usr/bin/env python3
"""log_dog_mog2.py"""

import sys
import cv2
import log_dog
import mog2
from video_stream_abc import VideoStreamABC


LOG_DOG_SCALE_FACTOR = 50

class LogDogMog2(VideoStreamABC):
    """Log-Dog then Mog2"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.log_dog = log_dog.LogDog(None)
        self.mog2 = mog2.Mog2(None)

    def process_frame(self, frame):
        """Log-Dog then Mog2"""
        return self.mog2.process_frame(
            128.0+ self.log_dog.process_frame(frame)*LOG_DOG_SCALE_FACTOR)


if __name__ == '__main__':
    LogDogMog2(cv2.VideoCapture(sys.argv[1])).start()
