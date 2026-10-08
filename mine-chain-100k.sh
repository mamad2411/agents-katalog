#!/usr/bin/env bash
# mine-chain-100k.sh — rantai otomatis menuju 100k, hemat panas (nice + jeda).
# Tahap: tunggu enum -> fetch SKILL.md baru -> repo-refs baru -> rebuild index -> regenerate -> lapor.
# Jalan background: bash ~/.agents/mine-chain-100k.sh [enum_log_name]
set -uo pipefail
A="$HOME/.agents"
LOG=/tmp/mine100k/chain.log
ENUMLOG_NAME="${1:-enum20.log}"
mkdir -p /tmp/mine100k
{
echo "=== CHAIN-2 mulai $(date -u +%FT%TZ) ==="
# 1. tunggu enum selesai
while pgrep -f 'ghscan-enum\.sh 20' >/dev/null 2>&1; do sleep 60; done
echo "--- enum selesai $(date -u +%FT%TZ), jsons: $(ls /tmp/ghscan-raw/*.json 2>/dev/null | wc -l) ---"
# 2. fetch skill baru (nice, curl, dedup+checkpoint)
export GH_TOKEN="$(gh auth token 2>/dev/null)"
nice -n 15 python3 "$A/ghscan-fetch.py" 2>&1 | tail -4
# 3. repo-refs baru dari repo yg terbukti punya SKILL.md (sparse, ringan, nice)
python3 - <<'PY'
import json, os
st = json.load(open(os.path.expanduser("~/.agents/.ghscan-fetch-state.json")))
done = st.get("done_repos", [])
rr = os.path.expanduser("~/.agents/repo-refs")
existing = {d for d in os.listdir(rr) if os.path.isdir(os.path.join(rr, d))}
norm = {e.replace("_", "/").lower() for e in existing}
new = [r for r in done if r.lower() not in norm]
json.dump(new, open("/tmp/new-repos.json", "w"))
print("repo-refs baru:", len(new))
PY
nice -n 15 python3 - <<'PY'
import json, os, subprocess, time
new = json.load(open("/tmp/new-repos.json"))
rr = os.path.expanduser("~/.agents/repo-refs")
ok = fail = skip = 0
# cap 1500 repo per batch biar adem + hemat disk
for i, full in enumerate(new[:1500], 1):
    name = full.replace("/", "_")
    target = os.path.join(rr, name)
    if os.path.exists(target):
        skip += 1; continue
    r = subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none",
                        "--sparse", f"https://github.com/{full}", target],
                       capture_output=True, timeout=40)
    if r.returncode != 0:
        fail += 1; continue
    subprocess.run(["git", "-C", target, "sparse-checkout", "set",
                    "README.md", "README", "docs"],
                   capture_output=True, timeout=15)
    subprocess.run(["bash", "-c",
        f"cd {target} && find . -maxdepth 2 -not -path './.git/*' | head -100 > TREE.txt; rm -rf .git; touch .metadata_never_index"],
        capture_output=True, timeout=15)
    ok += 1
    if i % 50 == 0:
        print(f"  [{i}] ok={ok} fail={fail} skip={skip}", flush=True)
        time.sleep(3)
print(f"repo-refs HASIL: ok={ok} fail={fail} skip={skip}")
PY
# 4. rebuild index + regenerate berurutan
nice -n 15 python3 "$A/build_skills_index.py" 2>&1 | tail -6
nice -n 15 python3 "$A/skills-index-md.py" 2>&1 | tail -2
nice -n 15 python3 "$A/skills-router.py" 2>&1 | tail -2
nice -n 15 python3 "$A/concept-flow-map.py" 2>&1 | tail -3
# 5. lapor
python3 - <<'PY'
import sqlite3, os
db = os.path.expanduser("~/.agents/skills-index.db")
c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
t = c.execute("select count(*) from skills").fetchone()[0]
print("TOTAL:", t, "| kurang:", max(0, 100000 - t))
for tier, n in c.execute("select tier,count(*) from skills group by tier order by 2 desc"):
    print(f"  {tier}: {n}")
import os as _o
rr = _o.path.expanduser("~/.agents/repo-refs")
print("repo-refs dirs:", len([d for d in _o.listdir(rr) if _o.path.isdir(_o.path.join(rr, d))]))
PY
echo "=== CHAIN-2 selesai $(date -u +%FT%TZ) ==="
} >> "$LOG" 2>&1 &
echo "chain-2 jalan background, log: $LOG (enum: $ENUMLOG_NAME)"