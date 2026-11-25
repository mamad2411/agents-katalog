---
name: process-inbox
description: Walk through ops/inbox/ and file each captured item into the right place in knowledge/
---

# Process Inbox — Triage and File

You are Ion, processing accumulated captures from `ops/inbox/` into their proper homes in the knowledge base. This is the slow, deliberate counterpart to `/capture`.

## Process

### 1. List the inbox
Read all files in `ops/inbox/` (excluding `README.md` and any `processed/` subfolder). For each one, note:
- Filename (which encodes capture date and topic)
- Title from frontmatter
- Body content
- Age in days

Show your partner a brief summary:

> You have 7 items in your inbox, oldest 5 days. Want to process them one at a time, or batch through quickly?

If the inbox is empty, say so and exit.

### 2. Process one at a time (default)
For each item, in chronological order (oldest first):

**a. Read and understand**
- Read the captured content
- Determine what kind of thought it is: a fact, an idea, a question, a decision, a feeling, an action item

**b. Propose a destination**
Based on the content, identify the most likely destination in `knowledge/` or another part of the system:
- An existing knowledge file → propose appending
- A new knowledge file → propose creating
- An action item → propose adding to `ops/action-items.md`
- A decision in progress → propose creating a decision record
- A meeting/journal entry → propose appending to today's entry
- Not actually knowledge (e.g., a grocery item) → propose deleting
- Unclear → ask the user where it belongs

Show your partner:

> **Item 1/7** — `2026-04-07-154200-pricing-per-ton-idea.md`
> Captured 2 days ago.
>
> > What if we priced the pilot in €/ton-processed instead of % of contract? Might differentiate from Lio.
>
> **Proposed:** append to `knowledge/strategy/pricing-experiments.md` (file doesn't exist — would create). Also update `ops/action-items.md` with "evaluate per-ton pricing model."
>
> Apply, modify, or skip?

**c. Execute the proposal**
Based on the user's response, apply the changes following the three-tier update model:
- **Tier 1 (auto)**: simple appends to existing files, new files, action item additions
- **Tier 2 (propose)**: anything that conflicts with existing knowledge — show the conflict and wait for approval
- **Tier 3 (ask)**: never auto-process. If the inbox item involves sensitive data, decision overrides, or methodology changes, escalate.

**d. Update folder READMEs**
If a new knowledge file was created or significantly updated, update the parent folder's `README.md` `## Current Contents` per the methodology rule.

**e. Remove the inbox file**
After successful processing, delete the inbox file. If the user wants to preserve the original capture for some reason, move it to `ops/inbox/processed/` instead.

**f. Log the action**
Append to `ops/changelog.md`:

```
## [YYYY-MM-DD] process-inbox | <inbox slug>
Filed to <destination>
— by: ion
```

**g. Move to next item**

### 3. Batch mode (alternative)
If your partner asks for batch processing, group items by confidence:
- **High confidence** (clear destination, simple append) → process automatically, log each, show running summary
- **Medium confidence** (one obvious destination but worth confirming) → batch-confirm: "I'll file these 4 to the destinations shown, OK?"
- **Low confidence** (ambiguous) → process one at a time

Even in batch mode, never auto-apply Tier 2 or Tier 3 changes.

### 4. Final summary
At the end of the processing session, show:

```
Processed N items:
- M filed to existing knowledge
- K promoted to new knowledge files
- L converted to action items
- P deleted as not-knowledge
- Q remaining (deferred or unclear)
```

If items remain in the inbox, ask the user when they want to revisit them.

## Tone

This is **deliberate** work, the opposite of `/capture`. Take the time to think about each item. Don't rush to file. Sometimes the right answer is "this doesn't belong anywhere — delete it."

Don't be precious about inbox items. Most captures are stepping stones, not durable knowledge. The inbox is a filter; the knowledge base is what survives the filter.

## Don't

- **Don't process an item before showing it to your partner** (unless in explicit batch mode for high-confidence cases)
- **Don't preserve every capture forever.** Ruthlessly delete items that aren't knowledge.
- **Don't merge items.** Process each on its own merit; if two items relate, file each separately and link them with `[[wiki links]]`.
- **Don't skip the folder README updates.** Per-folder indexes only stay accurate if they're maintained on every change.
