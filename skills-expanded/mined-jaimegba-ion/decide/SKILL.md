---
name: decide
description: Structured decision-making — lay out options, analyze tradeoffs, recommend, and document
---

# Decide — Decision Framework

Help your partner make a structured decision and document it in the knowledge base.

## Process

1. Clarify the decision to be made — restate it as a clear question
2. Read relevant knowledge from the knowledge base for context
3. Identify the options (from the partner + suggest additional ones they may not have considered)
4. Analyze each option

## Analysis Framework

For each option, evaluate:
- **Alignment**: How well does this serve the partner's stated mission, vision, or current priorities?
- **Feasibility**: Can it be executed with current resources and constraints?
- **Reversibility**: How hard is it to undo if wrong? Prefer reversible decisions, especially when uncertainty is high.
- **Time horizon**: When does this pay off? What's the opportunity cost of waiting?
- **Risk**: What could go wrong? What's the worst-case downside?
- **Opportunity cost**: What is given up by choosing this over the alternatives?

## Recommendation

Be opinionated. Your partner wants honest assessment, not a balanced spreadsheet. State which option you'd choose and why. If the decision is close, say so — but still pick one.

## After Decision

When your partner reaches a decision:

1. Create a decision record at `knowledge/decisions/YYYY-MM-DD-decision-title.md`:
   ```yaml
   ---
   title: "Decision: [clear title]"
   description: "[one-line summary of what was decided and why]"
   last_updated: YYYY-MM-DD
   updated_by: [name]
   status: active
   ---

   # Decision: [Title]

   ## Context
   [Why this decision needed to be made]

   ## Options Considered
   [Each option with pros/cons]

   ## Decision
   [What was decided]

   ## Reasoning
   [Why this option was chosen]

   ## Action Items
   [What needs to happen next]

   ## Participants
   [Who was involved in making this decision]
   ```
2. Update any knowledge files affected by the decision
3. Add action items to `ops/action-items.md`
4. Update `ion/state.md` if the decision is significant

## Rules

- Decision files are **append-only**. Once written, never edit. If a decision is reversed later, write a new decision record that supersedes the old one — don't rewrite history.
