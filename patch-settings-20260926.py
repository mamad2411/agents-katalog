#!/usr/bin/env python3
"""patch-settings-20260926.py — tambah hook context-guard + deny read (idempoten).

Dijalankan sekali; aman diulang (kalau sudah ada, tidak menambah dua kali).
Mekanisme deny = resmi docs Claude Code (large-codebases): permissions.deny
dengan pola Read(./**/vendor/**).
"""
import json
import os
import shutil
import sys
import time

HOME = os.path.expanduser("~")
GUARD = 'bash %s/.agents/context-guard.sh' % HOME
DENY = [
    "Read(./**/vendor/**)",
    "Read(./**/node_modules/**)",
    "Read(./**/dist/**)",
    "Read(./**/public/template/**)",
    "Read(./**/skills-expanded/**)",
    "Read(./**/*.min.js)",
]


def patch(path, add_hooks, add_deny, create=False):
    if not os.path.exists(path):
        if not create:
            print("skip (tidak ada):", path)
            return 0
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cfg = {}
        print("dibuat baru:", path)
    else:
        raw = open(path).read()
        try:
            cfg = json.loads(raw)
        except Exception as e:
            print("GAGAL parse", path, e)
            return 1
    changed = []

    if add_hooks:
        hooks = cfg.setdefault("hooks", {})
        for ev in ("SessionStart", "UserPromptSubmit"):
            groups = hooks.setdefault(ev, [])
            sudah = any("context-guard.sh" in (h.get("command") or "")
                        for g in groups for h in g.get("hooks", []))
            if sudah:
                continue
            groups.append({"hooks": [{"type": "command", "command": GUARD, "timeout": 5}]})
            changed.append("hook:" + ev)

    if add_deny:
        perms = cfg.setdefault("permissions", {})
        deny = perms.setdefault("deny", [])
        for rule in DENY:
            if rule not in deny:
                deny.append(rule)
                changed.append("deny:" + rule)

    if not changed:
        print("sudah lengkap (tidak diubah):", path)
        return 0
    bak = "%s.bak-%s" % (path, time.strftime("%Y%m%d"))
    if os.path.exists(path):
        shutil.copy2(path, bak)
    tmp = path + ".tmp%d" % os.getpid()
    with open(tmp, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)
    # validasi wajib: kalau rusak, kembalikan backup
    try:
        json.load(open(path))
    except Exception as e:
        shutil.copy2(bak, path)
        print("JSON rusak setelah patch → dikembalikan dari", bak, e)
        return 1
    print("dipatch:", path, "| backup:", bak)
    for c in changed:
        print("   +", c)
    return 0


if __name__ == "__main__":
    rc = patch(os.path.join(HOME, ".claude", "settings.json"), True, True)
    rc |= patch("/Users/chaali0324/receptor/.claude/settings.json", False, True, create=True)
    sys.exit(rc)
