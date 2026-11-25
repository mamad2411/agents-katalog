---
name: beets-lossless-automation
description: Operate and automate a lossless music library with beets — intake/import loops, tagging policy, quality-ranked deduplication (WAV > FLAC > lossy), fingerprints, quarantine-not-delete policy, and library maintenance. Use whenever a task involves beet/beets commands, music library imports, tagging, dedup, fingerprinting, duplicate cleanup, lossless archive management, or beets configuration — even if the user just says "organize my music", "clean up duplicates", or "import these albums" without naming beets.
---

# beets-lossless-automation

Drive a beets-managed lossless music library with minimal human intervention:
import, identify metadata, normalize tags, fingerprint, deduplicate with an
explicit quality policy, quarantine (never delete) losers, validate, and
report. The core discipline: **every decision is recorded, every rejection is
reversible, and the quality policy beats naive bitrate comparisons.**

This skill was forged on a real 13k-track library migration (Debian 12 CT,
beets 1.6.0) and every command/config claim in the references was verified
against plugin source or executed live. Where behavior differs between beets
versions, the reference files say so explicitly.

## First moves in any beets session

```bash
beet version              # pin the version BEFORE trusting any config advice
beet config -p            # where is the real config?
beet config -d            # where is the real library DB?
beet stats                # how many items, what state
```

Read `references/version-notes.md` next if the version is not 2.x — 1.6.0 has
silent traps (interactively-prompting badfiles, list-form duplicates keys that
match nothing, incremental disabling resume) that produce *empty results
instead of errors*.

## The quality policy (the part agents get wrong)

Duplicate decisions happen **only after** establishing two files are the same
recording. Then rank:

1. Verified matching MusicBrainz track ID
2. Lossless over lossy
3. `quality_rank` — explicit numeric tiers, NEVER lexical `$format` sorting:

```text
WAV/BWF: 3   (beets calls this format "WAVE" — match both names!)
FLAC:    2
ALAC:    2   (same tier as FLAC; codec-inspect m4a before trusting extension)
MP3:     1   (and AAC/OGG/Opus/AIFF lossy-or-lesser: 1)
Unknown: 0
```

4. bit depth → 5. sample rate → 6. bitrate → 7. tag completeness → 8. file size

A WAV made from an MP3 is not an upgrade. Bitrate never proves losslessness.
If provenance is ambiguous after all of the above: **keep both, defer the
group** — never guess.

Why numeric ranks: the `duplicates` plugin tiebreak sorts values *lexically as
well as descending*, so `format` sorts `WAV` below `FLAC` — the exact opposite
of the policy. Inject an integer `quality_rank` field instead (pattern in
`references/bulk-injection.md`).

## Dedup pipeline (the proven sequence)

Run dedup **once, after all inputs are final** — full import done, all
fingerprints computed and injected. No incremental passes.

1. **Fingerprint outside beets.** Chroma-during-import = one AcoustID API call
   per file (measured: 46 s for 2 files → ~10 days for 19k). Local `fpcalc`
   runs offline at ~1–2.5 files/sec. The capture loop MUST record fpcalc's
   stdout even when it exits nonzero — trailing-junk files print a valid
   fingerprint *then* error on final decode; `|| return 0` discards them and
   silently skips ~14% of real-world libraries. See `references/fingerprints.md`.
2. **Inject via ORM, one transaction** — `references/bulk-injection.md`.
   13,318 items in 2.5 s; without the wrapping transaction it is one fsync per
   item and hours of disk storming.
3. **Dry-run and verify the mechanism on a scratch library first.** Confirm
   the plugin groups what SQL says it should group, and that the tiebreak
   keeps the file the policy says to keep. Config syntax that silently
   matches nothing is documented in `references/version-notes.md`.
4. **Execute with `--move` into a dated quarantine dir.** Never `--delete`.
   **Assert the quarantine shares the library's filesystem first**
   (`stat -c %d` on both) — a cross-filesystem `--move` silently becomes a
   copy+delete at ~3–8 MB/s on spinning disks and can fill a small root volume.
   This has already caused a disk-full incident once: see
   `references/quarantine-and-disk-safety.md`. On the same filesystem the move is
   an instant rename; collisions are handled by beets (`unique_path`). Keep the
   loser manifest (`-f '$path'` output).
   Then **purge the quarantined rows from the DB (rows only, `delete=False`)**
   before the next pass — otherwise the next pass re-groups the same losers with
   their own winners and moves them again.
5. **Report**: groups found, losers quarantined by format tier, kept-winner
   samples, files skipped as corrupt. Review with the user before any merge
   or quarantine cleanup.

Two passes cover real libraries: fingerprint-keyed (`-k acoustid_fingerprint
-k acoustid_length -s`) for audio-identical copies, and tag-keyed
(`-k albumartist -k album -k title -s`) for same-tags-different-audio. Pass
keys explicitly on the CLI — CLI keys always work; config `keys:` forms are
version-fragile (see version notes).

## Intake loop (new files arriving)

```bash
beet import --pretend CANDIDATE      # preview grouping/matches, keep output in the batch log
beet import -q CANDIDATE             # automated import; verify exit status + log after
```

- Set `quiet_fallback` explicitly. `skip` (default) leaves unmatched candidates
  in the inbox → the runner must move them to a dated deferred location; never
  treat "left in inbox" as terminal. `asis` imports with existing tags — only
  with deliberate policy.
- Set `duplicate_action: skip`. The importer must never decide upgrades: the
  native `upgrade` action compares raw bitrate only, no lossless/lossy
  distinction. All duplicate decisions belong to the dedup pass above.
- `import.copy: yes` leaves originals in the inbox — the runner archives them
  (move, never delete) to a dated collision-resistant dir only after verified
  import. Every candidate ends the run with a disposition: imported,
  skipped-duplicate, deferred, quarantined, or archived.
- Shell safety: quote path variables, `find -print0` + `read -d ''`/`xargs -0`,
  `--` before operands. Music filenames carry apostrophes, `$`, Unicode.

Full annotated config template (with version-gated blocks): 
`references/config-template.md`.

## Hard prohibitions

- Never delete audio files as part of routine automation — quarantine is the
  default disposition for rejected/unreadable/ambiguous/superseded files.
- Never `import.delete: yes` (config key, not a flag — audit the config).
- Never `duplicates.delete: yes` or the plugin's `--delete`.
- Never `beet import -L`: it treats arguments as a *library query* and retags
  matching existing items instead of importing.
- Never treat size/bitrate/sample-rate/container as proof of quality.
- Never invent MusicBrainz IDs or dates; unresolved metadata gets deferred,
  not guessed.
- Never let an artwork failure block audio import.

## Operational discipline on modest hardware

These come from a 2-core/5400-RPM-HDD host and apply anywhere I/O-bound:

- Long jobs run detached (`nohup`), `nice`d/`ionice`d, single-worker, under an
  `flock` lockfile so relaunches cannot stack. Foreground SSH launches that
  time out **orphan their pipelines** — kill children in pipeline order and
  verify with `pgrep -c` before relaunching.
- Verify progress by outputs (row counts, file counts), not by `pgrep -f`
  patterns that can self-match the monitoring script.
- After any crash-kill of a process holding the SQLite DB: verify through
  beets' own read path (`beet ls -f '$field'`), not just raw SQLite — the two
  views can disagree after external writes; re-run the write via ORM to
  reconcile.
- Nested `ssh | pct exec | bash -c` quoting burns hours. Write scripts to
  files and push them (base64 over the transport), never inline-quote.
- **Disk-space safety for any bulk file operation:** know which volume you are
  writing to (`findmnt -T PATH`, compare `stat -c %d`), and when recovering from
  a full disk use `rsync -a --remove-source-files` so space is reclaimed per
  file — `cp`-then-`rm` holds the disk at 100% for the entire copy, which on a
  slow disk can mean hours of hazard for the services sharing that volume.

## Instance addendum: CT 101 "homelab-core"

- `ssh root@192.168.2.242`; beets 1.6.0 / Python 3.11.2 / Debian 12.15
- DB `/root/.musiclibrary.db`; config `/root/.config/beets/config.yaml`
  (asis import: `autotag/write/copy/move` all no — zero file mutation)
- Library volume `/opt/homelab/navidrome/music`; Navidrome runs in Docker here
  (production: rescan via Subsonic API, never restart without asking)
- `PYTHONPATH=/usr/share/beets` required for ORM scripts (non-standard install)
- No `sqlite3` CLI, no `lsof`, no `ffprobe` in this CT
- `fpcalc` from the `chromaprint` package; fingerprints cached at
  `/root/fingerprints.tsv` (path⇥duration⇥fingerprint) with done-list
  `/root/fp-done.txt`
- Full environment: `pvnkmnk/homelab-proxmox-ansible` → `docs/findings/2026-09-18-homelab-music-library-cleanup.md` (canonical; that repo is the authority for homelab state), plus `docs/LIBRARY_CLEANUP_WORKSTREAM.md` for the live workstream

## Upgrade path (planned, not yet executed)

The library currently runs beets 1.6.0. Upgrade to 2.x (2.13.1+, which adds
the badfiles automation keys) is scheduled **after** the current
dedup/merge pipeline completes — never mid-pipeline. The playbook, including
the fresh-Debian-13-CT option and post-upgrade revalidation checklist, is in
`references/upgrade-path.md`.

## References

- `references/version-notes.md` — **read this on any non-2.x install**;
  silent-failure config traps verified against 1.6.0 source
- `references/config-template.md` — full annotated config, version-gated
- `references/fingerprints.md` — fpcalc capture loop, resumable design, the
  nonzero-exit bug
- `references/bulk-injection.md` — ORM single-transaction attribute injection,
  WAVE naming, verification rules
- `references/quarantine-and-disk-safety.md` — **read before any
  `--move`**; the cross-device quarantine incident and the guard that prevents it
- `references/upgrade-path.md` — 1.6.0 → 2.x playbook
