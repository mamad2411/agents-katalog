---
name: batocera-display
description: >-
  Use when working on how games look on a Batocera cabinet: CRT and other
  shaders, shaderset resolution and per-game shader overrides, bezel/overlay
  artwork and alignment, generating missing .info sidecars, filtering
  unusable bezels, seasonal bezels and boot splash clips, pinning the display
  resolution, or diagnosing moire and
  cropped/misaligned game viewports inside bezels. Covers why a shaderset seems
  invalid, why .info top values are not alpha coordinates, and why Mega-Bezel
  per-game art fails. Not for performance/framerate tuning (batocera-tuning).
compatibility: Requires SSH access to a Batocera host (tested on v41-v44).
---

# Batocera Display

Shaders, bezels, and display mode — everything about how the picture looks.
Assumes the connection pattern, `batocera.conf`/configgen model, and verify loop
from `batocera-ops`. Because display changes are visual, the
`batocera-ops` **remote verify loop** (ES HTTP API launch + `batocera-screenshot`)
is your primary tool here: never declare a shader or bezel "working" from the
config alone — launch it and look.

## Shaders

Shaders are assigned per-system (or per-game) in `batocera.conf`. Two key
mechanisms and the traps around each.

### `shaderset` resolves against TWO search paths

`<system>.shaderset=<name>` is a **folder-name lookup** resolved against both:

1. `/userdata/shaders/configs/<name>/` (user-installed)
2. `/usr/share/batocera/shaders/configs/<name>/` (system-bundled)

Checking only one path is enough to wrongly declare a preset invalid. Some
built-in names are aliases that resolve to a preset deep under
`/usr/share/batocera/shaders/`. Before concluding a `shaderset` value is dead:

```bash
SSHB "find /userdata/shaders /usr/share/batocera/shaders -maxdepth 3 -iname '<name>*'"
```

And read the launch log for the shader actually used on the last launch — it is
authoritative:

```bash
SSHB "grep -i 'set-shader\|shader' /userdata/system/logs/es_launch_stdout.log | tail"
```

### Two shader keys: `shaderset` vs `-renderer.shader`

- `<system>.shaderset=<name>` — a Batocera shaderset folder (may bundle bezel
  art, e.g. Koko-AIO/Duimon presets).
- `<system>-renderer.shader=<path>` — a direct RetroArch `.slangp` path (relative
  to the shaders dir, or absolute). This is how you assign a plain CRT preset
  like `crt/crt-super-xbr` or a custom `.slangp`.

Per-game overrides use the exact-filename key from `batocera-ops` →
batocera-conf: `snes["Super Mario World (USA).sfc"]-renderer.shader=...`. A glob
(`snes["Star Fox*"]...`) **never matches**.

### Anti-moiré: integer scaling is impossible inside a custom-viewport bezel

A CRT mask shader (crt-royale and friends) can produce rainbow moiré when the
game isn't integer-scaled. The usual cure — `video_scale_integer` — **is ignored
for a custom viewport**, and bezels that force a custom RetroArch viewport (with
fractional coordinates) put you exactly there. So you cannot integer-scale inside
those bezels.

The workaround is to tame the mask instead of the scale: a wrapper `.slangp` that
`#reference`s the CRT preset and sets `mask_sample_mode_desired=1` (a
scale-tolerant mask sampling mode). Point the arcade systems' `-renderer.shader`
at the wrapper. Verify with before/after screenshots — this is precisely the kind
of change that must be seen, not assumed. Full detail in
[references/shaders.md](references/shaders.md).

### Pin the display mode in batocera.conf, not the boot conf

If a CEC-controlled TV renegotiates EDID on each wake and sometimes lands on
59.94Hz/1080i, pin it: `es.resolution=1920x1080.60.00`. This **must** go in
`/userdata/system/batocera.conf`, not `/boot/batocera-boot.conf` (the boot
conf's lower section is auto-synced from batocera.conf on boot and a direct edit
gets blanked). Confirm in `display.log` after a reboot.

## Bezels

Bezels/overlays are PNGs with a transparent "cutout" where the game shows,
plus a `.info` sidecar describing the viewport. Packs live under
`/userdata/decorations/<pack>/`, with per-game art at
`.../games/<system>/<rom>.png` (+ `.png.info`).

### `.info` coordinates are artistic intent, NOT the alpha cutout

The single biggest bezel trap. When a game renders misaligned inside the cutout,
the fix is the `.info` sidecar's `top`/`left`/`bottom`/`right` — but **`top` is
not the PNG's transparent-pixel offset.** It's where the artist intends the
game's viewport edge to sit, often *above* the alpha cutout because the top
bezel artwork is semi-transparent and the game is meant to extend behind it.

Do **not** derive `.info top` from the alpha bounding box (autodetecting the
transparent region and using that as `top` moves the game the wrong way).
Instead: launch, screenshot, and nudge `top` in ~20px steps (smaller = game
moves up, larger = down). Back up the `.info` before each iteration. See
[references/bezels.md](references/bezels.md).

### Generating missing `.info` sidecars

Some packs (notably thebezelproject) ship thousands of PNGs **without** `.info`
files. Without a sidecar, configgen guesses a viewport heuristically and often
gets it wrong (undersized, top-anchored game). [scripts/generate_tbp_info.py](scripts/generate_tbp_info.py)
alpha-detects each PNG's cutout and writes a correct `.info`, never overwriting
an existing one. This is the correct use of alpha detection — sizing a *missing*
sidecar — as opposed to the misalignment fix above, which is artistic and
eyeballed.

### Filtering unusable bezels

Some bezels have a cutout so small the game is postage-stamped. [scripts/filter_small_bezels.py](scripts/filter_small_bezels.py)
moves any bezel whose cutout's shorter dimension is below a threshold into a
`filtered_too_small/` sidecar dir, so Batocera falls back to the pack default.
Fully reversible (`mv filtered_too_small/* .`).

### SNES (and similar) fallback strategy

When a pack has per-game art for only a fraction of a large library (e.g. ~50 of
~760 SNES ROMs) and everything else falls back to an ugly generic system bezel,
invert the default: set the system to a clean shader-frame look (a Koko-AIO
ambilight preset, `<system>.bezel=none`) and write **per-game overrides** only
for the ROMs that *do* have real art. [scripts/snes-bezel-fallback.py](scripts/snes-bezel-fallback.py)
is a ready-to-adapt implementation (idempotent, generates a marker block,
backs up `batocera.conf`).

### Make your own fallback bezel

`<pack>/default.png` + `default.info` is the bezel every game without its own
art gets, so one good file improves a lot of games. You can build one from any
frontal picture of a monitor surround (a photo, a render, an image-model
output) as long as the screen area is one flat chroma green.
[scripts/make_bezel_from_green.py](scripts/make_bezel_from_green.py) scales the
green area onto the viewport from the existing `.info` and cuts it to alpha, so
the `.info` stays unchanged. [scripts/bezel_preview.py](scripts/bezel_preview.py)
mocks the result over a game screenshot and prints how many pixels each corner
hides. Keep the old `default.png` as a backup, then launch a game and
screenshot it. The prompt rules and the corner trap are in
[references/bezels.md](references/bezels.md).

### Seasonal fallback bezel

Because the fallback is one file, it is also the cheapest place for a seasonal
look: string lights in December, and the normal bezel back in January.
[scripts/bezel_season.sh](scripts/bezel_season.sh) reads a season name from a
state file and copies that season's files over the live ones. A season with no
folder gets the default folder, so the normal bezel returns without a second
script. Call it at boot and from a boot-service timer loop (see
`batocera-maintenance`; there is no cron). The same script swaps the boot
splash and one seasonal collection tile; see
[Seasonal boot splash](#seasonal-boot-splash) below.

Build the seasonal variant from the finished normal bezel: draw the decoration
on top, then reuse the normal bezel's alpha channel, so the opening and the
`.info` do not change. Do not send art that contains green (holly, green
bulbs) through the chroma-key script. It cuts those pixels out with the screen.

Two rules for image-model prompts came from a cobweb and blood-spatter variant:

- Name each thing you do not want. "Dry cobwebs" still gave thick wet strands
  until the prompt also said no drips, no runs and no hanging clumps.
- Attach a reference picture for a texture that words describe badly. One
  photo of spatter fixed in one pass what three prompt rewrites did not.

Four more came from a string-lights variant and a change of panel texture:

- For a string of lights, ask for exactly one cord, drawn as one continuous
  visible line from one image edge to the other. Then forbid by name a cord
  that passes behind a panel, branches, crosses itself or has loose ends.
  Without that the model draws cords that go everywhere and vanish.
- Avoid perforated or dotted panel textures. Clusters of small holes trigger
  trypophobia in some people. Avoid basket weave for the same reason: its dark
  gaps read as a grid of holes.
- For cloth, name the weave (for example diagonal twill) and say "stretched
  flat and tight". Without those words the cloth comes out as wrinkled vinyl.
- When an approved texture moves to another variant, attach the approved
  picture as the texture reference. Do not describe it again in words.

Change one element per pass and tell the model to keep the rest unchanged.
To preview a season that is months away, copy its files over the live ones,
launch a game, take a screenshot, then run the season script to put the
current season back. Compare a checksum of the live file with the season file
to confirm the restore.

### Seasonal boot splash

At boot Batocera plays a random `.mp4` from `/userdata/splash/`. Keep one file
there, and the choice is yours. Do not replace the normal clip with new art.
Keep it and add seasonal layers on top: snow, a string of lights, cobwebs.

- **Use the screen blend.** Draw each layer as bright art on pure black. The
  ffmpeg `screen` blend adds nothing where a layer is black, so a layer needs
  no alpha channel, and a plain `.mp4` or `.png` works.
- **Never put `eq=brightness` on a layer.** It lifts black to grey, and the
  blend then puts a grey haze on the whole picture. Make the source art
  brighter instead.
- **Fade the layers in when the logo lands**, not at the first frame, so the
  intro stays clean. Fade them out before the clip ends.
- **Mix a quiet sound under the original audio** with `amix normalize=0`. The
  default `normalize=1` halves the original track.

[scripts/make_splash_layers.py](scripts/make_splash_layers.py) renders falling
snow and two sounds (sleigh bells, thunder).
[scripts/make_season_splash.sh](scripts/make_season_splash.sh) puts any number
of layers on the normal clip:

```bash
python3 make_splash_layers.py layers --seconds 9
SOUND=layers/bells.wav FADE_IN=2.0 \
  sh make_season_splash.sh splash.mp4 splash-winter.mp4 layers/snow.mp4 lights.png
```

Play the result on the workstation first. Then put it at
`splash/<season>/splash.mp4` in the season folder, and put the normal clip at
`splash/default/splash.mp4`. `bezel_season.sh` copies the right one to
`/userdata/splash/splash.mp4`.

Verify with a real reboot, because nothing else plays the splash:

```bash
SSHB "md5sum /userdata/splash/splash.mp4 /userdata/system/season-bezel/splash/*/splash.mp4"
SSHB "ls -l /userdata/system/logs/mpv.log; grep -i 'splash' /userdata/system/logs/mpv.log | tail -5"
```

The live file must have the checksum of the current season's file, and
`mpv.log` must be newer than the reboot and name the file the boot player
opened.

**Seasonal collection tile.** `bezel_season.sh` can also add one custom
collection to the ES menu for one season (`COLLECTION=<name>
COLLECTION_SEASON=<season>`) and remove it afterwards. The trap: ES writes
`es_settings.cfg` when it exits cleanly, so an edit made while ES runs is lost
on the next clean exit. The script edits `CollectionSystemsCustom`, then sends
SIGKILL to the ES binary so the save handler never runs (it matches the
process by its exact command name, because the ES arguments change between
starts). It skips the pass while a game runs, because the kill would end that
game. The collection needs theme art or
its tile looks broken: see `batocera-ops` →
[emulationstation reference](../batocera-ops/references/emulationstation.md).
Verify with `grep CollectionSystemsCustom` on `es_settings.cfg` and one
screenshot of the menu.

**Seasonal screensaver.** The video screensaver can play one folder instead
of the game videos. Two settings in `es_settings.cfg` control it:
`SlideshowScreenSaverCustomVideoSource` (`true` or `false`) and
`SlideshowScreenSaverVideoDir` (the folder). If `grep` does not find both lines
in the file, set a custom video folder once in the ES screensaver menu; the
script changes a line and never adds one. Then keep one folder per
season and fill it with **hard links** to videos you already have:

```bash
SSHB 'mkdir -p /userdata/system/season-bezel/screensaver/winter'
SSHB 'ln "/userdata/roms/<system>/videos/<clip>.mp4" /userdata/system/season-bezel/screensaver/winter/'
```

A hard link is a second name for the same data. It uses no extra space, and it
keeps working when the file in the source folder is renamed, moved or removed
by a scraper run; a symlink would break. Both names must be on the same
filesystem, which is true for everything under `/userdata`. `bezel_season.sh`
switches the two settings: in a season that has a non-empty
`screensaver/<season>/` folder the screensaver plays only that folder, and in
every other season it plays the normal source again.

The script changes ES settings the safe way, and the pattern is worth copying
for any script that runs on a timer: **edit a copy, compare, then act.** It
copies `es_settings.cfg` to `/tmp`, applies every edit to the copy, and
compares the copy with the live file. Only when they differ does it replace
the file and restart ES. A pass that finds nothing to do writes nothing and
restarts nothing, so a 12-hour timer never interrupts the menu. Verify:

```bash
SSHB 'stat -c "%h %n" /userdata/system/season-bezel/screensaver/winter/* | head -3'   # link count 2
SSHB 'grep -E "SlideshowScreenSaver(CustomVideoSource|VideoDir)" /userdata/system/configs/emulationstation/es_settings.cfg'
SSHB 'sh /userdata/system/season-bezel/bezel_season.sh; tail -1 /userdata/system/season-bezel/season.log'
```

The second run of the script must add no log line. To see the result without
waiting for the idle timer, take three screenshots a minute apart once the
screensaver runs and match the frames to files in the season folder.

**A custom screensaver folder shows no bezel.** With
`SlideshowScreenSaverCustomVideoSource=true`, ES plays files that belong to no
game, and it draws decorations only for a game. To keep a bezel, burn it into
each clip: scale the clip into the bezel opening with
`force_original_aspect_ratio=decrease`, pad to the screen size, and overlay the
bezel PNG (or a looping RGBA `.mov` for animated lights) with ffmpeg. For a
lightning effect, copy real timing: 2 to 4 strobes about 100 ms apart (real
return strokes are about 60 ms apart; 30 fps cannot show that), each a
one-frame jump to peak with a fast decay, then a slower glow of about 0.4 s,
irregular gaps of several seconds, and a dim, cool bezel between strikes. A
pulse on one spot reads as a candle, not lightning. Keep full-area flashes
under 3 per second (photosensitivity guidance). Put
`scale=trunc(iw*sar/2)*2:ih,setsar=1` first, or clips with non-square pixels
(many arcade captures) come out stretched. Encode H.264 with `+faststart` and no
audio. ES re-reads the folder on every pick, so new files need no restart. When
you copy from a Mac with `tar`, macOS adds `._<name>` files; move them out of
the folder, because ES can pick them. Then a hard link no longer works for that
folder: every new clip has to go through the same burn step, so wrap it in one
intake script.

**Game-video screensaver bezel.** With game videos and
`ScreenSaverDecorations=systems` (the default), ES uses `global.bezel` only if
the set name starts with `default`. For any other set it draws the set named
`default`, which is the stock Batocera bezel. ES lists `/userdata/decorations`
before the stock sets, so a user folder `/userdata/decorations/default/` with
your own `default.png` and `default.info` replaces it. Set
`ScreenSaverDecorations=none` if you want no bezel at all. To check it, set a short `ScreenSaverTime` and take screenshots over
SSH. On v44, `batocera-screenshot` needs `export DISPLAY=:0
XAUTHORITY=/var/lib/.Xauthority` first, or x11grab fails with "Authorization
required" and no file is written.

### Standalone emulators ignore the `.info` viewport

Libretro cores place the picture from the `.info`. Most standalone emulators do
not: the launcher draws the bezel as an overlay and assumes a 4:3 picture at
full screen height (1440x1080 on a 1080p display). A bezel with a smaller
opening then covers the picture edges, and a non-4:3 emulator ratio makes it
worse. Fix it per system: set the emulator's own aspect option to 4:3 and give
that system a bezel whose opening is the 4:3 box.
[scripts/reslice_bezel.py](scripts/reslice_bezel.py) converts an existing bezel
to the new opening without stretching the side art.

### Don't attempt per-game Mega-Bezel cabinet art

Combining Mega-Bezel's photoreal CRT with per-game cabinet-art bezels is a known
dead end on Batocera (stale bezel symlink returns `bezel: None`, rotation isn't
propagated to the shader, and per-game cutout variance can't be bracketed by one
global scale offset). The full postmortem — including the false-positive that
fools you into thinking it works after one ROM — is in
[references/bezels.md](references/bezels.md). Read it before spending a day on
this; the short version is *don't*.
