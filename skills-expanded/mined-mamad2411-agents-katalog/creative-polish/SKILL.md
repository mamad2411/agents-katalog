---
name: creative-polish
description: Take a chosen visual to finished, production-ready state. Runs cleanup + refinement passes (fix artifacts, balance composition, color-grade, sharpen text, conform to spec/aspect) using image edit/regenerate. Use when the user says "polish this", "finalize", "clean up the image", "production-ready", "fix the artifacts", or has a selected visual that needs finishing. Final stage of the Creative Production set.
---

# Creative — Generative Polish

Turn a *selected* draft into a final, production-ready asset. This is the LAST stage — it only runs on an already-chosen visual. Polishing before a concept is locked wastes effort; this skill assumes the creative direction is settled and now it's about execution quality.

## When to use
- A concept has been chosen (from explore/scene/shot/ads/offer) and needs finishing.
- An image has fixable flaws: artifacts, bad hands/text, off composition, wrong aspect.
- Conforming a winner to final delivery specs (size, ratio, color).

## When NOT to use
- The concept isn't locked yet — polishing many candidates is wasteful; lock first.
- You need new concepts → the relevant explorer skill.
- The image is fundamentally wrong (bad composition at the core) — regenerate upstream instead of patching.

## Inputs (ask only what's missing)
- **The selected source image** (path or reference).
- **Target spec**: final aspect/size, where it'll be used, brand constraints.
- **What to improve** — specific issues, or run a full pass.

## Workflow
1. **Diagnose** the source. List concrete issues: artifacts, extra fingers/garbled text, composition imbalance, color cast, soft focus, wrong aspect, distracting background.
2. **Decide per issue**: **edit** (inpaint/region fix via an image-edit tool) when only a region is wrong — it keeps the rest stable; **regenerate** (re-prompt with stronger constraints + source as reference) when the issue is structural.
3. **Apply passes in order**: structural fixes → composition/crop → color grade → text legibility → final sharpen/export. Save iterations to `./creative/polish/<NN>.png` so you can roll back.
4. **Conform** to final aspect/size for the target medium.
5. **Show before/after** and confirm it meets spec.

## Worked example
Source: chosen hero from `creative-shot`, but has a duplicated keycap, blurry legend text, slightly cool cast, and is 1:1 but the hero slot needs 16:9.
```
issues: [duplicated keycap top-row] [legend text soft] [too cool ~-300K] [need 1792x1024]
passes:
 1. edit (inpaint): remove duplicate keycap, rebuild row — region fix, rest untouched
 2. regen-region: sharpen legend text, pass exact legends verbatim
 3. grade: warm +250K, lift shadows slightly
 4. crop/extend to 1792x1024 (outpaint left/right of product)
before: ./creative/shot/hero-34.png   after: ./creative/polish/hero-final.png
verify: keycaps correct, text crisp, neutral-warm, 1792x1024 ✓
```

## Quality bar
- No visible generation artifacts (hands, text, duplicated/merged elements).
- Exact visible text/wording preserved — never mutated during edits.
- Color and contrast are intentional and consistent with the brand/set.
- Delivered at the correct final aspect and resolution for its use.

## Common pitfalls
- **Text mutation** — regenerating a region silently changes wording. Always pass text verbatim and re-check.
- **Full-regen when an edit would do** — re-rolling the whole image loses everything that was already right. Prefer region edits.
- **Polishing unlocked concepts** — finishing 5 candidates nobody chose. Lock first.
- **No rollback** — overwriting the source. Save numbered iterations.

## Handoff
This is the terminal stage. Output the final asset(s) at spec. If the user wants the same treatment across a set, apply the same pass recipe to each and verify consistency.

## Tooling
Needs an image tool with **edit/inpaint + generate** support (ideally outpaint for aspect changes). If only generation (no edit) is available, prefer targeted regeneration with the source as reference; if no image tool at all, output the diagnosed issue list + the exact fix prompts.
