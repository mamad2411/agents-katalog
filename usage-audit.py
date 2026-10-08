#!/usr/bin/env python3
"""usage-audit.py — laporan token Claude Code dari transcript lokal (read-only).

Latar: limit harian/mingguan terasa "cepat habis" bukan karena model boros,
tapi karena sesi panjang (konteks ±500k token/pesan). Skrip ini mengukur ulang
dari ~/.claude/projects/*.jsonl supaya terlihat SEBELUM limit jebol.

Pakai:
  python3 ~/.agents/usage-audit.py                 # 7 hari + top sesi + peringatan
  python3 ~/.agents/usage-audit.py --days 14 --top 8
  python3 ~/.agents/usage-audit.py --json          # keluaran mesin (idempoten)

Tanggal selalu UTC (aturan repo). Tidak menulis apa pun.
"""
import argparse
import collections
import datetime as dt
import glob
import json
import os
import sys

BASE = os.path.expanduser("~/.claude/projects")
WARN_MB = float(os.environ.get("CONTEXT_WARN_MB", "10"))


def human(n):
    if n >= 1e9:
        return "%.2f miliar" % (n / 1e9)
    if n >= 1e6:
        return "%.1f jt" % (n / 1e6)
    if n >= 1e3:
        return "%.1f rb" % (n / 1e3)
    return "%d" % n


def scan(days, top):
    daily = collections.Counter()
    models = collections.Counter()
    sess = []
    for path in glob.glob(os.path.join(BASE, "*", "*.jsonl")):
        try:
            size = os.path.getsize(path)
        except OSError:
            continue
        cr = cw = inn = out = 0
        msgs = 0
        last_ts = None
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                if '"usage"' not in line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("type") != "assistant":
                    continue
                msg = obj.get("message") or {}
                use = msg.get("usage") or {}
                if not use:
                    continue
                msgs += 1
                cr += use.get("cache_read_input_tokens", 0)
                cw += use.get("cache_creation_input_tokens", 0)
                inn += use.get("input_tokens", 0)
                out += use.get("output_tokens", 0)
                models[msg.get("model") or "?"] += (use.get("cache_read_input_tokens", 0)
                                                    + use.get("cache_creation_input_tokens", 0)
                                                    + use.get("input_tokens", 0)
                                                    + use.get("output_tokens", 0))
                day = (obj.get("timestamp") or "")[:10]
                last_ts = obj.get("timestamp") or last_ts
                if day:
                    daily[day] += (use.get("cache_read_input_tokens", 0)
                                   + use.get("cache_creation_input_tokens", 0)
                                   + use.get("input_tokens", 0)
                                   + use.get("output_tokens", 0))
        total = cr + cw + inn + out
        if msgs:
            sess.append({"mb": size / float(1 << 20), "tokens": total, "msgs": msgs,
                         "cache_read": cr, "ctx_per_msg": cr // max(msgs, 1),
                         "file": os.path.basename(path)[:36], "last": last_ts})
    sess.sort(key=lambda s: s["tokens"], reverse=True)
    cutoff = (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=days - 1)).isoformat()
    recent = {d: v for d, v in daily.items() if d >= cutoff}
    return {"daily": recent, "models": models, "sessions": sess[:top],
            "days": days, "all_sessions": sess}


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    data = scan(a.days, a.top)
    if a.json:
        print(json.dumps({"days": data["days"], "daily": data["daily"],
                          "top_sessions": data["sessions"],
                          "models": dict(data["models"].most_common(5))},
                         indent=1, ensure_ascii=False, sort_keys=True))
        return 0

    now = dt.datetime.now(dt.timezone.utc)
    print("=== Token Claude Code (%d hari terakhir, UTC; hari ini %s) ===" % (a.days, now.date()))
    if not data["daily"]:
        print("  (belum ada aktivitas pada rentang ini)")
    for d in sorted(data["daily"]):
        print("  %s  %10s token" % (d, human(data["daily"][d])))
    print("  %-10s %10s" % ("TOTAL", human(sum(data["daily"].values()))))

    print("\n=== Model (bobot terbesar dulu) ===")
    for m, t in data["models"].most_common(5):
        print("  %-26s %10s token" % (m, human(t)))

    print("\n=== Sesi paling boros (yang bikin limit cepat habis) ===")
    for s in data["sessions"]:
        flag = " <-- >%.0fMB, /clear!" % WARN_MB if s["mb"] >= WARN_MB else ""
        print("  %13s tok | %5d pesan | konteks/pesan %9s | %5.1f MB | %s%s"
              % (human(s["tokens"]), s["msgs"], human(s["ctx_per_msg"]),
                 s["mb"], s["file"], flag))

    over = [s for s in data["all_sessions"] if s["mb"] >= WARN_MB]
    print("\nSesi di atas %.0f MB: %d (masing-masing = tiap pesan baca ±0,5 jt token)"
          % (WARN_MB, len(over)))
    print("Aksi: /clear di batas tugas · jangan --resume · guard otomatis: python3 ~/.agents/context-guard.py --report")
    return 0


if __name__ == "__main__":
    sys.exit(main())
