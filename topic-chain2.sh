#!/usr/bin/env bash
# topic-chain2.sh — jilid 2: enum topic baru -> fetch 2 worker -> repo-refs -> rebuild -> lapor.
set -uo pipefail
A="$HOME/.agents"
LOG=/tmp/mine100k/jilid2.log
mkdir -p /tmp/mine100k
{
echo "=== JILID-2 mulai $(date -u +%FT%TZ) ==="
export GH_TOKEN="$(gh auth token 2>/dev/null)"
# 1. enum+fifo-fetch worker-1 (depan), pages 10
nice -n 15 python3 "$A/topic-mine.py" --pages 10 2>&1 | tail -4
# 2. repo-refs baru (cap 1500)
python3 - <<'PY'
import json, os
st = json.load(open(os.path.expanduser("~/.agents/.ghscan-fetch-state.json")))
try:
    st2 = json.load(open(os.path.expanduser("~/.agents/.topic-mine-state.json")))
    done = list(set(st.get("done_repos", [])) | set(st2.get("done", [])))
except Exception:
    done = st.get("done_repos", [])
rr = os.path.expanduser("~/.agents/repo-refs")
existing = {d.replace("_", "/").lower() for d in os.listdir(rr) if os.path.isdir(os.path.join(rr, d))}
new = [r for r in done if r.lower() not in existing]
json.dump(new, open("/tmp/new-repos2.json", "w"))
print("repo-refs baru:", len(new))
PY
nice -n 15 python3 - <<'PY'
import json, os, subprocess, time
new = json.load(open("/tmp/new-repos2.json"))
rr = os.path.expanduser("~/.agents/repo-refs")
ok = fail = skip = 0
for i, full in enumerate(new[:1500], 1):
    target = os.path.join(rr, full.replace("/", "_"))
    if os.path.exists(target):
        skip += 1; continue
    r = subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none",
                        "--sparse", f"https://github.com/{full}", target],
                       capture_output=True, timeout=40)
    if r.returncode != 0:
        fail += 1; continue
    subprocess.run(["git", "-C", target, "sparse-checkout", "set",
                    "README.md", "README", "docs"], capture_output=True, timeout=15)
    subprocess.run(["bash", "-c",
        f"cd {target} && find . -maxdepth 2 -not -path './.git/*' | head -100 > TREE.txt; rm -rf .git; touch .metadata_never_index"],
        capture_output=True, timeout=15)
    ok += 1
    if i % 50 == 0:
        print(f"  [{i}] ok={ok} fail={fail} skip={skip}", flush=True)
        time.sleep(3)
print(f"repo-refs HASIL: ok={ok} fail={fail} skip={skip}")
PY
# 3. rebuild + regenerate + lapor
nice -n 15 python3 "$A/build_skills_index.py" 2>&1 | tail -6
nice -n 15 python3 "$A/skills-index-md.py" 2>&1 | tail -1
nice -n 15 python3 "$A/skills-router.py" 2>&1 | tail -1
nice -n 15 python3 "$A/concept-flow-map.py" 2>&1 | tail -3
python3 "$A/topic-report.py" 2>&1 | tail -8
echo "=== JILID-2 selesai $(date -u +%FT%TZ) ==="
} >> "$LOG" 2>&1 &
echo "jilid-2 jalan background, log: $LOG"