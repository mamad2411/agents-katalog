#!/usr/bin/env python3
"""ghscan-fetch.py — proses hasil enumerasi ghscan-enum.sh: JSON -> repo unik ->
unduh SKILL.md (curl, no rate limit) -> dedup vs index -> simpan ke skills-expanded/."""
import json, os, re, subprocess, sqlite3, glob
from datetime import datetime, timezone

AG = os.path.expanduser("~/.agents")
DEST = os.path.join(AG, "skills-expanded")
DB = os.path.join(AG, "skills-index.db")
LOG = os.path.join(AG, ".ghscan-fetch-state.json")
FM = re.compile(r'^name:\s*["\']?([\w-]+)', re.M)


def raw_get(owner, repo, path="SKILL.md"):
    """path persis dari code search -> 1 request. Fallback root kalau 404."""
    for p in (path, "SKILL.md"):
        r = subprocess.run(
            ["curl", "-s", "-f", "--max-time", "10",
             f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{p}"],
            capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout
    return None


def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return {}


def main():
    files = sorted(glob.glob("/tmp/ghscan-raw/*.json"))
    # kumpulkan (repo, path) — path persis dari code search = 1 request, no branching
    pairs = {}
    for f in files:
        d = load(f)
        for it in d.get("items", []):
            fn = it.get("repository", {}).get("full_name")
            pa = it.get("path") or "SKILL.md"
            if fn and fn not in pairs:
                pairs[fn] = pa
    repos = set(pairs)
    print(f"file json       : {len(files)}")
    print(f"repo unik       : {len(repos)}")

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    existing = {r[0] for r in conn.execute("SELECT name FROM skills")}
    conn.close()

    st = load(LOG)
    done = set(st.get("done_repos", []))
    new = st.get("new", 0); exists = st.get("exists", 0); miss = st.get("miss", 0)
    todo = sorted(repos - done)
    print(f"sudah di-fetch  : {len(done)} | sisa: {len(todo)}")

    for i, full in enumerate(todo, 1):
        owner, repo = full.split("/", 1)
        body = raw_get(owner, repo, pairs.get(full, "SKILL.md"))
        if body is None:
            miss += 1; done.add(full); continue
        m = FM.search(body.decode("utf-8", "ignore"))
        name = re.sub(r"-{2,}", "-", (m.group(1) if m else repo).lower()).strip("-")
        if name in existing:
            exists += 1
        else:
            d = os.path.join(DEST, f"ghscan-{owner}-{repo}")
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "SKILL.md"), "wb").write(body)
            existing.add(name); new += 1
        done.add(full)
        if i % 25 == 0:
            json.dump({"done_repos": sorted(done), "new": new, "exists": exists,
                       "miss": miss, "ts": datetime.now(timezone.utc).isoformat()},
                      open(LOG, "w"), indent=1)
            print(f"  [{i}/{len(todo)}] NEW={new} exists={exists} miss={miss}", flush=True)
    json.dump({"done_repos": sorted(done), "new": new, "exists": exists,
               "miss": miss, "ts": datetime.now(timezone.utc).isoformat()},
              open(LOG, "w"), indent=1)
    print(f"\nHASIL: BARU={new}  sudah-ada={exists}  gagal-ambil={miss}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
