---
name: content-optimization
description: Use when the message itself is the problem or is being written — subject lines and preheaders that under-deliver, body copy that does not convert, an offer stated ambiguously, or content that no longer matches the audience it goes to. Also use to decide what a message should contain and in what order — the lead, the proof, the product blocks, the single call to action. Produces content direction and testable variants, never finished creative. Answers "rewrite this subject line", "what should this email actually say?" and "why is nobody clicking?". Use campaign-optimization first if content is not yet established as the failure point.
license: MIT
metadata:
  targetbay.display_name: Content Optimization
  targetbay.version: "2.1.0"
  targetbay.category: content
  targetbay.requires: email_sms.campaign_analytics, email_sms.template_management, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.segmentation
  targetbay.composes: ab-testing, dynamic-content-personalizer
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Content Optimization

## Purpose

Improve what a message says, once it is established that what it says is the problem.

This skill produces **content direction** — the angle, the proof, the offer statement, the single call to
action — not finished creative. That boundary is deliberate: the reasoning is portable across brands, and
the final wording belongs to the people who own the brand voice.

## When to Use

- Click rate is below baseline while reach and opens are not
- A message's premise no longer matches its audience
- An offer is stated ambiguously enough to produce support tickets
- Subject lines under-deliver against their bodies
- Content direction is needed for a planned campaign or journey node
- A subject line and preheader need variants, with a basis for choosing between them
- A message's structure is in question rather than its wording — what leads, what follows, what to cut

## When Not to Use

- The failure point is not yet known. Use
  [campaign-optimization](../campaign-optimization/SKILL.md) first — most "content problems" are audience
  or offer problems.
- The audience is wrong. Use [audience-discovery](../audience-discovery/SKILL.md).
- A test needs designing. Use [ab-testing](../ab-testing/SKILL.md), which this skill composes.
- Finished creative is wanted. This package produces direction, not assets.
- The message is built and the question is whether it renders and reads for everyone. Use
  [email-render-qa](../email-render-qa/SKILL.md), which owns the built artefact; this skill stops at
  direction.
- The concern is what each variable element resolves to per recipient and what it falls back to. Use
  [dynamic-content-personalizer](../dynamic-content-personalizer/SKILL.md), which this skill
  composes.
- The incentive itself is undecided. Use [offer-strategy](../offer-strategy/SKILL.md) — this skill
  states an offer exactly, it does not choose one.
- Which products the message should feature. Use
  [product-recommendation-strategy](../product-recommendation-strategy/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The message content and its performance | The subject of the work | Blocked |
| The audience definition it went to | Content is judged against who received it | Blocked |
| Comparable messages from this store | What this store's audience responds to | Partial; lower confidence |
| The store's voice and terminology | Recommendations must sound like the store | Partial; keep direction structural |
| Product and offer facts | Claims must be supportable | Blocked for claims |
| Prior content test results | Avoids re-testing settled questions | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.campaign_analytics` | Message performance and comparisons |
| `email_sms.template_management` | Existing content and blocks; creating variants after approval |
| `email_sms.customer_intelligence` | Who the audience is and what they respond to |
| `email_sms.product_intelligence` | Product facts, stock, what can be claimed |
| `email_sms.segmentation` | The audience the content is judged against |

## Decision Process

```
1. Read the content against its audience   ← does the premise even apply to them?
2. Check the funnel position               ← which stage is the content responsible for?
3. Check the fundamentals                  ← one CTA, first-screen message, images-off, accessibility
4. Check the claims                        ← is every assertion supportable?
5. Check the offer statement               ← amount, applicability, exclusions, expiry, redemption
6. Check the architecture                  ← lead, proof, product blocks, CTA: is anything earning its place?
7. Identify the single largest weakness
8. Produce direction and a testable variant, with the metric it will be judged on
```

Subject line and preheader are worked as one unit, never separately:

```
a. State what the message is for           ← the variant has to be a hypothesis about that, not about tone
b. Generate variants across distinct angles ← clarity, specificity, curiosity, urgency, personal relevance
c. Reject any variant the body cannot honour
d. Name the downstream metric each variant is judged on   ← revenue or conversion, never opens alone
e. Hand the test design to ab-testing
```

## Decision Rules

Binding: [../../rules/content-rules.md](../../rules/content-rules.md),
[../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../knowledge/email-principles.md](../../knowledge/email-principles.md),
[../../knowledge/sms-principles.md](../../knowledge/sms-principles.md).

- Content is judged against its audience, never in isolation (N1). A message with the wrong premise cannot
  be fixed by better wording.
- One primary call to action (N2).
- No claim the store cannot support — no invented statistics, scarcity or deadlines (N3).
- Subject line and body must agree (N4).
- Lead with the reason the message exists (N5).
- Write for the channel; never port email copy into SMS (N6).
- Offers stated exactly: amount, applicability, exclusions, expiry, redemption (N7).
- Accessibility is a requirement: alt text, contrast, descriptive links, works with images off (N8).
- Follow the store's voice where one exists; do not import generic marketing register (N10).
- Personalised elements need an empty-state that reads correctly (P2, P12).
- Mark judgement calls as testable rather than presenting them as settled (N12).
- Change one thing at a time if the change is going to be tested.
- **Subject lines are never optimised on open rate alone** (G1). Open rate compares two subject lines
  inside a controlled test; it is not the outcome. Every variant names the downstream metric —
  revenue, or conversion where revenue is too sparse — and the guard metric that would make a win
  false ([../../knowledge/email-principles.md](../../knowledge/email-principles.md)).
- Subject line and preheader are one unit. A preheader left to default to the message's first body
  text is a wasted line, and a preheader that repeats the subject is the same line twice.
- A variant the body cannot honour is rejected before it is tested, not after it wins (N3, N4).
  Curiosity that the message does not resolve is the fastest route to a complaint.
- Message architecture is derived from the objective, not from the template's available blocks. Every
  block justifies its place, and a block added to fill the layout is padding (G7). Cutting is a
  legitimate recommendation.
- The reason the message exists goes above the first screen (N5), and the single call to action must
  be reachable there.
- Variable elements are specified through
  [dynamic-content-personalizer](../dynamic-content-personalizer/SKILL.md), which owns the signal,
  the fallback and the empty case (P2, P12). Do not design them here.
- Rendering, contrast and alternative text are checked on the built message by
  [email-render-qa](../email-render-qa/SKILL.md). This skill states the accessibility requirement
  (N8); it does not verify it against markup it has not seen (G7).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read content, performance, audience, comparables, product facts | `read_only` |
| ANALYZE | Check premise, funnel position, fundamentals, claims, offer statement | `analysis` |
| PLAN | Content direction and a testable variant | `recommendation` |
| PREVIEW | Present the direction with the reasoning and the evidence | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the direction and the variant | — |
| EXECUTE | Create the variant template | `mutation` |
| — | **Sending it** | `high_impact`, separate approval |
| MEASURE | Via [ab-testing](../ab-testing/SKILL.md) where volume allows | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the weakness identified with its
evidence; content direction — angle, proof, offer statement, single call to action; the empty-state
behaviour for every personalised element; an accessibility check; what should be tested versus what should
simply be fixed; and the claims that need verification before sending.

## Validation

- [ ] Content judged against its actual audience (N1)
- [ ] One primary call to action (N2)
- [ ] Every claim supportable from product or store data (N3)
- [ ] Subject line and body agree (N4)
- [ ] Channel-appropriate — not ported between email and SMS (N6)
- [ ] Offer stated exactly (N7)
- [ ] Accessibility checked: alt text, contrast, links, images-off (N8)
- [ ] Empty state defined for every personalised element (P2)
- [ ] Judgement calls marked testable (N12)
- [ ] Store voice respected where one exists (N10)
- [ ] Subject line and preheader treated as one unit, both specified
- [ ] Every subject variant names its downstream metric and its guard metric — never opens alone (G1)
- [ ] No variant retained that the body cannot honour (N3, N4)
- [ ] Every content block justified against the objective; padding cut rather than reordered (G7)
- [ ] Personalised elements handed to dynamic-content-personalizer, not designed here (P2)
- [ ] Rendering verification handed to email-render-qa rather than asserted (N8, G7)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce content direction | `recommendation` | None |
| Create a variant template | `mutation` | Preview, then confirm |
| **Send anything using it** | `high_impact` | **Explicit** |

## Examples

**"Rewrite this subject line, it's underperforming."**
Opens are at baseline; clicks are not. The subject line is doing its job. The body opens with brand
narrative and puts the reason for the message below the first screen. Recommends restructuring the body
lead (N5) and explicitly not changing the subject line — with the evidence for why.

**"Give us some subject line options for the restock email."**
Works the subject and preheader as one unit and starts from what the message is for — telling people
who asked about a specific item that it is available — which makes specificity the strongest angle
rather than curiosity. Produces four variants across distinct hypotheses, not four rewordings of
one: the item named, the scarcity stated as fact where the stock level supports it, the personal
trigger referenced, and a neutral control. Rejects a fifth that implied a deadline the store has not
set (N3). Names revenue per recipient as the metric and unsubscribe rate as the guard, on the
grounds that the highest-opening variant here is likely to be the vaguest one. Hands the sizing and
duration to ab-testing, which reports whether this send's volume can resolve four variants at all.

**"This promotion generated support tickets."**
The offer statement omits exclusions and the expiry is stated only in the image, which fails with images
off (N7, N8). Recommends an exact offer statement in text, and flags that the underlying policy needs
confirming before the next send.

## Failure Handling

| Situation | Response |
|---|---|
| Content unreadable through the capabilities | **Blocked** |
| No comparable messages | **Partial.** Work from fundamentals, lower confidence, mark choices testable |
| Store voice unknown | Keep direction structural and flag that wording needs a brand owner |
| A claim cannot be verified | Remove it from the direction and say why (N3) |
| Audience mismatch is the real problem | Report that content changes will not fix it, and hand to [audience-discovery](../audience-discovery/SKILL.md) |
| Volume too low to test the change | Recommend fixing the objective faults outright and testing nothing |
| Revenue attribution unavailable for variant judgement | **Partial.** Fall back to conversion, say why, and state that opens remain a comparison instrument rather than a criterion (G1) |
| The built message is not available, only its copy | Deliver direction and say rendering was not verified; route the built artefact to email-render-qa (G15) |
| Personalisation scheme not yet decided | Specify where variation belongs and hand it on rather than inventing fields (P1) |

Degraded outcomes set `status` and populate `unmet_requirements`.
