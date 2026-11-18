#!/usr/bin/env python3
"""news-image-20261118 entrypoint (Python 3.13, stdlib only, no network).

Copies the bundled entry.png to /output/entry.png. Fully deterministic:
the same bytes are written on every run.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(DST_DIR, "entry.png")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
