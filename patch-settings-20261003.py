#!/usr/bin/env python3
"""patch-settings-20261003.py — tambah hook loop-guard ke PreToolUse (idempoten).

Latar: audit 2026-10-03 menemukan limit habis karena LOOP (1.223 pesan/±500 jt
token sehari), bukan ukuran pesan. loop-guard.py menghitung tool call per sesi
dan memperingatkan di 80 (lunak) / 200 atau 500 pesan (keras); 0 byte saat normal.
"""
import json
import os
import shutil
import sys
import time

HOME = os.path.expanduser("~")
GUARD = "python3 " + os.path.join(HOME, ".agents", "loop-guard.py")
STAMP = time.strftime("%Y%m%d")


def patch(path):
    if not os.path.exists(path):
        print("skip (tidak ada):", path)
        return 0
    try:
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception as e:
        print("GAGAL parse", path, e)
        return 1
    groups = cfg.setdefault("hooks", {}).setdefault("PreToolUse", [])
    blob = json.dumps(groups)
    if "loop-guard.py" in blob:
        print("sudah lengkap (tidak diubah):", path)
        return 0
    bak = "%s.bak-%s" % (path, STAMP)
    shutil.copy2(path, bak)
    groups.append({"hooks": [{"type": "command", "command": GUARD, "timeout": 5}]})
    tmp = path + ".tmp%d" % os.getpid()
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)
    try:
        json.load(open(path, encoding="utf-8"))
    except Exception as e:
        shutil.copy2(bak, path)
        print("JSON rusak setelah patch → dikembalikan dari", bak, e)
        return 1
    print("dipatch:", path, "| backup:", bak)
    return 0


if __name__ == "__main__":
    rc = patch(os.path.join(HOME, ".claude", "settings.json"))
    sys.exit(rc)
