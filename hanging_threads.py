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

__version__ = "2.0.0"
__author__ = "Nicco Kunzmann"


SECONDS_FROZEN = 10  # seconds
TESTS_PER_SECOND = 10


def start_monitoring(seconds_frozen=SECONDS_FROZEN,
                     tests_per_second=TESTS_PER_SECOND):
    """Start monitoring threads

    seconds_frozen - How much time should thread hang to activate printing stack trace - default(10)
    tests_per_second - How much tests per second should be done for hanging threads - default(10)
    """
    thread = StoppableThread(target=monitor, args=(seconds_frozen,
                                                   tests_per_second))
    thread.daemon = True
    thread.start()
    return thread


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


def monitor(seconds_frozen, tests_per_second):
    """Monitoring thread function

    Checks if thread is hanging for time defined by
    seconds_frozen parameter in frequency
    of test_per_second parameter
    """
    current_thread = threading.current_thread()
    hanging_threads = set()
    old_threads = {}  # Threads found on previous iteration.

    while not current_thread.is_stopped():
        new_threads = get_current_frames()

        # Report died threads.
        for thread_id in old_threads.keys():
            if thread_id not in new_threads and thread_id in hanging_threads:
                log_died_thread(thread_id)

        # Process live threads.
        time.sleep(1. / tests_per_second)
        now = time.time()
        then = now - seconds_frozen
        for thread_id, thread_data in new_threads.items():
            # Don't report the monitor thread.
            if thread_id == current_thread.ident:
                continue
            frame = thread_data['frame']
            # If thread is new or it's stack is changed then update time.
            if (thread_id not in old_threads or
                    frame != old_threads[thread_id]['frame']):
                thread_data['time'] = now
                # If the thread was hanging then report awaked thread.
                if thread_id in hanging_threads:
                    hanging_threads.remove(thread_id)
                    log_awaked_thread(thread_id)
            else:
                # If stack is not changed then keep old time.
                last_change_time = old_threads[thread_id]['time']
                thread_data['time'] = last_change_time
                # Check if this is a new hanging thread.
                if (thread_id not in hanging_threads and
                        last_change_time < then):
                    # Gotcha!
                    hanging_threads.add(thread_id)
                    # Report the hanged thread.
                    log_hanged_thread(thread_id, frame)
        old_threads = new_threads


def get_current_frames():
    """Return current threads prepared for further processing"""
    return dict(
        (thread_id, {'frame': thread2list(frame), 'time': None})
        for thread_id, frame in sys._current_frames().items()
    )


def frame2string(frame):
    """Return info about frame

    Keyword arg:
        frame

    Return string in format:

    File {file name}, line {line number}, in {name of parent of code object ?}
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
    """Return list with string frame representation of each frame of thread"""
    l = []
    while frame:
        l.insert(0, frame2string(frame))
        frame = frame.f_back
    return l


def log_hanged_thread(thread_id, frame):
    """Print the stack trace of the deadlock after hanging `seconds_frozen`"""
    write_log('Thread {0} hangs '.format(thread_id), ''.join(frame))


def log_awaked_thread(thread_id):
    write_log('Thread {0} awaked'.format(thread_id))


def log_died_thread(thread_id):
    write_log('Thread {0} died  '.format(thread_id))


def write_log(title, message=''):
    sys.stderr.write(''.join([
        title.center(40).center(60, '-'), '\n', message
    ]))
