---
name: design-conventions
description: Use `design-conventions` to get Project Conventions when deciding on name of variable, class, file, system object, label or command or understanding acronyms and project definitions to avoid ambiguous wording.
---

## Internal Acronyms
- None.

## Definitions
- **Skill**: Reusable agent guidance loaded by `skill` tool.
- **Local memory**: Durable local fact stored by `learn`; not a reusable skill.
- **Reference**: Companion file inside skill, read through `skill` `reference` arg.

## Naming Rules
### Skill Tool Names
**Purpose:** Keep skill operations one tool family.
**Pattern:** Use `skill` to load and `skill_edit` to create or replace reusable `SKILL.md`. Use `learn` for durable local memory. Do not use removed `skill_read` or `skill_edit_reference`.

### Skill Reference Names
**Purpose:** Keep companion files linked to main skill.
**Pattern:** Pass relative reference path in `skill` `reference` arg. Pass `references[]` to `skill_edit`.

---

**IMPORTANT**: Edit this `design-conventions` skillwhenever new naming conventions or domain terms are introduced.
