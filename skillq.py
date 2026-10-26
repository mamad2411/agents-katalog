#!/usr/bin/env python3
"""skillq — cari skill di katalog lokal, output padat (0 tool MCP).
Pakai: skillq.py "kata kunci" [-n 5]   |   skillq.py -l <nama>   (cetak SKILL.md)
"""
import sqlite3, sys, os, re

DB = os.path.expanduser("~/.agents/skills-index.db")
STOP = set("yang dan dengan untuk dari pada ini itu saya mau bikin buat tolong bisa gimana cara agar supaya the and for with using use add create make new how please want need into that this from a an of to in on".split())

def terms(q):
    w = [t for t in re.findall(r"[\w./+-]+", q.lower()) if t not in STOP and len(t) > 1]
    return w or [q.lower()]

def main():
    a = sys.argv[1:]
    if not a:
        sys.exit('pakai: skillq.py "kata" [-n 5] | skillq.py -l <nama>')
    if a[0] in ("-l", "--load"):
        name = a[1]
        c = sqlite3.connect(DB)
        r = c.execute("SELECT path FROM skills WHERE name=? LIMIT 1", (name,)).fetchone()
        if not r:
            r = c.execute("SELECT path FROM skills WHERE name LIKE ? LIMIT 1", (f"%{name}%",)).fetchone()
        if not r:
            sys.exit(f"tidak ada skill '{name}'")
        with open(r[0], encoding="utf-8", errors="ignore") as f:
            print("".join(f.readlines()[:90]))
        return
    n = 5
    if "-n" in a:
        i = a.index("-n"); n = int(a[i+1]); a = a[:i] + a[i+2:]
    q = " ".join(a)
    c = sqlite3.connect(DB)
    rows = []
    order = "bm25(skills) + (CASE WHEN tier = 'curated' THEN 0.0 ELSE 0.8 END)"
    for joiner in (" AND ", " OR "):
        try:
            fts = joiner.join(terms(q))
            rows = c.execute(
                "SELECT name, COALESCE(category,''), COALESCE(description,''), path FROM skills "
                f"WHERE skills MATCH ? ORDER BY {order} LIMIT ?", (fts, n)).fetchall()
        except Exception:
            rows = []
        if rows:
            break
    if not rows:
        like = f"%{q}%"
        rows = c.execute(
            "SELECT name, COALESCE(category,''), COALESCE(description,''), path FROM skills "
            "WHERE name LIKE ? OR description LIKE ? LIMIT ?", (like, like, n)).fetchall()
    if not rows:
        print("tidak ada hasil")
        return
    for name, cat, desc, path in rows:
        d = (desc or "").replace("\n", " ").strip()[:60]
        short = path.replace(os.path.expanduser("~"), "~")
        print(f"- {name} [{cat or '-'}] {d} — {short}")

main()
