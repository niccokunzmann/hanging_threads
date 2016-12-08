import time

from hanging_threads import start_monitoring


if __name__ == '__main__':
    print("Starting the deadlocks monitoring")
    monitoring_thread = start_monitoring(seconds_frozen=1)
    time.sleep(3)

    print("Stopping the deadlocks monitoring")
    # This may be useful when working in shell.
    monitoring_thread.stop()
    time.sleep(3)

    print("Exiting")
