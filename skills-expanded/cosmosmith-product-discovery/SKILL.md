---
name: cosmosmith-product-discovery
description: Turn a rough product idea, vague user desire, or early "create a world" concept into a concise Cosmosmith idea brief. Use when the user has not yet provided a clear problem, target user, first valuable slice, or acceptance criteria; may use web research when market context is current or competitive.
---

# Cosmosmith Product Discovery

## Purpose

Clarify a rough idea without over-questioning the user, then produce `docs/cosmosmith/idea-brief.md`.

## Workflow

1. Read project `AGENTS.md` if present, `task.md` if present, and any existing `docs/cosmosmith/idea-brief.md`.
2. Capture the user's seed idea in one or two sentences.
3. Ask at most three high-leverage Socratic questions only when the answer would change the brief.
4. Use web research if current competitors, pricing, regulations, or ecosystem expectations matter.
5. Write or update `docs/cosmosmith/idea-brief.md` using the idea brief structure from the plugin template.
6. Update `task.md` with the next claimable task for `cosmosmith-spec-governor`.

## Output Requirements

The idea brief must include:

- User seed.
- Primary user.
- Job to be done.
- Pain or desire.
- Proposed world.
- First valuable slice.
- Acceptance criteria.
- Open questions.

## Completion

Stop when the idea brief is concrete enough for proposal and design work. If the user's intent is still too unclear, mark the task `blocked` in `task.md` with the exact missing decision.

