---
name: playbook-creative-ideas
description: The 3-bullet creative ideas email. Produces three per-company bullets that each sit in a slot the operator defined up front, so the model fills in the company detail and never invents a new idea. Triggers on "creative ideas campaign", "three ideas email", "I had a few ideas for you", "3 bullets", "use cases for their business", "what could they build with us". Outputs creative_idea_1, creative_idea_2, creative_idea_3 plus a rendered bullet block.
---

# Playbook: 3-Bullet Creative Ideas

> Best practice, not law. Override when the campaign calls for it; note the practice once and proceed.

**Use when** the premise is "I looked at your business and had three ideas."

**Not when** one personalized sentence tops an otherwise fixed email (`playbook-ai-specificity`), or
the hook is an event.

**Output:** `creative_idea_1 = "a production scheduler that plans injection molding runs against cleanroom capacity"`

## 1. Slot discipline is the whole idea

**The operator names what bullets 1, 2 and 3 are about. Those slots stay fixed for every lead, and
the model only fills a slot with a detail true of that company.** It never picks a subject, never
adds a fourth, and never writes an idea the seller cannot deliver.

The measurement that settles this:

| Approach | Usable |
|---|---|
| Free-form "have three ideas about this company" | **2/5** |
| Slot-defined, operator-named subjects | **21/23 (91%)** |

That is the entire playbook. Everything else is plumbing.

### The operator interview, before the prompt exists

1. **What is bullet 1 about?** Name the one thing the seller builds, sells or runs that goes in slot
   1 — **in the seller's own words.**
2. What is bullet 2 about?
3. What is bullet 3 about?
4. **For each slot, what specific detail about the prospect has to appear?**
5. **What must never appear?** Competitors, dollar figures, headcounts, named customers, anything the
   seller does not actually do.
6. **Hand-write the examples.** See the gate below.

⚠️ **If the operator cannot name three slots, this is the wrong playbook for the campaign.** Do not
fill the gap yourself. **An idea the operator did not ask for is an idea the seller cannot deliver on
the call.**

### ⛔ HARD GATE: the operator hand-writes 3 complete bullet sets for 3 real companies before any model call

**AI never drafts the exemplars it is graded against.**

If the model writes the examples, the examples encode the model's instincts rather than the seller's
offer, and every downstream grading round is measuring the model against itself. This is the same
contamination failure that forced a verdict to be withdrawn in `playbook-pricing-page` — a few-shot
block that contains the answers is not a prompt, it is an answer key.

## 2. Output contract

`creative_idea_1/2/3` (140 chars each) + `evidence_1/2/3` + `creative_ideas_block`.

**Abstain is `""`.** Never a sentinel string, never `null`.

⚠️ **Any empty bullet excludes the row** into a separate non-ideas campaign, because a sequencer
cannot pin a lead to a specific sequence variant. A 3-bullet email with 2 bullets is not a degraded
version of this campaign — it is a different email.

**Namespace the custom fields per client** (`creative_idea_1_<client>`). The JSON keys stay unchanged;
the suffix is on the pushed field. Near-duplicate custom-field names coexist silently on the same
lead record, and that is a very quiet way to send last client's bullets.

## 3. Source chain

**Only the evidence text is sourced.** Order: an internal company description, then a **free**
company-enrichment source, then client-owned tables, then a company-search API, then a rendering
proxy.

**A row still thin after all of that abstains.**

⚠️ **Gate each rung on the evidence being SHORT (`length < 200`), not on it being empty.** A
two-sentence boilerplate description is technically non-empty and produces three generic bullets that
read like a mail merge. Emptiness is the wrong test.

## 4. Verification

**VERDICT: PASS 5/6 (83%)** on the script path, **plus 27/32 (84%) grading real production rows
across seven live campaigns.**

The second number is the more useful one: it is out-of-sample, at real volume, across different
sellers.

⚠️ **Script path only.** Run the Clay acceptance check in `clay-table.md` before trusting a Clay
build.

Re-test if the usable rate drops under 60% on 20 rows, or evidence coverage drops under 80%.

## 5. Clay implementation

- **`clay-table.md`** — 14 columns, plus an 8-point acceptance check.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt

**Outside Clay: a nano-class model at minimal reasoning effort.** Measured at 1,195 input and 148
output tokens per row: **$0.12 per 1,000 rows against $0.27 for a mini-class model — nano wins by
2.2x.** Params: `max_completion_tokens=1200`, no `temperature`, JSON response format, flex tier for
batch.

**Inside Clay: `gpt-4o-mini`.** This is the opposite of the outside-Clay choice and it is deliberate.

⚠️ **A Clay AI column set to a nano-class model with reasoning unset is the worst of both worlds:** it
burns thousands of hidden reasoning tokens per row at standard pricing, runs roughly **19x more
expensive than mini**, and **frequently returns blank content** because the reasoning eats the token
budget. Clay has no flex or batch tier to soften that.

So build on mini, **write the model name in the column description**, and budget **$0.27/1k** for the
Clay path rather than $0.12. Switch only if you have opened the column and **confirmed** you can set
reasoning to its lowest value — then record the accepted value so the whole team stops paying mini
prices.

### Prompt shape

- **System block:** the seller's offer, the three named slots, the must-never-appear list, and the
  output contract.
- **Few-shot:** the operator's hand-written sets as faux prior turns.
- **Per-row, last:** company name, domain, and the evidence text.
- **Output:** `{creative_idea_1..3, evidence_1..3, confidence}`.

Rules that carry the quality: 8 to 22 words per bullet; no em or en dash; no trailing period; no
leading capital; **each bullet must name a detail from the evidence**; **an empty bullet is better
than a generic one**; never a competitor, a dollar figure, a headcount, or a named customer.

### The verifier is free, and it is in the same response

**`evidence_N` must appear as a real substring of the input evidence, normalized on both sides.**

That is the whole verification. No second model call: the model is asked to quote what it used, and
you assert the quote is real. A bullet whose evidence does not appear in the input was invented, and
it is blanked.

**Truncation guard:** `finish_reason=length` means retry, never abstain.

## 7. Edge cases and hard rules

| Symptom | Cause | Fix |
|---|---|---|
| The bullets are generic and interchangeable | Free-form ideation instead of fixed slots | **2/5 vs 21/23.** Name the slots |
| The bullets propose something the seller cannot build | The model picked the subject | Slots are the operator's, always |
| The exemplars sound like the model, not the seller | AI drafted the examples | **The hard gate.** Hand-write 3 sets on 3 real companies first |
| Every bullet is filled even on thin companies | The evidence rung was gated on emptiness | Gate on `length < 200` |
| Blank rate above 30% | Wrong evidence source for this client | Change the source, not the prompt |
| Blank rate under 5% | The prompt was loosened; models fill thin rows rather than abstain | **Read the thinnest 3 rows by hand** |
| A 3-bullet email arrives with 2 bullets | An empty bullet was allowed through | **Any empty bullet excludes the row** into the non-ideas campaign |
| Last client's bullets appear | Custom field names collided | **Namespace per client.** Near-duplicates coexist silently |
| The Clay column costs 19x the estimate | A reasoning model with reasoning unset | Use mini in Clay, or confirm you can set the level |
| Bullets contain an em dash or a trailing period | Lint not applied to rendered output | Lint the rendered block, not the raw fields |
| `a injection molding line` | Article agreement | Include an `a [aeiou]` check in the lint |

### Hard rules

- **Bullets are never spun, and the model never picks what a bullet is about.**
- **The operator hand-writes the exemplars first.**
- **Any empty bullet excludes the row.**
- **Namespace the custom fields per client.**
- **Assert the evidence substring on every non-empty bullet.**
