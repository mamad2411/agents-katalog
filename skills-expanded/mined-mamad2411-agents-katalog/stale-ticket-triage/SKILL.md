---
name: stale-ticket-triage
description: Replace the weekly "look at every ticket older than X days" meeting with a scheduled AI scan that picks close / snooze / keep per ticket plus a one-sentence reason, so a PM can bulk-approve in 90 seconds Monday morning.
tags: [project-management, jira, azure-devops, backlog-grooming, ai-agent]
publisher: agena
---

# Stale Ticket Triage

Backlogs accumulate dead rows. Most teams have a recurring Friday meeting
where someone walks every ticket older than X days and decides whether to
close, snooze, or keep it. That hour is the perfect AI workload — the
decision is shallow but the volume is high.

## How to apply this pattern

1. **Define stale**: a ticket is stale when its `updated_at` is older than
   the org's threshold (default 30 days) AND its status is still in the
   active set (not Closed / Done / Cancelled).

2. **Schedule the scan** (chip-pick: every 6h / 12h / daily 9am / weekly
   Sundays / monthly). Each run hits the source-platform API for every
   project the org cares about, lists stale issues, and sends each
   through a short LLM call.

3. **System prompt the LLM with three explicit verdicts** —
   `close` / `snooze` / `keep` — plus a one-sentence reason. Be
   conservative on `close`: only pick it when the ticket itself signals
   resolution (links a merged PR, mentions a follow-up). Default to
   `snooze` when unsure; never `close` from silence alone.

4. **Persist each verdict** as a triage decision row keyed by
   `(org, source, external_id)` so re-runs are idempotent. Status
   transitions: `pending` → `applied` / `skipped` / `overridden`.

5. **One-click bulk approve** in the UI: the human reviews the AI verdicts
   in a list, hits "Apply all AI suggestions", and the system writes back
   to Jira / Azure DevOps in a single batch.

## Example LLM reply format

```
VERDICT: close
REASON: Closed by PR #4221 (merged 38 days ago); customer hasn't
        responded since the fix shipped.
```

```
VERDICT: snooze
REASON: Still relevant but no recent customer activity; revisit when
        the related epic resumes.
```

## Notes

- **Audit trail is non-negotiable.** Every AI verdict and every human
  override needs a row with timestamp + user id. Bulk-approve must not
  destroy history; it appends.
- **Source-side scan** (read tickets directly from Jira / Azure DevOps)
  scales better than relying on imported task records, because most
  stale tickets were never imported into the AI tool.
- **Threshold is per-workspace.** Solo product teams might want 14 days;
  enterprise backlogs need 60-90.
- The verdict prompt is short on purpose — long prompts encourage the
  model to add commentary and skip the structured reply.
- Pair with **reporter-routing rules** so security tickets bypass the
  triage flow entirely — those should never be auto-closed.
