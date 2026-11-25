---
name: rekordbox-ingest-pipeline
description: Incremental pipeline for newly imported rekordbox tracks — analyze, tag, BPM-fix, bucket, and rebuild Matching without recomputing anything for existing tracks. Use when new tracks were imported and the index/tags/matching need updating.
---

# Progressive ingest for new tracks

Reference orchestrator: `scripts/ingest_new_tracks.sh`. Drive it phase by
phase with user review — don't fire-and-forget. Every step is incremental and
idempotent; nothing is recomputed for old tracks.

## Phase A — analysis (rekordbox may stay OPEN)

1. Sync new track file paths from rekordbox into the local cache
   (`analyzer.py paths`).
2. Embeddings + mood for tracks with no embedding yet (`analyze_fast.py`).
3. Independent BPM/key estimates for unanalyzed tracks (`essentia_features.py`).
4. Merge both into `metadata.sqlite` (`analyzer.py merge-v2` / `merge-audio`).

Long-running; if many tracks, run in background and monitor the log.

## Phase B — rekordbox writes (rekordbox must be CLOSED)

**Order matters — BPM correction before anything that buckets by BPM:**

1. `bpm_halftime_fix.py` — halve stored BPM where genre family says halftime
   AND the ML tempo confirms (≈ rb/2 within 5%). Idempotent by construction.
2. `ingest_tags.py` — fill My Tags (Genre/Energy/Vibe) for untagged tracks
   only, into the existing consolidated banks + `#hashtag` comments. Never
   create new banks during ingest.
3. Rebuild/extend sorted buckets — new tracks join frozen clusters by centroid
   cosine; never re-run k-means (`rebuild_nocat_bpm.py`).
4. `build_matching.py` — diff-based Matching update (insert new, soft-delete
   dropped, no churn on unchanged).

Always run the dry-run pass and show the user before `--apply`.

## After apply

1. User syncs the USB from rekordbox (incremental).
2. Push Matching into BOTH stick databases (`push_matching_to_usb.py` and
   `push_matching_legacy.py`) — sync alone leaves stale subsets there. See the
   rekordbox-matching-usb skill.
