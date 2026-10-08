---
name: ltm:compact
description: Review the current session and extract undocumented decisions into the project memory
---

# Compact — Extract Decisions to Memory

Perform a compact pass: review everything that happened in this session and
capture any significant decisions that aren't yet in `.memory/DECISIONS.md`.

## What to do

1. Read `.memory/DECISIONS.md` to understand what's already recorded.

2. Review this session's work. Look for:
   - Architecture or design choices that were made
   - Technology or library selections
   - Approaches that were tried and rejected
   - Business logic decisions or constraints discovered
   - Changes to previously recorded decisions
   - Current project status (focus, blockers, open questions)

3. For each unrecorded decision:
   - "Significant" = something a teammate joining next week would need to know.
   - Add a `### heading` with today's date and up to ~10 lines of context.
   - If the decision is truly complex (>10 lines needed), create a detail file
     in `.memory/details/YYYY-MM-DD-<topic>.md` and link to it.
   - If a prior decision was superseded, update it in-place with what changed
     and why. Add a Changelog entry.
   - Check for duplicates — update existing entries rather than adding new ones.

4. Update the `## Status` section with current focus, blockers, and open questions.

5. Update the `> Auto-maintained by claude-ltm. Last updated:` date.

6. Report to the user what was captured (or that nothing new was found).

## Detail file format

When creating a detail file in `.memory/details/`, use this structure:

```
---
decision: <title>
date: YYYY-MM-DD
status: ACTIVE
---

<!-- Valid status values: ACTIVE, SUPERSEDED -->

## Context
[Why this decision was needed — 2-3 sentences]

## Decision
[What was chosen and why — concise]

## Alternatives Considered
- Option B: [why rejected]

## Impact
- [Key consequence 1]
```

## Guidelines

- Keep entries concise. This is a decision log, not documentation.
- Routine code changes are NOT decisions. Choosing a database IS.
- When in doubt about significance, record it — pruning is easier than recreating.
