#!/usr/bin/env python3
"""crawl-and-scan.py — curated GitHub skill crawler + security scanner.

Stages:
  1. ENUM   — GitHub code search `filename:SKILL.md`, paginated (curl, not urllib — urllib hangs on this box).
  2. FETCH  — raw.githubusercontent.com, dedup vs skills-index.db.
  3. SCAN   — skill-security-auditor per skill dir, --json verdict (PASS/WARN/FAIL).
  4. REPORT — .crawl-scan-report.json + console summary.

Progress state : ~/.agents/.crawl-scan-state.json  {"done_repos": [...]}
Auth           : ~/.agents/.gh-token (mode 600, never commit).
Reuse          : patterns from gh-scan-skills.py / ghscan-enum.sh / ghscan-fetch.py.
"""
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

HOME = Path.home()
AGENTS = HOME / ".agents"
STATE = AGENTS / ".crawl-scan-state.json"
REPORT = AGENTS / ".crawl-scan-report.json"
OUT = AGENTS / "skills-expanded"
DB = AGENTS / "skills-index.db"
RAW_DIR = Path("/tmp/crawl-scan-raw")
TOKEN_FILE = AGENTS / ".gh-token"
AUDITOR = AGENTS / "skills/skill-security-auditor/scripts/skill_security_auditor.py"
FM_NAME = re.compile(r'^name:\s*["\']?([\w-]+)', re.M)

# small curated query set — each = 1 search API page (100 hits max)
QUERIES = [
    'filename:SKILL.md "name:"',
    'filename:SKILL.md "triggers"',
    'filename:SKILL.md "when to use"',
    'filename:SKILL.md "proactively activate"',
    'filename:SKILL.md "use when"',
    'filename:SKILL.md path:.claude/skills',
    'filename:SKILL.md "description:"',
    'filename:SKILL.md path:skills',
]
SEARCH_SLEEP = 7.0        # code-search API: 10 req/min
UA = "crawl-and-scan/1.0"


def token() -> str:
    return TOKEN_FILE.read_text().strip() if TOKEN_FILE.exists() else os.environ.get("GH_TOKEN", "")


def gh(url: str) -> subprocess.CompletedProcess:
    cmd = ["curl", "-sS", "-L", "--max-time", "30", "-H", f"User-Agent: {UA}"]
    t = token()
    if t:
        cmd += ["-H", f"Authorization: Bearer {t}"]
    cmd.append(url)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=40)


def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except Exception:
            pass
    return {"done_repos": []}


def save_state(st: dict) -> None:
    st["done_repos"] = sorted(set(st.get("done_repos", [])))
    STATE.write_text(json.dumps(st, indent=1))


def existing_names() -> set:
    if not DB.exists():
        return set()
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        return {r[0] for r in con.execute("SELECT name FROM skills")}
    finally:
        con.close()


def enum(plan_pages: int) -> list:
    """Stage 1: collect (repo, path) candidates into RAW_DIR/*.json, return all pairs."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pairs = []
    for qi, q in enumerate(QUERIES):
        for page in range(1, plan_pages + 1):
            fp = RAW_DIR / f"q{qi}_p{page}.json"
            if fp.exists():
                data = json.loads(fp.read_text() or "{}")
            else:
                url = ("https://api.github.com/search/code?q="
                       + urllib.parse.quote(q) + f"&per_page=100&page={page}")
                r = gh(url)
                try:
                    data = json.loads(r.stdout or "{}")
                except Exception:
                    data = {}
                fp.write_text(json.dumps(data))
                time.sleep(SEARCH_SLEEP)
            for item in data.get("items", []):
                repo = item.get("repository", {}).get("full_name")
                path = item.get("path")
                if repo and path:
                    pairs.append((repo, path))
    # dedup
    seen, uniq = set(), []
    for p in pairs:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


def fetch(pairs: list, limit: int, state: dict) -> list:
    """Stage 2: fetch new skills into OUT/<name>/SKILL.md. Returns fetched records."""
    OUT.mkdir(parents=True, exist_ok=True)
    names = existing_names()
    done = set(state.get("done_repos", []))
    fetched = []
    for repo, path in pairs:
        if len(fetched) >= limit:
            break
        if repo in done:
            continue
        url = f"https://raw.githubusercontent.com/{repo}/HEAD/{path}"
        r = gh(url)
        text = r.stdout
        if r.returncode != 0 or not text or text.startswith("404"):
            # fallback: root SKILL.md
            r = gh(f"https://raw.githubusercontent.com/{repo}/HEAD/SKILL.md")
            text = r.stdout
            if r.returncode != 0 or not text or text.startswith("404"):
                state.setdefault("done_repos", []).append(repo)
                continue
        m = FM_NAME.search(text)
        name = m.group(1) if m else repo.split("/")[-1].lower().replace("_", "-")
        name = re.sub(r"[^\w-]", "-", name)[:60]
        if name in names:
            state.setdefault("done_repos", []).append(repo)
            continue
        d = OUT / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(text)
        names.add(name)
        state.setdefault("done_repos", []).append(repo)
        fetched.append({"name": name, "repo": repo, "path": path})
        time.sleep(0.3)  # raw rate limit headroom
    save_state(state)
    return fetched


def scan(records: list) -> list:
    """Stage 3: run skill-security-auditor --json on each fetched skill dir."""
    for rec in records:
        d = OUT / rec["name"]
        try:
            r = subprocess.run(
                ["python3", str(AUDITOR), "--json", str(d)],
                capture_output=True, text=True, timeout=60,
            )
            try:
                j = json.loads(r.stdout)
                rec["verdict"] = j.get("verdict") or j.get("result") or "UNKNOWN"
                rec["findings"] = j.get("findings") or j.get("issues") or []
            except Exception:
                rec["verdict"] = "UNKNOWN"
                rec["findings"] = [{"raw": (r.stdout or r.stderr)[:500]}]
        except Exception as e:
            rec["verdict"] = "ERROR"
            rec["findings"] = [{"error": str(e)}]
    return records


def write_report(records: list) -> dict:
    counts = {"fetched": len(records), "PASS": 0, "WARN": 0, "FAIL": 0, "OTHER": 0}
    for r in records:
        v = r.get("verdict", "OTHER")
        counts[v] = counts.get(v, 0) + 1 if v in ("PASS", "WARN", "FAIL") else counts["OTHER"] + 1
    report = {"generated": time.strftime("%Y-%m-%dT%H:%M:%S"), "counts": counts, "skills": records}
    REPORT.write_text(json.dumps(report, indent=1))
    return counts


def main() -> int:
    args = set(sys.argv[1:])
    state = load_state()

    if "--status" in args:
        print(f"state: {len(state.get('done_repos', []))} repos done")
        print(f"out  : {len(list(OUT.iterdir())) if OUT.exists() else 0} skills in {OUT}")
        if REPORT.exists():
            print(f"last : {json.loads(REPORT.read_text()).get('counts')}")
        return 0

    plan_pages = 1
    if "--plan" in args:
        i = sys.argv.index("--plan")
        plan_pages = int(sys.argv[i + 1]) if i + 1 < len(sys.argv) else 1
        pairs = enum(plan_pages)
        print(f"[enum] {len(pairs)} unique (repo,path) candidates across {len(QUERIES)} queries x {plan_pages} pages")
        for repo, path in pairs[:15]:
            print(f"  {repo} :: {path}")
        if len(pairs) > 15:
            print(f"  ... +{len(pairs) - 15} more")
        return 0

    limit = 50
    if "--limit" in args:
        i = sys.argv.index("--limit")
        limit = int(sys.argv[i + 1]) if i + 1 < len(sys.argv) else 50

    # default = --all: enum(1 page) -> fetch(limit) -> scan -> report
    pairs = enum(1)
    print(f"[enum] {len(pairs)} candidates")
    records = fetch(pairs, limit, state)
    print(f"[fetch] {len(records)} new skills saved to {OUT}")
    if not records:
        print("nothing new to scan.")
        return 0
    records = scan(records)
    counts = write_report(records)
    print(f"[scan] {counts}")
    print(f"[report] {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
