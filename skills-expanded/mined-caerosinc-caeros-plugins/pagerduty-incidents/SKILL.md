---
name: pagerduty-incidents
description: Work PagerDuty incidents, including the REST incidents API, triage workflows, notes, status updates, and postmortems. Use when listing, acknowledging, resolving, or reviewing incidents.
---

# PagerDuty Incidents

An incident belongs to a service, is routed by that service's escalation
policy, and moves `triggered` -> `acknowledged` -> `resolved`. Priorities
(P1..P5), urgency (high/low), notes, and status updates hang off it.

## REST API basics

Base `https://api.pagerduty.com` (EU: `https://api.eu.pagerduty.com`).
Headers for token auth:

```
Authorization: Token token=$PAGERDUTY_API_KEY
Content-Type: application/json
```

Write endpoints require a `From: user@example.com` header identifying the
acting user. Key endpoints:

- `GET /incidents` with `statuses[]=triggered&statuses[]=acknowledged`,
  `service_ids[]`, `urgencies[]`, `since`/`until`, `sort_by`, pagination via
  `limit`/`offset` (check the `more` flag).
- `GET /incidents/{id}`, plus `/log_entries`, `/notes`, `/alerts` subpaths.
- `PUT /incidents/{id}`: change `status` (`acknowledged`, `resolved`),
  `priority`, `escalation_level`, or reassign (`assignments`).
- `POST /incidents/{id}/notes`: `{"note": {"content": "..."}}`.
- `POST /incidents/{id}/status_updates`: stakeholder-facing updates.
- `POST /incidents`: manual incident with `service`, `title`, `urgency`.
- `POST /incidents/{id}/snooze`, `.../merge` for dedup cleanup.

Monitoring integrations should send through the Events API v2
(`https://events.pagerduty.com/v2/enqueue` with a routing key), not the REST
API: it dedupes by `dedup_key` and drives trigger/acknowledge/resolve from
event `action`.

## Triage workflow

1. Acknowledge immediately: stops escalation and signals ownership.
2. Read alerts and recent change events on the incident; check sibling
   incidents on related services (shared cause is common).
3. Set priority honestly; add responders or reassign if it is not yours.
4. Post a note for every finding (timestamps become your timeline) and
   status updates for stakeholders on P1/P2.
5. Resolve only when the underlying condition is clear; auto-resolve via the
   monitoring tool's resolve event is preferred, so states stay in sync.

The bundled hosted MCP server exposes these operations as tools (list,
acknowledge, resolve, notes, escalation), so triage can happen
conversationally; tool availability follows your account permissions.

## Postmortems

After resolution on significant incidents:

- Build the timeline from log entries and notes
  (`GET /incidents/{id}/log_entries?include[]=channels` gives who did what,
  when).
- Capture: impact window, detection source, time to acknowledge, time to
  resolve, contributing factors, follow-up actions with owners.
- PagerDuty's built-in retrospective/postmortem feature (plan-dependent)
  links the report to the incident; otherwise export the timeline into your
  docs tool.
- Feed recurring causes back into service configuration: better alert
  grouping, adjusted urgency, or runbook links on the service.

## Practices

- Never resolve unacknowledged P1s in bulk; each needs an owner decision.
- Use `snooze` instead of resolve for known-flapping conditions.
- Keep `From` accurate: audit trails and on-call analytics depend on it.
