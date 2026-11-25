---
name: filmcraft-editing
description: How to edit video well with the filmcraft MCP tools (FilmCraft, the open-source Premiere-style editor) — live editing in the app, framing portrait footage, effects and keyframes, fades, transitions, renders and checking your own work. Use this whenever you are about to create, cut, grade, frame or render anything through the filmcraft tools (connect_app, create_project, add_clip, fit_clip, set_effect_param, render...), even for a quick one-off edit, and whenever the user wants to "see the edit in the app" or watch it happen live.
---

# Editing with FilmCraft through the filmcraft MCP tools

FilmCraft runs the same engine headless (`filmcraft-cli`) and in its desktop app. The MCP tools wrap
both. These notes are what makes the difference between an edit that technically exists and one
the user is happy with; most of them were learned the hard way on real projects.

## Work live when the user wants to watch

If the user wants to see the edit (or says "in the app", "real time", "show me"), call
`connect_app` first. It opens a **new** FilmCraft window in control mode — any window they already
have open is left alone — and from then on every tool without a `project` edits that window, so
each clip, effect and title appears as you make it. Create the project with `create_project`
(it opens in the app), and call `save_project` when done; live edits are not on disk until then.

Editing a project file headless while the same file is open in the app makes them fight (the app
won't reload it, and saving from the app overwrites your edits). Connected tools route around this
automatically when given the open project's path.

For long builds (dozens of shots), a plan file and `recap-edit`'s `build_from_plan.py --live` is far
faster than hundreds of individual tool calls; connect afterwards with `connect_app(port, token)`.

## Times, ids, tracks

- Tool times are seconds. Raw engine commands (`run_command`) use ticks: 254016000000 per second, or
  `{"seconds": n}` / `{"frame": n}` where accepted. Plan cuts in **frames** (`round(s * fps)`) so
  shots land exactly on beats and don't drift.
- `add_clip` returns `[video clip, audio clip]` ids; `list_timeline` shows ids, times and each clip's
  added effects. Item ids come from `import_media`.
- Put clips with `audio: false` when the soundtrack is music, so clip sound doesn't fight it.
- Layering: V1 main shots; higher tracks for overlays, flashes, an adjustment layer for the overall
  grade, then titles/captions on top. Create the sequence with enough video tracks up front.

## Framing: fit_clip, never hand-calculated scale

Most phone footage is portrait; most edits are landscape (or the reverse). `fit_clip` with
`mode: "fill"` covers the frame and shows only a slice of the source — for 9:16 into 16:9 that is
**about a third of the height**. Choose that slice with `focusY` (0 top … 1 bottom) by looking at the
footage: people in a portrait clip usually need `focusY` 0.3–0.45 to keep heads in; a horizon or
waterfall may need 0.6. Check with `export_frames`/`render_frame` — cut-off heads are the most common
complaint. `zoom` punches in (keep it modest: over-zoomed shots look soft and "too close"), `focusX`
recentres a subject, and the tool clamps so a filled frame never shows an edge. When a portrait
clip can't be framed well at landscape fill (a selfie becomes a giant face), show it whole and smaller
instead — e.g. as a picture-in-picture overlay — rather than forcing it full-frame.

## Effects, keyframes, fades, transitions

- `apply_effect(clips, effect, params)` then `set_effect_param` for anything else. Effect ids:
  `lumetri` (exposure, contrast, highlights, shadows, whites, blacks, temperature, tint, saturation,
  vibrance, sharpen, curve_red/green/blue `[[x,y]…]`, vignette_amount), `vr_denoise` (amount),
  `gaussian_blur`, `drop_shadow`, `noise`, `track_matte`. Intrinsic: `motion` (scale, position,
  rotation, uniform_scale, scale_width), `opacity` (opacity, blend: "Screen", "Multiply"...).
  See `references/effects.md` for transitions and less common effects.
- Keyframes: `set_effect_param(..., time, keyframe: true)` at timeline seconds.
- Fade out the last shot (and any caption over it) with `fade`, not Dip to Black: at the very end of a
  sequence Dip to Black can hard-cut, which viewers read as a freeze or a dropped frame.
- `add_transition` takes `params` (e.g. light_leak `{"color": [1, 0.5, 0.15, 1], "amount": 100}`).
  Built-ins are soft washes; reel-style light leaks with streaks need a custom overlay
  (recap-edit's `light_leak.py`, blend Screen).
- Order matters: denoise before colour correction (contrast amplifies noise you then can't remove).

## Image sequences: bake them

A PNG sequence written by a script (titles, overlays) should be imported with
`import_media(paths=[first frame], imageSequence: true, bake: true)`. Re-writing the frames of an
already-imported sequence can leave the app showing stale (static) frames; a baked ProRes movie with a
fresh name can't be stale.

## Quality

- Low light: denoise only the shots that need it (`vr_denoise` 40–50) and grade them gently
  (no contrast boost; pull blacks down instead). Heavy denoise or median filters make the whole video
  look soft — users notice blur faster than grain.
- 24 fps clips in a 30 fps sequence judder: `set_speed(speed 100, interpolation "frameBlending")`.
- Render with `render(maxRenderQuality: true, bitrateMbps: 30–40)` for 1080p delivery; `quality`
  does not change H.264 size, `bitrateMbps` does.

## Check your own work before reporting

Look at frames (`export_frames(every: 1)`), and run `check-render` on the output: it catches frozen
stretches, hard cuts to black, intros that don't animate and low bitrate. Say plainly what you checked
and what you didn't (e.g. you can't hear the audio).
