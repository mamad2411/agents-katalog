---
name: create-prd
description: >
  Author OKF-shaped PRDs under docs/prd/ (ignore or track per setup): MVP journey,
  FRs, DoD, bug appendix; cite docs/adr via create-adr; diagrams via ascii. Use when
  turning a grilled idea into a product requirement doc or editing an existing PRD.
disable-model-invocation: true
---

# create-prd

Author **PRDs** — MVP scope, one critical journey, behavioral FRs, DoD, living bug appendix. Durable “why” lives in **ADRs** via **`create-adr`**, not here.

Common entry: **`grill-me`** post-grill **A** (recommended default) auto-runs this skill from settled decisions.

## Homes

- PRD home: `docs/prd/` — **ignore or track** is a **`setup-bmurrtech-skills`** choice (default ignore; [ADR 0013](https://github.com/bmurrtech/skills/blob/main/docs/adr/0013-ADR-prd-tracking-choice.md)). Rationale: library [how-to-bmurrtech-skills — PRDs](https://github.com/bmurrtech/skills/blob/main/docs/how-to-bmurrtech-skills.md#prds-docsprd) / [knowledge/prd.md](https://github.com/bmurrtech/skills/blob/main/knowledge/prd.md) — not required in the consumer tree.
- Filename: `NNNN-PRD-<slug>.md` (no project-key prefix)
- Catalog: `docs/prd/index.md` (same track/ignore policy as the directory)
- ADR home: `docs/adr/` (tracked)

Missing scaffold / unclear PRD policy → run **`setup-bmurrtech-skills`** (re-asks Commit PRDs?).

## Action

- **New:** next `NNNN` = max in `docs/prd/` + 1 (first is `0001`). Write OKF frontmatter + body from [references/prd-template.md](references/prd-template.md). Update local `index.md`.
- **Edit:** only the user-specified file. Ambiguous create vs edit → ask.
- Proceed from conversation and existing docs; do not block on unanswered questionnaires.

### ADR — exist then cite / warrant then ask

| Branch | Action |
|--------|--------|
| User cites an ADR | Resolve path under `docs/adr/`; cite in Summary. Missing → say so; omit bullet. |
| Decision looks ADR-worthy (user asks, or warrant: costly to reverse · real alternatives · future “why?”) | If the grill thread is muddy, suggest **`handoff`** first. Ask once: create via **`create-adr`** now? Yes → run `create-adr`, then cite. No → todo and continue PRD. |

Skip the offer when warrant fails and the user did not ask.

### Diagrams

At least one ASCII diagram tied to UJ-1 or an FR — follow **`ascii`**.

## PRDs contain / do not

**Contain:** MVP definition, UJ-1, scope in/out/non-goals, behavioral FRs, phases (order only), DoD, bug appendix, ADR path cites, diagrams.

**Do not contain:** stack rationale / architecture “why” (→ `create-adr`); assumptions/constraints that belong in ADRs (cite instead).
