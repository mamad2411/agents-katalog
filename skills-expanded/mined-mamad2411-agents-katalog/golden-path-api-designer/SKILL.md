---
name: golden-path-api-designer
description: >-
  Design the golden-path-as-a-service API: the contract-first platform API
  behind APIM (Azure Front Door later for global/WAF) whose endpoints perform
  golden-path operations (create service, provision datastore, promote
  environment, approve change), and the thin platform MCP server over it that
  every agent runtime consumes. Use for platform API design on Azure, APIM
  products and policies for agent callers, golden-path endpoint contracts,
  approval endpoints for durable workflows, or planning the platform MCP
  server. Composes the adp-enablement contract, identity, and MCP skills with
  the Azure/APIM/Radius specifics.
---

# Golden-Path API Designer

## Purpose
The target state: golden paths are **an API, not templates developers copy**.
Repo-stamping (`radius-golden-path-builder`) is the transitional mechanism;
this skill designs its replacement — one governed API surface, fronted by
APIM, that both humans and agents call, with a platform MCP server as the
agent-facing adapter. Because the API owns governance, every MCP client
(Claude, Copilot, Codex) inherits identical guardrails.

## The three planes (and who designs each)
```
agents (any MCP client)
  │  MCP tools: create_service, provision_datastore, get_disposition,
  │             promote_environment, approve_change, get_run_status …
  ▼
platform MCP server            ← adp-enablement:mcp-platform-api-author
  │  OAuth2 client-credentials, short-lived, scoped
  │                            ← adp-enablement:agent-identity-engineer
  ▼
Golden-Path API on APIM        ← adp-enablement:agent-api-contract-designer
  │  contract-first OpenAPI, tolerant versioning, recoverable errors
  ▼
platform orchestrator backend  ← this skill: which Radius/AVM operation each
  │                              endpoint performs; approval hooks into
  ▼                              Dapr workflows (agentic-ops-builder)
Radius control plane + landing zones
```
This skill is deliberately thin: it invokes the three `adp-enablement` skills
for contract, identity, and MCP design, and adds only the Azure specifics.

## Azure specifics this skill owns
- **APIM surface:** products and subscription model vs OAuth2-only for agent
  callers; policy fragments (rate limits per agent principal, JWT validation,
  audit logging to Log Analytics); versioning path (`/platform/v1/...`).
- **Front Door timing:** add AFD in front of APIM only when global entry,
  WAF, or multi-region APIM arrives — AFD is not an API gateway; it
  complements APIM, never replaces it. Workload APIs and the platform API
  share the same gateway plane (the golden path's APIM route recipe already
  registers backends there).
- **Endpoint-to-operation mapping:** each endpoint's backend behavior in
  terms of Radius (`rad deploy`, recipe selection, environment binding),
  AVM deployments, and GitOps PRs — including which operations are
  synchronous, which return a workflow-run handle, and which pause on an
  approval event.
- **Approval endpoints:** `POST /approvals/{id}` closes the loop with
  `agentic-ops-builder`'s external-event workflows, making approvals part of
  the same governed API rather than a side channel.
- **Dogfooding:** the orchestrator backend itself deploys on the golden path
  (ACA backend + APIM route + Dapr) — the platform's first workload.

## Workflow
1. Read the constitution (authority boundaries decide which endpoints exist
   and which require approval semantics).
2. Enumerate golden-path operations from the current builder/templates; each
   becomes an endpoint with an SDD spec.
3. Run the three delegated designs (contract → identity → MCP surface).
4. Emit: OpenAPI spec, APIM policy set, MCP tool schema list (mirroring
   OpenAPI operations one-to-one), orchestrator backend spec, rollout ADR
   (template path -> API path migration).

## Guardrails
- Contract before backend — the OpenAPI spec is the SDD artifact; no endpoint
  ships without it.
- The MCP server carries no business logic or authorization of its own; if a
  rule matters, it lives in the API where every caller meets it.
- All mutating endpoints emit auditable events; destructive operations are
  approval-gated per the constitution.
