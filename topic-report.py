#!/usr/bin/env python3
"""topic-report.py — lapor total index + repo-refs (dipanggil topic-chain.sh)."""
import os, sqlite3
db = os.path.expanduser("~/.agents/skills-index.db")
c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
t = c.execute("select count(*) from skills").fetchone()[0]
print("FINAL-TOTAL:", t, "| kurang:", max(0, 100000 - t))
for tier, n in c.execute("select tier,count(*) from skills group by tier order by 2 desc"):
    print(f"  {tier}: {n}")
rr = os.path.expanduser("~/.agents/repo-refs")
print("repo-refs dirs:", len([d for d in os.listdir(rr) if os.path.isdir(os.path.join(rr, d))]))
