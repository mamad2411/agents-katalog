---
name: playbook-ai-specificity
description: Writes the one sentence that makes a generic offer feel written for this one company. Produces the tail of "I think we can help you ___". Triggers on "specificity line", "make it feel specific to them", "the specifically sentence", "why would they think this is for them", "personalize the offer not the intro". Outputs one lead-level merge field, blank when the company does not fit.
---

# Playbook: AI Specificity Line

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the offer is good but the email reads like it was sent to 5,000 people, and you need one
sentence that names what the client would actually do for **this** company.

**Do not use when:** you want a first line about a person or an event. **Those playbooks personalize
the opener. This one personalizes the offer** — which is a different and usually more durable move.

**One-line output:** `specificity_line = "know the landed cost of every pool float before you price it"`

## 1. Trigger and scope

This produces the tail of one fixed sentence:

> I think we can help you **{{specificity_line}}**.

**The whole job is one move: take the client's generic capability and say it back in the prospect's
own nouns.**

- A bookkeeping firm does not write "we help with margin reporting". It writes **"know what each pool
  noodle costs to make before you price the next run"**.
- A list-building service does not write "we build B2B lists". It writes **"build a list of every
  pool contractor in Texas with the owner's cell number"**.

Same offer, different words, and the prospect reads it as written for them.

**Two things this is not.** It is not a first line — it never mentions the person, their job, or
anything they did. And it is not a claim about the company's problems — it never says they are
struggling or missing something. **It says what the work would be.**

⚠️ **The frame lives in the campaign copy, not inside the variable.** Real campaigns have put the
frame inside the merge field, and then every lead carries the same eight opening words inside a
custom field — which is both a repetition problem and a spintax problem.

## 2. Output contract

### Inputs required per row

| Field | Type | Required? |
|---|---|---|
| `domain` (bare, lowercase) | string | yes |
| `company_name` | string | yes |
| `company_description` | string | **yes — this is the whole input** |
| `primary_offerings`, `revenue_streams` | string | no, they sharpen the anchor |
| **`client_offer_block`** | text block, **per client, not per row** | yes, locked once per client |

**The client offer block is the part people forget.** It is a fixed list of what the client actually
does, written as short capability lines. **The model is only allowed to promise something on that
list.**

### Output fields

| Field | Type | Example | Null? |
|---|---|---|---|
| `specificity_line` | 6-14 words, ≤90 chars | `know the landed cost of every pool float before you price it` | **yes, blank is a real answer** |
| `specificity_anchor` | QA only | `pool float` | yes |
| `specificity_offer_item` | QA only | `inventory and cost of goods sold tracking per product` | yes |
| `grade_line` | QA only | `4.9` | yes |

The anchor and offer item are **never sent to anyone.** They exist so the guard can check the line
mechanically, and so an operator can see *why* a line came out the way it did.

### Coverage expectation

**8/10 usable**, and 8/10 again on a re-run of the shipped script on the same domains.

Of the 2 failures: one was a grammar break **the guard could not see**, and one was a company with no
description in any source.

⚠️ **On the re-run the grammar break was gone and a different row went awkward instead.** That is the
non-determinism in this playbook, and the rule that follows from it: **judge a batch, never a row.**

Expect **10 to 20% blanks** on a normal ecommerce or SMB list, higher on lists full of tiny companies
with thin websites.

### Copy-fit rules

- Slots into `I think we can help you {{specificity_line}}.`
- **Starts with a plain verb** (track, see, know, build, cut), lowercase, no trailing period.
- **Never contains the company name, the words "help you", or the word "specifically".** All three
  are already in the frame.
- 6 to 14 words, one idea, no em dashes.
- **Never promises sales, growth, demand, or customers** unless the offer block says the client does
  that.

### Reading level is a gate, not an aspiration

Enforce **Flesch-Kincaid grade 7 on the generated tail.** Above it, one simplify rewrite; still
above, **the row blanks.** Measured: 8 filled tails scored 2.5 to 5.9, none needed the rewrite.

⚠️ **Gate the tail, not the rendered sentence — and this is measured, not assumed.**

The frame `Specifically, I think we can help you.` **scores 5.7 on its own** ("Specifically" is five
syllables inside a seven-word stem). Once any 6-to-14-word tail is added, the full sentence lands at
**7.0 to 9.8 no matter how plain the tail is.** A tail of grade 2.5 still renders at 7.0.

**Gating the render would blank every row for a property of house copy, not of the data.**

The clean fix is a copy change, not a data change: **dropping the word "Specifically" takes the worst
sampled render from grade 9.1 to 6.3**, under the bar, with **no change to the generated tail.** Do
that, and keep gating the tail anyway — it is the half you generate.

⚠️ **If you change the frame, change it in the copy and in the prompt's context sentence together,
and re-grade on the same domains.** The graded verdict was measured against the longer frame.

### Downstream gate

**The default posture: a row missing this campaign's personalization signal should generally not be
uploaded to this campaign at all.** Build the list so the line lands, and route the abstains to a
campaign whose copy does not need it. **That is also what lets you measure whether the line earns its
keep.**

Where a genuinely optional clause abstains on a small share of rows, **pre-render the whole sentence**
— frame plus value plus trailing period and space — into **one** field, so the body carries a single
merge field that renders as nothing when empty.

⛔ **Spintax is banned as the blank-handling mechanism.** It picks a variant at random and cannot
branch on whether a variable is empty.

**A blank is also a soft targeting signal: if more than 30% of a segment comes back blank, the list
is wrong for this campaign, not the prompt.**

## 3. Source chain (cost-tagged)

**The signal is not fetched, it is written.** The chain is only about getting one honest paragraph
describing what the company sells.

| # | Source | Cost | Result |
|---|---|---|---|
| 1 | An internal company database's derived description | FREE | **9/10 domains present, and rich enough to write from in 8 of those 9** |
| 2 | Plain homepage fetch, browser UA, meta description + first 1,500 chars | FREE | **1/4 on ecommerce domains.** Measured: one returned **0 bytes**, one 16 bytes, one **1 byte**, one refused the connection |
| 3 | Rendering proxy | METERED, **capped** | verified: **7,805 characters of clean text in 8.3s** after the plain fetch returned 0. Only when step 2 came back under ~400 characters **and the run's explicit row cap has budget** |

Step 2's numbers are worth internalizing: **modern ecommerce sites frequently return nothing to a
plain fetch.** If your evidence source is "just fetch the homepage", you will silently write from
nothing on exactly the list types this playbook is best at.

## 4. Verification

**VERDICT: PASS 8/10**, twice, on the same domains.

## 5. Clay implementation

- **`clay-table.md`** — the column build with the deterministic guard.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt

**In your own scripts:** a nano-class model at **minimal reasoning effort**. Measured ~1,848 input
and 59 output tokens per row. Params: `max_completion_tokens=400`, no `temperature`, flex tier for
batch.

**Inside Clay: `gpt-4o-mini`.** ⚠️ A Clay column set to a reasoning model **with the reasoning level
unset** is the 19x-more-expensive, returns-blanks configuration — measured at **1,088 to 2,000
reasoning tokens per row and 2 of 5 rows returning empty.**

**The prompt has three parts.** Part 1 is byte-identical for every client and must stay first. Part 2
is the client offer block, locked once per client. Part 3 is few-shot examples, which are
**client-specific and must be rebuilt for every client.**

### Part 1 — static prefix (never edited per client)

```text
You write one short merge field that gets dropped into the middle of a cold email sentence.

The sentence it goes into is exactly this, and you are writing only the {{VAR}} part:
"Specifically, I think we can help you {{VAR}}."

STEP 1, FIT CHECK. Read the company data. Decide if the client offer below really applies
to how THIS company makes money. Say yes for any company that makes or sells a product, or
sells a service, that the offer list can plainly serve. Say no for schools, city and
government bodies, hospitals, churches, charities, and any company whose business you
cannot tell from the data. Write "yes" or "no" in "fits". If no, return empty strings for
the rest and stop.

STEP 2, ANCHOR. Pick one anchor: a word or short phrase for the thing this company makes,
sells, or counts. Copy it from the company data word for word. It must be a real thing,
like "pool float", "washable rug", "hard cooler", "pool contractor". It cannot be a
business word like "product", "margin", "channel", "SKU", "revenue", or "customer".

STEP 3, OFFER ITEM. Pick the ONE line from the client offer list below that fits this
company best, using evidence in the company data, not the first item on the list. Copy it
word for word into "offer_item". You may not write anything the offer list does not say.

STEP 4, LINE. Write the merge field. It must contain the anchor, and it must say what the
offer item does, in plain words, for this company's anchor. Do not copy the offer item
wording into the line. Say it the way this company would say it.

Rules:
1. Write at a 5th-grade reading level. Use short, common words.
2. Start with a plain verb, like "track", "see", "know", "build", "cut". Lowercase first
   word. No comma at the start. No period at the end. Never write the words "help you"
   or "specifically".
3. Never write the company's name. The email already says it.
4. Never use an em dash or an en dash. Use a comma, or "and", "so", or "because".
5. Never state a fact that is not in the company data. Do not guess what they probably do.
6. Between 6 and 14 words. One idea only.
7. Never promise sales, growth, demand, traffic, or customers unless the offer list says
   the client does that. You describe the work, not the result of their business.
8. Never write the words "channel", "platform", or "across". If the company data names a
   real place they sell, like dealers, gift shops, Amazon, or their own site, name that
   place instead. If it names none, leave the place out of the line.
9. Banned phrases, because they fit any company: "product margins", "gross margin",
   "your business", "your products", "boost margins", "improve efficiency", "grow faster",
   "grow sales", "more sales", "drive demand", "increase sales". If your line needs one of
   these, your anchor was too vague. Go back to step 2.
10. If step 1 said no, or you cannot find a real anchor in the data, return empty strings.
   Never write "N/A", "unknown", "none", or a placeholder in brackets.
11. Empty is only for "fits": "no", or data too vague to name a real thing. If "fits" is
   "yes" you must write an anchor and a line. Low confidence is fine, write it anyway.
   Marketing fluff in the data is normal. One real product word is enough to work with.

Return JSON only, no markdown fence:
{"fits": "yes|no", "anchor": "<words copied from the company data, or empty>", "offer_item": "<one line copied from the offer list, or empty>", "line": "<merge field, or empty>", "confidence": "high|low"}
```

Rule 9 is the one that does the most work. **"If your line needs one of these, your anchor was too
vague. Go back to step 2."** A banned-phrase list alone just moves the fluff around; telling the
model *why* it reached for the phrase sends it back to the real fix.

### Part 2 — the client offer block (fill once per client, then lock)

```text
CLIENT OFFER (the company sending this email):
Name: {one line, what kind of company they are, never the brand name}
Sells to: {who they serve and roughly what size}
What they actually do:
- {capability 1, concrete, the words a customer would use}
- {capability 2}
- {capability 3}
- {capability 4}
- {capability 5}
What they do NOT do: {the four or five nearby things people assume, listed plainly}
```

Rules for this block, learned the hard way:

- **Five to seven capability lines**, each a thing a customer would recognize, **not a category.**
- **The "do NOT do" line is load-bearing.** Without it the model borrows adjacent promises.
- **The capability lines are copied verbatim into `offer_item`, so they double as the guard's
  whitelist.** Write them as short, quotable phrases.

Worked example:

```text
CLIENT OFFER (the company sending this email):
Name: a US outsourced bookkeeping and fractional CFO firm
Sells to: consumer product and ecommerce brands doing $2M to $50M a year
What they actually do:
- monthly close and clean books in QuickBooks or Xero
- inventory and cost of goods sold tracking per product (per SKU landed cost)
- margin reporting by product, by channel, and by sales platform
- cash flow forecasting ahead of inventory buys
- sales tax filing across states
- getting books ready for a lender, a bank line, or an investor
What they do NOT do: raise money, run ads, build software, fix supply chain, hire staff
```

### Part 3 — few-shot examples (client-specific, faux prior turns, 8 to 10 pairs)

Alternating `user` and `assistant` messages, **never a bulleted list inside the system prompt.**

**Include at least two abstains:** one obvious non-fit (a school district, a city department) and one
company whose description is pure fluff with no product word. **Without abstain examples the model
learns that every row deserves a line.**

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Every lead's email opens with the same eight words in a custom field | The frame was put inside the variable | **The frame lives in the copy.** Only the tail is generated |
| Lines are generic ("improve efficiency", "your products") | The anchor was a business word, not a real thing | Rule 9 sends the model back to step 2. **The banned list alone is not enough** |
| The line promises growth the client cannot deliver | The offer block is missing its "do NOT do" line | Add it. The model borrows adjacent promises without it |
| The line copies the offer list wording | Step 4 was skipped | The line must say the offer **in this company's nouns** |
| Every row blanks on a reading-level gate | You gated the **rendered sentence**, not the tail. The frame alone scores 5.7 | **Gate the tail.** Consider shortening the frame |
| The homepage fetch returns nothing on ecommerce sites | **Measured: 0 bytes, 16 bytes, 1 byte, connection refused** on four real brands | The rendering proxy, capped — or accept the abstain |
| Two runs give different lines for the same row | Real non-determinism, measured | **Judge a batch, never a row** |
| Over 30% blanks in a segment | **The list is wrong for this campaign**, not the prompt | Re-target, or route those rows elsewhere |
| The Clay column costs 19x the estimate | A reasoning model with the level unset | Use a mini-class model in Clay |
| `Specifically, I think we can help you .` | An empty variable inside a fixed frame | Route abstains out, or pre-render the whole sentence into one field |

### Hard rules

- **The model may only promise something on the client offer list.**
- **The frame never lives inside the variable.**
- **Gate the tail's reading level, not the rendered sentence's.**
- **Judge a batch, never a row.**
- **Spintax is never the blank-handling mechanism.**
