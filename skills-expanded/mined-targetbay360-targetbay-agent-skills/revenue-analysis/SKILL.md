---
name: revenue-analysis
description: Use when someone asks what happened to revenue rather than what to do about it — decomposing revenue into its drivers, attributing it across campaigns, automations and channels, comparing periods, and explaining a rise or fall with evidence. Read-only. Use revenue-growth when the question is which opportunities to pursue.
license: MIT
metadata:
  targetbay.display_name: Revenue Analysis
  targetbay.version: "2.0.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.store_profile, email_sms.order_intelligence, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.campaign_analytics, email_sms.automation_analytics
  targetbay.risk_level: analysis
  targetbay.execution_mode: analyze_only
  targetbay.status: foundation
---

# Revenue Analysis

## Purpose

Explain the store's revenue: what it decomposes into, where it came from, what changed against a prior
period, and how confident that explanation is.

This skill produces understanding, not actions. Separating it from
[revenue-growth](../revenue-growth/SKILL.md) means the analysis can be trusted on its own terms — it has
no recommendation to justify.

## When to Use

- "Why did revenue drop last month?"
- Establishing a baseline before planning
- Period-over-period comparison
- Attributing revenue across campaigns, automations and channels
- Another skill needs the decomposition before it can rank opportunities

## When Not to Use

- The question is what to do next. Use [revenue-growth](../revenue-growth/SKILL.md).
- One campaign needs diagnosis. Use [campaign-optimization](../campaign-optimization/SKILL.md).
- A financial forecast is wanted. This skill explains observed revenue; it does not model future revenue.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Order history across the analysis and comparison periods | The subject of the analysis | Blocked |
| Customer counts and cohorts per period | Decomposition into the customers term | Blocked |
| AOV and frequency distributions | The other two terms | Blocked |
| Campaign and automation revenue | Attribution across instruments | Partial; total only |
| Product and category revenue | Where revenue concentrates | Partial |
| The platform's attribution model and window | Comparisons are only valid within one model | Partial; state the caveat |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.store_profile` | Scale and period context |
| `email_sms.order_intelligence` | Revenue, orders, AOV, frequency, cohorts |
| `email_sms.customer_intelligence` | Customer counts, lifecycle mix, value concentration |
| `email_sms.product_intelligence` | Product and category contribution |
| `email_sms.campaign_analytics` | Campaign-attributed revenue |
| `email_sms.automation_analytics` | Automation-attributed revenue |

## Decision Process

```
1. Decompose        ← customers × frequency × AOV, for both periods
2. Locate the delta ← which term moved, and by how much
3. Decompose again  ← inside the moved term: which cohort, product, channel
4. Attribute        ← campaigns, automations, unattributed
5. Test alternatives← seasonality, mix shift, a single large order, an attribution artefact
6. State confidence ← and what could not be separated
```

Step 5 is what separates analysis from storytelling. A plausible cause is not a cause until the obvious
alternatives have been checked.

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../knowledge/marketing-principles.md](../../knowledge/marketing-principles.md).

- Always decompose before explaining. A total that moved tells you nothing about why.
- Compare like with like: same attribution model, same window, same definitions (G2).
- Check for mix shift before concluding a behaviour change. A revenue drop with stable orders is an AOV or
  mix story, not an engagement story.
- Check whether a small number of large orders moved the total. Medians and distributions, not just means.
- Unattributed revenue is reported as unattributed, never redistributed to make the numbers tidy.
- Correlation with a campaign is not attribution. Say which it is.
- State what the data cannot separate. Overlapping sends in one window frequently cannot be told apart.
- Never present an external benchmark as this store's number (G3).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read orders, customers, products, campaign and automation revenue for both periods | `read_only` |
| ANALYZE | Decompose, locate the delta, attribute, test alternative explanations | `analysis` |
| PREVIEW | Present the decomposition and the explanation with its confidence | `analysis` |
| VALIDATE | Run the checks below | — |

This skill never mutates and never sends.

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the revenue decomposition for both
periods; the delta per term; the drill-down into whichever term moved; attribution by instrument with an
explicit unattributed share; the alternative explanations tested and rejected; confidence; and the
limitations of the analysis.

## Validation

- [ ] Both periods decomposed into all three terms
- [ ] Comparison uses one attribution model and window
- [ ] Mix shift checked before behaviour change is concluded
- [ ] Distribution checked, not only the mean
- [ ] Unattributed revenue reported as such
- [ ] At least the obvious alternative explanations tested
- [ ] Confidence stated, with what could not be separated
- [ ] No external benchmarks presented as store data (G3)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |

Nothing here mutates. `targetbay.execution_mode` is `analyze_only`.

## Examples

**"Why did revenue drop last month?"**
Decomposition shows customer count and order frequency flat, AOV down. Drilling into AOV shows the mix
shifted toward a lower-priced category after a clearance campaign. The drop is a deliberate consequence of
a decision, not an engagement problem — a conclusion that would have been missed by looking at the total
or at open rates.

**"How much revenue do our automations produce?"**
Reports attributed revenue per journey, the share that is unattributed, and states explicitly that
automation and campaign attribution overlap for contacts who received both in the window — so the two
figures must not be summed.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.order_intelligence` unavailable | **Blocked.** There is nothing to analyse |
| Comparison period has no data | **Partial.** Report the current period without a delta |
| Attribution unavailable | **Partial.** Decompose without attribution and say so |
| Attribution model changed between periods | Report the comparison as invalid rather than misleading |
| Period too short to be meaningful | State the limitation; do not smooth it away |
| A single order dominates the delta | Report it explicitly rather than describing a trend |

Degraded outcomes set `status` and populate `unmet_requirements`.
