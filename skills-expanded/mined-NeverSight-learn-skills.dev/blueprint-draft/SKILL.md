---
name: blueprint-draft
description: Transform a shaping scratchpad into a formal engineering blueprint with decided language, collaborative estimation, and Linear ticket linking. Use when user is ready to write the blueprint, wants to draft the blueprint, or has completed the shaping period.
---

# Blueprint Draft

Transform a scratchpad (from `blueprint-scratchpad` or any freeform shaping doc) into a formal engineering blueprint. Every section uses decided language — no hedging above the fold.

## Process

### 1. Pre-flight

1. Ask for the scratchpad location if not already known. The scratchpad does not need to follow `[DECIDED]`/`[OPEN]`/`[REJECTED]` conventions — accept any freeform doc.
2. Read the scratchpad.
3. Scan for unresolved items. If critical open questions remain, flag them. User decides: resolve now or defer to Risks/Open Questions.

### 2. Section-by-section grill

For each blueprint section in order:
1. Synthesize what's decided in the scratchpad.
2. Present a draft in blueprint tone.
3. Grill on gaps or weak spots.
4. User approves, revises, or sends back.
5. Write the approved section to the working blueprint doc.

See [section-guide.md](section-guide.md) for per-section grill guidance.
See [blueprint-template.md](blueprint-template.md) for the output structure.

### 3. Scratchpad updates

When decisions are made or alternatives rejected during drafting, write them back to the scratchpad. It remains the living record of the full shaping + drafting journey.

### 4. Collaborative estimation

1. Propose work item rows derived from Technical Implementation (one row per logical chunk — typically 5-10 rows).
2. For each row: back-and-forth discussion on scope, complexity, days, testing time.
3. Run the "connection test" — every row maps to Technical Implementation and vice versa.
4. Link existing Linear tickets. Offer to draft new ones (never create without approval).

### 5. Linear ticket creation

1. Propose ticket title + description.
2. User approves, revises, or rejects.
3. Only after approval: create the ticket and add the link to the estimates table.

## Writing Rules

See [writing-rules.md](writing-rules.md) — enforced in all output.

## Conventions

- Codebase exploration only when the user directs it.
- No writes to shared systems without explicit approval.
