#!/usr/bin/env python3
"""skills-router.py — bangun katalog "SKILLS AVAILABLE" yang gampang dilihat AI.

Output (semua generated, jangan diedit manual):
  SKILLS-AVAILABLE.md  : ~1200 skill tier-1, dikelompokkan per kategori (maks 55/kategori)
  SKILLS-CATEGORIES.md : peta kategori ringkas (jumlah + contoh)
  skills-index.json    : versi mesin (dipakai MCP server & hook, tanpa query DB)

Pakai: python3 ~/.agents/skills-router.py
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

AGENTS = Path.home() / ".agents"
DB = AGENTS / "skills-index.db"
OUT_MD = AGENTS / "SKILLS-AVAILABLE.md"
OUT_CAT = AGENTS / "SKILLS-CATEGORIES.md"
OUT_JSON = AGENTS / "skills-index.json"

PER_CATEGORY = 0           # 0 = TANPA CAP: semua skill aktif dimasukkan ke katalog
DESC_CHARS = 88


def main():
    if not DB.exists():
        print("ERROR: %s belum ada — jalankan build_skills_index.py" % DB)
        return 1
    conn = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)

    rows = conn.execute(
        "SELECT COALESCE(category,''), name, COALESCE(description,'') FROM skills "
        "WHERE tier != 'junk' ORDER BY category, name"
    ).fetchall()
    total_active = conn.execute("SELECT COUNT(*) FROM skills WHERE tier != 'junk'").fetchone()[0]
    total_curated = conn.execute("SELECT COUNT(*) FROM skills WHERE tier='curated'").fetchone()[0]
    total_all = conn.execute("SELECT COUNT(*) FROM skills").fetchone()[0]
    counts = conn.execute(
        "SELECT COALESCE(category,''), COUNT(*) FROM skills WHERE tier != 'junk' GROUP BY category"
    ).fetchall()

    by_cat, tier1 = {}, []
    for cat, name, desc in rows:
        cat = cat or "(tanpa kategori)"
        bucket = by_cat.setdefault(cat, [])
        if PER_CATEGORY and len(bucket) >= PER_CATEGORY:
            continue
        bucket.append((name, (desc or "").strip()[:DESC_CHARS]))
        tier1.append((cat, name))

    md = [
        "# SKILLS AVAILABLE — katalog siap pakai (%d skill)" % len(tier1),
        "",
        "> **Untuk AI: baca ini SEBELUM mengerjakan apa pun.** Kalau ada skill yang cocok,",
        "> pakai skill itu dulu — jangan mengarang dari nol.",
        "> Cari cepat: `~/.agents/skill-search.sh \"<kata kunci>\"` atau tool MCP `skill_search`.",
        "",
        "Sumber: `%d` skill curated (dari `%d` entri total di index). Katalog penuh: `skills-index.db`."
        % (total_curated, total_all),
        "Kategori: **%d** · maks %d skill/kategori ditampilkan di sini." % (len(by_cat), PER_CATEGORY),
        "",
        "## Peta cepat kategori",
        "",
        "| Kategori | Tersedia di sini | Total curated |",
        "|---|---|---|",
    ]
    cmap = dict(counts)
    for cat in sorted(by_cat, key=lambda c: -cmap.get(c, 0)):
        md.append("| %s | %d | %d |" % (cat, len(by_cat[cat]), cmap.get(cat, 0)))
    md += ["", "---", ""]

    for cat in sorted(by_cat, key=lambda c: (-cmap.get(c, 0), c)):
        md.append("## %s (%d)" % (cat, cmap.get(cat, 0)))
        md.append("")
        for name, desc in by_cat[cat]:
            md.append("- **%s** — %s" % (name, desc) if desc else "- **%s**" % name)
        md.append("")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    cat_md = [
        "# SKILLS CATEGORIES — peta peran (generated %s)" % datetime.now().strftime("%Y-%m-%d %H:%M"),
        "",
        "Cari peran yang cocok → buka kategori di `SKILLS-AVAILABLE.md`.",
        "",
        "| Kategori | Tier-1 | Curated | Contoh |",
        "|---|---|---|---|",
    ]
    for cat in sorted(by_cat, key=lambda c: -cmap.get(c, 0)):
        ex = ", ".join("`%s`" % n for n, _ in by_cat[cat][:6])
        cat_md.append("| %s | %d | %d | %s |" % (cat, len(by_cat[cat]), cmap.get(cat, 0), ex))
    OUT_CAT.write_text("\n".join(cat_md) + "\n", encoding="utf-8")

    data = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "tier1_count": len(tier1),
        "total_curated": total_curated,
        "total_index": total_all,
        "per_category_cap": PER_CATEGORY,
        "categories": {c: [n for n, _ in v] for c, v in sorted(by_cat.items())},
        "summary": {c: {"tier1": len(v), "curated": cmap.get(c, 0)} for c, v in sorted(by_cat.items())},
    }
    OUT_JSON.write_text(json.dumps(data, indent=1), encoding="utf-8")

    print("tier-1 tersedia : %d skill (cap %d/kategori)" % (len(tier1), PER_CATEGORY))
    print("kategori        : %d" % len(by_cat))
    print("ditulis         : %s (%.0f KB)" % (OUT_MD, OUT_MD.stat().st_size / 1024))
    print("                  %s" % OUT_CAT)
    print("                  %s" % OUT_JSON)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
