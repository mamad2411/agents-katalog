---
name: inspect
description: Show AIP's evidenced architecture context for a Pitstop service as a table of claims with qualification, route evidence, evidence references, snapshot id and limitations. Read-only.
argument-hint: "[service name or id]"
disable-model-invocation: true
allowed-tools: mcp__plugin_aip_aip__get_service_dependencies mcp__plugin_aip_aip__get_evidence mcp__plugin_aip_aip__get_architecture_drift
disallowed-tools: Bash Write Edit NotebookEdit
---

# /aip:inspect

Inspect one service with AIP and print what it returns. Read-only: never edit files or run commands.

Requested service: `$ARGUMENTS`

1. **Subject.** If an argument is given, it is the service (a name or an id from the table below). Otherwise
   infer it from the session: the service folder you are working in, the files touched, or the last prompt. If
   you cannot tell, ask which service; do not guess.
2. **Context.** Use the environment and window the user or the demo prompt named (whole UTC days wholly in the
   past: from `T00:00:00Z` through `T23:59:59Z` of the last day; the window is inclusive, so do not end it at the
   next day's `T00:00:00Z`, and do not refuse `T23:59:59Z` as an incomplete day). If none was named, ask for
   them; never invent them.
3. **Ask.** Call `get_service_dependencies` for the service id. A receiving service has no receiver-side
   question: if it is a receiver, say so and offer to inspect the publisher that feeds it (the publishers are in
   the table).
4. **Print** one table, one row per dependency claim: receiver (`object`), queue (`delivery.subscription`),
   destination resolution, the claim's qualification (the publisher's) and coverage, whether the **route**
   carries observed evidence (read it from `resolution_evidence_refs`: declared, observed, or both; the
   claim's own `evidence_refs` are the publisher's and say nothing about the receiver), and the evidence
   reference ids; then the snapshot id, the observation context, the Broker
   claim, and every limitation verbatim. State plainly: receipt is per messaging destination (the exchange),
   never per event type; AIP holds no payload or field-level knowledge. If every claim reads
   `NOT_OBSERVED_IN_WINDOW` with coverage `NONE`, say only that AIP saw no publisher span for that service in that
   window; do not guess why (a replay, another environment, ingestion): offer a different window or the
   environment name to check.
5. **Drill-down on request only.** If asked to resolve references, call `get_evidence` at the answer's own
   snapshot; on `SNAPSHOT_NOT_AVAILABLE` ask the dependency question again for the same context and retry, at
   most three attempts, then report the drill-down as failed.

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
