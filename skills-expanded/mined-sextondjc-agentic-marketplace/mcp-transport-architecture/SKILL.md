---
name: mcp-transport-architecture
description: Use when MCP transport and session architecture decisions must be made deterministically across stdio, SSE, and streamable-http.
---

# MCP Transport Architecture

## Specialization

Define transport architecture decisions with explicit trade-offs, session behavior, and deployment constraints.

## Trigger Conditions

- A server transport is being selected or changed.
- Timeout/session behavior is inconsistent across environments.
- Deployment topology requires transport hardening.

## Hard Constraints

- Transport behavior must align with official MCP documentation and specification.
- Security and operability controls must be explicit.

## Inputs

- Target client ecosystem.
- Environment topology.
- Latency and concurrency expectations.
- Operational constraints.

## Required Outputs

- Transport decision record.
- Session and timeout policy.
- Failure-mode and recovery contract.

## Deterministic Workflow

1. Classify client and environment constraints.
2. Evaluate transport options against constraints.
3. Select primary and fallback transport modes.
4. Define session lifecycle and timeout semantics.
5. Publish risk and mitigation summary.

## Decision Matrix Template

| Criterion | stdio | SSE | streamable-http | Decision Notes |
|---|---|---|---|---|
| Local development fit | <score> | <score> | <score> | <notes> |
| Remote deployment fit | <score> | <score> | <score> | <notes> |
| Observability and ops | <score> | <score> | <score> | <notes> |

## Done Criteria

- Primary and fallback transport decisions are explicit.
- Session and timeout policy is complete.
- Failure-mode contract is documented.
