import logging as log
from threading import Condition, Lock


log.getLogger(__name__)


class ThreadWarden:
    """
    Maintains references to the locks that are used to control the
        execution of threads.
    """

    def __init__(self):
        self.num_readers: int = 0
        self.num_writers: int = 0
        self.reader_lock: Lock = Lock()
        self.writer_lock: Lock = Lock()
        self.reader_cv: Condition = Condition(lock=self.reader_lock)
        self.writer_cv: Condition = Condition(lock=self.writer_lock)

    def acquire_reader_lock(self) -> None:
        """
        Function to acquire the reader lock if there are no active readers
            or writers.
        """
        with self.reader_cv:
            while self.num_readers or self.num_writers:
                self.reader_cv.wait()
            self.num_readers += 1

        return

    def acquire_writer_lock(self) -> None:
        """
        Function to acquire the writer lock if there are no active readers
            or writers.
        """
        # Acquire the writer lock and await signal.
        with self.writer_cv:

            # Fall through, only if there are no active readers or writers.
            while self.num_readers or self.num_writers:
                self.writer_cv.wait()

            # * Enter mutual exclusion zone.
            self.num_writers += 1  # Lock

        return

    def notify_threads(self) -> None:
        """
        Function to notify any threads waiting to be signaled.
        """
        # Signal any threads waiting to run.
        with self.writer_cv:
            self.writer_cv.notify()

        with self.reader_cv:
            self.reader_cv.notify()

        return

    def release_reader_lock(self) -> None:
        """
        Function to release the reader lock and notify both reader and
            writer threads.
        """
        # * End of mutual exclusion zone.
        # Signal any threads waiting to run.
        with self.reader_cv:
            self.num_readers -= 1
            self.reader_cv.notify()

        with self.writer_cv:
            self.writer_cv.notify()

        return

    def release_writer_lock(self) -> None:
        """
        Function to release the writer lock and notify both reader and
            writer threads.
        """
        # * Exit mutual exclusion zone.
        # Signal any threads waiting to run.
        with self.writer_cv:
            self.num_writers -= 1  # Unlock
            self.writer_cv.notify()

        with self.reader_cv:
            self.reader_cv.notify()

        return


##########################################################################
###########################   THREAD WARDEN   ############################
##########################################################################


THREAD_WARDEN: ThreadWarden = ThreadWarden()


##########################################################################
##############################   GETTERS   ###############################
##########################################################################


def get_thread_warden() -> ThreadWarden:
    """
    Function that returns a reference to the global THREAD_WARDEN variable
        to other parts of the program.

    Returns:
        ThreadWarden: Object that controls the execution of threads within
            the application.
    """
    return THREAD_WARDEN
