---
name: batocera-ops
description: >-
  Use when connecting to or operating a Batocera arcade/retro-gaming cabinet
  over SSH: establishing the connection, understanding its read-only rootfs and
  /userdata layout, finding config/log/ROM paths, applying changes safely,
  verifying a display/config change end-to-end without a controller, or
  diagnosing why a setting reverts to its default on every launch (configgen).
  Foundation for the other batocera-* skills (roms, display, tuning,
  maintenance). Covers
  sshpass, batocera.conf, EmulationStation, the ES HTTP API, and
  batocera-screenshot. Not for game recommendations.
compatibility: Requires SSH access to a Batocera host (tested on v41-v43).
---

# Batocera Ops

Foundation for operating a Batocera cabinet with a coding agent over SSH. Read
this first; the sibling skills (`batocera-roms`, `batocera-display`,
`batocera-tuning`, `batocera-maintenance`) assume the connection pattern, path
model, and safety doctrine defined here.

## Overview

Batocera is an immutable-rootfs Linux distro for retro gaming. The system
partition is **read-only**; everything you can change lives under `/userdata`.
EmulationStation (ES) is the frontend; RetroArch and standalone emulators do
the playing. Configuration is layered: a single `batocera.conf` holds most
settings, but launch-time code (configgen) regenerates per-emulator configs on
every launch, so hand-edits to the generated files get stomped. Getting these
two facts right prevents most wasted sessions.

## Connecting

Batocera defaults to password SSH (no key from a fresh client). Parameterize
the host so nothing is hardcoded:

```bash
export BATOCERA_HOST=192.168.1.50   # your cabinet's LAN IP
```

Batocera's **documented default credentials are `root` / `linux`.** If yours
still uses them, change the password (ES menu → System Settings → Security, or
`passwd` over SSH) — a machine you SSH into as root should not ship with a
published password. The examples below read the password from an env var so it
never lands in shell history or a committed file:

```bash
export BATOCERA_PASS='linux'   # replace with your actual password

# convenience wrapper used throughout these skills
SSHB() { sshpass -p "$BATOCERA_PASS" ssh -o StrictHostKeyChecking=no "root@$BATOCERA_HOST" "$@"; }
SCPB() { sshpass -p "$BATOCERA_PASS" scp -o StrictHostKeyChecking=no "$@"; }
```

Run a command: `SSHB 'cat /usr/share/batocera/batocera.version'`
Copy down: `SCPB "root@$BATOCERA_HOST:/userdata/screenshots/x.png" .`
Copy up:   `SCPB ./file "root@$BATOCERA_HOST:/userdata/system/"`

If key auth is set up, drop `sshpass`. Batocera drops idle SSH connections; for
long-running work use `nohup … &` or `screen`/`tmux` if installed. Rapid
reconnects can trip the SSH daemon's throttle (transient "Permission denied");
wait a few seconds and retry rather than assuming the password is wrong.

## The filesystem model

- **Rootfs is read-only.** You cannot persist edits to `/usr`, `/etc`, or
  `/bin`. Anything you write there vanishes on reboot (or fails outright).
- **`/userdata` is the only writable tree.** ROMs, configs, saves, BIOS,
  decorations, shaders, scripts, logs — all under `/userdata`.
- Do work **on the box**, not over an SMB mount from another machine — the
  cabinet's own tools (chdman, 7z, python3) are already present and paths line
  up. Python 3 is available; there is no compiler.

## Key paths

| Path | What |
|------|------|
| `/userdata/roms/<system>/` | ROMs, one dir per system (see `batocera-roms`) |
| `/userdata/roms/<system>/gamelist.xml` | Per-system metadata + `<hidden>` flags |
| `/userdata/system/batocera.conf` | Main config: one file, `key=value` |
| `/userdata/system/configs/` | Per-emulator configs (many are regenerated) |
| `/userdata/system/configs/retroarch/retroarchcustom.cfg` | RetroArch overrides |
| `/userdata/system/configs/emulationstation/es_settings.cfg` | ES frontend settings |
| `/userdata/system/services/` | Boot services (v43+; replaced `custom.sh`) |
| `/userdata/system/logs/` | Per-launch + component logs (see reference) |
| `/userdata/decorations/` | Bezel/overlay packs |
| `/userdata/shaders/` | User shader presets and configs |
| `/userdata/saves/` | Emulator save states and SRAM |
| `/userdata/bios/` | BIOS files |
| `/usr/share/emulationstation/es_features.cfg` | Catalog of valid per-emulator setting keys + values (read-only; see batocera-conf reference) |
| `/userdata/screenshots/` | Where `batocera-screenshot` writes |

`batocera-conf` precedence, the configgen regeneration model, and where a
setting must live to survive a launch are in
[references/batocera-conf.md](references/batocera-conf.md). The log inventory
and ES restart mechanics are in
[references/emulationstation.md](references/emulationstation.md).

## Safety doctrine

This is a **shared physical device**, often the family/party arcade cabinet.
Treat it accordingly.

1. **Non-destructive first.** Read before you write. Prefer hiding to deleting,
   moving to removing, appending to overwriting. `/userdata` is the only thing
   standing between you and a re-image.
2. **Back up before you touch a config or gamelist.** One line, every time:
   `SSHB 'cp /userdata/system/batocera.conf /userdata/system/batocera.conf.bak-$(date +%Y%m%d-%H%M%S)'`
   Same for any `gamelist.xml` before editing it.
3. **Never inject synthetic input.** Do not use uinput virtual keyboards,
   `xdotool`, `evemu`, or virtual gamepads to "drive" the cabinet. Someone may
   be physically holding the controller; injected keypresses land in *their*
   open menu and silently change settings. If a test needs button/stick input,
   describe the exact steps and ask the human to drive. (The ES HTTP API launch
   below is **not** synthetic input — it is a documented control endpoint — but
   it does commandeer the screen, so skip it if someone is playing.)
4. **Verify against ground truth, not assumption.** After a change, re-read the
   file or launch the game and look. "It should work" is not evidence. See the
   verify loop below.

## Remote verify loop (no controller needed)

The signature agent-native capability: change a display/config setting and
confirm it end-to-end without touching the cabinet, using the ES HTTP API to
launch and `batocera-screenshot` to see the result.

```bash
# 1. Launch a specific ROM via the ES HTTP API (runs ON the box, port 1234).
#    Works even for files ES doesn't list in its menu.
SSHB "curl -s -m3 -X POST http://127.0.0.1:1234/launch -d '/userdata/roms/<system>/<rom>'"

# 2. Wait 20-45s. Title/attract screens can be slow; if the shot is black,
#    take a second one a few seconds later before concluding anything.

# 3. Capture the framebuffer (this exact command; there is no swissknife
#    --screenshot). Writes a PNG into /userdata/screenshots/.
SSHB "batocera-screenshot"

# 4. Kill the running emulator, copy the newest screenshot down, and look at it.
SSHB "batocera-es-swissknife --emukill"
SCPB "root@$BATOCERA_HOST:/userdata/screenshots/$(SSHB 'ls -t /userdata/screenshots | head -1')" /tmp/verify.png
# then Read /tmp/verify.png
```

**Config assertions after a libretro launch:** the *actual* values RetroArch
ran with are in
`/userdata/system/configs/retroarch/retroarchcustom.cfg` and
`.../cores/retroarch-core-options.cfg`, reflecting the **last** launch. Read
those to confirm a key landed, rather than trusting that your `batocera.conf`
edit took effect.

**Gotchas that waste a verify session:**
- **Piping RetroArch's output swallows it.** `retroarch … | grep` / `| tail`
  discards core errors silently. To see why a core failed, launch with
  `--log-file /tmp/ra.log` and read the file.
- **A stray manually-run `retroarch` blocks ES launches** — the ES launch exits
  instantly (~24ms, empty stderr, status 1). `SSHB 'killall -9 retroarch'`
  first.
- **Gamelist edits need ES stopped.** ES rewrites `gamelist.xml` on exit and
  clobbers live edits. Stop it (`/etc/init.d/S31emulationstation stop`) or use
  the SIGKILL-restart pattern in the emulationstation reference. Config edits to
  `batocera.conf` do not need this; gamelist XML edits do.
- **Check what ES actually lists** via the API:
  `SSHB "curl -s http://127.0.0.1:1234/systems/<system>/games"` (returns
  name/path/hidden per entry).

## Provenance and freshness

Batocera changes across releases (path renames, `custom.sh` → services, new
systems). These skills were distilled on v41-v43; commands are read-only unless
noted. Before trusting a version-specific claim, confirm the build:
`SSHB 'cat /usr/share/batocera/batocera.version'`. The canonical manual is the
[Batocera wiki](https://wiki.batocera.org); these skills capture operational
lessons the wiki doesn't, not a replacement for it.
