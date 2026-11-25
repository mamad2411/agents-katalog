---
name: 3d-brain-animations
description: >-
  Render 3D still images and rotating turntable animations of brain regions from ANY BrainGlobe
  atlas (mouse, rat, human, zebrafish, etc.), with optional glow/bloom highlighting and a
  semi-transparent whole-brain shell for context. Use this WHENEVER the user wants to visualize,
  render, picture, or animate brain anatomy: any species, any region (hippocampus, CA1, dentate
  gyrus, cortex, thalamus, amygdala, ...), any color, a glowing/highlighted region, a rotating
  brain video, or a neuroanatomy figure for a paper/thesis/slide — even if they don't mention
  Blender or BrainGlobe. Handles requests like "rotating animation of the rat hippocampus CA1
  glowing purple while the rest of the brain is semi-transparent". The skill installs anything
  missing and renders via bundled scripts, so do NOT write Blender/bpy code or probe the API.
---

# 3D Brain Animations

Turns a natural-language request into a 3D brain figure or animation. All logic is in bundled
scripts; a render is two bash calls plus a small JSON spec. **Never write `bpy`/Blender code or
introspect the API — translate the request into a spec and call the scripts.** (macOS; Blender
installed. First use installs deps + the add-on and downloads the atlas, a few minutes; later
runs are instant.)

`scripts/run.sh` auto-locates the installed Blender. Use absolute paths to this skill.

## Translate the request, then run two commands

From the user's words, fill in a spec:

- **Species → atlas** (pass to `setup` and put in the spec as `atlas`):
  | says | atlas |
  |---|---|
  | mouse | `allen_mouse_25um` (small/fast test: `allen_mouse_100um`) |
  | rat | `whs_sd_rat_39um` |
  | human | `allen_human_500um` |
  | zebrafish | `mpin_zfish_1um` |
  | other / unsure | run `bash scripts/run.sh find <guess_atlas> <kw>`, or ask |

  If the user names a species without an atlas, use the standard one above and say which you chose.
- **Region(s)** are given by **atlas-specific acronym**. If the user uses plain words ("hippocampus",
  "dentate gyrus") or you're unsure of the acronym for *this* atlas, resolve it first:
  `bash scripts/run.sh find <atlas> <keyword>` → prints `acronym <tab> name`. (E.g. CA1 is `CA1`
  in Allen mouse but the rat atlas also has `DG`, `SUB`, etc.) After rendering, confirm each region
  appears in `RESULT`'s `loaded` list; if one was skipped, the acronym was wrong — `find` it.
- **"rest of the brain semi-transparent" / "whole brain" / "in context"** → `"envelope": "auto"`
  (resolves the whole-brain shell for any atlas automatically). Omit `envelope` for no shell.
- **Color words → RGB** (0–1): purple `[0.5,0.05,1]`, blue `[0.05,0.25,1]`, green `[0.18,0.82,0.4]`,
  red `[0.93,0.2,0.24]`, orange `[0.99,0.52,0.13]`, yellow `[1,0.85,0.1]`, cyan/teal `[0.1,0.74,0.84]`,
  pink `[0.99,0.38,0.72]`. "glowing"/"highlight"/"lit up" → `"glow": true`.
- **"rotating"/"animation"/"video"/"turntable"** → `"mode": "anim"`. "full rotation" → one rotation
  (`rotations_per_phase: 1`). Multiple regions appearing one-by-one → `reveal: "sequential_solo"`
  (each alone) or `"sequential_cumulative"` (each adds on). Everything lit the whole time → `"all"`.

Then:
```bash
bash scripts/run.sh setup <atlas>          # idempotent; ends in READY
bash scripts/run.sh render /tmp/spec.json  # prints RESULT {...output...}
```
Stills → `<output>.png`; animations → `<output>.mp4` (frames also in `/tmp/bb_frames/`).
**Animations render many frames (minutes) — run the render command in the background.**
To show the result: Read the `.png`; for an `.mp4`, Read a couple of `/tmp/bb_frames/f_*.png`
to verify and give the user the `.mp4` path.

## Spec schema

Required: `atlas`, `regions`, `output`. Everything else defaults sensibly (dark background,
auto-framed camera, 3-light setup, EEVEE). Colors are `[r,g,b]` 0–1.

```jsonc
{
  "mode": "still",                 // "still" (default) | "anim"
  "atlas": "whs_sd_rat_39um",
  "output": "/Users/<you>/Desktop/figure",   // .png/.mp4 appended automatically
  "envelope": "auto",              // "auto" = whole-brain shell | a specific acronym | omit for none
  "envelope_alpha": 0.10,          // lower = more transparent
  "regions": [
    {"acronym": "CA1", "color": [0.5,0.05,1.0], "glow": true}   // color/glow/alpha optional
  ],
  "glow": {"emission":1.3,"strength":0.8,"size":0.32,"threshold":0.7,"saturation":1.2}, // optional
  "resolution": [1600,1100],       // anim default 1280x720
  "samples": 32,
  "view_dir": [0.5,-1.0,0.32],
  "background": [0.02,0.022,0.03],
  "anim": {                        // only when mode=="anim"
    "fps": 30, "deg_per_frame": 1.5,         // smaller = slower spin
    "reveal": "sequential_solo",             // sequential_solo | sequential_cumulative | all
    "rotations_per_phase": 1, "final_together_rotations": 1, "fade_frames": 20
  }
}
```

## Examples (request → spec)

**"Rotating animation, full rotation of the rat hippocampus CA1 glowing purple, rest of the brain
semi-transparent"** (`find whs_sd_rat_39um CA1` confirms acronym `CA1`):
```json
{"mode":"anim","atlas":"whs_sd_rat_39um","output":"/Users/me/Desktop/ca1_spin",
 "envelope":"auto",
 "regions":[{"acronym":"CA1","color":[0.5,0.05,1.0],"glow":true}],
 "anim":{"reveal":"all","rotations_per_phase":1,"deg_per_frame":1.5}}
```
Same request for **human** → just `"atlas":"allen_human_500um"` (and `setup allen_human_500um`);
for **mouse** → `"atlas":"allen_mouse_25um"`. The acronym may differ per atlas, so `find` it.

**Two regions revealed one at a time, then together (animation):**
```json
{"mode":"anim","atlas":"whs_sd_rat_39um","output":"/Users/me/Desktop/hippo",
 "envelope":"auto",
 "regions":[{"acronym":"CA1","color":[0.05,0.25,1.0],"glow":true},
            {"acronym":"DG","color":[0.50,0.05,1.0],"glow":true}],
 "anim":{"reveal":"sequential_solo","rotations_per_phase":1,"final_together_rotations":1}}
```

**Still figure, several solid-colored regions in a glass brain:**
```json
{"atlas":"allen_mouse_25um","output":"/Users/me/Desktop/mouse_fig","envelope":"auto",
 "regions":[{"acronym":"HPF","color":[0.16,0.42,0.98]},{"acronym":"TH","color":[0.99,0.52,0.13]}]}
```

## Notes

- Glow **more**: raise `glow.emission` (~1.3→1.6) and `glow.strength` (~0.8→1.0); keep `emission`
  under ~1.8 or colors wash to white.
- `setup` printing `NOT_READY`: read its `STATUS` — the atlas may be mid-download or the add-on
  install needs network.
- A region missing from `RESULT.loaded` means a wrong/mesh-less acronym; use `find` to fix it.
- The Blender MCP "connector" (live GUI) is optional; this skill runs Blender headless, which is
  reliable and cheap. If a live MCP Blender is connected you may open the produced `.blend`/frames
  there instead, but headless is the default.
