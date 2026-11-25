---
name: batocera-roms
description: >-
  Use when working with ROMs and gamelists on a Batocera cabinet: figuring out
  which directory a system's ROMs go in, why a game does not appear in the menu,
  which file formats and extensions a system accepts, curating a large library
  by hiding rather than deleting, editing gamelist.xml safely, cleaning up
  multi-disc games, or verifying dumps against No-Intro/Redump DATs. Covers
  extensionless-ROM-in-zip failures, the 3DO/Opera no-m3u trap, cave3rd, and the
  es_systems_custom.cfg landmine. Not for shaders/bezels (batocera-display), or
  ROM directories renamed by a Batocera version upgrade (batocera-maintenance).
compatibility: Requires SSH access to a Batocera host (tested on v41-v43).
---

# Batocera ROMs

Managing the game library: where ROMs live, why they do or don't show up, how to
curate a big collection without deleting anything, and how to verify dumps.
Assumes the connection pattern and safety doctrine from `batocera-ops`.

## System directories

ROMs live in `/userdata/roms/<system>/`, one directory per system. The directory
name is Batocera's internal system name, which is **not always** the obvious
one. Don't guess — look it up on the box:

```bash
# Every system Batocera knows, with its dir name and display name:
SSHB "grep -E '<name>|<fullname>' /usr/share/emulationstation/es_systems.cfg"

# What you actually have ROMs for:
SSHB "ls /userdata/roms/"
```

Names that trip people up: Cave CV1000 arcade lives in **`cave3rd`** (not
`cv1000`); Odyssey 2 is `odyssey2` (renamed from `o2em`); Half-Life is
`halflife` (renamed from `xash3d_fwgs`). Directory renames across versions are
common — the batocera-maintenance migration reference lists the ones that bite.

## Why a game doesn't appear

In rough order of likelihood:

1. **Wrong extension for that system.** Each system accepts a fixed set of
   extensions; a file with any other extension is invisible to ES. Check the
   accepted list:
   `SSHB "grep -A2 '<system>' /usr/share/emulationstation/es_systems.cfg | grep extension"`.
   A bare `.bin` is a frequent offender — for many disc systems `.bin` is *not*
   an ES extension (you need a `.cue` or `.chd`).
2. **It's hidden.** `<hidden>true</hidden>` in `gamelist.xml`, or its whole
   system is in the ES HiddenSystems list. Hidden games still exist on disk —
   this is a feature, see curation below.
3. **Extensionless ROM inside a zip.** ES lists the `.zip`, but the emulator
   refuses to load it because the inner file has no recognizable extension. See
   the formats reference — this fails *silently* (RetroArch exits ~1s, status 1,
   "Could not read content file").
4. **A custom system-list file overrode the stock list.** If a whole swath of
   systems vanished, suspect `es_systems_custom.cfg` — see the landmine below.

## gamelist.xml anatomy

Each system's `/userdata/roms/<system>/gamelist.xml` is per-game metadata:

```xml
<gameList>
  <game>
    <path>./Super Mario World (USA).sfc</path>
    <name>Super Mario World</name>
    <desc>...</desc>
    <image>./media/images/Super Mario World (USA).png</image>
    <hidden>true</hidden>          <!-- present + "true" = hidden from menu -->
    <favorite>true</favorite>
  </game>
</gameList>
```

- `<path>` is relative to the system dir and includes the extension. It's the
  join key to the file on disk.
- Removing the `<hidden>` element (or setting it to anything but `true`) unhides.
- **ES rewrites this file on exit.** Never edit it while ES is running and then
  let ES exit cleanly — it clobbers your edit. Stop ES or SIGKILL-restart it
  (see `batocera-ops` → emulationstation reference). Back the file up first.

## Curation: hide, don't delete

The core methodology for taming a large or messy library, e.g. building a
focused view for an arcade cabinet: **set `<hidden>true</hidden>`, never `rm`.**

Why hiding wins:
- **Reversible in one flag.** ROMs stay on disk; flip the flag to restore.
- **Non-destructive** — aligns with the `batocera-ops` doctrine on a shared
  machine. A wrong call costs a flag flip, not a re-download.
- **Composable** — you can layer passes (per-game hides, cross-platform dedup,
  regional-variant dedup) and roll any one back independently by restoring that
  pass's gamelist backup.

Workflow:
1. Back up the gamelist(s) you'll touch:
   `cp gamelist.xml gamelist.xml.bak-<tag>`.
2. Stop ES (or plan a SIGKILL-restart) so your edits survive.
3. Edit `<hidden>` flags — scripted for anything past a handful.
4. Restart ES and verify counts via the API:
   `curl -s http://127.0.0.1:1234/systems/<system>/games` and count
   `hidden` entries.

Methodology detail (system-level HiddenSystems, cross-platform canonicalization
/ 1G1R, regional and format dedup) is in
[references/curation.md](references/curation.md). It is method only — bring your
own taste; there are no game lists here.

## Multi-disc games

Multi-disc CD games (PSX, Saturn, 3DO, Sega CD…) each show every disc as its own
menu entry by default, cluttering the list. The clean fix — one visible entry
per game, remaining discs hidden, per-disc launch still possible — plus the
disc-swap mechanics that differ by emulator, is in
[references/formats-and-quirks.md](references/formats-and-quirks.md). A
ready-to-adapt implementation for 3DO is
[scripts/fix-3do-multidisc.py](scripts/fix-3do-multidisc.py). **Do not reach for
`.m3u` on 3DO/Opera** — that core doesn't support playlists (a documented trap
the script explains).

## Format landmines

Full detail in [references/formats-and-quirks.md](references/formats-and-quirks.md);
the ones that cost the most time:

- **`es_systems_custom.cfg` REPLACES the stock system list, it does not merge.**
  Drop a custom system definition in as `es_systems_custom.cfg` and ES boots
  with *only* your custom systems — every stock system disappears. To *add* a
  system, use a differently-named merge file, not `es_systems_custom.cfg`.
- **Extensionless ROM inside a zip** → silent load failure. `unzip -Z1 *.zip`
  and check the inner suffix; rezip with a proper extension.
- **3DO/Opera has no `.m3u` support**; multi-disc needs the per-entry approach.
- **Bare `.bin` disc images** are invisible on systems whose ES extension list
  wants `.cue`/`.chd`. Generate a `.cue`.

## Verifying dumps against DATs

To confirm your ROMs are known-good dumps (right data, not just right filename),
verify against **No-Intro** DATs (cartridges, hash match) and **Redump** DATs
(discs, extract + hash). Methodology, tiers, and known limits (GD-ROM CHDs that
can't hash-verify, Sega CD CDDA mismatches) are in
[references/dat-verification.md](references/dat-verification.md), with a
ready-to-run [scripts/dat-verify.py](scripts/dat-verify.py).
