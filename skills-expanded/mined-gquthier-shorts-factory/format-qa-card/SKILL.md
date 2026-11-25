---
name: format-qa-card
description: Render or adapt the Q&A card short-video format in Shorts Factory. A camera card with a question card and a headline. Use for Q&A, interviews and teaching extracts with a real question.
---

# Q&A card

Work inside the Shorts Factory checkout. Read [the renderer contract](../../templates/README.md) and [the implementation](../../templates/qa-card/template.mjs) before changing layout or timing. Shared identity lives in [brand.mjs](../../templates/brand.mjs).

ctx.question is optional; never invent the audience’s question. Reading time is 0.9 + 0.28 seconds per word, bounded to 2.2–4.2 seconds, followed by a short smaller state. Keep captions above the question card. Current overlays use discrete PNG states, not smooth animation.

Use the creator’s own media, profile and verified transcript. All template input comes from `TemplateCtx`; do not hardcode a person, path, sample hook or timing. Template spec times are TAKE seconds; overlay intervals are FINAL seconds after cuts. Preserve this distinction.

After changing the format, run `node --no-warnings --test test/templates.test.ts`, render a short fixture with `tools/render-smoke.ts`, and inspect opening, middle and final frames at delivery resolution. Check face/mouth clearance, caption timing, clipping and mobile safe zones. Hook quality and render quality are separate checks. Rendering does not authorize publication.
