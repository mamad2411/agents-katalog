---
name: format-typo-depth
description: Render or adapt the Type depth short-video format in Shorts Factory. Large opening words behind the speaker, then stacked emphasis typography. Use for a camera clip with a short, clearly timed opening.
---

# Type depth

Work inside the Shorts Factory checkout. Read [the renderer contract](../../templates/README.md) and [the implementation](../../templates/typo-depth/template.mjs) before changing layout or timing. Shared identity lives in [brand.mjs](../../templates/brand.mjs).

Use actual opening words, capped at 9 words and 3.8 seconds. Head masking requires usable person segmentation; screen recordings fall back to a compatible format. Special moments are separated by 5.5 seconds. Keep the included runtime bigColor patch and two sound assets; do not replace words or add claims for an effect.

Use the creator’s own media, profile and verified transcript. All template input comes from `TemplateCtx`; do not hardcode a person, path, sample hook or timing. Template spec times are TAKE seconds; overlay intervals are FINAL seconds after cuts. Preserve this distinction.

After changing the format, run `node --no-warnings --test test/templates.test.ts`, render a short fixture with `tools/render-smoke.ts`, and inspect opening, middle and final frames at delivery resolution. Check face/mouth clearance, caption timing, clipping and mobile safe zones. Hook quality and render quality are separate checks. Rendering does not authorize publication.
