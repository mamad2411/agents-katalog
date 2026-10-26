#!/usr/bin/env python3
"""Rebuild the mamatagents-branded core binary from the installed opencode.

The opencode v2 binary is a Bun single-file executable. Its TUI logo lives in
two places inside the binary:

  1. the JS source copy (unused at runtime, but kept in sync for tidiness)
  2. the bytecode string table: [u32 len|flag][u32 hash][data][pad to 4]

`flag & 0x80000000` marks an ASCII (1 byte/char) string; otherwise UTF-16LE.
Only the string payload is rewritten, so every length and offset stays intact
and the bytecode never needs relocating.

Run after `opencode upgrade` to re-apply the branding:

    python3 ~/.agents/mamat-reforge.py
"""

import os
import shutil
import subprocess
import sys

SRC = os.path.expanduser("~/.opencode/bin/opencode")
DST = os.path.expanduser("~/.local/share/mamat/bin/mamat-core")

OLD = [
    "                   ",
    "█▀▀█ █▀▀█ █▀▀█ █▀▀▄",
    "█__█ █__█ █^^^ █__█",
    "▀▀▀▀ █▀▀▀ ▀▀▀▀ ▀~~▀",
    "             ▄     ",
    "█▀▀▀ █▀▀█ █▀▀█ █▀▀█",
    "█___ █__█ █__█ █^^^",
    "▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀",
]


# 5x6 sub-pixel font. Each cell is a 2x2 quadrant, so 3 cells x 3 rows gives
# 6x6 sub-pixels per glyph -- enough for clean letterforms at 3 cells wide.
QUAD = {
    (1, 1, 1, 1): "█", (1, 1, 0, 0): "▀", (0, 0, 1, 1): "▄", (1, 0, 1, 0): "▌",
    (0, 1, 0, 1): "▐", (1, 0, 0, 0): "▘", (0, 1, 0, 0): "▝", (0, 0, 1, 0): "▖",
    (0, 0, 0, 1): "▗", (1, 1, 1, 0): "▛", (1, 1, 0, 1): "▜", (1, 0, 1, 1): "▙",
    (0, 1, 1, 1): "▟", (1, 0, 0, 1): "▚", (0, 1, 1, 0): "▞", (0, 0, 0, 0): " ",
}

FONT = {
    "M": ["#...#", "##.##", "#.#.#", "#...#", "#...#", "#...#"],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#"],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", ".###."],
    "E": ["#####", "#....", "####.", "#....", "#....", "#####"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
    "S": [".####", "#....", ".###.", "....#", "....#", "####."],
}
FONT = {k: [r.ljust(6, ".") for r in v] for k, v in FONT.items()}


def glyph(ch):
    g = FONT[ch]
    out = []
    for r in range(3):
        line = ""
        for c in range(3):
            tl, tr, bl, br = (
                1 if g[2 * r + y][2 * c + x] == "#" else 0
                for y, x in ((0, 0), (0, 1), (1, 0), (1, 1))
            )
            line += QUAD[(tl, tr, bl, br)]
        out.append(line)
    return out


def spell(word):
    return ["".join(glyph(c)[r] for c in word) for r in range(3)]


def new_logo():
    left = [("  " + spell("MAMAT")[i] + "  ").ljust(19) for i in range(3)]
    right = [spell("AGENTS")[i].ljust(19) for i in range(3)]
    return [" " * 19] + left + [" " * 19] + right


def parse_table(d, anchor):
    pos = anchor - 8 - (4 + 4 + 19 + 1)
    out = []
    for i in range(8):
        raw = int.from_bytes(d[pos : pos + 4], "little")
        n = raw & 0x7FFFFFFF
        is_ascii = bool(raw & 0x80000000)
        start = pos + 8
        nbytes = n if is_ascii else n * 2
        text = d[start : start + nbytes].decode("ascii" if is_ascii else "utf-16-le")
        out.append((start, n, is_ascii, text))
        nxt = start + nbytes
        pos = nxt + (-nxt) % 4
    return out


def main():
    if not os.path.exists(SRC):
        sys.exit(f"core tidak ada: {SRC}")

    NEW = new_logo()
    for s in NEW:
        assert len(s) == 19, (s, len(s))

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    d = bytearray(open(DST, "rb").read())

    anchor = d.find(OLD[1].encode("utf-16-le"))
    if anchor < 0:
        sys.exit("logo lama tidak ditemukan — versi opencode berubah, patch dilewati")
    entries = parse_table(d, anchor)
    for i, (_, _, _, text) in enumerate(entries):
        if text != OLD[i]:
            sys.exit(f"string tabel #{i} tidak cocok ({text!r}) — patch dilewati")

    for i in range(1, 8):
        start, n, is_ascii, _ = entries[i]
        if is_ascii:
            sys.exit("entri ASCII tak terduga — patch dilewati")
        d[start : start + n * 2] = NEW[i].encode("utf-16-le")

    sm = d.find(b"iC={left:[")
    em = d.find(b"},PR={left:")
    if sm > 0 and em > sm:
        old = bytes(d[sm : em + 1])

        def lit(lines):
            return "[" + ",".join('"' + x + '"' for x in lines) + "]"

        new = ("iC={left:" + lit(NEW[:4]) + ",right:" + lit(NEW[4:]) + "}").encode()
        pad = len(old) - len(new)
        if pad >= 0:
            d[sm : em + 1] = new + b" " * pad

    open(DST, "wb").write(d)
    os.chmod(DST, 0o755)

    subprocess.run(
        ["codesign", "--force", "--sign", "-", DST],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    r = subprocess.run([DST, "--version"], capture_output=True, text=True)
    print(f"reforge ok -> {DST}")
    print((r.stdout or r.stderr).strip()[:80])


if __name__ == "__main__":
    main()
