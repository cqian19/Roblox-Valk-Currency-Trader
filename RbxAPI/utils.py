"""A file for misc. helper functions"""
import sys
import os
import math
import cProfile

from functools import wraps

def profile(func):
    """Prints out all calls and times per call in function."""
    pr = cProfile.Profile()
    @wraps(func)
    def do_prof(*args, **kwargs):
        pr.enable()
        res = func(*args, **kwargs)
        pr.disable()
        pr.print_stats()
        return res
    return do_prof

def round_down(num):
    return math.floor(num*1000)/1000.0

def round_up(num):
    return math.ceil(num*1000)/1000.0

def to_num(num):
    """Convert string to int"""
    return int(''.join([s for s in str(num) if s.isdigit()]))

def find_data_file(filename):
    """Find cacert.pem for cx_frozen application using requests"""
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        datadir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(datadir, filename)
