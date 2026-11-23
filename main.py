"""news-image-20261123 entrypoint.

Writes the poster to /output/entry.png. The poster is a pre-rendered PNG
(poster.png, 1024x1024, under 1 MiB) drawn by draw_poster.py, a hand-written
PIL program that lays out thirty verified stories from Monday 23 November
2026 as a newspaper front page; this program only places the finished
image where the grader reads it. Runs with no network.
"""

import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "poster.png"
DST = Path("/output/entry.png")

MAX_BYTES = 1_048_576
WANT_WIDTH, WANT_HEIGHT = 1024, 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_dimensions(data: bytes) -> tuple:
    """Read width and height out of a PNG's IHDR chunk."""
    if data[:8] != PNG_MAGIC:
        raise ValueError("not a PNG (bad magic bytes)")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("not a PNG (no IHDR chunk)")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main() -> int:
    if not SRC.is_file():
        print("poster.png missing next to main.py", file=sys.stderr)
        return 1
    data = SRC.read_bytes()
    try:
        width, height = png_dimensions(data)
    except ValueError as exc:
        print(f"poster.png rejected: {exc}", file=sys.stderr)
        return 1
    if (width, height) != (WANT_WIDTH, WANT_HEIGHT):
        print(f"poster.png is {width}x{height}, want "
              f"{WANT_WIDTH}x{WANT_HEIGHT}", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"poster.png is {len(data)} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_bytes(data)
    # Confirm what landed on disk is exactly the bytes we checked.
    written = DST.read_bytes()
    if written != data:
        print("entry.png on disk differs from poster.png", file=sys.stderr)
        return 1
    print(f"wrote {DST} ({len(data)} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
