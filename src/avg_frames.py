#!/usr/bin/env python3
"""avg_frames.py"""

import sys
import numpy
import cv2
from video_stream_abc import VideoStreamABC


ALPHA = 0.1

# Inspired by Abid Rahman's blog:
# opencvpython.blogspot.com/2012/07/background-extraction-using-running.html
# NB: will get big errors after a while if don't normalize each frame

class AvgFrames(VideoStreamABC):
    """average frames"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.avg_frame = None

    def process_frame(self, frame, reset=False):
        """returns avg of all frames after updating with weighted frame"""
        frame = numpy.float32(frame)
        if self.avg_frame is None or reset:
            self.avg_frame = frame
        else:
            self.avg_frame = cv2.accumulateWeighted(frame, self.avg_frame,
                                                    ALPHA)
        return cv2.convertScaleAbs(self.avg_frame)


if __name__ == '__main__':
    AvgFrames(cv2.VideoCapture(sys.argv[1])).start()
