#!/usr/bin/env python3
"""skills-index-md.py — tulis ringkasan manusiawi (skills-INDEX.md) dari skills-index.db.

Ringan by design: hanya agregat + contoh, bukan dump 24k baris.
Pakai: python3 ~/.agents/skills-index-md.py
"""
import sqlite3
from datetime import datetime
from pathlib import Path

AGENTS = Path.home() / ".agents"
DB = AGENTS / "skills-index.db"
OUT = AGENTS / "skills-INDEX.md"
JUNK = AGENTS / "skills-junk.txt"


def q(conn, sql, *args):
    return conn.execute(sql, args).fetchall()


def main():
    if not DB.exists():
        print(f"ERROR: {DB} belum ada — jalankan: python3 ~/.agents/build_skills_index.py")
        return 1
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)

    total = q(conn, "SELECT COUNT(*) FROM skills")[0][0]
    tiers = q(conn, "SELECT tier, COUNT(*) FROM skills GROUP BY tier ORDER BY 2 DESC")
    cats = q(conn, "SELECT category, COUNT(*) FROM skills WHERE tier != 'docs' GROUP BY category ORDER BY 2 DESC")
    junk_n = len(JUNK.read_text().splitlines()) if JUNK.exists() else 0

    lines = [
        f"# Skills INDEX — {datetime.now():%Y-%m-%d %H:%M}",
        "",
        "Ringkasan katalog `~/.agents`. **Jangan edit file ini** — hasil generate "
        "`python3 ~/.agents/skills-index-md.py`.",
        "",
        "## Angka pokok",
        "",
        f"- Total entri: **{total}**",
    ]
    label = {
        "curated": "skill terpilih — sudah dirawat, layak di-invoke",
        "reference": "hasil scraping, punya deskripsi (cari dulu sebelum pakai)",
        "junk": "BUKAN skill (API doc/HTML/license/terlalu pendek) — jangan di-link",
        "docs": "BUKAN skill (tanpa deskripsi / halaman dokumentasi) — jangan di-link",
    }
    for t, n in tiers:
        lines.append(f"- `{t}`: **{n}** — {label.get(t, '-')}")
    lines += [
        "",
        "> **Baca angka dengan benar:** hanya `curated` yang boleh muncul sebagai kandidat",
        "> otomatis (hook/MCP). `reference` = bahan tambang — **wajib** dicek isinya dulu.",
        "> Kalau sebuah katalog atau laporan menampilkan angka jauh lebih besar dari",
        "> `curated` di atas sambil menyebutnya \"curated\", itu bug pelabelan.",
        "",
        "## Cek kesehatan katalog",
        "",
        "```bash",
        "python3 ~/.agents/skill-curate.py --report      # angka jujur + kandidat sampah",
        "python3 ~/.agents/skill-curate.py --dry-run      # lihat rencana tanpa ubah apa pun",
        "```",
        "",
        "## Cara pakai (ringan, tanpa MCP)",
        "",
        "```bash",
        'skill-search.sh "postgres index"            # cari semua tier',
        'skill-search.sh --tier curated "vue page"    # hanya skill terpilih',
        'skill-search.sh -p "docker"                  # tampilkan path SKILL.md',
        'skill-search.sh --load "playwright"          # lihat isi skill teratas',
        "link-skills-min.sh --repo <path>            # project-scope (symlink, bukan klon)",
        "link-skills-min.sh --status                 # cek wiring tiap tool",
        "python3 ~/.agents/build_skills_index.py     # rebuild index (head 4 KB, cepat)",
        "```",
        "",
        "## Skill per peran (kategori non-docs)",
        "",
        "| Kategori | Jumlah | Contoh |",
        "|---|---|---|",
    ]
    for cat, n in cats[:25]:
        ex = q(
            conn,
            "SELECT name FROM skills WHERE category = ? AND tier = 'curated' LIMIT 4",
            cat or "",
        )
        exs = ", ".join("`%s`" % e[0] for e in ex) or "—"
        lines.append(f"| {cat or '(kosong)'} | {n} | {exs} |")

    lines += [
        "",
        "## Kontaminan yang dipisah ke tier `docs`",
        "",
        f"- Jumlah: **{junk_n}** entri → daftar di `skills-junk.txt` (bahan pembersihan P1).",
        "- Disaring karena: tanpa `description` di frontmatter, atau nama dokumentasi "
        "teknis (mis. `Util`, `Pool`, `Client`).",
        "",
        "## Maintenance",
        "",
        "- Sumber tunggal: `~/.agents/skills-store` (curated). `skills-expanded/` = arsip scraping.",
        "- Jangan klon katalog ke folder tool — pakai `link-skills-min.sh` (symlink).",
        "- MCP: audit dengan `python3 ~/.agents/mcp-hygiene.py` (laporan) / `--apply`.",
        "- **Urutan regenerate yang benar** (jangan dibalik — dua generator terakhir baca DB):",
        "  ```bash",
        "  python3 ~/.agents/build_skills_index.py   # 1. tulis DB dari skills-store + skills-expanded",
        "  python3 ~/.agents/skills-index-md.py      # 2. tulis skills-INDEX.md (baca DB)",
        "  python3 ~/.agents/skills-router.py        # 3. tulis SKILLS-AVAILABLE / CATEGORIES / json",
        "  ```",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"ditulis: {OUT} ({OUT.stat().st_size/1024:.1f} KB) · total={total} · kategori={len(cats)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
