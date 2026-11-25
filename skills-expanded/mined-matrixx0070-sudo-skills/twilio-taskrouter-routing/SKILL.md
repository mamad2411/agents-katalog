---
name: twilio-taskrouter-routing
version: 1.0.0
description: Design skills-based task distribution with Twilio TaskRouter — Workspaces, Workflows, TaskQueues, Workers, Activities, and reservation handling.
author: matrixx0070
tags: [twilio, taskrouter, routing, contact-center, workflow, acd]
capabilities: []
---

## When to use

Use this when you need to distribute work items (calls, chats, SMS, tickets, leads) to the right human agent based on skills, priority, and availability — the core of a contact center or dispatch system. Reach for it when "who should handle this and are they free?" is the hard part: skills-based routing, priority queues, capacity limits, and reservation accept/reject loops.

**Not for:** the customer-facing conversation or IVR that *creates* the task — build that in twilio-studio-flows (its Enqueue widget hands off to TaskRouter). Not for verifying identity or numbers — see twilio-verify-send-otp and twilio-lookup-phone-intelligence.

## Method

1. **Create the Workspace.** Everything lives inside one TaskRouter Workspace (`WSxxxx...`) — Workers, TaskQueues, Workflows, Activities, and Tasks are all scoped to it.
2. **Define Activities.** Worker states such as Available, Unavailable, Offline, Busy. Decision point: only Activities marked `available` can receive reservations — mark break/wrap-up states unavailable.
3. **Model Workers with attributes.** Each Worker has a JSON attributes blob (e.g. `{"skills":["spanish","billing"],"level":2}`) plus a current Activity and capacity. Attributes are what routing matches on.
4. **Build TaskQueues with target expressions.** A TaskQueue selects eligible Workers via a `TargetWorkers` expression over worker attributes, e.g. `skills HAS "spanish"`. Decision point: keep queues aligned to skill/team, not to individuals.
5. **Author the Workflow.** The Workflow routes incoming Tasks through ordered filters to TaskQueues, with priority and timeouts, and optional escalation. Decision point: order filters most-specific first; add a fallback/default queue so no task is unroutable.
6. **Create Tasks with attributes.** A Task carries a JSON attributes blob (e.g. `{"selected_language":"spanish","type":"billing"}`) that the Workflow filters match against, plus a priority.
7. **Handle reservations.** TaskRouter offers a matched Task to a Worker as a Reservation via the Assignment Callback / event webhooks. Accept, reject, redirect, or issue instructions (e.g. `dequeue` a call to the worker). Decision point: on reject or timeout, the Task re-enters routing.
8. **Track capacity and events.** Respect per-Worker per-channel capacity so agents aren't overloaded; subscribe to TaskRouter event webhooks (reservation.created, task.completed, worker.activity.update) for real-time dashboards and SLA monitoring.

## Example

```javascript
const client = require('twilio')(accountSid, authToken);
const ws = client.taskrouter.v1.workspaces(workspaceSid);

// Worker with routing attributes
await ws.workers.create({
  friendlyName: 'Ana',
  attributes: JSON.stringify({ skills: ['spanish', 'billing'], level: 2 })
});

// TaskQueue targeting Spanish-speaking billing agents
await ws.taskQueues.create({
  friendlyName: 'ES Billing',
  targetWorkers: 'skills HAS "spanish" AND skills HAS "billing"'
});

// Create a Task the workflow will route
await ws.tasks.create({
  workflowSid: 'WW...',
  attributes: JSON.stringify({ selected_language: 'spanish', type: 'billing' }),
  priority: 5
});
```

```json
// Workflow configuration (routing_configuration)
{
  "task_routing": {
    "filters": [
      { "expression": "type == 'billing' AND selected_language == 'spanish'",
        "targets": [{ "queue": "WQ_es_billing", "priority": 10 }] }
    ],
    "default_filter": { "queue": "WQ_general" }
  }
}
```

## Pitfalls

- **No default/fallback queue.** A Task that matches no filter becomes stuck/unroutable. Always give the Workflow a `default_filter`.
- **Only `available` Activities get reservations.** If every Worker is in an unavailable Activity (wrap-up, break), Tasks queue indefinitely. Monitor Activity distribution.
- **Attributes are JSON strings, and expressions are strict.** A typo in a `TargetWorkers`/filter expression or a mismatched attribute key silently routes nothing. Validate attribute schemas.
- **Capacity misconfiguration overloads or starves agents.** Per-channel capacity governs concurrent Tasks; too low starves throughput, too high overloads agents. Tune per channel.
- **Reservations time out.** An unaccepted Reservation expires and the Task re-routes; if your assignment callback doesn't respond with instructions, calls can drop. Handle reservation events promptly.
- **Ignoring event webhooks.** Without subscribing to TaskRouter events you're blind to SLA breaches and stuck tasks. Wire the EventCallbackUrl and validate `X-Twilio-Signature`.

## Output format

```
TASKROUTER DESIGN
  workspace: <friendly name / WS SID>
  activities: <Available, Unavailable, Offline, Busy ...>
  workers:
    - <name> attributes:{skills, level, ...} capacity:{channel:n}
  taskqueues:
    - <name> targetWorkers: <expression>
  workflow_filters (ordered):
    - <expression> -> queue:<name> priority:<n> timeout:<s>
    default -> <fallback queue>
  task_attributes_schema: <keys used for matching>
  events_subscribed: <reservation.created, task.completed, ...>
```

## Reference

- **Product:** Twilio TaskRouter — an ACD/skills-based routing engine. API v1, host `taskrouter.twilio.com`, everything scoped to a **Workspace** (`WS...`).
- **Core resources:** Workers (`WK...`, with JSON `attributes`, an Activity, and capacity), Activities (`WA...`, availability states, `available` boolean), TaskQueues (`WQ...`, with a `TargetWorkers` expression), Workflows (`WW...`, ordered `task_routing.filters` + `default_filter`, priorities, timeouts), Tasks (`WT...`, JSON `attributes` + `priority`), Reservations (`WR...`, the offer of a Task to a Worker).
- **Matching:** filter and TargetWorkers expressions use TaskRouter's expression language over attribute JSON (`HAS`, `==`, `AND`, `OR`, `IN`). Routing is skills/priority/FIFO within a queue.
- **Reservation lifecycle:** pending → accepted/rejected/timeout/canceled/rescinded; accept then issue instructions (`dequeue`, `call`, `redirect`, `conference`) — commonly to connect a queued Twilio call to the worker.
- **Realtime:** JS SDK (Worker/TaskRouter JS SDK) for agent desktops; Assignment Callback URL for reservation handling; EventCallbackUrl for the full event stream (reservation.created, reservation.accepted, task.created/completed/canceled, worker.activity.update).
- **Auth & security:** Account SID + Auth Token or API Key SID/Secret for REST; short-lived capability/access tokens for browser JS SDK workers. Validate the `X-Twilio-Signature` header (HMAC-SHA1 of URL + params keyed by Auth Token) on assignment and event webhooks.
- **Integration:** Studio's Enqueue Call widget and Programmable Voice `<Enqueue workflowSid>` TwiML feed Tasks into TaskRouter, connecting IVR front-ends to skills-based agent routing.
