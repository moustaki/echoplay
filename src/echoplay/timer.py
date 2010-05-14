import time
import threading

class Timer (threading.Thread) :
    _next_tick = 0.0
    def __init__(self, bpm=None, delay=None, signature=4):
        if bpm:
            self._delay = 60.0 / bpm
        elif delay:
            self._delay = delay
        self._signature = signature
        self._is_alive = True
        threading.Thread.__init__(self)
    def run(self):
        print "Starting timer with delay " + str(self._delay) + "s"
        while self._is_alive:
            self._next_tick = time.time() + self._delay
            time.sleep(self._delay)
    def stop(self):
        self._is_alive = False
    def next_beat(self):
        sleep_for = self._next_tick - time.time()
        if sleep_for > 0:
            time.sleep(sleep_for)
        else:
            raise Exception('Next beat is in the past!')
