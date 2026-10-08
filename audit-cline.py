#!/usr/bin/env python3
"""audit-cline.py — hitung boros token Cline CLI dari riwayat sesi.

Cara: Cline menyimpan messages.json berisi seluruh percakapan. Tiap request API
mengirim ulang konteks yang tumbuh -> token terkirim kumulatif ≈
Σ (ukuran konteks sampai pesan itu) / 4. Diukur per sesi, per tipe pesan, dan
output tool paling besar (biasanya pembacaan file raksasa).

Pakai:  python3 ~/.agents/audit-cline.py            # semua sesi
        python3 ~/.agents/audit-cline.py --top 15   # 15 output tool terbesar
"""
import json, os, sys, glob, re, collections

HOME = os.path.expanduser("~")
SESS = os.path.join(HOME, ".cline", "data", "sessions")
BIG = 4000  # ambang output tool dianggap besar (chars)
FORBID = re.compile(r"(/vendor/|/node_modules/|/dist/|autoload_classmap|\.min\.js|/public/template/)")


def charlen(content):
    n = 0
    for c in (content or []):
        if isinstance(c, dict):
            n += len(c.get("text") or json.dumps(c, ensure_ascii=False))
    return n


def main():
    top_n = 8
    if "--top" in sys.argv:
        try:
            top_n = int(sys.argv[sys.argv.index("--top") + 1])
        except Exception:
            pass
    metas = []
    for meta in glob.glob(os.path.join(SESS, "*", "*.json")):
        if meta.endswith((".messages.json", ".compaction.json")):
            continue
        metas.append(meta)
    if not metas:
        print("tidak ada sesi Cline CLI di", SESS)
        return 1

    rows, big_tools, file_hits, grand = [], [], collections.Counter(), 0
    models = collections.Counter()

    for meta in metas:
        d = json.load(open(meta, encoding="utf-8"))
        mp = d.get("messages_path") or ""
        models[(d.get("provider"), d.get("model"))] += 1
        if not os.path.exists(mp):
            continue
        m = json.load(open(mp, encoding="utf-8"))
        msgs = m.get("messages", [])
        sysp = len(m.get("system_prompt") or "")
        running = sysp
        cum = 0
        per_role = collections.Counter()
        for x in msgs:
            cl = charlen(x.get("content"))
            running += cl
            cum += running
            per_role[x.get("role")] += cl
            for c in (x.get("content") or []):
                if not isinstance(c, dict):
                    continue
                t = c.get("text") or ""
                if cl > BIG:
                    big_tools.append((cl, d.get("session_id"), x.get("role"),
                                      re.sub(r"\s+", " ", t[:90])))
                for mm in FORBID.finditer(t):
                    file_hits[mm.group(0)] += 1
        rows.append((cum / 4.0, len(msgs), running / 4.0, os.path.basename(mp).split(".")[0][:20],
                     os.path.getsize(mp) / 2**20, per_role, d.get("team_name"), d.get("started_at", "")[:10]))
        grand += cum / 4.0

    rows.sort(reverse=True)
    print("=== PEMAKAIAN CLINE CLI (estimasi token = chars/4) ===")
    print("sekarang: %s\n" % __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
    hdr = "  %-22s %-11s %7s %10s %9s %8s  %s"
    print(hdr % ("sesi", "tanggal", "pesan", "MB file", "ctx akhir", "token kum", "team"))
    for t, n, ctx_end, sid, mb, per_role, team, date in rows:
        print(hdr % (sid, date, n, "%.1f" % mb, "%.0fk" % (ctx_end / 1000),
                     "%.1f jt" % (t / 1e6) if t >= 1e6 else "%.0f rb" % (t / 1e3), team or "-"))
    print("\ntotal estimasi terkirim: %.1f juta token dari %d sesi" % (grand / 1e6, len(rows)))
    print("model dipakai:", ", ".join("%s/%s ×%d" % (p, mo, c) for (p, mo), c in models.most_common()))

    print("\n=== %d OUTPUT TERBESAR (satu pesan) ===" % top_n)
    big_tools.sort(reverse=True)
    for cl, sid, role, snip in big_tools[:top_n]:
        print("  %8s chars  %-8s  %s" % ("{:,}".format(cl), role, snip))

    if file_hits:
        print("\n=== TERSISIP DI KONTEK: path terlarang (vendor/node_modules/dll) ===")
        for k, v in file_hits.most_common(8):
            print("  %4d× %s" % (v, k))
    else:
        print("\ntidak ada jejak path vendor/node_modules/dist di konteks.")
    print("\nAturan: sesi Cline >10 MB / >200 pesan = tutup (buka baru per tugas).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
