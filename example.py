import time

from hanging_threads import start_monitoring

def sleep(t):
    time.sleep(t)

if __name__ == '__main__':
    print("Starting the deadlocks monitoring")
    monitoring_thread = start_monitoring(seconds_frozen=1)
    print("Sleep 3 seconds in custom func")
    sleep(3)
    print("Sleep 3 seconds")
    time.sleep(3)
    print("Sleep 3 seconds")
    time.sleep(3)

    print("Stopping the deadlocks monitoring")
    # This may be useful when working in shell.
    monitoring_thread.stop()
    print("Sleep 3 seconds")
    time.sleep(3)
    print("Sleep 3 seconds")
    time.sleep(3)

    print("Exiting")
