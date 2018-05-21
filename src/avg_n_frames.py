#!/usr/bin/env python3
"""avg_n_frames.py"""

import sys
import numpy
import cv2
from video_stream_abc import VideoStreamABC
from video_stream_common import get_stream


class AvgNFrames(VideoStreamABC):
    """average n frames"""

    def __init__(self, stream):
        """constructor"""
        self.n_frames = 100
        self.frames = []
        self.avg_frame = None
        super().__init__(stream)

    def process_frame(self, frame):
        """returns average of self.n_frames frames after updating w/frame"""
        frame = numpy.float32(frame)
        self.frames.insert(0, frame)
        if self.avg_frame is None:
            self.avg_frame = frame
        elif len(self.frames) < self.n_frames:
            self.avg_frame = self.avg_frame + frame
        else:
            self.avg_frame = self.avg_frame - self.frames.pop() + frame
        return cv2.convertScaleAbs(self.avg_frame/float(len(self.frames)))


if __name__ == '__main__':
    AvgNFrames(get_stream(sys.argv[1])).start()
