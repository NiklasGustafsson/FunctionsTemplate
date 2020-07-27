import json
import sys

from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(ROOT / ".api"))
sys.path.insert(0, str(ROOT))

import Functions
from metadata import generate_metadata

for n in dir(Functions):
    f = getattr(Functions, n)
    if not callable(f):
        continue
    print("-" * 80)
    print("Checking", n)
    try:
        md = generate_metadata(n, f)
    except Exception as ex:
        print("Failed to calculate metadata", ex)
        continue
    print("Metadata:")
    pprint(md)
    try:
        json.dumps(md)
    except Exception as ex:
        print("Failed to dump metadata", ex)
        continue

print("=" * 80)
print("All checks completed")
