---
name: Checking live status before review
description: >-
  Use right before sending a person any item for review, approval, or a decision
  (a PR, issue, draft, deploy, or approval request), so the ask reflects the
  item's live state and not stale memory.
---
# Checking live status before review

## Rule
Before you send anyone an item to review or decide on, check that item's live status right then. Don't trust memory, a summary, a note, or another agent's message. Those go stale.

## Steps
1. Look up the item at its source, at the moment you send. Examples:
   - PR: `gh pr view <n> --repo <owner/repo> --json state,mergedAt,reviewDecision,isDraft`
   - Issue: `gh issue view <n> --repo <owner/repo> --json state,closedAt`
   - Draft, deploy, or approval: open it in its own tool and read its current state.
2. Decide:
   - **Still open and waiting on them:** send the review ask.
   - **Already merged, closed, shipped, or decided:** don't ask. Report it as done, with who or when if known.
   - **Can't check:** say so. Don't guess the status.
3. In the message, include the status you saw and the time you checked, in the person's time zone (for example, "open, checked 4:52 PM MT").

## Validation
Every review ask names a status and a check time. No ask goes out for an item that is already done.
