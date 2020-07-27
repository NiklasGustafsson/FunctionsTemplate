import sys
from pathlib import Path

ROOT = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(ROOT))

import Functions

for n in dir(Functions):
    f = getattr(Functions, n)
    if not callable(f):
        continue
    print("Checking", n)
