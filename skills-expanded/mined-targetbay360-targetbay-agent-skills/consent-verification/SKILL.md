---
name: consent-verification
description: Use when setting the standing policy for who a store may contact and how much — whether people must confirm before anything is sent to them, what to do with contacts imported or inherited with no provable consent record, and separately how many messages a segment should receive in a period across email and SMS together before contact becomes a cost. Answers "should we use double opt-in?", "can we mail this list we acquired?" and "how often is too often to email our customers?". Use list-hygiene when the list is consented and the problem is bounces, and campaign-conflict-resolver when specific sends already breach the ceiling this skill sets.
license: MIT
metadata:
  targetbay.display_name: Consent and Contact Policy
  targetbay.version: "1.1.0"
  targetbay.category: audience
  targetbay.requires: email_sms.suppression_and_consent, email_sms.customer_intelligence, email_sms.segmentation, email_sms.campaign_analytics, email_sms.store_profile, email_sms.automation, email_sms.marketing_calendar
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Consent Verification

## Purpose

Decide how a store establishes and evidences permission to message, per channel — and decide what
happens to contacts whose permission cannot be evidenced at all.

Confirming everywhere loses real subscribers at the point of highest intent and gains nothing where
capture was already clean. Confirming nowhere accumulates typos, other people's addresses and records
of unknown origin, and the cost arrives as complaints and blocks. Make the trade explicitly rather
than defaulting either way.

The same standing question has a second half the rules already bind but no skill has derived: how
much contact a segment should receive. [../../rules/frequency-rules.md](../../rules/frequency-rules.md)
gives F1 to F12 and every planning skill cites them, but each one counts only its own messages, so
the ceiling itself is never set anywhere. This skill sets it — per segment, per channel, and as a
combined total — so the planning skills have something to plan below and
[campaign-conflict-resolver](../campaign-conflict-resolver/SKILL.md) has something to arbitrate
against.

Permission and cadence are one policy because a contact who may lawfully be reached is not
automatically a contact who should be reached weekly.

This skill decides the policy; the capture and confirmation mechanics belong to the platform and to
[the best-practices skill](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/SKILL.md)
([../../rules/global-rules.md#G10](../../rules/global-rules.md)).

## When to Use

- Deciding whether to require a confirmation step before a contact enters the sending population
- A list has been imported, acquired or inherited and its origin cannot be evidenced
- Setting different consent requirements for email and SMS
- Deciding whether a re-permission pass is justified before mailing a list again
- Signup volume is healthy but complaint or bounce rates suggest the capture is not
- Setting how many messages a segment should receive in a period, across both channels
- Unsubscribe or complaint rates are rising while content quality has not changed
- Deciding which class of message yields when a contact is near the ceiling
- A planning skill needs a cadence assumption and none has been stated for this store

## When Not to Use

- The list is consented and the problem is bounces, complaints or placement. Use
  [list-hygiene](../list-hygiene/SKILL.md).
- The question is who to target among contacts you may lawfully reach. Use
  [audience-discovery](../audience-discovery/SKILL.md).
- The question is which channel carries a message to a consented contact. Use
  [channel-optimization](../channel-optimization/SKILL.md).
- The store is being set up and consent is one item among many. Use
  [store-onboarding](../store-onboarding/SKILL.md), which routes back here for this decision.
- Specific sends already contend and one must yield now. Use
  [campaign-conflict-resolver](../campaign-conflict-resolver/SKILL.md) — this skill sets the ceiling,
  that one arbitrates against it.
- One campaign's unsubscribe rate is the concern rather than the programme's cadence. Use
  [campaign-optimization](../campaign-optimization/SKILL.md).
- Contacts are already disengaged and the question is suppression. Use
  [list-hygiene](../list-hygiene/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Consent state and its provenance per contact, per channel | Whether permission can be evidenced at all | Blocked |
| Capture points in use, and what each one asks for | A blanket policy cannot be set across mismatched capture | Blocked |
| Complaint and bounce rates by acquisition source | Whether the current capture is actually producing a problem | Blocked |
| Signup volume by source | What a confirmation step would cost in growth | Partial; the trade cannot be quantified |
| Jurisdictions the store's contacts sit in | Which regimes bind, and where SMS rules differ sharply from email | Partial; recommend the stricter reading and say so |
| Whether the platform can hold an unconfirmed pending state | Whether verification is a platform or an external step | Partial |
| Current contact volume per segment across campaigns and automations | The cadence actually being delivered, which is rarely the cadence assumed | Blocked for the cadence half |
| Unsubscribe and complaint rate against contact volume per segment | Where this store's tolerance actually sits | Blocked for the cadence half |
| Engagement by segment | Tolerance varies by segment; one ceiling for everyone is wrong at both ends | Partial; a single ceiling is derived and flagged as coarse |
| The platform's configured caps and quiet hours | The floor the policy has to sit below | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.suppression_and_consent` | Consent state and provenance per channel; what is already suppressed |
| `email_sms.customer_intelligence` | Contact origin, acquisition source, engagement after signup |
| `email_sms.segmentation` | Sizing the unevidenced cohort and any re-permission audience |
| `email_sms.campaign_analytics` | Complaint and bounce rates by source, which is the evidence that capture is failing |
| `email_sms.store_profile` | Where the store and its contacts sit, and which capture points exist |
| `email_sms.automation` | Live journeys, whose messages share the same contact budget as campaigns (F3) |
| `email_sms.marketing_calendar` | Scheduled campaign volume per period, the other half of delivered cadence |

## Decision Process

```
1. Establish what consent evidence exists today, per channel, per source
2. Separate three populations
     evidenced · weakly evidenced · not evidenced at all
3. For the unevidenced: decide reachability             ← usually the answer is no, and no pass fixes it
4. Read complaint and bounce rate by source             ← is current capture actually failing?
5. Decide per channel, not once                         ← SMS is bound more tightly than email
6. Quantify what a confirmation step costs in signups   ← from this store's own volume
7. Set the requirement per capture point, not globally
8. Define the consent record: what is stored, and what it must prove

Then the cadence half, which reuses the populations above:

9.  Measure delivered contact per segment            ← campaigns and automations together, both channels
10. Plot unsubscribe and complaint against that volume ← where tolerance actually turns
11. Derive the ceiling per segment                   ← from this store's own turn, not a published figure
12. Split it per channel                             ← SMS gets its own, much smaller share
13. Decide what yields when a send would exceed it   ← class precedence, stated and reusable
14. Set the peak allowance and the recovery window after it
```

## Decision Rules

Binding: [../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md).

- A list with no provable consent record does not get mailed. No warm-up schedule, staged send or
  re-permission campaign launders it — a re-permission message to a list you may not mail is itself a
  message to a list you may not mail (S7).
- Consent is per channel (A10), and that includes a phone number sitting on an email-consented record.
- Deciding to require confirmation is a trade with a number on each side. State the expected signup
  loss from this store's own volume and the complaint exposure it removes; never assert that one
  outweighs the other without both (G2, G14).
- The decision is per capture point. A checkout box, a popup and an in-person signup have different
  evidence quality and may reasonably get different requirements.
- Consent evidence is what was agreed to, when, and through which capture point. A boolean flag with
  no provenance is not evidence and should be treated as weakly evidenced.
- Never infer consent from a transaction, an enquiry or the presence of contact details (A9, G12).
- Where jurisdiction is unknown, recommend on the stricter reading and record that it was a
  jurisdiction assumption rather than a finding (G15).
- Where the store insists on mailing an unevidenced list, this skill does not plan that send. It
  states the exposure and records the refusal (S8).
- Suppression state outranks any consent record. A suppressed contact stays suppressed regardless of
  what a later capture claims (S7).
- The platform's caps are the floor the policy sits below, never the target (F1). A policy that
  restates the platform's cap has decided nothing.
- The ceiling counts campaigns and automations together and both channels together (F2, F3). A
  segment-level figure that excludes journey messages is the number that produced the problem.
- The ceiling is derived from where *this store's* unsubscribe and complaint rates turn against
  contact volume, never from a published cadence recommendation (G2). This package ships no
  benchmarks.
- Tolerance varies by segment (F5). Recently active buyers and dormant contacts do not get the same
  ceiling, and the dormant one goes down rather than up (F6).
- SMS carries its own ceiling, much smaller, and consuming it does not release email capacity (F7).
- The policy states which class of message yields when the ceiling is reached, and that precedence is
  **derived and recorded**, not assumed. Handing the arbitration of a specific clash to
  [campaign-conflict-resolver](../campaign-conflict-resolver/SKILL.md) is what makes it reusable (F8).
- A peak period may raise the ceiling, but the raised figure is bounded and paired with the
  reduced-contact window that follows it (F10, F12).
- Every ceiling is stated as an assumption a planning skill can read and a human can correct (F4).
  An undeclared cadence assumption cannot be reviewed.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent state and provenance, capture points, rates by source, signup volume | `read_only` |
| ANALYZE | Separate evidenced, weakly evidenced and unevidenced; quantify the trade | `analysis` |
| PLAN | Requirement per capture point per channel; treatment of the unevidenced; the consent record | `recommendation` |
| PREVIEW | Present the trade with both numbers, and the unevidenced cohort with its size | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the policy and any suppression | — |
| EXECUTE | Materialise the affected audiences | `mutation` |
| — | **Sending a re-permission message to an evidenced list** | `high_impact`, explicit approval |
| — | **Suppressing an unevidenced cohort** | `destructive`, explicit approval after reporting size |
| MEASURE | Signup volume and complaint rate after the change, against the pre-change baseline | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the three consent populations
with sizes; the confirmation requirement per capture point per channel, with the expected signup cost
and the complaint exposure removed; the treatment of the unevidenced cohort, including any refusal to
mail it; the consent record specification; jurisdiction assumptions made; and the risks.

## Validation

- [ ] Consent evidence assessed per channel, not once (A10)
- [ ] The three populations sized separately
- [ ] Unevidenced contacts not proposed for any send, including re-permission (S7)
- [ ] Signup cost quantified from this store's own volume, not asserted (G2)
- [ ] Complaint and bounce rates read by source before concluding capture is or is not failing
- [ ] Requirement set per capture point rather than globally
- [ ] Consent record specified: what was agreed, when, through which capture point
- [ ] No consent inferred from a transaction, an enquiry or the presence of contact details (A9)
- [ ] Jurisdiction assumptions recorded where jurisdiction is unknown (G15)
- [ ] Suppression state confirmed to outrank any capture record (S7)
- [ ] Delivered contact measured across campaigns and automations, both channels (F2, F3)
- [ ] Ceiling derived from where this store's own rates turn, not a published figure (G2)
- [ ] A separate ceiling per segment, with dormant segments lower rather than higher (F5, F6)
- [ ] SMS ceiling stated separately and smaller, and not treated as email capacity (F7)
- [ ] Class precedence recorded so the next clash resolves the same way (F8)
- [ ] Peak allowance bounded and paired with a recovery window (F10, F12)
- [ ] Every ceiling stated explicitly as a reviewable assumption (F4)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse consent state | `read_only` / `analysis` | None |
| Recommend the policy | `recommendation` | None |
| Materialise an affected audience | `mutation` | Preview, then confirm |
| **Send a re-permission message to an evidenced list** | `high_impact` | **Explicit** |
| **Suppress an unevidenced cohort** | `destructive` | **Explicit**, after reporting size (S6) |
| **Mail a list with no provable consent record** | — | **Refused.** Not planned by this skill (S7, S8) |

## Examples

**"Should we make people confirm their email before we send anything?"**
Reads complaint and bounce rates by source and finds the popup producing most of both while the
checkout box produces almost none. Recommends confirmation on the popup only, quantifies the signup
loss from the store's own popup volume against the complaint exposure it removes, and leaves checkout
unchanged. Rejected: a store-wide requirement, which would have cost signups at the cleanest capture
point in exchange for nothing.

**"How often is too often to email our customers?"**
Measures what the store is actually delivering rather than what it believes it sends, and finds
campaigns are only part of it — contacts inside two live journeys receive materially more, which is
the group whose unsubscribe rate is rising. Plots unsubscribes against delivered volume per segment
and finds the turn sits in different places for recently active buyers and for the long-quiet
cohort. Sets a ceiling per segment rather than one for the store, lower for the quiet cohort rather
than higher, a separate and much smaller SMS ceiling, and a bounded peak allowance for the sale
period with the reduced window that follows it. Records which class of message yields at the
ceiling, so the next clash is arbitrated rather than re-decided. Rejected: a single store-wide
weekly figure, which would have been too much for the quiet cohort and too little for the segment
already tolerating more.

**"Import this list we bought and start the welcome series."**
Refuses. There is no consent record to evidence, so no send is planned — including a re-permission
message, which is itself a send to a list the store may not mail. States the exposure plainly:
complaint rate, provider blocks, and a reputation cost carried by every other send the store makes.
Offers the alternative that does work — capture these contacts through a channel where they act
first, verified at the point of signup. Rejected: the staged warm-up the store proposed, which
changes the rate of the exposure and not its nature.

## Failure Handling

| Situation | Response |
|---|---|
| Consent state or provenance unavailable | **Blocked.** A policy cannot be set without knowing what is evidenced today, and assuming consent is the error this skill exists to prevent (S12) |
| Capture points unknown | **Blocked.** A blanket policy across mismatched capture is either too strict at the clean points or too loose at the dirty ones |
| Complaint and bounce rates unavailable by source | **Partial.** Recommend on capture-quality reasoning alone, and state that the evidence for which source is failing is missing |
| Signup volume unavailable | **Partial.** Present the trade qualitatively and label the cost side as unquantified (G15) |
| Jurisdiction unknown | **Partial.** Recommend on the stricter reading and record the assumption |
| Platform cannot hold a pending unconfirmed state | **Partial.** The confirmation step is external; say so, and note the additional failure surface that adds |
| Store insists on mailing an unevidenced list | **Refused.** State the exposure, record the refusal and the reasoning, and stop. Do not produce a send plan for it (S8) |
| Delivered contact volume unavailable | **Blocked for the cadence half.** The consent policy still ships; state that no ceiling can be derived because the current cadence is unknown (F2) |
| Automation message volume unreadable | **Partial.** Derive the ceiling from campaign volume alone and state plainly that it understates delivered contact (F3) |
| Rates cannot be plotted against volume | **Partial.** Set the ceiling at the store's current delivered level as a hold-steady position, labelled as a placeholder rather than a derived figure (G15) |
| Engagement unavailable by segment | **Partial.** Derive one ceiling for the store, flag it as coarse, and say which segments it is likely wrong for (F5) |
| Platform caps unreadable | **Partial.** Set the policy without confirming the floor, and say the policy may sit above a cap it could not read (S12) |

Degraded outcomes set `status` and populate `unmet_requirements`.
