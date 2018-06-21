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
        if numpy.size(frame[0, 0]) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame


if __name__ == '__main__':
    Gray(cv2.VideoCapture(sys.argv[1])).start()
