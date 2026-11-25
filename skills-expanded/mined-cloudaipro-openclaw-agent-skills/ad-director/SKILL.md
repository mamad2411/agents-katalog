---
name: ad-director
description: Advertising creative direction for brand and product campaigns that produces campaign concepts, visual language, shot lists, and production-ready prompt packs. Use when users request commercials, ad storyboards, conversion creative, launch campaigns, or CTA-focused marketing videos and images. Do not use for long-form narrative filmmaking.
---

# Ad Director

## Objective
Generate conversion-oriented ad creative plans that connect strategy, visual language, and prompt-ready execution.

## Trigger Rules
Use when the request includes campaign or commercial intent.

Positive cues:
- Brand launch video, product commercial, promo reel.
- Ad storyboard, hook-first short, CTA script.
- Performance creative for paid social channels.
- Visual direction for ad concepts across tools.

Do not use when:
- The user wants long-form narrative film treatment.
- The main task is audience research only.
- The task is pure editing automation without creative direction.

## Inputs
Required:
- Brand or product name.
- Campaign objective.
- Target audience.

Optional:
- Channel and duration constraints.
- Tone and style references.
- Existing assets and legal boundaries.

## Output Schema
Return the universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Campaign brief.
2. Shot list table.
3. Prompt pack for image/video generation.
4. Production checklist.

## Workflow
1. Extract objective, audience, and offer.
2. Define single-minded message and CTA.
3. Select visual direction and pacing.
4. Build 6-8 shot progression with hook-to-CTA flow.
5. Compile model-ready prompts with consistent style constraints.
6. Validate internal consistency and channel fit.
7. Return assumptions, risks, and next actions.

## Quality Bar
- Keep value proposition explicit in first third.
- Keep visual style coherent across all shots.
- Keep CTA concrete and measurable.
- Flag missing strategic inputs explicitly.

## Safety Rules
- Refuse deceptive, illegal, or harmful advertising requests.
- Avoid fabricated claims or unverifiable statistics.
- Mark assumptions where user context is missing.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Creative artifact validator: `scripts/validate_creative_artifacts.py`
