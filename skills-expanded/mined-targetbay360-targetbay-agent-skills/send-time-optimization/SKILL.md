---
name: send-time-optimization
description: Use when the question is what hour and which day a message should go out — whether one send time for the whole list beats a per-contact time derived from when each person last engaged, whether this store has enough engagement history for per-contact timing to be anything other than noise, how local time zones and quiet hours bound the answer, and how to test a timing change without confounding it with a content change at the same time. Answers "when is the best time to send?", "does it matter what day we send on?" and "should we let it pick a time per person?". Use channel-optimization when the question is which channel carries the message, and automation-architect when the question is the delay between steps inside a journey rather than the hour a send goes out.
license: MIT
metadata:
  targetbay.display_name: Send-Time Optimization
  targetbay.version: "1.0.0"
  targetbay.category: optimization
  targetbay.requires: email_sms.campaign_analytics, email_sms.customer_intelligence, email_sms.automation_analytics, email_sms.segmentation, email_sms.experimentation, email_sms.suppression_and_consent
  targetbay.composes: ab-testing
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Send-Time Optimization

## Purpose

Decide which granularity of send timing this store's data can actually support — one time for
everyone, one per segment, or one per contact — and refuse the finer grain when the evidence cannot
carry it.

The failure this prevents is adopting per-contact timing on a difference inside the store's own
week-to-week variance. Per-contact timing needs engagement events *per person* — depth, not volume
([../../rules/personalization-rules.md#P10](../../rules/personalization-rules.md)) — which most
stores do not have. The opposite failure is treating the current send time as a fact when nobody ever
chose it (C6).

This skill recommends; it does not send.

## When to Use

- Choosing when a campaign should go out, and on which day
- Deciding whether per-contact send timing is worth adopting
- The current send time was inherited rather than chosen, and nobody can say why it is that time
- An international list is being sent to on a single clock
- Designing a test that isolates timing from content

## When Not to Use

- The question is which channel carries the message. Use
  [channel-optimization](../channel-optimization/SKILL.md).
- The question is which date in the month a campaign should land on, against everything else planned.
  Use [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md).
- The question is the delay between steps inside a journey. Use
  [automation-architect](../automation-architect/SKILL.md), which owns journey timing.
- The campaign underperformed and the cause is not yet established. Use
  [campaign-optimization](../campaign-optimization/SKILL.md) — timing is one candidate among several
  and is rarely the first.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Engagement events with timestamps, per contact | The only evidence per-contact timing can rest on | Blocked for per-contact; segment level may still be possible |
| Send volume and list size | Whether a timing difference could be detected at all | Blocked |
| Historical results by send hour and weekday | The current baseline, and its variance | Blocked |
| Week-to-week variance of the outcome metric | Separates a real timing effect from normal movement | Blocked |
| Time zone distribution across the list | Whether one clock is even coherent | Partial; assume one zone and state the assumption |
| Quiet-hours and frequency configuration | Bounds the answer, particularly on SMS | Blocked for SMS |
| What else is scheduled in the window | A better hour occupied by another send is not available | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.campaign_analytics` | Results by hour and weekday, and the variance around them |
| `email_sms.customer_intelligence` | Per-contact engagement timestamps and time zone, where held |
| `email_sms.automation_analytics` | Whether journey-carried messages show a different timing profile from campaigns |
| `email_sms.segmentation` | Sizing a per-segment timing split, and whether the segments survive it |
| `email_sms.experimentation` | Running the timing test and reading its result |
| `email_sms.suppression_and_consent` | Quiet-hours configuration and per-channel constraints that bound the answer |

## Decision Process

```
1. Establish the current time, and whether it was ever chosen
2. Read results by hour and weekday, and the variance around them
3. Ask the resolvability question first          ← delegated to ab-testing
     can this volume detect a difference the size we expect?
4. If no — stop. Recommend the current time and say why finer is unmeasurable
5. If yes — establish the coarsest grain the evidence supports
     one time · one per segment · one per contact
6. Check per-contact engagement depth               ← events per person, not events in total
7. Bound by time zone, quiet hours and channel
8. Check the window is free of other sends
9. Design the test so timing is the only variable
10. Recommend, with the expected effect and the variance it must clear
```

## Decision Rules

Binding: [../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md).

- Timing is a decision and must be stated as one, with its reason. An inherited send time is not an
  answer (C6).
- **Resolvability comes before granularity.** If the store's volume cannot detect the expected
  difference, the recommendation is to keep the current time — and that is a result, not a failure.
  Delegate the sizing to [ab-testing](../ab-testing/SKILL.md).
- Recommend the coarsest grain the evidence supports: a large list of one-event contacts supports
  nothing finer than a single time (P10).
- Per-contact timing is personalisation (P8) on verified data only — a contact with no engagement
  history gets the default, not an inferred time (P1).
- Local time and quiet hours bound every recommendation, and on SMS they are a legal constraint
  rather than a courtesy (F9, F7).
- One variable per test. A timing change shipped alongside a subject-line change produces a winner
  and no knowledge (C10).
- A better hour that is already occupied by another send is not available. Check the calendar before
  recommending it (C1, C7).
- Derive every threshold and window from this store's own history. Published "best time to send"
  figures describe someone else's list (G2).
- Report the variance the effect must clear alongside the effect itself. An uplift smaller than the
  store's week-to-week movement has not been observed (G14).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read results by hour and weekday, variance, engagement depth, time zones, quiet hours | `read_only` |
| ANALYZE | Test resolvability; establish the supportable grain; bound by channel and zone | `analysis` |
| PLAN | Recommend the grain and the time, with the test that would confirm it | `recommendation` |
| PREVIEW | Present the recommendation with the effect it must clear to be real | `recommendation` |
| VALIDATE | Run the checks below | — |

This skill does not mutate. Scheduling or sending at the recommended time is done by the calling
skill, as a `high_impact` action requiring explicit approval.

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the current send time and
whether it was chosen; results by hour and weekday with the store's own variance; the resolvability
verdict; the recommended grain and the evidence supporting it; the recommended time or times, bounded
by zone and quiet hours; the test design that would confirm it, with one variable; and the risks,
including the case where the recommendation is to change nothing.

## Validation

- [ ] Current send time established, and whether it was ever a decision (C6)
- [ ] Resolvability tested before any granularity is recommended, via [ab-testing](../ab-testing/SKILL.md)
- [ ] Recommended grain is the coarsest the evidence supports (P10)
- [ ] Per-contact grain justified on events *per person*, not aggregate volume
- [ ] Contacts without engagement history assigned the default rather than an inferred time (P1)
- [ ] Time zone distribution stated, or the single-zone assumption declared (G15)
- [ ] Quiet hours applied, and treated as binding on SMS (F9, F7)
- [ ] Recommended window checked against what else is scheduled (C1, C7)
- [ ] Test design isolates timing as the only variable (C10)
- [ ] Expected effect reported alongside the variance it must clear (G14)
- [ ] No published external timing benchmark used as this store's answer (G2)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read results, engagement depth and configuration | `read_only` / `analysis` | None |
| Recommend a time and a grain | `recommendation` | None |
| Schedule or send at the recommended time | `high_impact` | Handled by the calling skill; explicit approval |
| Adopt per-contact timing where resolvability failed | — | **Not recommended by this skill.** The recommendation is the current time (G2) |

## Examples

**"When is the best time to send our emails?"**
Reads results by hour and weekday and finds an apparent best hour whose advantage is smaller than the
store's own week-to-week variance at this volume. Recommends keeping the current time, states the
size of difference the store *could* detect, and notes that the question becomes answerable at
roughly double the volume. Rejected: the apparent winner, which was noise, and also a published
"best time" figure the store had found, which describes a different list.

**"Should we let it pick a time per person?"**
Finds enough total engagement events but a median of very few per contact — so per-contact timing
would be fitting a pattern to one or two data points for most of the list. Recommends a per-segment
split instead, on the two segments whose engagement depth supports it, with everyone else on the
store-wide time. Rejected: full per-contact timing, and also the do-nothing option, since the two
deep segments do show a real and resolvable difference.

## Failure Handling

| Situation | Response |
|---|---|
| Historical results by hour and weekday unavailable | **Blocked.** There is no baseline to improve on, and no variance to judge a difference against |
| Variance cannot be computed from the history available | **Blocked.** An effect cannot be distinguished from normal movement; recommend collecting before deciding |
| Per-contact engagement timestamps unavailable | **Partial.** Recommend at store or segment grain only, and state that per-contact timing could not be assessed (S12) |
| Engagement depth per contact too thin | Recommend the coarser grain. This is the expected outcome for most stores and is reported as a finding, not a limitation |
| Time zone distribution unavailable | **Partial.** Assume a single zone, state the assumption, and flag it as the first thing to check for an international list (G15) |
| Quiet-hours configuration unavailable | **Blocked** for SMS; **partial** for email, with the constraint stated as unverified (F9) |
| Calendar occupancy unavailable | **Partial.** Recommend the window and state that a collision with another send could not be ruled out (C7) |
| Store wants per-contact timing despite an unresolvable test | Recommend against it, state that any observed difference will not be attributable, and record the decision if it is taken anyway |

Degraded outcomes set `status` and populate `unmet_requirements`.
