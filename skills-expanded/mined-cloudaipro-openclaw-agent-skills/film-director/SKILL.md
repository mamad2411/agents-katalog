---
name: film-director
description: Cinematic directing skill for transforming story ideas into film treatment, act structure, scene planning, camera language, and lighting direction for AI-assisted pre-production. Use when users ask for movie-style narrative planning, scene breakdowns, or cinematography strategy. Do not use for short-form ad conversion creative.
---

# Film Director

## Objective
Produce narrative-first cinematic plans with coherent story logic, scene rhythm, and visual continuity.

## Trigger Rules
Use when the request centers on story and film grammar.

Positive cues:
- Film treatment, feature short outline, scene architecture.
- Shot design by emotional beats.
- Camera and lighting strategy for narrative continuity.

Do not use when:
- The request is ad campaign conversion optimization.
- The request is prompt-only copywriting without narrative structure.
- The task is non-creative operations planning.

## Inputs
Required:
- Core premise or story concept.
- Genre or tone.
- Desired duration or scope.

Optional:
- Reference films.
- Character list and arcs.
- Production constraints.

## Output Schema
Return the universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Logline and thematic statement.
2. Three-act or sequence treatment.
3. Scene-by-scene cinematography plan.
4. Lighting and color script notes.
5. Pre-production checklist.

## Workflow
1. Resolve premise, stakes, and protagonist drive.
2. Build act-level narrative progression.
3. Expand into scene beats with emotional transitions.
4. Define camera language and lensing intention per scene.
5. Define lighting plan and color evolution.
6. Check pacing, continuity, and thematic cohesion.
7. Return assumptions, risks, and next actions.

## Quality Bar
- Tie every scene to story progression.
- Keep camera choices motivated by emotion or information.
- Keep color and lighting shifts narratively justified.
- Surface continuity risks early.

## Safety Rules
- Decline requests for explicit harm instructions.
- Avoid sensitive misinformation framing.
- Mark invented details as assumptions.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Creative artifact validator: `scripts/validate_creative_artifacts.py`
