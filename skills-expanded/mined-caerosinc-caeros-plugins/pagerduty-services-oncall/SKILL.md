---
name: pagerduty-services-oncall
description: Manage PagerDuty services, escalation policies, and on-call schedules, including overrides and the oncalls API. Use when structuring services, changing escalation, or answering who is on call.
---

# PagerDuty Services, Escalation, On-Call

Routing chain: integration -> **service** -> **escalation policy** ->
(**schedules** and users) -> notifications. Get the chain right and paging is
predictable.

## Services

A service represents one owned system component with its own alerting
integrations and escalation policy.

- `GET /services`, `POST /services`, `PUT /services/{id}`.
- Key fields: `escalation_policy`, `alert_creation`
  (create alerts and incidents), alert grouping settings (time-based,
  content-based, or intelligent, plan-dependent), `auto_resolve_timeout`,
  `acknowledgement_timeout`, support hours and urgency rules (e.g. low
  urgency at night for non-critical services).
- Integrations: `POST /services/{id}/integrations` returns the routing key
  used by Events API v2 senders.
- Business services (plan-dependent) model user-facing capabilities on top of
  technical services for status and impact views.

Granularity rule: one service per independently-owned, independently-paged
component. Too coarse means wrong team paged; too fine means alert sprawl.

## Escalation policies

Ordered levels, each with targets (schedules or users) and an escalation
delay in minutes; optional loop count if nobody acknowledges.

- `GET/POST/PUT /escalation_policies`.
- Level 1: the owning team's primary on-call schedule. Level 2: secondary
  schedule or team lead. Level 3: engineering management.
- Target schedules, not individuals, wherever possible; policies with named
  humans rot when people change teams.

## Schedules

A schedule is composed of rotation layers; layers higher in the list win
where they overlap, and restrictions limit a layer to times of day or week.

- `GET /schedules`, `GET /schedules/{id}` (rendered final schedule),
  `POST /schedules/preview` to dry-run changes.
- Rotations: weekly or daily handoffs; follow-the-sun = two or three layers
  with time-of-day restrictions across regions.
- Overrides for swaps and vacations: `POST /schedules/{id}/overrides` with
  `start`, `end`, `user`. Never edit the rotation for a one-off swap.

## Who is on call

The `oncalls` API answers it directly:

```
GET /oncalls?schedule_ids[]=SCHED&earliest=true
GET /oncalls?escalation_policy_ids[]=EP&since=...&until=...
GET /oncalls?user_ids[]=USER          # when is this person on call
```

Filter by `escalation_level` (level 1 = who gets paged first). The bundled
hosted MCP server exposes services, escalation policies, schedules, and
oncalls as tools, so "who is on call for checkout tonight" is a direct query.

## Practices

- Review rendered schedules after any layer change; layer precedence
  surprises are the top cause of missed pages.
- Alert grouping on noisy services before adding escalation levels: fewer,
  better pages beat deeper escalation.
- Audit for gaps: any escalation policy level with zero current on-call is a
  silent hole (`earliest=true` per schedule finds them).
