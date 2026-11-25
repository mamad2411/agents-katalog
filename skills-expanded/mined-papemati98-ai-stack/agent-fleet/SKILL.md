---
name: agent-fleet
description: Execute lean TODO tasks through native CLI models with independent product review and targeted repairs; no procedural contract chain for new work.
---

# Agent Fleet: lean dispatch 1.0

For new work, use one short TODO from plan-delivery. A single small task
uses `agent-graph/scripts/todo_pair.py --todo <todo.json> --run-dir <absolute-dir>`;
larger work with real branches uses `todo_graph.py run` once. Each task has one maker and one independent
reviewer, its real dependencies and product checks. No planning, quality or
acceptance contracts, fidelity/sufficiency gates or audits of reports.

Fleet remains the native CLI transport and model/availability router. Preserve
exact-model identity, data-sharing denylist, credentials, quota and workspace
protections. Fit first; prefer cheaper competent makers and appropriately strong
reviewers. For comparable fit prefer unused paid capacity. Unknown quota is not
zero. Check before forwarding task content; do not try exhausted accounts in a loop.

Availability checks are shared per subscription pool and cached across CLI runs.
Snapshot expiry means recheck, not restored capacity. Kimi uses native usage data;
if it cannot resolve availability, one isolated minimal CLI ping uses no project
files or tools. A weekly counter cannot clear a monthly denial. A failed check
selects another eligible worker, not a full task as a probe. Never buy extra usage
or switch accounts automatically. Native quota errors refresh this small cache;
tokens remain telemetry, not a new contract or acceptance requirement.

TODO Graph starts ready disjoint tasks in parallel. Deterministic failing tests
go back to the maker before paid review. Product REPAIR returns concrete findings;
no fresh planning cycle. Preserve code on malformed handoff or transport failure.
Two identical failures without progress need diagnosis, not another blind retry.
Token estimates are telemetry, not acceptance gates. Explicit owner limits remain.
Transport, retained artifact, product acceptance and knowledge closeout are
separate states. A verified maker with only an unparsed terminal handoff can
continue to the declared checks and independent review on the retained artifact;
this is PARTIAL work, never ACCEPT. Wrong model, checkout, base, scope or missing
provenance stays blocked. Do not call the maker again to repair a report format.

The current strong parent plans and integrates; a cheap parent delegates one
planning pass, not every coordination decision. Actual model lineage must differ
between maker and reviewer even when models share the same CLI subscription.

Legacy fleet.py run/quality-gate/security-gate/accept-group retain their old
semantics for existing records. TODO results do not overwrite those ledgers.
Report actual worker/reviewer, model, product result, tokens/quota if known.
An accepted candidate is not a production deployment.

Incident metadata is appended without a global history scan. Run `fleet.py
incident-report` only when inspecting problems; it refreshes the derived index.
Do not poll the report per node. A stored event does not imply a refreshed index.
TODO stage telemetry is automatic; see agent-graph's Lightweight Telemetry.
