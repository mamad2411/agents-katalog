---
name: grant-tracker
description: >
  Maintain the cross-session grant pipeline. This skill should be used when the
  user says "what's in our grant pipeline", "what deadlines are coming up",
  "update the tracker", "we submitted X", "we won/lost X", or "grant status".
  Also invoked by other GrantForge skills to register status changes.
version: 0.1.0
---

# Grant Tracker

Keep `.grantforge/tracker.md` as the single source of truth for every
opportunity across its life. The tracker compounds: every closed
application feeds lessons and reusable language back into the profile.

## Tracker format

A markdown table, one row per opportunity:

`Funder | Program | Amount requested | Deadline | Status | Workspace folder | Next action | Owner | Notes`

Statuses: `watching` → `intake` → `preparing` → `ready to submit` →
`submitted` → `awarded` / `declined` / `withdrawn`. Keep closed items in
a separate "Closed" table at the bottom with outcome and amount.

## Behaviors

**Status report.** When asked about the pipeline, read the tracker and
report: items due in the next 30 days (sorted by deadline, with days
remaining), items stuck without movement, and totals (requested vs.
awarded year-to-date, win rate on decided applications). Flag any
`preparing` item whose deadline is inside the review buffer (5 days) and
has not been through grant-review.

**Updates.** On any status change, update the row, date-stamp it in Notes,
and set the next action. Other GrantForge skills call this behavior when
they move an application forward.

**On submission.** Record submission date, confirmation number, and
expected decision date if known. Set next action to the follow-up.

**On decision.** Record award or decline, amount, and any reviewer
feedback the funder provided — save feedback verbatim into the grant's
workspace folder. Then run the harvest: identify the strongest sections of
the application (or, on a decline, what reviewer feedback says to fix) and
offer to update `profile/boilerplate/` and the org profile's track-record
section. Wins get added to the track record immediately.

**Recurring check.** Offer to schedule a weekly pipeline check that
reports upcoming deadlines and stalled items.
