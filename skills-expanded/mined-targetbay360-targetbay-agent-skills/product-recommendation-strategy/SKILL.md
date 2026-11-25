---
name: product-recommendation-strategy
description: Use when the question is which specific items to put in front of a given customer and on what evidence — choosing what fills a product block, ranking candidates for one contact rather than for the catalogue, deciding how far down the evidence ladder a recommendation may go before it is a guess, and saying how many items are worth showing. Answers "which products should we recommend?", "what should go in this email's product block?" and "how do we pick items per customer?". Use cross-sell when the objective is breadth into a new category, upsell when it is a move to a higher tier, and aov-growth when the lever itself is not yet chosen.
license: MIT
metadata:
  targetbay.display_name: Product Recommendation Strategy
  targetbay.version: "1.0.0"
  targetbay.category: revenue
  targetbay.requires: email_sms.product_intelligence, email_sms.order_intelligence, email_sms.customer_intelligence, email_sms.segmentation, email_sms.campaign_analytics
  targetbay.risk_level: recommendation
  targetbay.execution_mode: recommend_only
  targetbay.status: foundation
---

# Product Recommendation Strategy

## Purpose

Decide which items a message puts in front of a given contact, in what order, and on the strength of
which evidence — so that every skill needing products asks the same question in the same place
rather than each inventing its own selection logic.

The failure this skill exists to prevent: a recommendation that reads as personal but rests on
nothing. Catalogue-wide bestsellers presented as "picked for you", an accessory for a product the
customer returned, or an item the store no longer sells. Each is indistinguishable from a real
recommendation until the recipient notices, and each costs more trust than the sale was worth.

This is the product counterpart to [audience-discovery](../audience-discovery/SKILL.md): it holds
the selection logic once so the skills above it stay about objectives.

## When to Use

- A campaign, automation or message needs specific items chosen for specific people
- Deciding how many products a block should carry, and in what order
- Judging whether the evidence supports a personalised recommendation or only a segment-level one
- A recommendation must be explained — "why is the store showing me this?"
- Deciding what to show when a contact has no purchase history at all

## When Not to Use

- The objective is breadth into a category the customer has not bought from. Use
  [cross-sell](../cross-sell/SKILL.md), which decides the objective and delegates item choice here.
- The objective is a move to a premium tier, larger size or subscription. Use
  [upsell](../upsell/SKILL.md).
- The lever is not yet chosen between thresholds, bundling and attachment. Use
  [aov-growth](../aov-growth/SKILL.md).
- The product is consumed on a cycle and the question is *when* to remind. Use
  [product-replenishment](../product-replenishment/SKILL.md).
- A specific item is back in stock or has dropped in price and the question is who to tell. Use
  [stock-and-price-alerts](../stock-and-price-alerts/SKILL.md).
- The question is who receives the message at all. Use
  [audience-discovery](../audience-discovery/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Catalogue with attributes, categories and price bands | The candidate set, and the basis for similarity | Blocked |
| Per-contact purchase history | The strongest evidence available, and what must be excluded | Partial; recommendations fall to segment level |
| Co-purchase relationships observed in this store | Attachment grounded in behaviour rather than assumption | Partial; attachment becomes an assertion |
| Category and browse affinity per contact | Intent where a purchase has not happened yet | Partial |
| Price band the contact actually buys in | Stops a recommendation the contact will not consider | Partial; ranking ignores affordability |
| Availability posture per product | Recommending an unavailable item wastes the placement | Partial; must be stated as unverified |
| Prior campaign response by product and category | Which recommendations have converted here before | Partial; ranking loses its feedback |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.product_intelligence` | Catalogue, attributes, categories, price bands, affinity and co-purchase relationships, availability posture |
| `email_sms.order_intelligence` | What each contact has bought, how often, and at what price point |
| `email_sms.customer_intelligence` | Lifecycle stage, value band and category affinity for the contact |
| `email_sms.segmentation` | Resolving the contact set the recommendation is being built for |
| `email_sms.campaign_analytics` | Which products and categories have converted in prior sends |

## Decision Process

```
1. Establish the recommendation's job          <- attachment, replacement, discovery, continuation
2. Build the candidate set from the catalogue  <- exclusions applied first, not last
3. Place each candidate on the evidence ladder <- strongest available evidence per contact, not per store
4. Stop at the weakest rung the job justifies  <- below it, say segment-level rather than personalised
5. Rank within the rung                        <- price band the contact buys in, then prior conversion
6. Decide how many to show                     <- derived from the placement and the evidence depth
7. Attach the reason to each item              <- if it cannot be stated, the item does not ship
8. State availability posture and what was unverifiable
```

## Decision Rules

Binding: [../../rules/global-rules.md](../../rules/global-rules.md),
[../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../knowledge/personalization-principles.md](../../knowledge/personalization-principles.md).

- Recommended products come from platform catalogue data, never from the model's own knowledge of
  what the store might sell (P5, G3). An item that cannot be resolved in the catalogue does not ship.
- Use the strongest evidence available for that contact, and say which rung it came from (P4). The
  ladder descends: bought before, co-purchased in this store, category affinity, attribute
  similarity, segment-level popularity, catalogue-wide popularity.
- Catalogue-wide popularity is the bottom rung and is never presented as personalised (P3, P9). It
  is a legitimate fallback stated as what it is.
- Every recommendation carries a reason that could be shown to the customer. An item whose reason is
  "the algorithm chose it" fails (G14).
- Exclusions are part of the candidate set, not a filter applied afterwards (A4): already owned where
  the product is not consumable, returned, discontinued, and anything the contact's consent or
  suppression state removes.
- Never assume availability or inventory depth. Where availability cannot be read, say so and let
  the composing skill decide whether to proceed (G3, S12).
- Never assume margin exists. Ranking by margin is available only when the platform supplies it;
  otherwise rank on evidence strength and observed conversion, and say which was used (G2).
- Respect the price band the contact actually buys in. A recommendation two bands above observed
  behaviour is a guess wearing a personalisation label (P4).
- The number of items is derived from the placement and the evidence, never fixed. One
  well-evidenced item outperforms six filler ones, and a block padded to fill a template is padding
  (G7, P3).
- Do not reference behaviour the customer would find surprising (P6). Browse-derived recommendations
  are presented as relevance, not as observation.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read catalogue, per-contact history, affinity, price band, availability, prior conversion | `read_only` |
| ANALYZE | Build candidates, apply exclusions, place each on the evidence ladder | `analysis` |
| PLAN | Ranked items per contact or per segment, each with its reason and evidence rung | `recommendation` |
| PREVIEW | Show the list with its rung, the exclusions applied, and what was unverifiable | `recommendation` |
| VALIDATE | Run the checks below | — |
| MEASURE | Conversion by product and by evidence rung, fed back into ranking | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) whose recommendations follow
[recommendation.schema.json](../../schemas/recommendation.schema.json): the ranked items, the
evidence rung each rests on, the reason attached to each, the exclusions applied and why, how the
item count was derived, the availability posture including anything unverified, and the contacts for
whom no recommendation above segment level was possible.

## Validation

- [ ] Every item resolves in the platform catalogue (P5, G3)
- [ ] Every item carries a stateable reason (G14)
- [ ] The evidence rung is named per item, not implied (P4)
- [ ] Segment-level and catalogue-wide fallbacks are labelled as such, never as personalised (P3, P9)
- [ ] Exclusions applied before ranking, not after (A4)
- [ ] Already-owned non-consumables, returns and discontinued items excluded
- [ ] Price band checked against the contact's observed behaviour
- [ ] Item count derived from placement and evidence, not fixed (G7)
- [ ] Availability posture stated, including where it could not be read (S12)
- [ ] Margin used only if the platform supplied it, and said so (G2)
- [ ] What could not be checked is declared (G15)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read catalogue, history and affinity | `read_only` / `analysis` | None |
| Produce the ranked recommendation set | `recommendation` | None |
| Use of the set in a message | — | Owned by the composing skill; this skill never sends or schedules |

## Examples

**"What products should go in the post-purchase email for someone who just bought a frame tent?"**
Builds candidates from co-purchase relationships observed in this store rather than from what
camping accessories generally pair with tents, which is the model's knowledge rather than the
store's data. Finds three items with real attachment evidence, one of which is out of the contact's
observed price band and drops to fourth rather than being excluded outright. Recommends three items,
not the template's six, because the fourth onwards rest only on category popularity and padding the
block would dilute the three that are evidenced. Rejected: a bestseller row labelled "picked for
you", which is the bottom rung presented as the top one.

**"Recommend products for our new subscribers who haven't bought anything."**
Reports that no rung above segment level is available for this cohort — there is no purchase
history, no co-purchase relationship and no browse affinity recorded. Recommends a category-led
selection derived from what this segment's earliest purchases have historically been, labelled
explicitly as segment-level rather than personal, and says that a first purchase is what unlocks
anything stronger. Rejected: attribute-similarity recommendations, which need a seed item that does
not exist here, and a personalised framing the evidence does not support.

## Failure Handling

| Situation | Response |
|---|---|
| Product intelligence unavailable | **Blocked.** Items cannot be invented from the model's own knowledge of the vertical (G3, P5) |
| Order intelligence unavailable | **Partial.** Recommend at segment level only, state that per-contact evidence is absent, and do not label the output personalised |
| Co-purchase relationships unavailable | **Partial.** Attachment drops off the ladder; fall to category affinity and say attachment could not be evidenced |
| Affinity and browse data unavailable | **Partial.** The ladder ends at segment level for contacts without purchase history |
| Availability posture unreadable | **Partial.** Ship the ranking with availability flagged unverified, and say the composing skill must confirm before send (S12) |
| Margin data absent | Proceed. Rank on evidence and observed conversion, and state that margin was not a factor rather than implying it was |
| Price band unresolvable for a contact | **Partial.** Rank on evidence alone for that contact and declare the omission (G15) |
| No candidate clears the exclusions | Report zero recommendations with the reason, rather than relaxing an exclusion to produce a list |
| Prior campaign analytics unavailable | **Partial.** Rank on evidence strength alone; state that no conversion feedback informed the order |

Degraded outcomes set `status` and populate `unmet_requirements`.
