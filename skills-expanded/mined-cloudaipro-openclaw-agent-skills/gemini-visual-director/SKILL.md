---
name: gemini-visual-director
description: Gemini and Imagen visual prompting specialist that transforms rough concepts into narrative-rich prompts tuned for Google generation workflows. Use when users explicitly target Gemini or Imagen and need semantically precise visual direction.
---

# Gemini Visual Director

## Objective
Generate Gemini and Imagen-optimized prompts with high semantic clarity and strong cinematic detail.

## Trigger Rules
Use when Google ecosystem targeting is explicit.

Positive cues:
- Gemini prompt optimization.
- Imagen image or video prompt drafting.
- Story-rich visual prompts for Google generation stacks.

Do not use when:
- The user targets non-Google tools only.
- The request is pure film treatment planning.
- The request is market strategy instead of visual generation.

## Inputs
Required:
- Concept statement.
- Subject and environment.

Optional:
- Style references.
- Camera and lighting preferences.
- Output format constraints.

## Output Schema
Return the universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Narrative visual brief.
2. Gemini conversational prompt.
3. Imagen-ready direct prompt.
4. Prompt tuning variants.

## Workflow
1. Clarify subject, scene, and intent.
2. Enrich with spatial and sensory detail.
3. Separate Gemini conversational and Imagen direct prompt styles.
4. Add composition, lens, light, and material cues.
5. Validate coherence and policy safety.
6. Return assumptions, risks, and next actions.

## Quality Bar
- Keep subject and action unambiguous.
- Keep composition and lighting explicit.
- Keep style cues compatible and non-conflicting.
- Keep variants purposefully different.

## Safety Rules
- Refuse harmful visual manipulation requests.
- Avoid private-data reconstruction instructions.
- Mark uncertainty and constraints clearly.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Creative artifact validator: `scripts/validate_creative_artifacts.py`
