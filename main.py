"""Entrypoint: copy the pre-rendered front page to the output directory.

The image (entry.png, in this same directory) was rendered in advance by
render.py, which documents how it was drawn. This program only copies
those exact bytes to $MAKEFUN_OUTPUT_DIR/entry.png when that variable is
set, or to entry.png in the working directory otherwise. No rendering
happens at runtime: no Pillow, no fonts, no image libraries are needed.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.png")
    else:
        target = "entry.png"
    if os.path.abspath(source) == os.path.abspath(target):
        return
    shutil.copyfile(source, target)


if __name__ == "__main__":
    main()
