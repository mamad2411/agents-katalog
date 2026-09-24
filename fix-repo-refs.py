#!/usr/bin/env python3
"""
Perbaiki + bereskan repo-refs
=============================
1. Folder tanpa STUB.md tapi punya README -> bikin STUB.md (jadi berguna).
2. Folder tanpa STUB.md dan tanpa README -> hapus (junk).
3. Laporkan ukuran sebelum/sesudah.

Usage: python3 fix-repo-refs.py [--apply]
       (tanpa --apply = cuma laporan, tidak mengubah apa-apa)
"""

import os
import sys
import shutil
from datetime import datetime

REFS = os.path.expanduser("~/.agents/repo-refs")
READMES = ["README.md", "readme.md", "Readme.md", "README.rst",
           "README", "readme", "README.txt"]
APPLY = "--apply" in sys.argv


def dirsize(path):
    t = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                t += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return t


def main():
    fixed = []
    junk = []
    saved = 0
    for name in sorted(os.listdir(REFS)):
        path = os.path.join(REFS, name)
        if not os.path.isdir(path) or name.startswith("."):
            continue
        if os.path.exists(os.path.join(path, "STUB.md")):
            continue
        readme = None
        for r in READMES:
            p = os.path.join(path, r)
            if os.path.exists(p):
                readme = p
                break
        if readme:
            fixed.append((name, readme))
        else:
            junk.append(name)
            saved += dirsize(path)

    print(f"Repo tanpa STUB.md: {len(fixed) + len(junk)}")
    print(f"  punya README -> diperbaiki: {len(fixed)}")
    print(f"  kosong       -> dihapus    : {len(junk)}"
          f"  ({saved / 1024 / 1024:.1f} MB)")
    for n in junk[:20]:
        print(f"    - {n}")

    if not APPLY:
        print("\n(dry-run — tambahkan --apply untuk eksekusi)")
        return

    for name, readme in fixed:
        try:
            with open(readme, errors="ignore") as f:
                body = f.read()[:4000]
            repo_guess = name.replace("_", "/", 1)
            stub = (f"# {repo_guess}\n\n"
                    f"Source: https://github.com/{repo_guess}\n"
                    f"Fixed: {datetime.now().isoformat()[:10]}\n\n"
                    f"## README\n{body}\n")
            with open(os.path.join(REFS, name, "STUB.md"), "w") as f:
                f.write(stub)
        except OSError:
            pass
    for name in junk:
        shutil.rmtree(os.path.join(REFS, name), ignore_errors=True)

    print(f"\nDIPERBAIKI: {len(fixed)} | DIHAPUS: {len(junk)}"
          f" ({saved / 1024 / 1024:.1f} MB dibebaskan)")


if __name__ == "__main__":
    main()