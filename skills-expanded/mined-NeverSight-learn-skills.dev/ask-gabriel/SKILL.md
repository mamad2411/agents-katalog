---
name: ask-gabriel
description: >-
  Thin router over this pack: recommend which skill to run next. Sole
  auto-invokable skill. Use when unsure which skill, what to run next, before
  non-trivial work, after a phase completes, when multiple pack skills could
  apply, or the user asks what to do. Agents should reach for this often.
---

# Ask Gabriel

You don't remember every skill — ask. Stay **thin**: recommend only; do **not** load other skills' bodies until the user accepts.

**Sole auto-invokable skill** in this pack. Dual skills (`/grill-me`, `/repair`, …) self-select standalone vs flow via [variants.md](../variants.md) — never recommend `*-flow` names.

## On-ramps

| Situation | Start with |
| --- | --- |
| Unsure which skill | Stay here — answer below |
| Fuzzy idea / research | `/analyze` |
| Need a Linear/GitHub ticket | `/write-ticket` |
| Build until X is true | `/goal` (ticket: `/goal IN-1234` or `/goal #42`) |
| Ship branch + optional PR | `/publish` |
| Linear ticket → landed PR (autonomous) | `/just-do-it IN-1234` |
| Sharpen intent | `/grill-me` |
| Structure / folders / data shape | `/architecture` |
| Fix or polish UI | `/design` |
| Bug / something broken | `/repair` |
| Review local branch vs main | `/code-review` |
| Review open GitHub PR | `/pr-review` |
| Lock complex behavior with tests | `/create-test` (user must ask; only after `/code-review` or `/pr-review` recommends) |

Internals (`/validate`, `/implement`, `/taste`, …) are flow steps looked up by `/goal` or `/repair` — not typical destinations. Taste/architecture/design **doctrine** is loaded by other skills when relevant.

## How to answer

1. If the ask is unclear, ask for one sentence of intent.
2. Recommend **one** next skill and the next 1–2 steps.
3. Do **not** run that skill unless the user says to (or said “just pick and go”).
4. Never dump doctrine or other SKILL bodies into this turn.
