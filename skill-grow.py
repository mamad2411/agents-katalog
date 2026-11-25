#!/usr/bin/env python3
"""skill-grow — tambah skill nyata dari 100k repo terindeks, dengan scan wajib.

Alur per repo:
  1. GET /repos/<slug>/git/trees/HEAD?recursive=1  -> cari semua SKILL.md
  2. download raw (paralel) -> skills-expanded/<nama>/SKILL.md
  3. scan inline (aturan sama dengan repo-hub) -> FAIL dibuang, PASS/WARN masuk
  4. INSERT ke skills-index.db -> langsung bisa dicari `sk`

Pakai:
  python3 skill-grow.py --target 500000 --minutes 240
  python3 skill-grow.py --status

State: ~/.agents/.skill-grow-state.json (resume otomatis)
"""
import argparse
import importlib.util
import json
import os
import re
import sqlite3
import sys
import threading
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
OUT = os.path.join(AG, "skills-expanded")
DB = os.path.join(AG, "skills-index.db")
REPO_DB = os.path.join(AG, "repos.db")
STATE = os.path.join(AG, ".skill-grow-state.json")
TOKEN_FILE = os.path.join(AG, ".gh-token")

FM_NAME = re.compile(r"^name:\s*[\"']?([\w.-]+)", re.M)
FM_DESC = re.compile(r"^description:\s*[\"']?(.+)$", re.M)


def load_scanner():
    spec = importlib.util.spec_from_file_location("rh", os.path.join(AG, "repo-hub.py"))
    rh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rh)
    return rh


def token():
    try:
        return open(TOKEN_FILE).read().strip()
    except Exception:
        return ""


def api(url, tok):
    for attempt in range(4):
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
            "User-Agent": "skill-grow"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                # kuota habis: JANGAN tidur lama (dulu bikin proses menggantung
                # berjam-jam). Lewati repo ini, lanjut ke berikutnya.
                return None
            if e.code == 404:
                return None
            time.sleep(5)
        except Exception:
            time.sleep(4)
    return None


def raw(slug, path):
    for _ in range(3):
        try:
            req = urllib.request.Request(
                f"https://raw.githubusercontent.com/{slug}/HEAD/{path}",
                headers={"User-Agent": "skill-grow"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception:
            time.sleep(1)
    return None


def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {"done": [], "skills": 0, "repos": 0}


def save_state(s):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f)
    os.replace(tmp, STATE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=500000)
    ap.add_argument("--minutes", type=int, default=240)
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--tree-workers", type=int, default=3)
    ap.add_argument("--dl-workers", type=int, default=8)
    args = ap.parse_args()

    st = load_state()
    conn = sqlite3.connect(DB, timeout=60, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=60000")
    total = conn.execute("SELECT COUNT(*) FROM skills").fetchone()[0]
    if args.status:
        print(f"skill di indeks: {total} · repo diproses: {len(st['done'])} · "
              f"ditambah sesi ini: {st['skills']}")
        return

    rh = load_scanner()
    compiled = [(sev, name, re.compile(rx)) for sev, name, rx in rh.SEC_RULES]
    tok = token()
    if not tok:
        sys.exit("butuh ~/.agents/.gh-token")

    done = set(st.get("done", []))
    rc = sqlite3.connect(REPO_DB, timeout=30)
    # prioritaskan repo yang lahir dari topik skill/agent (yield SKILL.md jauh lebih tinggi)
    repos = [r[0] for r in rc.execute(
        "SELECT slug FROM repos WHERE ("
        " lower(slug||' '||coalesce(desc,'')) LIKE '%skill%' OR"
        " lower(slug||' '||coalesce(desc,'')) LIKE '%agent%' OR"
        " lower(slug||' '||coalesce(desc,'')) LIKE '%claude%' OR"
        " lower(slug||' '||coalesce(desc,'')) LIKE '%mcp%' OR"
        " lower(slug||' '||coalesce(desc,'')) LIKE '%prompt%') ORDER BY "
        "(CASE WHEN origin LIKE 'api:%' THEN 0 ELSE 1 END), "
        "(CASE WHEN slug LIKE '%skill%' OR slug LIKE '%agent%' THEN 0 ELSE 1 END), "
        "stars DESC, slug")]
    todo = [r for r in repos if r not in done]
    print(f"[grow] indeks={total} · kandidat repo={len(todo)} · target={args.target}", flush=True)

    names = {r[0] for r in conn.execute("SELECT name FROM skills")}
    grows = {"ins": 0}
    lock = threading.Lock()
    start = time.time()
    added = fails = 0

    def handle(item):
        nonlocal added, fails
        slug, path = item
        if time.time() - start > args.minutes * 60:
            return
        text = raw(slug, path)
        if not text or len(text) < 400:
            return
        low = text.lower()
        if "used to hold an archived copy" in low or "this page used to hold" in low:
            with lock:
                fails += 1
            return
        for sev, _, rx in compiled:
            if sev == "critical" and rx.search(text):
                with lock:
                    fails += 1
                return
        m = FM_NAME.search(text)
        base = (m.group(1) if m else os.path.basename(os.path.dirname(path)) or "skill")
        base = re.sub(r"[^\w.-]", "-", base).lower()[:60]
        if len(base) < 3:
            return
        with lock:
            name = base
            if name in names:
                return
            names.add(name)
        d = os.path.join(OUT, name)
        try:
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            return
        dm = FM_DESC.search(text)
        desc = re.sub(r"\s+", " ", dm.group(1)).strip()[:200] if dm else f"Skill dari {slug}"
        with lock:
            grows["ins"] += 1
            conn.execute("INSERT INTO skills(name,description,tier,category,path,source) "
                         "VALUES(?,?,?,?,?,?)",
                         (name, desc, "curated", "mined", os.path.join(d, "SKILL.md"),
                          f"github/{slug}"))
            added += 1
            if grows["ins"] % 20 == 0:
                conn.commit()

    def plan(slug):
        tree = api(f"https://api.github.com/repos/{slug}/git/trees/HEAD?recursive=1", tok)
        with lock:
            plan.stat["n"] += 1
            if plan.stat["n"] % 50 == 0:
                print(f"  ..tree {plan.stat['n']} repo dipindai", flush=True)
        if not tree:
            return []
        return [(slug, it["path"]) for it in tree.get("tree", [])
                if it.get("type") == "blob" and it["path"].endswith("SKILL.md")
                and it.get("size", 1) < 200_000]

    plan.stat = {"n": 0}
    batch = 200
    while todo and total + added < args.target and time.time() - start < args.minutes * 60:
        chunk, todo = todo[:batch], todo[batch:]
        with ThreadPoolExecutor(max_workers=args.tree_workers) as ex:
            lists = list(ex.map(plan, chunk))
        items = [x for sub in lists for x in sub]
        with ThreadPoolExecutor(max_workers=args.dl_workers) as ex:
            list(ex.map(handle, items))
        conn.commit()
        st["done"] = list(done | set(chunk))
        st["skills"] = st.get("skills", 0) + added
        st["repos"] = len(st["done"])
        save_state(st)
        done |= set(chunk)
        total = conn.execute("SELECT COUNT(*) FROM skills").fetchone()[0]
        print(f"[grow] repo={len(done)} · skill total={total} · +sesi={added} · ditolak_scan={fails}",
              flush=True)
    conn.commit()
    print(f"[grow] selesai: total={conn.execute('SELECT COUNT(*) FROM skills').fetchone()[0]}", flush=True)


if __name__ == "__main__":
    main()
