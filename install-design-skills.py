#!/usr/bin/env python3
"""install-design-skills.py — pasang skill UI/UX profesional dari katalog
`skills-expanded` (hasil scan internet) ke `skills-store`, lewat gerbang
kualitas `skill-promote.py`.

Tujuan: AI punya bahan nyata untuk menghasilkan UI/UX setara produk komersial,
bukan menebak dari ingatan. Skill yang sudah ada tidak dipasang ulang.

Pakai:
  python3 ~/.agents/install-design-skills.py            # dry-run
  python3 ~/.agents/install-design-skills.py --apply    # pasang
"""
import importlib.util
import os
import sqlite3
import sys

AG = os.path.expanduser("~/.agents")
DB = f"{AG}/skills-index.db"
STORE = f"{AG}/skills-store"

spec = importlib.util.spec_from_file_location("sp", f"{AG}/skill-promote.py")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)

# Bucket -> FTS query. Urutan = prioritas saat anggaran slot dibagi.
BUCKETS = [
    ("arah-desain", 'design direction OR art direction OR "visual identity" OR moodboard OR aesthetic'),
    ("anti-slop", 'critique OR "design review" OR "design audit" OR polish OR "visual quality"'),
    ("design-system", 'design system OR "design tokens" OR "component library" OR theming'),
    ("layout", 'layout OR grid OR spacing OR "page structure" OR "information architecture"'),
    ("dashboard", 'dashboard OR "data visualization" OR "admin panel" OR KPI OR analytics'),
    ("motion", 'motion OR transition OR "micro-interaction" OR easing OR animation'),
    ("aksesibilitas", 'accessibility OR WCAG OR "screen reader" OR "keyboard navigation"'),
    ("landing", 'landing page OR hero OR conversion OR "call to action" OR copywriting'),
]

PER_BUCKET = 5
MIN_SCORE = 62
# Artefak scraping: slug panjang/mesin-generated, bukan nama skill yang enak dibaca.
SKIP_PREFIX = ("topic-", "ghscan-", "mined-", "awesome-")
# Vendor desktop (WinForms) — bukan target stack web/mobile di katalog ini.
SKIP_CONTAINS = ("syncfusion", "winforms", "wpf")


def main():
    apply_ = "--apply" in sys.argv
    existing = set(os.listdir(STORE))
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    chosen = {}

    for bucket, query in BUCKETS:
        seen_dirs = set()
        picked = 0
        rows = con.execute(
            "SELECT name, description, path FROM skills WHERE skills MATCH ? "
            "AND path LIKE '%skills-expanded%' ORDER BY rank LIMIT 400",
            (query,),
        ).fetchall()
        for _name, _desc, path in rows:
            d = os.path.dirname(path)
            if d in seen_dirs:
                continue
            seen_dirs.add(d)
            slug = os.path.basename(d)
            if slug in existing or slug in chosen:
                continue
            if slug.startswith(SKIP_PREFIX) or len(slug) > 40:
                continue
            if any(bad in slug for bad in SKIP_CONTAINS):
                continue
            sc, _why = sp.score(path)
            if sc < MIN_SCORE:
                continue
            chosen[slug] = (sc, path, bucket)
            picked += 1
            if picked >= PER_BUCKET:
                break
    con.close()

    items = [(sc, p, slug) for slug, (sc, p, _) in chosen.items()]
    items.sort(key=lambda x: -x[0])
    print(f"kandidat: {len(items)}")
    for sc, _p, slug in items:
        print(f"  {sc:3d}  {slug:42s} {chosen[slug][2]}")

    if not apply_:
        print("\n(dry-run — tambahkan --apply untuk memasang)")
        return 0

    done = sp.promote(items)
    print(f"\nterpasang: {len(done)}")
    for d in done:
        print(f"  + {d['slug']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
