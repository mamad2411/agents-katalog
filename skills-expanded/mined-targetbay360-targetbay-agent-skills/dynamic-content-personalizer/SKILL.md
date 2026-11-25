---
name: dynamic-content-personalizer
description: Use when deciding what a message should vary per recipient beyond their first name — which verified signal each dynamic element draws on, what it falls back to when that signal is missing, how deep the variation should go before it stops paying, and which elements should be dropped rather than defaulted. Answers "how should we personalize this email?", "what merge fields can we actually use?" and "what happens when the data isn't there?". Use content-optimization when the fixed wording is the problem, and product-recommendation-strategy when the question is only which items to show.
license: MIT
metadata:
  targetbay.display_name: Dynamic Content Personalizer
  targetbay.version: "1.0.0"
  targetbay.category: content
  targetbay.requires: email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.order_intelligence, email_sms.segmentation, email_sms.template_management
  targetbay.composes: product-recommendation-strategy, audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Dynamic Content Personalizer

## Purpose

Decide which parts of a message vary per recipient, what signal each variable part is driven by,
what it resolves to when that signal is absent, and where variation should stop because the next
increment of it costs more than it returns.

The failure this skill exists to prevent: personalisation that is confidently wrong. A greeting
addressed to a blank, a replenishment reminder for a product the customer returned, a "because you
loved" line attached to something they never bought. Each is more damaging than no personalisation
at all, because it demonstrates the store is guessing while claiming to know.

The rules for what may drive personalisation exist and are binding —
[../../rules/personalization-rules.md](../../rules/personalization-rules.md), P1 to P12. This skill
is where they get applied to a specific message.

## When to Use

- A campaign or automation message needs its dynamic elements specified before it is built
- Deciding whether a proposed personalised element is supported by data that actually exists
- Designing the fallback for every variable element, and deciding which have no acceptable fallback
- Auditing an existing template whose merge fields were added without a fallback plan
- Judging whether deeper personalisation is worth its complexity for this store

## When Not to Use

- The fixed wording, offer framing or subject line is what underperforms. Use
  [content-optimization](../content-optimization/SKILL.md), which composes this skill for the
  variable parts.
- Only the choice of items matters. Use
  [product-recommendation-strategy](../product-recommendation-strategy/SKILL.md), which this skill
  composes.
- The question is who receives the message. Use
  [audience-discovery](../audience-discovery/SKILL.md) — a difference large enough to need its own
  audience is segmentation, not personalisation.
- The message is built and the concern is whether it renders. Use
  [email-render-qa](../email-render-qa/SKILL.md), which checks the empty case renders; this skill
  decides what the empty case should be.
- The question is whether a model may write the copy unattended. Use
  [ai-content-governance](../ai-content-governance/SKILL.md).
- The timing of the send is the variable. Use
  [send-time-optimization](../send-time-optimization/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Which fields the platform actually holds per contact, and their fill rate | A merge field with a low fill rate is a fallback plan, not a personalisation | Blocked |
| Purchase history per contact | The strongest signal available, and the basis for most useful variation | Partial; variation drops to segment level |
| Lifecycle stage and value band | Frames the message's premise, which is stronger personalisation than any single field | Partial |
| Product attributes for anything referenced | Stops a message describing an item incorrectly | Blocked for product-referencing elements |
| Category and price-band affinity | Relevance where no purchase has happened | Partial |
| Recency of every signal used | Stale data presented as current is the most damaging failure | Partial; staleness cannot be bounded |
| The message's structure and where variation is possible | Which elements can vary at all | Blocked |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.customer_intelligence` | Available fields and their fill rate, lifecycle stage, value band, affinity, signal recency |
| `email_sms.product_intelligence` | Attributes of any product referenced, so the message describes it correctly |
| `email_sms.order_intelligence` | Purchase history, intervals and price points behind the strongest variations |
| `email_sms.segmentation` | Sizing each fallback branch, so a fallback serving most recipients is recognised as the real message |
| `email_sms.template_management` | The message structure and which elements can vary |

## Decision Process

```
1. Establish what the message is for      <- the premise, which is the first thing to personalise
2. Inventory the fields that exist, with their fill rates   <- not the fields one wishes existed
3. Propose each variable element with the signal that drives it
4. Place each signal on the verification ladder   <- transacted, observed, inferred, absent
5. Reject anything resting on inference or on a sensitive attribute
6. Define the fallback for every survivor, and size the branch it serves
7. Drop any element whose fallback is as good as its personalised form
8. Bound staleness per signal, and say what happens past the bound
9. Hand product selection to product-recommendation-strategy
```

## Decision Rules

Binding: [../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/content-rules.md](../../rules/content-rules.md),
[../../knowledge/personalization-principles.md](../../knowledge/personalization-principles.md).

- Never personalise on data the platform cannot verify for that contact (P1, G3, G12). A field the
  model believes is typical for the vertical is not data.
- Every personalised element has a defined fallback, and the empty case is designed rather than
  discovered (P2, P12). An element with no acceptable fallback is dropped, not defaulted to
  something misleading.
- Personalisation must earn its place (P3). Where the fallback branch covers most recipients, the
  fallback *is* the message and the variation is complexity without return (G7).
- Personalise on the strongest verified signal available, and say which rung it came from (P4).
  Transacted outranks observed; observed outranks inferred; inferred is not used.
- Products referenced come from platform data through
  [product-recommendation-strategy](../product-recommendation-strategy/SKILL.md) (P5). This skill
  does not select items itself.
- Never reference behaviour the recipient would find surprising (P6), and never personalise on a
  sensitive or inferred-sensitive attribute (P7) — including anything inferred from name, location
  or product category.
- Stale data must not be presented as current (P9). Every signal carries a staleness bound and a
  defined behaviour past it.
- Depth follows data depth (P10). A store with thin history gets premise-level personalisation and
  is told why, rather than a deep scheme that mostly renders fallbacks.
- Never let one contact's data reach another's message (P11). Where a variable element is resolved
  in bulk, say how the isolation holds.
- Timing is personalisation (P8), but the send hour belongs to
  [send-time-optimization](../send-time-optimization/SKILL.md).
- The subject line and preheader are part of the personalisation scheme, not separate from it — a
  personalised subject over a generic body is a mismatch (N4).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read available fields and fill rates, history, attributes, recency, message structure | `read_only` |
| ANALYZE | Place each proposed element on the verification ladder; size each fallback branch | `analysis` |
| PLAN | The element specification: signal, rung, fallback, staleness bound, and what is dropped | `recommendation` |
| PREVIEW | Render each element's populated and empty forms, with the share of recipients each serves | `plan` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the scheme before it is built into a template | — |
| EXECUTE | Configure the dynamic elements in the template | `mutation` |
| MEASURE | Fallback rate per element after send, against the predicted branch sizes | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: each variable element with the
signal that drives it, the verification rung, the fallback, the share of recipients the fallback
serves, and the staleness bound; the elements rejected and why; the elements dropped because the
fallback was as good as the variation; a worked preview of the populated and empty message; and the
fields that were wanted but do not exist.

## Validation

- [ ] Every element traces to a field the platform holds for that contact (P1, G3)
- [ ] Every element has a defined, non-misleading fallback (P2)
- [ ] The empty case is specified for every element and shown in preview (P12)
- [ ] Fallback branch sizes stated; any element whose fallback dominates is dropped (P3, G7)
- [ ] Verification rung named per element, and nothing rests on inference (P4)
- [ ] No sensitive or inferred-sensitive attribute used (P7)
- [ ] Nothing referenced that the recipient would find surprising (P6)
- [ ] Staleness bound set per signal with defined behaviour past it (P9)
- [ ] Products sourced through product-recommendation-strategy, not chosen here (P5)
- [ ] Subject line and body personalisation agree (N4)
- [ ] Depth matched to the store's actual data depth, and the limit stated (P10)
- [ ] Fields wanted but absent are declared rather than quietly worked around (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read fields, history and message structure | `read_only` / `analysis` | None |
| Propose the personalisation scheme | `recommendation` | None |
| Preview populated and empty forms | `plan` | None |
| Configure dynamic elements in a template | `mutation` | Preview, then confirm |
| **Send using the scheme** | `high_impact` | **Explicit**, owned by the sending skill |

## Examples

**"Make the replenishment email more personal than just their first name."**
Establishes that the premise itself is the strongest available personalisation — this recipient is
approaching the end of a product they bought — and that it rests on transacted data rather than
inference. Proposes four elements: the product with its variant, the derived reorder timing, a
complementary item sourced through product-recommendation-strategy, and the greeting. Rejects a
"favourite category" line because the store's category affinity is inferred from browse rather than
purchase for most of this cohort. Sets the greeting's fallback to a neutral opening rather than a
blank, and drops a "your usual size" element after finding the size field's fill rate means the
fallback would serve most recipients — at which point the fallback is the message.

**"Can we open with 'Hi {{first_name}}, still loving your {{last_purchase}}?'"**
Reports two problems the wording hides. The last-purchase field resolves to a returned item for part
of the audience, because return status is not part of what the field reads — so the element needs
the exclusion before it needs a fallback. And the framing asserts an emotional state the store
cannot verify (P6). Recommends the same premise stated as a question about reordering rather than as
an assumption about feeling, keeps the greeting with a neutral fallback, and shows the empty case
rendered so the store can see what a missing name actually looks like.

## Failure Handling

| Situation | Response |
|---|---|
| Field inventory or fill rates unavailable | **Blocked.** A personalisation scheme built on assumed fields is the failure this skill exists to prevent (P1) |
| Message structure unavailable | **Blocked.** Which elements can vary is not knowable from a description of the message |
| Purchase history unavailable | **Partial.** Offer premise- and segment-level variation only, and state that per-contact depth is not available (P10) |
| Product attributes unavailable for a referenced item | Drop the element rather than describing the product from general knowledge (G3, P5) |
| Signal recency unreadable | **Partial.** State that staleness cannot be bounded, and restrict elements to signals where age does not change meaning (P9) |
| Fill rate low enough that the fallback dominates | Drop the element and say so. A mostly-fallback element is complexity that returns nothing (P3, G7) |
| An element has no acceptable fallback | Drop it. Never default to a value that reads as fact when it is a placeholder (P2) |
| Store insists on an element resting on inference | Decline that element, state the failure mode plainly, and offer the nearest version supported by verified data (P1) |
| Preview cannot be rendered | **Partial.** Deliver the specification with the empty cases written out, and say the visual preview was not produced |

Degraded outcomes set `status` and populate `unmet_requirements`.
