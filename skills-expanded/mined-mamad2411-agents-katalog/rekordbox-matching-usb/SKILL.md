---
name: rekordbox-matching-usb
description: Populate rekordbox's Matching (track suggestions) from embeddings and push it onto USB export databases (exportLibrary.db and exportExt.pdb) when device sync won't. Use for Matching, related-tracks, or USB export DB work.
---

# Matching pairs + USB export injection

Reference implementations: `scripts/build_matching.py`,
`scripts/push_matching_to_usb.py` (OneLibrary `exportLibrary.db`),
`scripts/push_matching_legacy.py` (classic `exportExt.pdb`).

## Building pairs (master.db `djmdRecommendLike`)

- **Similarity threshold matters**: cosine ≥ **0.90** on the 1280-dim
  embeddings. 0.85 sits near the random-pair 99th percentile in this space and
  yields millions of junk pairs. Calibrate against random pairs first.
- BPM-compatible within 8% at 1:1, 2:1, or 1:2 (use corrected/feel BPM).
- Rank by similarity + small bonus (≈ 0.02) for Camelot-compatible keys
  (same / ±1 / relative).
- Top ~6 partners per track, deduped to one row per unordered pair.
- **Diff-based updates**: compute the desired pair set, INSERT only new pairs,
  soft-delete dropped ones (`rb_local_deleted=1` + fresh USN — rekordbox's own
  mechanism, so incremental device sync carries removals), leave unchanged rows
  untouched to avoid USN churn.

## Why direct USB writes are needed

Rekordbox's incremental device sync uses a change ledger; rows written to
master.db outside the rekordbox UI never enter it, so synced sticks keep stale
Matching subsets (observed across repeated syncs). Fix: write the stick's own
databases directly after syncing. Sync leaves those tables alone afterward, so
the injection survives.

## The export databases

- `PIONEER/rekordbox/exportLibrary.db` — SQLCipher-encrypted SQLite
  (Device Library Plus / OneLibrary; read by CDJ-3000-class players). The key
  is a static one shared by all rekordbox installs — NOT distributed in this
  repo; supply via `RB_DLP_KEY` env var or a `.dlp_key` file. Its `content`
  table maps `masterContentId` → master.db ContentID for exact ID translation.
  Skip pairs whose partner isn't on the stick.
- `PIONEER/rekordbox/exportExt.pdb` — the classic binary format; **this is
  what XDJ-XZ-class gear actually reads** (deck-verified). Page-level binary
  writing: audit the ID map and require byte-identical page round-trips as
  safety gates before touching it.

Both pushes follow the standard contract: back up the target DB, dry-run by
default, `--apply` to commit. Never write while rekordbox is syncing.
