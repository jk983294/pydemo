from pathlib import Path
import sys
_current_root = str(Path(__file__).resolve().parents[0])
#print(_current_root)
sys.path.append(_current_root)
import pydemo