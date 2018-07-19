#!/usr/bin/env python3
"""gray.py"""

import sys
import numpy
import cv2
from video_stream_abc import VideoStreamABC


class Gray(VideoStreamABC):
    """gray each frame"""
    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)

    def process_frame(self, frame):
        """gray frame"""
        if len(frame.shape) < 3:
            return frame
        else:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


if __name__ == '__main__':
    Gray(sys.argv[1]).start()
