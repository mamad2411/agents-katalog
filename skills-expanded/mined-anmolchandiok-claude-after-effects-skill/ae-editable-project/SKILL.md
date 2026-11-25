---
name: ae-editable-project
description: Turns a motion video that was made with code (HTML canvas, JS/Node or Python renders, SVG, any frame-by-frame renderer) into a native, fully editable After Effects project (.aep). The project has live text layers, shape layers, one precomp per object, a camera null with real keyframes, effects as toggleable layers, audio stems and narration markers. It's the AE equivalent of a layered PSD. Use this whenever the user wants an After Effects file, an .aep, "an editable version", "layers I can change", a project to hand to a motion designer or editor, or wants to tweak, retime or reuse a video that was rendered from code. Use it even if they only say "AE", "After Effects project", "make it editable" or "like a PSD but for video".
---

# Editable After Effects project from a code-made video

The goal is a project a motion designer can open and work in as if they had built it by hand. Text is real text, paths are shape layers, every object is a named precomp, and the camera is one null they can re-keyframe. The opposite is a rendered frame sequence dropped into a comp, which can't be edited, so never deliver that as the main animation.

The approach has three steps:
1. Export the scene from the **same data the renderer draws**.
2. Write it as `scene.json`.
3. Have After Effects build the project itself, by running a generated ExtendScript.

You never write a binary .aep by hand.

```
renderer data ──export──▶ scene.json + assets/ ──make_jsx.js──▶ build.jsx ──After Effects──▶ project.aep (+ check stills)
```

Bundled scripts (in `scripts/`):
- `aelib.jsx`: the builder that runs inside After Effects. It reads the scene and creates comps, layers, keys, masks, effects, mattes, markers and audio, then saves the .aep and a build log.
- `make_jsx.js`: `node make_jsx.js [--portable] scene.json build.jsx`. Checks the scene (missing assets, bad parents, precomp order) and writes one self-contained `build.jsx`. With `--portable`, paths are relative to `build.jsx`, so the folder can be zipped and run on another computer, including Windows. Use it for anything you deliver.
- `run_in_ae.sh`: `run_in_ae.sh build.jsx /abs/path/Project.aep [timeout]`. On macOS, runs the build in the installed After Effects, waits for it, and prints the log.

Read `references/scene-spec.md` before writing the exporter. It defines every field, easing, the checked effect match names and value ranges, and the gotchas that cost time.

## Workflow

### 1. Inventory what the video draws

Read the renderer and list everything that appears on screen and how it moves:
- The world or background.
- Each object or document.
- Each piece of text.
- The camera move.
- Moments timed to words or beats.
- The look: grain, glow, vignette, motion blur, fades.
- The audio.

For each item, note where its numbers come from (constants, geometry functions, timing files).

### 2. Map each element to its AE-native form

Choose the form a motion designer would build by hand:

| In the code | In After Effects |
|---|---|
| Camera move over a world (translate, scale, rotate) | One **CAMERA null**. Anchor Point = the point the camera looks at, in world coordinates. Scale = zoom. Rotation = roll. Position = comp centre. Parent every world layer to it. Then `screen = position + R·scale·(p − anchor)`, which is exactly a canvas camera transform, so the world layers keep the coordinates the code uses. |
| Handheld shake, impact jolts | An expression on the null's position and rotation, driven by **Slider Controls** named for what they do ("Handheld amount", "Impact strength") |
| An object or document (print, paper, card, book) | Its own **precomp** containing a border, photo, text, a contact shadow and a "Dim" solid. Author it at 2× and scale the layer to 50%. Turn **collapse** on. Animate the drop-in on the precomp layer. |
| Vector paths (coastlines, rules, circles, lines) | **Shape layers**, one group per logical piece, named |
| Text | **Text layers** with the real string and the PostScript font name. Never use pre-rendered text images. |
| Bitmaps the code generates (placeholder photos, paper textures) | Export them as PNG/JPG assets, name them so they're easy to swap ("PHOTO — replace me") |
| Writing that appears word by word on the narration | A text layer with `reveal: { times: [...] }`. The builder keys a Write-on mask per word (measured in AE), and the text stays editable. |
| A line drawing itself on | Trim Paths `end` keyed 0→100 |
| Stamp or slam | Scale/opacity keys plus an entry in the camera impacts list |
| Hero focus / dimming others | A black "Dim" solid with Preserve Transparency inside each precomp, plus a screen-space dim solid over the background, with opacity keys |
| Film look | Named adjustment layers ("LOOK — Soft glow", "LOOK — Film grain"), a vignette solid with a feathered inverted mask, a fade solid, and comp motion blur on world layers. Name them all so they're easy to switch off. |
| Audio | Separate stems (voice, music/fx) as audio layers, plus the narration lines as **comp markers** |

### 3. Export from the source of truth

Add an export path to the existing renderer instead of retyping numbers. For example, expose its internals (`module.exports`, an `--export` flag, or importing its modules) and write `export_ae.js` / `export_ae.py`. It should produce `scene.json` and an `assets/` folder. That way the AE project and the MP4 can't drift apart, and re-exporting after a story change is one command.

Getting the motion to match:
- **Camera and other curves.** Put keys at the meaningful moments (hold starts and ends, landings), not on every frame. Give each key the curve's true speed at that point with **33.333% influence**: that reproduces a cubic Hermite exactly. Where a move also does something mid-way (a pull-back zoom, log-space zoom), add keys at ¼, ½ and ¾ of the move with their own derivatives. Take derivatives numerically from the renderer's own camera function.
- **Signed speeds.** Rotation, scale and opacity speeds are signed. Spatial properties (position, anchor point) take magnitude only.
- **Per-frame keys** are only acceptable for genuinely irregular things, like a flicker. Everything else should be easy to grab and move.
- **Retiming.** Read timings from the same file the renderer uses (e.g. `timings.json`), so retiming the voiceover retimes the project.

Write for the human who opens it:
- Name every layer for what it is ("Ink circle (draws on 'Kestrel Point')", "Map dim (hero focus)").
- Put a one-line `comment` on anything non-obvious.
- Use labels to group, and give the camera null a distinct label.
- Narration lines go in as comp markers.

### 4. Build and check

```bash
node <skill>/scripts/make_jsx.js --portable --quiet scene.json build.jsx   # build.jsx sits next to assets/
<skill>/scripts/run_in_ae.sh build.jsx "/abs/path/My Project.aep" 1500
```

- **Prerequisite (one-time, in AE):** Settings → Scripting & Expressions → enable "Allow Scripts to Write Files and Access Network". Without it, saving and the build log fail. If the runner times out, this setting (or an open dialog in AE) is the usual cause; ask the user to check.
- **It won't discard work.** If the open AE project has unsaved changes, the build stops and says so in the log. Never work around this by discarding the user's project; ask them to save or close it. Use `--quiet` for automated builds so the message goes to the log, not a dialog that blocks AE. Regenerate without `--quiet` for the `build.jsx` you deliver, so a person running it by hand sees the message.
- **The build log** (`<Project>.build-log.txt`) lists every layer, effect or property that failed. Treat any issue as a bug in the scene and fix it at the exporter, not in AE.
- **Check stills.** Set `project.stills` to 5–8 telling times: a word-synced moment, mid-drop, a hero hold, the title. The builder renders them from the main comp. They render asynchronously after the save, and the runner waits for them. They're 16-bit PNGs that ffmpeg can't always read, so view them with `sips -s format jpeg -Z 1920 in.png --out out.jpg`.
- **Compare side by side** with frames from the original render at the same times. Check framing, which object is hero, whether text reveals land on the word, and colour and brightness. Then fix the exporter and rebuild. Glow in AE is much stronger than a canvas "screen of a blurred copy", so start with a high threshold (~200 of 255) and low intensity (~0.2).

If After Effects isn't on this machine, or the person who will edit is on another computer, don't try to launch it. Deliver the portable folder (`build.jsx`, `assets/`, `scene.json`, README). They run it with **File → Scripts → Run Script File…** and the .aep is saved next to `build.jsx`. The README must tell them to enable the scripting file-write setting first, and that fonts must be installed.

### 5. Deliver

Deliver one folder containing:
- `<Name>.aep`
- `assets/`
- `build.jsx` and `scene.json`, so the project can be rebuilt
- the exporter script
- a short `README.md` that says how to:
  - move the camera: keyframe the CAMERA null's Anchor Point (where it looks) and Scale (zoom)
  - swap a photo: in the Project panel, select the asset and use File → Replace Footage
  - retime a word: drag that layer's Write-on keys, or re-export after changing timings
  - toggle the look layers
  - change text: double-click it
  - which fonts must be installed

Tell the user plainly:
- what is matched exactly (layout, timing, keys)
- what is approximated (AE glow, grain and colour differ a little from canvas compositing)
- what you checked with stills and what you didn't (e.g. full-length playback)

## Things that have gone wrong before

These are the reasons behind the conventions above:
- **Shadows and blurs on shape or text layers don't scale with the camera**, because their effects apply after the transform. Use solids with masks for world-space glows and shadows.
- **Precomps go soft when the camera zooms in.** Fix with collapse transformations, and author at 2×.
- **Feathered masks get cut off at the solid's edge.** Make glow solids much bigger than the glow.
- **Fonts must be PostScript names.** Check unknown ones in AE with a quick probe: set `textDocument.font` and read it back.
- **ExtendScript is ES3, and it misreads chained ternaries** (`a ? b : c ? d : e`): use a lookup table or `if`/`else` instead. If you change `aelib.jsx`, test it on a tiny scene first (one text layer, one shape, one precomp) before the full build.
