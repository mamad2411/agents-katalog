---
name: ab-testing
description: Use when designing a test, deciding whether a test is worth running, or reading a completed test's result — sizing variants, setting the decision threshold and duration in advance, choosing whether the design needs a holdout that receives nothing, and judging whether a difference is real or noise. Covers any dimension — offer, audience, product, timing, channel and content — not just subject lines. Use campaign-optimization when the question is what is wrong; this skill runs the experiment that answers it.
license: MIT
metadata:
  targetbay.display_name: A/B Testing
  targetbay.version: "2.1.0"
  targetbay.category: optimization
  targetbay.requires: email_sms.experimentation, email_sms.campaign_analytics, email_sms.segmentation, email_sms.order_intelligence
  targetbay.composes: audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# A/B Testing

## Purpose

Design tests that produce decisions, and read results honestly — including the frequent, correct answer
that the store's volume cannot resolve the question.

The failure this skill exists to prevent: running an underpowered test, seeing a difference, and treating
noise as strategy.

## When to Use

- A test needs designing: variants, split, size, duration, threshold
- Deciding whether a question is worth testing at all
- Reading a completed test and deciding what it means
- Auditing test history before proposing a settled question again

## When Not to Use

- The question is *what* is wrong. Use
  [campaign-optimization](../campaign-optimization/SKILL.md), which composes this skill once it has a
  hypothesis.
- The content angle itself is the subject. Use
  [content-optimization](../content-optimization/SKILL.md).
- The decision must be made now and cannot wait for a result. Make it on reasoning and say so.
- The incentive itself needs choosing before anything can be tested. Use
  [offer-strategy](../offer-strategy/SKILL.md).
- The question is which hour to send rather than whether timing matters. Use
  [send-time-optimization](../send-time-optimization/SKILL.md), which composes this skill.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The hypothesis and the variable being tested | A test without one is data collection | Blocked |
| Audience size available for the test | Determines whether any result is readable | Blocked |
| Baseline performance on the outcome metric | The thing a difference is measured against | Blocked |
| Typical variance in that metric for this store | Separates a real difference from normal movement | Partial; be conservative |
| Prior test history | Prevents re-running settled questions | Partial |
| The platform's winner-selection behaviour | Some platforms auto-send a winner; that changes the design | Partial; state the assumption |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.experimentation` | Test configuration, variants, results, winner state |
| `email_sms.campaign_analytics` | Baseline and variance for the outcome metric |
| `email_sms.segmentation` | Sizing the testable audience |
| `email_sms.order_intelligence` | Revenue outcomes, which are usually the real metric |

## Decision Process

```
1. Restate the hypothesis        ← belief, effect, audience, measure
1a. Identify the dimension       ← which lever is under test; each has its own trap
1b. Decide whether a holdout is needed  ← is the question 'which variant' or 'does this earn anything'?
2. Confirm one variable          ← if several change, it is not a test
3. Check the test history        ← already settled? a deliberate re-test is fine; a blind repeat is not
4. Size it                       ← can this audience resolve the minimum effect worth acting on?
5. If not resolvable → stop      ← recommend deciding on reasoning instead
6. Fix duration and threshold    ← before it runs, never after seeing results
7. Define the outcome metric and the guard metric
8. Run, then read against the pre-set threshold
```

Step 5 is the one most often skipped. A test that cannot resolve the effect is worse than no test: it
produces a number that feels like evidence.

**The dimensions, and what each one specifically needs.** A test is not always a subject line.

| Dimension | What varies | The trap specific to it |
|---|---|---|
| Subject and preheader | The opening unit | Winning on opens while losing on revenue. Judge downstream |
| Content | Angle, structure, call to action | Changing structure and wording together, which is two variables |
| Offer | Instrument or depth | The deeper offer almost always wins on conversion; the cost side is what has to be measured |
| Product | Which items are featured | Confounded with availability and price; hold both steady or the test measures stock |
| Audience | Who receives it | Two audiences are not two variants of one test — they have different baselines |
| Timing | Hour or day | Contaminated by anything else in the window; needs the longest run |
| Channel | Email against SMS | Different consent populations, so rarely a clean comparison. Usually a holdout question instead |
| Holdout | Sending against not sending | The only design that measures whether the message earns anything at all |

## Decision Rules

Binding: [../../knowledge/experimentation-principles.md](../../knowledge/experimentation-principles.md),
[../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md).

- One variable. Several changes at once make a new campaign, not a test (C10).
- Size, duration and decision threshold are fixed **before** the test runs. Stopping when the numbers look
  good is how noise becomes strategy.
- The outcome metric is an outcome — revenue or conversion — not a proxy. A subject-line test won on opens
  and lost on revenue chose the wrong winner.
- Always carry a guard metric: unsubscribes and complaints. A variant that wins on clicks while burning the
  list is a loss.
- Test the large levers first: offer, audience, timing, channel — before subject lines and creative
  details.
- "No detectable difference" is a result. Report it as one; do not hunt for a segment where the variant
  won.
- One test at a time per audience. Overlapping tests contaminate each other.
- Winners decay. A re-test of a settled question is legitimate when declared as a re-test.
- **A holdout answers a question no variant comparison can**: whether the send produced incremental
  revenue, or harvested purchases that would have happened anyway. Where the decision is whether a
  campaign or journey should exist at all, a holdout is the correct design and a two-variant test is
  the wrong instrument (G1).
- A holdout has a cost — the revenue the withheld group does not produce — and that cost is stated
  before approval, not discovered afterwards (S4). Where it cannot be afforded, say so and report
  that incrementality will remain unmeasured rather than substituting a variant test.
- An audience test is not a variant test. Two audiences have different baselines, so the comparison
  is each against its own history, never against each other (A2).
- A product test holds availability and price steady, or it measures stock rather than preference.
- A channel test rarely compares like with like, because the consented populations differ (A10). State
  that limitation rather than reporting the winner as if it generalised.
- Where the store's volume cannot resolve the effect, say so plainly and recommend the decision on
  reasoning. **Do not report a result as significant when the design could not establish it**, and do
  not present a directional difference as a finding (G2, G15).
- Record the result where the next recommendation will cite it.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read baseline, variance, audience size, test history | `read_only` |
| ANALYZE | Size the test against the minimum effect worth acting on | `analysis` |
| PLAN | Variants, split, duration, threshold, outcome and guard metrics | `recommendation` |
| PREVIEW | Present the design, including whether it can resolve anything | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the test | — |
| EXECUTE | Create the test | `mutation` |
| — | **Sending the test** | `high_impact`, separate approval |
| MEASURE | Read against the pre-set threshold, including the guard metric | `read_only` |
| OPTIMIZE | Apply the winner, record the result | `mutation` |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the restated hypothesis; the test
design — variants, split, audience size, duration, decision threshold, outcome and guard metrics; whether
the test is resolvable at this store's volume; what a null result would mean; and, when reading a
completed test, the verdict against the pre-set threshold with the guard metric checked.

## Validation

- [ ] Exactly one variable changes
- [ ] Hypothesis states belief, effect, audience and measure
- [ ] Size checked against the minimum effect worth acting on
- [ ] Duration and threshold fixed before running
- [ ] Outcome metric is an outcome, not a proxy
- [ ] Guard metric defined
- [ ] Test history checked for a settled question
- [ ] No overlapping test on the same audience
- [ ] The dimension under test named, with its specific trap addressed
- [ ] Holdout considered, and its cost stated where one is used (S4)
- [ ] Audience tests compared against each audience's own baseline, not against each other (A2)
- [ ] Product tests hold availability and price steady
- [ ] Channel test limitations stated where the consented populations differ (A10)
- [ ] No directional difference reported as a finding where the design could not resolve it (G2)
- [ ] Unresolvable tests reported as unresolvable rather than run

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and design | `read_only` / `recommendation` | None |
| Create the test | `mutation` | Preview, then confirm |
| **Send the test** | `high_impact` | **Explicit**, with per-variant recipient counts |
| Apply a winner to future sends | `mutation` | Confirm; state what changes |
| Enable automatic winner sending | `high_impact` | Explicit; state that a send will happen without further review |

## Examples

**"Test two subject lines."**
Sizes the audience against the store's normal variance and finds the split cannot resolve a difference
smaller than a large one. Reports that the test would not be readable, and recommends testing the offer
instead — a larger lever with an effect the volume can actually detect.

**"Our variant B won, let's roll it out."**
Reads the result against the threshold set before the run. B won on clicks but is level on revenue and
higher on unsubscribes. Verdict: not a winner. Recommends keeping A and states what B's result suggests
testing next.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.experimentation` unavailable | **Blocked** for execution; the design can still be produced as a recommendation |
| Audience too small to resolve anything | Report that, and recommend deciding on reasoning |
| No baseline for the metric | **Partial.** Design conservatively and state that the threshold is provisional |
| Several variables already changed | Report it is not a test; state what to isolate |
| Result read after the threshold was moved | Report the original threshold and the verdict against it |
| Platform auto-sends a winner | State this explicitly before approval — a send will occur without a second review |
| Holdout cost is unacceptable to the store | Proceed without it, and record that incrementality is unmeasured rather than implying the variant result covers it |
| The dimension cannot be isolated | Report it as not testable and name what would have to be held steady |
| Result is directional but below threshold | Report it as inconclusive. A direction is not a finding, and reporting it as one is how a threshold becomes decorative |

Degraded outcomes set `status` and populate `unmet_requirements`.
