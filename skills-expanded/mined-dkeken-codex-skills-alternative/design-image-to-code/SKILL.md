---
name: design-image-to-code
description: Turn a reference image or mockup into a working local frontend that matches it closely. Inspects the image, extracts the design system (layout, type, spacing, color, components), implements it, then screenshot-compares and iterates to close the gap. Use when the user says "image to code", "build this mockup", "code this screenshot", "make this design real", or provides a UI image to implement. Part of the Product Design set. Uses a browser tool for screenshot verification.
---

# Design — Image To Code

Reproduce a reference image as a real, runnable frontend — verified by screenshot diff, not "looks roughly like it". The discipline that separates this from generic codegen: you *measure* the result against the reference and iterate until the gap is minor and explainable.

## When to use
- You have a mockup/screenshot (from a designer, `design-ideate`, or generated) to implement.
- "Build this design", "code this screenshot", "make this real".
- Recreating a UI you can see but don't have code for.

## When NOT to use
- The source is a *live site* (you can hit its URL/HTML) → `design-url-to-code` (it can extract real CSS).
- No image yet, just an idea → `design-ideate`.
- You need interactivity/flow wiring, not a static match → `design-prototype` (run this first to build screens).

## Inputs
- The **reference image(s)** (path).
- **Target stack**: ask; default to matching the repo, else React + Vite + Tailwind + TS.
- `./design/context.md` constraints if present.

## Workflow
1. **Inspect** the image with a vision/read tool. Inventory every meaningful element. Extract the design system: layout grid, type scale, spacing rhythm, palette, components, radii, shadows.
2. **Reuse before inventing**: if adapting an existing project, read its components/tokens/fonts first and use them.
3. **First pass**: build to match the **primary viewport** as closely as possible. Don't chase responsive yet.
4. **Capture**: run the app, screenshot at the reference's exact dimensions via a browser-automation tool.
5. **Compare & list mismatches** in priority order: layout → type → spacing → color → icons.
6. **Iterate** until differences are minor and explainable. *Then* handle responsive (tablet/mobile).
7. **Missing assets**: use supplied files; generate raster assets with an image tool; or use clearly-marked placeholders + a note.

## Worked example
```
reference: ./mocks/pricing.png  (1440px wide)
stack: matches repo → Next.js + Tailwind + Aurora DS
pass 1: built 3-tier pricing grid, header, CTA
capture: screenshot @1440 → ./design/checks/pricing-impl.png
mismatches:
 - [layout] cards 3-col but gap too tight (16 vs ~32 in ref)
 - [type] tier price 32px, ref ~40px
 - [color] "popular" badge wrong accent (#7C3 vs ref #16A34A)
 - [spacing] section pad 48 vs ref ~80
iterate: fix gap=32, price=40px, badge=#16A34A, section pad=80
re-capture: gap now minor (sub-pixel font rendering only) → DONE
responsive: collapse to 1-col < 768px, stack CTA
verify: build clean, typecheck clean, runs at :3000
```

## Quality bar / Definition of done
- Implementation screenshot ≈ reference at the target viewport; remaining diffs are minor and *explained*.
- Existing design-system components/tokens reused, not duplicated.
- Build + typecheck clean; runs locally with one command.
- Responsive handled after the reference-size match is solid.

## Common pitfalls
- **Claiming parity without comparing** — always capture + diff. "Looks close" isn't verification.
- **"Improving" the design** — match the reference unless explicitly asked to deviate; note any forced deviations (e.g. for a11y).
- **Inventing new tokens** when the project already has a scale — creates drift.
- **Chasing responsive too early** — nail the reference viewport first, or you iterate on a moving target.
- **Eyeballing spacing/type** — measure against the reference; "looks like 16" is often 24.

## Handoff
Static screens done → `design-prototype` (wire interactivity/flow) → `design-qa` (conformance) → `design-share`.

## Tooling
Needs a **vision/read tool** (inspect the image) and a **browser-automation tool** (screenshot the build for comparison). Optional image tool for missing assets. Without a browser tool you can still build, but flag that visual parity is unverified.
