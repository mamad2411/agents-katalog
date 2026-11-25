---
name: automation-architect
description: Use when designing or restructuring an automation journey — a welcome series, post-purchase flow, abandoned cart or browse journey, replenishment, win-back or VIP track. Decides how many separate automations one objective needs, whether to split a journey by audience, product, category, order value or price band, how many nodes it should have, when each step fires and which channel carries it. Answers "should this be one automation or several?" and "should we split this flow?". Use automation-strategy when the question is which automations the store should have at all, and automation-optimization when an existing journey needs tuning rather than reshaping.
license: MIT
metadata:
  targetbay.display_name: Automation Architect
  targetbay.version: "2.1.0"
  targetbay.category: automation
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.automation, email_sms.automation_analytics, email_sms.suppression_and_consent
  targetbay.composes: audience-discovery, product-recommendation-strategy, offer-strategy
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Automation Architect

## Purpose

Turn one automation objective into a concrete, justified topology: how many journeys, for whom, with
which nodes, in what order, at what intervals, on which channels.

This skill exists because automation architecture is a decision problem that agents habitually solve by
template. The two assumptions it must never make:

- **one objective = one automation**
- **one automation = a fixed number of nodes**

Both numbers are derived from the store. Every variant and every node in the output carries the reason it
exists, and variants that were considered and rejected are recorded with why.

## When to Use

- A store wants a journey built for a specific objective: post-purchase, welcome, replenishment, cart or
  browse abandonment, win-back, VIP, subscription lifecycle
- An existing journey needs restructuring rather than tuning — the shape is wrong, not the copy
- The question is "should this be one automation or several?"
- A decision is needed on whether an audience, product, category, price band or attribute warrants its own
  journey
- Another skill needs a topology designed as part of a larger plan

## When Not to Use

- The store needs a portfolio-level answer — which automations exist, which are missing, which should be
  merged. Use [automation-strategy](../automation-strategy/SKILL.md).
- An existing automation is structurally sound and needs performance tuning. Use
  [automation-optimization](../automation-optimization/SKILL.md).
- The trigger is a date or business event rather than a customer behaviour. That is a campaign — see
  [../../knowledge/campaign-principles.md](../../knowledge/campaign-principles.md).
- The real question is who to target, not what to build. Use
  [audience-discovery](../audience-discovery/SKILL.md).
- No automation capability is available. Say so and stop; do not design something that cannot be built.
- The question is which items a node should feature. Use
  [product-recommendation-strategy](../product-recommendation-strategy/SKILL.md), which this skill
  composes — the journey decides that a node recommends products, not which ones.
- The question is what incentive a node carries. Use [offer-strategy](../offer-strategy/SKILL.md),
  which this skill composes.
- The journey is designed and two of its messages now contend with a campaign. Use
  [campaign-conflict-resolver](../campaign-conflict-resolver/SKILL.md).
- A step cannot live inside the platform at all. Use
  [automation-orchestration](../automation-orchestration/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Store profile, vertical, catalogue shape | Determines which variant axes are even plausible | Blocked |
| Existing automations and their topology | Prevents duplicating or competing with what exists | Blocked — see [../../rules/global-rules.md#G6](../../rules/global-rules.md) |
| Lifecycle distribution and stage thresholds | Sizes each candidate variant | Blocked |
| Order history: repeat interval, AOV distribution | Supplies timing and value bands | Timing becomes a guess; declare it |
| Product attributes, categories, price bands | Determines product-driven variants | Product variants not proposed |
| Existing automation performance per node | Shows where current journeys lose people | Partial; no evidence for restructuring |
| Channel consent and engagement by segment | Determines channel per node | Plan email-only and say why |

## Required MCP Capabilities

Declared in frontmatter; defined in [../../capabilities.yaml](../../capabilities.yaml). Concrete TargetBay
Email & SMS MCP tool mappings are **TODO** — see
[../../docs/mcp-integration.md](../../docs/mcp-integration.md).

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, catalogue size, sending posture |
| `email_sms.customer_intelligence` | Lifecycle distribution, value bands, engagement, channel preference |
| `email_sms.product_intelligence` | Categories, attributes, price bands, affinity |
| `email_sms.order_intelligence` | Repeat interval, purchase frequency, AOV |
| `email_sms.segmentation` | Resolving and sizing candidate audiences |
| `email_sms.automation` | Reading existing topology; creating the designed journeys after approval |
| `email_sms.automation_analytics` | Per-node drop-off in existing journeys |
| `email_sms.suppression_and_consent` | Channel eligibility per audience |

## Decision Process

```
1. Understand the objective
      ↓  what business outcome, which revenue term
2. Read existing automations                    ← never skip; G6
      ↓  what already triggers on this event
3. Understand the customers who would enter
      ↓  lifecycle mix, value spread, engagement, consent
4. Understand the products involved
      ↓  category, attributes, price bands, consumption cycle
5. Enumerate candidate variants                 ← generate widely
      ↓
6. Test each variant                            ← R4: size, difference, value, coverage
      ↓  survivors become journeys; the rest are recorded as rejected
7. Determine topology per variant               ← nodes justify themselves, R8
      ↓
8. Determine timing                             ← from observed intervals, R13
      ↓
9. Determine channel per node                   ← consent, then preference, then cost
      ↓  a channel change mid-journey is a branch and must clear R10
9a. Determine what each node says               ← products and offers delegated, not decided here
      ↓
10. Define goal and exit per variant            ← R15
      ↓
11. Resolve conflicts with existing journeys    ← R16
      ↓
12. Validate, then produce the plan
```

Steps 5 and 6 are the core of the skill: generate variants broadly, then eliminate them ruthlessly.

## Decision Rules

Binding: [../../rules/automation-rules.md](../../rules/automation-rules.md) (R1–R18),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

**How many automations**

- A variant is created only when it passes all four tests in
  [../../rules/automation-rules.md#R4](../../rules/automation-rules.md): size, difference, value, coverage.
- Work the candidate axes listed in [../../rules/automation-rules.md#R2](../../rules/automation-rules.md).
  None of them is automatically a variant; each is a hypothesis the four tests above must confirm.
- If the surviving set is one journey, that is a correct answer. State that alternatives were considered.
- If an existing automation already covers a variant, extend it rather than adding a parallel one.

**How many nodes**

- No default count, no template length (R7). Node count follows the decision window, what the store
  genuinely has to say, and the customer's own interval.
- Every node states its purpose. A node that cannot justify itself is removed (R8).
- Branch only where the paths stay different (R10). If branches reconverge immediately, use a condition
  or personalise inside one message.
- Prefer a flat journey with conditions over nested depth (R12).
- The journey ends when the goal is met or the decision window closes — not when a round number of
  messages has been sent.

**Timing**

- Derive intervals from observed behaviour: delivery time, usage time, repeat interval, decision window.
- Where the data to derive an interval is missing, state the interval is a default and mark it testable.

**What each node carries**

- A node's message type is a topology decision; its contents are not. Products are delegated to
  [product-recommendation-strategy](../product-recommendation-strategy/SKILL.md) and incentives to
  [offer-strategy](../offer-strategy/SKILL.md). A journey that hard-codes a discount depth or a
  product list has embedded two decisions it does not own, and both go stale inside it (G7).
- **Do not branch on product or price band merely because the data allows it** (R3, G9). A
  product-attribute branch earns its place only when the two paths say materially different things
  for materially different windows — a consumable with a short repeat cycle against a durable with a
  long one is a real divergence; two price bands receiving the same message with a different number
  in it is not.
- An offer escalating across a journey's nodes is an offer ladder, and the ladder's shape is
  [offer-strategy](../offer-strategy/SKILL.md)'s decision. Escalating depth by default is how a
  journey teaches customers to wait for its last message.
- Where a node's recommendation would rest only on catalogue-wide popularity, state that the node is
  effectively unpersonalised and reconsider whether it earns its place (R8).

**Channel**

- Consent first, observed channel response second, cost third (R14).
- A change of channel mid-journey is a branch, not a formatting choice, and it must clear R10: the
  paths have to stay different after it. Where consent splits the audience by channel, that is a
  genuine branch; where it does not, one path with a channel-appropriate message is simpler (R12).
- Channel assignment across the whole journey is bounded by the per-channel cadence budget, which is
  smaller for SMS and is shared with every campaign reaching the same contact (F2, F3, F7).
- SMS must clear a higher bar — see [../../knowledge/sms-principles.md](../../knowledge/sms-principles.md).
- If `email_sms.messaging_sms` is unavailable, design email-only and record the gap.

## Workflow

Follows the execution lifecycle in [../../docs/architecture.md](../../docs/architecture.md). This skill
owns DISCOVER through VALIDATE and stops at APPROVE.

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read store profile, existing automations, lifecycle, orders, products, consent | `read_only` |
| ANALYZE | Size candidates, find lifecycle gaps, locate drop-off in existing journeys | `analysis` |
| PLAN | Select variants, design topology, timing, channels, goals, exits | `plan` |
| PREVIEW | Present every variant and node with its justification, plus rejected variants | `plan` |
| VALIDATE | Run the checks below | `plan` |
| APPROVE | Human decision on which variants to build | — |
| EXECUTE | Create journeys via `email_sms.automation` — one at a time | `mutation` |
| VERIFY | Confirm created topology matches the approved plan | `read_only` |
| MEASURE | Hand to [automation-optimization](../automation-optimization/SKILL.md) after enough volume | — |

Creating an automation is `mutation`. **Activating** one is `high_impact` and always requires separate
approval — see [../../rules/safety-rules.md#S2](../../rules/safety-rules.md).

## Expected Output

A workflow plan conforming to
[../../schemas/workflow.schema.json](../../schemas/workflow.schema.json), plus recommendations conforming
to [../../schemas/recommendation.schema.json](../../schemas/recommendation.schema.json), wrapped in a
[skill result](../../schemas/skill-result.schema.json).

Per variant: name, audience and its size, the rationale for its existence, nodes with purpose and timing,
edges with branch conditions, channels, exit criteria, success metric.

Also required: `rejected_variants` — what was considered and why it was not built (R5). A plan without
this reads as if only one option was ever seen.

## Validation

Before presenting:

- [ ] Every variant passes all four R4 tests, and the evidence for each is stated
- [ ] Every audience resolved and sized against `email_sms.segmentation` (A1)
- [ ] Every node has a stated purpose (R8)
- [ ] No branch whose paths reconverge without diverging (R10)
- [ ] Every wait interval traces to observed data, or is labelled a default
- [ ] Every variant has a goal and an exit (R15)
- [ ] Every channel assignment has confirmed consent and an available capability
- [ ] No conflict with existing journeys, or precedence explicitly stated (R16)
- [ ] No duplication of an existing automation (G6)
- [ ] Total contact from this journey counted against existing cadence (F2, F3)
- [ ] No product or price-band branch that does not change what the paths say (R3, G9)
- [ ] Product selection delegated, not embedded in the journey (G7)
- [ ] Offer depth and any ladder delegated, not hard-coded in a node
- [ ] Every mid-journey channel change justified as a branch under R10
- [ ] `rejected_variants` populated
- [ ] No invented data anywhere in the plan (G3)

Any unchecked item is either fixed or declared in `warnings` / `unmet_requirements`.

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read existing automations and customer data | `read_only` | None |
| Produce the topology plan | `plan` | None |
| Create segments the plan needs | `mutation` | Preview, then confirm |
| Create automations in draft | `mutation` | Preview, then confirm |
| **Activate an automation** | `high_impact` | **Explicit, per journey** |
| Modify a live automation | `mutation` → `high_impact` | Explicit; state what changes for in-flight contacts |
| Delete or replace an existing automation | `destructive` | Explicit, after reporting what is lost (S6) |

Approval covers the specific journeys described. A widened audience or an added variant needs new
approval (S3).

## Examples

**"Improve our post-purchase marketing."**
Reads existing automations and finds one generic post-purchase journey. Lifecycle data shows first-time
buyers convert to a second purchase at a materially different rate than repeat buyers, and the catalogue
splits into consumable and durable products with different follow-up needs. Candidate variants: first-time
buyer, repeat buyer, VIP, consumable purchase, durable purchase, high-AOV, discount-led purchase. After
R4 testing, three survive; VIP is folded in as a branch because the audience is too small to measure
separately, and discount-led is rejected outright. Topologies differ: the consumable journey carries a
replenishment node timed to the observed reorder interval, the durable journey does not.

**"Should we split our welcome series by product category?"**
Sizes each category's prospect audience and checks whether the welcome message would genuinely differ.
Two categories are large enough and have distinct first-purchase paths; the remaining four are folded
into one journey with product personalisation. The answer is three journeys, not six, and the four
rejected splits are recorded.

**"Build a replenishment journey."**
Derives per-product reorder intervals from order history, groups products whose intervals cluster, and
produces one journey per cluster with timing set ahead of the interval. Products with no observed repeat
pattern are excluded, and that exclusion is stated rather than filled with a default interval.

Full narrated traces: [../../examples/automation-strategy.md](../../examples/automation-strategy.md).

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.automation` unavailable | **Blocked.** Report; do not design what cannot be built |
| Existing automations unreadable | **Blocked.** Designing blind risks duplicating live journeys (G6) |
| No order history / new store | **Partial.** Design the minimum viable journey, label all intervals as defaults, mark them testable |
| Audience too small for any variant | Return a single journey with personalisation, and say why splitting was rejected |
| Objective ambiguous | Ask once, with the candidate interpretations. Do not guess (S8) |
| SMS capability unavailable | Design email-only, record in `unmet_requirements`, note where SMS would have been used |
| Existing automation already covers the objective | Return a modification plan, not a new journey |
| Consent data unavailable | **Partial.** Plan email-only; never assume consent |
| Conflicting live journey found | Surface the conflict and propose precedence before proposing new nodes |
| Product intelligence unavailable | **Partial.** Design the topology and mark product-carrying nodes as unspecified; never populate them from general knowledge of the vertical (G3) |
| Offer strategy not yet decided | Design the node as offer-bearing with the depth unset, and record it as a dependency rather than choosing a figure |
| A branch cannot be shown to diverge | Collapse it into one path with a condition, and record the branch as rejected (R10, R5) |

Every degraded outcome sets `status` to `partial` or `blocked` and populates `unmet_requirements`. This
skill never fabricates intervals, audience sizes or performance figures to complete a plan (G3, G15).
