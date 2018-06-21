#!/usr/bin/env python3
"""fps.py - class to measure frames-per-second"""

import datetime
import unittest
import time


class FPS():
    """
    Class to measure frames per second
    """
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self.start_time = None
        self.end_time = None
        self.n_frames = 0

    def start(self):
        """
        Call this to start measuring FPS
        """
        # start the timer
        if self.start_time is None:
            self.start_time = datetime.datetime.now()

        return self

    def stop(self):
        """
        Call this to stop measuring FPS, when you need the result
        """
        # stop the timer
        self.end_time = datetime.datetime.now()

    def update(self):
        """
        Call this once per frame
        """
        # increment the total number of frames examined during the
        # start and end intervals
        self.n_frames += 1

    def elapsed(self):
        """
        Call this only after stop(), returns elapsed time of FPS measurements
        """
        # return the total number of seconds between the start and
        # end interval
        return (self.end_time - self.start_time).total_seconds()

    def fps(self):
        """
        Call this only after stop(), returns FPS (over measured time period)
        """
        # compute the (approximate) frames per second
        return self.n_frames / self.elapsed()

class ModuleTests(unittest.TestCase):
    """
    module tests
    """
    @staticmethod
    def test01():
        """
        can we instantiate?
        """
        print("[INFO] test sleep period: {:.4f}".format(TEST_SLEEP))

        fps = FPS().start()

        while fps.n_frames < N_TEST_FRAMES:
            time.sleep(TEST_SLEEP)
            fps.update()

        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] FPS (has loop overhead): {:.2f}".format(fps.fps()))


if __name__ == "__main__":
    N_TEST_FRAMES = 120
    TEST_FPS = 40.0
    TEST_SLEEP = 1.0/TEST_FPS

    unittest.main()
