---
name: list-hygiene
description: Use when bounces, spam complaints or one mailbox provider turning against the store are the problem rather than the campaign — deciding which contacts leave the sending population and when, how to respond to a hard bounce versus a repeated soft one, whether a complaint trend means pausing sends entirely, what to do with subscribers who have never once opened, and when a sunset path beats another attempt. Answers "our bounce rate is climbing", "engagement has collapsed at one provider" and "who should we remove from the list?". Use deliverability-qa when authentication or sender reputation is the suspected cause, and customer-winback when lapsed buyers might still be recovered.
license: MIT
metadata:
  targetbay.display_name: List Hygiene
  targetbay.version: "1.1.0"
  targetbay.category: audience
  targetbay.requires: email_sms.suppression_and_consent, email_sms.campaign_analytics, email_sms.customer_intelligence, email_sms.segmentation, email_sms.event_stream
  targetbay.composes: audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# List Hygiene

## Purpose

Decide which contacts leave the sending population, when, and by which route — and decide when a
deliverability signal means stopping sends rather than tuning them.

Two failures bracket the decision: treating deliverability as a content problem, where rewriting
subject lines while still mailing a never-opening cohort moves nothing; and suppressing on a single
soft bounce, which discards deliverable customers. State both costs rather than asserting one.

This skill decides the programme's response. The platform classifies bounces and holds suppression
state ([../../rules/global-rules.md#G10](../../rules/global-rules.md)).

## When to Use

- Bounce or complaint rates are rising, or a mailbox provider has started blocking
- Deciding who to suppress, and what to do with contacts who have never engaged
- Designing a sunset path for a disengaged cohort
- Deciding whether a deliverability signal justifies pausing sends
- Setting the alert threshold at which a rate becomes a problem for this store

## When Not to Use

- The lapsed contacts might still buy and the objective is revenue. Use
  [customer-winback](../customer-winback/SKILL.md) — recovery is decided there, and suppression is its
  last step rather than its first.
- Customers are going quiet but still purchasing. Use
  [customer-retention](../customer-retention/SKILL.md).
- The question is which channel to reach a reachable contact on. Use
  [channel-optimization](../channel-optimization/SKILL.md).
- The problem is one campaign's performance, not the sending population. Use
  [campaign-optimization](../campaign-optimization/SKILL.md).
- Authentication, sender reputation or a volume ramp is the suspected cause. Use
  [deliverability-qa](../deliverability-qa/SKILL.md), which diagnoses the layer above this one and
  composes this skill for the population half of the remedy.
- The question is whether the list may lawfully be mailed at all, or how often. Use
  [consent-verification](../consent-verification/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Suppression state and consent per channel | The current sending population | Blocked |
| Bounce classification from the platform, hard against soft | Permanent and temporary failures get different responses | Blocked |
| Complaint rate over time, and its recent variance | A threshold derived from this store rather than borrowed | Blocked |
| Engagement recency per contact | Separates never-engaged from quiet-but-reachable | Partial; suppression recommendations become coarse |
| Prior value per contact | States what suppression costs in revenue | Partial; the trade-off cannot be quantified |
| Acquisition source per contact | Locates a bad source rather than blaming the whole list | Partial; remediation is guesswork |
| Send volume and cadence history | Distinguishes a rate change from a volume change | Partial |
| Engagement, bounce and complaint movement split by receiving domain | Whether one provider or the whole programme has turned | Partial; the diagnosis stays list-wide |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.suppression_and_consent` | Current suppression state, consent per channel, what is already excluded |
| `email_sms.campaign_analytics` | Bounce, complaint and engagement rates, and their movement over time |
| `email_sms.customer_intelligence` | Engagement recency and prior value per contact |
| `email_sms.segmentation` | Sizing the affected cohorts and materialising a sunset audience |
| `email_sms.event_stream` | Individual bounce, complaint and unsubscribe events, for classification at contact level |

## Decision Process

```
1. Read the current rates and their recent variance   ← the store's own baseline, not a published figure
2. Establish whether this is a rate change or a volume change
3. Locate the concentration                           ← by acquisition source, cohort, campaign
3a. Split by receiving domain                         ← one provider turning is a different problem
4. Classify the affected contacts into three responses
     suppress now · bounded sunset path · leave alone
5. Size each group and state its prior value          ← what suppression costs
6. Decide whether sending continues while this is fixed ← a complaint rate can mean stop, not tune
7. Define the sunset path's bound and its terminus
8. Produce the plan, with the revenue cost stated alongside the deliverability gain
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/deliverability-rules.md](../../rules/deliverability-rules.md),
[../../knowledge/email-principles.md](../../knowledge/email-principles.md),
[../../knowledge/deliverability-principles.md](../../knowledge/deliverability-principles.md).

- The platform classifies and enforces; this skill decides the response (G10). Never propose a
  parallel suppression list maintained outside the platform.
- A permanent failure is suppressed. A single temporary failure is not — the repeat count that makes
  it permanent is derived from this store's own pattern, never a fixed number.
- The alert threshold is derived from this store's recent variance. A published benchmark tells you
  whether a number is unusual for the industry, not whether it is unusual for this store (G2).
- Suppression is destructive and is reported before it is proposed: the count, the prior value, and
  what is lost (S6, S2).
- Never re-add a suppressed or unsubscribed contact (S7). Whether an unevidenced list may be mailed at
  all is decided by [consent-verification](../consent-verification/SKILL.md), not here.
- Never-engaged and lapsed-but-engaged are different populations with different responses. Confirm
  both exist and size them before recommending anything (A1, A2).
- A sunset path is bounded before it starts, and it ends in suppression rather than looping. An
  unbounded sunset is the thing it was meant to replace.
- A sunset path does not escalate frequency
  ([../../rules/frequency-rules.md#F6](../../rules/frequency-rules.md)).
- When the complaint rate is the signal, pausing sends outranks tuning them. Say so plainly rather
  than offering a content change as the remedy.
- Segment the diagnosis by acquisition source before blaming the list. One bad source reads as a
  general decline and sends remediation to the wrong place.
- Split rates by receiving domain before drawing a list-wide conclusion (D6). A collapse at one
  provider while the others hold steady is the signature of a provider-specific problem, and a
  list-wide suppression is the wrong response to it.
- Read the trend, not the level (D3). A rate sitting where it has always sat is not a finding; the
  same rate moving in one direction over successive sends is. Where history is too short for a
  trend, say the level is uninterpretable rather than comparing it to a published figure.
- Inbox placement is not observable from sending data (D7). Engagement movement by receiving domain
  is the closest proxy and is labelled as a proxy, never reported as "we are in the spam folder".
- Authentication and reputation are the layer above this one (D1). Where the diagnosis points there,
  hand it to [deliverability-qa](../deliverability-qa/SKILL.md) rather than proposing suppression as
  a remedy for a problem suppression does not touch (D8).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read rates, variance, suppression state, engagement recency, acquisition source | `read_only` |
| ANALYZE | Locate concentration; classify contacts into the three responses | `analysis` |
| PLAN | Suppression set, sunset path and its bound, pause recommendation, alert threshold | `recommendation` |
| PREVIEW | Present each group with its size, prior value and what is lost | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the suppression and any pause | — |
| EXECUTE | Materialise the sunset audience | `mutation` |
| — | **Suppressing contacts** | `destructive`, explicit approval after reporting what is lost |
| — | **Pausing or resuming sending** | `high_impact`, explicit approval |
| MEASURE | Rate movement after the change, against the pre-change baseline | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the current rates with the
store's own variance and the derived alert threshold; where the problem concentrates; the three
contact groups with sizes and prior value; the suppression recommendation with what it costs; the
sunset path with its bound and terminus; whether sending should continue meanwhile; and the risks,
including the revenue forgone.

## Validation

- [ ] Rates compared against this store's own recent variance, not a published benchmark (G2)
- [ ] Rate change distinguished from volume change
- [ ] Concentration located by acquisition source and cohort before any list-wide recommendation
- [ ] Hard and soft failures given different responses
- [ ] Suppression set sized, and its prior value stated (S6)
- [ ] Never-engaged and lapsed-but-engaged sized separately (A1, A2)
- [ ] Sunset path bounded, with its terminus stated before it starts
- [ ] Pause recommendation made explicitly where the complaint rate warrants it
- [ ] No suppressed or unsubscribed contact proposed for re-entry (S7)
- [ ] No parallel suppression mechanism proposed outside the platform (G10)
- [ ] Rates split by receiving domain before any list-wide conclusion (D6)
- [ ] Trend read over successive sends, not a single level (D3)
- [ ] Placement claims stated as proxies, never asserted (D7)
- [ ] Authentication and reputation questions routed to deliverability-qa rather than answered here (D1)
- [ ] What could not be checked is declared (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse rates and cohorts | `read_only` / `analysis` | None |
| Recommend the response | `recommendation` | None |
| Materialise a sunset audience | `mutation` | Preview, then confirm |
| **Send any sunset message** | `high_impact` | **Explicit, per send** |
| **Suppress contacts** | `destructive` | **Explicit**, after reporting count and prior value (S6) |
| **Pause or resume sending** | `high_impact` | **Explicit** |

## Examples

**"Our bounce rate is climbing and we're landing in spam."**
Separates the two signals rather than treating them as one. Finds the bounce rise concentrated in
contacts from a single acquisition source over a recent window, and the spam placement associated
with a never-engaged cohort acquired much earlier. Recommends suppressing the permanent failures
immediately, a bounded sunset for the never-engaged, and fixing the capture source — because
suppressing the bounces without fixing the source means the same rise again next month. Rejected:
rewriting subject lines, which was the store's assumption and addresses neither signal.

**"Should we just delete everyone who hasn't opened in a year?"**
Sizes the cohort and reports its prior value, which turns out to include a group of infrequent
high-value buyers whose purchase interval is longer than the proposed window. Recommends splitting
them out and sunsetting the rest, because a window derived from opens alone discards customers who
buy without opening. Rejected: the single-window deletion, and also the alternative of leaving the
cohort alone, which is what created the placement problem.

## Failure Handling

| Situation | Response |
|---|---|
| Suppression and consent data unavailable | **Blocked.** Deciding who leaves the sending population without knowing who is already excluded risks proposing suppression twice or missing it entirely |
| Bounce classification unavailable | **Blocked.** Treating all failures alike either keeps mailing dead addresses or discards deliverable ones; do not guess the classification (S12) |
| Rate history too short to establish variance | **Partial.** Report levels rather than movement, state that no threshold can be derived yet, and recommend the measurement before the intervention |
| Engagement recency unavailable | **Partial.** Recommend only on bounce and complaint signal; say that never-engaged contacts cannot be separated from quiet ones |
| Prior value unavailable | **Partial.** Present suppression without its revenue cost, and label the trade-off as unquantified (G15) |
| Acquisition source unavailable | **Partial.** Diagnosis stays list-wide; state that a single bad source cannot be ruled out |
| Store refuses the suppression | Proceed with the rest of the plan, restate the deliverability cost to every other send plainly, and record it as an accepted risk |
| Complaint rate already at a level that risks a block | Recommend pausing sends first. Do not offer a content change as the remedy |
| Rates cannot be split by receiving domain | **Partial.** Diagnosis stays list-wide; state that a single-provider cause cannot be ruled out (D6) |
| The concentration points at authentication or reputation | Hand to deliverability-qa with the evidence attached. Suppression does not remedy a layer it cannot reach (D1, D8) |
| No placement signal of any kind exists | Expected, not an error. Report placement as unknown and present engagement movement by domain as a proxy (D7) |

Degraded outcomes set `status` and populate `unmet_requirements`.
