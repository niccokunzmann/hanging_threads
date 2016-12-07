import time

from hanging_threads import start_monitoring


if __name__ == '__main__':
    monitoring_thread = start_monitoring(seconds_frozen=1)
    time.sleep(3)
