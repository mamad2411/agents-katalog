---
name: store-onboarding
description: Use when onboarding a store onto TargetBay Email & SMS — newly signed up, just migrated or moved from another platform, or starting from scratch with no automations and no sending history. Answers "what should we set up first?" for email and SMS. Audits what data actually exists, decides the baseline journeys to build and in what order, plans a deliberately light first period, and sets a review point. Deliberately conservative, because most planning skills depend on history a new store does not have — this skill says so rather than inventing defaults.
license: MIT
metadata:
  targetbay.display_name: Store Onboarding
  targetbay.version: "3.0.0"
  targetbay.category: planning
  targetbay.requires: email_sms.store_profile, email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.product_intelligence, email_sms.segmentation, email_sms.automation, email_sms.suppression_and_consent
  targetbay.composes: automation-strategy, audience-discovery, monthly-marketing-planner
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Store Onboarding

## Purpose

Get a new store from nothing to a working baseline, and be explicit about what cannot be decided yet.

Almost every other skill in this package derives its thresholds from history. A new store has none. The
discipline here is refusing to substitute defaults for evidence, while still shipping something useful on
day one.

## When to Use

- Onboarding a store onto TargetBay Email & SMS for the first time
- A store is new to TargetBay
- An existing store has no automations and no meaningful sending history
- Establishing a baseline email and SMS programme before any optimisation
- Auditing what data is actually available before planning depends on it

## When Not to Use

- The store has history and an existing programme. Use
  [opportunity-discovery](../opportunity-discovery/SKILL.md) or
  [automation-strategy](../automation-strategy/SKILL.md).
- Only the automation portfolio is in question. Use
  [automation-strategy](../automation-strategy/SKILL.md).
- The store has run for a while and simply lacks automations — that is a coverage gap, not onboarding.
- The onboarding question spans reviews, loyalty or onsite personalization as well as email and SMS. Use
  [onboarding-blueprint](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-onboarding/skills/onboarding-blueprint/SKILL.md),
  which sequences all three products against one contact budget rather than planning email and SMS alone.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| What data the platform actually holds for this store | Determines what is decidable at all | Blocked |
| Catalogue: size, categories, consumable or durable | Which baseline journeys apply | Blocked |
| Vertical and market | Which playbook applies | Partial; use the general overlay |
| Any imported order history | Enables earlier derivation of intervals | Partial; everything stays provisional |
| Contact list size and consent state | What can be sent, and to whom | Blocked |
| Existing sending history from a prior platform | Deliverability posture and warm-up needs | Partial; warn |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, scale, markets, plan limits |
| `email_sms.customer_intelligence` | What customer data exists, and how complete it is |
| `email_sms.order_intelligence` | Whether any order history is present to derive from |
| `email_sms.product_intelligence` | Catalogue shape, consumable versus durable |
| `email_sms.segmentation` | Which segments exist, and list sizes |
| `email_sms.automation` | Confirming there is no existing coverage |
| `email_sms.suppression_and_consent` | Consent state per channel; what may be sent |

## Decision Process

```
1. Audit what data exists          ← and record what does not, explicitly
2. Establish what is decidable now ← versus what needs history first
3. Check list provenance and consent ← an imported list is a deliverability decision
4. Select the baseline journeys    ← coverage before sophistication
5. Order the build                 ← highest-certainty, highest-coverage first
6. Set the review point            ← when enough history exists to derive real thresholds
7. Plan a deliberately light first period
```

Step 6 matters as much as the build: onboarding produces a plan *and* the date at which its provisional
choices get replaced by derived ones.

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/automation-rules.md](../../rules/automation-rules.md),
[../../knowledge/email-principles.md](../../knowledge/email-principles.md).

- **Label every provisional value as provisional.** A default interval used because history is absent is
  not a derived interval, and must never be presented as one (G3, G15).
- Coverage before sophistication. Welcome and post-purchase before VIP journeys and branching.
- Build the smallest journeys that work. They will be rebuilt once real data exists, so elaborate topology
  now is wasted effort (G7).
- An imported list is a deliverability risk, not an asset. Check consent provenance, start with the most
  recently engaged portion, and increase volume gradually rather than sending to everything at once.
- Never assume consent transferred from a prior platform. Confirm it through
  `email_sms.suppression_and_consent` (S7).
- Plan a light first period. Early sends establish the store's reputation, and reputation is easier to
  build than to repair.
- Set an explicit review point tied to observable data — a number of orders or repeat purchases, not a
  calendar date.
- Do not run optimisation skills yet. There is nothing to optimise, and they will correctly report
  themselves blocked.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Audit available data, catalogue, list, consent, existing coverage | `read_only` |
| ANALYZE | Establish what is decidable; assess list provenance and deliverability posture | `analysis` |
| PLAN | Baseline journeys, build order, light first period, review point | `plan` |
| PREVIEW | Present the plan with every provisional value marked | `plan` |
| VALIDATE | Run the checks below | `plan` |
| APPROVE | Human approves the baseline | — |
| EXECUTE | Delegated to [automation-strategy](../automation-strategy/SKILL.md) and the campaign skills | `mutation` |
| — | **Any activation or send** | `high_impact`, explicit approval |
| MEASURE | Re-derive thresholds at the review point and replace the provisional values | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: a data-availability audit listing what
exists and what does not; what is decidable now versus what needs history; the baseline journey set with
build order; every provisional value flagged with what would replace it; the list and deliverability
assessment including any ramp-up recommendation; a deliberately light first-period plan; and the review
point expressed in observable terms.

## Validation

- [ ] Data audit completed and gaps listed explicitly
- [ ] Every provisional value marked as provisional (G3, G15)
- [ ] Baseline journeys cover the lifecycle basics before anything specialised
- [ ] No branching or variants proposed without data to justify them (R3, R4)
- [ ] List provenance and consent verified (S7)
- [ ] Deliverability ramp-up addressed for imported lists
- [ ] First period planned light
- [ ] Review point stated in observable terms, not as a date
- [ ] No optimisation skills invoked

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Audit and plan | `read_only` / `plan` | None |
| Create segments and journeys | `mutation` | Preview, then confirm |
| **Activate any journey** | `high_impact` | **Explicit, per journey** |
| **First send to an imported list** | `high_impact` | **Explicit**, with the ramp-up plan and recipient count stated |

The first send to a migrated list deserves more scrutiny than any later one: it sets the store's sending
reputation, and that is slow to repair.

## Examples

**"We've just moved to TargetBay — what should we set up?"**
Audit finds a migrated contact list, a migrated catalogue, and no order history. Consent state is present
but engagement recency is not, so the recommendation is to start with the most recently active portion and
increase volume over several sends. Baseline: welcome, post-purchase, abandonment — three simple journeys,
every interval marked provisional. Review point set at a stated number of repeat purchases, at which the
intervals get derived and the journeys rebuilt. First period planned deliberately light.

**"Set up our replenishment reminders."**
Reports that reorder intervals cannot be derived without repeat-purchase history, names what would be
needed, and recommends the simple post-purchase journey in the meantime — rather than assigning a default
interval that would fire at the wrong time for every product.

## Failure Handling

| Situation | Response |
|---|---|
| No customer or order data at all | **Partial.** Recommend welcome and abandonment only; everything else waits |
| Consent state unavailable | **Blocked** for sending. Confirm consent before any send to a migrated list |
| List provenance unknown | Treat as high risk; recommend engaged-portion-only sending and say why |
| Catalogue not connected | **Partial.** Journeys that need product data are deferred, not defaulted |
| Store asks for a full programme immediately | Build the baseline, state plainly which parts need history, and set the review point |
| Existing automations found | This is not onboarding; hand to [automation-strategy](../automation-strategy/SKILL.md) |

Degraded outcomes set `status` and populate `unmet_requirements`. This skill fails loudly rather than
filling gaps with defaults.
