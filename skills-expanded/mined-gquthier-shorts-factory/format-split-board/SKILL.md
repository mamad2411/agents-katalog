---
name: format-split-board
description: Render or adapt the Split board short-video format in Shorts Factory. A dark explanatory stage above a camera card. Use for a demonstration, process, tool or a concrete number that benefits from a visual beat.
---

# Split board

Work inside the Shorts Factory checkout. Read [the renderer contract](../../templates/README.md) and [the implementation](../../templates/split-board/template.mjs) before changing layout or timing. Shared identity lives in [brand.mjs](../../templates/brand.mjs).

Keep the seam at y=1000, place explanatory beats in the upper stage, and retain the speaker below. Safe zones: top 220 px, bottom 420 px, right 140 px. Use ctx.beats and timestamps from the spoken words; never invent a statistic for decoration.

Use the creator’s own media, profile and verified transcript. All template input comes from `TemplateCtx`; do not hardcode a person, path, sample hook or timing. Template spec times are TAKE seconds; overlay intervals are FINAL seconds after cuts. Preserve this distinction.

After changing the format, run `node --no-warnings --test test/templates.test.ts`, render a short fixture with `tools/render-smoke.ts`, and inspect opening, middle and final frames at delivery resolution. Check face/mouth clearance, caption timing, clipping and mobile safe zones. Hook quality and render quality are separate checks. Rendering does not authorize publication.
