---
name: engineering
description: Route to the right engineering skill in skills/engineering/ — architecture review, code review, bug diagnosis, test-driven development, UI design engineering (build, polish, anti-slop review), and UX/UI assessment. Use when the user asks to review code, debug, find a root cause, write tests first, improve architecture, build or polish a user interface, or evaluate a product's UX/UI.
---

# Engineering Skills

Use this skill to pick the right skill in `skills/engineering/`. Open only the skill that matches the request; do not load all of them.

## Skills in this category

| Skill | Use when | Output |
|---|---|---|
| [architecture-review](architecture-review/SKILL.md) | Improving design, module boundaries, coupling, or simplifying a codebase | Review findings and simplification options |
| [code-review](code-review/SKILL.md) | Reviewing a diff, PR, or local change for bugs, regressions, and missing tests | Prioritized findings |
| [diagnose](diagnose/SKILL.md) | Debugging an error, stack trace, failing test, flaky behavior, or regression | Root cause and fix |
| [tdd](tdd/SKILL.md) | Building or fixing behavior through red-green-refactor | Tests first, then code |
| [ui-design-engineering](ui-design-engineering/SKILL.md) | Building, hardening, polishing, or reviewing a web UI, including motion, accessibility, and the anti-slop gate | Working interface or review report |
| [ux-ui-design-assessment](ux-ui-design-assessment/SKILL.md) | Auditing a project's UX/UI, or designing UX/UI for a new product, as a written document | `UX-UI-ASSESSMENT.md` or `UX-UI-DESIGN-DOC.md` |

## Routing

- Something is broken and the cause is unknown → `diagnose`, then `tdd` to lock the fix in.
- A change is ready and needs a second look → `code-review`.
- The structure feels tangled or hard to change → `architecture-review`.
- Code for a screen, component, or flow is needed → `ui-design-engineering`.
- A written UX/UI evaluation or design document is needed, without code → `ux-ui-design-assessment`; hand implementation to `ui-design-engineering`.
- A request spans two skills → start with the one that produces the information the other needs (for example `ux-ui-design-assessment` before `ui-design-engineering`).

## Rules

- This skill only routes. Do the work by following the chosen skill's own `SKILL.md`.
- Follow the project's Planning Mode rules for multi-file or architectural work before editing code.
- If no skill here fits, say so and continue with normal judgment instead of forcing a match.
