---
name: photo-intake-processing
description: Use when importing, reviewing, indexing, selecting, compressing, or preparing site photos and videos for landscape analysis, AI concepts, client presentation, or final visualization.
---

# Photo Intake Processing

## Goal

Make site photo capture useful for analysis and AI: preserve originals, select useful shots, describe angles, and identify missing views.

## Process

1. Treat `01_site_survey/01_photos_raw` as immutable source archive.
2. Store selected copies in `01_site_survey/02_photos_selected`.
3. Fill or update `01_site_survey/PHOTO_INDEX.md`.
4. For each important photo, record shooting point, direction, visible content, and use.
5. Check required groups: house, entry, boundaries, neighbors, trees, utilities, problem zones.
6. For AI-ready materials, prepare a short list of frames: house, key structures, general site view, problem zones.

## Rules

- Do not delete or overwrite raw files.
- Do not put all photos into client presentation.
- If photos need compression, keep a copy and preserve the source link.
- If the angle is unclear, mark it as `needs_orientation` instead of guessing confidently.

## Output

- Updated `PHOTO_INDEX.md`.
- Selected photo list.
- Missing angles or repeated measurement list.
