#!/usr/bin/env python3
"""Abstract base class for doing stuff with each frame in a video stream"""

import sys
import abc
from threading import Lock, Thread, Event
import cv2
from fps import FPS
from pacer import Pacer


WINDOW_NAME = 'cam'

class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the is_stopped() condition."""
    def __init__(self, pace=None,  **kwargs):
        super().__init__(**kwargs)
        # self.stop_event: set it to stop the thread
        self._stop_event = Event()
        self.fps = FPS()

        if pace:
            print('pace: ', pace)
            self.pacer = Pacer(pace)
        else:
            self.pacer = None

        self.is_started = False

    def stop(self):
        """Stop thread gracefully"""
        self._stop_event.set()

    def is_stopped(self):
        """Returns true only if we've been started and then stopped"""
        return self._stop_event.isSet()

class VideoStreamABC():
    """Abstract base class for multithreaded OpenCV video streaming"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, stream, full_screen=False, grab_fps=30, proc_fps=30):
        self.stream = stream
        self.frame_lock = Lock()
        self.frame = None
        self.grab_thread = StoppableThread(grab_fps,
                                           target=self.grab_thread_loop)
        self.proc_thread = StoppableThread(proc_fps, 
                                           target=self.proc_thread_loop)

        if full_screen:
            cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN,
                                  cv2.WINDOW_FULLSCREEN)

    def start(self):
        """Start capturing & processing frames"""
        self.grab_thread.start()
        self.proc_thread.start()

    def grab_thread_loop(self):
        """Main loop of thread that continuously grabs video frames"""
        # fps = FPS()
        self.grab_thread.pacer.start()
        self.grab_thread.fps.start()
        while not self.grab_thread.is_stopped():
            (got_it, frame) = self.stream.read()
            if not got_it:
                print('Video stream stopped, ending video grabbing.')
                self.grab_thread.fps.stop()
                print('[GRAB] elasped time: {:.2f}'.format(
                    self.grab_thread.fps.elapsed()))
                print('[GRAB] approx. FPS: {:.2f}'.format(
                    self.grab_thread.fps.fps()))
                print('[GRAB] n_frames: %i' % self.grab_thread.fps.n_frames)
                self.grab_thread.stop()
            self.frame_lock.acquire()
            self.frame = frame
            self.frame_lock.release()
            if self.grab_thread.pacer:
                self.grab_thread.pacer.update()
            self.grab_thread.fps.update()

    def proc_thread_loop(self):
        """Main loop of thread that processes & displays grabbed video frames"""
        # fps = FPS()
        self.proc_thread.pacer.start()
        self.proc_thread.fps.start()
        while not self.grab_thread.is_stopped():
            self.frame_lock.acquire()
            frame = self.frame
            self.frame_lock.release()
            if frame is not None:
                # we process the frame in the next line
                cv2.imshow(WINDOW_NAME, self.process_frame(frame))
                if cv2.waitKey(1) == 27:
                    self.proc_thread.fps.stop()
                    print('[PROC] elasped time: {:.2f}'.format(
                        self.proc_thread.fps.elapsed()))
                    print('[PROC] approx. FPS: {:.2f}'.format(
                        self.proc_thread.fps.fps()))
                    print('[PROC] n_frames: %i' % self.proc_thread.fps.n_frames)
                    self.grab_thread.stop()
                    self.proc_thread.stop()
                    cv2.destroyAllWindows()
                if self.proc_thread.pacer:
                    self.proc_thread.pacer.update()
                self.proc_thread.fps.update()

    @abc.abstractmethod
    def process_frame(self, frame):
        """Abstract method that must be implemented by inherited child class."""
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

    # you can supply whatever stream you want, e.g. the one returned
    # by cv2.VideoCapture(), as long as it has the read() function
    # implemented for getting the next frame and that this function
    # returns two values, as in: (got_it, frame) = stream.read()
    VisualizeOnly(cv2.VideoCapture(sys.argv[1])).start()
