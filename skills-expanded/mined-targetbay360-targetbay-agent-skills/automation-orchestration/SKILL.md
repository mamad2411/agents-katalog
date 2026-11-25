---
name: automation-orchestration
description: Use when part of a journey cannot live inside the marketing platform and the question is where each step should run — a trigger the platform does not emit, a wait longer than it supports, data it does not hold, a human approval step, an enrichment call, or a sync with a CRM, a spreadsheet or an advertising audience. Decides what stays inside the platform, what moves to an external workflow tool, and what the store gives up by moving it — suppression enforcement, frequency counting, attribution and reporting. Answers "should we build this inside the platform or outside it?", "how do we connect this to our other systems?" and "what triggers this journey?". Use automation-architect to design the journey itself and automation-strategy to decide which journeys should exist at all.
license: MIT
metadata:
  targetbay.display_name: Automation Orchestration
  targetbay.version: "1.0.0"
  targetbay.category: automation
  targetbay.requires: email_sms.automation, email_sms.event_stream, email_sms.event_tracking, email_sms.suppression_and_consent, email_sms.campaign_analytics, email_sms.store_profile
  targetbay.composes: automation-architect
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Automation Orchestration

## Purpose

Decide where each step of a journey runs — inside the platform, driven by an event the store pushes,
or in an external workflow tool — and state what each move outside costs.

A step moved outside for a good reason — a trigger the platform does not emit, data it does not hold
— takes the send with it, and suppression checking, frequency counting and attribution go too unless
something is put back. The opposite failure is rebuilding in an orchestrator what the platform
already does, creating a second source of truth that will disagree with the first.

This skill decides placement, not journey shape — that is
[automation-architect](../automation-architect/SKILL.md) — and it names no external product.

## When to Use

- A journey needs a trigger the platform does not emit
- A step needs data the platform does not hold, or an enrichment call to another system
- A human approval or review step has to sit inside a journey
- Contacts, events or audiences need to stay in step with a CRM, a spreadsheet or another system
- Deciding whether an existing external workflow should be moved back into the platform
- A journey already runs partly outside and nobody can say which layer enforces what

## When Not to Use

- The question is what shape a journey should take — how many steps, which branches, what timing.
  Use [automation-architect](../automation-architect/SKILL.md).
- The question is which journeys should exist at all. Use
  [automation-strategy](../automation-strategy/SKILL.md).
- A journey exists, runs entirely inside the platform, and underperforms. Use
  [automation-optimization](../automation-optimization/SKILL.md).
- The question is who approves generated content. Use
  [ai-content-governance](../ai-content-governance/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The journey's intended steps, in order | Placement is decided per step, not per journey | Blocked |
| Which triggers the platform emits, and which it does not | The first and most common reason a step moves outside | Blocked |
| Which layer enforces suppression, consent and frequency for an externally dispatched send | The cost of moving a send; a topology where neither enforces is refused | Blocked |
| Existing automations and their triggers | Whether a step already exists inside the platform | Blocked |
| Whether the platform can record and act on a store-pushed event | Decides whether a store-pushed trigger needs an orchestrator at all | Partial; assume it cannot and say so |
| Which systems hold the data a step needs | Whether an enrichment step is even possible | Partial |
| How attribution and reporting are read today | What breaks when a send leaves the platform | Partial; reporting impact unstated |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.automation` | Existing automations, their triggers and topology; what the platform can express natively |
| `email_sms.event_stream` | Which events the platform emits, and whether they can be subscribed to as a trigger surface |
| `email_sms.event_tracking` | Whether the store can push an event in, and whether one can drive a journey |
| `email_sms.suppression_and_consent` | Which enforcement exists on the platform side, and what an external send would bypass |
| `email_sms.campaign_analytics` | How results are attributed today, and what an external send loses |
| `email_sms.store_profile` | Plan limits and which integrations the store already has |

## Decision Process

```
1. List the journey's steps in order
2. For each step, ask in this order
     a. Can the platform do this natively?           ← if yes, stop; it belongs there
     b. Can the store push an event that makes it native?
     c. Does it need an external orchestrator?
3. For every step placed outside, name what moves with it
     the trigger · the wait · the data · the send
4. For every externally dispatched send, name the enforcing layer for each of
     suppression · consent · frequency · quiet hours
5. If any of those four has no enforcing layer, the topology is refused
6. State what reporting and attribution lose
7. Prefer the smallest boundary crossing that works
8. Produce the placement plan, with the reversal path for each external step
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/automation-rules.md](../../rules/automation-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Deterministic enforcement belongs to the platform (G10). An orchestrator never maintains its own
  suppression or consent state; it reads the platform's and acts on it.
- A send dispatched from outside may sit outside the platform's enforcement. Name the layer enforcing
  suppression, consent, frequency and quiet hours for every such send. **A topology where the answer
  for any of the four is "neither" is refused, not flagged** (G13, S2).
- An externally dispatched send still spends from the same frequency budget as everything else. It is
  counted, not exempt (F2, F3).
- Prefer the platform. Move a step outside only for a stated reason, and record the reason — "it was
  easier in the orchestrator" is not one (G7, G16).
- Read the existing topology before proposing a new one; a trigger may already exist inside the
  platform (G6, R17).
- Every external step states its reversal path: what it would take to bring it back inside. An
  external step with no reversal path is a permanent dependency and should be recognised as one.
- Do not assume a capability is present because an adjacent integration exposes something similar. A
  capability that has not been confirmed is not one you may plan against (S12).
- State what attribution and reporting lose when a send leaves the platform, before the move is
  approved rather than after (G14, G15).
- Name no external product. The placement decision does not depend on which orchestrator the store
  uses, and naming one makes the recommendation stale the moment they switch.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read existing automations and triggers, the event surface, enforcement layers, integrations | `read_only` |
| ANALYZE | Apply the placement test per step; identify what moves with each external step | `analysis` |
| PLAN | Placement per step, enforcement owner per external send, reporting impact, reversal paths | `plan` |
| PREVIEW | Present the topology with the enforcement table and what is given up | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the placement and accepts the stated losses | — |
| EXECUTE | Create or modify the platform-side automations and event subscriptions | `mutation` |
| — | **Activating a journey that dispatches sends from outside the platform** | `high_impact`, explicit approval |
| MEASURE | Whether enforcement held; whether attribution survived; per-step failure rates | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: each step with its placement and
the reason; for every externally dispatched send, the enforcing layer for suppression, consent,
frequency and quiet hours; what reporting and attribution lose; the reversal path per external step;
any topology refused and why; and the risks, including every capability assumed but unconfirmed. The
journey shape itself follows [the workflow schema](../../schemas/workflow.schema.json).

## Validation

- [ ] Placement decided per step, not per journey
- [ ] Platform-native checked first for every step (G7)
- [ ] Existing automations and triggers read before proposing a new one (G6, R17)
- [ ] Every externally dispatched send has a named enforcing layer for all four of suppression, consent, frequency and quiet hours (G13)
- [ ] Any topology with an unenforced dimension refused (S2)
- [ ] External sends counted against the same frequency budget (F2, F3)
- [ ] Reporting and attribution impact stated before approval (G14)
- [ ] Reversal path stated for every external step
- [ ] No capability planned against that has not been confirmed (S12)
- [ ] No orchestrator-side copy of suppression or consent state proposed (G10)
- [ ] No external product named
- [ ] Unconfirmed assumptions declared (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read the topology and event surface | `read_only` / `analysis` | None |
| Recommend the placement | `plan` / `recommendation` | None |
| Create or modify platform automations and subscriptions | `mutation` | Preview, then confirm |
| **Activate a journey that dispatches sends from outside the platform** | `high_impact` | **Explicit**, with the enforcement table accepted |
| **Any topology where suppression, consent, frequency or quiet hours has no enforcing layer** | — | **Refused.** Not planned by this skill (G13, S2) |

## Examples

**"Half of this journey needs data we keep in our own system — where should each step actually run?"**
Walks the steps and finds only two of six need the external data at all. Recommends keeping the
trigger, the waits and the sends inside the platform, and moving just the enrichment outside, pushing
its result back as an event rather than moving the send with it. That keeps every send under platform
enforcement and keeps attribution intact. Rejected: lifting the whole journey into the orchestrator,
which was the store's assumption and would have moved four sends outside suppression for the sake of
two enrichment calls.

**"We already run this in our workflow tool and want to add a second message."**
Reads the existing topology and finds the current send dispatched externally with no stated
enforcement owner for suppression or frequency. Refuses to plan the second message onto that
topology, because adding a send to an unenforced path doubles an existing exposure. Recommends first
routing the existing send back through the platform, then adding the second natively. Rejected:
adding the message as asked and noting the risk, which would have left the store believing the
problem was addressed.

## Failure Handling

| Situation | Response |
|---|---|
| Journey steps not specified | **Blocked.** Placement is a per-step decision; there is nothing to decide against |
| Existing automations unreadable | **Blocked.** Proposing a trigger without knowing what already fires risks two journeys competing for the same event (R16) |
| Cannot establish which layer enforces suppression for an external send | **Blocked.** This is the question the skill exists to answer; guessing it is the failure mode (S12) |
| `email_sms.event_stream` unavailable or unconfirmed | **Partial.** Plan on the assumption that events cannot be subscribed to as triggers, state the assumption, and prefer schedule-driven placement |
| `email_sms.event_tracking` unavailable or unconfirmed | **Partial.** Plan on the assumption that a store-pushed event cannot drive a platform journey, which pushes more steps outside; say so explicitly |
| Attribution model unknown | **Partial.** State that the reporting impact of an external send could not be assessed (G15) |
| Store insists on an unenforced topology | **Refused.** State which dimension is unenforced and what it permits, record the refusal, and offer the smallest change that makes it enforceable (S8) |

Degraded outcomes set `status` and populate `unmet_requirements`.
