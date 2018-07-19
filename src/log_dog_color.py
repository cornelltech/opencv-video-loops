#!/usr/bin/env python3
"""log_dog_color.py"""

import sys
import numpy
import cv2
from log_dog import LogDog
from video_stream_abc import VideoStreamABC


class LogDogColor(VideoStreamABC):
    """log-dog a frame, show in color"""

    def __init__(self, stream, *args, **kwargs):
        super().__init__(stream, *args, **kwargs)
        self.log_dog = LogDog(None)

    def process_frame(self, frame):
        """log-dog a frame"""
        lab_img = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        (l_img, a_img, b_img) = cv2.split(lab_img)
        l_img = self.log_dog.process_frame(frame)
        l_img = numpy.floor(128.0+(128.0*l_img)).astype('uint8')
        lab_img = cv2.merge([l_img, a_img, b_img])
        return cv2.cvtColor(lab_img, cv2.COLOR_LAB2BGR)


if __name__ == '__main__':
    LogDogColor(sys.argv[1]).start()
