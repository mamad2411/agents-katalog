---
name: cma-production-guardrails
description: Enterprise guardrails for autonomous agents based on Claude Managed Agents. Implements enforced session spend ceilings, requires_action human approval gates, geographic data pinning, and stateful rollback.
---

# CMA Production Guardrails Architecture

## Core Guardrail Mechanisms
1. **Enforced Spend Ceilings:** Sets strict per-session budget limits (session.budget_reached). The agent automatically halts when the budget threshold is hit.
2. **Human-in-the-Loop (requires_action):** High-risk tool calls (database write, money movement, PR merge) pause the session and emit a webhook for human authorization.
3. **Inference Geo Pinning:** Enforces data residency by restricting model execution to designated geographic regions (inference_geo).
4. **Prompt Versioning & Rollback:** Server-side prompt definitions allow instantaneous rollbacks without redeploying application code.
