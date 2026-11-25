---
name: agentic-ops-builder
description: >-
  Build durable agentic operations for an Azure platform on Dapr Workflow:
  human-in-the-loop provisioning approvals that survive days-long pauses,
  monitor-pattern health checks, saga/compensation for multi-step
  provisioning, and Cluster-Doctor-style remediation loops (detect -> issue
  with context -> agent diagnosis via MCP -> remediation PR -> human
  approval). Use for platform automation workflows, approval flows, day-2
  operations agents, auto-remediation design, or wiring agent-proposed
  changes into a PR-gated GitOps loop on AKS.
---

# Agentic Ops Builder

## Purpose
The agentic layer of the platform: durable workflows that let agents operate
the platform — not just author it — while humans keep decision authority.
Everything an agent proposes lands as a PR or an approval request; nothing
mutates environments directly.

## Runtime decision (learned the hard way, encode it)
Durable agentic workloads target **Dapr Workflow on AKS** (workflow stable
since Dapr 1.15). Azure Container Apps' managed Dapr does **not** support the
workflow/actor server SDK extensions or Dapr in ACA jobs — ACA is fine for
stateless building-block workloads, wrong for the durable automation layer.
Dapr Agents (v1.0 GA, Python) is the step-up option when a workflow needs
autonomous planning rather than predefined steps.

## The four workflow patterns to build from
1. **External-event approval (human-in-the-loop).** Provisioning requests
   pause on an external event; "the pause can last seconds, hours, or days —
   the workflow rehydrates wherever it left off." This is the mechanism behind
   every approval gate the constitution requires.
2. **Monitor.** Recurring checks (recipe drift, AVM pin currency, orphaned
   module status, cert expiry) via continue-as-new — never infinite loops.
3. **Saga / compensation.** Multi-step provisioning (subscription vending ->
   foundation -> environment -> registration) with explicit compensations, so
   a failed step unwinds cleanly instead of stranding half a landing zone.
4. **Remediation loop (Cluster-Doctor pattern).** Detector (GitOps health,
   alerts) fires -> issue created with full context -> labeled agent diagnoses
   through MCP tools (AKS MCP, Azure MCP) -> opens a remediation PR ->
   human approves -> GitOps reconciles. Crawl: manual label. Run: auto-label
   with tight guardrails.

## Workflow
1. Read the constitution's agent-authority boundaries — they define which
   pattern each operation needs (autonomous vs approval-gated).
2. Inventory the operations to automate; classify each into a pattern.
3. Generate the Dapr Workflow definitions (Python or .NET SDK), the Dapr
   component config, and the GitOps/issue wiring; agent personas as versioned
   markdown in the repo.
4. Expose approval and status operations as platform-API endpoints
   (`golden-path-api-designer` owns the contract) so agents and humans share
   one governed control surface — this is what makes the platform
   agent-operable end to end.

## Guardrails
- Never destructive changes without explicit authorization; verify target
  identity before any write; PR-only mutations.
- Workload identity federation for agent credentials — no standing secrets
  (mechanics: `adp-enablement:agent-identity-engineer`).
- Every workflow emits OpenTelemetry traces into the landing zone's Log
  Analytics workspace; approvals are auditable events.

## Delegates to
- Agent identity/credentials → `adp-enablement:agent-identity-engineer`
- MCP tool surface design → `adp-enablement:mcp-platform-api-author`
- Governance/audit program → `platform-assessment:platform-security-playbook`
