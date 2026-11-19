"""Entry program for the make.fun news-image-20261119 contest.

Copies the pre-drawn front page (assets/entry.png, drawn by
tools/render.py with Pillow primitives) to the output directory.
Standard library only; no network, no randomness, no timestamps, so
both runs write identical bytes.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "assets" / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out_dir / "entry.png")


if __name__ == "__main__":
    main()
