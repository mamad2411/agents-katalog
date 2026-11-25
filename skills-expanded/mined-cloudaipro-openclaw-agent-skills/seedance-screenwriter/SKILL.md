---
name: seedance-screenwriter
description: VMCA prompt compiler that translates scene descriptions into high-weight Traditional Chinese prompts optimized for video generation workflows using positive-only phrasing. Use when users ask for direct prompt-writing instead of full directing plans.
---

# Seedance Screenwriter

## Objective
Compile concise, high-signal VMCA prompts that users can paste directly into video generation tools.

## Trigger Rules
Use when the primary request is prompt writing quality and structure.

Positive cues:
- Video prompt refinement.
- VMCA formatting.
- Prompt weight enhancement and cinematic suffixes.

Do not use when:
- The request requires full narrative treatment.
- The request requires ad strategy and CTA architecture.
- The request requires platform orchestration beyond prompt text.

## Inputs
Required:
- Core scene description.

Optional:
- Mood, lens language, frame rate style.
- Duration and aspect ratio.
- Exclusion or compliance constraints.

## Output Schema
Return the universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. VMCA master prompt.
2. Compact prompt variant.
3. Expanded cinematic variant.
4. Prompt tuning checklist.

## Workflow
1. Parse raw scene intent.
2. Fill VMCA blocks: Visual, Motion, Camera, Atmosphere.
3. Enforce positive-only phrasing.
4. Add cinematic quality suffixes.
5. Provide compact and expanded variants.
6. Return assumptions, risks, and next actions.

## Quality Bar
- Keep each VMCA block explicit.
- Keep wording concrete and imageable.
- Keep modifiers non-contradictory.
- Keep output directly usable.

## Safety Rules
- Remove unsafe or policy-violating requests.
- Avoid explicit harm encouragement.
- Mark unknowns instead of inventing.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Creative artifact validator: `scripts/validate_creative_artifacts.py`
