"""A file for misc. helper functions"""
import sys
import os
import math

def round_down(num):
    return math.floor(num*1000)/1000.0


def round_up(num):
    return math.ceil(num*1000)/1000.0


def to_num(num):
    return int(''.join([s for s in str(num) if s.isdigit()]))

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        datadir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(datadir, filename)

def raises_exception(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        return False
    except Exception:
        return True
