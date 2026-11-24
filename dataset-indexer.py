#!/usr/bin/env python3
"""dataset-indexer — bangun indeks metadata dataset publik (target 100k+).

Sumber (semua tanpa API key):
  - HuggingFace Hub API: ~1 juta+ dataset, metadata saja
  - OpenML API: ~6rb dataset ML
  - data.gov CKAN API: ratusan ribu dataset pemerintah AS

Output: ~/.agents/datasets-index.db (SQLite + FTS5)
Jalan resumable — aman diulang, skip yang sudah ada.
"""
import json
import os
import sqlite3
import sys
import time
import urllib.parse
import urllib.request

DB = os.path.expanduser("~/.agents/datasets-index.db")
UA = {"User-Agent": "dataset-indexer/1.0"}


def init_db():
    c = sqlite3.connect(DB, timeout=60)
    c.execute("CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT)")
    c.execute("""CREATE TABLE IF NOT EXISTS ds(
        source TEXT, slug TEXT, name TEXT, descr TEXT,
        tags TEXT, downloads INTEGER, extra TEXT,
        PRIMARY KEY(source, slug))""")
    c.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS ds_fts USING fts5(
        name, descr, tags, content='ds', content_rowid='rowid')""")
    # sinkronisasi FTS bila tabel ds sudah ada sebelumnya
    n = c.execute("SELECT count(*) FROM ds_fts").fetchone()[0]
    if n == 0:
        c.execute("INSERT INTO ds_fts(rowid,name,descr,tags) SELECT rowid,name,descr,tags FROM ds")
    c.commit()
    return c


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def add(c, source, slug, name, descr, tags, downloads, extra=""):
    try:
        c.execute("INSERT OR IGNORE INTO ds VALUES(?,?,?,?,?,?,?)",
                  (source, slug, name or "", (descr or "")[:500],
                   tags or "", int(downloads or 0), extra[:500]))
    except sqlite3.Error:
        pass


def rebuild_fts(c):
    """Rebuild FTS5 dari tabel ds (dipanggil di akhir / incremental)."""
    c.execute("DELETE FROM ds_fts")
    c.execute("INSERT INTO ds_fts(rowid,name,descr,tags) SELECT rowid,name,descr,tags FROM ds")
    c.commit()


# ---------- Sumber 1: HuggingFace ----------
def index_hf(c, limit=950000, page=1000):
    """HF API: skip deprecated -> pagination via header Link rel=next (cursor).
    Cursor disimpan di meta supaya bisa resume tanpa ulang dari awal."""
    done, errs = 0, 0
    cur = c.execute("SELECT v FROM meta WHERE k='hf_cursor'").fetchone()
    if cur:
        url = cur[0]
        print(f"[hf] resume dari cursor tersimpan", flush=True)
    else:
        url = ("https://huggingface.co/api/datasets?limit=%d"
               "&sort=downloads&direction=-1") % page
    while done < limit and url:
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                rows = json.loads(r.read())
                link = r.headers.get("Link", "")
            errs = 0
        except Exception as e:
            errs += 1
            print(f"[hf] error @{done} ({errs}x): {e}", flush=True)
            if errs >= 10:
                break
            time.sleep(5)
            continue
        if not rows:
            break
        for r in rows:
            slug = r.get("id", "")
            tags = ",".join(r.get("tags", [])[:12])
            cd = r.get("cardData") or {}
            add(c, "hf", slug, r.get("id", ""),
                r.get("description") or cd.get("dataset_summary", ""),
                tags, r.get("downloads", 0),
                f"likes={r.get('likes',0)} gated={r.get('gated',False)}")
        c.commit()
        done += len(rows)
        if done % 10000 == 0:
            print(f"[hf] {done} dataset...", flush=True)
        if len(rows) < page:
            break
        # cursor berikutnya dari header Link
        nxt = ""
        for part in link.split(","):
            if 'rel="next"' in part:
                nxt = part.split("<")[1].split(">")[0]
        if nxt:
            c.execute("INSERT OR REPLACE INTO meta VALUES('hf_cursor',?)", (nxt,))
            c.commit()
        url = nxt
        time.sleep(0.3)
    print(f"[hf] selesai: {done}", flush=True)


# ---------- Sumber 2: OpenML ----------
def index_openml(c):
    try:
        d = fetch("https://www.openml.org/api/v1/json/data/list?limit=20000", timeout=120)
        rows = d.get("data", {}).get("dataset", [])
        for r in rows:
            did = r.get("did") or r.get("dataset_id")
            add(c, "openml", str(did), r.get("name", ""),
                (r.get("description") or "")[:500],
                ",".join(r.get("tag", [])[:12]) if isinstance(r.get("tag"), list) else str(r.get("tag", "")),
                r.get("n_instances") or 0, f"n_features={r.get('n_features','')}")
        c.commit()
        print(f"[openml] {len(rows)} dataset", flush=True)
    except Exception as e:
        print(f"[openml] error: {e}", flush=True)


# ---------- Sumber 3: Zenodo (786rb+ dataset, DOI) ----------
def index_zenodo(c, limit=5000, page=25):
    done = 0
    while done < limit:
        url = ("https://zenodo.org/api/records?q=type:dataset"
               f"&size={page}&sort=mostviewed&offset={done}")
        try:
            d = fetch(url, timeout=90)
        except Exception as e:
            print(f"[zenodo] error offset={done}: {e}", flush=True)
            time.sleep(5)
            continue
        hits = d.get("hits", {}).get("hits", [])
        if not hits:
            break
        for h in hits:
            md = h.get("metadata", {})
            rid = h.get("id", "")
            desc = md.get("description", "") or ""
            # buang HTML biar FTS bersih
            import re as _re
            desc = _re.sub(r"<[^>]+>", " ", desc)
            subs = md.get("subjects", [])
            tags = ",".join((s.get("subject", "") if isinstance(s, dict) else str(s))
                            for s in subs[:12])
            creators = ",".join((cr.get("name", "") for cr in (md.get("creators") or [])[:5] if isinstance(cr, dict)))
            add(c, "zenodo", str(rid), md.get("title", ""), desc[:500],
                tags, h.get("stats", {}).get("views", 0),
                f"doi={md.get('doi','')} creators={creators[:150]}")
        c.commit()
        done += len(hits)
        if done % 5000 == 0:
            print(f"[zenodo] {done}...", flush=True)
        if len(hits) < page:
            break
        time.sleep(0.5)
    print(f"[zenodo] selesai: {done}", flush=True)


def main():
    c = init_db()
    which = sys.argv[1:] or ["hf", "openml", "zenodo"]
    if "hf" in which:
        index_hf(c)
    if "openml" in which:
        index_openml(c)
    if "zenodo" in which or "datagov" in which:
        index_zenodo(c)
    rebuild_fts(c)
    total = c.execute("SELECT count(*) FROM ds").fetchone()[0]
    per = c.execute("SELECT source,count(*) FROM ds GROUP BY source").fetchall()
    print(f"TOTAL: {total} dataset | {per}", flush=True)


if __name__ == "__main__":
    main()
