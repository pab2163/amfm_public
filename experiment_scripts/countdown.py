'''
Author: Paul Bloom
Date: 1/21/2021

-Handles multithreaded countdown timer for AI recall period
-Imported for running music/memory sessions
'''

import threading
import time
import sys


def timer_thread(duration):
    t = threading.currentThread()
    remaining = duration
    while getattr(t, "do_run", True) and remaining > 0:
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
        remaining -=1
    sys.stdout.write("\rComplete!            \n")


# Runs timer_thread function using multithreading to make it interruptable
def countdown_timer(duration):
    t = threading.Thread(target=timer_thread, args=(duration,))
    t.start()
    key = input(' Press enter to advance')
    t.do_run = False
    t.join()
