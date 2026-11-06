#!/usr/bin/env python3
"""Rebuild the mamatagents-branded core binary from the installed opencode.

The opencode v2 binary is a Bun single-file executable. Its TUI logo lives in
two places inside the binary:

  1. the JS source copy (unused at runtime, but kept in sync for tidiness)
  2. the bytecode string table: [u32 len|flag][u32 hash][data][pad to 4]

`flag & 0x80000000` marks an ASCII (1 byte/char) string; otherwise UTF-16LE.
Only the string payload is rewritten, so every length and offset stays intact
and the bytecode never needs relocating.

The branded binary is written back to the official install path
(~/.opencode/bin/opencode). Keeping it there is what lets OpenCode's built-in
updater detect the install method: it compares realpath(process.execPath) with
realpath(~/.opencode/bin/opencode). A copy in another directory made that check
fail with "Could not detect the installation method".

Run after `opencode upgrade` to re-apply the branding:

    python3 ~/.agents/mamat-reforge.py
"""

import os
import shutil
import subprocess
import sys

SRC = os.path.expanduser("~/.opencode/bin/opencode")
BACKUP = os.path.expanduser("~/.local/share/mamat/bin/opencode.pristine")
WORK = os.path.expanduser("~/.local/share/mamat/bin/mamat-core.work")
MARKER = os.path.expanduser("~/.local/share/mamat/bin/branded-version")

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


def binary_version(path):
    try:
        r = subprocess.run([path, "--version"], capture_output=True, text=True)
    except OSError:
        return ""
    text = (r.stdout or r.stderr).strip()
    return text.split()[-1] if text else ""


def write_marker(version):
    os.makedirs(os.path.dirname(MARKER), exist_ok=True)
    with open(MARKER, "w", encoding="utf-8") as f:
        f.write(version + "\n")


def main():
    if not os.path.exists(SRC):
        sys.exit(f"core tidak ada: {SRC}")

    NEW = new_logo()
    for s in NEW:
        assert len(s) == 19, (s, len(s))

    d = bytearray(open(SRC, "rb").read())

    # Already branded (e.g. auto-heal ran twice): nothing to patch.
    if NEW[1].encode("utf-16-le") in d:
        write_marker(binary_version(SRC))
        print(f"reforge sudah aktif -> {SRC}")
        return

    # Keep a pristine copy of the official release for rollback/debugging.
    if OLD[1].encode("utf-16-le") in d:
        os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
        with open(BACKUP, "wb") as f:
            f.write(d)

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

    # Build next to the official path, verify, then swap in atomically. Writing
    # directly to SRC would fail when the running executable is SRC.
    os.makedirs(os.path.dirname(WORK), exist_ok=True)
    with open(WORK, "wb") as f:
        f.write(d)
    os.chmod(WORK, 0o755)

    subprocess.run(
        ["codesign", "--force", "--sign", "-", WORK],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if not binary_version(WORK):
        sys.exit("binary hasil patch tidak bisa dijalankan — patch dibatalkan")

    shutil.move(WORK, SRC)
    os.chmod(SRC, 0o755)
    subprocess.run(
        ["codesign", "--force", "--sign", "-", SRC],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    version = binary_version(SRC)
    write_marker(version)
    print(f"reforge ok -> {SRC}")
    print(version)


if __name__ == "__main__":
    main()
