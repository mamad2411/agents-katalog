---
name: openmark-newsletter-comparison
description: Compose a comparison newsletter from Ahmad's OpenMark saves — A vs B vs C, side-by-side, table-driven. Use when Ahmad wants to compare tools, models, frameworks, approaches, or platforms across his saves. Trigger phrases include "compare", "X vs Y", "head to head", "which should I use", "differences between", "trade-offs between", "/newsletter-comparison". Output centers a markdown table with consistent columns, supports it with short prose blocks, ends with a clear recommendation.
metadata:
  type: composition
---

# OpenMark — Newsletter Comparison

Compare 2-5 things from Ahmad's saves. The table IS the spine. Prose only exists to add context the table can't carry.

## When to use vs other newsletter skills

| User intent | Skill |
|---|---|
| "Compare A vs B" / "X vs Y" / trade-offs | this one (comparison) |
| Single-thesis argument | openmark-newsletter-essay |
| Categorical weekly recap | openmark-newsletter-roundup |
| Punchy analytical newsletter | openmark-newsletter |

## Get the comparison set FIRST

If Ahmad didn't name the items, ASK once:

> "Which 2-5 specific things are we comparing? And what's the dimension that matters most — cost, performance, DX, lock-in, license?"

Don't pull data without (a) the items list AND (b) the dimensions. Without both, comparison drifts into recap.

## Tool sequence

For each named item:

1. `search_semantic(query="<item name>", n=8)` — what Ahmad saved about it.
2. `find_by_tag(tag="<item-name-lowercase>", n=10)` if the item has a tag.

Run these in parallel across items.

Then dedupe across all returned hits. Pick the top 2–3 anchors PER item that ground specific claims (perf numbers, pricing, license terms, DX quotes).

`WebFetch` the 2 strongest anchors per item to extract specifics. If a fetch fails, drop that anchor.

## Output format — NON-NEGOTIABLE

```
# {Punchy title — name the comparison, ≤ 9 words}

> **{One-sentence recommendation. Who wins for what.}**

{Opening paragraph: 2–3 sentences. Set the stakes — when does this
comparison matter? Who is the reader (someone shipping, evaluating,
choosing)? NO definitions of the items themselves.}

## The table

| Dimension | {Item A} | {Item B} | {Item C} |
|---|---|---|---|
| **License** | MIT | Apache-2.0 | Closed |
| **Cost** | Free | $20/mo seat | Free tier + $99/mo |
| **DX (1-5)** | 4 | 3 | 5 |
| **Lock-in** | Low | Medium | High |
| **Best at** | Speed | Flexibility | Polish |
| **Worst at** | Docs | Latency | Cost |

(Headers and dimensions are EXAMPLES. Use dimensions Ahmad named, plus
any high-signal dimensions the data supports. 4–8 rows. Every cell is
short — phrase, number, or one word.)

## How to read this

{2–4 sentences. Spell out the trade-off pattern the table reveals.
Reference specific cells by name. If two items tie on most rows, name
the one tiebreaker dimension.}

## When to pick each

### Pick **{Item A}** if {one-sentence condition}.

{1–2 sentences of context. Cite the strongest anchor: [phrase](URL).}

### Pick **{Item B}** if {one-sentence condition}.

{Same pattern.}

### Pick **{Item C}** if {one-sentence condition}.

{Same pattern.}

## The numbers (if any)

{Optional section. ONLY include if WebFetch returned concrete numbers.
Format as 2–4 sentences citing the URLs. No fabricated stats.}

## Sources cited

1. [{title}]({URL}) — {which item, what claim it grounds}
2. [{title}]({URL}) — {which item, what claim it grounds}
...

_Comparing {N} items across {M} dimensions · {K} sources cited_
```

### Formatting rules — strictly enforced

- **Single H1.** No subtitle.
- **Recommendation as blockquote** under the H1.
- **The table is mandatory.** 4–8 dimensions, 2–5 items.
- Each cell ≤ 30 chars. If a value needs more, abbreviate or split into a separate row.
- **"Pick X if" sections use `###` not `##`** — they're sub-recommendations of the recommendation block.
- **Cite URLs inline** in the "Pick" sections — `[phrase](URL)`.
- **End with `## Sources cited`.** Required for auto-export.

## Voice

Direct. Comparative. No "both are great." Every recommendation names ONE specific use case. Examples:

| Generic | Comparison voice |
|---|---|
| "Both LangChain and LlamaIndex are popular." | "LangChain wins for orchestration. LlamaIndex wins for the retrieval layer." |
| "It depends on your use case." | "If your team ships features weekly, pick A. If you optimize for cost, pick B." |
| "There are pros and cons to each." | "C has the best DX and the worst lock-in. Choose your pain." |

## What NOT to do

- Don't compare more than 5 items. Below 2 is not a comparison; above 5 is a roundup.
- Don't list "pros and cons" in prose. That's what the table is for.
- Don't hedge in the blockquote recommendation. Pick one or name the one tiebreaker.
- Don't include items Ahmad hasn't saved — the comparison must be grounded in his bookmarks.
