---
name: story-refine
description: Audit an existing user story and fix it in place. Cohn+Gherkin canonical. Inherits all hard rules from storywright-base.
trigger: "/story-refine | refine this story | improve this story | refinar historia | this story is incomplete"
intent: Refinement skill for stories that already exist but are incomplete or weakly specified. Behavior 100% identical to siblings except for source (existing story text) and split-behavior (recommend /story-split when pre-split count ≥2).
version: 2.3.0
inputs:
  - text
  - image
  - figma-link
outputs:
  - story.standard.md
  - story.dev.md
  - .storywright-context.json
composes:
  - _components/storywright-base
  - _components/clarification-questions
  - _components/business-rules
  - _components/acceptance-criteria
  - _components/edge-cases
  - _components/analytics-events
  - _components/risks-and-dependencies
  - _components/definition-of-done
  - _components/invest-checklist
  - _components/story-formatter
  - _components/estimation
---

## Purpose

Bring an existing user story up to standard *without* turning it into a feature spec. Emits two files: `story.standard.md` (PM-facing) + `story.dev.md` (dev-facing).

**All hard rules, canonical output shape, language detection, mechanical pre-split test, context persistence, terminal-only Q, mechanical NxN dep matrix, per-child V audit, and INVEST handling live in `[[storywright-base]]`. Read that first. Anything in this file is a SOURCE-SPECIFIC or SPLIT-BEHAVIOR delta only.**

## Source-specific differential

- **Source:** an existing user story (text). May be vague, missing sections, or have hand-wavy ACs.
- **What changes vs base:**
  - **Preserve original wording** where it was already good. Refine is NOT regenerate — if the PM already wrote a sharp persona / goal / so-that, do not rephrase it.
  - **Don't renumber ACs** the team may already reference externally. Append new content, don't shuffle.
  - **Detect which sections are present / missing / weak** before applying the base canonical block. Fill only what's weak; leave good sections alone.
  - If companion image / Figma is attached, base conflict-detection applies. Story text is canonical for `User Story / Scope / Business value`; image/Figma is canonical for `component names / observable states` referenced in AC.

## Split behavior differential

If the base **deterministic pre-split test** returns count ≥2:
- **STOP refining.**
- Show candidate children + per-pair dep notes (base rule 10) + V audit (base rule 11).
- Ask via `AskUserQuestion`: "This story has [N] independent flows. Run split now?" with options:
  - "Yes, split" → execute `[[story-split]]` inline (epic + children + .storywright-context.json).
  - "Continue without split" → proceed with single-story path (fill canonical block → INVEST → render both files).
  - "No, keep as-is" → stop. No output written.
- Do NOT silently auto-split without the AskUserQuestion confirmation.

If count ≤1:
- Proceed with the base step-by-step Application skeleton, applying the source-specific preservation rules above.

## Application (step-by-step)

Follow the **base Application** skeleton exactly. Refine-specific behavior:
- Step 5 (gap-check): only fill **weak/missing** sections; leave sharp sections alone.
- Step 7 (pre-split test): on count ≥2 → STOP refining, route to `/story-split` recommendation.
- Step 11 (log): label as "Refinement log".

## Examples

### Good — READY
Input: story with title + Use Case + 2 vague ACs.
- Pre-split count = 1.
- Tighten ACs to single Given/When/Then. Leave Use Case alone (was good).
- INVEST → READY. ≤3-line Refinement log. Render.

### Good — SPLIT
Input: story with 7 AC bullets (grid + counter + pagination + link).
- Pre-split count = 4 (grid, counter, pagination, link).
- STOP. Terminal message: candidate children + dep notes + V audit + "Run `/story-split`".
- No refined story written.

### Good — passive goal fires
Refining: *"As a user, I want to view list of customers, so that I find details."*
- Rule G of base fires. Ask: "What does the user do with the customer they find?"
- User: "Call them." → strengthen so-that.

### Bad
Treating refine like generate — restating the user goal when the PM already wrote it.

### Bad
Renumbering AC bullets the team may already reference.

### Bad
Producing a 400-line refined story (violates base rule 3 + INVEST Small ceiling).

## Common Pitfalls (refine-specific)

- Rewriting good content. If a section is sharp, leave it.
- Renumbering ACs. Append, don't shuffle.
- Skipping the base pre-split test (step 7) — refining an oversized story produces an oversized refined story.
- All other pitfalls listed in `[[storywright-base]]` apply equally.

## References

- [[storywright-base]] — the rulebook
- [[story-generate]] (when input is ambiguous, not an existing story)
- [[story-split]] (when count ≥2)
- [[story-from-figma]] (when input is Figma URL)

<claude-specific>
- Read `[[storywright-base]]` before applying. Do not duplicate its rules in your reasoning.
- Diff the original sections against the refined ones; only emit changes that materially improve the story.
- Use extended thinking when running the base pre-split counter.
</claude-specific>
