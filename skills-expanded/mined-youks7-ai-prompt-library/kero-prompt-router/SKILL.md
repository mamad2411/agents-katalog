---
name: kero-prompt-router
description: Select and adapt KeRo AI Prompt Library prompts or multi-stage workflows for e-commerce, copywriting, TikTok, localization, AI image, AI video, storyboards, and automation tasks. Use when a user wants help finding, filling, or applying a reusable prompt from this library; do not use as a general replacement for direct task execution when no library asset is needed.
---

# KeRo Prompt Router

Route a production request to the smallest useful library asset, then adapt it to the user's real inputs.

## Route the request

1. Identify the requested output, platform, audience, language, available source material, and whether the work is a single-step prompt or a multi-stage production workflow.
2. Search `references/library-index.json` by title, category, tags, model, and summary. Prefer one strong match; offer alternatives only when they lead to materially different outcomes.
3. Use a regular prompt for a bounded deliverable. Use a workflow when the request requires analysis, direction selection, staged generation, iteration, or quality review.
4. After selecting an item from the metadata-only index, read exactly that matching file under `references/prompts/` or `references/workflows/`. Do not load every Prompt body at once.

Read `references/category-map.md` when the task spans categories or the correct route is unclear.

## Adapt the asset

- Treat user-provided product facts, images, copy, brand rules, and platform requirements as authoritative.
- Ask only for missing information that would materially change the result. Otherwise use explicit, reversible assumptions and label them.
- Replace placeholders with the user's real information. Do not leave unexplained variables in a final reusable prompt.
- Preserve factual constraints. Never invent prices, certifications, materials, dimensions, performance claims, platform policies, or customer evidence.
- For visual work, confirm structure, color, branding, quantity, surface finish, and material response. Explicitly surface requirements such as brushed metal, polished metal, matte plastic, transparent glass, fabric weave, wood grain, or soft-touch coating when they affect the image.
- When current platform rules or model capabilities matter, verify them from authoritative sources rather than treating repository examples as permanent rules.

## Deliver the result

Return:

1. the selected Prompt or Workflow name and why it fits;
2. any blocking inputs still needed;
3. a filled, copy-ready prompt or the next executable workflow stage;
4. a short verification checklist tailored to the requested output.

If no library asset is a good match, say so and create a task-specific prompt using the same factual and input discipline. Do not pretend that a weak match came from the library.
