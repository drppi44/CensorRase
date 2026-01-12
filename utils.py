import time
import logging
import functools


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        logging.info("%s took %.2fs", func.__name__, t1 - t0)
        return result
    return wrapper
