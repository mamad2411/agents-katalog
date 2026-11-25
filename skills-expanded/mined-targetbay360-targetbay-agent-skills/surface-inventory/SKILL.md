---
name: surface-inventory
description: Use when the question is what onsite personalization currently exists and what it is doing — which surfaces carry placements, offers or search configuration, what each one is worth, where attention is being spent for nothing, and which surfaces host a decision but carry no help. Answers "what's actually personalised on our site right now?" and "what have we already got running?". This is the assessment skill every other personalization skill routes through; use personalization-audit when the question is what to do next rather than what exists.
license: MIT
metadata:
  targetbay.display_name: Surface Inventory
  targetbay.version: "2.0.0"
  targetbay.category: onsite
  targetbay.requires: onboarding.store_context, onboarding.consent_and_tracking, onboarding.recommendation_placement, onboarding.recommendation_analytics, onboarding.offers, onboarding.offer_analytics, onboarding.experience_analytics, onboarding.onsite_search
  targetbay.risk_level: analysis
  targetbay.execution_mode: analyze_only
  targetbay.status: foundation
---

# Surface Inventory

## Purpose

Establish what is currently running on the store's surfaces, what each element is doing, and where
attention is being spent without return.

Every other onsite skill here needs the same foundation: the map of surfaces, what occupies them, and
what consent permits. Deriving it once, here, stops five skills from proposing additions to pages that are
already crowded ([../../rules/global-rules.md#G5](../../rules/global-rules.md)).

## When to Use

- Taking over a personalization setup somebody else built
- Before adding any placement, offer or targeting scheme
- A page converts badly and its onsite elements are a candidate explanation
- Nobody can say what is currently personalised
- Auditing what consent actually permits here

## When Not to Use

- The question is which recommendation strategy belongs where. Use
  [recommendation-strategy](../recommendation-strategy/SKILL.md).
- The question is who should see which offer. Use
  [offer-targeting](../offer-targeting/SKILL.md).
- The question is about search queries specifically. Use
  [onsite-search](../onsite-search/SKILL.md).
- The whole setup needs ranking by what to fix first. Use
  [personalization-audit](../personalization-audit/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Consent and tracking state | Decides what is permissible before anything else | Blocked |
| Current placements and their configuration | The inventory itself | Blocked |
| Current offers, their targeting and frequency | The other half of the inventory | Blocked |
| Per-element performance | What each is worth | Partial; value unassessable |
| Page and funnel performance | The baseline each element sits inside | Partial |
| Search configuration | Search is a surface and is usually unexamined | Partial |
| Traffic composition, anonymous versus identified | What proportion any personalised path reaches | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `onboarding.consent_and_tracking` | What may be collected or acted on, and for which traffic |
| `onboarding.store_context` | Catalogue size, traffic volume, vertical |
| `onboarding.recommendation_placement` | Which placements exist, on which surfaces, with which strategy |
| `onboarding.recommendation_analytics` | Per-placement impressions, clicks, attributed revenue |
| `onboarding.offers` | Which offers run, with what targeting and frequency |
| `onboarding.offer_analytics` | Per-offer engagement, dismissal and conversion |
| `onboarding.experience_analytics` | Page and funnel baselines the elements sit inside |
| `onboarding.onsite_search` | Search configuration as a surface in the inventory |

## Decision Process

```
1. Read consent state first                   ← it bounds everything after it
2. Enumerate every element on every surface
3. Name the decision each surface hosts
4. Attach performance to each element
5. Measure attention cost against outcome
6. Find surfaces hosting a decision with no help
7. Find elements earning nothing
8. Report the traffic split, anonymous versus identified
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/surface-rules.md](../../rules/surface-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Read consent before anything else (G19, [#S15](../../rules/safety-rules.md)). The inventory states what is
  currently permissible, not only what is currently configured — those can differ, and where they do it is
  the most important finding on the page.
- Name the decision every surface hosts (U1). A placement sitting in front of no decision is reported as
  decoration regardless of its engagement numbers.
- Evaluate elements on outcome, never on impressions (U7, G17). An element with high engagement and no
  conversion effect is a candidate for removal, not for expansion.
- Report the anonymous share of traffic explicitly (G23). An elaborate identified-visitor experience
  reaching a small minority is a finding.
- State attribution limits wherever attributed revenue is reported (G18). Revenue flowing through a
  placement is not revenue caused by it.
- Report empty surfaces — pages hosting a real decision with nothing helping — alongside crowded ones. Both
  are inventory findings.
- Report what is working. An inventory that lists only problems cannot be checked for completeness.
- Never propose changes here. This skill is `analyze_only`; the acting skills compose it.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent, placements, offers, search, performance | `read_only` |
| ANALYZE | Map surfaces to decisions, attach outcomes, find gaps and waste | `analysis` |
| PLAN | Rank findings by attention cost against outcome | `analysis` |
| PREVIEW | Present the inventory with its evidence and its confidence | `analysis` |
| VALIDATE | Run the checks below | — |
| MEASURE | Re-inventory after changes have run a full comparison window | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: consent state and what it permits, a
surface-by-surface inventory naming the decision each hosts and the elements on it, per-element outcome
performance with its attribution limits, surfaces hosting a decision with no help, elements earning
nothing, and the anonymous-versus-identified traffic split.

Plus: what is working, and anything that could not be assessed.

No recommendations to act are produced here — the acting skills compose this one.

## Validation

- [ ] Consent state read first, and what it permits stated (G19, S15)
- [ ] Every surface's hosted decision named, or the surface reported as decoration (U1)
- [ ] Every element assessed on outcome, not impressions (U7, G17)
- [ ] Attribution limits stated wherever attributed revenue appears (G18)
- [ ] Anonymous traffic share reported explicitly (G23)
- [ ] Surfaces with a decision and no help reported, not only crowded ones
- [ ] Working elements reported as working
- [ ] No change proposed from this skill
- [ ] Anything unassessable recorded in `unmet_requirements` (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |

Every action this skill implies is owned by a composing skill, which carries its own approval
requirements.

## Examples

**"What personalization do we actually have running?"**
Finds eleven elements across four templates, of which three are on surfaces that host no decision and two
duplicate each other on the product page. Reports that the product page's strongest element by attributed
revenue also cannibalises the one below it, so the attribution is not incremental. Notes that the cart
page — which hosts the clearest completion decision in the funnel — carries nothing at all.

**"We turned on personalization in the EU and nothing seems to happen."**
Consent state shows most EU traffic has not granted tracking, so the identified-visitor paths those
elements depend on never resolve. Reports that the configured experience and the permissible experience
differ for the majority of that traffic, and that the anonymous path was never designed — which is the
finding, rather than anything about the elements themselves (G23, T2).

## Failure Handling

| Situation | Response |
|---|---|
| `onboarding.consent_and_tracking` unavailable | **Blocked.** What is permissible cannot be established, and an inventory that assumes permission is not usable (S15, G19) |
| `onboarding.recommendation_placement` or `onboarding.offers` unavailable | **Blocked.** There is no inventory without the elements |
| Per-element analytics unavailable | **Partial.** Report the inventory and the decisions hosted; state that element value is unassessed |
| Page performance unavailable | **Partial.** Elements cannot be compared against a baseline; say so and lower confidence |
| Traffic composition unavailable | **Partial.** Report that the reach of identified-visitor paths is unknown (G23) |
| Attribution method not exposed | Report attributed revenue with its method marked unknown, and do not call any of it incremental (G18, U5) |
| Nothing is configured | Report that, with the surfaces that host decisions and carry nothing. An empty inventory is a valid and useful result |

Degraded outcomes set `status` and populate `unmet_requirements`.
