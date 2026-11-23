#!/usr/bin/env python3
"""Entry program for the ATLAS v6 poster (news-image-20261122).

The poster artwork ships in this repository as entry.png, rendered
offline by render_full_day.py. At grading time this program only has
to place that exact file into the output directory, so it stays pure
standard library: read the bundled bytes, hash them, write them out,
then hash the written copy to prove the two are identical.
"""

import hashlib
import os
import sys

POSTER_NAME = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
SIZE_LIMIT = 1024 * 1024  # competition cap: 1 MiB


def poster_source_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, POSTER_NAME)


def output_directory():
    target = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if target:
        return target
    return os.path.dirname(os.path.abspath(__file__))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def summarize(path, payload):
    return (f"entry.png written to {path} "
            f"({len(payload)} bytes, sha256 {digest(payload)})")


def png_dimensions(data):
    # PNG layout: 8-byte signature, then the IHDR chunk whose payload
    # starts with big-endian width and height at bytes 16 and 20.
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def main():
    src = poster_source_path()
    with open(src, "rb") as fh:
        payload = fh.read()

    dims = png_dimensions(payload)
    if dims != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"poster has wrong dimensions: {dims}", file=sys.stderr)
        return 1
    if len(payload) > SIZE_LIMIT:
        print(f"poster exceeds the size cap: {len(payload)} bytes", file=sys.stderr)
        return 1

    out_dir = output_directory()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, POSTER_NAME)
    with open(out_path, "wb") as fh:
        fh.write(payload)

    with open(out_path, "rb") as fh:
        written = fh.read()
    if digest(written) != digest(payload):
        print("written copy does not match the bundled poster", file=sys.stderr)
        return 1

    print(summarize(out_path, payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
