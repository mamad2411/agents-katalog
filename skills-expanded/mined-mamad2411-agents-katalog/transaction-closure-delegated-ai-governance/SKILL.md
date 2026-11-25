---
name: transaction-closure-delegated-ai-governance
description: Evaluate and govern delegated AI agents by transaction closure rather than mere task completion. Covers the shift from super-apps to agent economies, the contestable transaction closure framework, the ClosureBench evaluation concept, and the governance principles for agents that act on behalf of humans. Use when designing agent governance frameworks, evaluating whether an agent has truly completed a delegated transaction, building agent accountability systems, or establishing dispute-resolution infrastructure for agentic commerce. NOT for task-completion benchmarking of non-delegated agents or for payment protocol selection.
---

# Transaction Closure for Delegated AI Governance

## Overview

Delegated AI agents have evolved from super-app assistants into autonomous economic actors that execute multi-step transactions on behalf of humans. The conventional evaluation paradigm — measuring task completion (did the agent finish the requested steps?) — is structurally insufficient for delegated commerce. A new position paper argues that delegated AI must be evaluated and governed by **transaction closure**: the verifiable, contestable, and auditable completion of an end-to-end transaction that satisfies the human's original intent, not just the agent's step sequence. This skill operationalizes that framework for A-Tech.

## When to Use

- Designing governance or accountability frameworks for AI agents that act on human behalf
- Evaluating whether an agent has truly closed a transaction vs merely completed its steps
- Building dispute-resolution or audit infrastructure for agentic commerce
- Establishing evaluation criteria for delegated agents in regulated or high-stakes environments
- Distinguishing super-app task completion from agent-economy transaction closure
- Creating agent handoff protocols where closure must be verified before responsibility transfers

NOT for:
- Benchmarking agents that execute tasks without human delegation (use ai-agent-evaluation-framework-2026)
- Payment protocol specification (use agentic-payments-protocol-ap2 or agent-pay-card-network-integration)
- Trust-layer cryptography (use verifiable-intent-agentic-trust-layer)
- Agent marketplace economics (use agent-marketplace-builder-economy)

## Core Process / Workflow

### 1. Understand the Paradigm Shift: Task Completion → Transaction Closure

The evolution from super-apps to agent economies changes what "done" means.

| Dimension | Task Completion (Super-App Era) | Transaction Closure (Agent Economy) |
|-----------|--------------------------------|-------------------------------------|
| Unit of evaluation | Did the agent perform the requested steps? | Did the transaction achieve the human's intent with verifiable, contestable proof? |
| Accountability | Agent reported success | All parties can verify and contest closure |
| Failure mode | Step executed incorrectly | Closure claimed without intent satisfaction |
| Audit trail | Logs of agent actions | Tamper-resistant evidence binding intent → action → outcome |
| Human role | Approves each step | Sets constraints; closure is verified against them |
| Economic scope | Single app context | Cross-protocol, cross-merchant, cross-agent |

**The core problem:** An agent can complete every step (search, select, pay, confirm) and still fail to close the transaction in a way that satisfies the human's original intent — wrong item, wrong price, unauthorized scope expansion, or a dispute with no resolution path.

### 2. The Four Pillars of Transaction Closure

A delegated transaction is "closed" only when all four conditions hold:

1. **Intent Satisfaction** — The outcome matches what the human actually authorized, including constraints (spend limits, merchant restrictions, item specifications). Not just what the agent interpreted.
2. **Verifiable Evidence** — A tamper-resistant record binds the human's identity, their specific instructions, and the transaction outcome into a single auditable artifact that any party can inspect.
3. **Contestability** — Any party (human, merchant, payment network) can raise a dispute and the evidence trail supports resolution. Closure is not final until the contestation window passes or is resolved.
4. **Portability** — The closure record travels with the transaction across protocols, merchants, and agents. It is not locked to a single platform's logs.

### 3. The ClosureBench Evaluation Concept

Traditional agent benchmarks (SWE-bench, GAIA, τ-bench) measure task completion: did the agent produce the correct output? Delegated agents need a different evaluation surface.

**ClosureBench (proposed) evaluates:**

| Criterion | What it measures | Example |
|-----------|-----------------|---------|
| Intent alignment | Does the outcome match the human's stated constraints? | Agent bought a hotel room within budget, but wrong dates — task complete, closure fails |
| Constraint adherence | Did the agent stay within authorization bounds? | Agent exceeded spend limit by 12% because "the better option was worth it" |
| Evidence completeness | Can a third party reconstruct what happened? | Audit trail missing the agent's reasoning for choosing merchant B over A |
| Contestation resolution | Can disputes be resolved from the evidence? | Human disputes charge; merchant and agent logs disagree on authorization scope |
| Cross-protocol portability | Does the closure record survive platform transitions? | Agent initiated on Platform X, completed on Platform Y; closure record fragmented |

### 4. Governance Architecture for Delegated Agents

```
┌─────────────────────────────────────────────────────────┐
│                 HUMAN (Delegator)                        │
│  Sets intent, constraints, authorization scope           │
└──────────────┬──────────────────────────────────────────┘
               │ Verifiable Intent (constraints signed)
               ▼
┌─────────────────────────────────────────────────────────┐
│              AGENT (Delegate)                            │
│  Executes within constraints, produces fulfillment       │
│  evidence at each step                                    │
└──────────────┬──────────────────────────────────────────┘
               │ Fulfillment credentials (key-bound, scoped)
               ▼
┌─────────────────────────────────────────────────────────┐
│           CLOSURE VERIFICATION LAYER                     │
│  1. Intent satisfaction check (outcome vs constraints)   │
│  2. Evidence completeness audit                          │
│  3. Contestation window opens                            │
│  4. If uncontested → closure finalized                   │
│  5. If contested → dispute resolution protocol           │
└──────────────┬──────────────────────────────────────────┘
               │ Closure record (portable, tamper-resistant)
               ▼
┌─────────────────────────────────────────────────────────┐
│    MERCHANT / PAYMENT NETWORK / OTHER AGENTS             │
│  Verify closure record independently                     │
└─────────────────────────────────────────────────────────┘
```

### 5. The Three Delegation Modes and Their Closure Requirements

| Mode | Human Presence | Constraint Binding | Closure Verification |
|------|---------------|-------------------|---------------------|
| **Immediate** | Human present at checkout | Final values signed by human | Two-layer: human signs final values; agent presents fulfillment |
| **Autonomous (bounded)** | Human absent; agent acts within bounds | Constraints signed up front; agent key bound | Three-layer: human signs constraints; agent signs fulfillment within bounds; closure verified against constraints |
| **Open-ended** | Human absent; agent has broad mandate | Minimal constraints; relies on agent judgment | Highest risk; requires real-time monitoring, spend alerts, and post-hoc contestation |

**Design principle:** Autonomous mode is the production default for agentic commerce. The constraint layer is what makes closure contestable rather than merely trust-based. Open-ended mode should be avoided for financial transactions until closure infrastructure matures.

### 6. Constraint Types for Transaction Closure

The framework treats constraints as first-class authorization limits that the closure verification layer must validate:

1. **Spend limits** — maximum total, per-transaction, or per-merchant
2. **Merchant restrictions** — allow/deny lists, category restrictions
3. **Item specifications** — required attributes, quality thresholds
4. **Time windows** — transaction must complete within a deadline
5. **Geographic scope** — jurisdiction or delivery location limits
6. **Confirmation thresholds** — human re-confirmation required above a value
7. **Reversibility** — transaction must be cancelable within a window
8. **Disclosure scope** — what information the agent may share with merchants

**Critical rule:** Unknown constraint types in open mandates must be rejected, not silently ignored. An unrecognized constraint can silently unbound the agent's authority.

### 7. A-Tech Application Matrix

#### A-Coder
- **Agent-generated code as a transaction:** When an AI coding agent produces code on behalf of a developer, the "closure" is not just "code was generated" but "the code satisfies the developer's intent, is verifiable, and is contestable if it produces unexpected behavior." Apply the four pillars: intent satisfaction (does the code do what was asked?), verifiable evidence (provenance trail), contestability (can the developer dispute and revise?), portability (does the provenance survive across IDE sessions?).
- **Constraint-bound code generation:** Spend limits become token budgets; merchant restrictions become approved dependency sources; confirmation thresholds become review checkpoints for security-sensitive changes.

#### Be Practical
- **Curriculum module:** "From task completion to transaction closure: governing delegated AI." The paradigm shift, the four pillars, the three delegation modes, the constraint taxonomy.
- **Exercise:** Design the closure verification layer for an agent that books travel on behalf of a user. Identify which constraints are needed. Map what evidence each party needs. Design the contestation flow.

#### Builder's Club
- **Reference architecture:** Open-source closure verification layer that any agent marketplace can adopt. The layer sits between the agent and the merchant/payment network, validates fulfillment against constraints, and produces a portable closure record.
- **Community standard:** Propose transaction closure as a governance standard for Builder's Club agent marketplace participants.

## Cross-References

- **`verifiable-intent-agentic-trust-layer`** — The cryptographic trust layer that makes transaction closure technically possible (SD-JWT credential chains, selective disclosure, constraint validation). This skill defines what closure means; that skill defines how to prove it.
- **`ai-agent-evaluation-framework-2026`** — The hierarchical evaluation framework for agents. This skill extends it with the transaction-closure evaluation dimension for delegated agents.
- **`agentic-payments-protocol-ap2`** and **`agent-pay-card-network-integration`** — The payment infrastructure. Transaction closure is the governance layer above payment execution.
- **`agentic-commerce-trust-design`** — The trust-gap diagnosis for agent shopping. Transaction closure is the structural fix for the conversion gap.
- **`earning-agents-autonomous-agent-economy`** — Earning agents need closure verification to establish reputation and resolve disputes with other agents.
- **`agentic-payments-compliance-2026`** — The compliance layer. Transaction closure provides the auditable evidence that compliance requires.

## References

- See [references/closure-governance-framework.md](references/closure-governance-framework.md) for the detailed framework, the ClosureBench evaluation criteria, the constraint specification, and the delegation-mode comparison.