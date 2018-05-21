#!/usr/bin/env python3
"""Abstract base class for doing stuff with each frame in a video stream"""

import sys
import abc
from threading import Lock, Thread
import cv2
from fps import FPS
from pacer import Pacer
from video_stream_common import get_stream


class VideoStreamABC():
    """Abstract base class for multithreaded OpenCV video streaming"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, stream, desired_fps=30):
        """Constructor"""
        self.stream = stream
        self.desired_fps = desired_fps
        self.grab_thread = Thread(target=self.grab_thread_loop)
        self.proc_thread = Thread(target=self.proc_thread_loop)
        self.frame_lock = Lock()
        self.frame = None
        self.looping = False

    def start(self):
        """Start capturing & processing frames"""
        if self.is_running():
            raise Exception('Cannot start, already running')
        self.looping = True
        self.grab_thread.start()
        self.proc_thread.start()

    def stop(self):
        """Stop capturing & processing frames"""
        self.looping = False
        self.stream.release()
        cv2.destroyAllWindows()

    def grab_thread_loop(self):
        """Main loop of thread that continuously grabs video frames"""
        fps = FPS()
        fps.start()
        while self.looping:
            (got_it, frame) = self.stream.read()
            if not got_it:
                print('Video stream stopped')
                break
            self.frame_lock.acquire()
            self.frame = frame
            self.frame_lock.release()
            fps.update()
        fps.stop()
        print('[GRAB] elasped time: {:.2f}'.format(fps.elapsed()))
        print('[GRAB] approx. FPS: {:.2f}'.format(fps.fps()))
        print('[GRAB] n_frames: %i' % fps.n_frames)

    def proc_thread_loop(self):
        """Main loop of thread that processes grabbed video frames"""
        if self.desired_fps:
            pacer = Pacer(self.desired_fps)
            pacer.start()
        fps = FPS()
        fps.start()
        while self.looping:

            self.frame_lock.acquire()
            frame = self.frame
            self.frame_lock.release()

            if frame is not None:
                cv2.imshow('cam', self.process_frame(frame))
                if cv2.waitKey(1) == 27:
                    self.stop()
                fps.update()

            if self.desired_fps:
                pacer.update()

        fps.stop()

        print('[PROC] elasped time: {:.2f}'.format(fps.elapsed()))
        print('[PROC] approx. FPS: {:.2f}'.format(fps.fps()))
        print('[PROC] n_frames: %i' % fps.n_frames)

    def is_running(self):
        """Returns whether both threads are still alive"""
        return self.grab_thread.isAlive() or self.proc_thread.isAlive()

    @abc.abstractmethod
    def process_frame(self, frame):
        """
        Abstract method that must be implemented for various streams
        that inherit from this base class.

        This method reads new frames every time it is called and sets
        self.frame to a new frame it just read.

        This method also detects the end of stream (e.g. EOF when streaming
        from a file and stops the thread upon such detection.

        This method works in conjunction with the constructor - its
        initialization happens there.
        """
        raise Exception('Abstract method process_frame() not implemented!')

if __name__ == '__main__':
    # To create a class that does something with each video frame,
    # create a class that inerits from VideoStreamABC and has one
    # method: 'processs_frame', which takes a single argument 'frame'
    # and does whatever it wants with it, but it must return an image
    # of the same dimensions as 'frame'. This example class
    # 'VisualizeOnly' is just for visualization, i.e. it returns
    # 'frame' as is. It quits when the user hits the ESC key.
    class VisualizeOnly(VideoStreamABC):
        """Class to show video frames using imshow()"""
        def process_frame(self, frame):
            return frame

    # you can supply whatever stream you want to the constructor, as long as
    # it has the read() function implemented, to get the next frame, and that
    # this function returns two values, as in: (got_it, frame) = stream.read()
    VisualizeOnly(get_stream(sys.argv[1])).start()
