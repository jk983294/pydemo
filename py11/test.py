import os
import sys
from pathlib import Path
_current_root = str(Path(__file__).resolve().parents[1])
sys.path.append(_current_root + '/cmake-build-debug/lib')
sys.path.append(_current_root + '/install/lib')
sys.path.append(_current_root + '/lib')
import pydemo


if __name__ == '__main__':
    print(pydemo.data_func1([1, 2], [3, 4]))
    print(pydemo.data_func2([1, 2], [3, 4]))