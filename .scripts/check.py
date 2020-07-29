import json
import sys

from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(ROOT / "api"))
sys.path.insert(0, str(ROOT))

import Functions
from metadata import generate_metadata

exitcode = 0

for n in dir(Functions):
    f = getattr(Functions, n)
    if not callable(f):
        continue
    print("-" * 80)
    print("Checking", n)
    try:
        md = generate_metadata(n, f, tidy=False)
    except Exception as ex:
        print("Failed to calculate metadata", ex)
        exitcode += 1
        continue
    try:
        md = generate_metadata(n, f, tidy=True)
    except Exception as ex:
        print("Failed to calculate tidied metadata", ex)
        exitcode += 1
        continue
    print("Metadata:")
    pprint(md)
    try:
        json.dumps(md)
    except Exception as ex:
        print("Failed to dump metadata", ex)
        exitcode += 1
        continue

print("=" * 80)
print("All checks completed with {} failure(s)".format(exitcode))
sys.exit(exitcode)
