---
name: code-generated-video
description: "Use when a short teaser is asked for in the ff-tracking style: every pixel and sound from code."
version: 1.1.0
author: coordinator role of hermes-fleet-apps
license: MIT
---

# Code-generated teasers (ff-tracking template on fframes)

The ff-tracking look: a virtual camera films a terminal while a tracker locks onto the
glyphs; every pixel and every sound comes from code. It makes short teasers for a
project. Source: `github.com/mrsarac/ff-tracking` (MIT, Copyright (c) 2026 Mustafa
Saraç), built on fframes (MIT). Keep a local clone in the media work folder
(`<work folder>/ff-tracking`), with no remote of your own. Jobs arrive as a brief
from the coordinator naming the teaser and its texts; the media role renders,
verifies and hands back paths.

**This template is its own style source.** Palette, font (JetBrains Mono, OFL) and
camera look are fixed inside the template, so a teaser needs no `tokens.json`: a
"no tokens.json = stop" rule does not apply here. Change only the texts, the shot
count and the timing. A new palette or a project's brand colours = a designer
decision: stop and ask.

Read the upstream README and `docs/WINDOWS.md` (on Windows) once before the first build.

## Always-on rules

- **Readability before style.** Upstream cuts every 0.5 s (`SCENE_FRAMES = 15` at
  30 fps), which is too fast to read the words. Default to >= 1 s per shot
  (`SCENE_FRAMES = 30`) and scale the typing/lock frames with it (`TYPE_END`,
  `LOCK_AT`, the collapse divisor). Never shorten shots back for "energy" without asking.
- **Slower shots alone do not make the words readable: say so up front.** The stock
  cameras zoom 2.5-3x and the lock box hatches over the last word, so the full line is
  never in frame. For a readable cut, lower the `cam()` zoom pair so the whole hero line
  fits, and make the hatched boxes lighter; offer this as a "clear" variant that
  changes the style, rather than presenting a slowed render as the readability fix.
- **Keystrokes must be audible.** Upstream's per-key click is faint. If the owner wants
  a real keyboard sound, layer it in `tools/sfx.py`: bright switch click + low "thock"
  + quiet release click, randomised per key, around -3 dB. Keep it synthesised, never
  a downloaded sample.
- **No real names or real personal data on screen.** Teaser texts are made up but
  plausible (counts, file names). Never show real people's names, and do not name
  third-party sites or brands the project works with.
- **Everything inside the project folder.** A shared FFmpeg build and libclang (what
  `docs/WINDOWS.md` requires) live once in a shared toolchain folder next to the
  clone; never download a second copy. Python lives in `.venv/` (listed in
  `.git/info/exclude`). A uv cache, if needed, goes in a scratch dir and is deleted
  right after use.

## Procedure

1. **Setup once:** a small wrapper (e.g. `tools/teaser.ps1` or `.sh`) points
   `FFMPEG_DIR` and `LIBCLANG_PATH` at the shared toolchain, uses `.venv/` for
   numpy+scipy and unsets `PYTHONPATH`/`PYTHONHOME`, then calls upstream's render
   script. A fresh `.venv` needs only `uv venv .venv` + `uv pip install --python
   <.venv python> numpy scipy`.
2. **One file per teaser** (a local change, not upstream): move `TITLE`, `SCENE_LIST`
   (12 shots) and `LOG` out of `hud/src/lib.rs` into `teasers/<name>.rs` and load it
   with `include!(concat!(env!("CARGO_MANIFEST_DIR"), "/../teasers/", env!("TEASER"), ".rs"))`;
   the default name sits in `.cargo/config.toml [env]`, and the env var overrides it.
   Cargo tracks `env!`, so switching teaser triggers a rebuild.
   - Keep the last two shots as `Collapse` and `Done`: their animation is tied to them.
   - Insert new shots before those two.
3. **Check the fit before rendering:** `TEASER=<name> cargo test -q -p hud`.
   The test `hero_lines_fit_the_canvas` catches lines that leave the screen.
   Typing-shot text should stay around <= 20 characters at the default sizes; shorten
   the text rather than the font.
4. **Render** through the wrapper; it produces `out/<name>.mp4`.
   - Run it in the background with notify.
   - The first build takes several minutes; after that, roughly 2-3 min per 6 s of
     video on a recent desktop GPU.
   - Render several teasers one after the other in one background loop.
5. **Verify by looking:** build a contact sheet from frame `LOCK_AT - 1` of each shot,
   where typing is finished and the lock box does not yet cover the last word. The
   first frame shows only ~35 % of the line, and a frame after the lock hides the last
   word, so both make a correct line look broken.
   `ffmpeg -i out/x.mp4 -vf "select='eq(mod(n\,F)\,K)',scale=480:-1,tile=4x3" -frames:v 1 sheet.jpg`
   with F = `SCENE_FRAMES` and K = `LOCK_AT - 1`. Read every line with vision. Also run
   `ffprobe` for duration, frame count and the audio stream. The keyboard sound is not
   checked by any of this: say it was not listened to.
6. **Deliver over a chat bot:** the 1080p render is ~10 MB per second of video, so
   anything over ~5 s is past a 50 MB bot upload limit (Telegram's, for example).
   Re-encode a copy with x264 at `bitrate ~ 45 MB x 8000 / seconds - 200` kb/s
   (12 s -> ~26 Mb/s -> ~37 MB) with `-movflags +faststart`, keep the original in
   `out/`, and offer to delete the copies once the owner has them.
7. **Clean:** delete the build logs, contact sheets, `out/pass/` and `out/tracks.json`.
   Keep `target/` (~1.8 GB, it makes the next render fast) and `.venv/`, and say why.

## Pitfalls

- **Do not render while another process holds the GPU by default.** A process that
  already uses the GPU can hold most of the VRAM and many GB of RAM. Make
  the wrapper refuse to start while one runs, with a `-Force` override.
  - Check the process list yourself when the owner says "go": the other process may
    still be running when they think it is not. Report it and let them choose: stop
    it, or force.
  - If forced, run each render with `-Force` plus a free-RAM watchdog in the same
    background loop: poll free RAM every 5 s, stop the render (`lens`/`flat`) below
    ~1.5 GB, and log the lowest value. That protects the other process from an
    out-of-memory kill.
  - To stop a running loop, `process_manage kill` the background session first: it
    takes the child render down with it, while killing only `lens.exe` lets the loop
    start the next teaser.
- **Pass PowerShell one-liners in SINGLE quotes from bash.** In double quotes, bash
  expands `$_` and `$o` before PowerShell sees them, and the command fails to parse.
- Upstream's `tools/render.ps1` always writes `out/tracking.mp4`; the wrapper must
  rename it per teaser, otherwise each render overwrites the previous one.
- The fixed 16:9 canvas (`W`, `H`) is wired through the camera and the tests. A vertical
  reel (1080x1920) is a real port, not a constant change; say so before promising one.
- Length = `SCENES x SCENE_FRAMES / FPS`. Upstream warns that long Windows renders can
  exhaust memory, because each encoder worker decodes the 4K first pass. Test anything
  past ~30 s before promising it.
