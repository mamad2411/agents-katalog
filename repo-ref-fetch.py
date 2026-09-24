#!/usr/bin/env python3
"""
Repo Reference Fetcher (README-only, tanpa git)
================================================
Ganti mass-repo-cloner.py yang berat (git clone -> 31GB proyeksi).
Cara baru: HTTP GET README dari raw.githubusercontent.com (tanpa git,
tanpa .git, tanpa rate-limit API). Hasil: STUB.md ringkas + meta.json.

Perkiraan: ~10KB/repo -> 14.405 repo = ~150MB (bukan 31GB).

Usage:
  python3 repo-ref-fetch.py                # lanjut fetch (resume)
  python3 repo-ref-fetch.py --workers 4    # atur paralel (default 4)
  python3 repo-ref-fetch.py --limit 200    # batasi jumlah
  python3 repo-ref-fetch.py --status       # lihat progress
  python3 repo-ref-fetch.py --index        # rebuild index
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO_LIST = "/tmp/all-repos.json"
REFS_DIR = os.path.expanduser("~/.agents/repo-refs")
INDEX_FILE = os.path.join(REFS_DIR, "repo-master-index.json")
PROGRESS = os.path.expanduser("~/.agents/repo-ref-progress.json")
WORKERS = 4
LIMIT = 0
THROTTLE = 0.15  # detik per request (jaga adem)

READMES = ["README.md", "readme.md", "README.rst", "README"]
BRANCHES = ["HEAD", "main"]


def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "repo-ref-fetch/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="ignore")


def fetch_one(repo_full):
    """Ambil README satu repo. Return 'ok' | 'skip' | 'fail'."""
    name = repo_full.replace("/", "_")
    repo_path = os.path.join(REFS_DIR, name)
    stub_path = os.path.join(repo_path, "STUB.md")
    if os.path.exists(stub_path):
        return "skip"

    content = None
    for branch in BRANCHES:
        for rd in READMES:
            time.sleep(0.05)
            url = f"https://raw.githubusercontent.com/{repo_full}/{branch}/{rd}"
            try:
                content = http_get(url, timeout=10)
                if content and len(content.strip()) > 50:
                    break
                content = None
            except (urllib.error.HTTPError, urllib.error.URLError,
                    TimeoutError, OSError):
                content = None
        if content:
            break

    if not content:
        return "fail"

    os.makedirs(repo_path, exist_ok=True)
    body = content[:4000]
    stub = (f"# {repo_full}\n\n"
            f"Source: https://github.com/{repo_full}\n"
            f"Fetched: {datetime.now().isoformat()[:10]}\n\n"
            f"## README\n{body}\n")
    with open(stub_path, "w") as f:
        f.write(stub)
    save_json(os.path.join(repo_path, "meta.json"), {
        "repo": repo_full,
        "url": f"https://github.com/{repo_full}",
        "readme_chars": len(content),
        "stub_chars": len(stub),
        "fetched": datetime.now().isoformat(),
    })
    return "ok"


def run(workers, limit):
    repos = load_json(REPO_LIST, [])
    progress = load_json(PROGRESS, {"ok": [], "fail": []})
    done = set(progress.get("ok", []) + progress.get("fail", []))
    todo = [r for r in repos if r not in done]
    if limit:
        todo = todo[:limit]

    print("=== REPO REF FETCH (README-only) ===")
    print(f"Total repo: {len(repos)} | sudah: {len(done)} | antre: {len(todo)}")
    print(f"Workers: {workers} | throttle: {THROTTLE}s")
    sys.stdout.flush()

    ok = fail = skip = 0
    done_n = 0
    CHUNK = 150
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for start in range(0, len(todo), CHUNK):
            chunk = todo[start:start + CHUNK]
            futs = {ex.submit(fetch_one, r): r for r in chunk}
            for fut in as_completed(futs):
                repo = futs[fut]
                done_n += 1
                try:
                    res = fut.result()
                except Exception:
                    res = "fail"
                if res == "skip":
                    skip += 1
                    progress["ok"].append(repo)
                elif res == "ok":
                    ok += 1
                    progress["ok"].append(repo)
                else:
                    fail += 1
                    progress["fail"].append(repo)
            save_json(PROGRESS, progress)
            print(f"  [{done_n}/{len(todo)}] ok={ok} gagal={fail} skip={skip}")
            sys.stdout.flush()

    save_json(PROGRESS, progress)
    remaining = len(repos) - len(set(progress.get("ok", []) + progress.get("fail", [])))
    save_json(os.path.expanduser("~/.agents/repo-ref-state.json"), {
        "total": len(repos),
        "ok": len(progress.get("ok", [])),
        "fail": len(progress.get("fail", [])),
        "remaining": remaining,
        "complete": remaining <= 0,
        "updated": datetime.now().isoformat(),
    })
    print(f"\nSELESAI: ok={ok} gagal={fail} skip={skip} | sisa={remaining}")
    rebuild_index()


def show_status():
    repos = load_json(REPO_LIST, [])
    progress = load_json(PROGRESS, {"ok": [], "fail": []})
    ok = len(progress.get("ok", []))
    fail = len(progress.get("fail", []))
    total = len(repos)
    pct = (ok + fail) / total * 100 if total else 0
    print("=== PROGRESS REPO REFS ===")
    print(f"Total: {total} | ok: {ok} | gagal: {fail} | progress: {pct:.1f}%")
    if os.path.exists(REFS_DIR):
        dirs = [d for d in os.listdir(REFS_DIR)
                if os.path.isdir(os.path.join(REFS_DIR, d)) and not d.startswith(".")]
        stubbed = [d for d in dirs
                   if os.path.exists(os.path.join(REFS_DIR, d, "STUB.md"))]
        print(f"Folder: {len(dirs)} | punya STUB.md: {len(stubbed)}")


def rebuild_index():
    repos = []
    if os.path.exists(REFS_DIR):
        for name in sorted(os.listdir(REFS_DIR)):
            path = os.path.join(REFS_DIR, name)
            if not os.path.isdir(path) or name.startswith("."):
                continue
            preview = ""
            stub = os.path.join(path, "STUB.md")
            if os.path.exists(stub):
                with open(stub, errors="ignore") as f:
                    preview = f.read()[:400]
            repos.append({"name": name, "path": path, "stub_preview": preview})
    save_json(INDEX_FILE, {"version": "2.0", "count": len(repos),
                           "repos": repos, "updated": datetime.now().isoformat()})
    print(f"Index rebuilt: {len(repos)} repo -> {INDEX_FILE}")


def main():
    global WORKERS, LIMIT
    os.makedirs(REFS_DIR, exist_ok=True)
    args = sys.argv[1:]
    if "--status" in args:
        show_status()
        return
    if "--index" in args:
        rebuild_index()
        return
    if "--workers" in args:
        WORKERS = int(args[args.index("--workers") + 1])
    if "--limit" in args:
        LIMIT = int(args[args.index("--limit") + 1])
    run(WORKERS, LIMIT)


if __name__ == "__main__":
    main()