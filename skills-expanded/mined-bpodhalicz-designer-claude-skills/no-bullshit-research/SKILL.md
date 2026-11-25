---
name: no-bullshit-research
license: MIT. See LICENSE.md
metadata:
  author: "Bogusław Podhalicz (Hotkeys Supply)"
  version: "2.0.1"
  languages: "en, pl"
description: >
  Research with sources: every number, date, quote and vendor claim is traced to a page Claude actually opened and date-checked, or it is labeled as uncertain or dropped. Use whenever a response would contain specific numbers, statistics, prices, dates, named studies, quotes, vendor or tool capabilities, "latest in X," "current state of Y," market data, due diligence, or comparisons presented as fact — anything repeatable to a client, team, or audience. Especially in fast-moving fields (AI, models, tools, frameworks, pricing, regulation) where last year's truth is already wrong. Don't wait for the word "research": if the output could be screenshotted with the user's name on it, trigger. When in doubt, trigger.
---

# No Bullshit Research

Research and source-backed answers that hold up to a line-by-line fact-check. The whole skill exists to protect the person from the reputational cost of repeating something the AI made up.

**The one rule everything else serves:** if a statement can be repeated to a third party as fact, it must be verifiable, verified, and traceable to its source — or it must be labeled as uncertain, or dropped.

## How this skill is organized

Read this file first. It holds everything needed for a standard research answer: when to trigger, the verification protocol, the output format, and the self-audit. Load the extra files only when the situation calls for it:

- **`REFERENCE.md`** — the situational playbook (latest/recent queries, fast-moving tech, company/product claims, quotes, sources that disagree, hurry, no web access) plus the full source-quality red-flag catalog. Read it when you hit one of those situations.
- **`EXAMPLES.md`** — one full worked answer in the correct output format. Read it if you're unsure how the finished output should look.
- **`README.md`** — why the skill exists, install notes, author. Not needed to run the skill.

## The three jobs, always blended

1. **Verify before claiming.** Every factual statement is matched to a real source that was actually fetched and read — not a search snippet, not training memory.
2. **Label uncertainty.** Anything not fully verified gets an explicit confidence label with a reason. Silent uncertainty is a failure.
3. **Self-audit before delivery.** The answer is re-read for contradictions, unsourced numbers, vague dates, and banned phrases before it ships.

The point isn't pedantry. It's that anything the person repeats to a client, teammate, or audience survives scrutiny.

## When to use this skill

Use it whenever the answer would contain factual content that could be repeated to a third party and being wrong would be embarrassing: research summaries, statistics, citations, vendor comparisons, "latest in X," "what does Y think about Z," market data, due diligence, evidence-backed recommendations.

Trigger even on casual phrasing ("what do you know about X," "any data on Z," "is it true that…"). **If the output could be screenshotted and posted with the person's name on it, this skill applies.**

Be extra aggressive about triggering when:

- The person is preparing material for a client, audience, leadership, or public post.
- The topic is fast-moving (AI, frameworks, tools, pricing, regulation), where last year's truth may already be wrong.
- The output will include numbers, percentages, or specific dates.
- The person is comparing tools, vendors, or methods.
- The person quotes or paraphrases what someone said.

### Content types that always activate it

Numbers, percentages, prices, market sizes · specific dates or durations · named studies, papers, reports, surveys · direct or paraphrased quotes · claims about what a company/product/person does or said/released · factual comparisons · "best practice / industry standard / most people / the research shows" · current state of any field, tech, market, or regulation · biographical, historical, or geographical facts · evidence-based recommendations · "latest version / newest feature."

## When NOT to use it

Skip it for pure creative writing; brainstorming clearly framed as speculation; opinion explicitly requested as opinion; code generation, debugging, refactoring; math or logic derived from the person's own inputs; rephrasing, editing, or translating the person's own text; casual conversation with no factual claims.

If the answer would be no worse for being slightly wrong, the skill probably doesn't apply.

## The verification protocol

Five stages, in order. Don't skip ahead.

### Stage 1 — Plan before searching

Before any tool call, note (briefly, internally): what specific factual claims will this answer make? For each, what would a legitimate source look like (primary paper, official doc, government dataset, reputable named-author outlet)? What's the minimum number of sources to call it verified? Contested or high-stakes claims need **at least two independent sources**, not one.

### Stage 2 — Search and fetch

- Search with specific, narrow queries. Broad queries return SEO sludge.
- **Physically fetch every source you plan to cite.** Never cite from a search snippet alone — snippets are often misleading or out of date. Fetch the full page.
- A failed fetch (404, paywall, redirect to homepage, login wall) means that source is **not usable**. Don't cite it; log the failure.
- Prefer primary sources, in this order: (1) the original document — paper, dataset, filing, press release, government source; (2) the author's or organization's own site; (3) reputable secondary sources with a named author and original reporting; (4) Wikipedia — a starting point and pointer to *its* citations, not the source itself; (5) aggregators, listicles, SEO blogs — **not citable**, only a path to the primary source.

**Search again before giving up.** One failed search is not evidence of absence — it usually means the query was bad. Before marking anything ⚠️ Unverified or ❌ Dropped, run **at least two meaningfully different searches** (three for high-stakes claims): reformulate the wording; switch register (business ↔ technical, or another language); go to where the source would live (`site:developers.google.com …`, Scholar, arXiv) rather than what it would say; search the inverse claim; try the exact phrasing the source might use. Note the alternative queries in the log — it shows the person you actually looked, and lets them point you at a source they know exists.

### Stage 3 — Recency check

A source can be real, fetched, and on-topic **and still wrong because it's stale.** Before citing, check the publication date and match it to how fast the topic moves:

- **High-velocity** (AI models and tools, social platform features, crypto, framework versions, pricing, regulation in flux): prefer the **last 6 months**; anything past 12 months needs a recency check or a downgrade.
- **Medium-velocity** (most B2B SaaS features, design trends, market sizing, employment data): prefer the **last 12–24 months**.
- **Low-velocity** (foundational research, established frameworks, historical facts, definitions): date matters less; an older authoritative source can still be best.

For fast-moving topics, lead with date-bounded queries that include the **actual current year** (not the word "latest"). If only an older source exists, state its date in the answer and downgrade to ❓ Partial with the note "field has likely moved — verify against current vendor docs." For deeper handling of fast-moving tech and product claims, see `REFERENCE.md`.

### Stage 4 — Match claim → exact passage

For every claim, find the **exact passage** in the fetched source that supports it — not "this page is generally about X." If the page talks around the claim but doesn't state it, it doesn't support it: find another source or drop the claim. If the source says something slightly different, rewrite the claim to match the source — don't stretch the source to fit the answer.

### Stage 5 — Self-consistency + label

Re-read the answer as a hostile reviewer: do any two points contradict? Are the numbers internally consistent? Does any vague time word ("recently," "lately") survive? Does any statistic, name, study, or quote appear without a source? Fix before delivering.

Then label every factual claim with one of four labels:

| Label | Meaning | When |
|---|---|---|
| ✅ **Verified** | Source fetched, exact passage matches, source is legit and on-topic | Default for citable claims |
| ❓ **Partial** | Source supports only part, or is secondary/weaker, or is the only source where two are ideal, or is older than ideal | A real but limited basis |
| 🧠 **Inferred** | Not stated in any source, but follows logically from verified facts (say what it's inferred from) | Use sparingly |
| ⚠️ **Unverified** | No reliable source, sources contradict, or couldn't be checked | Use when honest — don't guess instead |

`❌ Dropped` is not a confidence label — it's used only in the log, for claims considered but removed because they couldn't be sourced.

## Output format

The goal is an answer the person can scan in ten seconds and trust in one minute — not a wall of text. Every research answer has four parts, in this order.

### 1. Confidence Snapshot (top of the answer)

A compact header so the person sees the trust level before reading a word:

```
🟢 / 🟡 / 🔴 Bottom line: [one sentence — safe to repeat as-is / repeat with the caveats below / don't repeat yet]
Confidence: ✅ N verified · ❓ N partial · 🧠 N inferred · ⚠️ N unverified
Freshness: newest source [date] · oldest cited [date] · topic velocity: high / medium / low
```

Traffic light: 🟢 all key claims verified · 🟡 solid but with caveats · 🔴 major gaps or contradictions.

### 2. Answer

The actual answer, in short scannable chunks — lead with the answer, not the methodology. Use inline citation markers `[1]`, `[2]` tied to the sources table.

To avoid clutter, **verified claims carry no inline label** (✅ is the default and is shown in the snapshot and log). Only non-verified claims get an inline chip, using emoji + one-word tag — the snapshot's legend makes them unambiguous:

> The market roughly doubled over this period. [2] ❓ *partial*
> Given both facts above, it likely also affects Z. 🧠 *inferred*
> I couldn't find a verified figure for this specific metric. ⚠️ *unverified*

### 3. Sources (compact table)

One row per source — scannable, not a paragraph each:

```
| # | Source (author / org, date) | Status | Backs |
|---|---|---|---|
| 1 | Title — Org, 2026-03 | ✅ fetched, on-topic | claim about X |
| 2 | Title — Author, 2024-09 | ❓ paywalled, abstract only | market-size claim |
```

Status is honest: fetched and on-topic, paywalled/abstract-only, no visible date, etc. If a source is paywalled and only the abstract is accessible, say so and downgrade the claim to ❓ Partial.

### 4. Verification Log

A short, honest section. **The heading uses 🔎, never ❓** — the question mark is reserved for the Partial label, and reusing it as a heading would clash.

```
## 🔎 Verification Log
✅ Verified: [claims fully cited and fetched]
❓ Partial: [weaker-evidence claims, and why]
🧠 Inferred: [reasoning, not citation — and from what]
⚠️ Unverified: [things the person might expect that I couldn't substantiate, and why]
❌ Dropped: [claims I considered but couldn't source, so removed]
🔁 Searches that failed before I found it / gave up: [alternative queries tried]
```

Only show categories that have entries — but the ⚠️ Unverified and ❌ Dropped lines are not optional; if they're empty, write "none." Their presence signals you actually looked. Keep the whole log tight; it's a receipt, not a second essay.

## Banned phrases

Forbidden unless immediately followed by a specific, cited source: "studies show / research suggests / it's well documented" · "experts say / industry leaders agree" · "recently / lately / in the past few years / just last week" · "most people / the majority of / X% of users" (any percentage without a source) · "it's known that / everyone knows" · "according to a recent report" (without naming it) · "trending / going viral" (without a source) · "industry standard / best practice is" (without sourcing the standard).

If a question naturally invites one of these, rewrite the answer around verified facts or say you can't verify the framing.

## Source red flags (short list)

Treat as **non-citable** unless they are themselves the subject of the question: AI content farms (no named author, "as an AI" leftovers, suspiciously round numbers); keyword-farm SEO pages; unsourced "Top 10" listicles; press releases treated as journalism (fine for what a company says about itself, not as independent verification); forums/Reddit/Quora (leads, not authority); stale caches when the live page differs; impersonation domains (`nytimes.co`). When a result *looks* authoritative but the URL is suspicious, check the masthead and about page before citing. Full catalog and edge cases: `REFERENCE.md`.

## When you genuinely don't know

**First — did you actually try?** Confirm you ran the "search again before giving up" rule: at least two meaningfully different queries, three for high-stakes. "I didn't find it" after one search is not "it doesn't exist."

If you've genuinely tried and come up empty, say so plainly. Good non-answers: "I couldn't find a reliable source for that number; the closest verified figure is [X] from [source], which measures a slightly different thing. I tried [A], [B], [C]." / "I can't verify [person] said that — the quote isn't on their site or published work across multiple queries." / "Sources disagree: [A] says X, [B] says Y; I don't have a basis to pick." / "This is outside what I can verify from public sources — you'd need [the company / a specialist / internal docs]."

A clean "I don't know, here's why, here's what I tried" preserves trust. A confident wrong answer destroys it. A premature "I don't know" after one weak query wastes the person's time.

## Self-audit before sending

- [ ] Every number, date, name, study, and quote is cited or labeled.
- [ ] Every cited URL was actually fetched; every cited passage actually exists on the page.
- [ ] Every date is specific — no "recently."
- [ ] Fast-moving topics: sources are fresh enough, or staleness is flagged.
- [ ] No two points contradict each other.
- [ ] Every non-verified claim carries a chip; the snapshot counts match the log.
- [ ] For every ⚠️ Unverified / ❌ Dropped item, I tried at least two different searches.
- [ ] No banned phrases survive.
- [ ] The Confidence Snapshot, Sources table, and Verification Log are all present.
- [ ] **If the person repeated this publicly and someone fact-checked it line by line, would I be embarrassed?**

The last question is the real test. If the answer is "yes, a little" — go back and fix it.

---

*No Bullshit Research v2.0.1 · MIT · Bogusław Podhalicz. Background, rationale, and install notes in `README.md`.*
