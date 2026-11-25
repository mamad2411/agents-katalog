---
name: pagerduty-opsgenie-configuration-validation
description: >
  Validates PagerDuty and Opsgenie escalation policy and schedule
  configuration for coverage gaps and single points of failure before an
  incident exposes them — checking that every rung resolves to a
  genuinely independent human, that schedules have no unstaffed windows,
  and that num_loops/repeat settings actually repeat. Use when the user
  asks to "audit our escalation policies," "check if our on-call
  schedule has gaps," "make sure this policy isn't a single point of
  failure," "test our PagerDuty/Opsgenie configuration before relying on
  it," or after any roster/schedule change to confirm coverage still
  holds.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: incident-tooling-and-itsm
  maturity: stable
---

# PagerDuty/Opsgenie Configuration Validation

## Purpose

An escalation policy that looks correct in the console — three rungs,
reasonable timeouts — can still be a single point of failure if rung 2
resolves to the same one person as rung 1, or a schedule can have a
silent gap where no layer is active for a specific week because a
rotation's end date was never extended. These defects are invisible
until the exact moment they matter: a real page that nobody receives.
This skill covers systematically validating PagerDuty/Opsgenie
escalation policies and schedules — for coverage gaps, single points of
failure, and structurally broken repeat/timeout settings — as a
recurring check, not a one-time read-through. It assumes the
configuration already exists (see
[pagerduty-and-opsgenie-oncall-configuration](../pagerduty-and-opsgenie-oncall-configuration/SKILL.md)
for how to build it); this skill is strictly about proving it's correct
before an incident is the first time anyone finds out otherwise.

## When to use

- Before relying on a newly created escalation policy or schedule in
  production — validate it the same day it's created, not after the
  first real page.
- After any roster change (someone joins/leaves the rotation, a schedule
  layer's end date passes) to confirm coverage still holds — schedules
  silently degrade over time as end dates lapse or people leave without
  being removed from every layer they were on.
- Periodically (e.g. monthly, alongside the on-call load review in
  [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md))
  as a standing audit, not only reactively.
- Investigating "why didn't anyone get paged" after an incident, to
  determine whether the escalation policy itself had a structural gap
  versus a one-off human/tooling failure.
- Before a major reorg, team split, or on-call tool migration
  (PagerDuty ↔ Opsgenie) that touches many escalation policies at once.

## Prerequisites & environment

- Read access to the PagerDuty/Opsgenie API (`${PAGERDUTY_API_TOKEN}` /
  `${OPSGENIE_API_KEY}`) to pull escalation policies, schedules, and
  their resolved on-call membership — validation needs the *resolved*
  membership (who a schedule actually points to right now and for the
  next N weeks), not just the policy's static JSON.
- Python 3.9+ if using the reference script in `scripts/` — no
  third-party dependencies required for the coverage-logic check itself
  (add `requests` only if wiring it directly to the live API rather than
  exported JSON).
- A place to run this on a schedule (CI cron job, a scheduled Lambda/
  Cloud Function, or a cron on an ops host) so it's a recurring audit,
  not a manual one-off.
- Familiarity with the escalation policy/schedule structures being
  validated — see
  [pagerduty-and-opsgenie-oncall-configuration](../pagerduty-and-opsgenie-oncall-configuration/SKILL.md)
  for the shape of the JSON/Terraform this skill checks.

## Step-by-step guidance

1. **Pull the resolved configuration, not just the static policy.** A
   schedule's `escalation_rules` reference a `schedule_reference`, but
   the actual humans on call rotate weekly — resolve each schedule
   target to its current (and near-future) on-call user(s) via
   `GET /schedules/{id}/users?since=...&until=...` (PagerDuty) or
   `GET /v2/schedules/{id}/on-calls` (Opsgenie) before checking coverage,
   so the check reflects who's actually reachable this week, not an
   abstract schedule definition.

2. **Check every escalation rung resolves to at least one target.** A
   rung whose target was a user who left the company, or a schedule that
   was deleted, silently resolves to nothing — the escalation "moves on"
   to the next rung instantly with no page sent at all.

3. **Check that at least two rungs resolve to genuinely distinct
   humans.** The core single-point-of-failure check: flatten every
   rung's resolved user set and confirm the union has ≥2 distinct
   people, and that at least one later rung introduces someone *not*
   already covered by an earlier rung. A policy with rung 1 = "Alice"
   and rung 2 = "Alice" (via a schedule that also resolves to Alice this
   week) is not actually redundant just because it has two rungs.

4. **Check `num_loops`/repeat behavior is non-zero** for any policy
   backing a service that can page overnight or on weekends — a policy
   with no repeat silently gives up after running through its rungs once
   if nobody acknowledges, leaving the incident open and unescalated
   with no further notification.

5. **Check schedule layers for date-range gaps.** Query the resolved
   on-call user for every day in the next 4-6 weeks
   (`GET /schedules/{id}/users?since=<today>&until=<+6w>`); any day
   returning zero on-call users is a hard gap — often caused by a
   rotation's `rotation_turn_length_seconds`/end date lapsing, or an
   override that was added but never removed and now blocks the
   underlying layer from ever resuming.

6. **Check for stale overrides and expired maintenance windows** left
   active past their intended end — an override that was meant to cover
   one person's PTO week but was never removed continues silently
   routing pages to whoever covered for them, long after that person is
   back and unaware they're still officially "on call" for someone else.

7. **Run the reference script** (`scripts/check_escalation_coverage.py`)
   against exported policy JSON as a concrete starting point for either
   a CI gate or a scheduled audit job:
   ```bash
   python3 scripts/check_escalation_coverage.py payments-escalation.json
   ```
   Adapt `load_policy()` in the script to call the live PagerDuty/
   Opsgenie API directly rather than reading a static export, once this
   is wired into a recurring job.

8. **Report findings back into a place people will actually see them** —
   post failures to the team's ops channel or open a ticket, don't let a
   validation job run silently and log to a file nobody reads. This is a
   natural place to route findings into
   [chatops-runbook-automation](../chatops-runbook-automation/SKILL.md)'s
   incident-channel bot as a scheduled notification, or into
   [servicenow-itsm-integration](../servicenow-itsm-integration/SKILL.md)
   as a tracked problem-record if the org runs ITSM change control over
   on-call configuration.

## Best practices

- Validate against the *resolved* on-call schedule (who's actually on
  call this week and next), not just the static escalation policy JSON
  — a policy can be structurally fine while a specific week's rotation
  assignment is broken.
- Run this validation on every escalation policy/schedule change via CI
  (a merge to the Terraform config that manages them), not only on a
  periodic cadence — catch a newly introduced gap before it merges.
- Treat "only one distinct human reachable across the whole policy" as
  a hard failure, not a warning — this is the exact condition that turns
  an on-call system into theater.
- Check 4-6 weeks forward for schedule gaps, not just the current week —
  a rotation's end date lapsing three weeks out is invisible today but
  will be a real gap when that week arrives.
- Keep the check itself simple and dependency-light (see the reference
  script) so it's easy to run in any CI system or scheduled job, rather
  than depending on a heavyweight framework.
- Re-validate after org changes that don't touch the escalation policy
  directly but change who's *in* it — a team reorg, someone's role
  change, or an employee departure.

## Common pitfalls

- **Symptom:** An escalation policy has three rungs configured, and it
  looks properly redundant in the console — but during a real incident,
  all three rungs paged the same one person because two of the three
  targets were schedules that both currently resolve to them.
  **Fix:** Validate resolved membership, not rung count — flatten every
  rung's actual on-call user(s) for the current period and confirm the
  union includes at least two distinct people, using the check in step 3
  (and the reference script) rather than eyeballing the policy structure.

- **Symptom:** A schedule was set up with a rotation that has an implicit
  end (e.g. a fixed number of turns configured months ago), and three
  months later a specific week has zero on-call coverage — nobody
  notices until a page during that week goes unanswered.
  **Fix:** Proactively query resolved on-call coverage 4-6 weeks forward
  on a recurring basis (step 5) and alert on any day with zero on-call
  users, rather than discovering the gap only when an incident falls
  into it.

- **Symptom:** An engineer's PTO override was added to cover one week,
  but was never removed — months later, pages meant for the original
  rotation member are still silently routed to the PTO-covering
  colleague, who has long since stopped expecting them.
  **Fix:** Audit overrides for ones past their intended end date on the
  same cadence as the rest of the validation, and require overrides to
  always be created with an explicit end time rather than open-ended.

- **Symptom:** `num_loops` on a production escalation policy is left at
  its default (no repeat); an unacknowledged Sev1 page runs through all
  rungs once, reaches the final rung's target, and then simply stops
  with the incident still unacknowledged and no further notification.
  **Fix:** Explicitly set `num_loops >= 1` (or Opsgenie's equivalent
  repeat setting) for any policy backing a service capable of paging
  outside business hours, and include this as a checked condition (step
  4) rather than trusting the default.

## Worked example

**Scenario:** A monthly audit job validates all escalation policies for
the `payments` and `checkout` teams before the on-call load review.

Exported policy for `checkout-team-escalation` (resolved schedule
membership already expanded for the current week):

```json
{
  "name": "checkout-team-escalation",
  "num_loops": 1,
  "escalation_rules": [
    {
      "targets": [
        { "type": "schedule_reference", "id": "SCHED-CHECKOUT-PRI", "members": ["U-FRANK"] }
      ]
    },
    {
      "targets": [
        { "type": "schedule_reference", "id": "SCHED-CHECKOUT-SEC", "members": ["U-FRANK"] }
      ]
    },
    {
      "targets": [
        { "type": "user_reference", "id": "U-MANAGER-GRACE" }
      ]
    }
  ]
}
```

Running the reference script:

```bash
python3 scripts/check_escalation_coverage.py checkout-team-escalation.json
```

Output:

```
FAIL  checkout-team-escalation.json
  - checkout-team-escalation: rung 2 adds no new humans beyond earlier rungs (['U-FRANK']) — escalation would loop back to the same person/people instead of reaching someone new.
```

Investigation shows `SCHED-CHECKOUT-SEC` (the "secondary" schedule) was
created by copying the primary schedule's layer as a starting template
during setup, and the second rotation member was never actually swapped
in — the secondary schedule silently resolves to the same person as
primary for the current week. The fix: correct the secondary schedule's
membership to a genuinely different rotation, re-run the script to
confirm it now passes, and add this check as a required CI step whenever
`checkout-team-escalation`'s Terraform definition changes.

## Cross-references

- [pagerduty-and-opsgenie-oncall-configuration](../pagerduty-and-opsgenie-oncall-configuration/SKILL.md) — how the escalation policies and schedules validated here are actually built and configured.
- [servicenow-itsm-configuration-validation](../servicenow-itsm-configuration-validation/SKILL.md) — the same "validate before it blocks or misroutes a real incident" discipline applied to ServiceNow workflow/approval configuration.
- [chatops-runbook-automation](../chatops-runbook-automation/SKILL.md) — a natural destination for this validation's findings (a scheduled bot post to the ops channel) and for the audit job itself to be triggered from.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) — the on-call load review and escalation-timeout SLAs this validation should be run alongside.
