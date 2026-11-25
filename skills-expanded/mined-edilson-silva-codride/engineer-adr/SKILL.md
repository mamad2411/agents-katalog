---
name: engineer-adr
description: Draft a new Architecture Decision Record
---

# ADR

Every other skill in this framework treats ADRs as load-bearing — `engineer-discover` scans them, ADR-compliance checking validates code against them, `engineer-architecture` checks alignment with them — but none of them help you *write* one. This skill does.

Use it whenever a real architectural decision gets made: a technology choice, a pattern adopted (or rejected), a trade-off resolved in a specific direction. Not for implementation details that don't constrain future work.

The user's request should describe the decision to record. If they didn't state it clearly, ask before proceeding rather than guessing.

## 1. Find the right number and check for conflicts

- List `docs/technical-context/adr/` (create it if it doesn't exist). Numbers are zero-padded and sequential (`001-`, `002-`, ...) — the new one is the next number.
- Skim existing ADRs for anything this decision touches, contradicts, or supersedes. If it does, say so explicitly and ask the human whether the old ADR should be marked **Superseded**, with a link to the new one — don't silently leave a contradiction in place.

## 2. Understand the decision

Ask the human (don't assume):
- What circumstances led to needing this decision? What's the problem it resolves?
- What did we decide, precisely?
- What alternatives were considered, and why were they not chosen?
- What are the consequences — both the benefits and the real costs/trade-offs? A decision with no downsides listed usually means they weren't looked for hard enough.
- Is this decision reversible, and how costly would reversing it be?

## 3. Write it

Save to `docs/technical-context/adr/<NNN>-<slug>.md`:

```markdown
# ADR-<NNN>: <Decision Title>

**Status**: Accepted
**Date**: YYYY-MM-DD

## Context
What circumstances led to this decision?

## Decision
What did we decide?

## Rationale
Why did we choose this approach?

## Consequences
What are the positive and negative impacts? Be honest about the costs, not just the benefits.

## Alternatives Considered
What other options did we evaluate, and why weren't they chosen?
```

Keep it concrete and specific to this project — a generic ADR that could apply to any codebase isn't useful to ADR-compliance checking or to the next engineer reading it.

## 4. Wrap up

- If this ADR supersedes another, update the old one's `Status` to `Superseded by ADR-<NNN>` and add a note linking forward.
- Tell the human to run `engineer-discover` to refresh `docs/technical-context/briefing/adrs-summary.md` so the new ADR is picked up by `engineer-context`'s selective loading and by ADR-compliance checking.
