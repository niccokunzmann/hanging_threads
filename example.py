import time

from hanging_threads import start_monitoring

def sleep(t):
    time.sleep(t)

if __name__ == '__main__':
    print("Starting the deadlocks monitoring")
    monitoring_thread = start_monitoring(seconds_frozen=1)
    sleep(3)
    time.sleep(2)
    print("Stopping the deadlocks monitoring")
    # This may be useful when working in shell.
    monitoring_thread.stop()
    time.sleep(3)

    print("Exiting")
