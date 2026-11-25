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


def main() -> int:
    line = load_line()
    check_gate(line)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_text(line, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
