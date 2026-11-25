---
name: incident-digest
description: Turns the mail and Teams traffic around an incident into a dated timeline with the open questions and who owns each. Use when the user asks for an incident timeline, what happened during an outage, to prepare a post-incident review, or to catch up on an incident in progress.
---

# Incident Digest

Rebuilds what happened and when, from the traffic, so the review starts from a timeline instead of
from memory.

## Inputs
- **Email** and Teams traffic for the incident window
- **Enterprise Search** for any status page, runbook or change record referenced in the traffic
- `references/config.md` for the severity vocabulary and the channels that matter

## Procedure
1. **Establish the window.** First signal to last all-clear, from the traffic itself. If the
   incident is open, say so and mark the timeline as in progress.
2. **Build the timeline** in UTC and in the user's local time, one row per event that changed what
   people knew or did. Chatter that changed nothing is not an event.
3. **For each row**: timestamp, what happened, who said it, and the source link.
4. **Separate three things explicitly**, because post-incident reviews fail when they blur:
   **what was observed**, **what was believed at the time**, and **what is now known**. A belief
   that turned out wrong stays in the timeline, labelled, because it explains the decisions.
5. **List open questions** with an owner each, and anything the traffic references but does not
   resolve.
6. **Write** the digest to the output folder.

## Output
Timeline table, then: observed versus believed versus known, open questions with owners, and
references the traffic made to documents that were not found.

## Definition of done
Every timeline row is sourced, beliefs are separated from facts, and open questions carry owners.

**No blame, ever.** The digest names who said what, because that is the record, and never why
anyone did or did not do something. Attributing motive is out of scope and corrosive.

## When there is no data
- Sparse traffic: say the timeline is thin and name the window searched. A three-row timeline
  honestly labelled is better than a padded one.
- Conflicting timestamps across systems: show both and say they conflict.
- Incident still open: mark in progress and say the all-clear was not found.

## Boundaries
- **Never post to a channel, never reply to a thread, never update a status page.**
- Never assign an action. List open questions with suggested owners for a human to assign.
- Never state a root cause. Surface what the traffic says and label it belief or finding.
- Never include customer identifiers in the digest unless the user asks and approves.
- **Draft only.** The digest is written for the user. Circulating it to a review group is the
  user's action, behind the normal approval prompt.

## Self-check
- Is every row sourced and timestamped?
- Are beliefs at the time clearly separated from what is now known?
- Did I avoid stating a root cause or attributing motive?
