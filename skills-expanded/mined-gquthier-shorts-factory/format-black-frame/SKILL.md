---
name: format-black-frame
description: Render or adapt the Black frame short-video format in Shorts Factory. Horizontal footage inside a vertical black canvas. Use for screen recordings, slides or a wide shot whose content must remain legible.
---

# Black frame

Work inside the Shorts Factory checkout. Read [the renderer contract](../../templates/README.md) and [the implementation](../../templates/black-frame/template.mjs) before changing layout or timing. Shared identity lives in [brand.mjs](../../templates/brand.mjs).

Preserve the full screen recording instead of zooming into a small webcam. Keep the fixed hook above the 1080×608 footage region at y=656. Position captions within the video without covering the useful interface.

Use the creator’s own media, profile and verified transcript. All template input comes from `TemplateCtx`; do not hardcode a person, path, sample hook or timing. Template spec times are TAKE seconds; overlay intervals are FINAL seconds after cuts. Preserve this distinction.

After changing the format, run `node --no-warnings --test test/templates.test.ts`, render a short fixture with `tools/render-smoke.ts`, and inspect opening, middle and final frames at delivery resolution. Check face/mouth clearance, caption timing, clipping and mobile safe zones. Hook quality and render quality are separate checks. Rendering does not authorize publication.
