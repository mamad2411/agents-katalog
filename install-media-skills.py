#!/usr/bin/env python3
"""install-media-skills.py — pilih skill animasi/video/film dari skills-expanded,
gerbang kualitas skill-promote.py, lalu pasang ke skills-store.

Pakai: python3 install-media-skills.py [--apply]
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.expanduser("~/.agents"))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "sp", os.path.expanduser("~/.agents/skill-promote.py")
)
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)

AG = os.path.expanduser("~/.agents")
DB = f"{AG}/skills-index.db"
STORE = f"{AG}/skills-store"
EXPANDED = f"{AG}/skills-expanded"

# Bucket -> FTS query. Order = priority when the 30-slot budget is allocated.
BUCKETS = [
    ("video-edit", 'ffmpeg OR "video editing" OR "video editor" OR montage OR reel OR "beat sync" OR clips'),
    ("film", 'film OR cinematic OR cinematography OR "color grading" OR compositing OR "post production" OR mastering'),
    ("animation", 'animation OR "motion graphics" OR lottie OR "after effects" OR "svg motion" OR kinetic'),
    ("storyboard", 'storyboard OR "shot breakdown" OR screenplay'),
    ("captions", 'subtitle OR caption OR srt OR transcript OR "burn-in"'),
    ("ai-video", '"image to video" OR "text to video" OR "ai video" OR veo OR runway OR kling'),
    ("screen-demo", '"screen recording" OR "demo video" OR screencast OR walkthrough'),
]

PER_BUCKET = 6
MIN_SCORE = 62


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
        for name, desc, path in rows:
            d = os.path.dirname(path)
            if d in seen_dirs:
                continue
            seen_dirs.add(d)
            slug = os.path.basename(d)
            if slug in existing or slug in chosen:
                continue
            # Flattened-path scrape artefacts are long, machine-generated slugs;
            # they read badly as installed skill names.
            if slug.startswith(("topic-", "ghscan-")) or len(slug) > 40:
                continue
            sc, why = sp.score(path)
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
    for sc, p, slug in items:
        print(f"  {sc:3d}  {slug:45s} {chosen[slug][2]}")

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
