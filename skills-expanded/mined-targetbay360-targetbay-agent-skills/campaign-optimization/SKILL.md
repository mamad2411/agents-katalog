---
name: campaign-optimization
description: Use when a campaign, newsletter or email blast underperformed and needs diagnosis — falling engagement, declining clicks, weak revenue, rising unsubscribes, or a recurring send that keeps getting worse. Works backwards from revenue and conversion to find the actual failure point — audience, offer, timing, channel or content — then forms a hypothesis and proposes a testable change. Also use to understand why a campaign did well. Never optimises on open rate alone.
license: MIT
metadata:
  targetbay.display_name: Campaign Optimization
  targetbay.version: "2.2.0"
  targetbay.category: optimization
  targetbay.requires: email_sms.campaign_management, email_sms.campaign_analytics, email_sms.customer_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.experimentation, email_sms.suppression_and_consent
  targetbay.composes: audience-discovery, ab-testing, content-optimization, deliverability-qa, offer-strategy
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Campaign Optimization

## Purpose

Diagnose why a campaign underperformed and propose a change that can be tested and measured.

The discipline: find the failure point before proposing a fix. Most campaign "optimisation" rewrites the
subject line of a campaign that failed because it went to the wrong people with the wrong offer.

## When to Use

- A campaign underperformed and the reason is unclear
- Recurring campaigns have been declining
- Deciding what to test next
- Reviewing a period's campaigns for patterns
- A campaign performed well and the reason should be identified and reused
- Deciding whether to re-send a campaign to the people who did not open it

## When Not to Use

- The campaign has not run yet — that is planning, not optimisation
- A triggered journey underperforms. Use
  [automation-optimization](../automation-optimization/SKILL.md).
- The store needs a strategy rather than a fix. Use [revenue-growth](../revenue-growth/SKILL.md).
- Sample size is too small to diagnose anything. Say so and stop.
- The failure point is already known to be the message itself. Use
  [content-optimization](../content-optimization/SKILL.md) directly.
- Every send is affected, not one campaign. That is the sending programme, not a campaign. Use
  [deliverability-qa](../deliverability-qa/SKILL.md).
- The campaign has not been sent and needs clearing first. Use
  [email-quality-auditor](../email-quality-auditor/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Campaign configuration: audience, offer, timing, channel, content | The variables being diagnosed | Blocked |
| Full performance: revenue, conversion, AOV, click, open, unsubscribe, complaint | The funnel to locate the break in | Blocked |
| Comparable campaigns from this store | The baseline that makes "underperformed" meaningful | Partial; no comparison, lower confidence |
| Audience definition and size at send time | Whether targeting was the failure | Blocked |
| Post-send purchase behaviour | Whether revenue arrived later than attribution suggests | Partial |
| Test history | What has already been tried | Partial; risk of repeating settled tests |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.campaign_management` | Campaign configuration; creating variants after approval |
| `email_sms.campaign_analytics` | Full-funnel performance, comparisons, per-variant results |
| `email_sms.customer_intelligence` | Who actually responded versus who was targeted |
| `email_sms.order_intelligence` | Revenue and AOV attributable to the send |
| `email_sms.segmentation` | Audience definitions and sizes |
| `email_sms.experimentation` | Test configuration and results |
| `email_sms.suppression_and_consent` | Whether cadence or suppression shaped the result |

## Decision Process

```
Analyze          ← full funnel, not the headline metric
   ↓
Identify problem ← locate the break: reach, open, click, convert, value, retain
   ↓
Find evidence    ← comparisons, segment breakdowns, timing, prior sends
   ↓
Hypothesise      ← one variable, one stated belief, one expected effect
   ↓
Recommend change ← the smallest change that tests the hypothesis
   ↓
Create variant   ← after approval
   ↓
Test             ← sized and time-boxed in advance
   ↓
Measure          ← on the outcome metric, not the proxy
   ↓
Learn            ← record what the result settled, and what it did not
   ↓
Optimize         ← apply, then re-enter at the next-largest lever
```

The loop only compounds if **Learn** is a step rather than a sentiment. A result that is not written
down where the next diagnosis will find it means the same hypothesis gets tested again in six
months, and the store pays twice for one answer.

**Locating the break.** Walk the funnel in order and stop at the first stage that is materially below
baseline:

| Stage below baseline | Likely cause | Owning skill |
|---|---|---|
| Delivered / reach | Authentication, sender reputation, a provider turning | [deliverability-qa](../deliverability-qa/SKILL.md) |
| Delivered / reach | Suppression, bounces, an unengaged population | [list-hygiene](../list-hygiene/SKILL.md) |
| Opened | From name, subject, preheader, fatigue | [content-optimization](../content-optimization/SKILL.md) |
| Opened | Send hour or day | [send-time-optimization](../send-time-optimization/SKILL.md) |
| Opened | Too much contact in the window | [consent-verification](../consent-verification/SKILL.md), which owns the ceiling |
| Clicked | Content angle, call to action | [content-optimization](../content-optimization/SKILL.md) |
| Clicked | Audience mismatch | [audience-discovery](../audience-discovery/SKILL.md) |
| Converted | Offer strength or depth | [offer-strategy](../offer-strategy/SKILL.md) |
| Converted | Wrong products featured | [product-recommendation-strategy](../product-recommendation-strategy/SKILL.md) |
| Converted | Landing experience, price, stock | Outside this package; report it |
| AOV | Merchandising, bundling, threshold mechanics | [aov-growth](../aov-growth/SKILL.md) |
| Retained | The campaign bought a purchase at the cost of the relationship | [customer-retention](../customer-retention/SKILL.md) |

Diagnose in funnel order. A click problem diagnosed as a subject-line problem produces a fix that
changes nothing.

## Decision Rules

Binding: [../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/content-rules.md](../../rules/content-rules.md),
[../../knowledge/experimentation-principles.md](../../knowledge/experimentation-principles.md).

- **Never optimise on opens alone.** Opens are a diagnostic, and an unreliable one (G1,
  [../../knowledge/email-principles.md](../../knowledge/email-principles.md)).
- Priority of outcomes: revenue, conversion, AOV, customer value, unsubscribe and complaint risk, then
  engagement.
- A variant that wins on clicks while raising unsubscribes is a loss. Always check the cost side.
- One variable per test. If several things must change, that is a new campaign (C10).
- Test design is delegated to [ab-testing](../ab-testing/SKILL.md): size and threshold are fixed before
  the test runs, and an unresolvable test is reported as unresolvable rather than run.
- Content-level fixes are delegated to [content-optimization](../content-optimization/SKILL.md) once the
  funnel evidence shows the message is the failure point.
- Check the test history before proposing a test that has already been settled — and note that winners
  decay, so a deliberate re-test is legitimate when stated as one.
- Fix the largest lever first: audience and offer before content, content before subject line.
- A campaign that underperformed because it should not have been sent is a planning finding, not a
  content finding. Say that.
- A re-send to non-openers is a second send, not a free one. It spends from the same frequency
  budget as everything else and is counted against it
  ([../../rules/frequency-rules.md#F2](../../rules/frequency-rules.md),
  [../../rules/frequency-rules.md#F3](../../rules/frequency-rules.md)).
- A re-send changes one thing — normally the subject line — and reuses the body. Changing both makes
  the result unattributable and turns a cheap re-send into an untested new campaign (C10).
- Suppress anyone who opened, clicked, converted or unsubscribed since the original, re-evaluated at
  send time (A13).
- A third attempt at the same non-responders is escalation in the wrong direction and is normally
  refused; a different channel or a different message is the legitimate next move
  ([../../rules/frequency-rules.md#F6](../../rules/frequency-rules.md)).
- **Reach failures are diagnosed before anything above them.** A campaign that under-delivered is not
  a content problem, and the two causes at that stage are different skills: authentication and
  reputation go to [deliverability-qa](../deliverability-qa/SKILL.md), population and suppression go
  to [list-hygiene](../list-hygiene/SKILL.md) (D1, D8).
- Never assert inbox placement as the cause of a low open rate (D7). It is a candidate, stated as
  one, and the evidence for it is engagement movement by receiving domain rather than the open rate
  itself.
- The offer is a lever with an owner. Where the break is at conversion and the offer is implicated,
  delegate to [offer-strategy](../offer-strategy/SKILL.md) rather than proposing a depth here (C4).
- **Learn is a step.** Every completed cycle records the hypothesis, the result, what it settled and
  what it did not, and the date — because winners decay and a settled question has a shelf life
  ([../../knowledge/experimentation-principles.md](../../knowledge/experimentation-principles.md)).
  An inconclusive test is recorded as inconclusive, not discarded.
- A recommendation that was applied and not measured is an open loop. Report it as one rather than
  moving to the next lever (G15).
- Record the outcome where the next recommendation will find it.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read campaign configuration, performance, audience, comparables | `read_only` |
| ANALYZE | Walk the funnel, break down by segment, locate the failure | `analysis` |
| PLAN | Form the hypothesis, design the test, propose the change | `recommendation` |
| PREVIEW | Present diagnosis, evidence and proposed test | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the change and the test | — |
| EXECUTE | Create the variant | `mutation` |
| — | **Sending the test** | `high_impact`, separate approval |
| MEASURE | Read results on the outcome metric | `read_only` |
| OPTIMIZE | Apply the winner, record the result, move to the next lever | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing:

1. **Diagnosis** — where the funnel broke, with the comparison that establishes it
2. **Evidence** — segment breakdowns, comparable campaigns, timing analysis, with periods and sample sizes
3. **Hypothesis** — in the form *we believe X will improve Y for Z because W, measured by M*
4. **Recommended change** — the smallest change that tests it
5. **Test design** — variant split, sample size, duration, decision threshold, success metric
6. **Risks** — including what a false positive would cost

Where the sample is too small to resolve the question, that finding replaces the test design.

## Validation

- [ ] Full funnel examined, not the headline metric
- [ ] Diagnosis identifies a specific stage with evidence
- [ ] Unsubscribe and complaint rates checked alongside positive metrics
- [ ] Hypothesis states one variable and an expected effect
- [ ] Sample size and duration decided before the test
- [ ] Test history checked for an already-settled question
- [ ] Success metric is an outcome, not a proxy
- [ ] Comparison baseline is from this store (G3)
- [ ] Recommendation targets the largest lever, not the easiest one
- [ ] Reach failures diagnosed before higher stages, and routed to the right owner (D1, D8)
- [ ] No placement claim asserted from open rate alone (D7)
- [ ] Offer questions delegated rather than answered with a discount depth (C4)
- [ ] The result recorded with what it settled and what it did not, and dated
- [ ] Any applied-but-unmeasured prior recommendation reported as an open loop (G15)
- [ ] Sample-size limitations stated where they exist

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and diagnose | `read_only` / `analysis` | None |
| Recommend a change | `recommendation` | None |
| Create a variant or test | `mutation` | Preview, then confirm |
| **Send the test or the revised campaign** | `high_impact` | **Explicit** |
| Apply a winner to future sends | `mutation` | Confirm; state what changes |

## Examples

**"This campaign underperformed — fix the subject line."**
Funnel shows open rate at baseline and click rate less than half of it. The subject line worked; the
offer did not apply to most of the audience. Recommends re-targeting to the affinity-matched subset and
testing offer relevance, not subject wording. States plainly that the requested fix would have changed
nothing.

**"Our weekly newsletter is declining."**
Finds engagement declining across all segments while cadence has risen, with unsubscribes climbing on the
least-engaged segment. Diagnoses cadence, not content, and recommends reducing frequency for the
low-engagement segment before any content test — a change the store can measure within a month.

**"This campaign did well — what worked?"**
Breaks down by segment and finds the result concentrated in one affinity group, not distributed.
Recommends targeting that group deliberately rather than repeating the broad send, and records the
finding so the next plan cites it.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.campaign_analytics` unavailable | **Blocked.** Diagnosis requires performance data |
| No comparable campaigns | **Partial.** Diagnose structurally, state there is no baseline, lower confidence |
| Sample too small to diagnose | Report that plainly. Do not manufacture a cause from noise |
| Revenue attribution unavailable | **Partial.** Diagnose to conversion, state the attribution gap |
| Multiple variables changed at once | Report that the campaign is not diagnosable as a test, and what to isolate next time |
| Store's volume cannot resolve the test | Recommend the change on reasoning, explicitly not as a test |
| Requested fix targets the wrong lever | Say so, give the evidence, and propose the right one |
| The break is at reach | Diagnose no further up the funnel; route to deliverability-qa or list-hygiene with the evidence, and say which and why (D1) |
| Engagement cannot be split by receiving domain | **Partial.** Placement stays a candidate cause rather than a finding (D6, D7) |
| No record of prior cycles | **Partial.** Proceed, and state that the test history could not be checked — a settled question may be re-tested |
| A prior recommendation was applied but never measured | Report the open loop before proposing a new cycle; an unmeasured change contaminates the next baseline |

Degraded outcomes set `status` and populate `unmet_requirements`. Never present a cause without the
evidence that supports it (G2, G14).
