#!/usr/bin/env python3
"""gray.py"""

import sys
import numpy
import cv2
from video_stream_abc import VideoStreamABC
from video_stream_common import get_stream


class Gray(VideoStreamABC):
    """gray each frame"""
    def process_frame(self, frame):
        """gray frame"""
        if numpy.size(frame[0, 0]) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame


if __name__ == '__main__':
    Gray(get_stream(sys.argv[1])).start()
