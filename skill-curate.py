#!/usr/bin/env python3
"""skill-curate.py — audit & penyaring katalog curated (TANPA menghapus apa pun).

Latar: katalog `~/.agents` berisi ~67k entri, tapi hanya sebagian kecil yang
benar-benar prosedural. Script ini memisahkan "skill sungguhan" dari artefak
scraping (changelog, instalasi, nama 1 huruf, fragmentasi bernomor) dan
menuliskannya ke daftar review — TIDAK memindahkan atau menghapus file.

Aturan keras (AGENTS.md):
  * tidak menghapus apa pun (hanya tulis laporan + daftar review)
  * idempotent (jalankan 2x = hasil sama)
  * UTC di laporan
  * file lama -> backup .bak-YYYYMMDD sebelum ditimpa

Pakai:
  python3 ~/.agents/skill-curate.py --report     # ringkasan angka jujur (default)
  python3 ~/.agents/skill-curate.py --dry-run    # daftar kandidat, tanpa menulis
  python3 ~/.agents/skill-curate.py --apply      # tulis skills-review.txt + skills-curated-clean.txt
  python3 ~/.agents/skill-curate.py --test       # self-test klasifikasi (tanpa I/O)

Hasil (hanya bila --apply):
  skills-review.txt        : entri curated yang ditandai perlu ditinjau (1 nama/baris)
  skills-curated-clean.txt : entri curated yang lolos filter (siap jadi katalog inti)
"""
import argparse
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENTS = Path.home() / ".agents"
DB = AGENTS / "skills-index.db"
STORE = AGENTS / "skills-store"
REVIEW = AGENTS / "skills-review.txt"
CLEAN = AGENTS / "skills-curated-clean.txt"

# ── Aturan penanda "bukan skill sungguhan" ──────────────────────────────────

TRIVIAL_NAMES = {"a", "an", "the", "i", "x", "y", "z", "n", "s", "c", "v",
                 "tmp", "test", "tests", "draft", "untitled", "new", "copy"}
NUMERIC_ONLY = re.compile(r"^\d{1,4}[a-z]?$")
VERSION_RANGE = re.compile(r"^\d+-\d+-\d+-\d+-")
UPGRADE_DOC = re.compile(r"(upgrade-instructions|migration-guide-only|release-notes|^changelog)", re.I)
META_DOC = re.compile(
    r"^(install|installation|setup|getting-started|overview|index|inventory|"
    r"readme|license|changelog|contributing|code-of-conduct|table-of-contents)$", re.I)
AGENT_INVENTORY = re.compile(r"^(commands-inventory|agents-inventory|agents-installation|"
                             r"commands-installation|agents-and-commands)$", re.I)
CONFIG_ARTIFACT = re.compile(
    r"(cursor-rules|cursorrules|clinerules|^\.?rulesc$|coding-rulesc|"
    r"^rules?$|^config$|^settings$|package-json$)", re.I)
FRAGMENT_NUM = re.compile(r"^\d{2,3}-[a-z]")
GENERIC_DESC = re.compile(
    r"^\s*(this (skill|document|file|guide|repository)|a skill|skill for|"
    r"documentation|todo|tbd|n/?a|\-|\.)\s*\.?\s*$", re.I)
MIN_DESC_WORDS = 6
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")


def desc_is_thin(desc, name=""):
    """True bila deskripsi terlalu kurus *untuk ukuran informasinya*.

    Bahasa non-spasi (Mandarin/Jepang/Korea) tidak bisa dihitung dengan split() —
    satu kalimat Mandarin panjang akan terlihat "1 kata" dan salah ditandai.
    Untuk teks CJK pakai ambang karakter; untuk teks berspasi pakai jumlah kata.
    Nama yang sudah self-explanatory (mis. `gws-docs`, `lark-task`) diberi
    toleransi lebih longgar: deskripsi pendeknya tetap informatif.
    """
    d = (desc or "").strip()
    if not d:
        return True
    if CJK_RE.search(d):
        return len(d) < 12                      # kalimat CJK pendek saja yang tipis
    if len(d.split()) < MIN_DESC_WORDS:
        # nama spesifik + deskripsi pendek ("Read and write Google Docs.") = cukup
        return not re.search(r"-(docs|sheets|drive|forms|calendar|gmail|meet|keep|"
                             r"tasks|script|events|workflow)$", (name or "").lower())
    return False



def reasons_for(name, desc, path):
    """Kembalikan daftar alasan sebuah entri ditandai perlu ditinjau.

    Kosong = lolos filter (kandidat curated bersih). Fungsi murni — gampang dites.
    """
    out = []
    n = (name or "").strip()
    d = (desc or "").strip()
    low = n.lower()

    if not n:
        return ["nama-kosong"]
    if low in TRIVIAL_NAMES:
        out.append("nama-trivial")
    elif len(n) <= 2 and not re.match(r"^\d+$", n) and desc_is_thin(d, n):
        # Nama sangat pendek (mis. 'ck') hanya jadi masalah bila deskripsi juga tipis.
        # Deskripsi yang menjelaskan "apa + kapan dipakai" sudah cukup membuktikan
        # ini skill nyata, apa pun panjang namanya.
        out.append("nama-terlalu-pendek-tanpa-desc")
    if NUMERIC_ONLY.match(low):
        out.append("nama-numerik")
    if VERSION_RANGE.match(low):
        out.append("rentang-versi")
    if UPGRADE_DOC.search(low):
        out.append("doc-upgrade")
    if META_DOC.match(low):
        out.append("doc-meta")
    if AGENT_INVENTORY.match(low):
        out.append("inventaris-agent")
    if CONFIG_ARTIFACT.search(low):
        out.append("artefak-config")
    if FRAGMENT_NUM.match(low) and desc_is_thin(d, n):
        out.append("fragment-nomor-tanpa-desc")
    if not d:
        out.append("tanpa-desc")
    elif GENERIC_DESC.match(d):
        out.append("desc-generik")
    elif desc_is_thin(d, n):
        out.append("desc-terlalu-pendek")
    return out



def load_rows():
    if not DB.exists():
        print(f"ERROR: {DB} belum ada — jalankan: python3 ~/.agents/build_skills_index.py",
              file=sys.stderr)
        return None
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    return conn.execute(
        "SELECT name, COALESCE(description,''), COALESCE(path,'') "
        "FROM skills WHERE tier='curated' ORDER BY name"
    ).fetchall()


def backup(p):
    """Backup sekali per hari (idempotent, tidak menumpuk)."""
    if not p.exists():
        return
    bak = p.with_name(p.name + f".bak-{datetime.now(timezone.utc):%Y%m%d}")
    if not bak.exists():
        shutil.copy2(p, bak)
        print(f"  backup: {bak.name}")


def write_list(p, names):
    backup(p)
    p.write_text("\n".join(names) + ("\n" if names else ""), encoding="utf-8")
    print(f"  tulis : {p.name} ({len(names)} entri)")


def report(rows):
    flagged, clean, by_reason = [], [], {}
    for name, desc, path in rows:
        rs = reasons_for(name, desc, path)
        if rs:
            flagged.append(name)
            for r in rs:
                by_reason[r] = by_reason.get(r, 0) + 1
        else:
            clean.append(name)
    return {"flagged": flagged, "clean": clean, "by_reason": by_reason}


def cmd_report(rows):
    r = report(rows)
    total = len(rows)
    pct = (len(r["clean"]) * 100 // total) if total else 0
    print("=== Kesehatan katalog curated (UTC %s) ==="
          % datetime.now(timezone.utc).isoformat(timespec="seconds"))
    print(f"  entri curated di index : {total}")
    print(f"  lolos filter (bersih)  : {len(r['clean'])}  ({pct}%)")
    print(f"  perlu ditinjau         : {len(r['flagged'])}")
    print()
    print("  Alasan tertandai (satu entri bisa punya >1 alasan):")
    for reason, n in sorted(r["by_reason"].items(), key=lambda kv: -kv[1]):
        print(f"    {reason:28s} {n}")
    print()
    print("  Jika 'bersih' jauh di bawah ekspektasi, cek `--dry-run` dulu.")
    print("  Tidak ada file yang diubah oleh --report.")
    return 0


def cmd_dry_run(rows):
    print("=== DRY RUN — tidak ada file yang diubah ===")
    r = report(rows)
    print(f"  curated total : {len(rows)}")
    print(f"  bersih        : {len(r['clean'])}")
    print(f"  ditandai      : {len(r['flagged'])}")
    print()
    print("  30 contoh yang ditandai:")
    shown = 0
    for name, desc, path in rows:
        rs = reasons_for(name, desc, path)
        if rs and shown < 30:
            print(f"    - {name[:58]:58s} [{','.join(rs)}]")
            shown += 1
    print()
    print("  Jalankan dengan --apply untuk menulis daftar review.")
    return 0


def cmd_apply(rows):
    print("=== APPLY — menulis daftar review (TIDAK menghapus apa pun) ===")
    r = report(rows)
    write_list(REVIEW, r["flagged"])
    write_list(CLEAN, r["clean"])
    print(f"  curated bersih : {len(r['clean'])} → {CLEAN.name}")
    print(f"  perlu ditinjau : {len(r['flagged'])} → {REVIEW.name}")
    print()
    print("  Langkah berikutnya (P1, butuh keputusan user):")
    print("    tinjau isi skills-review.txt, lalu pindahkan yang terbukti")
    print("    bukan skill dari skills-store/ ke arsip — JANGAN hapus.")
    return 0


def cmd_test():
    """Self-test murni: tidak menyentuh DB atau file."""
    cases = [
        ("playwright", "Use when the task requires automating a real browser from the terminal for navigation and forms.", False),
        ("a", "Some short thing here that is not informative at all.", True),
        ("01", "A perfectly fine long description with enough words to pass the check.", True),
        ("0-10-0-11-extension-author-upgrade-instructions", "Upgrade guide for extension authors covering version changes in detail.", True),
        ("021-problem-framing", "ok.", True),
        ("021-problem-framing", "Frames the problem statement before design so stakeholders agree on scope early.", False),
        ("install", "How to install this package on your machine with all the required steps documented.", True),
        ("000-aiuelab-launch-initiative-cursor-rules-coding-rulesc", "Cursor rules scraped from a project repository config file.", True),
        ("postgres-query-tuning", "Diagnose and fix slow PostgreSQL queries using EXPLAIN ANALYZE and index strategy.", False),
        ("absolute-ui", "Build a polished interface with consistent spacing, typography and interaction states.", False),
        ("lark-approval", "飞书审批：查询和处理审批待办/已办/实例，搜索可发起审批定义、查看定义详情并发起原生审批实例。", False),
        ("gws-docs", "Read and write Google Docs.", False),
        ("ck", "Persistent per-project memory for Claude Code. Auto-loads project context on session start.", False),
        ("tbd", "N/A", True),
    ]
    bad = 0
    for name, desc, want in cases:
        got = bool(reasons_for(name, desc, ""))
        mark = "OK  " if got == want else "FAIL"
        if got != want:
            bad += 1
            print(f"  {mark} {name!r} want_flagged={want} got={got} reasons={reasons_for(name, desc, '')}")
        else:
            print(f"  {mark} {name!r} flagged={got}")
    print()
    print(f"self-test: {len(cases)-bad}/{len(cases)} lulus")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description="Audit & saring katalog curated (tanpa hapus).")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--report", action="store_true", help="ringkasan angka (default)")
    g.add_argument("--dry-run", action="store_true", help="daftar kandidat tanpa menulis file")
    g.add_argument("--apply", action="store_true", help="tulis skills-review.txt + skills-curated-clean.txt")
    g.add_argument("--test", action="store_true", help="self-test klasifikasi (tanpa I/O)")
    a = ap.parse_args()

    if a.test:
        return cmd_test()
    rows = load_rows()
    if rows is None:
        return 1
    if a.apply:
        return cmd_apply(rows)
    if a.dry_run:
        return cmd_dry_run(rows)
    return cmd_report(rows)


if __name__ == "__main__":
    raise SystemExit(main())


