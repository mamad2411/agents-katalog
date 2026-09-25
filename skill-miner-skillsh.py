#!/usr/bin/env python3
"""skill-miner-skillsh.py — tambang SKILL.md dari direktori skills.sh (20.000 entry).

Keunggulan vs skill-miner.py (GitHub API):
  * TIDAK pakai API tree -> TIDAK kena rate limit (60/jam). Makai raw.githubusercontent.com.
  * Sumber 20.000 skill dari ~2.366 repo yang BELUM di-tambang registry.

Sumber: ~/.agents/SKILLS-SKILLSH-DIRECTORY.md (baris "- slug — https://www.skills.sh/owner/repo/slug")

Cara: untuk tiap entry, coba beberapa layout umum di branch default (HEAD):
    <slug>/SKILL.md · skills/<slug>/SKILL.md · .claude/skills/<slug>/SKILL.md · SKILL.md (root)
Dedup: by nama kanonik (sudah ada di index -> skip) + by md5 konten.
Idempotent & aman: tidak menimpa file yang ada.

Pakai:
  python3 ~/.agents/skill-miner-skillsh.py --limit 200      # coba 200 entry
  python3 ~/.agents/skill-miner-skillsh.py --probe 50       # dry-run: cek hit rate saja
  python3 ~/.agents/skill-miner-skillsh.py                  # semua 20.000
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import urllib.request

AG = os.path.expanduser("~/.agents")
SRC = os.path.join(AG, "SKILLS-SKILLSH-DIRECTORY.md")
DEST = os.path.join(AG, "skills-expanded")
DB = os.path.join(AG, "skills-index.db")
RAW = "https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"
UA = {"User-Agent": "skill-miner-skillsh/1.0"}

ENTRY_RE = re.compile(r"^-\s+([A-Za-z0-9._-]+)\s+—\s+https://www\.skills\.sh/([^/]+)/([^/]+)/([^/\s]+)\s*$")
FM_NAME = re.compile(r"^name:\s*[\"']?([\w-]+)", re.M)
FM_DESC = re.compile(r"^description:\s*[\"']?(.{5,})", re.M)


def parse_entries():
    out = []
    if not os.path.exists(SRC):
        return out
    with open(SRC, encoding="utf-8", errors="ignore") as f:
        for ln in f:
            m = ENTRY_RE.match(ln.rstrip())
            if m:
                slug, owner, repo, s2 = m.groups()
                out.append((slug, owner, repo, s2))
    return out


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def canonical(n):
    return re.sub(r"-{2,}", "-", (n or "").strip().lower()).strip("-")



_TREE_CACHE = {}


def api_fetch(owner, repo, slug):
    """Fallback monorepo: 1 request GitHub API memetakan path, ambil SKILL.md yang folder~slug."""
    key = (owner, repo)
    if key in _TREE_CACHE and _TREE_CACHE[key] is None:
        return None          # repo ini sudah gagal dipetakan -> skip semua slug-nya
    if key not in _TREE_CACHE:
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        req = urllib.request.Request(url, headers=UA)
        tok = os.environ.get("GH_TOKEN", "")
        if tok:
            req.add_header("Authorization", f"Bearer {tok}")
        try:
            with urllib.request.urlopen(req, timeout=8) as r:
                _TREE_CACHE[key] = [x.get("path", "") for x in
                                    json.loads(r.read().decode("utf-8", "ignore")).get("tree", [])
                                    if x.get("path", "").endswith("SKILL.md")]
        except Exception:
            _TREE_CACHE[key] = None   # tandai gagal: jangan retry per entry
    paths = _TREE_CACHE.get(key) or []
    if not paths:
        return None
    slug_l = slug.lower()
    for p in paths:
        if True:
            if slug_l in p.lower():
                try:
                    return get(RAW.format(owner=owner, repo=repo, path=p))
                except Exception:
                    return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--probe", type=int, default=0)
    ap.add_argument("--offset", type=int, default=0, help="mulai dari entry ke-N")
    a = ap.parse_args()

    entries = parse_entries()
    if a.offset:
        entries = entries[a.offset:]
    if a.limit:
        entries = entries[:a.limit]
    if a.probe:
        entries = entries[:a.probe]
    if not entries:
        print("tidak ada entry di SKILLS-SKILLSH-DIRECTORY.md")
        return 1

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    existing = {r[0] for r in conn.execute("SELECT name FROM skills")}
    seen_hash = set()
    stats = {"hit": 0, "new": 0, "exists": 0, "nodup": 0, "nofile": 0}
    t0 = time.time()

    for i, (slug, owner, repo, s2) in enumerate(entries, 1):
        print(f'  [{i}] {owner}/{repo}/{s2}', flush=True)
        body = None
        for path in (f"{s2}/SKILL.md", f"skills/{s2}/SKILL.md",
                     f".claude/skills/{s2}/SKILL.md", "SKILL.md"):
            try:
                body = get(RAW.format(owner=owner, repo=repo, path=path))
                break
            except Exception:
                continue
        if not body:
            body = api_fetch(owner, repo, s2)
        if not body:
            stats["nofile"] += 1
            if a.probe:
                print(f"  [probe] {owner}/{repo}/{s2}: tidak ada SKILL.md")
            continue
        stats["hit"] += 1
        text = body.decode("utf-8", "ignore")
        nm = FM_NAME.search(text)
        name = canonical(nm.group(1) if nm else slug)
        if a.probe:
            print(f"  [probe] {owner}/{repo}/{s2}: HIT name={name} bytes={len(body)}")
            continue
        h = hashlib.md5(body).hexdigest()
        if h in seen_hash:
            stats["nodup"] += 1
            continue
        seen_hash.add(h)
        if name in existing:
            stats["exists"] += 1
            continue
        outdir = os.path.join(DEST, f"skillsh-{owner}-{repo}-{canonical(s2)}")
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "SKILL.md"), "wb") as f:
            f.write(body)
        existing.add(name)
        stats["new"] += 1
        if stats["new"] % 50 == 0:
            print(f"  [{i}/{len(entries)}] {stats} ({time.time()-t0:.0f}s)", flush=True)
    conn.close()
    print(f"selesai: {stats} | {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
