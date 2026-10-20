---
name: incident-postmortem-loop
description: "Own the loop from incident-declared through postmortem-document through action-items-closed — without losing follow-through three weeks later."
---

# Incident postmortem loop

Most postmortems die in week two. They get written, action items get filed, and then nobody closes them. This skill is the loop that makes the second half happen.

## When to run

- Any incident that hit production or customer-visible scope.
- Any incident that paged on-call.
- Any near-miss the team chooses to learn from.

## Phase 1 — During the incident

1. Page on-call via `pagerduty` if not already.
2. Open a coordination thread in Slack — single source of truth.
3. Keep a running timeline. Agents present in the thread must run `agent-status-pings`.
4. Resolve the incident — recovery is the priority, not blameless analysis.
5. Declare the incident resolved with a timestamp and a one-line summary.

## Phase 2 — Within 24 hours

1. Author the postmortem doc using `sks_docs_propose_patch` or `initiative_file_upload`. Sections:
   - Summary
   - Impact (customer impact, duration, scope)
   - Timeline (from your running thread)
   - Root cause (5 whys, not 1 why)
   - Contributing factors
   - What went well
   - What didn't
   - Action items (each with an owner and a deadline)
2. Share the draft in the team's review channel. Capture comments inline.

## Phase 3 — Action items

1. For each action item, create a planning task (`jira_create_task`) with the postmortem doc as the parent.
2. Assign an owner with `auto-assign-tasks` if the org has opted in.
3. Set a deadline. Default: 2 weeks for code changes, 4 weeks for process changes.
4. Add the action item to the team's weekly review agenda.

## Phase 4 — Closeout (3-4 weeks later)

1. Pull the linked tasks. If any are open past their deadline, escalate to a human lead.
2. When all action items are closed, post a closeout note on the original postmortem doc with the dates each item closed.
3. Update internal playbooks / `internal-wiki` with anything that would have prevented or shortened this incident.

## Anti-patterns

- Postmortem written, action items filed, nobody assigned. Always assign.
- Action items with no deadline. Always set one.
- Skipping Phase 4 closeout. Without it the loop is just a story.
