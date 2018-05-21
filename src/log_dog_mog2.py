#!/usr/bin/env python3
"""log_dog_mog2.py"""

import sys
import log_dog
import mog2
from video_stream_abc import VideoStreamABC
from video_stream_common import get_stream


LOG_DOG_SCALE_FACTOR = 50

class LogDogMog2(VideoStreamABC):
    """Log-Dog then Mog2"""

    def __init__(self, stream):
        self.log_dog = log_dog.LogDog(None)
        self.mog2 = mog2.Mog2(None)
        super().__init__(stream)

    def process_frame(self, frame):
        """Log-Dog then Mog2"""
        return self.mog2.process_frame(
            128.0+ self.log_dog.process_frame(frame)*LOG_DOG_SCALE_FACTOR)


if __name__ == '__main__':
    LogDogMog2(get_stream(sys.argv[1])).start()
