#!/usr/bin/env python3
"""Common video utility functions"""

import sys
from pathlib import Path
import cv2


def get_stream(arg):
    """Return a cv2 video stream, based on the input argument 'arg'"""
    try:
        print('Capturing video from USB camera # %s' % arg)
        arg = int(arg)
    except ValueError:
        file = Path(arg)
        if file.is_file():
            print('Capturing video from file %s' % arg)
        else:
            print('Capturing video from URL %s' % arg)

    return cv2.VideoCapture(arg)


if __name__ == '__main__':
    get_stream(sys.argv[1])
