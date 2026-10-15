---
name: skill-schema-v2
description: "Load when creating, auditing, refactoring, or repairing an Agent Skill for reuse, governance, and runtime efficiency."
version: "2.0.0"
last_updated: "2026-06-02"
depends: []
metadata:
  author: "yinyo"
  category: "skill-engineering"
  package: "skill-schema-v2.skill"
---

# Skill Schema V2

This is the compatibility entrypoint for the v2 skill schema. The installable v2 package is in `skill-schema-v2.skill/`.

Use it when a user is designing, auditing, refactoring, or repairing an Agent Skill.

## Core Rule

A skill has three surfaces:

```text
Routing Surface: name + description + frontmatter
Contract Surface: goal + inputs + permissions + evidence + output + verification + handoff
Runtime Boundary Surface: docs + examples + scripts + operators + fallback paths
```

The three surfaces must be aligned. If the description routes one task, the contract must govern that task, and runtime resources must support that task without forcing irrelevant context into the model.

## What Changed in v2

v2 adds three 2026 findings:

- **Contractual Skills**: skills should be readable task contracts with explicit boundaries and acceptance criteria.
- **138K SKILL.md reusability study**: routing defects, body bloat, poor resources, safety issues, portability gaps, and persona/scope conflicts are measurable defects.
- **SkillSmith**: raw skill injection wastes context; skills should expose minimal runtime boundaries and load detail progressively.

## Audit Output

When auditing, score out of 100:

| Area | Points |
|---|---:|
| Routing | 15 |
| Contract | 20 |
| Runtime Boundary | 15 |
| Reusability | 15 |
| Safety | 15 |
| Signal Density | 10 |
| Versioning | 5 |
| Self-Consistency | 5 |

## Runtime Resources

Load only as needed:

- `skill-schema-v2.skill/SKILL.md` for the complete v2 contract.
- `skill-schema-v2.skill/docs/v2-design-spec.md` for design rationale.
- `skill-schema-v2.skill/docs/audit-rubric.md` for scoring details.
- `skill-schema-v2.skill/docs/repair-playbook.md` for repair patterns.
- `docs/paper-digests.md` for paper evidence.
