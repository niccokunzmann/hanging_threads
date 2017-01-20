#!/usr/bin/python
"""

Copy this code and do

    import hanging_threads

If a thread is at the same place for SECONDS_FROZEN then the stacktrace is printed.

This script prints

--------------------    Thread 6628     --------------------
  File "hanging_threads.py", line 70, in <module>
        time.sleep(3) # TEST
--------------------    Thread 6628     --------------------
  File "hanging_threads.py", line 70, in <module>
        time.sleep(3) # TEST

"""
import sys
import threading
try:
    try:
        from threading import _get_ident as get_ident
    except ImportError:
        from threading import get_ident
except ImportError:
    from thread import get_ident
import linecache
import time

__version__ = "1.0.1"
__author__ = "Nicco Kunzmann"


SECONDS_FROZEN = 10  # seconds
TESTS_PER_SECOND = 10


class StoppableThread(threading.Thread):
    """
    Thread class with a stop() method.
    The thread itself has to check regularly for the is_stopped() condition.
    """
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stopped = False

    def stop(self):
        self._stopped = True

    def is_stopped(self):
        return self._stopped


def frame2string(frame):
    """Return info about frame

    Keyword arg:
        frame

    Return string in format:

    File {filename}, line {line number}, in {name of parent of code object ?}
    Line from file at line number

    """
    lineno = frame.f_lineno  # or f_lasti
    co = frame.f_code
    filename = co.co_filename
    name = co.co_name
    s = '  File "{0}", line {1}, in {2}'.format(filename, lineno, name)
    line = linecache.getline(filename, lineno, frame.f_globals).lstrip()
    return s + '\n\t' + line


def thread2list(frame):
    """Return list of string frame representation for each fream of thread"""
    l = []
    while frame:
        l.insert(0, frame2string(frame))
        frame = frame.f_back
    return l


def monitor(seconds_frozen, tests_per_second):
    """Monitoring thread function

    Checks if thread is hanging for time defined by
    seconds_frozen parameter in frequency
    of test_per_second parameter
    """
    current_thread = threading.current_thread()
    self = get_ident()
    old_threads = {}
    while not current_thread.is_stopped():
        time.sleep(1. / tests_per_second)
        now = time.time()
        then = now - seconds_frozen
        frames = sys._current_frames()
        new_threads = {}
        for frame_id, frame in frames.items():
            new_threads[frame_id] = thread2list(frame)
        for thread_id, frame_list in new_threads.items():
            if thread_id == self: continue
            if thread_id not in old_threads or \
               frame_list != old_threads[thread_id][0]:
                new_threads[thread_id] = (frame_list, now)
            elif old_threads[thread_id][1] < then:
                print_frame_list(frame_list, thread_id)
            else:
                new_threads[thread_id] = old_threads[thread_id]
        old_threads = new_threads


def print_frame_list(frame_list, frame_id):
    """Print the stack trace of the deadlock after hanging `seconds_frozen`"""
    sys.stderr.write('-' * 20 + 
                     'Thread {0}'.format(frame_id).center(20) +
                     '-' * 20 +
                     '\n' + 
                     ''.join(frame_list))


def start_monitoring(seconds_frozen=SECONDS_FROZEN,
                     tests_per_second=TESTS_PER_SECOND):
    """Start monitoring thread

    seconds_frozen - How much time should thread hang to activate printing stack trace - default(10)
    tests_per_second - How much tests per second should be done for hanging threads - default(10)
    """
    thread = StoppableThread(target=monitor, args=(seconds_frozen,
                                                   tests_per_second))
    thread.daemon = True
    thread.start()
    return thread
