#!/usr/bin/env python3
"""gh-scan-skills.py — Cari SKILL.md di SELURUH GitHub lewat Code Search API.

Kenapa: skills.sh (20k) + registry (2,5k) sudah jenuh (yield 0-2,6%).
GitHub Code Search melaporkan 6,4 JUTA file bernama SKILL.md — sebagian besar
TIDAK terdaftar di skills.sh/registry. Jalur inilah untuk menambahpuluhan
ribu skill baru yang benar-benar unik.

2 tahap (hemat rate limit):
  1. ENUMERASI REPO via code search (10 req/menit, token wajib).
     Query divariasikan (path/stars/created) untuk menembus batas 1.000/query.
  2. AMBIL SKILL.md via raw.githubusercontent (TIDAK kena rate limit).

Checkpoint: ~/.agents/.ghscan-state.json (resume, tidak ulang kerja).

Pakai:
  python3 ~/.agents/gh-scan-skills.py --plan 200    # 200 query (~22 menit)
  python3 ~/.agents/gh-scan-skills.py --status
  python3 ~/.agents/gh-scan-skills.py --test
"""
import argparse, json, os, random, re, sqlite3, sys, time
import urllib.parse, urllib.request
from datetime import datetime, timezone

AG = os.path.expanduser("~/.agents")
DEST = os.path.join(AG, "skills-expanded")
DB = os.path.join(AG, "skills-index.db")
STATE = os.path.join(AG, ".ghscan-state.json")
TOKEN = os.environ.get("GH_TOKEN", "")
UA = {"User-Agent": "gh-scan-skills/1.0", "Accept": "application/vnd.github+json"}

PATH_HINTS = ["skills", ".claude", "claude", "agent", "agents", "prompts",
              "mcp", "plugin", "plugins", "toolkit", "tool", "prompt",
              "commands", "rules", "workspace", "packages", "src", "docs",
              "examples", "skillsets", ".agents", "cursor", "openai", "gemini"]
FM = re.compile(r"^name:\s*[\"']?([\w-]+)", re.M)


def gh(url, timeout=25):
    """pakai subprocess curl (bukan urllib) — di mesin ini urllib sering
    hang di SSLSocket_read, sementara curl selalu lancar."""
    import subprocess
    cmd = ["curl", "-s", "--max-time", str(timeout),
           "-H", "Accept: application/vnd.github+json",
           "-H", f"User-Agent: {UA['User-Agent']}"]
    if TOKEN:
        cmd += ["-H", f"Authorization: Bearer {TOKEN}"]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
    if not r.stdout.strip():
        raise RuntimeError("curl empty response")
    return json.loads(r.stdout)


def code_search(q, page=1, per_page=100):
    url = ("https://api.github.com/search/code?q=" + urllib.parse.quote(q)
           + f"&per_page={per_page}&page={page}")
    return gh(url)


def load_state():
    if os.path.exists(STATE):
        try:
            return json.load(open(STATE))
        except Exception:
            pass
    return {"queries_done": [], "repos": [], "done_repos": [], "fetched": 0,
            "new": 0, "exists": 0, "err": 0,
            "started": datetime.now(timezone.utc).isoformat()}


def save_state(s):
    tmp = STATE + ".tmp"
    json.dump(s, open(tmp, "w"), indent=1)
    os.replace(tmp, STATE)


def gen_queries(n):
    """n query UNIK. Kombinasi path-hint × bucket stars/language supaya setiap
    query menghasilkan set hasil berbeda (batas 1.000 hasil/query)."""
    buckets = ["", "stars:1..5", "stars:6..20", "stars:21..100", "stars:101..500",
               "stars:>500", "language:Markdown", "language:TypeScript",
               "language:Python", "language:JavaScript"]
    qs, seen = [], set()

    def add(q):
        if q not in seen:
            seen.add(q)
            qs.append(q)

    add("filename:SKILL.md")
    add("filename:skill.md")
    add("filename:Skill.md")
    for p in PATH_HINTS:
        add(f"filename:SKILL.md path:{p}")
        for b in buckets[1:]:
            add(f"filename:SKILL.md path:{p} {b}")
    for b in buckets:
        add(f"filename:SKILL.md {b}".strip())
    return qs[:n]


def enumerate_repos(plan, state):
    all_q = gen_queries(max(plan * 2, 50))
    todo = [q for q in all_q if q not in state["queries_done"]][:plan]
    known = set(state["repos"])
    found = []
    files = state.setdefault("files", [])
    seen_files = {(f["repo"], f["path"]) for f in files}
    for i, q in enumerate(todo, 1):
        try:
            d = code_search(q)
        except Exception as e:
            if "rate limit" in str(e).lower() or "403" in str(e):
                print(f"  [rate limit] stop di query {i}/{len(todo)} — resume nanti")
                break
            state["err"] += 1
            continue
        for it in d.get("items", []):
            full = it["repository"]["full_name"]
            path = it.get("path") or "SKILL.md"
            if (full, path) not in seen_files:
                seen_files.add((full, path))
                files.append({"repo": full, "path": path})
            if full not in known:
                known.add(full); found.append(full)
        state["queries_done"].append(q)
        if i % 10 == 0 or i == len(todo):
            state["repos"] = sorted(known); save_state(state)
            print(f"  [{i}/{len(todo)}] query ok · repo unik: {len(known)} · file: {len(files)}", flush=True)
        time.sleep(6.5)
    state["repos"] = sorted(known); save_state(state)
    return found


def raw_get(owner, repo, branch, path="SKILL.md"):
    """download file via curl (no rate limit). Return bytes or None."""
    import subprocess
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    r = subprocess.run(["curl", "-s", "-f", "--max-time", "15", url],
                       capture_output=True)
    return r.stdout if r.returncode == 0 and r.stdout else None


def fetch_one(item):
    """Ambil 1 kandidat (dipakai paralel)."""
    full, path = item["repo"], item["path"]
    owner, repo = full.split("/", 1)
    body = None
    for br in ("HEAD", "main", "master"):
        body = raw_get(owner, repo, br, path)
        if body is not None:
            break
    return item, body


def fetch_skills(repos, state):
    from concurrent.futures import ThreadPoolExecutor
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    existing = {r[0] for r in conn.execute("SELECT name FROM skills")}
    conn.close()
    files = state.get("files") or []
    done = set(state.get("done_repos", []))
    todo = [f for f in files if f"{f['repo']}::{f['path']}" not in done]
    print(f"  fetch paralel: {len(todo)} file", flush=True)
    lock_existing = existing
    i = 0
    with ThreadPoolExecutor(max_workers=10) as ex:
        for item, body in ex.map(fetch_one, todo, chunksize=4):
            i += 1
            state["fetched"] += 1
            full, path = item["repo"], item["path"]
            if body is not None:
                m = FM.search(body.decode("utf-8", "ignore"))
                fallback = os.path.splitext(os.path.basename(path))[0] if "/" in path else full.split("/")[1]
                name = re.sub(r"-{2,}", "-", (m.group(1) if m else fallback).lower()).strip("-")
                if name in lock_existing:
                    state["exists"] += 1
                else:
                    owner, repo = full.split("/", 1)
                    slug = re.sub(r"[^a-z0-9-]+", "-", f"ghscan-{owner}-{repo}-{name}")[:90].strip("-")
                    d = os.path.join(DEST, slug)
                    try:
                        os.makedirs(d, exist_ok=True)
                        open(os.path.join(d, "SKILL.md"), "wb").write(body)
                        lock_existing.add(name); state["new"] += 1
                    except OSError:
                        state["err"] += 1
            done.add(f"{full}::{path}")
            if i % 200 == 0 or i == len(todo):
                state["done_repos"] = sorted(done); save_state(state)
                print(f"  [fetch {i}/{len(todo)}] new={state['new']} exists={state['exists']}", flush=True)
    state["done_repos"] = sorted(done); save_state(state)


def status():
    s = load_state()
    print("=== gh-scan-skills status ===")
    print(f"  query selesai : {len(s['queries_done'])}")
    print(f"  repo unik     : {len(s['repos'])}")
    print(f"  di-fetch      : {len(s.get('done_repos', []))}")
    print(f"  skill BARU    : {s['new']}")
    print(f"  sudah ada     : {s['exists']}")
    print(f"  error         : {s['err']}   started: {s['started']}")


def self_test():
    print("=== self-test ===")
    qs = gen_queries(20)
    assert len(qs) == 20 and len(set(qs)) == 20
    print("  ✓ 20 query unik")
    if not TOKEN:
        print("  ! GH_TOKEN kosong"); return 1
    try:
        d = code_search(qs[0], per_page=2)
        print(f"  ✓ code search jalan: total_count={d.get('total_count')}, items={len(d.get('items',[]))}")
    except Exception as e:
        print(f"  ✗ GAGAL: {e}"); return 1
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=int, default=200)
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args()
    if a.status: status(); return 0
    if a.test: return self_test()
    if not TOKEN:
        print("ERROR: GH_TOKEN wajib", file=sys.stderr); return 1
    st = load_state()
    print(f"=== enumerasi {a.plan} query ===", flush=True)
    repos = enumerate_repos(a.plan, st)
    print(f"=== repo baru: {len(repos)} ===", flush=True)
    if not a.no_fetch and (repos or st.get("files")):
        print(f"=== ambil SKILL.md ({len(st.get('files') or [])} file kandidat) ===", flush=True)
        fetch_skills(repos, st)
    status(); return 0


if __name__ == "__main__":
    raise SystemExit(main())
