---
name: photo-cull
description: Pick the good photos out of a folder of camera RAW files (Sony .ARW and other RAW formats). Generates previews, scores every frame for sharpness and exposure, groups burst near-duplicates, then visually reviews the top candidates and assembles a selects/ folder. Use when asked to cull, sort, pick keepers, or find the best shots from a RAW photo shoot.
disable-model-invocation: true
---

# photo-cull

First-pass culling of a RAW photo shoot. Combines **objective metrics**
(sharpness, exposure — computed by a script) with **subjective judgment**
(composition, expression, eyes open/closed — done by you, via vision) to pick
the keepers, without ever touching the original RAW files.

## When to use

The user wants to find/pick/cull/sort the "good" photos from a folder of RAW
files (e.g. a `*_<date>` shoot folder full of `.ARW` files).

## Prerequisites (already present on this machine)

- `sips` — built-in macOS CLI, reads Sony `.ARW` and other RAW formats natively.
- Python 3 with `cv2`, `numpy`, `Pillow`.
- No `exiftool`/`dcraw`/`darktable` needed — the workflow avoids them.

There is **no dedicated photo-culling MCP server** available; this skill is the
intended path.

## Hard rules

1. **Never modify or delete original RAW files.** Read only.
2. Culling means **selecting**, not deleting rejects. Winners are copied (or
   symlinked) into `selects/`.
3. Confirm with the user before any bulk copy/move/delete.

## Workflow

### 1. Run the scoring script

```bash
python3 ~/.claude/skills/photo-cull/cull.py <shoot_folder>
```

This:
- extracts a downscaled JPEG of every RAW into `<shoot_folder>/_previews/`
  (skips ones already generated — safe to re-run; add `--skip-previews` to reuse
  existing previews),
- computes per-frame **sharpness** (center-weighted Laplacian variance) and
  **exposure** (mean brightness, shadow/highlight clipping %),
- groups consecutive frames into **bursts** by **capture-time gaps** (a pause of
  >8s starts a new scene; falls back to sequence numbers if timestamps are
  missing),
- writes `<shoot_folder>/metrics.csv` and prints a summary: total frames,
  burst count, flagged frames (blurry / over- / under-exposed / clipped), and a
  **shortlist** = the sharpest clean frame in each burst.

Useful flags: `--max-dim 1024` (preview size), `--workers N` (parallelism).

> Big shoots (hundreds of RAWs, ~tens of GB) take a few minutes to generate
> previews the first time. Tell the user it's running; it parallelizes across
> cores. Consider running it in the background for very large folders.

### 2. Read the summary, then visually review the shortlist

The script's shortlist is a *mechanical* pick (sharpest unflagged frame per
burst). It cannot judge composition, expression, eye contact, or which of two
equally-sharp frames is better. **You do that** by viewing the previews.

**Use contact sheets to review efficiently** — reviewing hundreds of previews
with individual Read calls burns context. Generate labeled thumbnail grids
instead:

```bash
python3 ~/.claude/skills/photo-cull/contact_sheet.py <shoot_folder>          # shortlist
python3 ~/.claude/skills/photo-cull/contact_sheet.py <shoot_folder> --all    # all clean frames
# Review a dense burst's alternatives (note: zsh needs ${=var} to word-split a list):
files=$(awk -F, '$2==33{printf "%s ", $1}' <shoot_folder>/metrics.csv)
python3 ~/.claude/skills/photo-cull/contact_sheet.py <shoot_folder> --files ${=files}
```

Sheets land in `<shoot_folder>/_contact_sheets/`; Read those. For dense "hero"
bursts (a long portrait/posing run), the shortlist shows only ONE frame — sheet
that burst's full frame list to pick the best expression/pose.

Then, drilling in:

- Use the **Read** tool on `_previews/<name>.jpg` for any frame that needs a
  closer look than the contact sheet allows.

### 2b. MANDATORY: verify every finalist at full preview resolution

Contact-sheet thumbnails and the sharpness/exposure metrics are a *filter*, not
a verdict. Before anything lands in `selects/`, **Read each finalist's full
`_previews/` JPEG** and confirm with your own eyes. Metrics and thumbnails have
demonstrably let these through:

- **Closed / squinting eyes** — invisible at thumbnail size, fatal for a portrait
  (especially shooting into the sun). Check every face.
- **Sharpness ≠ good photo** — a sharp shot of *playground netting* or a fence
  outscores a soft portrait. A high `sharpness` number can mean "busy texture,"
  not "great image." Confirm the *subject* is what's sharp.
- **Mislabeled content** — "lone figure on beach" that is actually an empty
  seascape; an "establishing portrait" that is a cityscape. Verify what's in the
  frame before writing it into a scene group or the IG list.
- **Awkward in-between frames** — head down, mid-blink, fiddling with clothing —
  that scored fine on exposure but aren't real poses.
- **Near-duplicates** — three almost-identical frames; keep the single best.

If a finalist fails, pull the burst's alternatives (contact_sheet `--files`) and
swap in a frame that passes. Originals are copies into `selects/`, so revising is
cheap — but get it right before telling the user it's done.
- For each burst, confirm or override the script's pick based on: subject in
  focus, eyes open, good expression, framing/composition, no distracting
  clipping. Within a burst the frames are near-identical, so compare and keep
  the single best (occasionally two if genuinely different).
- Reconsider "blurry"-flagged frames only if the blur is intentional (motion,
  bokeh) — otherwise trust the flag.

Batch your `Read` calls (view several previews per turn) to move quickly.

### 3. Propose the selects, get confirmation

Present a concise list: chosen file per burst + one-line reason, and note any
bursts you dropped entirely (all blurry/eyes-closed/etc.). Ask the user to
confirm or adjust before copying anything.

### 4. Assemble `selects/`

After confirmation, copy the chosen **originals** (not previews) into
`<shoot_folder>/selects/`:

```bash
mkdir -p <shoot_folder>/selects
cp <shoot_folder>/DSC07818.ARW <shoot_folder>/selects/
```

Use `cp` (copies, originals stay put). Use `ln -s` instead only if the user
prefers symlinks to save disk.

**Group the selects by scene.** Put each keeper into a numbered scene subfolder
that follows the shoot's chronology, e.g.:

```
selects/01_establishing/  02_beach_portraits/  03_golden_hour/
        04_sunset_yoga/   05_morning_beach/
```

**Call out the Instagram-worthy shots.** Add `selects/instagram/` containing
**ranked symlinks** (`01_<file>`, `02_<file>`, …) to the ~6–10 strongest frames
in posting order — no extra disk, and the rank prefix sorts them. Favor: a
single clear subject, golden-hour/silhouette light, clean composition/negative
space, and a strong "vibe." Explain the ranking in the report.

Write a short `cull-report.md` in the shoot folder summarizing counts, the
scene groups, the keep/drop decisions, and the Instagram ranking.

## Metric reference

| Metric              | Meaning                                  | Flagged when |
|---------------------|------------------------------------------|--------------|
| `sharpness`         | center-weighted Laplacian variance       | `< 60` (blurry) |
| `mean`              | average brightness 0–255                 | `<50` dark / `>205` bright |
| `shadow_clip_pct`   | % pixels crushed to black                | `>10%` |
| `highlight_clip_pct`| % pixels blown to white                  | `>10%` |
| `burst`             | near-duplicate group id (by seq number)  | — |

Thresholds are tuned for 1024px previews and live at the top of `cull.py`.
They're starting points — if a particular shoot (e.g. deliberately dark/moody,
or lots of intentional motion blur) trips too many false flags, say so and
adjust the constants rather than blindly trusting the flags.

## Notes

- `_previews/` and `metrics.csv` are derived/disposable — regenerable any time.
- The script is non-destructive: it only reads RAWs and writes into `_previews/`
  and `metrics.csv`.
- See the workspace `AGENTS.md` for folder conventions.
