---
name: campaign-conflict-resolver
description: Use when a campaign and the automations already running would both reach the same customers at the same time, when two automations fire for the same contact, or when a seasonal push overlaps a lifecycle message or the same moment is planned on both email and SMS. Decides which send proceeds, which is delayed, which is suppressed for the overlap and which switches channel. Answers "our campaign overlaps with automations that are running, what do we do?", "two automations both fire for the same customers" and "which message wins?". Use marketing-calendar to sequence a plan before any of this arises, and channel-optimization for channel assignment absent contention.
license: MIT
metadata:
  targetbay.display_name: Campaign Conflict Resolver
  targetbay.version: "1.0.0"
  targetbay.category: planning
  targetbay.requires: email_sms.marketing_calendar, email_sms.campaign_management, email_sms.automation, email_sms.automation_analytics, email_sms.suppression_and_consent, email_sms.customer_intelligence, email_sms.segmentation
  targetbay.composes: audience-discovery
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Campaign Conflict Resolver

## Purpose

Decide what happens when more than one send reaches the same contact in the same window: which
proceeds, which is delayed, which is suppressed for that overlap only, and which moves to another
channel — and derive the priority from this store's own economics rather than from a fixed ranking.

The failure this skill exists to prevent: every send being individually correct and collectively
intolerable. Each skill counted only its own messages, the calendar showed no collision because
automations are not on it, and the contact received four messages in three days. The second failure
is the blunt fix — pausing all automations during a promotional period — which silently kills the
cart recovery that was earning more per contact than the promotion.

A universal hierarchy is not hard-coded here. Which class of message outranks which is a **store
policy**, derived, stated, and reusable once set.

## When to Use

- A planned campaign overlaps with live automations reaching the same contacts
- Two or more automations are both eligible for the same contact at the same time
- A seasonal or promotional push runs over an existing lifecycle programme
- The same moment is planned on both email and SMS and it is unclear whether that is deliberate
- Setting the store's contention policy once, so later plans resolve without re-deciding
- A frequency ceiling has been breached and the question is which send yields

## When Not to Use

- No conflict exists yet and the task is sequencing a plan so none arises. Use
  [marketing-calendar](../marketing-calendar/SKILL.md) or
  [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md).
- The question is which channel should carry a message, absent contention. Use
  [channel-optimization](../channel-optimization/SKILL.md).
- The question is how often this audience may be contacted at all. Use
  [consent-verification](../consent-verification/SKILL.md), which owns contact policy.
- One campaign needs clearing before it goes out and contention is only one of the checks. Use
  [email-quality-auditor](../email-quality-auditor/SKILL.md), which detects collisions and delegates
  here.
- Two automations overlap because the portfolio itself is wrong. Use
  [automation-strategy](../automation-strategy/SKILL.md) to consolidate them rather than arbitrating
  the same clash every month.
- The conflict is between a marketing message and a transactional one. Transactional delivery is a
  platform responsibility and is never suppressed here
  ([../../rules/global-rules.md#G10](../../rules/global-rules.md)).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Scheduled campaigns across the window | One half of the contending set | Blocked |
| Live automations and their entry conditions | The half the calendar does not show | Blocked |
| Audience overlap between the contenders | Whether a conflict exists at all, and for how many | Blocked |
| Per-contact value of each contending send | What yielding actually costs, per message | Partial; priority falls back to class |
| The store's contact ceiling for this audience | What counts as too much before anything is arbitrated | Partial |
| Channel consent per contact | Whether substitution is even available | Partial; substitution drops off the options |
| Existing contention policy, if one has been set | Consistency across months, rather than re-deciding | Partial; a policy is derived and proposed |
| Time-sensitivity of each send | A dated moment cannot be delayed; a lifecycle message usually can | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.marketing_calendar` | Scheduled and in-flight campaigns across the window, and calendar occupancy |
| `email_sms.campaign_management` | The configuration and timing of each contending campaign |
| `email_sms.automation` | Live journeys, their entry conditions and which contacts are currently inside them |
| `email_sms.automation_analytics` | Per-entrant value of each journey, which is what yielding costs |
| `email_sms.suppression_and_consent` | Channel consent, quiet hours and the caps that bound every option |
| `email_sms.customer_intelligence` | Engagement and value of the overlapping contacts, for frequency tolerance |
| `email_sms.segmentation` | Measuring the overlap and materialising any exclusion the resolution needs |

## Decision Process

```
1. Enumerate everything reaching this audience in the window   <- campaigns and automations together
2. Measure the actual overlap                                  <- how many contacts, receiving how many
3. Confirm a conflict exists                                   <- overlap below the ceiling is not a conflict
4. Establish or read the store's contention policy             <- derived from value, stated, reusable
5. Value each contender per contact reached                    <- what yielding costs, not which feels important
6. Choose the least destructive resolution per contender
     allow - delay - suppress for this overlap - substitute channel
7. Prefer delay over suppression, and suppression scoped to the overlap over a blanket pause
8. State what each yielding send gives up
9. Record the policy so the next overlap resolves the same way
```

## Decision Rules

Binding: [../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/automation-rules.md](../../rules/automation-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/safety-rules.md](../../rules/safety-rules.md).

- Resolve collisions explicitly and say which send yields (F8). An unresolved overlap is a decision
  made by whichever send happens to fire first.
- Count campaigns and automations against the same budget (F2, F3). A conflict is invisible to any
  skill that counts only its own messages.
- Automations must not compete with each other (R16). Two journeys eligible for the same contact at
  the same time is a portfolio defect surfaced here and fixed in
  [automation-strategy](../automation-strategy/SKILL.md).
- Overlapping audiences are prioritised, not ignored (A8), and the priority is derived from per-contact
  value rather than from a fixed class ranking. A cart recovery journey frequently outearns a
  promotional broadcast per contact; a store policy that always ranks broadcasts first destroys that
  quietly.
- **No universal hierarchy is hard-coded.** Where a store has stated a policy, apply it and say so.
  Where it has not, derive one from observed value, propose it explicitly, and record it for reuse.
- Prefer the least destructive resolution available. Delay beats suppression; suppression scoped to
  the overlapping contacts beats pausing a journey for everyone (G7, G16).
- Never suppress a transactional or platform-mandated message (G10). Contention is a marketing
  problem only.
- Channel substitution requires consent on the substituted channel (A10) and respects that channel's
  much lower ceiling (F7). Substitution is not a way to exceed the total budget.
- Sequence rather than overlap where the calendar allows it (C7), and check the calendar before
  arbitrating (C1).
- A dated moment cannot be delayed past its date. Say so rather than proposing a delay that voids the
  send's reason for existing.
- Do not escalate contact to a non-responder to resolve a conflict in their favour (F6).
- Show the blast radius of any suppression or pause before it is approved (S4, S6).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read calendar, live automations, entry conditions, overlap, consent, per-entrant value | `read_only` |
| ANALYZE | Measure overlap against the ceiling; value each contender; test whether a conflict exists | `analysis` |
| PLAN | Resolution per contender, the derived or applied policy, and what each yielding send gives up | `plan` |
| PREVIEW | Contacts affected per resolution, and the revenue each yield forgoes | `plan` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the resolution and any policy being set | — |
| EXECUTE | Apply exclusions, reschedule, or adjust automation entry for the overlap | `mutation` |
| — | **Pausing a live automation** | `high_impact`, explicit approval with the blast radius shown |
| MEASURE | Whether the yielding sends recovered their value after the window | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the contending sends with their
audiences and overlap size; whether a conflict exists against the store's ceiling; the contention
policy applied, or derived and proposed with its basis; the resolution per contender — allow, delay,
suppress for this overlap, or substitute channel — with the per-contact value each yield forgoes;
the blast radius of any suppression; and the resolutions rejected as more destructive than necessary.

Where the resolution requires a portfolio change rather than an arbitration, it says so and hands to
[automation-strategy](../automation-strategy/SKILL.md) rather than arbitrating the same clash again
next month.

## Validation

- [ ] Campaigns and automations enumerated together, not separately (F2, F3)
- [ ] Overlap measured, not assumed — a conflict is a count, not an impression
- [ ] The store's ceiling used to decide whether a conflict exists at all
- [ ] Priority derived from per-contact value, or from a stated store policy (A8)
- [ ] No universal class hierarchy assumed
- [ ] Least destructive resolution chosen, with the more destructive ones recorded as rejected (G7)
- [ ] Suppression scoped to overlapping contacts rather than blanket, wherever possible
- [ ] Transactional and platform-mandated messages excluded from arbitration (G10)
- [ ] Channel substitution checked against consent and the substituted channel's ceiling (A10, F7)
- [ ] Dated moments not proposed for a delay past their date
- [ ] Blast radius shown before any suppression or pause is approved (S4)
- [ ] Recurring conflicts flagged as a portfolio defect rather than re-arbitrated (R16)
- [ ] The resolution recorded as a reusable policy

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read calendar, automations and overlap | `read_only` / `analysis` | None |
| Produce the resolution plan | `plan` | None |
| Apply an exclusion or reschedule a campaign | `mutation` | Preview, then confirm |
| **Pause or alter entry to a live automation** | `high_impact` | **Explicit**, with contacts affected and value forgone shown (S4) |
| **Send anything after the resolution** | `high_impact` | **Explicit**, owned by the sending skill |

## Examples

**"Our Black Friday campaign goes to everyone, but we have five automations running."**
Enumerates both and measures the overlap rather than assuming it. Finds most of the list is in no
journey at all, a small group is mid-way through cart recovery, and a smaller one is in a
post-purchase sequence. Values each: the cart journey earns materially more per contact over the
window than the broadcast does, so the store's instinct to pause automations during the promotion
would trade its highest-value messages for its lowest. Recommends allowing the broadcast, suppressing
it for cart-recovery contacts for the duration of their journey only, and delaying the post-purchase
sequence's non-urgent third message past the peak. Rejects the blanket automation pause with the
forgone revenue stated, and rejects doing nothing, which puts the overlapping contacts above the
store's own ceiling. Records the resulting policy so December resolves without re-deciding.

**"Two automations both fire for customers who buy a subscription product."**
Establishes that this is not an arbitration problem. Both journeys are eligible by design, the
overlap is complete rather than incidental, and resolving it monthly would mean deciding the same
thing forever. Reports it as a portfolio defect under R16, proposes a one-off tie-break to stop the
immediate double-sending, and hands the consolidation to automation-strategy. Declines to install a
permanent suppression rule, which would hide the defect rather than fix it.

## Failure Handling

| Situation | Response |
|---|---|
| Calendar unavailable | **Blocked.** Contention cannot be arbitrated against an unknown set of contenders |
| Live automations or entry conditions unavailable | **Blocked.** Arbitrating campaigns alone misses the half that is not on the calendar (F3) |
| Audience overlap cannot be measured | **Blocked.** A conflict is a count; without it, any resolution is speculative |
| Per-entrant value unavailable | **Partial.** Priority falls back to the store's stated policy, or to a proposed one whose basis is declared as class rather than value (G15) |
| No contact ceiling established for this store | **Partial.** Derive a working ceiling from observed cadence and engagement, state it as derived, and recommend setting it properly (F4) |
| Channel consent unreadable | **Partial.** Substitution drops off the available resolutions; say so rather than proposing it unverified (A10) |
| The same conflict has been arbitrated before | Report it as recurring, apply the recorded policy, and recommend the portfolio fix rather than a third arbitration (R16) |
| Every resolution still breaches the ceiling | Say so plainly and recommend which send should not run at all. A resolution that leaves the contact over the ceiling has not resolved anything |
| Store asks to pause all automations for the period | Present the forgone value per journey and the alternative scoped resolution. Proceed on their decision and record it as an accepted cost |

Degraded outcomes set `status` and populate `unmet_requirements`.
