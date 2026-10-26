#!/usr/bin/env python3
"""opencode-limit-guard.py — deteksi & cegah kena rate limit model free opencode.

Sumber data (semua lokal, tanpa API):
  log  : ~/.local/share/opencode/log/opencode.log   -> event 429 / rate_limit
  db   : ~/.local/share/opencode/opencode.db        -> token terpakai (rolling window)

Contoh:
    python3 ~/.agents/opencode-limit-guard.py                # status 24 jam
    python3 ~/.agents/opencode-limit-guard.py --days 7
    python3 ~/.agents/opencode-limit-guard.py --watch        # pantau live
    python3 ~/.agents/opencode-limit-guard.py --budget 20    # warning >20M token / 5 jam

Exit code: 0 aman, 2 kalau ada limit hit dalam periode (bisa dipakai hook/CI).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

LOG = os.path.expanduser("~/.local/share/opencode/log/opencode.log")
DB = os.path.expanduser("~/.local/share/opencode/opencode.db")

RE_TS = re.compile(r"timestamp=(\S+)")
RE_PROV = re.compile(r"providerID=([^\s]+)")
RE_MODEL = re.compile(r"modelID=([^\s]+)")
RE_SESSION = re.compile(r"session\.id=([^\s]+)")
RE_LIMIT = re.compile(r"\b429\b|rate[ _-]?limit|too many requests|quota", re.I)

SUGGEST = {
    "mimo-v2.6-flash-free": "glm-5.3-flash-free / deepseek-v4.1-flash-free",
    "glm-5.3-flash-free": "mimo-v2.6-flash-free / deepseek-v4.1-flash-free",
    "deepseek-v4.1-flash-free": "glm-5.3-flash-free / mimo-v2.6-flash-free",
}


def human(n: int) -> str:
    for unit, div in (("B", 10**9), ("M", 10**6), ("k", 10**3)):
        if abs(n) >= div:
            return f"{n / div:.1f}{unit}"
    return str(n)


def parse_log(since: datetime):
    hits = []
    if not os.path.exists(LOG):
        return hits
    with open(LOG, "r", errors="ignore") as f:
        for line in f:
            if not RE_LIMIT.search(line):
                continue
            m = RE_TS.search(line)
            ts = None
            if m:
                try:
                    ts = datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))
                except ValueError:
                    ts = None
            if ts and ts < since:
                continue
            prov = RE_PROV.search(line)
            model = RE_MODEL.search(line)
            sess = RE_SESSION.search(line)
            hits.append(
                {
                    "ts": ts,
                    "provider": prov.group(1) if prov else "?",
                    "model": model.group(1) if model else "?",
                    "session": sess.group(1) if sess else "?",
                    "raw": line.strip()[:160],
                }
            )
    return hits


def usage_window(hours: float):
    """Token terpakai per model dalam N jam terakhir."""
    if not os.path.exists(DB):
        return {}, 0
    since_ms = int((datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp() * 1000)
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=5)
    per_model = defaultdict(int)
    total = 0
    for (data,) in con.execute(
        "select data from message where time_created >= ?", (since_ms,)
    ):
        try:
            d = json.loads(data)
        except (ValueError, TypeError):
            continue
        if d.get("role") != "assistant":
            continue
        t = int((d.get("tokens") or {}).get("total") or 0)
        per_model[d.get("modelID") or "?"] += t
        total += t
    con.close()
    return per_model, total


def status(days: int, budget: float):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    hits = parse_log(since)
    per_model, win_total = usage_window(5)
    per_model_24, total_24 = usage_window(24)

    print(f"opencode limit guard — {days} hari terakhir")
    print(f"  log : {LOG}")
    print()
    print(f"  limit hit (429/rate-limit) : {len(hits)}")
    if hits:
        last = hits[-1]
        when = last["ts"].astimezone().strftime("%Y-%m-%d %H:%M") if last["ts"] else "?"
        print(f"  terakhir kena              : {when} · {last['provider']}/{last['model']}")
        c = Counter(f"{h['provider']}/{h['model']}" for h in hits)
        for k, v in c.most_common(6):
            print(f"    - {k:<40} {v}x")
    print()
    print(f"  token 5 jam terakhir       : {human(win_total)}")
    for m, v in sorted(per_model.items(), key=lambda kv: -kv[1])[:5]:
        print(f"    - {m:<40} {human(v)}")
    print(f"  token 24 jam terakhir      : {human(total_24)}")
    for m, v in sorted(per_model_24.items(), key=lambda kv: -kv[1])[:5]:
        print(f"    - {m:<40} {human(v)}")

    warn = []
    if budget and win_total > budget * 10**6:
        warn.append(f"token 5 jam ({human(win_total)}) sudah lewat budget {budget}M")
    for h in hits[-3:]:
        m = h["model"]
        if m in SUGGEST:
            warn.append(f"{m} kena limit -> pindah ke {SUGGEST[m]}")
    if warn:
        print("\n  SARAN")
        for w in dict.fromkeys(warn):
            print(f"    ! {w}")
    else:
        print("\n  aman, belum ada tanda limit.")
    return 2 if hits else 0


def rpm_report(days: int) -> int:
    """Apakah 429-mu disebabkan RPM (request/menit) atau bukan."""
    from collections import Counter

    if not os.path.exists(DB):
        sys.exit(f"DB tidak ada: {DB}")
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    per_min = Counter()
    for (ts,) in con.execute(
        "select time_created from message where json_extract(data,'$.role')='assistant'"
    ):
        per_min[datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M")] += 1
    con.close()

    vals = sorted(per_min.values())
    if not vals:
        sys.exit("Belum ada data request.")
    q = lambda f: vals[min(len(vals) - 1, int(len(vals) * f))]
    print(f"POLA REQUEST/MENIT — {days} hari")
    print(f"  menit aktif : {len(per_min)}")
    print(f"  RPM p50 {q(.5)} · p90 {q(.9)} · p99 {q(.99)} · max {vals[-1]}")
    print("\n  menit terpadat:")
    for m, c in per_min.most_common(5):
        print(f"    {m}  {c:>3} req")

    hits = parse_log(datetime.now(timezone.utc) - timedelta(days=days))
    print(f"\n  429 dalam periode: {len(hits)}")
    if hits:
        rows = []
        for h in hits:
            k = h["ts"].astimezone().strftime("%Y-%m-%d %H:%M") if h["ts"] else "?"
            rows.append(per_min.get(k, 0))
        zero = sum(1 for r in rows if r == 0)
        prev = [per_min.get((h["ts"] - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M"), 0)
                if h["ts"] else 0 for h in hits]
        med_prev = sorted(prev)[len(prev) // 2]
        burst = sum(1 for p in prev if p >= 5)
        print(f"  RPM saat 429      : median {sorted(rows)[len(rows)//2]}, 0 req {zero}/{len(rows)}")
        print(f"  RPM menit sebelum : median {med_prev}, >=5 req {burst}/{len(rows)}")
        print("\n  KESIMPULAN")
        if burst < len(rows) * 0.3:
            print("    -> BUKAN RPM / bukan burst. 429 datang walau trafik rendah,")
            print("       artinya kuota provider sudah habis atau provider agregator")
            print("       (smart / or-free / omniroute) yang menolak.")
            print("       Throttle request TIDAK akan menolong; ganti model/provider.")
        else:
            print("    -> pola cocok RPM/burst: 429 muncul setelah request menumpuk.")
            print("       Solusi: jeda antar request, kurangi tool call per tugas,")
            print("       atau pecah kerjaan jadi beberapa sesi.")
    print("\n  catatan: RPM dihitung dari pesan assistant yang berhasil (request sukses).")
    return 0


def watch(interval: int, budget: float):
    print(f"Memantau {LOG} tiap {interval}s (Ctrl-C untuk stop)...")
    seen = len(parse_log(datetime.now(timezone.utc) - timedelta(days=30)))
    warned_win = False
    while True:
        try:
            hits = parse_log(datetime.now(timezone.utc) - timedelta(days=30))
            if len(hits) > seen:
                for h in hits[seen:]:
                    when = h["ts"].astimezone().strftime("%H:%M:%S") if h["ts"] else "--:--:--"
                    print(f"[{when}] LIMIT {h['provider']}/{h['model']}")
                    sug = SUGGEST.get(h["model"])
                    if sug:
                        print(f"           -> ganti model: {sug}")
                seen = len(hits)
            if budget:
                _, win = usage_window(5)
                if win > budget * 10**6 and not warned_win:
                    print(f"[!] token 5 jam = {human(win)} (> {budget}M) — pertimbangkan sesi baru / model lain")
                    warned_win = True
                elif win <= budget * 10**6 * 0.8:
                    warned_win = False
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nstop.")
            return 0


def main():
    ap = argparse.ArgumentParser(description="Deteksi & cegah rate limit opencode")
    ap.add_argument("--days", type=int, default=1)
    ap.add_argument("--budget", type=float, default=0,
                    help="warning kalau token 5 jam > N juta (0 = mati)")
    ap.add_argument("--rpm", action="store_true", help="analisis pola request/menit + korelasi 429")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--interval", type=int, default=5)
    args = ap.parse_args()
    if args.rpm:
        sys.exit(rpm_report(args.days))
    if args.watch:
        sys.exit(watch(args.interval, args.budget))
    sys.exit(status(args.days, args.budget))


if __name__ == "__main__":
    main()
