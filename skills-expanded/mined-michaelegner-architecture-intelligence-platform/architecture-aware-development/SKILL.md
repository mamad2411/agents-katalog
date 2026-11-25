---
name: architecture-aware-development
description: Use when a task changes an event, a message contract, shared data, a deployment or a service boundary in the Pitstop system and you need the evidenced architecture context before planning - which services AIP resolves as receiving from the messaging destination the changed service publishes to, what was observed, and where the evidence stops. Queries AIP read-only and puts an Evidence section into the plan.
allowed-tools: mcp__plugin_aip_aip__get_service_dependencies mcp__plugin_aip_aip__get_evidence mcp__plugin_aip_aip__get_architecture_drift
disallowed-tools: Bash Write Edit NotebookEdit
---

# Architecture-aware development with AIP

AIP (Architecture Intelligence Platform) answers from declared architecture plus runtime observation, and it
says how far each claim is evidenced. Use it to bound your plan, never to replace reading the code.

## What AIP can and cannot tell you

- It resolves the **receivers** of a messaging destination, **asked through the publishing service**. AIP has no
  receiver-side question: the receivers are the `RESOLVED_SERVICE` claims in the publisher's answer, each with
  its queue as `delivery.subscription`.
- Receipt is **per messaging destination** (the exchange, a Topic in AIP), **never per event type**. An answer
  says nothing about which receiver handles which event.
- Every claim carries the **publisher's** qualification (`CONFIRMED`, `OBSERVED_ONLY`, `NOT_OBSERVED_IN_WINDOW`,
  with coverage when not observed). It is identical for all receivers: AIP has no per-queue qualification.
  A receiver's route may additionally carry observed evidence; a route without it is **not** an unused route.
  Read the route evidence from the claim's `resolution_evidence_refs` (declared, observed, or both): that is the
  receiver's route. The claim's own `evidence_refs` are the **publisher's** and say nothing about the receiver.
- AIP holds **no payload or field-level knowledge**. Which receiver reads a field is something you must inspect
  in that receiver's code.

## Workflow

1. **Name the observation context.** Use the environment and window the user or the prompt gives you (one or more
   whole UTC days wholly in the past: only those are stable under later evidence; from `T00:00:00Z` through
   `T23:59:59Z` of the last day, the window is inclusive, so never end it at the next day's `T00:00:00Z`). If none
   is given, ask. Never invent an environment or a window.
2. **Ask the publisher.** Call `get_service_dependencies` for the **publishing** service of the changed event,
   using the table below to map a service name to its AIP service id. If you do not know which service
   publishes, find that in the repository first and say how you know.
3. **Resolve the evidence you rely on.** Call `get_evidence` with the answer's `evidence_refs` and its own
   `snapshot_id`. The snapshot id changes whenever evidence is ingested, and a stale snapshot is refused with
   `NOT_ANSWERED` and the limitation `SNAPSHOT_NOT_AVAILABLE`. Then ask the dependency question again for the
   **same** context and retry `get_evidence` with the new answer's references and snapshot, **at most three
   attempts** in total. If all fail, report the drill-down as failed, naming the last snapshot ids, and do not
   cite unresolved references.
4. **Optionally** call `get_architecture_drift` for the same service and context. Report only what it returns
   (declared-but-unexercised, not "undocumented").
5. **Write the Evidence section** (below) into your plan before the plan's steps.
6. **Compare with the repository's documents yourself.** If a document lists different consumers than AIP
   resolves, say so, labelled as **your reading of the documents**, not as an AIP drift claim.

## Service ids

| Service (folder / name) | AIP service id | Role on the exchange `Pitstop` |
|---|---|---|
| CustomerManagementAPI | `service:customer-management-api` | publishes |
| TimeService | `service:time-service` | publishes |
| VehicleManagementAPI | `service:vehicle-management-api` | publishes |
| WorkshopManagementAPI | `service:workshop-management-api` | publishes |
| AuditlogService | `service:auditlog-service` | receives via queue `Auditlog` |
| InvoiceService | `service:invoice-service` | receives via queue `Invoicing` |
| NotificationService | `service:notification-service` | receives via queue `Notifications` |
| ReportingService | `service:reporting-service` | receives via queue `Reporting` |
| WorkshopManagementEventHandler | `service:workshop-management-event-handler` | receives via queue `WorkshopManagement` |

## The Evidence section

Put this in the plan, with values copied from the AIP answers:

```
## Evidence (AIP)
Context: <environment>, <window_start> to <window_end>; snapshot <snapshot_id>
Publisher: <service> -> Topic <name> through Broker <name>
| Receiver | Queue | Qualification (the publisher's) | Route has observed evidence | Evidence refs |
Unknowns carried over from AIP: <every limitation and NOT_ANSWERED statement, verbatim>
Not known to AIP: which receiver reads <the fields being changed>; per-event-type receipt.
```

## Rules

- Copy the answer's limitations and `NOT_ANSWERED` statements into the plan as **unknowns**, never as risks
  resolved.
- **Never** state what a consumer does with a payload, or which fields it reads, from AIP evidence. Say
  "inspect the consumer" and plan that inspection for **each** receiver AIP resolves, including any that no
  document lists.
- Treat every receiver as unknown until you have inspected it. Absence of further evidence is never
  completeness, and "unobserved" never means "unused".
- Do not claim that the change is safe, or that AIP identified the breaking consumers.
- This skill only reads. It never edits files, runs commands or changes AIP.
