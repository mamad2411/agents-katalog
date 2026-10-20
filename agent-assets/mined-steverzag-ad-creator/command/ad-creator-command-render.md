---
description: Export an ad to PNG/MP4 in out/ — no edits, no judgement
argument-hint: [ad slug, optionally a format, e.g. "elevia-seguro-resbalon 9x16"]
---

Export an ad. **Nothing else.** Don't edit the ad, don't critique it, don't fix
what you notice — `/adjust` and `/critique` own that.

Target: **$ARGUMENTS** — if empty, use the ad this conversation has been working
on, or the only folder in `ads/`. Ask if it's ambiguous.

## 1. Recompile the brand if the render says it's stale

`pnpm render` does **not** recompile `brand.css` — an export doesn't mutate
source. It does check, and prints this when the compiled CSS no longer matches
the brand JSON:

```
⚠ brand.css is stale — brands/<brand>.json has changed since it compiled
  this export will use the old tokens — fix: pnpm brand ads/<slug> <brand>
```

**Don't ignore that line.** The render still succeeds, with the old colours and
fonts, which is the most common way an export comes out wrong for no visible
reason. Recompile and render again.

## 2. Export

```bash
pnpm render ads/<slug>                  # every format in ad.config.json
pnpm render ads/<slug> --format 9x16    # one
pnpm render --all                       # every ad
```

The renderer refuses a format that isn't in `ad.config.json` — it will tell you
which ones the ad has. Adding one is a config change, so that's `/adjust`, not
something to do silently here.

Motion costs ~3.5–4 frames/second: a 20s ad at 30fps is 600 frames, about 2.5
minutes. **That's expected — don't kill a render that looks stalled.**

## 3. If it fails or comes out wrong

Hand to the **`render-ad`** skill; it owns diagnosis. The usual causes:

| Symptom | Cause |
|---|---|
| Frozen frame where motion should be | Animation not on the paused timeline, or a `<video>` not registered with `ctx.video()` |
| Blank or partial frame | `ready` never resolved — a font or image that never loaded |
| Missing text | Font fell back and reflowed, or content is outside `.ad-safe` |
| Old colours or fonts | Stale `brand.css` — step 1 |
| Missing ffmpeg binary | `ffmpeg-static` postinstall blocked; see `pnpm-workspace.yaml` |

## 4. Report

List the files written and their formats, from `out/manifest.json`. Note the
render time for motion.

**State plainly that you have not looked at the output.** An exit code of 0 says
the encoder ran, not that the ad is right. Offer `/verify` next.
