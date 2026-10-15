---
name: lesson-blueprint
description: Transform the lesson plan into a detailed slide-by-slide blueprint for HTML rendering. Produces slides-blueprint.md. Never renders HTML. Every field in the blueprint schema must be filled. No vague media descriptions.
---

You are creating the slide blueprint from the approved lesson plan.

## BEFORE STARTING

1. Read `aulas/<slug>/briefing.md`
2. Read `aulas/<slug>/lesson-plan.md` (must have `time_budget_check: pass`)
3. Read `aulas/<slug>/sources.md`

If lesson-plan.md is missing or `time_budget_check: fail`: stop and state what's needed.

## Slide allocation from plan

Each lesson block becomes one or more slides. Typical allocation:
- introdução: 1–2 slides (capa + agenda OR capa + objective slide)
- desenvolvimento: 2–4 slides per sub-topic
- fixação: 1–2 slides (activity prompt + example)
- fechamento: 1 slide (resumo or call-to-action)

Total slides: aim for 1 slide per 3–4 minutes of planned duration.
For a 45-minute lesson: target 10–15 slides.

## For each slide, fill ALL required fields

Every slide entry in the blueprint must contain (NO EXCEPTIONS):

**Identity:** slide_number, lesson_block_ref, type, priority, estimated_duration_seconds

**Pedagogical:** pedagogical_objective (one sentence mapping to a briefing objective)

**Content:** title (≤8 words), body_items (≤5 items, each ≤15 words), body_density, speaker_notes (or null if not needed)

**Media:** required (bool), type, description (≥20 words if required=true), alt_text, pedagogical_function

**Layout:** template, media_position, content_alignment, typography_hierarchy, text_size_hint

**Meta:** visual_intent, sources (list of source_ids), rendering_notes, accessibility_notes, responsive_notes

## Media description rules

If `media.required: true`:
- `description` must be ≥ 20 words
- Describe what the image/diagram/video should SHOW, not what it should MEAN
- Include: subject matter, composition, key elements, style (diagram vs. photo vs. animation)
- Example of INVALID description: "imagem do relógio lógico"
- Example of VALID description: "Diagrama de sequência mostrando três processos P1, P2, P3 em linhas verticais paralelas com setas horizontais representando mensagens trocadas. Cada evento mostra seu timestamp de Lamport. Fundo branco, linhas pretas, setas coloridas por processo."

`pedagogical_function` must explain the cognitive reason for the media:
- INVALID: "ilustrar o conceito"
- VALID: "Mostra a propagação de timestamps através de mensagens, tornando a regra de incremento concreta e visualizável — sem este diagrama, alunos tendem a confundir incremento com sincronização"

## Sample-then-continue validation

After writing slides 1–3, STOP and show them to the professor:
"Aqui estão os primeiros 3 slides do blueprint. A direção está certa? (sim / ajustar: campo=valor)"

Only continue to remaining slides after "sim" to the sample.

## GUARDRAILS

- NEVER render HTML
- NEVER leave `rendering_notes` or `accessibility_notes` empty
- NEVER use `body_density: high` for slide types other than: comparacao, agenda, resumo
- NEVER add content not present in lesson-plan.md
- NEVER describe media as "decorativa" without a compelling justification
- NEVER write slides-blueprint.md before the sample is approved
- Ensure slides-blueprint.md has `total_slides` matching the actual count in the file

## Output

Write to `aulas/<slug>/slides-blueprint.md` following `.super-professor/templates/slides-blueprint.template.md`.
Set `total_slides` = actual number of slides generated.
