#!/usr/bin/env python3
"""audit-opencode.py — hitung token & biaya opencode dari DB lokal.

Sumber: ~/.local/share/opencode/opencode.db
        tabel `message`, kolom `data` (JSON): tokens{input,output,reasoning,cache.read/write}, cost
        tabel `session`: title, directory

Tanpa API, tanpa akun. DB dibuka read-only supaya tidak mengganggu opencode
yang sedang jalan.

Contoh:
    python3 ~/.agents/audit-opencode.py                 # 7 hari terakhir
    python3 ~/.agents/audit-opencode.py --days 30
    python3 ~/.agents/audit-opencode.py --all
    python3 ~/.agents/audit-opencode.py --json
    python3 ~/.agents/audit-opencode.py --session ses_xxx
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timedelta

DB_DEFAULT = os.path.expanduser("~/.local/share/opencode/opencode.db")


def rupiah(n: float) -> str:
    return f"${n:,.4f}"


def human(n: int) -> str:
    for unit, div in (("B", 1_000_000_000), ("M", 1_000_000), ("k", 1_000)):
        if abs(n) >= div:
            return f"{n / div:.1f}{unit}"
    return str(n)


def load(db_path: str, since_ms: int | None, session_filter: str | None):
    if not os.path.exists(db_path):
        sys.exit(f"DB tidak ditemukan: {db_path}\n(opencode belum pernah jalan?)")
    uri = f"file:{db_path}?mode=ro"
    con = sqlite3.connect(uri, uri=True, timeout=5)
    cur = con.cursor()

    titles, dirs = {}, {}
    try:
        for sid, title, directory in cur.execute("select id, title, directory from session"):
            titles[sid] = title or "(tanpa judul)"
            dirs[sid] = directory or ""
    except sqlite3.Error:
        pass

    rows = []
    q = "select session_id, time_created, data from message"
    for sid, ts, data in cur.execute(q):
        if session_filter and sid != session_filter:
            continue
        if since_ms is not None and ts < since_ms:
            continue
        try:
            d = json.loads(data)
        except (ValueError, TypeError):
            continue
        if d.get("role") != "assistant":
            continue
        tok = d.get("tokens") or {}
        cache = tok.get("cache") or {}
        rows.append(
            {
                "session": sid,
                "ts": ts,
                "model": d.get("modelID") or "?",
                "provider": d.get("providerID") or "?",
                "input": int(tok.get("input") or 0),
                "output": int(tok.get("output") or 0),
                "reasoning": int(tok.get("reasoning") or 0),
                "cache_read": int(cache.get("read") or 0),
                "cache_write": int(cache.get("write") or 0),
                "total": int(tok.get("total") or 0),
                "cost": float(d.get("cost") or 0.0),
            }
        )
    con.close()
    return rows, titles, dirs


def agg(rows, keyfn):
    out = defaultdict(lambda: {"msgs": 0, "input": 0, "output": 0, "reasoning": 0,
                               "cache_read": 0, "total": 0, "cost": 0.0})
    for r in rows:
        a = out[keyfn(r)]
        a["msgs"] += 1
        for f in ("input", "output", "reasoning", "cache_read", "total"):
            a[f] += r[f]
        a["cost"] += r["cost"]
    return out


def table(headers, data, aligns=None):
    aligns = aligns or ["<"] * len(headers)
    cols = len(headers)
    widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    line = "  ".join(f"{headers[i]:{aligns[i]}{widths[i]}}" for i in range(cols))
    print(line)
    print("  ".join("-" * widths[i] for i in range(cols)))
    for row in data:
        print("  ".join(f"{str(cell):{aligns[i]}{widths[i]}}" for i, cell in enumerate(row)))


def main():
    ap = argparse.ArgumentParser(description="Audit token/biaya opencode dari DB lokal")
    ap.add_argument("--db", default=DB_DEFAULT)
    ap.add_argument("--days", type=int, default=7, help="rentang hari (default 7)")
    ap.add_argument("--all", action="store_true", help="semua data, abaikan --days")
    ap.add_argument("--session", help="filter satu session id")
    ap.add_argument("--top", type=int, default=8, help="jumlah baris tabel (default 8)")
    ap.add_argument("--json", action="store_true", help="keluarkan JSON")
    args = ap.parse_args()

    since = None
    label = "semua waktu"
    if not args.all:
        since = int((datetime.now() - timedelta(days=args.days)).timestamp() * 1000)
        label = f"{args.days} hari terakhir"

    rows, titles, dirs = load(args.db, since, args.session)
    if not rows:
        print(f"Tidak ada data assistant untuk {label}.")
        return

    tot = {k: sum(r[k] for r in rows) for k in
           ("input", "output", "reasoning", "cache_read", "cache_write", "total")}
    cost = sum(r["cost"] for r in rows)
    per_day = agg(rows, lambda r: datetime.fromtimestamp(r["ts"] / 1000).strftime("%Y-%m-%d"))
    per_model = agg(rows, lambda r: f'{r["provider"]}/{r["model"]}')
    per_sess = agg(rows, lambda r: r["session"])

    cache_denom = tot["input"] + tot["cache_read"]
    cache_hit = (tot["cache_read"] / cache_denom * 100) if cache_denom else 0.0
    avg_ctx = tot["total"] / len(rows)

    if args.json:
        print(json.dumps(
            {
                "range": label,
                "messages": len(rows),
                "tokens": tot,
                "cost_usd": round(cost, 6),
                "cache_hit_pct": round(cache_hit, 2),
                "avg_tokens_per_message": round(avg_ctx, 1),
                "per_day": {k: v for k, v in sorted(per_day.items())},
                "per_model": dict(sorted(per_model.items(), key=lambda kv: -kv[1]["total"])),
                "per_session": dict(sorted(per_sess.items(), key=lambda kv: -kv[1]["total"])),
            },
            indent=2,
        ))
        return

    print(f"opencode token audit — {label}")
    print(f"DB: {args.db}")
    print()
    print(f"  pesan assistant : {len(rows):,}")
    print(f"  sesi            : {len(per_sess):,}")
    print(f"  total token     : {tot['total']:,}  ({human(tot['total'])})")
    print(f"    input         : {tot['input']:,}")
    print(f"    output        : {tot['output']:,}")
    print(f"    reasoning     : {tot['reasoning']:,}")
    print(f"    cache read    : {tot['cache_read']:,}")
    print(f"    cache write   : {tot['cache_write']:,}")
    print(f"  biaya tercatat  : {rupiah(cost)}")
    print(f"  cache hit rate  : {cache_hit:.1f}%   (cache_read / (input + cache_read))")
    print(f"  rata2 / pesan   : {avg_ctx:,.0f} token")

    print("\nPER HARI")
    table(
        ["tanggal", "pesan", "total token", "cache hit"],
        [
            [d, f"{v['msgs']:,}", human(v["total"]),
             f"{(v['cache_read'] / (v['input'] + v['cache_read']) * 100 if (v['input'] + v['cache_read']) else 0):.0f}%"]
            for d, v in sorted(per_day.items(), reverse=True)[: args.top]
        ],
        ["<", ">", ">", ">"],
    )

    print("\nPER MODEL")
    table(
        ["model", "pesan", "input", "output", "cache read", "total", "biaya"],
        [
            [m, f"{v['msgs']:,}", human(v["input"]), human(v["output"]),
             human(v["cache_read"]), human(v["total"]), rupiah(v["cost"])]
            for m, v in sorted(per_model.items(), key=lambda kv: -kv[1]["total"])[: args.top]
        ],
        ["<", ">", ">", ">", ">", ">", ">"],
    )

    print("\nTOP SESI (paling boros)")
    table(
        ["total", "pesan", "judul", "folder"],
        [
            [human(v["total"]), f"{v['msgs']:,}",
             (titles.get(s, s)[:38] + ("…" if len(titles.get(s, s)) > 38 else "")),
             os.path.basename(dirs.get(s, "")) or "-"]
            for s, v in sorted(per_sess.items(), key=lambda kv: -kv[1]["total"])[: args.top]
        ],
        [">", ">", "<", "<"],
    )


if __name__ == "__main__":
    main()
