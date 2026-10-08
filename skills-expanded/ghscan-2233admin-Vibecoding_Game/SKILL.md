# Evolution Blend Skill Rules

## Goal
`evolutionBlendSkill` is the shared core for both Fusion and Devour evolution image generation.
It owns:
1. Multi-reference image-edit request construction (target + donor references).
2. Prompt guardrails (single subject, white background, no watermark).
3. Default fusion preset batch definitions.

## Hard Rules
1. Fusion and Devour must use one shared pipeline entry, never duplicated split logic.
2. Evolution images must keep white background and no text/watermark constraints.
3. Reference-image policy must be defined in skill mode config, not hardcoded in multiple UI branches.
4. New element presets must be added in the skill config, not scattered across files.
5. Live evolution and preset batch generation must stay distinguishable to avoid overriding current live portraits.
6. Evolution completion must surface gameplay feedback (types, traits, skills, portrait task status), not only internal state mutation.

## Sync Requirement
When `src/game/evolution-pipeline.js` changes, also update:
- `docs/game-architecture.md`
- `docs/system-data-flow.md`
- `docs/context-log.md`
