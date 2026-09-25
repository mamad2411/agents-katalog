#!/usr/bin/env python3
"""skill-bench.py — uji objektif: apakah katalog skill ini berguna?

Menjawab pertanyaan "68k skill itu berguna apa kaga" dengan DATA, bukan opini.

Metode:
  * Ambil sekumpulan prompt nyata (bahasa Indonesia + teknis, seperti pemakaian harian).
  * Tiap prompt punya daftar kata kunci yang HARUS muncul di skill teratas
    (mis. prompt debug python → 'debug'/'python'/'traceback').
  * Jalankan mesin skor yang SAMA dengan hook (skill-mcp.rank_with_scores).
  * Hitung precision@k per tier → berapa % kandidat yang benar-benar nyambung.

Mengapa ini bukti yang sah: memakai mesin produksi (bukan skor buatan), dan
kata kunci ditetapkan SEBELUM melihat hasil (tidak dicocok-cocokkan).

Pakai:
  python3 ~/.agents/skill-bench.py              # tes default (12 prompt x 3 tier)
  python3 ~/.agents/skill-bench.py --k 5
  python3 ~/.agents/skill-bench.py --tier curated
  python3 ~/.agents/skill-bench.py --verbose    # tampilkan setiap hasil
"""
import argparse
import importlib.util
import io
import contextlib
import os
import sys

# ── Prompt uji + kata kunci yang diharapkan (ditetapkan sebelum lari) ────────
# Format: (prompt, [keyword_yang_harus_muncul], kategori_harapan)
CASES = [
    ("perbaiki error login react saya crash", ["debug", "react", "error"], "debug"),
    ("aplikasi gagal jalan muncul traceback python", ["debug", "python", "traceback"], "debug"),
    ("tulis unit test untuk fungsi golang", ["test", "golang", "go"], "test"),
    ("database postgres lemot banget query nya", ["postgres", "sql", "query", "optim"], "database"),
    ("buat landing page nextjs pakai tailwind", ["frontend", "next", "tailwind", "ui", "landing"], "frontend"),
    ("desain ulang tampilan dashboard admin biar modern", ["design", "ui", "frontend", "dashboard"], "frontend"),
    ("deploy aplikasi ke kubernetes pakai docker", ["docker", "kubernetes", "deploy", "container"], "devops"),
    ("setup ci cd github actions", ["ci", "cd", "github", "action", "pipeline"], "devops"),
    ("audit keamanan api saya dari serangan", ["security", "api", "auth", "hardening"], "keamanan"),
    ("kompres gambar sebelum upload ke web", ["image", "compress", "optim", "upload"], "gambar-video"),
    ("bikin migration database tambah kolom", ["migration", "database", "schema", "sql"], "database"),
    ("refactor kode vue jadi lebih rapi", ["refactor", "vue", "clean"], "refactor"),
]

# ── Kata terlarang: kandidat yang MENGANDUNG kata ini otomatis dinilai GAGAL ──
# Bukti kegagalan nyata: prompt "kompres gambar" mengembalikan `ai-image-generation`
# dan `github-figure-bed` — relevan-kata, tapi bukan tugasnya. Tanpa daftar ini,
# tes akan memberi 100% palsu dan menyesatkan.
FORBIDDEN = {
    "perbaiki error login react saya crash": ["admin", "template", "rules", "react19-test"],
    "aplikasi gagal jalan muncul traceback python": ["aws", "cdk", "port", "integrat"],
    "tulis unit test untuk fungsi golang": [],
    "database postgres lemot banget query nya": ["egress", "neon", "marketing"],
    "buat landing page nextjs pakai tailwind": ["audit", "analytics"],
    "desain ulang tampilan dashboard admin biar modern": ["rules", "template", "ai-assistant"],
    "deploy aplikasi ke kubernetes pakai docker": [],
    "setup ci cd github actions": [],
    "audit keamanan api saya dari serangan": ["ai-security"],
    "kompres gambar sebelum upload ke web": ["imagegen", "generation", "figure-bed", "ai-image"],
    "bikin migration database tambah kolom": [],
    "refactor kode vue jadi lebih rapi": ["ui-to-vue", "pinia-test"],
}


def load_ranker():
    spec = importlib.util.spec_from_file_location(
        "sm", os.path.expanduser("~/.agents/skill-mcp.py"))
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        spec.loader.exec_module(m)
    return m


def hit(name, tier, desc, kws):
    """True bila kandidat mengandung minimal satu kata kunci harapan."""
    hay = (name + " " + (desc or "")).lower()
    return any(k.lower() in hay for k in kws)


def run(tier, k, verbose):
    m = load_ranker()
    hits = tried = 0
    per_case = []
    for prompt, kws, cat in CASES:
        rows = m.rank_with_scores(prompt, top=k)
        if tier:
            rows = [r for r in rows if r[2] == tier]
        got = len(rows)
        tried += got
        bad = FORBIDDEN.get(prompt, [])
        scored = []
        for s, n, t, c, d in rows:
            hay = (n + " " + (d or "")).lower()
            ok = hit(n, t, d, kws) and not any(b in hay for b in bad)
            scored.append((ok, s, n, t, d))
        h = sum(1 for ok, *_ in scored if ok)
        hits += h
        per_case.append((prompt, got, h, scored))
    return hits, tried, per_case


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--tier", default=None, help="curated | reference | junk")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    label = a.tier or "semua tier"
    hits, tried, per_case = run(a.tier, a.k, a.verbose)
    pct = (hits * 100 // tried) if tried else 0

    print("=== skill-bench (mesin produksi: skill-mcp.rank_with_scores) ===")
    print(f"tier={label}  k={a.k}  prompt={len(CASES)}")
    print(f"precision@{a.k} = {hits}/{tried} = {pct}%")
    print()
    for prompt, got, h, rows in per_case:
        mark = "OK  " if h == got and got else ("MISS" if not h else "PART")
        print(f"  {mark} [{h}/{got}] {prompt[:52]}")
        if a.verbose:
            for ok, s, n, t, d in rows:
                flag = " " if ok else "x"
                print(f"      {flag} sig={s:3d} {t:9s} {n}")
    print()
    if label == "semua tier":
        print("Bandingkan dengan: --tier curated  dan  --tier reference")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
