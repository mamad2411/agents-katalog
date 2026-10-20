---
name: leeway-message-ingress-authority
description: Per-message LeeWay ingress guard. Before substantive reasoning or execution, checks whether the current session has a valid LeeWay skill authority receipt, refreshes canonical skills only when missing/stale/contradictory, preserves Formula evaluator exposure state, and routes the original user message through Context, Formula, Universal Capability Kernel, Tool Gateway, and Conversation Vault when available. Check every message; reload only when necessary.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  mode: always-on-message-ingress
  stage: post-bootstrap-pre-context
  repository: 4citeB4U/LeeWay-Agent-Skills
  compatibility: Agent Skills / GitHub Copilot / Codex / MCP / OpenCode / Hermes
---

# LeeWay Message Ingress Authority

## Per-message law
For every user message, before substantive reasoning, execution, or response, ask:

> Do I possess a valid current-session LeeWay Skill Authority Receipt?

**Check every message. Reload only when necessary.**

## Valid receipt
A valid `LEEWAY_SKILL_SESSION_RECEIPT` establishes `4citeB4U/LeeWay-Agent-Skills` and, when available, current authority ref/commit plus verified core-stack availability.

The receipt must also preserve the current `formulaEvaluatorState`, `formulaExecutionState`, `toolGatewayState`, and `conversationVaultState` when those capabilities are known.

The receipt is invalid when missing, unknown, stale, contradictory, incompatible with the current runtime/session, or when canonical authority is known to have changed.

## Refresh path
If invalid:

1. Retrieve/verify the canonical repository using authorized host capabilities.
2. Verify at minimum:
   - `AGENTS.md`
   - `leeway-bootstrap-authority`
   - `leeway-continuity-authority`
   - `leeway-message-ingress-authority`
   - `leeway-context-engineering`
   - `leeway-formula-governance`
   - `leeway-agent-operating-loop`
   - `leeway-capability-resilience`
   - `leeway-universal-capability-kernel`
   - `leeway-skill-orchestrator`
   - `leeway-parallel-workplane`
   - `leeway-veritas`
   - `leeway-receipt-authority`
   - `leeway-learning-ledger`
   - `leeway-skill-lifecycle-governance`
   - `leeway-reference-authority`
   - `leeway-tool-gateway`
   - `leeway-conversation-vault`
   - `leeway-human-conversation`
   - `leeway-og-expressive-identity`
3. Verify `leeway-quantum-readiness` when quantum/hybrid relevance exists.
4. Re-evaluate Formula evaluator exposure using `config/leeway-formula-evaluator-contract.yaml`.
5. Re-discover Tool Gateway and Conversation Vault only when the runtime exposes or changes those adapters.
6. Establish/update the session receipt.
7. Return to the original user message without losing or replacing it.

If authority remains current, reuse it. Do not repeatedly download unchanged full skill files merely to prove diligence.

## Formula evaluator boundary
If no canonical evaluator or authorized adapter is actually exposed:

`FORMULA_EVALUATOR_STATE = UNEXPOSED`
`FORMULA_EXECUTION_STATE = NOT_EXECUTED`

That state does not block governed reasoning, cross-domain capability weaving, reference work, non-Formula runtime tools, Tool Gateway use, Conversation Vault capture, or LeeWay delivery.

Never upgrade `UNEXPOSED` to `AVAILABLE`, `AUTHORIZED`, or `EXECUTED` without evidence.

## Governed route
`Bootstrap → Continuity → Ingress → Context/Phi-C64 → Formula/Phi-D → Agent Operating Loop → Capability Resilience → Universal Capability Kernel → Skill Orchestrator → Task Capability Weave → Tool Gateway when available → Focal Execution → Veritas → Receipt → Conversation Vault when available → LeeWay Delivery`

The kernel may let many micro-capabilities shape one answer while keeping heavy full-skill/runtime execution bounded.

## Fail closed
Never claim a skill was loaded when it was unavailable. Never claim Formula execution merely because Formula Governance was loaded. Never claim Tool Gateway execution merely because a connector exists. Never claim historical conversation possession merely because a vault exists.

If refresh is required and canonical authority cannot be reached:
`LEEWAY_SKILL_AUTHORITY = BLOCKED`

Preserve the strongest verified continuity available and distinguish remembered context from live authority.

## Behavioral proof
Successful loading should show up through continuity, provenance discipline, Formula/execution separation, evaluator-state honesty, cross-domain capability weaving, source-aware explanation, governed tool use when available, conversation-evidence discipline, technical precision, linchpin framing, and canonical LeeWay expressive identity.

Do not expose hidden chain-of-thought. Expose receipts, decisions, sources, tests, measurements, and execution states when material.
