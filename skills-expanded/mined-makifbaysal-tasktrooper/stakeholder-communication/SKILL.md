---
name: stakeholder-communication
category: pm
description: Use when updating the stakeholder - report in outcome language (what changed for users, what's next, what decision is needed), translate technical detail, and surface risks early
source: anthropics/knowledge-work-plugins stakeholder-update (Apache-2.0), adapted
---
# Stakeholder Communication

## Overview

The stakeholder cares about outcomes, not mechanics. The failure modes are forwarding raw technical detail and reporting risks only once they've already hurt.

**Core principle:** Outcome language, and bad news early.

## Rules

- Report what changed for users, what's next, and what decision (if any) is needed.
- **Translate, don't forward.** "Fixed an N+1 in the task query" → "The board now loads quickly on large projects."
- **Bad news early:** report a risk when you detect it, not when it materializes.

## Structure

```
Done since last update: <user-facing outcomes>
In progress:            <what's being built now>
Blocked / needs you:    <the decision required, if any>
```

## Decision-request format

When the update needs a decision, don't just flag it — frame it so one reply resolves it:

```
Decision needed: <the one-sentence question>
Options:         (a) <option> — <one-line tradeoff>
                 (b) <option> — <one-line tradeoff>
Recommendation:  <a> because <reason>
If no answer by <when>: <what happens — e.g. "work stays queued behind it">
```

## Worked Example

Raw: "TaskExporter has an N+1; QA bounced it; the architect flagged a missing index."

Reported: "Export is close but held in review — a performance issue on large projects is being fixed now (no action needed). Everything else from this batch is done. Next up is the mobile export button; I'll need you to confirm the filename format when we get there."

## Common Mistakes

- Forwarding jargon (N+1, nil deref, migration).
- A "green" update that hides a known risk.
- Reporting a slip only after the deadline passed.

## Red Flags

- The update contains a term a non-engineer wouldn't understand.
- A risk you knew about last update surfaced as a surprise this update.
