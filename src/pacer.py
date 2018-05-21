#!/usr/bin/env python3
"""pacer.py - paced operations"""

import datetime
import time
import unittest
from fps import FPS


class Pacer(object):
    """
    Class to enforce a specific FPS by sleeping, if necessary, between frames
    """
    def __init__(self, desiredFPS):
        """constructor"""
        self.start_time = None
        self.last_update_time = None
        self.desired_period = 1.0/desiredFPS
        self.update_error = 0

    def start(self):
        """call once, before the loop starts"""
        self.start_time = time.time()
        self.last_update_time = self.start_time
        return self

    def update(self):
        """called on each loop iteration, blocks till time is due"""
        now = time.time()
        elapsed = now-self.last_update_time
        delta_time = self.desired_period-elapsed+self.update_error

        if delta_time > 0:
            # too fast, sleep to wait out full period
            self.update_error = delta_time
            time.sleep(delta_time)
        else:
            # too slow, fix the update_error so that next time we sleep less
            self.update_error = 0

        self.last_update_time = now

class ModuleTests(unittest.TestCase):
    """module tests"""
    @staticmethod
    def test01():
        """can we instantiate? """
        fps = FPS().start()
        pacer = Pacer(DESIRED_FPS).start()

        while fps.n_frames < N_TEST_FRAMES:
            print(datetime.datetime.now())
            fps.update()
            pacer.update()

        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        print("[INFO] n_frames: %i" % fps.n_frames)


if __name__ == "__main__":
    N_TEST_FRAMES = 200
    DESIRED_FPS = 40.0

    unittest.main()
