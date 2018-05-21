#!/usr/bin/env python3
"""log.py"""

import sys
import numpy
import cv2
from gray import Gray
from video_stream_common import get_stream


# This is an example of composing two process_frame functions
# by inheriting from a class that has one: superclass is Gray
# and this class is Log - we take the logarithm of a grayscale
# version of each frame

LOG_FACTOR = 3

class Log(Gray):
    """log a frame"""

    def process_frame(self, frame):
        """log a frame"""
        # first convert to gray by calling process_frame() of superclass
        gray = super().process_frame(frame)
        #pylint: disable=unused-variable
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)
        #pylint: enable=unused-variable
        log_scaled = numpy.log(1+LOG_FACTOR*(gray-min_val)/(max_val-min_val))
        return log_scaled


if __name__ == '__main__':
    Log(get_stream(sys.argv[1])).start()
