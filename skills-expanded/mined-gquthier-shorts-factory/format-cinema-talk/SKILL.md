---
name: format-cinema-talk
description: Render or adapt the Cinema talk short-video format in Shorts Factory. Full-screen vertical talking head with restrained captions and timed punch-ins. Use when the speaker’s delivery carries the content.
---

# Cinema talk

Work inside the Shorts Factory checkout. Read [the renderer contract](../../templates/README.md) and [the implementation](../../templates/cinema-talk/template.mjs) before changing layout or timing. Shared identity lives in [brand.mjs](../../templates/brand.mjs).

Avoid forced widescreen-to-face cropping for slides. The renderer falls back to black-frame when the source is a screen recording. Keep punctuation/word timings from the transcript. Punch-ins should follow sentence boundaries, spaced at least 3.5 seconds apart.

Use the creator’s own media, profile and verified transcript. All template input comes from `TemplateCtx`; do not hardcode a person, path, sample hook or timing. Template spec times are TAKE seconds; overlay intervals are FINAL seconds after cuts. Preserve this distinction.

After changing the format, run `node --no-warnings --test test/templates.test.ts`, render a short fixture with `tools/render-smoke.ts`, and inspect opening, middle and final frames at delivery resolution. Check face/mouth clearance, caption timing, clipping and mobile safe zones. Hook quality and render quality are separate checks. Rendering does not authorize publication.
