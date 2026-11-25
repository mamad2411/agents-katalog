---
name: format-selfie-headline
description: Render or adapt the Selfie headline short-video format in Shorts Factory. Full-screen vertical footage with a persistent sentence above the face. Use for an informal observation or a single strong point.
---

# Selfie headline

Work inside the Shorts Factory checkout. Read [the renderer contract](../../templates/README.md) and [the implementation](../../templates/selfie-headline/template.mjs) before changing layout or timing. Shared identity lives in [brand.mjs](../../templates/brand.mjs).

Use the dark top gradient and keep the title away from the face. Size to the actual hook length. Do not pack multiple ideas into the title. Keep caption treatment from the implementation; review long hooks at 1080×1920.

Use the creator’s own media, profile and verified transcript. All template input comes from `TemplateCtx`; do not hardcode a person, path, sample hook or timing. Template spec times are TAKE seconds; overlay intervals are FINAL seconds after cuts. Preserve this distinction.

After changing the format, run `node --no-warnings --test test/templates.test.ts`, render a short fixture with `tools/render-smoke.ts`, and inspect opening, middle and final frames at delivery resolution. Check face/mouth clearance, caption timing, clipping and mobile safe zones. Hook quality and render quality are separate checks. Rendering does not authorize publication.
