---
name: pagerduty-and-opsgenie-oncall-configuration
description: >
  Configures on-call schedules, escalation policies, and alert routing/
  deduplication rules in PagerDuty and Opsgenie — the tool-specific API/
  Terraform configuration that implements an on-call rotation, not the
  generic on-call process design. Use when the user asks to "set up a
  PagerDuty schedule," "configure an Opsgenie escalation policy," "route
  alerts to the right team in PagerDuty," "add alert deduplication so we
  stop getting paged 50 times for one outage," "add a secondary on-call
  layer," or "configure a maintenance window/override in PagerDuty or
  Opsgenie."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: incident-tooling-and-itsm
  maturity: stable
---

# PagerDuty and Opsgenie On-Call Configuration

## Purpose

An on-call rotation is only as good as its configuration: a schedule with
a timezone mistake pages someone at 3am for a shift that was supposed to
start at 9am local; an escalation policy missing a second rung means an
unacknowledged page just... stops; and alert routing without
deduplication turns one noisy dependency into fifty pages for the same
outage, training responders to ignore their pager. This skill covers the
concrete PagerDuty and Opsgenie configuration — schedules, layers,
escalation policies, event orchestration/alert policies, deduplication
keys, and maintenance windows — that implements the on-call *process*.
The process itself (severity levels, Incident Command roles, rotation
length, follow-the-sun design) is covered in
[incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md);
this skill is where that design becomes an actual escalation policy JSON
payload or Terraform resource. Whether that configuration is *correct* —
no gaps, no single point of failure — is a separate concern covered in
[pagerduty-opsgenie-configuration-validation](../pagerduty-opsgenie-configuration-validation/SKILL.md).

## When to use

- Standing up a new on-call schedule (primary/secondary rotation) in
  PagerDuty or Opsgenie for a team or service that doesn't have one yet.
- Writing or editing an escalation policy — how many rungs, what timeout
  between them, who/what each rung pages.
- Routing alerts from a monitoring/alerting source (Prometheus
  Alertmanager, Datadog, CloudWatch) into the correct PagerDuty service
  or Opsgenie team, including severity-based routing.
- Configuring alert deduplication so a flapping check or a burst of
  correlated alerts from one root cause produces one incident, not one
  page per alert.
- Setting up a maintenance window/override so planned maintenance or a
  known ongoing issue doesn't page anyone unnecessarily.
- Migrating an escalation policy or schedule from one tool to the other
  (PagerDuty ↔ Opsgenie) and needing the equivalent concept mapped over.

## Prerequisites & environment

- A PagerDuty account with an API access token (`${PAGERDUTY_API_TOKEN}`)
  with `write` scope on schedules/escalation policies/services, or
  Opsgenie API key (`${OPSGENIE_API_KEY}`) with admin/configuration
  access — never hardcode either in a config file or script.
- Team/service structure already decided: which services page which
  team, and whether escalation policies are per-service or shared across
  a team's services.
- If managing configuration as code, the Terraform providers
  `pagerduty/pagerduty` or `opsgenie/opsgenie` (or direct REST calls) —
  Terraform is strongly preferred over console clicks so schedules and
  escalation policies are diffable and reviewable in a PR.
- Monitoring already producing alerts with enough metadata (a stable
  `dedup_key`/alias, severity, source service) to route and deduplicate
  on — see
  [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  for the Alertmanager side of getting that metadata into the alert
  payload in the first place.
- Decide the on-call process (severity levels, rotation length,
  follow-the-sun) *before* configuring the tool — see
  [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md).
  This skill implements that design; it doesn't design it from scratch.

## Step-by-step guidance

1. **Model the schedule as layers (PagerDuty) or rotations (Opsgenie).**
   PagerDuty layers stack — a base weekly rotation plus an override
   layer for holidays — and later layers take priority:
   ```json
   {
     "schedule": {
       "name": "payments-primary-oncall",
       "time_zone": "America/New_York",
       "schedule_layers": [
         {
           "name": "Weekly Rotation",
           "start": "2026-08-03T09:00:00-04:00",
           "rotation_virtual_start": "2026-08-03T09:00:00-04:00",
           "rotation_turn_length_seconds": 604800,
           "users": [
             { "user": { "id": "PXXXXX1", "type": "user_reference" } },
             { "user": { "id": "PXXXXX2", "type": "user_reference" } },
             { "user": { "id": "PXXXXX3", "type": "user_reference" } }
           ]
         }
       ]
     }
   }
   ```
   Opsgenie equivalent (a rotation inside a schedule):
   ```json
   {
     "name": "payments-primary-oncall",
     "timezone": "America/New_York",
     "rotations": [
       {
         "name": "weekly-rotation",
         "startDate": "2026-08-03T13:00:00Z",
         "type": "weekly",
         "participants": [
           { "type": "user", "id": "user-uuid-1" },
           { "type": "user", "id": "user-uuid-2" },
           { "type": "user", "id": "user-uuid-3" }
         ]
       }
     ]
   }
   ```
   Set `time_zone`/`timezone` explicitly to the team's actual timezone,
   not the account default — a schedule silently inheriting UTC is the
   single most common cause of "the page went out at the wrong time."

2. **Write the escalation policy with at least two independent rungs.**
   PagerDuty:
   ```json
   {
     "escalation_policy": {
       "name": "payments-team-escalation",
       "num_loops": 2,
       "escalation_rules": [
         {
           "escalation_delay_in_minutes": 5,
           "targets": [{ "id": "SCHED-PRIMARY-ID", "type": "schedule_reference" }]
         },
         {
           "escalation_delay_in_minutes": 10,
           "targets": [{ "id": "SCHED-SECONDARY-ID", "type": "schedule_reference" }]
         },
         {
           "escalation_delay_in_minutes": 15,
           "targets": [{ "id": "USER-MANAGER-ID", "type": "user_reference" }]
         }
       ]
     }
   }
   ```
   `num_loops: 2` means the whole chain repeats twice before the incident
   is marked unacknowledged and left open — don't leave this at the
   default of `0` (no repeat) for anything Sev1/Sev2-capable.
   Opsgenie's equivalent is an **escalation** object referencing a team
   and rules:
   ```json
   {
     "name": "payments-team-escalation",
     "ownerTeam": { "name": "payments" },
     "rules": [
       { "condition": "if-not-acked", "notifyType": "default", "delay": { "timeAmount": 5 }, "recipient": { "type": "schedule", "name": "payments-primary-oncall" } },
       { "condition": "if-not-acked", "notifyType": "default", "delay": { "timeAmount": 10 }, "recipient": { "type": "schedule", "name": "payments-secondary-oncall" } },
       { "condition": "if-not-acked", "notifyType": "default", "delay": { "timeAmount": 15 }, "recipient": { "type": "user", "username": "eng-manager@example.com" } }
     ]
   }
   ```
   Whether this policy actually has redundant coverage at every rung (not
   just two rungs that both happen to point at the same one person) is
   the specific thing
   [pagerduty-opsgenie-configuration-validation](../pagerduty-opsgenie-configuration-validation/SKILL.md)
   checks — do that validation after writing any escalation policy, not
   only when something goes wrong.

3. **Route alerts to the correct service/team with explicit rules, not
   a single catch-all integration.** PagerDuty Event Orchestration lets
   you route on payload fields before an event even creates an incident:
   ```yaml
   # PagerDuty Event Orchestration (router) — abbreviated
   sets:
     - id: start
       rules:
         - label: "Route payments alerts to payments service"
           conditions:
             - expression: "event.summary matches part 'payments'"
           actions:
             route_to: "SERVICE-PAYMENTS-ID"
         - label: "Route checkout alerts to checkout service"
           conditions:
             - expression: "event.summary matches part 'checkout'"
           actions:
             route_to: "SERVICE-CHECKOUT-ID"
   ```
   Opsgenie uses **alert policies** on the team/integration with `match`
   conditions and a `routeTo` action, evaluated similarly. Either way,
   route on a stable field the monitoring source guarantees is present
   (a `service` or `team` label from Alertmanager, not a free-text
   message you have to substring-match).

4. **Deduplicate at the source, using a stable key, not the tool's
   default event-per-alert behavior.** PagerDuty's Events API v2 accepts
   a `dedup_key` — reusing the same key across firing/resolving events
   for the same underlying problem collapses them into one incident:
   ```json
   {
     "routing_key": "${PAGERDUTY_INTEGRATION_KEY}",
     "event_action": "trigger",
     "dedup_key": "payments-db-replica-lag-us-east-1",
     "payload": {
       "summary": "Replica lag exceeds 30s on payments-db-replica-2",
       "severity": "critical",
       "source": "payments-db-replica-2"
     }
   }
   ```
   Opsgenie's equivalent is `alias` — sending a new event with the same
   `alias` updates the existing alert instead of creating a new one:
   ```json
   {
     "message": "Replica lag exceeds 30s on payments-db-replica-2",
     "alias": "payments-db-replica-lag-us-east-1",
     "priority": "P1"
   }
   ```
   Derive the key from stable identity (resource + check name), not from
   anything that changes per firing (a timestamp, a random ID) — a key
   that changes every time defeats deduplication entirely.

5. **Configure maintenance windows and overrides for planned work**,
   rather than muting a whole service (which also blocks real
   unrelated incidents). PagerDuty:
   ```json
   {
     "maintenance_window": {
       "start_time": "2026-08-01T02:00:00Z",
       "end_time": "2026-08-01T04:00:00Z",
       "services": [{ "id": "SERVICE-PAYMENTS-ID", "type": "service_reference" }],
       "description": "Scheduled payments-db major version upgrade"
     }
   }
   ```
   Scope maintenance windows to the specific service under maintenance,
   with a description that explains why — a team finding an unexplained
   maintenance window six months later has no way to know if it's safe
   to remove.

6. **Set per-user notification rules deliberately** (push → SMS → phone
   call escalation within the user's own device preferences), and
   require every on-call user to have at least two contact methods
   configured — a user with only a push notification and a phone that's
   on Do Not Disturb is a silent gap in the rotation regardless of how
   correct the escalation policy is.

7. **Manage all of the above as code** (Terraform `pagerduty_schedule`,
   `pagerduty_escalation_policy`, `opsgenie_schedule`,
   `opsgenie_escalation` resources, or version-controlled JSON applied
   via CI) rather than console edits, so a schedule or escalation change
   goes through the same review as any other production configuration
   change.

## Best practices

- Give every escalation policy at least two independent human rungs
  before it falls through to a policy-wide "notify everyone" — see the
  dedicated validation skill for how to check this systematically rather
  than by inspection.
- Set schedule timezones explicitly and audit them whenever a rotation
  member relocates — an inherited default timezone is a common source of
  off-hours pages landing at the wrong local time.
- Deduplicate as close to the alert source as practical (a stable
  `dedup_key`/`alias` derived from resource + check name) so one root
  cause never fans out into dozens of pages; pair with Alertmanager-side
  grouping if the monitoring stack supports it.
- Route by explicit payload fields (service/team labels), never by
  matching free-text alert summaries — a message wording change silently
  breaks substring-based routing.
- Prefer scoped, time-bound maintenance windows on the specific affected
  service over muting an entire team's paging, and always attach a
  reason.
- Keep escalation policies and schedules in version control (Terraform
  or equivalent) so changes are reviewable and diffable, not
  console-only tribal knowledge.
- Re-run the validation skill after *any* escalation policy or schedule
  edit, not just at initial setup — a policy that was correct at launch
  can silently develop a gap after a routine roster change.

## Common pitfalls

- **Symptom:** An escalation policy has a single rung, or every rung
  points at the same one person (e.g. rung 1 pages a schedule with one
  member, rung 2 pages that same person directly).
  **Fix:** This is a single point of failure — if that person is
  unreachable, the page never actually escalates to anyone new. Add at
  least one independent human at a later rung (secondary on-call, a
  manager, a different team member) and validate it with
  [pagerduty-opsgenie-configuration-validation](../pagerduty-opsgenie-configuration-validation/SKILL.md)
  rather than trusting a visual policy review.

- **Symptom:** One flapping check or one root-cause outage generates
  dozens of separate pages within minutes, and responders start
  acknowledging without reading — "alert fatigue" in its most literal
  form.
  **Fix:** Add a stable `dedup_key`/`alias` at the event-submission layer
  so repeated firings of the same underlying condition update one
  incident instead of creating new ones, and check whether the
  monitoring source itself (Alertmanager `group_by`) should be
  correlating these before they ever reach PagerDuty/Opsgenie.

- **Symptom:** A schedule was created without setting `time_zone`
  explicitly; it inherited the PagerDuty account's default timezone
  (often UTC), so the "9am–5pm local" rotation actually runs on a
  4-8 hour offset from what the team intended.
  **Fix:** Set `time_zone`/`timezone` explicitly on every schedule at
  creation time, and audit existing schedules whenever a rotation
  member's location changes.

- **Symptom:** A maintenance window is set on an entire service to
  silence a known noisy alert, and a real, unrelated incident on that
  same service goes unpaged during the window.
  **Fix:** Scope maintenance windows as narrowly as the tool allows
  (specific alert/integration where supported, not the whole service),
  keep them time-bound with an end time, and prefer fixing/tuning the
  noisy alert over muting the service long-term.

- **Symptom:** A user's notification rules are only "push notification,"
  and their phone is in Do Not Disturb mode during an off-hours page —
  the escalation policy looks correct on paper but the actual human
  never gets notified.
  **Fix:** Require every on-call-eligible user to configure at least two
  escalating contact methods (push → SMS → phone call) and periodically
  audit for users with only one configured.

## Worked example

**Scenario:** The `payments` team needs a primary/secondary weekly
rotation, a three-rung escalation policy, alert routing that separates
`payments-api` from `payments-db` alerts, and deduplication for a known
flapping replica-lag check — configured in PagerDuty via Terraform.

```hcl
resource "pagerduty_schedule" "payments_primary" {
  name      = "payments-primary-oncall"
  time_zone = "America/New_York"

  layer {
    name                         = "Weekly Rotation"
    start                        = "2026-08-03T09:00:00-04:00"
    rotation_virtual_start       = "2026-08-03T09:00:00-04:00"
    rotation_turn_length_seconds = 604800
    users                        = [pagerduty_user.alice.id, pagerduty_user.bob.id, pagerduty_user.carla.id]
  }
}

resource "pagerduty_schedule" "payments_secondary" {
  name      = "payments-secondary-oncall"
  time_zone = "America/New_York"

  layer {
    name                         = "Weekly Rotation"
    start                        = "2026-08-03T09:00:00-04:00"
    rotation_virtual_start       = "2026-08-03T09:00:00-04:00"
    rotation_turn_length_seconds = 604800
    users                        = [pagerduty_user.dan.id, pagerduty_user.eve.id]
  }
}

resource "pagerduty_escalation_policy" "payments" {
  name      = "payments-team-escalation"
  num_loops = 2

  rule {
    escalation_delay_in_minutes = 5
    target {
      type = "schedule_reference"
      id   = pagerduty_schedule.payments_primary.id
    }
  }
  rule {
    escalation_delay_in_minutes = 10
    target {
      type = "schedule_reference"
      id   = pagerduty_schedule.payments_secondary.id
    }
  }
  rule {
    escalation_delay_in_minutes = 15
    target {
      type = "user_reference"
      id   = pagerduty_user.eng_manager.id
    }
  }
}

resource "pagerduty_service" "payments_db" {
  name                    = "payments-db"
  escalation_policy       = pagerduty_escalation_policy.payments.id
  alert_creation          = "create_alerts_and_incidents"
}
```

Alertmanager sends the replica-lag alert with a stable `dedup_key`
derived from `{{ .Labels.instance }}` (not a timestamp), so a check that
flaps every 30 seconds for ten minutes produces one PagerDuty incident,
not twenty:

```json
{
  "routing_key": "${PAGERDUTY_INTEGRATION_KEY}",
  "event_action": "trigger",
  "dedup_key": "payments-db-replica-lag-payments-db-replica-2",
  "payload": {
    "summary": "Replica lag exceeds 30s on payments-db-replica-2",
    "severity": "critical",
    "source": "payments-db-replica-2",
    "custom_details": { "service": "payments-db" }
  }
}
```

Before rolling this out, run the escalation-coverage check from
[pagerduty-opsgenie-configuration-validation](../pagerduty-opsgenie-configuration-validation/SKILL.md)
against `payments-team-escalation` to confirm rung 1 and rung 2 resolve
to genuinely different humans, not an overlapping roster.

## Cross-references

- [pagerduty-opsgenie-configuration-validation](../pagerduty-opsgenie-configuration-validation/SKILL.md) — validating that the escalation policy and schedule configured here actually has no coverage gaps or single points of failure before relying on it in production.
- [servicenow-itsm-integration](../servicenow-itsm-integration/SKILL.md) — syncing incidents created by this PagerDuty/Opsgenie configuration into a ServiceNow incident/change record for ITIL-heavy organizations.
- [chatops-runbook-automation](../chatops-runbook-automation/SKILL.md) — triggering automated runbook actions from the incident this escalation policy pages someone into.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) — the severity levels, rotation design, and Incident Command process this tool configuration implements.
