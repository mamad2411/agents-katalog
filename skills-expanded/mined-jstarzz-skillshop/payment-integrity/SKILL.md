---
name: payment-integrity
description: "Review payment workflows so retries, ambiguous gateway outcomes, webhooks, local state and settlement cannot create duplicate charges or false success. Use when payment integration, gateway state, settlement reconciliation."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "security"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Payment Integrity

Review payment workflows so retries, ambiguous gateway outcomes, webhooks, local state and settlement cannot create duplicate charges or false success.

## Activate when

- payment integration
- gateway state
- settlement reconciliation

## Focus

- Primary mission: Review payment workflows so retries, ambiguous gateway outcomes, webhooks, local state and settlement cannot create duplicate charges or false success.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Model the authoritative payment lifecycle and distinguish intent, gateway request, approval/authorization, capture/sale, settlement, refund and failure according to the actual gateway.
2. Ensure client retries and double-submits cannot create duplicate financial operations.
3. Persist enough local intent/correlation state to reconcile ambiguous timeout-after-charge outcomes instead of blindly marking them failed.
4. Treat gateway webhooks and query/reconciliation responses as repeatable inputs; updates must be idempotent.
5. Test duplicate submit, duplicate webhook, delayed/out-of-order webhook, gateway timeout, DB failure before/after gateway success and reconciliation after process restart.
6. Verify displayed local success never exceeds what the authoritative financial state supports.
7. Record gateway transaction IDs/correlation safely without leaking sensitive payment data.

## Deliverables

- Verified security findings
- Attack/data-flow reasoning
- Concrete remediation and regression checks
- A result that directly satisfies: Review payment workflows so retries, ambiguous gateway outcomes, webhooks, local state and settlement cannot create duplicate charges or false success.

## Common failure modes

- Checklist dumping without reachable evidence
- Relying on UI hiding for authorization
- Logging or persisting secrets while testing security
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
