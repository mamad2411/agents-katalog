---
name: music-library-organizer
description: Import, tag, and organize music files using beets; enforce consistent folder structure, metadata, and MusicBrainz tagging across the local music library.
---

# music-library-organizer

## Purpose
Automate music file tagging and library organization using beets. Ingests raw downloads, applies MusicBrainz-backed metadata, enforces directory structure, deduplicates, and prepares files for streaming via Subsonic/Navidrome.

> **Deep beets mechanics live in `beets-lossless-automation`** (sibling skill):
> version-specific config traps, the fpcalc fingerprint capture loop, ORM
> bulk-injection patterns, full config template, and the 1.6.0→2.x upgrade
> playbook. This skill stays instance-focused (CT 101 workflow); go there for
> anything version-fragile or mechanical.

## Invocation
- "Organize new music downloads with beets"
- "Tag and import [artist/album] into library"
- "Fix missing tags in music library"
- "Deduplicate music library"
- "Run beets import on download folder"

## Workflow Steps
1. **Scan:** Identify new files in the slskd download directory (or configured inbox).
2. **Import:** Decide tag policy explicitly first. `beet import -A` means **asis — beets imports WITHOUT MusicBrainz lookup** (opposite of auto-tag). For MusicBrainz-backed tagging run plain `beet import` (interactive) or `beet import -q` after confirming config; never assume `-A` tags anything.
3. **Review:** Flag low-confidence matches for manual review; log ambiguous items.
4. **Organize:** Move/copy files into the canonical library structure: `Library/Artist/Year - Album/Track - Title.ext`.
5. **Tag:** Apply standardized tags: artist, album, year, genre, MusicBrainz IDs, ReplayGain.
6. **Deduplicate:** Run `beet duplicates` and resolve conflicts (keep highest quality).
7. **Notify:** Signal `subsonic-media-server` to rescan library after import completes.
8. **Log:** Record import summary in `homelab-logbook`.

## Safety
- Never delete original files without explicit confirmation.
- Preserve original files in an inbox backup before moving.
- Do not overwrite manual tag edits without user approval.
- Validate file integrity (checksum) before and after move.

## MCP
- No dedicated MCP; invoked via shell commands or agent subprocess calls to `beet` CLI.
- Pairs with `slskd-mcp` for end-to-end acquisition-to-library pipeline.

## Dedup Strategy (verified on the homelab-core library)

0. **Config syntax that actually works (beets 1.6.0, validated end-to-end on a scratch library):**
   ```yaml
   duplicates:
     keys: albumartist album title        # BARE STRING — a YAML list [albumartist album title] silently matches nothing
     tiebreak:
       items: [quality_rank, bitdepth, samplerate, bitrate]  # must nest under items:/albums: — flat mapping is silently ignored
   types:
     quality_rank: int
   ```
   The tiebreak list sorts **descending on every field**, so this order = WAV > FLAC > MP3, then deeper → higher rate → higher bitrate.

## Bulk Attribute Injection (the only pattern that works here)

- Use the beets ORM inside **one transaction**: `with lib.transaction(): for item in lib.items(): item.attr = x; item.store()` — 13,318 items in 2.5s. Row-by-row stores without a wrapping transaction = one fsync per item = hours of D-state disk storm on a 5400 RPM HDD.
- **beets names WAV files `WAVE`**, not WAV — rank mappings must match both or the WAV tier silently sinks to the bottom.
- If beets is installed at a non-standard path, `from beets.library import Library` needs that path on `PYTHONPATH` (here: `/usr/share/beets`).
- Verify attribute changes via `beet ls -f '$attr'` (beets' own read path), not raw SQLite — the two views can disagree after external writes.
- `pgrep -f "beet.*import"` self-matches any script whose source contains `from beets.library import` — use `pgrep -af` and eyeball the output.

1. **Fingerprints via local `fpcalc`, not the chroma plugin during import.** Chroma during import does a per-file AcoustID API round-trip (measured: 46s for 2 files → ~10 days for a 19k-track library). Local `fpcalc` runs ~2.5/sec offline; bulk-inject the results into the beets DB afterwards.
2. **`beet duplicates` is the native dedup engine.** Set keys `[acoustid_fingerprint, albumartist album title]`. Quality order (idols' explicit policy): **WAV > FLAC > MP3**, all bitrates within a tier equal, then bit depth → sample rate → bitrate as fidelity proxy. **Gotcha:** the plugin sorts tiebreak fields lexically, so raw `format` ranks WAV *below* FLAC — use a computed rank field (e.g. a field plugin exposing `quality_rank`: WAV=3, FLAC=2, MP3=1) and tiebreak `[quality_rank, bitdepth, samplerate, bitrate]`. Verify which item the plugin keeps with a scratch-library test before any real `--move`. Use `--move` into a quarantine dir + `--log` for the report.
3. **Non-destructive policy (standing order):** quarantine duplicates with a report, never delete. Keep sources + a pre-change snapshot until the user approves. Run dedup **once, after all matching data (fingerprints + full import) is complete** — no incremental dedup passes.
4. **Disk-space check gates the merge:** if free space < staged size, merge must be a **move**, not a copy.
5. **AcoustID API lookups are for duplicate groups only** (~100s of calls), never the whole library. MusicBrainz needs no key; AcoustID needs a free key.

## Instance Addendum: CT 101 "homelab-core" (192.168.2.242)

- Access: `ssh root@192.168.2.242`; beets 1.6.0 / Python 3.11.2; DB `/root/.musiclibrary.db`
- Library volume: `/opt/homelab/navidrome/music` (590 GiB, watch free space)
- Config: `/root/.config/beets/config.yaml` — `autotag: no, write: no, copy: no, move: no` (asis import, zero file mutation); chroma configured with idols' AcoustID key
- Staging dir convention: `.staging-YYYYMMDD/` (hidden); rollback snapshot `pre-dedup-YYYYMMDD` on PVE
- Container facts: no `lsof`/`fuser` (use `/proc/*/fd` scanning); no ffprobe (beets DB already stores bitrate/depth/rate)
- Host is a 2-core/5400-RPM-HDD laptop — heavy beets/fpcalc work must run `nice -n 19 ionice -c3`, single-worker, with an `flock` lockfile so relaunches can't stack
- Navidrome runs in Docker on this CT — production; rescan via Subsonic API, never restart without asking
- Full verified state: `pvnkmnk/homelab-proxmox-ansible` → `docs/findings/2026-09-18-homelab-music-library-cleanup.md` and `docs/LIBRARY_CLEANUP_WORKSTREAM.md` (canonical). Deep beets mechanics live in the `beets-lossless-automation` skill.

## References
- beets documentation: https://beets.readthedocs.io/
- MusicBrainz: https://musicbrainz.org/
- beets GitHub: https://github.com/beetbox/beets

## Companion Skills
- `slskd-media-acquisition` — source of new music files
- `subsonic-media-server` — streaming target after organization
- `dj-library-curator` — curation layer on top of organized library
- `homelab-logbook` — import event logging
