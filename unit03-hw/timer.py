#! /usr/bin/env python3

import time

class TimerError(Exception):
    pass

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        if self._start_time is not None:
            raise TimerError("Timer is running, use .stop() to end it!")
        
        self._start_time = time.perf_counter()
    
    def stop(self, sig_figs = 4):
        if self._start_time is None:
            raise TimerError("Timer is not running, use .start() to begin!")
        elapsed = round(time.perf_counter() - self._start_time, sig_figs)
        self._start_time = None
        print(f'Elapsed time: {elapsed} seconds')