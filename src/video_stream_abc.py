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
    regularly for the stopped() condition."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        """Gracefully stop the threads"""
        self._stop_event.set()

    def is_stopped(self):
        """Returns true only if we've been started and then stopped"""
        return self._stop_event.isSet()

class VideoStreamABC():
    """Abstract base class for multithreaded OpenCV video streaming"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, stream, full_screen=False, desired_fps=30):
        """Constructor"""
        self.stream = stream
        self.desired_fps = desired_fps
        self.frame_lock = Lock()
        self.frame = None
        self.grab_thread = StoppableThread(target=self.grab_thread_loop)
        self.proc_thread = StoppableThread(target=self.proc_thread_loop)
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
        fps = FPS()
        fps.start()
        while not self.grab_thread.is_stopped():
            (got_it, frame) = self.stream.read()
            if not got_it:
                print('Video stream stopped, ending video grabbing.')
                self.grab_thread.stop()
            self.frame_lock.acquire()
            self.frame = frame
            self.frame_lock.release()
            fps.update()
            if self.desired_fps:
                pacer.update()

        fps.stop()
        print('[GRAB] elasped time: {:.2f}'.format(fps.elapsed()))
        print('[GRAB] approx. FPS: {:.2f}'.format(fps.fps()))
        print('[GRAB] n_frames: %i' % fps.n_frames)


    def proc_thread_loop(self):
        """Main loop of thread that processes & displays grabbed video frames"""
        if self.desired_fps:
            pacer = Pacer(self.desired_fps)
            pacer.start()
        fps = FPS()
        fps.start()
        while not self.grab_thread.is_stopped():
            self.frame_lock.acquire()
            frame = self.frame
            self.frame_lock.release()
            if frame is not None:
                cv2.imshow(WINDOW_NAME, self.process_frame(frame))
                if cv2.waitKey(1) == 27:
                    self.grab_thread.stop()
                    self.proc_thread.stop()
                    fps.stop()
                    print('[PROC] elasped time: {:.2f}'.format(fps.elapsed()))
                    print('[PROC] approx. FPS: {:.2f}'.format(fps.fps()))
                    print('[PROC] n_frames: %i' % fps.n_frames)
                    cv2.destroyAllWindows()
                fps.update()
            if self.desired_fps:
                pacer.update()

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
    VisualizeOnly(cv2.VideoCapture(sys.argv[1])).start()
