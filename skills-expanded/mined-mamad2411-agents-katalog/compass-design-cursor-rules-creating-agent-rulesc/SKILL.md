---
description: How to add agent guidance — AGENTS.md tiers, dual styling rules, skills; avoid always-on bloat
globs: "claude.md,.cursor/rules/**/*.mdc"
alwaysApply: false
---

# Creating agent guidance

Use when adding or changing project agent instructions. Prefer **conditional** context over always-on text.

## Three tiers

| Tier | Where | What |
| --- | --- | --- |
| Universal (always on via `@AGENTS.md`) | Root [AGENTS.md](../../AGENTS.md) | Short must-dos, hooks, blurbs, **index** — no long examples/tables |
| Area-nested | `src/guidelines/AGENTS.md`, `packages/compass-ui/AGENTS.md`, `packages/compass-proto/AGENTS.md` (+ tiny `CLAUDE.md` with `@AGENTS.md`) | Docs / Storybook / proto handbooks |
| Path-scoped styling | [.claude/rules/styling.md](../../.claude/rules/styling.md) **and** [.cursor/rules/styling.mdc](styling.mdc) | BEM, tokens, motion, opacity, Scrollbars — **keep both bodies in sync** |

Playbooks (multi-step how-tos) → [.cursor/skills/](../skills/) (e.g. `add-docs-topic`), not always-on AGENTS.

Claude path nudges (thin): `.claude/rules/guidelines.md` — point at nested AGENTS; do not duplicate full handbooks.

## Efficiency

- Do **not** `@import` large files from `CLAUDE.md` (only `@AGENTS.md`).
- Do **not** set `alwaysApply: true` unless the rule must hit every turn (prefer `globs` / agent-requested `description`).
- Put mapping tables and bad/good examples in the styling pair or nested AGENTS — not root AGENTS.
- Never leave the only copy of a must-follow rule solely under `.cursor/rules` or solely under `.claude/rules` without the AGENTS / dual-file pattern.

## Checklist

- [ ] Root AGENTS stayed thin (or only gained an index link)
- [ ] Area content landed in the right nested `AGENTS.md`
- [ ] Styling changes updated **both** `.claude/rules/styling.md` and `.cursor/rules/styling.mdc`
- [ ] Playbooks are skills when procedural
- [ ] No duplicated full tables across tiers
