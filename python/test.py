import errno
import os
import random
import sys
import time
from pathlib import Path
_current_root = str(Path(__file__).resolve().parents[1])
sys.path.append(_current_root + '/cmake-build-debug/lib')
sys.path.append(_current_root + '/install/lib')
sys.path.append(_current_root + '/lib')
import pydemo
from optparse import OptionParser


if __name__ == '__main__':
    a = [1.0, 2.0]
    b = [3.0, 4.0]
    print(pydemo.data_func1(a, b))
    print(pydemo.data_func2(a, b))
