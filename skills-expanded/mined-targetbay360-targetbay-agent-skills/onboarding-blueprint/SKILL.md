---
name: onboarding-blueprint
description: Use when a store is new to TargetBay and the question is what to set up first across all three products — onboarding email, SMS, reviews, loyalty and onsite personalization as one sequence rather than four independent setups. Decides what each product contributes, what it must wait for and why, who owns contact with a customer when two products both want to reach them, and what observation would justify each next step. Produces a sequenced ninety-day plan with every borrowed value labelled; provisions nothing.
license: MIT
metadata:
  targetbay.display_name: Cross-Product Onboarding Blueprint
  targetbay.version: "0.3.0"
  targetbay.category: planning
  targetbay.requires: onboarding.store_context, onboarding.intake
  targetbay.composes: context-audit, onboarding-intake
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Cross-Product Onboarding Blueprint

## Purpose

Turn what is known about one store into the order in which its three products get built.

Four products configured independently produce four correct plans and one bad outcome: three of them
message the same customer, and the one that does not is the one that could have started immediately. The
blueprint exists because the sequence is a decision nobody makes when each product is set up on its own.

## When to Use

- Onboarding a store across more than one TargetBay product
- A store has just signed up or migrated and nothing has been configured yet
- An existing store is adding products and the contact load needs reconciling before it does
- The question is "what should we set up first?" and the answer spans products

## When Not to Use

- Only email and SMS are in scope. Use
  [store-onboarding](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/store-onboarding/SKILL.md).
- The store has an established programme across products and the question is what to improve. Use each
  product's audit skill, for example
  [review-program-audit](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-reviews/skills/review-program-audit/SKILL.md).
- Nothing is known about the store yet. Run [context-audit](../context-audit/SKILL.md) first; a blueprint
  built without it is the default checklist this plugin exists to replace (G1).
- The plan already exists and needs building. Use
  [onboarding-provisioning](../onboarding-provisioning/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The context audit's partition | Determines what is decidable at all | Blocked |
| Capability readiness per product | A product with no reachable capabilities cannot be sequenced into the plan | Blocked |
| Existing coverage per product | Prevents proposing what already exists (G5) | Partial; treat as unknown and say so |
| Consent state per channel | Decides what may be sent and to whom (S7) | Blocked for any sending step |
| Stated constraints from intake | Capacity, margin, brand policy, restricted markets | Partial; say which decisions are unconstrained as a result |
| Detected vertical | Selects the playbook overlay for provisional defaults | Partial; use the general overlay or none |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onboarding.store_context` | Catalogue and customer shape, vertical, brand, coverage, readiness |
| `onboarding.intake` | Objectives and constraints the platform cannot observe |

## Decision Process

```
1. Read the context audit         ← what is decidable, what is borrowed, what is absent
2. Select the playbook overlay    ← or none, when vertical confidence is thin
3. Rank products by what they spend, not by what they are worth
4. Compute the contact budget     ← across all three products, one number (X1, X7)
5. Assign moment ownership        ← who may message at each lifecycle moment (X2)
6. Sequence the horizon           ← capture before consumption, reversible before irreversible
7. State each step's precondition ← an observation, never a date (SQ4)
8. Set the review point           ← when the provisional values become derivable
```

Step 3 is where the blueprint stops being a checklist. **Onsite personalization goes first in almost
every plan** — not because it is the most valuable, but because it spends none of the contact budget and
waits on no evidence the store does not have (X3, SQ2). **Review triggers go early** because capture is
not retroactive: a trigger armed on day sixty cannot ask about a day-ten order (SQ1). **Lifecycle email
and SMS follow**, gated on consent and deliverability rather than on the calendar. **Loyalty goes last**,
because tier thresholds and points economics need a repeat rate the store does not yet have, and a
programme built on invented thresholds is one nobody can later explain (SQ6).

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/contact-ownership-rules.md](../../rules/contact-ownership-rules.md),
[../../rules/sequencing-rules.md](../../rules/sequencing-rules.md),
[../../knowledge/onboarding-sequence.md](../../knowledge/onboarding-sequence.md).

- **State the maximum weekly contact per customer across all three products, as a number.** A blueprint
  that cannot is not approvable (X7). "Each product is within its own limits" is not that number.
- **Assign every lifecycle moment to exactly one product** (X2). A moment with two owners is a customer
  with two messages.
- **Onsite spends no contact budget** and is sequenced accordingly (X3).
- **Capture before consumption** (SQ1).
- **Every step's precondition is an observation, never a date** (SQ4, G14). "After 200 orders", not "in
  week six".
- **A provisional value may not gate an irreversible step** (SQ5). Either the step waits for the value to
  be derived, or the step is made reversible.
- **Label every borrowed value as provisional, with what would replace it** (G3, G12, G14).
- **Do not propose what already exists** (G5). Existing coverage is read first and the blueprint works
  around it.
- **Never plan an unconfirmed send capability as certain** (S8). SMS in particular appears as a labelled
  branch conditional on the capability manifest, not as a planned channel.
- **Never assume migrated consent** (S7). An imported list gets a ramp, and its first send is its own approval.
- If the platform cannot enforce one contact budget across products, say so on the blueprint's face and
  mark the number provisional (X9).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read the audit, readiness, coverage, consent and stated constraints | `read_only` |
| ANALYZE | Rank products by what they spend; compute the contact budget; assign moment ownership | `analysis` |
| PLAN | Sequence the horizon with a precondition per step | `plan` |
| PREVIEW | Present the sequence, the budget, the ownership map and every provisional value | `plan` |
| VALIDATE | Run the checks below | `plan` |
| APPROVE | Human approves the blueprint | — |
| EXECUTE | Delegated to [onboarding-provisioning](../onboarding-provisioning/SKILL.md) | `mutation` |
| — | **Any activation or send** | `high_impact`, explicit and per resource |
| MEASURE | At the review point, re-derive the provisional values and revise the sequence | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) at `risk_level: plan` containing: the sequenced
plan across the horizon with each step's owning product and its precondition in observable terms; the
maximum weekly contact per customer across all three products, with how it was computed; the
moment-ownership map; every provisional value flagged with what would replace it; the consent and
deliverability posture including any ramp for an imported list; which products were deferred and what
evidence each is waiting for; and the review point.

## Validation

- [ ] Maximum weekly contact per customer across all three products is stated as a number (X7)
- [ ] Every lifecycle moment has exactly one owning product (X2)
- [ ] Every step's precondition is an observation, not a date (SQ4)
- [ ] No irreversible step gated on a provisional value (SQ5)
- [ ] Every provisional value labelled, with its replacing observation (G3, G14)
- [ ] Capture-shaped configuration sequenced ahead of consumption-shaped (SQ1)
- [ ] Existing coverage read, and nothing proposed that duplicates it (G5)
- [ ] Consent read per channel; no send planned against unknown consent without a ramp (S7)
- [ ] No unconfirmed send capability planned as certain (S8)
- [ ] Each deferred product carries the evidence it is waiting for (SQ7)
- [ ] Review point stated in observable terms
- [ ] The plan would read differently for a different store (G1)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Audit, analyse and sequence | `read_only` / `analysis` / `plan` | None |
| Approve the blueprint | `plan` | Preview, then confirm |
| Create the resources it describes | `mutation` | Delegated to provisioning; preview then confirm |
| **Activate anything** | `high_impact` | **Explicit, per resource, never in bulk** (S3) |
| **First send to an imported list** | `high_impact` | **Explicit**, with the ramp and recipient count stated |

The first send to a migrated list deserves more scrutiny than any later one: it creates the store's
sending reputation, and reputation is far slower to repair than to build (S14).

## Examples

**"We just signed up. Set up everything across email, reviews, loyalty and onsite."**
The audit reports a 1,840-product beauty catalogue, 14,000 migrated contacts whose consent is mostly
unknown, no order history on the platform, and no existing coverage. The blueprint starts with onsite
recommendations and review triggers — neither spends contact budget, and the review trigger must be armed
before the first orders arrive or those asks are lost. Lifecycle email follows, restricted to the 4,102
contacts with granted consent and ramped over several sends. SMS appears as a branch, unplanned, because
the manifest reports the capability unverified. Loyalty is deferred with its reason stated: tier
thresholds need a repeat rate, and the store has none. Maximum weekly contact is stated as three, taken
from the stated constraint. Review point: 200 customers with a second purchase.

**"Both Reviews and Email want to message customers after delivery. Which wins?"**
Post-purchase and delivery are Reviews' moment (X2), so the first review request belongs to Reviews and
Email & SMS does not message into that window. The blueprint states it once, in the ownership map, rather
than leaving each product to discover the collision at send time — and the aggregate number in the
approval request reflects the resolution rather than the sum.

## Failure Handling

| Situation | Response |
|---|---|
| Context audit unavailable | **Blocked.** A blueprint without it is a default checklist (G1) |
| Contact budget cannot be computed across products | **Partial.** State it provisionally with its `replaced_by`, and say plainly on the blueprint that it is planned rather than enforced (X9) |
| Consent state unavailable | **Blocked** for every sending step. Non-sending steps may still be sequenced |
| A product's capabilities are unreachable | Sequence the rest; record the product as deferred with the capability it is waiting for, not as unnecessary |
| SMS capability unverified | Plan email-only; show SMS as a conditional branch (S8) |
| No order history at all | **Partial.** Deliver sequencing, catalogue-shape decisions, stated constraints and labelled playbook defaults. Offer no derived thresholds |
| Vertical confidence thin | Use the general overlay or none, and say which (G2) |
| Existing coverage found | Not a blocker. Work around it; propose replacing something only as its own `destructive` finding with its own approval (S6) |

Degraded outcomes set `status` and populate `unmet_requirements`. This skill delivers a smaller honest
plan rather than a complete invented one.
