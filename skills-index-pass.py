#!/usr/bin/env python3
"""skills-index-pass — scan + daftarkan skill yang sudah ada di disk tapi belum masuk indeks.

Terjadi kalau crawler mati di tengah jalan (fetch selesai, scan/index tidak).
Idempotent: hanya folder yang namanya belum ada di skills-index.db.

Pakai:
  python3 ~/.agents/skills-index-pass.py            # proses semua
  python3 ~/.agents/skills-index-pass.py --limit 50 # coba dulu
"""
import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
OUT = os.path.join(AG, "skills-expanded")
DB = os.path.join(AG, "skills-index.db")
HUB = os.path.join(AG, "repo-hub.py")

FM_NAME = re.compile(r"^name:\s*[\"']?([\w.-]+)", re.M)
FM_DESC = re.compile(r"^description:\s*[\"']?(.+)$", re.M)


def main():
    a = sys.argv[1:]
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 0
    c = sqlite3.connect(DB, timeout=120, check_same_thread=False)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA busy_timeout=120000")
    have = {r[0] for r in c.execute("SELECT name FROM skills")}
    lock = threading.Lock()
    todo = [d for d in sorted(os.listdir(OUT))
            if os.path.isdir(os.path.join(OUT, d))
            and os.path.exists(os.path.join(OUT, d, "SKILL.md"))
            and d not in have]
    if limit:
        todo = todo[:limit]
    print(f"[pass] {len(todo)} folder belum terindeks", flush=True)

    def work(name):
        p = os.path.join(OUT, name, "SKILL.md")
        r = subprocess.run([sys.executable, HUB, "scan", os.path.join(OUT, name), "--json"],
                           capture_output=True, text=True, timeout=180)
        try:
            findings = json.loads(r.stdout or "[]")
        except Exception:
            findings = []
        if any(f.get("severity") == "critical" for f in findings):
            return ("blocked", name)
        try:
            txt = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            return ("skip", name)
        if len(txt) < 400:
            return ("skip", name)
        low = txt.lower()
        if "used to hold an archived copy" in low or "this page used to hold" in low:
            return ("stub", name)
        m = FM_DESC.search(txt)
        desc = re.sub(r"\s+", " ", m.group(1)).strip()[:200] if m else f"Skill {name}"
        try:
            with lock:
                c.execute("INSERT OR IGNORE INTO skills(name,description,tier,category,path,source) "
                          "VALUES(?,?,?,?,?,?)",
                          (name, desc, "curated", "mined", p, "github/pass"))
            return ("ok", name)
        except Exception as e:
            return ("err:" + str(e)[:60], name)

    stats = {"ok": 0, "blocked": 0, "skip": 0, "stub": 0}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, (st, name) in enumerate(ex.map(work, todo), 1):
            stats[st.split(":")[0]] = stats.get(st.split(":")[0], 0) + 1
            if i % 50 == 0:
                c.commit()
                print(f"  {i}/{len(todo)} · ok={stats['ok']} blocked={stats['blocked']} "
                      f"stub={stats['stub']} skip={stats['skip']}", flush=True)
    c.commit()
    total = c.execute("SELECT count(*) FROM skills WHERE tier<>'junk'").fetchone()[0]
    print(f"[pass] selesai · {stats} · indeks aktif={total}")


if __name__ == "__main__":
    main()
