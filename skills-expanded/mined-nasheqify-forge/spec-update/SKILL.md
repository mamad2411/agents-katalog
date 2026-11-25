---
name: spec-update
description: >
  DEPRECATED. Split into two more specific skills.
  Use retroactive_spec_update for code-as-evidence catch-up (existing specs
  drifted from code). Use spec_authoring for new specs or new sections
  that need Interview-based User-Intent clarification.
status: deprecated
invocation:
  primary: sub-skill
  secondary: [workflow-step]
disable-model-invocation: false
uses: []
---

# Skill: spec-update (DEPRECATED)

This skill was an early draft that conflated two different use cases:

1. **Retroactive catch-up**: Code evolved, spec drifted, sync needed.
2. **Feature addition to existing spec**: New functionality documented.

These are structurally different workflows — (1) has the code as evidence
and needs no User-Intent interview, (2) requires an Interview-based
clarification because the User-Intent is not yet captured anywhere.

## Replacement

| Old use case | New skill |
|---|---|
| Retroactive catch-up | `skills/retroactive_spec_update/SKILL.md` |
| Feature addition to existing spec (needs Interview) | `skills/spec_authoring/SKILL.md` (§"Wann aufrufen" covers this) |
| Cross-spec consistency post-amendment | `skills/spec_amendment_verification/SKILL.md` |
| Spec quality review | `skills/spec_board/SKILL.md` |

## Why deprecated

The skill had one phase labeled "Write entlang 5 Primitives" but the input
to that phase was ambiguous — sometimes git log (retroactive), sometimes
user-intent (feature addition). The two inputs require different workflows
(code walkthrough vs interview), so splitting into two skills is cleaner.

Do not use this skill. Pick the right successor from the table above.
