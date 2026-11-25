---
name: video-sharingan
description: Reverse-engineer the audiovisual production of a reference video (motion design, product launch, changelog, app promo, trailer) into measured numbers and a recreation brief. Use this when the user shares a video and says "make ours like this", "copy this style/camera/pacing", "what camera moves does this use", "how fast is the camera", "recreate this launch video", or before generating a video with Hyperframes, /brag, Remotion or After Effects from a reference. Measures cuts and shot durations, camera language (truck/pedestal/pan/push-in/pull-out/orbit, speed in px/s and %W/s, scale %/s, easing, whether the camera ever stops), framing, depth of field and rack focus, grain/vignette/bloom/chromatic aberration, UI micro-animation vs camera pacing, and audio (music vs SFX, tempo, cuts on beat). Ignores theme, palette and branding. Outputs analysis.json, brief.md with do/don't rules, and QC gates to compare a render against the reference.
---

# video-sharingan: copy the technique, not the pixels

Turn a reference video into **numbers** and a **recreation brief** a generator can follow. Eyeballing a
video lies about speed, easing and whether the camera ever stops, so measure first, then write the brief.

```
probe → cuts → contact sheets → camera per shot → focus/look → audio → brief → (render) → compare
```

Everything below is one command, `scripts/sharingan.py analyze` (or `./sharingan analyze`). The steps are listed
so you know what each number means, can re-run a single stage, and can **check the numbers with your own eyes**.

## Setup (once)

```bash
command -v ffmpeg ffprobe python3          # ffmpeg is required
python3 -m pip install -r requirements.txt  # numpy + opencv-python-headless (+ pytest)
```

If the reference is a URL, download it first (`yt-dlp -o ref.mp4 <url>`, or `curl` for a direct mp4). If it
can't be downloaded, ask the user for a screen recording. Never commit reference media anywhere: it's
usually copyrighted.

## 1. Run the full pipeline

```bash
python3 scripts/sharingan.py analyze ref.mp4 -o sharingan-ref --title "Reference name"
```

Writes:
- `sharingan-ref/analysis.json`: every measurement (schema in the README)
- `sharingan-ref/brief.md`: the recreation brief with do/don't rules and QC gates
- `sharingan-ref/sheets/overview.png`, `shots.png`: contact sheets (**read them**)
- `sharingan-ref/focus/focus_shotNN.png`: sharpness heatmaps (red = sharp)
- `sharingan-ref/parts/*.json`: per-stage outputs

Runtime is about 1–2 s per second of 1080p video on a laptop.

## 2. Verify, stage by stage (do not skip)

Numbers are only as good as the shot list. Work through these in order:

1. **Probe** (`analysis.source`): fps, size, duration. Note `vfr_suspect`. VFR screen recordings make
   px/s unreliable, so re-encode CFR first: `ffmpeg -i in.mp4 -vf fps=30 -c:v libx264 -crf 16 cfr.mp4`.
2. **Cuts** (`analysis.edit`): open `sheets/overview.png` and `sheets/shots.png`. Every row in `shots.png`
   must be ONE continuous shot.
   - Missed cut or false cut? Re-run with manual cuts: `analyze ref.mp4 --cuts 3.5,7.25,…` (seconds).
   - Detection already rejects UI reflows (lists collapsing, modals) by checking camera-trajectory continuity.
   - Dissolves and whips are not auto-detected: look for ghosted frames on the sheet.
3. **Camera** (`analysis.camera.shots[]`): for each shot, read `move`, `center_speed_px_s_1080p`,
   `speed_pctW_s`, `scale_pct_s`, `ease.best`, `never_stops`, `enters_moving`/`exits_moving`, `pull_out`.
   - Velocities are **content motion**. The camera moves the opposite way (content sliding left = truck right).
   - Compare speeds across references at **1080p-equivalent** or **%W/s**, never raw px.
   - `pull_out.reflow_suspect_at_s` lists windows where the UI re-laid out. Check those frames by eye
     before you call it a pull-out.
   - Doubt a number? Cross-check with the independent tracker:
     `python3 scripts/camera_track.py ref.mp4 --shots sharingan-ref/parts/shots.json --method orb`.
     LK and ORB should agree within about 5 %.
   - Cut mid-move? Then a shot may be a *slice* of a longer eased move. Read `ease.speed_thirds_rel`.
4. **Focus & framing** (`analysis.focus`): `dof` (deep / shallow-band / shallow-spot / soft-overall), band
   orientation, `rack_focus_suspected`, `framing` (macro / medium / wide). Open the heatmaps.
5. **Look** (`analysis.look`): grain σ, vignette falloff, bloom, chromatic aberration, grade. These are
   heuristics. Compression eats grain, and dark UI edges can fake a vignette. Confirm on a full-res frame:
   `ffmpeg -ss 5 -i ref.mp4 -frames:v 1 frame.png`.
6. **Audio** (`analysis.audio`): `class` (music / music+sfx / sfx-only / silent), `tempo_bpm`,
   `cuts.verdict` (cut on the beat or not, against the chance rate), `ui_events.synced_fraction`
   (SFX landing on UI changes). Listen once to confirm the class.

For deeper dives, every stage also runs alone: `sharingan probe|cuts|sheet|camera|focus|look|audio …`.

## 3. Write the brief

`brief.md` is generated from the measurements. Edit it with what only a human or an LLM can see, using
`templates/brief.md` as the canonical format:

- Keep the **distilled spec** paragraph at the top paste-able on its own (Hyperframes style).
- Every rule is an **absolute, testable target**: "push-in +1.2 %/s", never "zoom a bit more".
- Add what the tool can't measure: staging (UI on a tilted 3D plane? device frame?), what the UI does in each
  shot, the story beat of each shot, typing or cursor behaviour.
- **Ignore the theme.** Dark mode, palette, fonts and brand don't belong in the brief. The user's product keeps its own.
- Log intentional differences in **Deviations** (e.g. "reference pulls out in shot 4; we never pull out").
- See `examples/linear-style-changelog/brief.md` for a finished, real-world brief.

## 4. Hand it to a generator

- **Hyperframes / `/brag`:** paste the distilled spec plus sections 2–10 into the composition prompt. Camera
  tweens use `ease: "none"` when the brief says linear, and push-ins become a scale tween at the measured %/s.
- **Remotion:** translate px/s into `interpolate(frame, [0, durationInFrames], [x0, x0 + v * dur])` with
  `Easing.linear`, and scale as `Math.pow(1 + rate/100, t)`.
- **After Effects / Motion / anything else:** the shot table is the edit decision list.

## 5. Self-check: compare your render against the reference

```bash
python3 scripts/sharingan.py analyze render.mp4 -o render-analysis
python3 scripts/sharingan.py compare sharingan-ref/analysis.json render-analysis/analysis.json
```

`compare` prints a gate table (speed window, never-stops, no pull-out, linear easing, shot durations,
cut-while-moving, audio class, cut/beat sync) and **exits 1 on any hard failure**. Fix one axis at a time
with absolute values, re-render and re-compare. Before you call it done, also watch the render once and read its contact sheet.

## Rules of thumb

- Measure before you describe. If a number contradicts your impression, trust the number but look at the
  frames to understand why.
- One reference rarely has a single speed. Report the window (min–max) and the median, and pick a target
  inside it.
- Shot list first, everything else second: a wrong cut poisons every per-shot number.
- This skill copies **grammar** (camera, optics, edit, sound), never assets. Don't ship 1:1 clones of
  someone else's brand.

## Files

- `scripts/sharingan.py`: CLI entrypoint (`analyze`, `compare`, and per-stage commands)
- `scripts/{probe,cuts,contact_sheet,camera_track,focus_map,look,audio,brief,compare}.py`: the stages, each runnable alone
- `templates/brief.md`: brief format
- `references/camera-language.md`: definitions, thresholds, and production traps
- `examples/synthetic/`: generator plus ground truth for the self-test (`pytest tests/`)
- `examples/linear-style-changelog/brief.md`: worked example with real measured numbers
