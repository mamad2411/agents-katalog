---
name: rekordbox-metadata-enrichment
description: Enrich rekordbox tracks with genre/label/year/catalog from Discogs and Spotify via a local SQLite cache with confidence-gated, fill-empty application. Use when tracks are missing genre, label, year, or catalog metadata.
---

# Metadata enrichment (Discogs + Spotify)

Reference implementation: `scripts/analyzer.py`. Architecture:

```
fetch (slow, API, resumable)  →  metadata.sqlite (local cache)  →  apply (fast, gated, fill-empty)
```

Never write API results straight into rekordbox — cache locally first, so
fetching is incremental/resumable and application is reviewable and re-runnable.

## Fetch

- **Discogs** (the workhorse): search by artist/title; if the title contains a
  `[CATNO]`, search by catalog number instead — much more accurate for
  white-labels/promos. Free token, hard cap 60 req/min, no paid tier. A large
  library takes about a day in the background.
- **Spotify**: client-credentials auth (no user login). Search `isrc:<ISRC>` for
  an exact match, then fetch artist genres + album release date.
  **The audio-features endpoint is DEAD for new apps (Nov 2024, returns 403)** —
  probe once, mark dead, don't retry. Use local ML models for audio features
  instead (see rekordbox-audio-analysis skill).
- Pluggable sources: a `SOURCES` registry of `src_<name>(db, track, ctx)`
  functions plus a generic `feature(rb_id, source, name, value)` table means a
  new source needs no schema change.
- Score each match 0–1 (name similarity, catno hit, year plausibility).

## Apply

- `--min-confidence` gate (0.55–0.6 worked well; below that, matches get bad).
- **Fill-empty only** — never overwrite store metadata.
- Record provenance: `(rb_id, field, value, source, confidence)` for every
  applied value, so weak fills can be found and upgraded when better sources
  are added later.
- Follow every rule in the rekordbox-db-safety skill.

## Field mapping used

Genre←Discogs style, Label←Discogs label, Year←release year,
Catalog#←rekordbox `Subtitle` field (visible, otherwise unused).

## Skip-list caution

If you filter out "junk" tracks before fetching/analyzing, don't key on an
empty Artist field — plenty of real music has artist baked into the title.
Gate on duration instead (e.g. keep anything ≥ 60s).
