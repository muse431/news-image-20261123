"""news-image-20261123 entrypoint.

Writes the poster to /output/entry.png. The poster itself is a pre-rendered
PNG (poster.png, 1024x1024, under 1 MiB) drawn from poster.html by the
builder's render step; this program just places it where the grader reads it.
Runs with no network.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "poster.png")
DST = "/output/entry.png"


def main() -> int:
    if not os.path.isfile(SRC):
        print("poster.png missing next to main.py", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG (bad magic bytes)", file=sys.stderr)
        return 1
    size = os.path.getsize(DST)
    print(f"wrote {DST} ({size} bytes)")
    if size > 1048576:
        print("entry.png exceeds the 1 MiB limit", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
