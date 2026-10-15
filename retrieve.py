#!/usr/bin/env python3
"""retrieve.py — pencarian hybrid (BM25/FTS5) satu pintu untuk SEMUA aset.

Pakai:  python3 retrieve.py "code review" [-k 5] [--kind agents] [--json]

Sumber: retrieve.db (dibuat oleh build-retrieve-index.py) = skill + cap + mcp.
Tujuan: AI ambil 3-5 aset paling relevan, bukan memuat semuanya (hemat token).
"""
import json, os, re, sqlite3, sys
from pathlib import Path

DB = Path.home() / ".agents" / "retrieve.db"


def _fts_query(q):
    toks = [t for t in re.split(r"[^0-9A-Za-z]+", q or "") if len(t) > 1]
    return " OR ".join('"%s"' % t for t in toks[:12])


def search(query, k=5, kind=None):
    if not DB.exists():
        return []
    fq = _fts_query(query)
    if not fq:
        return []
    conn = sqlite3.connect(DB)
    try:
        if kind:
            cur = conn.execute(
                "SELECT name,kind,source,path,id,stars,bm25(assets) s "
                "FROM assets WHERE assets MATCH ? AND kind = ? ORDER BY s LIMIT ?",
                (fq, kind, k))
        else:
            cur = conn.execute(
                "SELECT name,kind,source,path,id,stars,bm25(assets) s "
                "FROM assets WHERE assets MATCH ? ORDER BY s LIMIT ?",
                (fq, k))
        out = []
        for name, kd, src, path, aid, stars, s in cur.fetchall():
            out.append({"name": name, "kind": kd, "source": src, "path": path,
                        "id": aid, "stars": stars, "score": round(-s, 3)})
        return out
    except Exception:
        return []
    finally:
        conn.close()


def main():
    args = sys.argv[1:]
    if not args:
        print("pakai: retrieve.py \"query\" [-k N] [--kind X] [--json]")
        return
    query = args[0]
    k = 5
    kind = None
    as_json = "--json" in args
    if "-k" in args:
        try:
            k = int(args[args.index("-k") + 1])
        except Exception:
            pass
    if "--kind" in args:
        kind = args[args.index("--kind") + 1]
    res = search(query, k, kind)
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return
    if not res:
        print("(tidak ada hasil)")
        return
    for i, r in enumerate(res, 1):
        print("%d. [%s] %s  (★%s, %s)  score=%.2f"
              % (i, r["kind"], r["name"], r["stars"], r["source"], r["score"]))


if __name__ == "__main__":
    main()
