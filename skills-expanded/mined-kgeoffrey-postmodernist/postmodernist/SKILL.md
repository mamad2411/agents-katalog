---
name: postmodernist
description: Critique AI-generated strategy, marketing, and positioning prose. Use for framing-level rewrites that surface hidden assumptions and fake polish, not for factual QA, coding, or basic copyediting.
---

# Postmodernist Critique

## Overview

Use this skill to pressure-test AI-generated prose that sounds polished, reasonable, and slightly wrong. Treat the text as something to debug and rebuild, not something to defend.

## Use This Skill For

- Mission statements, positioning docs, launch plans, PRDs, strategy memos, investor decks, marketing copy, and similar prose that was drafted by AI
- Requests to critique, audit, pressure-test, or rewrite AI-generated text at the level of framing, assumptions, audience, or rhetoric
- Cases where the user wants to know what the text cannot see, who it excludes, or why it reads as generically "AI"

## Do Not Use This Skill For

- Factual verification, legal or medical review, or anything that depends on current citations
- Grammar cleanup, proofreading, tone softening, or light copyediting without structural critique
- Code, debugging, data analysis, or non-prose tasks

## Working Method

1. Silently scan the text through all six lenses before drafting.
2. Keep the one to three lenses that reveal different structural problems. Drop overlaps.
3. Prioritize what is hidden, flattened, overgeneralized, overpolished, or suspiciously frictionless.
4. Treat the text as raw material to rebuild for the user's purpose, not as an author's intent to explain away.

## Output Modes

### Default critique

Use this for most requests. Write short continuous prose with no bullets or headers. End with:

- one sentence that reframes the whole text
- for persuasive or strategic text, one concrete revision direction on a new line beginning with `Revision:`

### Lens-specific critique

If the user explicitly names a lens or theorist, focus on that lens. In this mode, you may name the lens in the answer because the user asked for it.

### Structured strategy audit

Only use this when the user explicitly asks for a structured audit, memo, deliverable, or presentation-ready review. In that case, use `references/ai-strategy-auditor.md` and format the answer in these sections:

1. `Narrative Audit`
2. `Authenticity Check`
3. `Frame Report`
4. `Revision Direction`

End with one final sentence labeled `Frame Break:`.

## Style Rules

- Do not use academic jargon as decoration.
- By default, do not name the lenses in the output.
- Be specific about who the current framing works for and who it fails.
- Skip what is working unless it changes the diagnosis.
- Prefer concrete audience, incentive, and power analysis over vague taste judgments.
- Do not use em dashes in the output.

## Reference Map

Read only what you need:

- `references/01-deconstruction-toolkit.md` for hidden oppositions and false binaries
- `references/02-structural-awareness.md` for frame limits and omitted perspectives
- `references/03-skepticism-grand-narratives.md` for universal claims and false consensus
- `references/04-hyperreal-navigation.md` for overpolished, generic, AI-signaling prose
- `references/05-world-building.md` for audience or worldview pivots
- `references/06-interpretive-agency.md` for extracting utility and rebuilding the text
- `references/ai-strategy-auditor.md` only when the user explicitly wants a structured audit deliverable
