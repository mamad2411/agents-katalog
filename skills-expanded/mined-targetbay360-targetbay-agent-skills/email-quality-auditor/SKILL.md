---
name: email-quality-auditor
description: Use as the last check before a campaign is sent or an automation is switched on — sweeping audience, consent, suppression, recent contact, personalisation fallbacks, links, opt-out, offer accuracy, product availability, collisions with other sends and the sending programme's condition, then returning one verdict with every objection stated. Answers "can we safely send this?", "is this campaign ready?", "check this before it goes out" and "review this automation before we switch it on". Use campaign-optimization when a campaign has already run and underperformed, and deliverability-qa when the sending programme rather than one message is in question.
license: MIT
metadata:
  targetbay.display_name: Email Quality Auditor
  targetbay.version: "1.0.0"
  targetbay.category: optimization
  targetbay.requires: email_sms.campaign_management, email_sms.segmentation, email_sms.suppression_and_consent, email_sms.template_management, email_sms.campaign_analytics, email_sms.product_intelligence, email_sms.marketing_calendar, email_sms.customer_intelligence
  targetbay.composes: deliverability-qa, email-render-qa, dynamic-content-personalizer, audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Email Quality Auditor

## Purpose

Stand between a finished campaign and a real audience. Sweep every dimension that can make a send
wrong, return a single verdict — **PASS**, **WARN** or **BLOCK** — and state the reason for every
objection so a human can decide rather than guess.

The failure this skill exists to prevent: a send that was correct in each part and wrong as a whole.
Every skill upstream optimised its own dimension and none of them counted what the recipient
actually receives. The audience was fine, the copy was fine, the offer was fine, and the contact got
their fourth message in three days containing a discount on a discontinued product.

The second failure is a gate that blocks everything, which teaches people to skip it. **BLOCK is
narrow and reserved.** Most real defects are WARN with the cost stated, and the store decides.

## When to Use

- A campaign is built and someone is about to schedule or send it
- A store asks whether a send is safe, ready, or likely to cause a problem
- Reviewing a send that a person feels uneasy about without being able to say why
- Before activating an automation that will send unattended
- Auditing a recurring send that has not been re-checked since it was built

## When Not to Use

- The campaign has already run and underperformed. Use
  [campaign-optimization](../campaign-optimization/SKILL.md).
- The sending programme rather than one campaign is the question — authentication, reputation,
  ramping. Use [deliverability-qa](../deliverability-qa/SKILL.md), which this skill composes for
  that dimension.
- Two sends contend and the question is which one yields. Use
  [campaign-conflict-resolver](../campaign-conflict-resolver/SKILL.md), which decides the
  arbitration; this skill only detects the collision and reports it.
- Only rendering is in doubt. Use [email-render-qa](../email-render-qa/SKILL.md).
- Whether a list may lawfully be mailed at all. Use
  [consent-verification](../consent-verification/SKILL.md).
- The campaign does not exist yet. Use
  [monthly-marketing-planner](../monthly-marketing-planner/SKILL.md) or the skill that owns the
  objective.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The campaign as configured — audience, content, schedule, offer | The object being audited | Blocked |
| Resolved audience size after exclusions | The blast radius, which every approval depends on | Blocked |
| Consent state and suppression list for the resolved audience | The one dimension where a defect is a stop, not a warning | Blocked |
| Recent contact history for the same audience | Whether this send is the fourth message in three days | Partial; frequency cannot be judged |
| Calendar occupancy and live automations over the send window | Detects collisions with other sends | Partial; conflicts go undetected |
| Personalisation scheme and its fallbacks | The empty case is the most common silent defect | Partial |
| Availability and price for every product referenced | Stops a send promoting what cannot be bought | Partial; must be reported unverified |
| Offer terms as stated, and as configured | An offer the store cannot honour is a claim it cannot support | Blocked for offer campaigns |
| The sending programme's current condition | A sound campaign onto a failing programme still fails | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.campaign_management` | The campaign's configuration, schedule and offer as set up |
| `email_sms.segmentation` | Resolving the audience and its size after exclusions |
| `email_sms.suppression_and_consent` | Consent per channel, suppression state, quiet hours and caps |
| `email_sms.template_management` | The built message, its links, footer, opt-out and dynamic elements |
| `email_sms.campaign_analytics` | Recent contact history, and the programme's engagement and complaint posture |
| `email_sms.product_intelligence` | Availability and price of every product the message references |
| `email_sms.marketing_calendar` | Other campaigns and automations reaching this audience in the window |
| `email_sms.customer_intelligence` | Lifecycle and engagement of the resolved audience, for frequency tolerance |

## Decision Process

```
1. Resolve the audience and state the blast radius    <- every later judgement is scaled to it
2. Run the stop conditions first                      <- consent, suppression, opt-out, unsupportable claim
3. Stop and return BLOCK if any is present            <- do not continue grading a send that cannot go
4. Sweep the remaining dimensions in parallel         <- frequency, collisions, personalisation,
                                                         products, offer, rendering, deliverability
5. Delegate each specialist dimension to its owner    <- never re-derive their reasoning here
6. Classify every finding: stop, must-fix, accepted-cost
7. Derive the verdict from the findings, not from a score
8. State every objection with its cost and its remedy
9. Name every dimension that could not be checked
```

## Decision Rules

Binding: [../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/campaign-rules.md](../../rules/campaign-rules.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/content-rules.md](../../rules/content-rules.md),
[../../rules/deliverability-rules.md](../../rules/deliverability-rules.md).

- **BLOCK is reserved for four conditions.** A missing, broken or bypassed opt-out (N9, S7);
  suppression or consent that the send would override (S7); an audience whose consent cannot be
  evidenced; and a claim or offer term the store cannot support (N3, N7). Nothing else blocks.
- Everything else is **WARN**, stated with its cost, and the store decides. A gate that blocks on
  preference is a gate people learn to route around.
- The blast radius is shown before any approval is requested (S4), and an approval covering an
  earlier version of the campaign does not carry forward (S3).
- Never weaken consent, suppression or opt-out to let a send proceed, under any framing (S7).
- Count total contact for this audience across campaigns *and* automations, not just this send
  (F2, F3). A send that is the fourth message in a short window is a finding even when each of the
  four was individually justified.
- Read the calendar before judging the send in isolation (C1, C7). Report a detected collision and
  hand the arbitration to
  [campaign-conflict-resolver](../campaign-conflict-resolver/SKILL.md) rather than deciding it here.
- Delegate rather than duplicate (G7): rendering to
  [email-render-qa](../email-render-qa/SKILL.md), fallbacks to
  [dynamic-content-personalizer](../dynamic-content-personalizer/SKILL.md), programme condition to
  [deliverability-qa](../deliverability-qa/SKILL.md), audience definition to
  [audience-discovery](../audience-discovery/SKILL.md). This skill owns the verdict, not the
  reasoning behind each dimension.
- Check that this campaign does not duplicate one already scheduled (C3, G5).
- Confirm audience, content and window together — never one without the others (C9).
- An unverifiable dimension is reported as unchecked, never as passed (S12, G15). A verdict that
  hides which dimensions were skipped is worse than no verdict.
- Verdicts are derived from findings, not from a numeric score. No weighting scheme is fixed here,
  because a score lets a genuine defect be offset by unrelated strengths.
- The audit never sends, schedules or edits. It returns a verdict.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read the campaign, resolve the audience, read consent, calendar, products, message, programme state | `read_only` |
| ANALYZE | Run stop conditions; sweep remaining dimensions; delegate the specialist ones | `analysis` |
| PLAN | Classify findings; derive the verdict; attach cost and remedy to each objection | `recommendation` |
| PREVIEW | Present blast radius, verdict, every objection, and every unchecked dimension | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human decides whether to send, fix, or abandon | — |
| — | **Sending or scheduling** | `high_impact`, owned by the sending skill, never by this one |
| MEASURE | Whether the findings predicted what the send actually produced | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the verdict, PASS, WARN or
BLOCK; the resolved audience size; each stop condition with its state; every finding with its
dimension, cost, remedy and classification; which dimensions were delegated and what each returned;
the dimensions that could not be checked, named individually; and, where the verdict is BLOCK, the
single condition that produced it, stated first.

A WARN verdict lists what the store is accepting if it proceeds. A BLOCK verdict offers the nearest
send that would not be blocked, where one exists.

## Validation

- [ ] Audience resolved and blast radius stated before any verdict (S4)
- [ ] All four stop conditions checked explicitly, each reported as pass, fail or unchecked
- [ ] BLOCK used only for a stop condition — no other finding escalated to it
- [ ] Total contact counted across campaigns and automations, not this send alone (F2, F3)
- [ ] Calendar read and collisions reported, with arbitration delegated (C1, C7)
- [ ] Duplicate of an existing scheduled campaign ruled out (C3, G5)
- [ ] Every product referenced confirmed available, or reported unverified (G3)
- [ ] Offer terms as written matched against the offer as configured (N7)
- [ ] Opt-out present and functional (N9)
- [ ] Personalisation empty cases checked via the composed skill (P2, P12)
- [ ] Rendering checked via the composed skill, not re-derived here (G7)
- [ ] Every unchecked dimension named in the output (S12, G15)
- [ ] No consent, suppression or opt-out weakened to reach a PASS (S7)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read the campaign, audience, calendar and message | `read_only` / `analysis` | None |
| Return the verdict and its findings | `recommendation` | None |
| Fix a finding | `mutation` | Out of scope; owned by the skill that holds the artefact |
| **Send or schedule after a WARN** | `high_impact` | **Explicit**, with the accepted costs restated (S2, S4) |
| **Send after a BLOCK** | — | Not available. A stop condition is not a cost the store may accept (S7, N9) |

## Examples

**"Can we send the flash sale tonight?"**
Resolves the audience and reports the blast radius first. Stop conditions pass — consent is
evidenced, the opt-out works, the offer terms match the configured discount. The sweep finds three
things: a third of the audience is mid-way through an abandoned-cart automation and would receive
this as a third message in two days; two of the six featured products are out of stock; and the
programme's complaint rate has been climbing for three weeks, which deliverability-qa returns as a
reputation trend rather than a threshold breach. Verdict **WARN**, with the cheapest remedy named —
exclude the automation cohort and drop the two unavailable products, which resolves two findings
without touching the schedule. The complaint trend is stated as an accepted cost if the store
proceeds tonight, and as the thing to fix before the next send.

**"The campaign's ready, we just need to add the list we got from the trade show."**
Reports **BLOCK** on the first stop condition it reaches: the added contacts have no evidenced
consent record, so the send would mail people the store cannot show agreed to be mailed. States that
this is not a cost the store may accept and why (S7). Offers the nearest unblocked send — the same
campaign to the consented audience, which is most of it — and hands the question of whether the
trade show contacts can ever be mailed to consent-verification. Declines to suggest any framing that
would let the added list through.

**"Check the welcome automation before we switch it on."**
Treats an unattended automation as a higher bar than a one-off, because nobody will review each
send. Stop conditions pass. Finds that the second message's greeting has no fallback, which renders
as a blank for the share of signups whose name is not captured — small per send, permanent across
every future entrant. Finds the third message references a product line the store discontinued after
the automation was built. Verdict **WARN**, with both classified as must-fix rather than accepted
cost, on the grounds that an unattended journey repeats its defects indefinitely while a campaign
defect happens once.

## Failure Handling

| Situation | Response |
|---|---|
| The campaign configuration is unavailable | **Blocked.** There is nothing to audit; do not audit a description of the campaign |
| Audience cannot be resolved | **Blocked.** Without a blast radius no approval is meaningful (S4) |
| Consent or suppression state unavailable | **Blocked.** The one dimension that cannot be reported as unchecked and still yield a verdict (S7, S12) |
| Contact history unavailable | **Partial.** Return the verdict with frequency named as unchecked, and say what that leaves unknown (F2) |
| Calendar unavailable | **Partial.** Collisions cannot be detected; state it rather than implying none exist (C1) |
| Product availability unreadable | **Partial.** Report each referenced product as unverified and recommend confirming before send |
| Deliverability state unavailable | **Partial.** Carry deliverability-qa's own degraded result through rather than substituting a judgement |
| A composed skill returns blocked | Propagate it as an unchecked dimension with that skill's reason attached; never fill the gap with an assumption |
| Store asks for a PASS despite a stop condition | Decline, state the condition plainly, and offer the nearest send that would not be blocked (S7) |
| Send is imminent and dimensions remain unchecked | Return the verdict with the unchecked list prominent. Time pressure does not convert unchecked into passed |

Degraded outcomes set `status` and populate `unmet_requirements`.
