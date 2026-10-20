#!/usr/bin/env python3
"""retrieve.py — pencarian hybrid (BM25/FTS5 + rerank leksikal) satu pintu.

Pakai:  python3 retrieve.py "code review" [-k 5] [--kind agents] [--json]

Sumber: retrieve.db (dibuat oleh build-retrieve-index.py) = skill + cap + mcp.
Tujuan: AI ambil 3-5 aset paling relevan, bukan memuat semuanya (hemat token).

Tiga lapisan (tanpa dependency eksternal, tetap jalan di mesin 8 GB):
  1. BM25 ber-bobot kolom  — name 8x, body 1x (FTS5 bm25(assets, ...))
  2. Kandidat pool 60      — AND dulu, fallback OR kalau hasil terlalu sedikit
  3. Rerank leksikal       — exact/prefix name, phrase, coverage token, bm25, stars
Plus dedupe nama: 205k skill hasil mining banyak yang nama sama dari repo berbeda.
"""
import json, math, os, re, sqlite3, sys
from pathlib import Path

DB = Path.home() / ".agents" / "retrieve.db"
POOL = 60

# bobot kolom FTS5: name, body, kind, source, path, id  (stars = UNINDEXED)
W_NAME, W_BODY, W_KIND, W_SRC, W_PATH, W_ID = 8.0, 1.0, 0.5, 0.3, 0.0, 0.0

# query expansion ID -> EN: katalog isinya bahasa Inggris, query-nya sering Indonesia
SYN = {
    "hemat": "save compress reduce budget", "irit": "save compress budget",
    "token": "token context", "konteks": "context window",
    "kode": "code", "coding": "code", "program": "code",
    "uji": "test testing", "tes": "test", "pengujian": "testing",
    "perbaiki": "fix debug repair", "bug": "bug debug", "error": "error debug",
    "hapus": "delete remove cleanup", "bersih": "clean cleanup lint",
    "buat": "create build generate", "bikin": "create build generate",
    "desain": "design ui ux", "tampilan": "ui design frontend",
    "keamanan": "security secure audit", "aman": "secure safety",
    "cari": "search find", "riset": "research search",
    "dokumen": "document doc", "tulis": "write writing",
    "rapikan": "refactor format clean", "struktur": "structure refactor",
    "deploy": "deploy deployment", "pasang": "install setup",
    "atur": "config configure setup", "konfigurasi": "config configure",
    "optimasi": "optimize optimization performance", "cepat": "fast performance",
    "lambat": "slow performance optimize", "database": "database db sql",
    "gambar": "image picture", "video": "video", "suara": "audio voice",
    "agen": "agent", "otomatis": "automation automate",
    "laporan": "report", "jadwal": "schedule cron",
}


def _tokens(q):
    return [t.lower() for t in re.split(r"[^0-9A-Za-z]+", q or "") if len(t) > 1][:12]


def _expand(toks):
    """tiap token -> grup (token asli OR sinonim EN)."""
    groups = []
    for t in toks:
        alts = [t] + [w for w in SYN.get(t, "").split() if w != t]
        groups.append("(" + " OR ".join('"%s"' % w for w in alts) + ")")
    return groups


def _fts_query(q, mode="or"):
    toks = _tokens(q)
    if not toks:
        return ""
    groups = _expand(toks)
    if mode == "and":
        return " AND ".join(groups)
    flat = []
    for g in groups:
        flat.extend(re.findall(r'"([^"]+)"', g))
    return " OR ".join('"%s"' % w for w in flat)


def _norm(s):
    return " ".join(re.split(r"[^0-9a-z]+", (s or "").lower())).strip()


def _fetch(conn, fq, kind, limit):
    sql = ("SELECT name,kind,source,path,id,stars,substr(body,1,1500) b,"
           "bm25(assets,?,?,?,?,?,?) s FROM assets WHERE assets MATCH ?")
    params = [W_NAME, W_BODY, W_KIND, W_SRC, W_PATH, W_ID, fq]
    if kind:
        sql += " AND kind = ?"
        params.append(kind)
    sql += " ORDER BY s LIMIT ?"
    params.append(limit)
    return conn.execute(sql, params).fetchall()


def _rerank(rows, q):
    toks = _tokens(q)
    if not toks:
        return []
    qn = _norm(q)
    qt = set(toks)
    qx = set(qt)
    for t in toks:
        qx.update(SYN.get(t, "").split())
    extra = qx - qt
    if not rows:
        return []
    bms = [r[7] for r in rows]
    lo, hi = min(bms), max(bms)
    span = (hi - lo) or 1.0

    scored = []
    for name, kd, src, path, aid, stars, body, s in rows:
        nn = _norm(name)
        ntok = set(nn.split())
        btok = set(_norm(body).split())
        nb = 1.0 - (s - lo) / span                     # bm25 -> 0..1 (1 = terbaik)
        cov_n = len(qt & ntok) / len(qt)
        cov_b = len(qt & btok) / len(qt)
        cov_x = (len(extra & btok) / len(extra)) if extra else 0.0
        exact = 1.0 if nn == qn else 0.0
        phrase = 1.0 if qn and (" %s " % qn) in (" %s " % nn) else 0.0
        allin = 1.0 if qt <= ntok else 0.0
        star = min(math.log1p(stars or 0) / 12.0, 0.1)
        score = (1.6 * nb + 1.2 * cov_n + 1.0 * exact + 0.6 * phrase
                 + 0.4 * allin + 0.3 * cov_b + 0.25 * cov_x + star)
        scored.append((score, name, kd, src, path, aid, stars, s))

    scored.sort(key=lambda x: -x[0])
    return scored


def search(query, k=5, kind=None, pool=POOL):
    if not DB.exists():
        return []
    conn = sqlite3.connect(DB)
    try:
        rows = _fetch(conn, _fts_query(query, "and"), kind, pool)
        if len(rows) < max(8, k * 3):                  # AND terlalu sempit -> tambah OR
            seen = {r[4] for r in rows}
            rows += [r for r in _fetch(conn, _fts_query(query, "or"), kind, pool)
                     if r[4] not in seen]
    except Exception:
        return []
    finally:
        conn.close()

    out, seen_name = [], set()
    for score, name, kd, src, path, aid, stars, _ in _rerank(rows, query):
        key = (_norm(name), kd)
        if key in seen_name:                           # duplikat hasil mining
            continue
        seen_name.add(key)
        out.append({"name": name, "kind": kd, "source": src, "path": path,
                    "id": aid, "stars": stars, "score": round(score, 3)})
        if len(out) >= k:
            break
    return out


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
