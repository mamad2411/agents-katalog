---
name: automation-recipe-selector
description: Use when a store wants to know which ready-made automation recipes to adopt from a published library and in what order — picking from a finite catalogue of trigger-by-trigger recipes instead of designing one from scratch, ranking each recipe by what this store can actually support today, naming the data, consent and integration prerequisite every recipe has before it can run, and saying plainly when none of them fit. Answers "which recipes should we use?", "is there a ready-made recipe for this?" and "what can we adopt with what we already have?". Use automation-strategy when the portfolio should be derived from this store's own data rather than picked from a library, and automation-architect to design a single journey in detail once one is chosen.
license: MIT
metadata:
  targetbay.display_name: Automation Recipe Selector
  targetbay.version: "1.0.0"
  targetbay.category: automation
  targetbay.requires: email_sms.store_profile, email_sms.automation, email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.suppression_and_consent, email_sms.event_stream, email_sms.campaign_analytics
  targetbay.composes: automation-strategy, audience-discovery
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Automation Recipe Selector

## Purpose

Given a finite published library of automation recipes and one store, decide which to adopt and in
what order — ranked by readiness rather than by appeal.

The failure this prevents is a store adopting the recipes that sound most valuable and stalling on
all of them, because each one needed a trigger, a consent record or an integration nobody checked
for. Every recipe carries prerequisites. A recipe whose prerequisites are unmet is not "next" — it is
blocked, and the work that meets the prerequisite is what goes in front of it.

When the library does not contain what this store needs, say so and hand over to
[automation-strategy](../automation-strategy/SKILL.md). A library is a shortcut, not a substitute for
deciding.

## When to Use

- A store wants to adopt ready-made recipes rather than design journeys from scratch
- Deciding which recipes to set up first, and what has to be true before each one can run
- A store has adopted several recipes and wants to know what to add next
- Checking whether the library contains anything for a problem the store has named
- A vertical playbook is in hand and its recipe order needs testing against this store's evidence

## When Not to Use

- The portfolio should be derived from this store's own data rather than chosen from a catalogue.
  Use [automation-strategy](../automation-strategy/SKILL.md).
- One recipe has been chosen and needs designing in detail. Use
  [automation-architect](../automation-architect/SKILL.md).
- The store is brand new with no history at all. Use
  [store-onboarding](../store-onboarding/SKILL.md), which sets the baseline first and routes back
  here afterwards.
- An adopted recipe underperforms. Use
  [automation-optimization](../automation-optimization/SKILL.md).
- The question is where a recipe's steps should run. Use
  [automation-orchestration](../automation-orchestration/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The recipe library and each entry's prerequisites | There is nothing to rank without it | Blocked |
| Existing automations and their triggers | A recipe duplicating a live journey is not an addition | Blocked |
| Which triggers the platform emits, and which the store can push | The most common blocking prerequisite | Blocked |
| Consent state and suppression, per channel | Several recipes are unlawful or pointless without it | Blocked |
| Audience sizes for each recipe's target population | A recipe whose audience is negligible is not worth the setup | Blocked |
| Store profile — vertical, catalogue, sending history | Which recipes are structurally applicable | Partial; rank on data alone |
| Vertical playbook, when supplied | Supplies the starting recipe order | Partial; rank on store evidence alone and say so |
| Which integrations the store already has | Whether an integration-dependent recipe is blocked or ready | Partial; treat as blocked and say so |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Vertical, catalogue shape, sending history, plan limits, existing integrations |
| `email_sms.automation` | Existing journeys and their triggers, so an adopted recipe does not duplicate one |
| `email_sms.customer_intelligence` | Whether the contact data a recipe depends on is actually populated |
| `email_sms.order_intelligence` | Whether order and purchase-interval prerequisites are met |
| `email_sms.segmentation` | Sizing each recipe's target audience |
| `email_sms.suppression_and_consent` | Consent prerequisites per channel, and what is already excluded |
| `email_sms.event_stream` | Which triggers exist, which is the prerequisite that blocks most often |
| `email_sms.campaign_analytics` | Current performance, which says where a recipe would add the most |

## Decision Process

```
1. Read the library and each recipe's prerequisites
2. Read what this store already runs         ← a recipe duplicating a live journey is dropped here
3. For each remaining recipe, test readiness
     trigger available? · audience large enough? · consent present? · integration present?
4. Partition into ready · blocked · not applicable
5. Take the playbook's order as the prior, where a playbook was supplied
6. Re-rank the ready set by expected value   ← delegated to automation-strategy
7. For each blocked recipe, name the single prerequisite and sequence that work in front of it
8. If nothing in the library fits, say so and hand to automation-strategy
9. Produce the adoption sequence, saying which position came from the playbook and which from data
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/automation-rules.md](../../rules/automation-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Read the existing automations before recommending any recipe. A recipe that triggers on an event a
  live journey already triggers on is a collision, not an addition (G6, R16, R17).
- **Readiness gates rank, and readiness is all this skill ranks on.** A recipe whose prerequisite is
  unmet is sequenced behind the work that meets it, never recommended with the prerequisite as a
  footnote. Expected value within the ready set is ordered by
  [automation-strategy](../automation-strategy/SKILL.md) rather than re-derived here, so one store
  does not get two different orderings depending on which skill was asked.
- Name one blocking prerequisite per blocked recipe, not a list. The single thing standing in the way
  is actionable; a list of six is a reason to do nothing.
- Confirm each recipe's audience exists and is large enough to be worth the setup. A recipe for an
  audience of a handful belongs inside an existing send instead (A1, A2, A12).
- Where a playbook is supplied, its order is a prior and not a conclusion. Re-rank on store evidence
  and report which position came from which — this is required of any skill taking a playbook
  ([../../playbooks/README.md](../../playbooks/README.md)).
- Prefer the fewest recipes that serve the objective. A store adopting a long list adopts none of them
  properly (G7).
- **Refuse to stretch the library.** If no entry fits, say so plainly and hand over to
  [automation-strategy](../automation-strategy/SKILL.md). Recommending the nearest recipe because it
  is the nearest is how a store ends up with a journey nobody wanted.
- Never recommend a recipe whose consent prerequisite is unmet, and never propose acquiring the
  consent as part of the same step (S7, A10).
- A recipe is a starting shape. Say what it will need adapted for this store rather than presenting
  it as finished (G14).
- Do not assume a capability or a trigger exists because a recipe describes one. An unconfirmed
  prerequisite is unmet (S12).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read the library, existing automations, triggers, consent, audiences, integrations | `read_only` |
| ANALYZE | Test readiness per recipe; partition into ready, blocked and not applicable | `analysis` |
| PLAN | Rank the ready set; sequence prerequisite work in front of the blocked | `plan` |
| PREVIEW | Present the adoption sequence with each prerequisite and its provenance | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the sequence | — |
| EXECUTE | Hand each chosen recipe to [automation-architect](../automation-architect/SKILL.md) to design | `mutation` |
| — | **Activating any adopted journey** | `high_impact`, explicit approval |
| MEASURE | Adoption rate against the sequence; which prerequisites actually blocked in practice | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the ready, blocked and
not-applicable partitions with every recipe placed; the adoption sequence for the ready set with the
evidence behind each position; for each blocked recipe, the single prerequisite and the work that
would clear it; which positions came from the playbook and which from store data; anything the
library does not cover, with the handover to `automation-strategy`; and the risks.

## Validation

- [ ] Existing automations read before any recommendation (G6, R17)
- [ ] Every recipe placed in exactly one of ready, blocked or not applicable
- [ ] Each blocked recipe carries exactly one named prerequisite
- [ ] Each ready recipe's audience confirmed to exist and sized (A1, A2)
- [ ] Audiences too small routed to an existing send rather than a new journey (A12)
- [ ] Playbook order treated as a prior, with provenance reported per position
- [ ] No recipe recommended whose consent prerequisite is unmet (S7, A10)
- [ ] Unconfirmed prerequisites treated as unmet rather than assumed (S12)
- [ ] Gaps in the library stated, with the handover to automation-strategy
- [ ] What each recipe needs adapted for this store stated, not presented as finished (G14)
- [ ] Recipes that would collide with a live journey excluded, not merely flagged (R16)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read the library and the store's current state | `read_only` / `analysis` | None |
| Recommend the adoption sequence | `plan` / `recommendation` | None |
| Hand a recipe to design and creation | `mutation` | Preview, then confirm |
| **Activate any adopted journey** | `high_impact` | **Explicit, per journey** |
| **Adopt a recipe whose consent prerequisite is unmet** | — | **Refused.** Not sequenced by this skill (S7) |

## Examples

**"Which of your ready-made recipes should we set up first?"**
Reads the store's existing journeys and finds a welcome already live, so the welcome recipe drops out
entirely rather than being ranked second. Of the rest, cart recovery ranks first on unserved value
but is blocked — the store has no way to distinguish an abandoned cart from a completed order — so
the sequence puts that one signal ahead of it and leads with the review request, which is ready
today. Reports that the review request's position came from store evidence and that the vertical
playbook would have put stock alerts first, which the store's variant data cannot yet support.
Rejected: ranking cart recovery first because it is the highest-value recipe, which would have left
the store stalled on it.

**"Is there a recipe for chasing customers whose subscription payment failed?"**
Checks the library and finds nothing for dunning — it is a billing problem with different consent and
retention requirements, and no entry covers it. Says so plainly and hands over to
[automation-strategy](../automation-strategy/SKILL.md) rather than offering the win-back recipe as
the nearest thing. Rejected: adapting the win-back recipe, which targets lapsed buyers on a
marketing consent basis and would be the wrong instrument on the wrong legal footing.

## Failure Handling

| Situation | Response |
|---|---|
| The recipe library is unavailable | **Blocked.** There is nothing to rank. Hand to [automation-strategy](../automation-strategy/SKILL.md), which needs no catalogue |
| Existing automations unreadable | **Blocked.** Recommending a recipe that duplicates a live journey is the failure this skill should catch first (R16) |
| Trigger availability cannot be established | **Blocked.** Readiness is the ranking, and the trigger is the prerequisite that blocks most often (S12) |
| Consent state unavailable | **Blocked.** Several recipes are unlawful without it, and assuming consent is never acceptable (S7) |
| Audience sizes unavailable | **Blocked.** A ranking that cannot tell a large unserved audience from a negligible one is not a ranking (A1) |
| Store profile unavailable | **Partial.** Rank on data and existing automations; state that structural applicability could not be assessed |
| Integration inventory unavailable | **Partial.** Treat integration-dependent recipes as blocked, and name confirming the integration as the prerequisite |
| Nothing in the library fits | Report that plainly, with what the store actually needs, and hand to [automation-strategy](../automation-strategy/SKILL.md). This is a correct outcome, not a failure |

Degraded outcomes set `status` and populate `unmet_requirements`.
