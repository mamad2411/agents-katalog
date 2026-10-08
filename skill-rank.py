#!/usr/bin/env python3
# Cetak 3 skill teratas untuk teks tugas (dipakai skill-inject.sh). Ranking = skill-mcp.rank_for_task.
import sys,os,importlib.util,io,contextlib
spec=importlib.util.spec_from_file_location("sm",os.path.expanduser("~/.agents/skill-mcp.py"))
m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
MIN=int(os.environ.get("SKILL_MIN_SCORE","15"))  # >=15 ≈ minimal 2 kata cocok (1 kata generik ≈ 10)
import json
HIDE=json.load(open(os.path.expanduser("~/.agents/skill-hide.json")))  # duplikat → versi utama
rows=m.rank_with_scores(" ".join(sys.argv[1:]),top=3)
out=[]
for sig,n,*_ in rows:
    n=HIDE.get(n,n)
    if sig>=MIN and n not in out: out.append(n)
print(",".join(out))
