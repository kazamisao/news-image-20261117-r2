"""Entry program for news-image-20261117, round 2 (stdlib only).

The picture lives beside this file as news.png: a one-page illustrated
broadsheet of the world news of Tuesday, 17 November 2026, drawn by
render.py — a hero panel on the Kerch Bridge strike, six panels on
Hormuz, Zaporizhzhia, the Gaza aid call, COP31, US measles and Trump in
Manila, and an "Also today" strip with five more stories.

This program only delivers those bytes, untouched, to the output path.
No network, same bytes on every run.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "news.png")
LIMIT = 1048576  # the gate's 1 MiB cap


def target_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.png")


def main():
    if os.path.getsize(SOURCE) > LIMIT:
        raise SystemExit("news.png exceeds the 1 MiB entry limit")
    target = target_path()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(SOURCE, target)
    if os.path.getsize(target) != os.path.getsize(SOURCE):
        raise SystemExit("entry.png copy is incomplete")


if __name__ == "__main__":
    main()
