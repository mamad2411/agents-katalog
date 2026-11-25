# /hermes-draft-skill

## Description

Generate and review local skill drafts from evaluated Hermes candidates with strong reuse potential.

## Usage

```
/hermes-draft-skill
/hermes-draft-skill --candidate <candidate_id>
/hermes-draft-skill --draft <skills/local/<name>/SKILL.md>
```

## Process

1. Select an evaluated candidate with reusable execution evidence.
2. Draft a local skill output without editing canonical/global skill assets directly.
3. Link the draft to candidate evidence and review rationale.
4. Keep the draft in local review state until separately promoted.

## Rules

- Generate local skill drafts only
- Do not auto-promote draft skills into canonical/global assets
- Require evidence links before review handoff

## Related

- [Hermes Distill Command](./hermes-distill.md)
- [Hermes Draft Rule Command](./hermes-draft-rule.md)
- [Hermes Skill Drafting Skill](../skills/hermes-skill-drafting/SKILL.md)
