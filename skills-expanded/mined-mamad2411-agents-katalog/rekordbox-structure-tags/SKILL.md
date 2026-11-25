---
name: rekordbox-structure-tags
description: Organize a rekordbox library — genre-first folder structure, My Tags derived from structure, comment-hashtag mirroring, hardware 4-bank limit. Use when restructuring playlists/folders or designing a tagging scheme.
---

# Library structure and tagging scheme

## Philosophy (agree on this with the user before scripting)

- **Folders/playlists = crates & sets** — curation and order (genre browsing, gig prep).
- **Tags + native fields = attributes** — genre, label, energy, mood; things you filter by.
- **Smart playlists = the bridge** — auto-built crates from tag/field combos.

## Folder reorg

Target a small set of top-level folders (reference build: 8 genre folders +
`sets`, `_unsorted`, `_system`, plus any personal crates kept separate).
Script it with pyrekordbox `move_playlist`; see `scripts/reorg.py`. Decide the
full target tree on paper first and review it with the user.

## Derive tags from structure — never double-enter

- **Genre** My Tag ← top-level folder membership (`scripts/genre_situation.py`).
- **Label** My Tags ← label-crate playlist membership (`scripts/tag_and_merge.py`).
- **Energy** ← existing energy/intensity playlists.

## Comment-hashtag mirror

CDJs don't show My Tags on every screen. Mirror every tag into the Comment
field as `#hashtags` (append, dedupe, never clobber existing comment text).
Comments are visible and searchable on all hardware.

## Hardware limit: 4 My Tag banks

XDJ/CDJ Track Filter shows only **four** My Tag categories. If banks
accumulate, consolidate by re-parenting `DjmdMyTag` rows (assignments follow
the tag IDs); soft-delete emptied banks. See `scripts/mytag_consolidate.py`.
Reference layout: Genre / Energy / Vibe / Label.

## Rules of thumb

- Verify "duplicates" by comparing ContentIDs, not names/counts.
- Keep other people's crates (partner, b2b collaborators) out of the genre
  system entirely.
- Coarse genre beats fine genre for tags — folders and clustering handle nuance.
