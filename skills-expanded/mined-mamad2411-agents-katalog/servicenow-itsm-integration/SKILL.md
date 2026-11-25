---
name: servicenow-itsm-integration
description: >
  Integrates ServiceNow Incident, Change, and Problem management with
  engineering paging/incident tools (PagerDuty, Opsgenie) for ITIL-heavy
  enterprises that need an auditable, compliance-grade record alongside
  fast real-time paging — Table API incident sync, Change Request
  approval workflow (including emergency changes during an active
  incident), Problem record linkage, and CMDB-based assignment routing.
  Use when the user asks to "sync PagerDuty incidents into ServiceNow,"
  "set up a ServiceNow change request for a production deploy," "link an
  incident to a problem record," "route a ServiceNow incident to the
  right assignment group," or "our ServiceNow and PagerDuty incidents
  are out of sync."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: incident-tooling-and-itsm
  maturity: stable
---

# ServiceNow ITSM Integration

## Purpose

Engineering incident tools like PagerDuty and Opsgenie are optimized for
speed — page the right human in seconds. ServiceNow's Incident, Change,
and Problem management modules are optimized for something different:
an auditable, ITIL-compliant record of what happened, who approved what,
and how it connects to the CMDB — the record a compliance auditor, a
change advisory board, or an enterprise-wide reporting dashboard needs,
and that PagerDuty was never designed to be. In an ITIL-heavy enterprise
these aren't a choice between one or the other; a real incident needs
both a paged human acting in minutes and a synced ServiceNow record
that's got the right assignment group, links to the change that likely
caused it, and (if a fix requires a production change mid-incident) an
emergency change request that doesn't wait for a weekly CAB meeting.
This skill covers that integration and sync — not how to design the
on-call paging itself (see
[pagerduty-and-opsgenie-oncall-configuration](../pagerduty-and-opsgenie-oncall-configuration/SKILL.md))
or the incident-command process running in parallel (see
[incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md)).

## When to use

- Standing up bi-directional sync so a PagerDuty/Opsgenie incident
  automatically creates and updates a ServiceNow Incident record (and
  vice versa), instead of someone manually copy-pasting details between
  tools.
- Writing or troubleshooting a Change Request workflow for a production
  deployment — standard vs. normal vs. emergency change types, and CAB
  approval routing.
- Linking a recurring or unresolved incident to a Problem record for
  root-cause tracking that outlives any single incident.
- Configuring CMDB-based assignment group routing so a ServiceNow
  incident lands with the team that actually owns the affected
  Configuration Item, not a generic triage queue.
- Debugging a sync issue: incidents duplicating, status ping-ponging
  between tools, or a ServiceNow incident stuck in the wrong assignment
  group.
- Deciding how a mid-incident production fix (a rollback, a config
  change) gets an emergency Change Request without waiting for the
  normal weekly CAB cycle.

## Prerequisites & environment

- A ServiceNow instance (`${SNOW_INSTANCE_URL}`, e.g.
  `https://yourcompany.service-now.com`) with Table API access enabled
  and an integration user account holding at minimum the `itil` role
  (incident/problem read-write) and change-management roles as needed
  (`change_manager` or scoped ACLs for the Change table) — use OAuth2 or
  a scoped API key stored as `${SNOW_CLIENT_ID}`/`${SNOW_CLIENT_SECRET}`,
  never basic auth with a hardcoded password.
- Either the native PagerDuty-for-ServiceNow / Opsgenie-ServiceNow
  integration app (simplest, maintained by the vendor) or a custom
  webhook-driven sync via ServiceNow Flow Designer/Scripted REST APIs —
  prefer the native app unless it doesn't cover a specific required
  field mapping.
- CMDB Configuration Items (CIs) already populated for the services in
  scope, with each CI mapped to an owning assignment group — sync is
  only as good as CMDB accuracy; a service with no CI or a stale CI
  owner will misroute every incident against it.
- Clarity on change types your ServiceNow instance supports (Standard,
  Normal, Emergency) and who is authorized to raise an Emergency Change
  — this must be resolved before an incident, not decided live during
  one.
- Existing PagerDuty/Opsgenie paging configuration to sync against — see
  [pagerduty-and-opsgenie-oncall-configuration](../pagerduty-and-opsgenie-oncall-configuration/SKILL.md).

## Step-by-step guidance

1. **Create the ServiceNow Incident from the paging tool's incident
   trigger**, via the Table API, carrying over the paging tool's
   incident ID as a correlation field so later updates target the same
   record instead of creating duplicates:
   ```http
   POST /api/now/table/incident
   Host: ${SNOW_INSTANCE_URL}
   Authorization: Bearer ${SNOW_ACCESS_TOKEN}
   Content-Type: application/json
   ```
   ```json
   {
     "short_description": "Checkout success rate dropped sharply",
     "description": "Auto-created from PagerDuty incident PD-INC-48213. See link for live timeline.",
     "urgency": "1",
     "impact": "1",
     "cmdb_ci": "checkout-api",
     "correlation_id": "PD-INC-48213",
     "correlation_display": "PagerDuty",
     "assignment_group": "checkout-team"
   }
   ```
   `correlation_id` is the field every subsequent update must query on
   (`GET /api/now/table/incident?sysparm_query=correlation_id=PD-INC-48213`)
   — this is what makes the sync idempotent instead of duplicate-prone.

2. **Sync status changes bidirectionally through a defined mapping**,
   not a free-text guess — PagerDuty/Opsgenie states map onto ServiceNow
   incident states explicitly:

   | Paging tool state | ServiceNow `incident_state` |
   |---|---|
   | Triggered | 2 (In Progress) |
   | Acknowledged | 2 (In Progress) |
   | Resolved | 6 (Resolved) |
   | (Postmortem complete) | 7 (Closed) |

   Implement this as a Flow Designer flow (webhook trigger →
   `incident_state` field update) or a scripted REST endpoint the paging
   tool calls on state transitions — and make the same mapping work in
   reverse (a ServiceNow-side status edit reflected back), guarding
   against the sync-loop pitfall below.

3. **Route incidents by CMDB CI → assignment group**, not a static
   default queue:
   ```
   incident.cmdb_ci  → looks up →  cmdb_rel_ci (or a dedicated
   ci_to_team mapping table)  →  incident.assignment_group
   ```
   Configure this as a Business Rule or Flow Designer flow on incident
   `insert`/`update` that resolves `assignment_group` from the CI's owner
   relationship, so a new service only needs its CMDB CI's owner set
   correctly once, rather than a routing rule maintained per-service in
   two places.

4. **Model change types deliberately** — most ServiceNow instances ship
   with three:
   - **Standard**: pre-approved, low-risk, repeatable (e.g. a routine
     config change from a pre-approved template) — no per-instance CAB
     approval needed.
   - **Normal**: requires CAB (Change Advisory Board) approval on its
     usual cadence — the default for anything non-trivial and
     non-urgent.
   - **Emergency**: bypasses the normal CAB *schedule* but still requires
     approval — typically from an on-call/emergency-CAB approver
     reachable in minutes, not the weekly meeting.
   ```json
   {
     "short_description": "Emergency rollback of checkout-api v2.14.1",
     "type": "emergency",
     "justification": "Mitigating active Sev1 incident INC0048213 — rolling back to v2.14.0",
     "cmdb_ci": "checkout-api",
     "risk": "moderate",
     "assignment_group": "checkout-team"
   }
   ```
   Link the Change Request to the active Incident record
   (`change_request.parent_incident` or a related-list relationship) so
   the audit trail shows exactly which incident justified bypassing
   standard CAB timing.

5. **Require an actual (even if fast) emergency-change approval, not a
   silent bypass.** Configure the Emergency change type's approval
   definition to route to a small, always-reachable on-call
   approver group (mirroring the paging tool's own on-call schedule) with
   a tight SLA (e.g. 15 minutes), rather than either (a) requiring the
   full weekly CAB — too slow for an active Sev1 — or (b) no approval at
   all — which erases the audit trail the whole ITSM integration exists
   to provide.

6. **Link recurring/unresolved incidents to a Problem record** for
   root-cause tracking that outlives the incident:
   ```http
   POST /api/now/table/problem
   ```
   ```json
   {
     "short_description": "Recurring checkout-api replica lag causing intermittent 5xx",
     "cmdb_ci": "checkout-db",
     "incident": "INC0048213"
   }
   ```
   Then relate every future incident with the same root cause back to
   this Problem record (`problem_id` field on the incident) instead of
   letting each recurrence be investigated from scratch.

7. **Guard every inbound webhook/sync call with an idempotency key** —
   use the paging tool's incident ID (already captured as
   `correlation_id`) to check-then-update rather than blindly inserting,
   so a retried webhook delivery (both PagerDuty and Opsgenie retry on
   timeout) doesn't create a duplicate ServiceNow incident for the same
   underlying page.

## Best practices

- Always carry the paging tool's incident ID into `correlation_id` and
  query on it before any write — this single field is what keeps sync
  idempotent under retries and prevents duplicate records.
- Keep Emergency Change approval fast (minutes, from a dedicated
  reachable approver group) but never optional — an emergency change
  with zero approval defeats the audit purpose ITSM integration exists
  for in the first place.
- Drive assignment-group routing off CMDB CI ownership, and treat a
  stale/missing CI-to-team mapping as a data-quality bug to fix at the
  source, not a routing exception to special-case per service.
- Link every Change Request made during an incident back to that
  incident record explicitly, so a postmortem (see
  [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md))
  can trace exactly which changes were made under emergency conditions.
- Prefer the vendor-maintained PagerDuty/Opsgenie ServiceNow integration
  app over a fully custom webhook sync unless a specific field mapping
  genuinely requires it — a custom sync is another system to maintain
  and another source of sync-loop bugs.
- Validate the workflow/approval configuration itself before depending
  on it in a real incident — see
  [servicenow-itsm-configuration-validation](../servicenow-itsm-configuration-validation/SKILL.md).

## Common pitfalls

- **Symptom:** A PagerDuty incident and its synced ServiceNow record
  bounce a status update back and forth — PagerDuty resolves, the sync
  flow marks ServiceNow Resolved, a ServiceNow business rule fires and
  pushes a status back to PagerDuty, which re-triggers the sync flow
  again, and so on.
  **Fix:** Give the sync flow a clear single source of truth per field
  and direction (e.g. paging-tool status is authoritative while an
  incident is open; ServiceNow becomes authoritative only after
  Resolved, for closure/RCA fields) and have each sync leg check whether
  the target value already matches before writing, rather than writing
  unconditionally on every event.

- **Symptom:** During an active Sev1, the fix requires a production
  rollback, but the Change Request created for it sits waiting for the
  next weekly CAB meeting — the incident drags on for hours because the
  Change process, not the technical fix, is the bottleneck.
  **Fix:** Configure and use the Emergency change type (step 4/5) with a
  fast, always-reachable approver group instead of routing every
  production change through Normal/CAB regardless of urgency — this
  needs to be set up and tested *before* the incident, not requested for
  the first time mid-Sev1.

- **Symptom:** A retried PagerDuty webhook delivery (e.g. after a
  transient network timeout) creates a second, duplicate ServiceNow
  incident for the same underlying page, and both get worked
  independently by different assignees.
  **Fix:** Query by `correlation_id` before inserting (step 1/7) —
  check-then-update, not insert-always — so a retried delivery updates
  the existing record instead of creating a new one.

- **Symptom:** A new microservice's incidents consistently land in a
  generic "Unassigned" ServiceNow queue instead of the owning team, so
  they sit until someone notices manually.
  **Fix:** The service's CMDB CI either doesn't exist yet or has no
  owning-group relationship configured — this is a CMDB data-quality gap
  to fix at onboarding time for every new service, not a routing
  exception to patch per incident.

## Worked example

**Scenario:** `checkout-api`'s Sev1 (from the worked example in
[incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md))
needs both the PagerDuty incident and a synced ServiceNow record, plus
an emergency Change Request for the rollback that mitigates it.

1. PagerDuty incident `PD-INC-48213` triggers; a Flow Designer flow
   (webhook-triggered) creates the ServiceNow incident:
   ```json
   {
     "short_description": "Checkout success rate dropped sharply",
     "urgency": "1",
     "impact": "1",
     "cmdb_ci": "checkout-api",
     "correlation_id": "PD-INC-48213",
     "assignment_group": "checkout-team"
   }
   ```
   Response: `201 Created`, `number: "INC0048213"`.

2. The Tech Lead identifies a bad config in the latest deploy and
   proposes a rollback. Because this is an active Sev1, an Emergency
   Change is raised instead of waiting for the weekly CAB:
   ```json
   {
     "short_description": "Emergency rollback of checkout-api v2.14.1",
     "type": "emergency",
     "justification": "Mitigating active Sev1 INC0048213 — rolling back to v2.14.0",
     "cmdb_ci": "checkout-api",
     "parent_incident": "INC0048213",
     "assignment_group": "checkout-team"
   }
   ```
   The on-call emergency-CAB approver (a role staffed 24/7, distinct
   from the normal weekly CAB) approves within 6 minutes; the change
   record (`CHG0031840`) is now the audit trail for the rollback.

3. The rollback completes and checkout's error rate recovers. The sync
   flow updates `INC0048213`'s `incident_state` to `6` (Resolved) when
   PagerDuty's incident is resolved, using `correlation_id` to target
   the exact record rather than searching by description text.

4. Because this is the second time in a month checkout-api has had a
   config-related rollback, a Problem record is opened and linked:
   ```json
   {
     "short_description": "Recurring checkout-api deploy-config regressions",
     "cmdb_ci": "checkout-api",
     "incident": "INC0048213"
   }
   ```
   giving the team a durable place to track the underlying root cause
   across incidents, separate from any single incident's record.

## Cross-references

- [servicenow-itsm-configuration-validation](../servicenow-itsm-configuration-validation/SKILL.md) — validating that the assignment routing, approval workflow, and sync flows described here won't block or misroute a real incident before depending on them.
- [pagerduty-and-opsgenie-oncall-configuration](../pagerduty-and-opsgenie-oncall-configuration/SKILL.md) — the paging-tool side this integration syncs against; escalation policies and services referenced by `correlation_id` here.
- [chatops-runbook-automation](../chatops-runbook-automation/SKILL.md) — automated runbook actions taken during the incident this integration is tracking should also be reflected in the ServiceNow record for audit purposes.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) — the Incident Command process and severity levels that drive when a ServiceNow record and emergency change get created in the first place.
