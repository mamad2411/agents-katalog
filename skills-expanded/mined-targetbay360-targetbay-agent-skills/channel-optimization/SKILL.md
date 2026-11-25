---
name: channel-optimization
description: Use when deciding how email and SMS should divide the work for an objective — which messages belong on which channel, which segments are reached where, how a paired email and SMS are ordered and how far apart, what each channel's version of the message actually says, and whether SMS is worth its cost for a given moment. Answers "should this be email, SMS, or both?", "what should we send on SMS?" and "how do we coordinate the two channels?". Use campaign-conflict-resolver when two sends already contend for the same contact, and audience-discovery when the question is who to reach rather than where.
license: MIT
metadata:
  targetbay.display_name: Channel Optimization
  targetbay.version: "2.1.0"
  targetbay.category: optimization
  targetbay.requires: email_sms.customer_intelligence, email_sms.campaign_analytics, email_sms.automation_analytics, email_sms.segmentation, email_sms.suppression_and_consent, email_sms.messaging_sms
  targetbay.composes: audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Channel Optimization

## Purpose

Decide which channel carries which message, for whom, and in what order.

The failure this skill prevents: treating SMS as a louder email. Sending the same content on both channels
doubles the cost, doubles the fatigue, and adds nothing.

## When to Use

- A store is introducing SMS and needs a channel strategy
- Deciding which moments in a journey or sequence warrant SMS
- Email engagement is falling in a segment that may be reachable elsewhere
- SMS costs are rising without matching revenue
- Sequencing email and SMS around a deadline or launch

## When Not to Use

- The question is who to target rather than where to reach them. Use
  [audience-discovery](../audience-discovery/SKILL.md).
- A specific campaign underperformed. Use
  [campaign-optimization](../campaign-optimization/SKILL.md) first; channel may not be the failure.
- The content is the problem. Use [content-optimization](../content-optimization/SKILL.md).
- Two sends already contend for the same contact and one must yield. Use
  [campaign-conflict-resolver](../campaign-conflict-resolver/SKILL.md) — this skill assigns channels
  ahead of time; that one arbitrates once a collision exists.
- The question is whether the store may contact these people at all, or how often. Use
  [consent-verification](../consent-verification/SKILL.md), which owns the contact policy this
  skill's assignments have to fit inside.
- The question is what hour a send goes out. Use
  [send-time-optimization](../send-time-optimization/SKILL.md); this skill decides the offset
  between two channel touches, not the clock time of either.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Consent state per channel per contact | A hard eligibility constraint | Blocked |
| Engagement by channel per segment | Which channel each group actually responds to | Blocked |
| SMS availability and cost | Whether SMS is an option and what it costs | Blocked for SMS |
| Message-level performance by channel | What each channel earns here | Partial; lower confidence |
| Quiet hours and local time configuration | Timing constraints, and legal ones for SMS | Blocked for SMS |
| Existing channel mix across campaigns and journeys | Current cadence per channel | Blocked |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.customer_intelligence` | Channel preference and engagement per segment |
| `email_sms.campaign_analytics` | Per-channel campaign performance |
| `email_sms.automation_analytics` | Per-channel node performance in journeys |
| `email_sms.segmentation` | Sizing channel-eligible audiences |
| `email_sms.suppression_and_consent` | Consent per channel, quiet hours, caps |
| `email_sms.messaging_sms` | SMS availability. **Unverified** — see [../../docs/mcp-integration.md](../../docs/mcp-integration.md) |

## Decision Process

```
1. Establish eligibility        ← consent per channel, per segment; SMS capability present?
2. Measure current mix          ← what each channel currently carries and earns
3. Classify each message        ← context-carrying, or time-critical single-action?
4. Assign channel by fit        ← not by availability
5. Split the audience by channel ← derived per segment from consent and observed response
6. Check cost against value     ← SMS must clear a higher bar per message
7. Sequence complementary sends ← email explains, SMS deadlines; decide the offset between them
8. Write the brief per channel  ← what each channel's version says, not the same words truncated
9. Check per-channel cadence    ← SMS has its own, smaller budget
10. Recommend, with what NOT to move, and who is reached on nothing
```

## Decision Rules

Binding: [../../knowledge/sms-principles.md](../../knowledge/sms-principles.md),
[../../knowledge/email-principles.md](../../knowledge/email-principles.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md).

- Consent first, observed response second, cost third (R14).
- Email consent is never SMS consent (A10).
- SMS carries one idea, one link, one action. If the message needs explaining, it is an email (N6).
- Never duplicate the same content on both channels at the same moment. Complementary sequencing or
  nothing.
- SMS must clear a higher bar: the value of immediacy must exceed the cost per recipient.
- SMS cadence is tracked separately and is much smaller (F7). SMS opt-outs are usually permanent.
- Quiet hours and local time are planning constraints, not courtesies (F9).
- For a segment that has stopped opening email, a different channel is a stronger move than more email —
  where consent exists (F6).
- Where `email_sms.messaging_sms` is unavailable, produce an email-only strategy and record the gap
  rather than planning sends that cannot happen (S12).
- The channel split across segments is **derived for this store**, from consent coverage and observed
  per-channel response, never from a fixed tier map. "VIP gets both, everyone else gets email" is a
  pattern, not a rule, and a store whose SMS consent sits mostly outside its VIP tier is worse off
  under it (G2, A9).
- Reaching a segment on nothing is a legitimate assignment. Where a segment's engagement makes
  further contact a deliverability cost rather than a revenue opportunity, say so and hand the
  population question to [list-hygiene](../list-hygiene/SKILL.md) (F6).
- When both channels carry the same moment, the **offset between them is a decision**, stated and
  justified. Two touches in the same hour is one message sent twice; two touches days apart is two
  unrelated messages.
- Each channel gets its own content brief. An SMS is not the email's subject line, and truncating
  the email is how a store teaches people that SMS carries nothing new (N6). The wording itself
  belongs to [content-optimization](../content-optimization/SKILL.md).
- Every assignment is counted against the contact's total budget across both channels, not against
  each channel separately (F2, F3). Moving a message to SMS does not make room on email.
- Where the assignment would put a contact over the ceiling, report the collision and hand it to
  [campaign-conflict-resolver](../campaign-conflict-resolver/SKILL.md) rather than resolving it here
  (F8).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent, per-channel engagement, current mix, costs, quiet hours | `read_only` |
| ANALYZE | Classify messages, measure per-channel value, size eligible audiences | `analysis` |
| PLAN | Channel assignment, sequencing, per-channel cadence | `recommendation` |
| PREVIEW | Present the mix with cost and reach implications | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves | — |
| EXECUTE | Applied by the owning campaign or automation skill | `mutation` |
| — | **Any SMS send** | `high_impact`, explicit, with count and cost |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: consented and eligible audience size
per channel; per-message channel assignment with the reason; complementary sequences where both channels
are used; per-channel cadence budget; SMS cost exposure at the recommended volume; messages explicitly
recommended to stay on email; and the quiet-hours and local-time constraints that apply.

## Validation

- [ ] Consent checked per channel, never assumed from email consent (A10)
- [ ] SMS capability availability confirmed before planning SMS (S12)
- [ ] Every SMS assignment justified by immediacy, not availability
- [ ] No duplicate content on both channels at the same moment
- [ ] SMS cost stated at the recommended volume
- [ ] Per-channel cadence budgets separate, with SMS the smaller (F7)
- [ ] Quiet hours and local time applied (F9)
- [ ] Messages that should stay on email named explicitly
- [ ] Channel split derived from this store's consent coverage and response, not a fixed tier map (G2)
- [ ] Offset between paired channel touches stated and justified
- [ ] A separate content brief produced per channel, not one truncated for the other (N6)
- [ ] Total contact counted across both channels, not per channel (F2, F3)
- [ ] Segments assigned to no contact named, with the reason (F6)
- [ ] Any resulting collision handed to campaign-conflict-resolver rather than resolved here (F8)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend a channel mix | `recommendation` | None |
| Apply to campaigns or journeys | `mutation` | In the owning skill; preview then confirm |
| **Any SMS send** | `high_impact` | **Explicit**, with recipient count and cost |

## Examples

**"We're adding SMS — what should we send on it?"**
Consent analysis shows a fraction of the list is SMS-eligible. Recommends four moments: delivery and
order updates, restock notifications, the final day of a sale window, and high-value cart recovery.
Explicitly recommends *against* moving the newsletter, launches or educational content — each needs
context SMS cannot carry, and moving them would burn the channel within weeks.

**"Should the launch go to everyone on both channels?"**
Splits by what the data supports rather than by tier. Finds SMS consent concentrated in a cohort
acquired through a checkout opt-in rather than in the high-value segment the store assumed, so a
VIP-first channel map would reach few of the people it was designed for. Assigns the launch email to
the whole consented list, an SMS on the final day to the SMS-consented cohort regardless of value
band, and no contact at all to a never-engaged segment whose inclusion would cost more in
deliverability than it could return. Sets the offset between the two touches at the point where the
email's click window has flattened, so the SMS reaches people the email did not. Rejected: the
same-day paired send, which is one message delivered twice.

**"Our SMS costs are up but revenue isn't."**
Finds SMS carrying promotional content that duplicates email sends. The cost is real, the incremental
revenue is not. Recommends cutting to deadline and operational moments, and reports the expected saving
alongside the reach that is given up.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.messaging_sms` unavailable | **Partial.** Produce an email-only strategy; record where SMS would have been used |
| Consent data unavailable | **Blocked** for SMS; email-only recommendations proceed |
| No per-channel performance history | **Partial.** Assign by message type and mark the assignments testable |
| SMS cost unknown | State the cost exposure as unquantified and recommend confirming it before volume rises |
| Quiet-hours configuration unavailable | **Blocked** for SMS scheduling; this is a legal exposure, not a preference |
| SMS-eligible audience very small | Report it; a channel strategy for a handful of contacts is not worth building |
| Per-segment consent coverage unreadable | **Partial.** Assign at list level and state that the split could not be derived, rather than falling back to a tier map (G2) |
| Assignment puts contacts over the contact ceiling | Report the collision and delegate the arbitration; do not silently drop a channel to fit (F8) |

Degraded outcomes set `status` and populate `unmet_requirements`.
