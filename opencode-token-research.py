#!/usr/bin/env python3
"""opencode-token-research.py — riset mendalam ke mana token opencode pergi.

Beda dengan audit-opencode.py (ringkasan cepat), script ini dipakai untuk
analisis: efisiensi per model, tren, deteksi pemborosan, tool mana yang mahal,
dan estimasi biaya kalau pakai model berbayar.

Sumber (lokal, read-only):
  ~/.local/share/opencode/opencode.db
    message : data JSON -> role, tokens{input,output,reasoning,cache.read/write,total}, cost, modelID
    part    : data JSON -> type (text/reasoning/tool/compaction/patch/step-*), tool
    session : title, directory

Contoh:
    python3 ~/.agents/opencode-token-research.py                  # 30 hari
    python3 ~/.agents/opencode-token-research.py --days 7
    python3 ~/.agents/opencode-token-research.py --all --md report.md
    python3 ~/.agents/opencode-token-research.py --json
    python3 ~/.agents/opencode-token-research.py --price-in 3 --price-out 15
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

DB_DEFAULT = os.path.expanduser("~/.local/share/opencode/opencode.db")
SPARK = "▁▂▃▄▅▆▇█"


def human(n: float) -> str:
    n = float(n)
    for unit, div in (("B", 1e9), ("M", 1e6), ("k", 1e3)):
        if abs(n) >= div:
            return f"{n / div:.1f}{unit}"
    return f"{n:.0f}"


def pct(a: float, b: float) -> str:
    return f"{(a / b * 100):.1f}%" if b else "0.0%"


def spark(vals):
    if not vals:
        return ""
    import math
    logs = [math.log10(max(v, 1)) for v in vals]
    lo, hi = min(logs), max(logs)
    if hi == lo:
        return SPARK[3] * len(vals)
    return "".join(SPARK[min(7, int((v - lo) / (hi - lo) * 7))] for v in logs)


def sess_label(sessions, sid):
    s = sessions.get(sid, {})
    title = (s.get("title") or "").strip()
    if not title or title.startswith("New session"):
        base = os.path.basename((s.get("dir") or "").rstrip("/"))
        return f"{base or sid} (tanpa judul)"
    return title


def table(headers, rows, aligns=None):
    aligns = aligns or ["<"] * len(headers)
    widths = [len(h) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(str(c)))
    print("  ".join(f"{headers[i]:{aligns[i]}{widths[i]}}" for i in range(len(headers))))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(f"{str(c):{aligns[i]}{widths[i]}}" for i, c in enumerate(r)))


def load(db, since_ms, session_filter):
    if not os.path.exists(db):
        sys.exit(f"DB tidak ditemukan: {db}")
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=5)

    sessions = {}
    for sid, title, directory, ts in con.execute(
        "select id, title, directory, time_created from session"
    ):
        sessions[sid] = {"title": title or "(tanpa judul)", "dir": directory or "", "ts": ts}

    msgs = []
    for mid, sid, ts, data in con.execute(
        "select id, session_id, time_created, data from message"
    ):
        if session_filter and sid != session_filter:
            continue
        if since_ms and ts < since_ms:
            continue
        try:
            d = json.loads(data)
        except (ValueError, TypeError):
            continue
        if d.get("role") != "assistant":
            continue
        t = d.get("tokens") or {}
        c = t.get("cache") or {}
        msgs.append(
            {
                "id": mid,
                "session": sid,
                "ts": ts,
                "model": d.get("modelID") or "?",
                "provider": d.get("providerID") or "?",
                "input": int(t.get("input") or 0),
                "output": int(t.get("output") or 0),
                "reasoning": int(t.get("reasoning") or 0),
                "cache_read": int(c.get("read") or 0),
                "cache_write": int(c.get("write") or 0),
                "total": int(t.get("total") or 0),
                "cost": float(d.get("cost") or 0.0),
            }
        )

    parts = defaultdict(Counter)
    tools = Counter()
    for sid, data in con.execute("select session_id, data from part"):
        if session_filter and sid != session_filter:
            continue
        try:
            d = json.loads(data)
        except (ValueError, TypeError):
            continue
        typ = d.get("type") or "?"
        parts[sid][typ] += 1
        if typ == "tool":
            tools[d.get("tool") or "?"] += 1
    con.close()
    return msgs, parts, tools, sessions


def ctx_now(db, session_id):
    """Perkiraan konteks request terakhir sebuah sesi (assistant terakhir yang punya token)."""
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    rows = con.execute(
        "select data from message where session_id = ? and "
        "json_extract(data,'$.role') = 'assistant' order by time_created desc limit 5",
        (session_id,),
    ).fetchall()
    con.close()
    for (data,) in rows:
        d = json.loads(data)
        t = d.get("tokens") or {}
        val = int(t.get("input") or 0) + int((t.get("cache") or {}).get("read") or 0) + int(t.get("output") or 0)
        if val:
            return val
    return 0


def do_reset_ctx(db, session_id, keep, archive, confirmed):
    """Arsipkan lalu buang pesan lama satu sesi supaya konteks kembali ~0."""
    import shutil
    import subprocess

    if not os.path.exists(db):
        sys.exit(f"DB tidak ditemukan: {db}")

    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    if not session_id:
        row = con.execute(
            "select session_id, count(*) c from message group by session_id order by c desc limit 1"
        ).fetchone()
        if not row:
            sys.exit("Tidak ada pesan.")
        session_id = row[0]
    title = con.execute("select title from session where id = ?", (session_id,)).fetchone()
    rows = con.execute(
        "select id, time_created from message where session_id = ? order by time_created",
        (session_id,),
    ).fetchall()
    con.close()
    if not rows:
        sys.exit(f"Sesi {session_id} tidak punya pesan.")

    drop = rows[: len(rows) - keep] if keep > 0 else list(rows)
    before = ctx_now(db, session_id)
    print("reset konteks sesi")
    print(f"  sesi        : {session_id}  {('· ' + title[0]) if title else ''}")
    print(f"  pesan total : {len(rows)}  (disimpan {len(rows) - len(drop)}, dibuang {len(drop)})")
    print(f"  konteks kini: {human(before)}")
    if not drop:
        print("  sudah di bawah batas --keep, tidak ada yang dibuang.")
        return
    if not confirmed:
        print("\n  Belum dieksekusi. Tambahkan --yes untuk jalan (backup otomatis dibuat).")
        return

    running = subprocess.run(["pgrep", "-x", "opencode"], capture_output=True, text=True)
    if running.stdout.strip():
        sys.exit("opencode masih jalan. Tutup dulu, lalu ulangi.")

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    arch = os.path.expanduser(archive) if archive else os.path.join(
        os.path.dirname(db), f"backup-ctx-{ts}")
    os.makedirs(arch, exist_ok=True)
    for suffix in ("", "-wal", "-shm"):
        src = db + suffix
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(arch, os.path.basename(src)))

    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    jsonl = os.path.join(arch, f"trimmed-{session_id}.jsonl")
    ids = [r[0] for r in drop]
    with open(jsonl, "w") as f:
        q = ("select id, time_created, data from message where session_id = ? "
             "order by time_created")
        for mid, tsc, data in con.execute(q, (session_id,)):
            if mid in ids:
                f.write(json.dumps({"id": mid, "ts": tsc, "data": json.loads(data)}) + "\n")
    con.close()

    con = sqlite3.connect(db, timeout=15)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()
    for mid in ids:
        cur.execute("delete from part where message_id = ?", (mid,))
        cur.execute("delete from message where id = ?", (mid,))
    # hitung ulang agregat sesi dari pesan yang tersisa
    agg = cur.execute(
        "select coalesce(sum(json_extract(data,'$.tokens.input')),0),"
        " coalesce(sum(json_extract(data,'$.tokens.output')),0),"
        " coalesce(sum(json_extract(data,'$.tokens.reasoning')),0),"
        " coalesce(sum(json_extract(data,'$.cost')),0)"
        " from message where session_id = ?", (session_id,)).fetchone()
    cur.execute("update session set tokens_input=?, tokens_output=?, tokens_reasoning=?, cost=?"
                " where id=?", (agg[0], agg[1], agg[2], agg[3], session_id))
    con.commit()
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    con.close()

    after = ctx_now(db, session_id)
    print(f"\n  selesai: konteks {human(before)} -> {human(after)}")
    print(f"  arsip pesan dibuang : {jsonl}")
    print(f"  backup DB           : {arch}/opencode.db")
    print("  catatan: konteks 0 baru terasa saat sesi dilanjutkan (request berikutnya)")


def do_limits(db, since_ms, days, top):
    """Riset kapasitas token model: batas resmi vs konteks terbesar yang benar-benar diterima."""
    cache = os.path.expanduser("~/.cache/opencode/models.json")
    if not os.path.exists(cache):
        cache = "/tmp/models.json"
    if not os.path.exists(cache):
        sys.exit("Cache model tidak ada. Jalankan opencode sekali atau unduh models.dev/api.json")
    meta = json.load(open(cache))

    msgs, _, _, _ = load(db, since_ms, None)
    per = defaultdict(list)
    for m in msgs:
        per[f'{m["provider"]}/{m["model"]}'].append(m)

    rows = []
    for key, items in per.items():
        prov, _, mid = key.partition("/")
        m = (meta.get(prov, {}).get("models") or {}).get(mid, {})
        lim = m.get("limit") or {}
        ctx = lim.get("context")
        out = lim.get("output")
        # konteks 1 request = input + cache read + output (bukan total gabungan)
        req = [i["input"] + i["cache_read"] + i["output"] for i in items]
        mx = max(req) if req else 0
        avg = sum(req) / len(req) if req else 0
        rows.append({
            "model": key, "ctx": ctx, "max_out": out, "msgs": len(items),
            "avg": avg, "max": mx,
            "use": (mx / ctx * 100) if ctx else None,
            "over": sum(1 for t in req if ctx and t > ctx),
        })
    rows.sort(key=lambda r: -(r["max"] or 0))

    print(f"KAPASITAS TOKEN MODEL vs PEMAKAIAN — {days} hari")
    print(f"cache model: {cache}\n")
    table(
        ["model", "ctx resmi", "max output", "pesan", "avg/request", "max/request", "% ctx", "lebih"],
        [[r["model"], human(r["ctx"]) if r["ctx"] else "?",
          human(r["max_out"]) if r["max_out"] else "?",
          r["msgs"], human(r["avg"]), human(r["max"]),
          f'{r["use"]:.0f}%' if r["use"] is not None else "-",
          r["over"] or "-"] for r in rows[: top]],
        ["<", ">", ">", ">", ">", ">", ">", ">"],
    )

    print("\nTEMUAN")
    for r in rows[: top]:
        if not r["ctx"]:
            continue
        if r["over"]:
            print(f"   ! {r['model']}: {r['over']} request melampaui batas resmi "
                  f"{human(r['ctx'])} (terbesar {human(r['max'])})")
            print(f"     -> provider nyatanya masih menerima; angka models.dev TIDAK bisa dipakai "
                  f"sebagai patokan keras")
        elif r["max"] >= r["ctx"] * 0.9:
            print(f"   ! {r['model']}: sudah {r['use']:.0f}% dari {human(r['ctx'])} — sisa ruang tipis")
        else:
            print(f"   - {r['model']}: terpakai {r['use']:.0f}% dari {human(r['ctx'])}, "
                  f"sisa {human(r['ctx'] - r['max'])}")
    print("   - 'max/request' = input + cache read + output pada satu request (konteks nyata)")
    print("   - batas request/menit (RPM/TPM) model free tidak dipublikasikan;")
    print("     yang bisa diamati cuma 429 di log -> opencode-limit-guard.py")
    print("   - angka 'ctx resmi' dari models.dev (cache lokal opencode), bukan dari akunmu")


def do_reset(db: str, archive: str | None, confirmed: bool) -> None:
    """Backup + arsip JSONL, lalu kosongkan riwayat pesan supaya hitungan token = 0."""
    import shutil
    import subprocess

    if not os.path.exists(db):
        sys.exit(f"DB tidak ditemukan: {db}")

    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    n_msg = con.execute("select count(*) from message").fetchone()[0]
    n_part = con.execute("select count(*) from part").fetchone()[0]
    n_sess = con.execute("select count(*) from session").fetchone()[0]
    con.close()

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    arch = os.path.expanduser(archive) if archive else os.path.join(
        os.path.dirname(db), f"backup-{ts}")
    print(f"reset token opencode")
    print(f"  DB        : {db}")
    print(f"  akan hapus: {n_msg} pesan, {n_part} part (sesi tetap: {n_sess})")
    print(f"  backup ke : {arch}")
    if not confirmed:
        print("\n  Belum dieksekusi. Jalankan ulang dengan --yes kalau yakin.")
        print("  (riwayat chat opencode ikut hilang, hanya tersisa di backup)")
        return

    running = subprocess.run(["pgrep", "-x", "opencode"], capture_output=True, text=True)
    if running.stdout.strip():
        pids = " ".join(running.stdout.split())
        sys.exit(f"opencode masih jalan (pid: {pids}).\n"
                 "Tutup dulu (quit dari app / Ctrl-C di terminal), lalu ulangi.\n"
                 "Reset saat app hidup bisa bikin DB korup.")

    os.makedirs(arch, exist_ok=True)
    for suffix in ("", "-wal", "-shm"):
        src = db + suffix
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(arch, os.path.basename(src)))
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    jsonl = os.path.join(arch, "messages.jsonl")
    with open(jsonl, "w") as f:
        for row in con.execute(
            "select m.id, m.session_id, m.time_created, m.data, s.title, s.directory "
            "from message m left join session s on s.id = m.session_id"
        ):
            f.write(json.dumps({
                "id": row[0], "session": row[1], "ts": row[2],
                "data": json.loads(row[3]), "title": row[4], "dir": row[5],
            }) + "\n")
    con.close()

    con = sqlite3.connect(db, timeout=15)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()
    cur.execute("delete from part")
    cur.execute("delete from message")
    try:
        cur.execute("delete from session_message")
    except sqlite3.Error:
        pass
    cur.execute("""update session set cost = 0, tokens_input = 0, tokens_output = 0,
                   tokens_reasoning = 0 where 1""")
    try:
        cur.execute("update session set tokens_cache_read = 0, tokens_cache_write = 0 where 1")
    except sqlite3.Error:
        pass
    con.commit()
    left = cur.execute("select count(*) from message").fetchone()[0]
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    con.execute("VACUUM")
    con.close()

    print(f"\n  selesai. pesan tersisa: {left}")
    print(f"  arsip JSONL : {jsonl}")
    print(f"  backup DB   : {arch}/opencode.db")
    print("  cek hasil   : python3 ~/.agents/opencode-token-research.py --days 1")


def main():
    ap = argparse.ArgumentParser(description="Riset token opencode")
    ap.add_argument("--db", default=DB_DEFAULT)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--session")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--price-in", type=float, default=3.0, help="USD / 1M input token")
    ap.add_argument("--price-out", type=float, default=15.0, help="USD / 1M output token")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", help="tulis laporan markdown ke file ini")
    ap.add_argument("--limits", action="store_true",
                    help="riset kapasitas token tiap model (context/output limit) vs pemakaianmu")
    ap.add_argument("--reset-ctx", action="store_true",
                    help="potong konteks 1 sesi jadi ~0 (arsip + hapus pesan lama, sesi tetap)")
    ap.add_argument("--keep", type=int, default=0, help="jumlah pesan terakhir yang disimpan (0 = kosongkan sesi)")
    ap.add_argument("--reset", action="store_true",
                    help="nolkan hitungan token (hapus riwayat pesan). Butuh --yes")
    ap.add_argument("--yes", action="store_true", help="konfirmasi untuk --reset")
    ap.add_argument("--archive", help="folder backup (default: ~/.local/share/opencode/backup-<ts>)")
    args = ap.parse_args()

    if args.reset_ctx:
        do_reset_ctx(args.db, args.session, args.keep, args.archive, args.yes)
        return

    if args.reset:
        do_reset(args.db, args.archive, args.yes)
        return


    since = None
    label = "semua waktu"
    if not args.all:
        since = int((datetime.now(timezone.utc) - timedelta(days=args.days)).timestamp() * 1000)
        label = f"{args.days} hari terakhir"

    if args.limits:
        do_limits(args.db, since, args.days, args.top)
        return

    msgs, parts, tools, sessions = load(args.db, since, args.session)
    if not msgs:
        print(f"Tidak ada data untuk {label}.")
        return

    tot = {k: sum(m[k] for m in msgs) for k in
           ("input", "output", "reasoning", "cache_read", "cache_write", "total")}
    ctx_tokens = tot["input"] + tot["cache_read"]
    billed_out = tot["output"] + tot["reasoning"]
    cache_hit = tot["cache_read"] / ctx_tokens * 100 if ctx_tokens else 0
    est_cost = (tot["input"] / 1e6 * args.price_in
                + tot["cache_read"] / 1e6 * args.price_in * 0.1
                + billed_out / 1e6 * args.price_out)

    per_day = defaultdict(lambda: {"msgs": 0, "total": 0, "cache": 0, "input": 0})
    per_model = defaultdict(lambda: {"msgs": 0, "input": 0, "output": 0, "reasoning": 0,
                                     "cache_read": 0, "total": 0, "cost": 0.0})
    per_sess = defaultdict(lambda: {"msgs": 0, "total": 0, "cache": 0, "input": 0,
                                    "output": 0, "reasoning": 0, "first": None, "last": None,
                                    "models": Counter()})
    for m in msgs:
        day = datetime.fromtimestamp(m["ts"] / 1000).strftime("%Y-%m-%d")
        d = per_day[day]
        d["msgs"] += 1
        d["total"] += m["total"]
        d["cache"] += m["cache_read"]
        d["input"] += m["input"]
        mo = per_model[f'{m["provider"]}/{m["model"]}']
        mo["msgs"] += 1
        for k in ("input", "output", "reasoning", "cache_read", "total"):
            mo[k] += m[k]
        mo["cost"] += m["cost"]
        s = per_sess[m["session"]]
        s["msgs"] += 1
        s["total"] += m["total"]
        s["cache"] += m["cache_read"]
        s["input"] += m["input"]
        s["output"] += m["output"]
        s["reasoning"] += m["reasoning"]
        s["models"][m["model"]] += 1
        s["first"] = m["ts"] if s["first"] is None else min(s["first"], m["ts"])
        s["last"] = m["ts"] if s["last"] is None else max(s["last"], m["ts"])

    days = sorted(per_day)
    day_vals = [per_day[d]["total"] for d in days]

    if args.json:
        out = {
            "range": label,
            "messages": len(msgs),
            "sessions": len(per_sess),
            "tokens": tot,
            "cache_hit_pct": round(cache_hit, 2),
            "avg_tokens_per_message": round(tot["total"] / len(msgs), 1),
            "cost_recorded_usd": round(sum(m["cost"] for m in msgs), 6),
            "cost_estimate_usd": round(est_cost, 2),
            "price_assumption": {"input_per_m": args.price_in, "output_per_m": args.price_out},
            "per_day": {d: per_day[d] for d in days},
            "per_model": dict(per_model),
            "per_session": {k: {**v, "title": sessions.get(k, {}).get("title", ""),
                                "models": dict(v["models"])} for k, v in per_sess.items()},
            "tool_calls": dict(tools),
        }
        txt = json.dumps(out, indent=2, default=str)
        print(txt)
        if args.md:
            with open(args.md, "w") as f:
                f.write(txt)
        return

    # ---------- laporan teks ----------
    print(f"RISET TOKEN OPENCODE — {label}")
    print(f"DB: {args.db}\n")
    print("1. RINGKASAN")
    print(f"   sesi {len(per_sess)} · pesan assistant {len(msgs)} · rata2 {human(tot['total'] / len(msgs))} token/pesan")
    print(f"   total {human(tot['total'])} token")
    print(f"     input          {human(tot['input']):>8}  {pct(tot['input'], tot['total'])}")
    print(f"     cache read     {human(tot['cache_read']):>8}  {pct(tot['cache_read'], tot['total'])}")
    print(f"     output         {human(tot['output']):>8}  {pct(tot['output'], tot['total'])}")
    print(f"     reasoning      {human(tot['reasoning']):>8}  {pct(tot['reasoning'], tot['total'])}")
    print(f"   cache hit {cache_hit:.1f}% · biaya tercatat ${sum(m['cost'] for m in msgs):.4f}")
    print(f"   estimasi kalau berbayar (in ${args.price_in}/M, out ${args.price_out}/M): ${est_cost:,.2f}")

    print("\n2. TREN HARIAN")
    shown = days[-args.top:]
    table(
        ["tanggal", "pesan", "token", "avg/pesan"],
        [[d, per_day[d]["msgs"], human(per_day[d]["total"]),
          human(per_day[d]["total"] / per_day[d]["msgs"])] for d in shown],
        ["<", ">", ">", ">"],
    )
    if len(shown) > 1:
        print(f"   tren  {spark([per_day[d]['total'] for d in shown])}  (skala log: {shown[0]} -> {shown[-1]})")

    print("\n3. EFISIENSI MODEL")
    table(
        ["model", "pesan", "avg/pesan", "out:in", "reason%", "cache hit"],
        [[k, v["msgs"], human(v["total"] / v["msgs"]),
          f'{(v["output"] / v["input"]):.3f}' if v["input"] else "-",
          f'{(v["reasoning"] / v["total"] * 100):.0f}%' if v["total"] else "-",
          f'{(v["cache_read"] / (v["input"] + v["cache_read"]) * 100):.0f}%' if (v["input"] + v["cache_read"]) else "-"]
         for k, v in sorted(per_model.items(), key=lambda kv: -kv[1]["total"])],
        ["<", ">", ">", ">", ">", ">"],
    )

    print("\n4. DETEKSI PEMBOROSAN")
    findings = []
    for sid, v in per_sess.items():
        avg = v["total"] / v["msgs"]
        if avg > 100_000:
            findings.append(("context besar", sid,
                             f"rata2 {human(avg)}/pesan (>100k) — riwayat di-resend tiap request"))
        if v["reasoning"] > v["output"] and v["reasoning"] > 20_000:
            findings.append(("reasoning boros", sid,
                             f"reasoning {human(v['reasoning'])} > output {human(v['output'])}"))
        ch = v["cache"] / (v["input"] + v["cache"]) * 100 if (v["input"] + v["cache"]) else 100
        if ch < 70:
            findings.append(("cache jelek", sid, f"cache hit {ch:.0f}% (<70%)"))
        comp = parts.get(sid, Counter()).get("compaction", 0)
        if comp >= 3:
            findings.append(("sering compact", sid, f"{comp}x compaction — sesi terlalu panjang"))
    if findings:
        for kind, sid, note in findings[: args.top * 2]:
            print(f"   ! [{kind}] {sess_label(sessions, sid)[:40]}")
            print(f"       {note}")
    else:
        print("   tidak ada pola pemborosan mencolok.")

    print("\n5. TOP SESI (token)")
    table(
        ["total", "pesan", "avg", "judul"],
        [[human(v["total"]), v["msgs"], human(v["total"] / v["msgs"]),
          sess_label(sessions, s)[:40]]
         for s, v in sorted(per_sess.items(), key=lambda kv: -kv[1]["total"])[: args.top]],
        [">", ">", ">", "<"],
    )

    print("\n6. TOOL PALING SERING (proxy biaya konteks)")
    table(["tool", "panggilan"], [[k, v] for k, v in tools.most_common(args.top)],
          ["<", ">"])
    tot_tools = sum(tools.values())
    if tot_tools:
        print(f"   total {tot_tools} tool call · ~{human(tot['total'] / tot_tools)} token per tool call")

    print("\n7. REKOMENDASI")
    recs = []
    if cache_hit < 80:
        recs.append(f"cache hit {cache_hit:.0f}% — jaga prefix prompt stabil (jangan edit system prompt di tengah sesi).")
    if tot["total"] / len(msgs) > 60_000:
        recs.append(f"rata2 konteks {human(tot['total'] / len(msgs))}/pesan — mulai sesi baru per tugas, jangan lanjutkan sesi raksasa.")
    if any(v["reasoning"] > v["output"] for v in per_sess.values()):
        recs.append("beberapa sesi: reasoning > output — pakai varian reasoning rendah untuk tugas mekanis (rename, format, grep).")
    if tools.get("bash", 0) > tools.get("read", 0) * 2:
        recs.append(f"bash {tools['bash']}x vs read {tools.get('read', 0)}x — output bash besar ikut masuk konteks; ringkas output (head/tail).")
    if not recs:
        recs.append("pola pemakaian sudah sehat; tidak ada yang perlu diubah.")
    for r in recs:
        print(f"   - {r}")

    if args.md:
        with open(args.md, "w") as f:
            f.write(f"# Riset token opencode — {label}\n\n")
            f.write(f"- sesi: {len(per_sess)}, pesan: {len(msgs)}\n")
            f.write(f"- total token: {tot['total']:,} (input {tot['input']:,}, "
                    f"cache read {tot['cache_read']:,}, output {tot['output']:,}, reasoning {tot['reasoning']:,})\n")
            f.write(f"- cache hit: {cache_hit:.1f}%\n- estimasi biaya: ${est_cost:,.2f}\n\n")
            f.write("## Model\n\n| model | pesan | avg/pesan | total |\n|---|---|---|---|\n")
            for k, v in sorted(per_model.items(), key=lambda kv: -kv[1]["total"]):
                f.write(f"| {k} | {v['msgs']} | {human(v['total'] / v['msgs'])} | {human(v['total'])} |\n")
            f.write("\n## Temuan\n\n")
            for kind, sid, note in findings:
                f.write(f"- **{kind}** — {sessions.get(sid, {}).get('title', sid)}: {note}\n")
            f.write("\n## Rekomendasi\n\n")
            for r in recs:
                f.write(f"- {r}\n")
        print(f"\n   laporan markdown ditulis: {args.md}")


if __name__ == "__main__":
    main()
