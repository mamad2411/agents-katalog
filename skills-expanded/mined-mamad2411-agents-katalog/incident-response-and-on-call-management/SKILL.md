---
name: incident-response-and-on-call-management
description: >
  Guides designing incident response structure and on-call operations —
  Incident Command System roles (Incident Commander, Communications
  Lead, Operations/Tech Lead, Scribe), severity/priority levels and the
  paging behavior each implies, on-call rotation design (primary/
  secondary escalation, follow-the-sun handoffs), and on-call health
  (alert fatigue, fair page load distribution). Use when a user asks to
  "set up an incident command process", "define severity levels and who
  gets paged", "design an on-call rotation/escalation policy", "reduce
  alert fatigue for on-call", or "our on-call rotation is burning people
  out."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: site-reliability-engineering
  maturity: stable
---

# Incident Response and On-Call Management

## Purpose

An outage doesn't become a well-handled incident just because someone
gets paged — without predefined roles, severity levels, and an
escalation policy, the first ten minutes of a real incident are spent
figuring out who's in charge, whether this is bad enough to wake anyone
else up, and who's supposed to be telling customers/leadership what's
happening, while the actual fix waits. This skill covers structuring
incident response around a lightweight Incident Command System (ICS) so
technical work and coordination don't compete for the same person's
attention, defining severity levels with an explicit paging outcome for
each, designing on-call rotations (including follow-the-sun for global
teams) with real escalation timeouts, and tracking on-call health so the
rotation doesn't quietly burn out whoever happens to get paged the most.

## When to use

- Standing up (or fixing) an incident response process from scratch —
  no clear roles, or the same person always ends up doing everything.
- Defining severity/priority levels so paging behavior is consistent
  instead of "sometimes we page everyone, sometimes nobody."
- Designing or revising an on-call rotation: primary/secondary structure,
  escalation timeouts, follow-the-sun handoffs across regions/time zones.
- On-call is causing burnout or attrition — too many pages, uneven
  distribution across the team, or frequent off-hours pages for
  non-urgent issues.
- A recent incident revealed confusion about who could declare an
  incident, who had authority to make a mitigation call, or who was
  supposed to update customers/status pages.

## Prerequisites & environment

- A paging/on-call tool (PagerDuty, Opsgenie, Grafana OnCall, or
  equivalent) with escalation policies configurable per team/service.
- Alerting already wired from the monitoring stack into that paging tool
  — see
  [Prometheus and Grafana monitoring stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  for Alertmanager routing mechanics, and
  [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md)
  for burn-rate alerts that should be a primary paging source.
- A dedicated incident communication channel pattern (e.g. a Slack/Teams
  bot that spins up a fresh `#incident-<id>` channel plus a bridge/call
  line per declared incident) and, for customer-facing services, a
  status-page tool.
- Clarity on who is authorized to declare an incident (should be *any*
  engineer, not gated behind a manager) and a low-friction way to do it
  (a slash command or a single button, not a multi-step form).

## Step-by-step guidance

1. **Define severity levels with an explicit paging outcome for each** —
   severity should be decided in seconds during an incident, not debated:

   | Severity | Definition | Paging behavior | Comms cadence |
   |---|---|---|---|
   | Sev1 | Full outage or critical data-integrity risk, affects all/most customers | Page primary + secondary immediately; IC assigned within 5 min | Status page update within 15 min, updates every 30 min |
   | Sev2 | Significant partial degradation (one region, one major feature) | Page primary on-call | Internal updates every 30-60 min; customer comms if customer-visible |
   | Sev3 | Minor degradation, workaround exists, no broad customer impact | Ticket during business hours, no page | Internal only, as needed |
   | Sev4 | Cosmetic/minor, no functional impact | Ticket, backlog priority | None required |

   Encode this table directly in the paging tool's routing rules so it's
   enforced automatically, not left to judgment calls under pressure.

2. **Assign Incident Command System roles** — for anything Sev1/Sev2,
   split coordination from execution:
   - **Incident Commander (IC):** owns the incident overall — decides
     severity, decides when to escalate/de-escalate, keeps the incident
     moving, is *not* necessarily the person fixing the issue. Trained
     and rostered separately from the technical on-call rotation so the
     IC role doesn't default to "whoever is most senior and now also
     stuck doing everything."
   - **Operations/Tech Lead:** drives the technical investigation and
     mitigation (rollback, failover, config change).
   - **Communications Lead:** owns stakeholder updates — status page,
     internal leadership, customer support — so the Tech Lead isn't
     interrupted every ten minutes for a status update.
   - **Scribe:** logs the timeline in real time (timestamps, actions
     taken, decisions made) directly into the incident channel/doc —
     this becomes the raw material for the postmortem (see
     [blameless-postmortem-and-root-cause-analysis](../blameless-postmortem-and-root-cause-analysis/SKILL.md)).
   For a small team, one person may hold Comms + Scribe, but IC and Tech
   Lead should be different people whenever more than one responder is
   available.

3. **Design the on-call rotation:**
   - **Primary + secondary** structure: primary is paged first;
     secondary is paged automatically if primary doesn't acknowledge
     within a fixed timeout.
   - **Escalation timeout example:** acknowledge within 5 minutes, or
     auto-escalate to secondary; secondary has 10 minutes, or escalate to
     the team's engineering manager.
   - **Rotation length:** weekly is generally preferable to daily —
     shorter rotations increase context-switching overhead per handoff;
     longer than two weeks increases fatigue and reduces the team's
     collective on-call experience.
   - **Follow-the-sun** (for globally distributed teams): hand off
     primary responsibility at region/business-hours boundaries rather
     than paging someone at 3am when a colleague in another time zone is
     awake. Require a structured handoff (see Best practices) at every
     boundary — an implicit handoff means the next region starts an
     active incident blind.

4. **Encode the escalation policy in the paging tool.** Example
   (PagerDuty-style, values illustrative):
   ```yaml
   escalation_policy:
     name: payments-team-escalation
     escalation_rules:
       - escalation_delay_minutes: 5
         targets:
           - schedule: payments-primary-oncall
       - escalation_delay_minutes: 10
         targets:
           - schedule: payments-secondary-oncall
       - escalation_delay_minutes: 15
         targets:
           - user: payments-eng-manager
   ```

5. **Run the incident end to end:** declare → assemble roles per
   severity → mitigate (often a fast rollback or traffic shift — see
   [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md)
   for the mechanics) → confirm steady state restored against the
   service's SLO dashboards → explicit stand-down/all-clear → hand the
   scribe's timeline to the postmortem process within 48-72 hours.

6. **Monitor on-call health continuously**, not just after someone
   complains:
   - Track pages-per-person per rotation and flag imbalance (e.g. one
     engineer receiving 3x the team average).
   - Track off-hours pages and time-to-acknowledge as leading indicators
     of fatigue.
   - Run a recurring (e.g. monthly) on-call load review; noisy/low-value
     alerts identified there should be tuned or retired — see
     [toil-reduction-and-operational-automation](../toil-reduction-and-operational-automation/SKILL.md)
     for prioritizing which alerts/manual tasks to fix versus tolerate.

## Best practices

- Keep IC and hands-on-fixer as different people for Sev1/Sev2 whenever
  staffing allows — a single person trying to both coordinate and debug
  makes both worse.
- Use a fresh, dedicated channel per incident (not the team's standing
  channel) so the timeline is self-contained and easy to hand to the
  postmortem.
- Require a structured handoff at every follow-the-sun boundary: open
  incidents, active mitigations in flight, who owns what, and what's
  explicitly *not* yet resolved.
- Make severity determination mechanical (tied to customer impact
  criteria in the table), not a judgment call made under stress by
  whoever happens to be paged.
- Declare "stand-down" explicitly, with a stated reason (fix verified /
  root cause mitigated / workaround holding) — don't let incidents fade
  out ambiguously.
- If an incident's root cause involves a compromised dependency, leaked
  credential, or a bypassed security gate, loop in the security incident
  path alongside the normal IC structure — see
  [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md)
  for the pipeline-gate context a security-flavored incident usually
  needs to reference (what gate should have caught this, and why didn't
  it block).
- Review on-call load data on a fixed cadence, not only reactively after
  someone burns out or quits.

## Common pitfalls

- **Symptom:** During a Sev1, the on-call engineer is simultaneously
  trying to debug the root cause, post status updates, and answer
  Slack questions from five different people — nothing moves fast.
  **Fix:** Split IC/Comms/Tech Lead roles even with a small team; pull in
  secondary on-call or a manager to take the Comms role immediately
  rather than letting one person do everything.

- **Symptom:** A Sev1 page goes unacknowledged for 40 minutes before
  anyone notices no one responded.
  **Fix:** No escalation timeout was configured (or it silently failed).
  Set an explicit ack SLA (e.g. 5 minutes) with automatic escalation to
  secondary, then to a manager, and test the escalation policy
  periodically like the rest of the alerting stack.

- **Symptom:** One engineer on the rotation receives noticeably more
  pages than everyone else, month over month, and is showing signs of
  burnout.
  **Fix:** No one is tracking pages-per-person. Instrument the paging
  tool's reporting, review load distribution monthly, and rebalance the
  rotation (or fix the underlying noisy alerts — often the same alerts
  every time) rather than treating it as bad luck.

- **Symptom:** A follow-the-sun handoff happens with a one-line "all
  good, nothing going on" message, then the next region discovers an
  active, unresolved incident an hour into their shift.
  **Fix:** Require a structured handoff template (open incidents, active
  mitigations, explicit owner, known unknowns) at every boundary — an
  implicit "all good" is not a handoff.

- **Symptom:** Severity is decided ad hoc each time — the same kind of
  partial outage gets called Sev1 (paging the whole company) once and
  Sev3 (no page at all) another time.
  **Fix:** Encode severity criteria and their paging behavior directly
  into the routing rules of the paging tool (step 1's table), so the
  decision is mechanical rather than a fresh judgment call under
  pressure each time.

## Worked example

**Scenario:** `payments-api` checkout success rate drops sharply at
14:02 UTC.

1. The fast-burn SLO alert (from
   [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md))
   fires and pages `payments-primary-oncall` via the escalation policy in
   step 4.
2. Primary acknowledges within 3 minutes, declares the incident as
   **Sev1** per the severity table (checkout affects all customers), and
   a fresh `#incident-2026-0728-01` channel is created automatically.
3. A trained IC (not the paged on-call engineer, pulled from a separate
   IC rotation) takes command within 5 minutes; the paged engineer
   becomes Tech Lead; an available teammate takes Comms; the IC assigns
   Scribe duty to a fourth responder joining the bridge.
4. Comms posts an initial status-page update within 12 minutes ("We are
   investigating elevated checkout errors").
5. Tech Lead identifies a bad config in the latest deploy and executes a
   rollback (see
   [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md)),
   restoring the checkout success rate by 14:22 UTC.
6. IC confirms steady state against the SLO dashboard for 15 minutes,
   then declares stand-down at 14:40 UTC with the reason "rollback
   verified, error rate back within SLO."
7. The scribe's timeline is handed to the postmortem process (see
   cross-references) within 24 hours; the on-call load review that month
   notes this was the primary's second Sev1 page in the same week and
   flags the rotation for rebalancing.

## Cross-references

- [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md) — burn-rate alerts are the primary source of pages this skill's escalation policy responds to.
- [blameless-postmortem-and-root-cause-analysis](../blameless-postmortem-and-root-cause-analysis/SKILL.md) — the scribe's live timeline and the incident's severity/impact feed directly into the postmortem.
- [toil-reduction-and-operational-automation](../toil-reduction-and-operational-automation/SKILL.md) — chronic noisy/low-value pages found during on-call load reviews are toil to be automated or eliminated, not just tolerated.
- [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md) — rollback/traffic-shift mechanics commonly used as the mitigation step during an incident.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) — reference when an incident's root cause has a security angle (compromised dependency, bypassed pipeline gate) to reason about which gate should have caught it.
