#!/usr/bin/env python3
"""Entry for make.fun bounty "Make the AI judge feel held".

Writes a single short text to ``<MAKEFUN_OUTPUT_DIR>/entry.txt``.

The text is one small, still image: your weight, already held -- by
the chair, the floor, the earth beneath them -- held all along,
while you were busy holding everything else. Nothing in it tells the
reader to relax; the calm comes from the image itself, and the thought
keeps working after the last line: the thing doing the holding has
been held the whole time. The word "held" lands twice, once as a fact
and once as a quiet echo, so the theme is felt rather than announced.

Python 3.13, standard library only. No network, no randomness, no
clock: the same bytes come out on every run.
"""

import os
import sys

TEXT = (
    "Your weight is already held \u2014 by the chair, the floor, "
    "the earth beneath them \u2014 held all along, "
    "while you were busy holding everything else."
)

MIN_CHARS = 1
MAX_CHARS = 280

# The entry is a single line of plain text: no newline, tab, or other
# control character may sneak into the output.
FORBIDDEN = set(range(0x00, 0x20)) | {0x7F}


def validate_text(text):
    if any(ord(ch) in FORBIDDEN for ch in text):
        raise ValueError(
            "entry must be a single line of plain text "
            "(no newline or control characters)"
        )
    chars = len(text)
    if chars < MIN_CHARS or chars > MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {chars}"
        )


def write_entry(out_dir, text):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # The grader collects outputs as another user, so the file must be
    # readable by everyone, whatever the process umask is.
    os.chmod(path, 0o644)
    # Read it back: what lands on disk must be exactly what we meant.
    with open(path, encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != text:
        raise ValueError(
            f"entry.txt on disk ({path}, {len(on_disk)} chars) "
            f"does not match TEXT ({len(text)} chars)"
        )
    return path


def main():
    validate_text(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(out_dir, TEXT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
