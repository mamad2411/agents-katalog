---
name: operational-runbook-execution-and-escalation
description: >
  Guides junior/entry-level engineering work: executing pre-approved
  runbooks and established deployment procedures exactly as documented,
  first-response alert triage (acknowledge, assess severity, apply the
  documented fix or escalate), and knowing the explicit criteria for when
  to stop and hand off rather than improvise a fix beyond the runbook's
  scope. Covers building judgment over time by logging deviations from
  the runbook for review rather than silently freelancing a workaround.
  Use when a junior/entry-level engineer (or an agent acting as one) is
  first-responder on an alert, is asked to "follow the runbook for X,"
  needs to decide "should I escalate this or keep trying," is running a
  documented deployment/rollback procedure, or is writing up a runbook
  deviation after an on-call shift.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: role-based-engineering-practices
  maturity: stable
---

# Operational Runbook Execution and Escalation

## Purpose

At entry level, the highest-leverage skill isn't clever improvisation
under pressure — it's disciplined execution of a documented procedure and
knowing precisely when to stop and hand off rather than push past the
edge of that documentation. A junior engineer who deviates from a runbook
mid-incident because a step "looks wrong" or a fix "seems obvious" is
making a judgment call without the system context (blast radius, prior
outages, why the runbook says what it says) that would let a senior
engineer make that same call safely. This skill covers executing
runbooks and deployment procedures exactly as written, triaging alerts
methodically (acknowledge, assess severity, apply the documented fix or
escalate), recognizing the explicit escalation criteria a runbook should
define, and treating every deviation — successful or not — as material to
document rather than a private workaround, since that documentation is
what turns runbook-following into real operational judgment over time.

## When to use

- You are the first responder on a paged alert and need to identify,
  read, and execute the correct runbook rather than debug from scratch.
- You are running an established deployment, rollback, or maintenance
  procedure (e.g. a documented database failover, a certificate renewal,
  a scaling procedure) that already has a written, approved runbook.
- A runbook step doesn't produce the expected result, or the situation
  doesn't match what the runbook describes, and you need to decide
  whether to keep going, try something adjacent, or escalate.
- You've just finished (or handed off) a runbook execution and need to
  document what actually happened, including any deviation from the
  written steps, before closing the ticket.
- You are new to an on-call rotation and need a concrete model for what
  "doing the job well" looks like at this level, as distinct from the
  independent design/RCA work covered at the next level in
  [independent-solution-design-and-technical-review](../independent-solution-design-and-technical-review/SKILL.md).

## Prerequisites & environment

- Read access to the team's runbook repository/wiki, mapped from alert
  name/tag to the specific runbook (e.g. an alert's annotation links
  directly to its runbook URL — if it doesn't, that gap itself is worth
  flagging, not silently working around).
- Access to the paging tool (PagerDuty, Opsgenie, Grafana OnCall, or
  equivalent) to acknowledge alerts and see the on-call escalation chain
  — see
  [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md)
  for how severity levels and escalation timeouts are defined at the
  program level; this skill covers executing within that structure as the
  first responder.
- Read access to the relevant logs/dashboards/metrics the runbook
  references for verification steps.
- Scoped, least-privilege access to perform *only* the actions the
  runbook documents (e.g. restart a specific service, run a specific
  script) — not blanket production admin access "just in case." If a
  runbook step requires access you don't have, that is itself an
  escalation trigger, not a reason to find a workaround with broader
  credentials.
- A known, current escalation path: who is secondary on-call, what their
  timeout is, and how to reach them (page, phone, chat) if the primary
  channel doesn't get a response.
- A place to log deviations and post-shift notes (a ticket, a shared
  on-call log, a runbook-feedback channel) that a runbook owner actually
  reviews — logging into a void that nobody reads defeats the purpose.

## Step-by-step guidance

1. **Acknowledge the alert immediately** in the paging tool, before doing
   anything else — an unacknowledged page that later escalates to a
   colleague when you were in fact already responding wastes their time
   and muddies the incident record.

2. **Identify the correct runbook from the alert itself**, not from
   memory or a guess at what's probably wrong. Most well-instrumented
   alerts link directly to a runbook URL in their annotation/description;
   if this one doesn't, say so explicitly when you escalate or write up
   the shift rather than proceeding on assumption.

3. **Assess severity using the runbook's/team's documented triage
   criteria**, not personal judgment made under pressure. A runbook
   should tell you what to check to classify severity (customer impact,
   error rate threshold, which systems are affected) and what severity
   implies for urgency and further paging — see the severity-level
   framing in
   [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md).

4. **Execute the runbook's steps in order, verifying after each one**,
   rather than running several actions back-to-back and checking once at
   the end — if step 3 doesn't produce the stated expected result, that
   is information you need before deciding whether step 4 is still safe
   to run.

   Example runbook excerpt (`runbooks/payments-api-high-memory.md`):
   ```markdown
   # Runbook: payments-api high memory usage alert

   ## Trigger
   Alert `payments-api-memory-p95-high` fires when container memory
   usage exceeds 85% for 10 minutes.

   ## Severity
   Sev3 by default (no customer impact yet). Escalate to Sev2 immediately
   if error rate also exceeds 1% (check the `payments-api` Grafana
   dashboard, "Error Rate" panel).

   ## Steps
   1. Confirm the alert is real: check the "Memory Usage" panel on the
      `payments-api` Grafana dashboard. Expected: sustained >85% for the
      affected pod(s).
   2. Check for a recent deploy: `kubectl rollout history deployment/payments-api -n payments`.
      If a deploy occurred in the last 2 hours, STOP here and escalate
      per the "Escalation triggers" section below — do not proceed to
      step 3. A memory regression tied to a recent deploy needs the
      deploying engineer or a senior engineer, not a restart.
   3. If no recent deploy, restart the affected pod:
      `kubectl delete pod <pod-name> -n payments` (the Deployment will
      recreate it — this is a documented, approved action for this
      alert, not an ad hoc restart).
   4. Verify: memory usage on the new pod stays under 70% for 15 minutes
      and the "Error Rate" panel shows no change.
   5. If memory climbs back above 85% within 1 hour of the restart, STOP
      — this is recurring, not a one-off blip. Escalate per below.

   ## Escalation triggers (stop and hand off, do not improvise past this point)
   - A recent deploy correlates with the alert (step 2).
   - The problem recurs within 1 hour of the documented fix (step 5).
   - Error rate crosses 1% at any point (reclassify Sev2, page secondary
     on-call immediately per the on-call escalation policy).
   - Any step's actual result doesn't match its "expected" description.

   ## Escalation contact
   Secondary on-call via PagerDuty schedule `payments-secondary-oncall`.
   ```

5. **Treat the runbook's escalation triggers as hard stops, not
   suggestions.** If you hit one, escalate — do not attempt an adjacent
   fix that isn't in the document, even if you have a hunch it would
   work. The runbook's escalation point exists specifically because
   someone with more context decided this is where judgment calls need
   more information than a first responder has by design.

6. **Escalate with a structured handoff**, not a vague "it's still
   broken": state what alert fired, what runbook you followed, exactly
   which step you're stopped at and why, what you observed at each prior
   step, and current system state. A senior engineer picking this up
   should not have to re-derive what you already know.

7. **After resolution or handoff, log any deviation from the written
   runbook** — a step that didn't match reality, an escalation trigger
   that fired, a step whose instructions were ambiguous — in the shift
   log or a ticket, even if you worked around it successfully in the
   moment. This is what lets the runbook owner fix the document instead
   of the same ambiguity tripping up the next first responder too.

## Best practices

- Treat the runbook as ground truth for the duration of the incident,
  even if you believe you know a faster or better way — propose the
  improvement afterward, as a documented change to the runbook, not as a
  live improvisation during an active page.
- Timebox each step mentally before you start it (the runbook's stated
  timeout, or a sane default if none is given) so a hung step becomes a
  decision point rather than something you sit and wait on indefinitely.
- Verify after every step, not just at the end — cheap, frequent
  verification catches a step that silently didn't do what you expected
  long before it compounds into a bigger problem.
- Escalate early rather than late. Escalating a problem that turns out to
  be simple costs a few minutes of a senior engineer's time; sitting on a
  problem past the documented escalation trigger while you keep trying
  costs much more once it's finally handed off in a worse state.
- When a runbook step is ambiguous, out of date, or simply wrong, say so
  explicitly in the incident record and follow up with a ticket to fix
  the runbook — don't silently "figure it out" and leave the document
  wrong for the next person.
- Keep a personal (or team) log of every runbook you've executed and
  every deviation you noted — reviewing that log periodically is how
  judgment about *why* the runbook says what it says actually builds over
  time, ahead of eventually working more independently as covered in
  [independent-solution-design-and-technical-review](../independent-solution-design-and-technical-review/SKILL.md).

## Common pitfalls

- **Symptom:** A runbook step's escalation trigger is met (e.g. "a recent
  deploy correlates with the alert — stop and escalate"), but the
  responder feels confident and tries an unlisted fix instead of
  escalating.
  **Fix:** This is a genuinely risky pitfall, not a minor process
  miss — improvising past a documented escalation point removes the
  safety margin the runbook's author built in deliberately, often based
  on a prior incident where exactly this improvisation made things
  worse. Escalate at the trigger every time, regardless of how confident
  the fix feels in the moment; note the idea in the handoff so the
  escalated engineer can evaluate it with full context instead of it
  being tried blind.

- **Symptom:** A runbook step's "expected result" clearly doesn't match
  what's actually observed, but the responder proceeds to the next step
  anyway on the assumption it'll probably be fine.
  **Fix:** Stop at the first mismatch between expected and actual result
  and treat it as an implicit escalation trigger even if the runbook
  doesn't name that exact case — a runbook's steps are usually written
  assuming each prior step succeeded as documented; proceeding on an
  unverified assumption compounds the uncertainty with each subsequent
  step.

- **Symptom:** An alert fires at 2am, the assigned runbook is two
  versions out of date and references a service that was renamed six
  months ago, and the responder spends 40 minutes trying to reconcile it
  before finally escalating.
  **Fix:** If the runbook clearly doesn't match current reality within
  the first few minutes, escalate immediately and flag the runbook as
  stale in the same message — don't burn the acute incident window
  trying to privately reverse-engineer a broken document; fixing the
  document is separate, follow-up work.

- **Symptom:** A responder performs an action that isn't in the runbook
  at all — for example, restarting a production database, force-deleting
  a stuck Kubernetes resource, or manually editing data — because it
  "should" fix the symptom, without any documented approval for that
  specific action.
  **Fix:** This is a destructive-action risk, not routine
  troubleshooting: any action with a real risk of data loss or wider
  outage that isn't explicitly documented and approved in the runbook is
  outside a first responder's authorized scope. Escalate instead, and if
  a genuinely useful undocumented action gets approved by whoever you
  escalate to, get it added to the runbook afterward so it's a documented
  step next time, not a one-off judgment call repeated informally.

- **Symptom:** A shift ends, the ticket is closed as resolved, and no
  note is made that step 3 of the runbook actually failed the first time
  and had to be retried — three weeks later, the next responder hits the
  identical failure and has no idea it happened before.
  **Fix:** Log every deviation, even ones that resolved themselves on
  retry, in the shift log or ticket before closing — a runbook owner who
  never sees these reports has no signal that the document needs
  updating, and the same friction repeats for every future first
  responder.

## Worked example

**Scenario:** At 03:14 UTC, alert `checkout-api-error-rate-high` pages
the on-call rotation for a junior engineer's first solo overnight shift.

1. **Acknowledge** the page in PagerDuty within 90 seconds.
2. **Find the runbook** via the alert's linked
   `runbooks/checkout-api-error-rate.md` — it exists and looks current.
3. **Assess severity**: the runbook's triage step says check the "5xx
   rate" panel; it's at 4%, above the runbook's documented 2% Sev2
   threshold — classify Sev2 and note it in the incident channel per the
   severity table in
   [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md).
4. **Execute step 1**: check for a recent deploy — none in the last 6
   hours. Proceed.
5. **Execute step 2**: restart the two flagged pods per the documented
   command. Verify per step 3: 5xx rate drops to 0.3% within 5 minutes,
   matching the runbook's "expected" description. Looks resolved.
6. **Execute step 4 (final verification)**: hold for 15 minutes as
   instructed. At minute 12, the 5xx rate climbs back to 3.8%.
7. **This matches an explicit escalation trigger** ("recurs within 30
   minutes of the fix") — the engineer does not attempt a second restart
   or try anything else. They page secondary on-call with a structured
   handoff: alert name, runbook followed, steps 1-4 completed with
   results, the recurrence at minute 12, and current 5xx rate.
8. Secondary on-call (a senior engineer) picks it up, and — because this
   didn't have a documented fix beyond the runbook's scope — proceeds
   under
   [independent-solution-design-and-technical-review](../independent-solution-design-and-technical-review/SKILL.md)'s
   root-cause process rather than the runbook.
9. **After stand-down**, the junior engineer logs the deviation in the
   incident ticket: "runbook's restart step resolved symptoms for ~12
   minutes before recurrence; escalated per the recurrence trigger;
   root cause was a connection-pool leak not covered by this runbook."
   This note becomes the seed of a runbook update once the senior
   engineer's root-cause fix (see cross-reference) is confirmed.

## Cross-references

- [independent-solution-design-and-technical-review](../independent-solution-design-and-technical-review/SKILL.md) — the next level of practice: what happens once an issue is escalated past a runbook's scope, including root-cause analysis on incidents with no existing runbook.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) — the severity levels, paging behavior, and escalation timeouts this skill's triage and escalation steps operate within.
- [blameless-postmortem-and-root-cause-analysis](../../../site-reliability-engineering/skills/blameless-postmortem-and-root-cause-analysis/SKILL.md) — where a logged runbook deviation or a recurring escalation trigger typically ends up feeding a formal postmortem's action items.
- [pipeline-failure-triage-and-recovery](../../../devops/skills/pipeline-failure-triage-and-recovery/SKILL.md) — the equivalent first-response triage discipline (classify before acting, narrowest safe recovery action) applied specifically to a failed CI/CD pipeline run rather than a production alert.
