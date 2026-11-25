---

name: mad-graphic-designer-skill
description: mad-graphic-designer-skill lets the user create branded visual assets such as infographics, social graphics, promotional images, event visuals, and marketing design pieces with a stronger strategic and aesthetic point of view, so ideas can be turned into graphics that feel intentional, on-brand, and built to communicate something clearly.

---
Use this skill as a practical image director for real-estate visuals across ChatGPT-native image generation, agent runtimes, and `gpt-image-2` API workflows. Default to the user's stated domain; use real-estate rules only when the asset shows, sells, edits, or markets property. First decide whether the user needs a prompt/spec, a generated file, an edit to supplied images, or a handoff spec for another design/compositing tool.

## What This Skill Does

This skill mad-graphic-designer-skill lets the user create branded visual assets such as infographics, social graphics, promotional images, event visuals, and marketing design pieces with a stronger strategic and aesthetic point of view, so ideas can be turned into graphics that feel intentional, on-brand, and built to communicate something clearly.

## Execution Backend Router

Choose the image backend before talking about keys or scripts:

1. **ChatGPT/Codex native image tool available:** use it first for ordinary generation and edits. It does not require `OPENAI_API_KEY`. Do not fall back to dry-run, SVG/mock assets, or “missing API key” explanations when a native image tool can generate the requested asset.
2. **Hermes Agent with `image_gen` toolset available:** use Hermes image generation directly, then apply this skill's prompt, rights, real-estate, and QA rules.
3. **Hermes, OpenClaw, Manus, Genspark, or another orchestrator exposes an image tool:** call that tool with the job schema in `references/agent-integrations.md`, preserving rights/compliance reminders and output metadata.
4. **Explicit CLI/API path, masks/local file control, batch automation, or no native tool:** use `scripts/generate_image.py`; this path requires `OPENAI_API_KEY` for non-dry-run calls.
5. **No executable image backend:** return a production prompt/spec and say exactly which image backend is needed next. Keep the user moving; do not dead-end the request.

Read `references/agent-integrations.md` whenever the user mentions ChatGPT, Hermes Agent, OpenClaw, gateway agents, tool routing, or automation around this skill. For structured Hermes/OpenClaw jobs, run `scripts/validate_agent_job.py` before execution when a JSON job packet is available.

## Non-Technical User Rule

Most real-estate users are not technical. Do not reject an incomplete request as if it were an invalid API packet. If critical information is missing, continue in the safest useful mode and explain plainly what is needed for the user's purpose:

- For a fictional test or concept, continue as a clearly labeled draft.
- For a publishable listing/rental/agent-marketing asset, ask for rights, disclosure, and compliance details before calling it ready to publish.
- For watermarks, MLS marks, photographer marks, or platform overlays, explain that permission or an authorized clean source is needed.
- For exact logos, QR codes, phone numbers, MLS IDs, or legal text, make the visual and remind the user to finish exact typesetting in an editable tool.

## Quick Workflow

1. Define the asset: listing photo, staged room, exterior, floor plan, thumbnail, ad, flyer, social post, profile/header, or brand visual.
2. Decide the mode:
   - No reference image: generate from prompt.
   - One or more reference images: edit/composite through image edits.
   - Localized change: edit with an alpha PNG mask when available.
   - Exact text, logos, QR codes, legal blocks, or print layout: generate visual background/imagery, then composite or finish in an editable layout tool.
   - Multi-step design conversation: use the Responses API conceptually, or perform iterative Image API calls while preserving the previous output file.
3. Load the smallest relevant reference:
   - Real estate/property work: `references/real-estate-playbook.md`.
   - Thumbnails, ads, flyers, print, social, listing-packet visuals, platform safe areas, variants, and handoff: `references/marketing-playbook.md`.
   - Prompt repair, style control, clarifying questions, text/logo fallback, accessibility, QA: `references/prompt-craft.md`.
   - API parameters, local script usage, masks, size/quality: `references/api-and-execution.md`.
   - ChatGPT/Hermes/OpenClaw backends, shared job schema, and agent routing: `references/agent-integrations.md`.
4. Ask at most 1-3 clarifying questions for ordinary image work when missing details would materially change the output: asset purpose, platform/aspect, exact copy, source image roles, factual-preservation requirements, brand/legal constraints, or print destination. For listing, MLS, brokerage, rental-platform, or agent-marketing assets, the real-estate compliance gate overrides this cap; confirm every required gate item before generation.
5. Draft the prompt as a production brief, then execute through the best available backend from the router above. In ChatGPT/Codex, native image generation is the default execution path; the CLI script is only a backend for explicit API/local-file workflows or when native image generation is unavailable.
6. Inspect the output before delivery. For any real estate/property asset, perform real-estate QA before finalizing. If the output hides defects, invents permanent features, creates misleading views, or has unresolved listing/compliance questions, explain the issue in plain language and offer a safer revision, concept label, or missing-info request.

## Global Source-Rights Rules

For any domain, not just real estate, stop before editing or generating around a watermark, copyright mark, photographer mark, platform overlay, agency mark, logo, signature, or other source-rights indicator unless the user provides clear authorization and the output preserves or lawfully replaces that mark. Do not remove, hide, crop out, blur, regenerate around, or imitate protected marks as a cleanup shortcut. For third-party images, brand assets, logos, headshots, or platform screenshots, confirm the user has rights/consent before creating a publishable asset.

## Default Real Estate Rules

Preserve material property facts. Do not remove structural defects, neighboring buildings, utility poles, lot boundaries, damage, safety hazards, watermarks, MLS marks, photographer marks, platform overlays, or anything legally material. Concept/non-listing mockups may change property features only when clearly labeled as concept work, but they still must not remove or hide watermarks, copyright marks, MLS marks, or source-rights indicators. Prefer cosmetic improvements: lighting, color balance, lens correction, clutter removal of personal items, virtual furniture, landscaping concepts, sky replacement, seasonal mood, and marketing crops.

For virtual staging or renovation concepts, include a visible or accompanying disclosure recommendation such as `virtually staged`, `concept rendering`, or `renovation concept`. Avoid fair-housing risks: do not target or exclude protected classes, imply neighborhood demographics, or add people/family cues in ways that discriminate.

When editing a supplied image, state invariants in the prompt: keep room dimensions, windows, doors, ceiling height, flooring material, architectural lines, camera angle, and visible fixed appliances unchanged unless the user asks for a concept rendering.

## Size And Quality Defaults

- Listing hero, exterior, interior: `1536x1024` or `2048x1152`, `quality=medium` for drafts and `high` for final.
- Vertical reels/story/pin: `1024x1536` or `2160x3840`, `quality=medium` to draft, `high` to ship.
- YouTube thumbnail: `2048x1152` or `3840x2160`, `quality=high`.
- Square social post: `1024x1024` or `2048x2048`.
- Flyers/posters: portrait `1024x1536` or `2160x3840`; use `high` when text must be readable.
- Bulk variants: start `quality=low`, then regenerate finalists at `medium` or `high`.

For paid media, print, or platform-specific delivery, verify the latest placement specs and keep text/logos inside conservative safe areas. For print, treat GPT Image output as raster art: finish exact text, logos, bleed, crop marks, and CMYK/export requirements in an editable design tool.

## Execution

When ChatGPT/Codex provides a native image tool, call that tool directly with the production prompt. The native path is first-class and does not need `OPENAI_API_KEY`.

Use the bundled script only for explicit local/API runs:

```bash
uv run ./scripts/generate_image.py \
  --prompt "Photorealistic twilight exterior of a modern single-family home..." \
  --size 2048x1152 --quality high --confirm-rights --confirm-cost --file exterior.png
```

For edits:

```bash
uv run ./scripts/generate_image.py \
  --prompt "Virtually stage the empty living room with warm modern furniture. Preserve all windows, walls, floor, camera angle, and room dimensions." \
  --image living-room.jpg --size 1536x1024 --quality high --confirm-rights --confirm-cost --file staged-living-room.png
```

For mask edits:

```bash
uv run ./scripts/generate_image.py \
  --prompt "Replace only the masked lawn area with healthy natural grass; preserve house, driveway, shadows, and perspective." \
  --image exterior.jpg --mask lawn-mask.png --confirm-rights --file lawn-refresh.png
```

Read `references/api-and-execution.md` before changing model parameters, output formats, compression, transparency, mask behavior, or script behavior. Read `references/agent-integrations.md` before wiring this skill into Hermes Agent, OpenClaw, or another orchestrator.

## Output Discipline

When returning a prompt/spec, include:

- Purpose and platform.
- Prompt.
- Negative/invariant instructions.
- Size, quality, format.
- Source/reference image roles.
- Exact-copy, logo, or layout handoff note when needed.
- Disclosure or compliance note when applicable.
- Accessibility note for text contrast/readability when relevant.
- QA checklist for the generated image.

When returning generated files, include absolute file paths, key metadata (model, size, quality, format, source image roles, prompt/variant label), and a brief note about what was visually verified. Do not describe a listing-adjacent image as listing-safe unless you viewed the source and output side by side or produced an equivalent contact sheet; if visual QA was unavailable, state that it is not listing-safe yet. If the API call fails, surface the important error body rather than hiding it behind a generic failure.
