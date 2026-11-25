#!/usr/bin/env python3
"""Writes the entry line for the 'Have You Tried Turning It Off?' bounty.

Reads the line from line.txt sitting next to this script, validates it
against the competition gate (UTF-8, 1-199 characters, single line, not
only whitespace), and writes it verbatim to entry.txt in the output
directory (MAKEFUN_OUTPUT_DIR if set, otherwise /output).
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 199


def load_line() -> str:
    path = Path(__file__).resolve().parent / "line.txt"
    text = path.read_text(encoding="utf-8")
    return text.strip("\n").rstrip("\r")


def check_gate(text: str) -> None:
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"line has {len(text)} characters, gate allows 1-{MAX_CHARS}")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if not text.strip():
        raise ValueError("line must not be only whitespace")
    text.encode("utf-8")  # raises if not encodable


def write_entry(out_dir: Path, line: str) -> None:
    """Write via a temp file in the same directory, then rename atomically.

    A plain write can leave a half-written entry.txt if the process dies
    mid-write; renaming a fully written temp file means entry.txt is
    either the old complete text or the new complete text, never a torn
    mix. The temp name is unique per process so two runs cannot collide.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = out_dir / f".entry.txt.tmp-{os.getpid()}"
    try:
        tmp.write_text(line, encoding="utf-8")
        os.replace(tmp, out_dir / "entry.txt")
    finally:
        tmp.unlink(missing_ok=True)


def main() -> int:
    line = load_line()
    check_gate(line)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    write_entry(out_dir, line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
