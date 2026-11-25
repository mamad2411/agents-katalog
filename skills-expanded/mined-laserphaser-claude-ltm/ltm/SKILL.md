---
name: ltm:save
description: Explicitly save a specific decision to the project memory
---

# Save a Decision to Memory

The user wants to explicitly record a specific decision. They may provide
the decision as an argument (e.g., `/ltm:save chose Stripe for payments`)
or describe it in their message.

## What to do

1. Read `.memory/DECISIONS.md` to check for existing related entries.

2. Parse the user's input to understand the decision being recorded.

3. Check for duplicates — if a similar decision already exists, update it
   rather than creating a new entry.

4. Add the decision to the appropriate section in `.memory/DECISIONS.md`:
   - Use a `### heading` with today's date
   - Include up to ~10 lines of context explaining the decision and rationale
   - Place it under the most fitting `## Section` heading (create a new section
     if none fits — sections are free-form)
   - If the decision supersedes a prior one, update the old entry in-place and
     add a Changelog entry

5. If the decision is complex and the user provided extensive rationale:
   - Create a detail file at `.memory/details/YYYY-MM-DD-<topic>.md`
   - Keep the main file entry concise with a link to the detail file

6. Update the `> Auto-maintained by claude-ltm. Last updated:` date.

7. Confirm to the user what was saved and where.

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
