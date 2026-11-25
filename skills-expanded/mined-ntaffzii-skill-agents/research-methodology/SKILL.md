---
name: research-methodology
description: Use this skill as a pre-search discipline before running daily-news-report, github-skill-research, project-discovery, or any research task with multiple sources — frame the question, decide source-quality tiers, track what was checked vs. skipped, and separate "one source claims this" from "multiple independent sources agree." Trigger on "research this properly", "systematic search", "อยากได้ข้อมูลที่ครบจริง", "don't just take the first result", or automatically whenever a research skill is about to start searching. Pairs with claim-citation-check as the finalization-side check; this is the search-side discipline.
---

# Research Methodology

## Overview

Ad hoc research — search, read the first few plausible results, summarize — is fast but has a specific, recurring failure mode: it stops as soon as something *sounds* right, not when the question is actually answered, and it can't tell "three sources agree" from "three sources repeating the same original claim" (an echo chamber, not corroboration). This skill is the discipline layer that runs *before* searching — [claim-citation-check](../claim-citation-check/SKILL.md) is the equivalent check that runs *after*, on the draft. Together they bracket a research task; this skill alone does not verify anything, it structures how the searching happens.

## When to use

- ก่อนเริ่มค้นข้อมูลสำหรับ research report, news brief, หรือ skill/project comparison
- The question has room for real disagreement between sources, or the topic is unfamiliar enough that "what counts as a good source" isn't obvious
- Before `daily-news-report`, `github-skill-research`, or `project-discovery` starts synthesizing — run this first, not as an afterthought

## When NOT to use

- A quick factual lookup with one obvious, uncontested source (a library's version number, a function's signature) — the overhead isn't worth it
- The task is synthesis/writing from sources already gathered — that's `markdown-report`'s job; this skill is specifically about the searching phase

## Core knowledge

**1. Frame the question before searching.** A vague question ("tell me about X") produces a vague, first-plausible-result search. Narrow it to something a search can actually resolve ("what does X's official docs say the default timeout is, as of the current major version") before running the first query.

**2. Decide source-quality tiers up front, not after finding something.**

| Tier | Examples | Weight |
|---|---|---|
| Primary / official | Vendor docs, source code, the standard's own spec, a repo's own README | Highest — treat as ground truth unless contradicted by newer official source |
| Maintained secondary | Actively-updated community docs, a maintainer's own blog post, a well-cited technical writeup | Medium — good corroboration, not a substitute for checking primary when it matters |
| Unverified / aggregator | Random blog posts, forum answers, SEO content, an AI-generated summary of the topic | Lowest — fine for orientation, never the sole basis for a specific factual claim |

Decide the tier *before* reading, so a low-tier source that happens to say something convenient doesn't get treated as more authoritative than it is.

**3. Track what was checked and what was skipped — explicitly, not just in your head.** If a search returns 10 results and only the first 3 got read, say so ("checked the top 3 official-docs hits; did not check community forum threads") rather than presenting the summary as if the full result set was considered. This is the single most commonly skipped step in ad hoc research, because it feels like unnecessary overhead — it isn't; it's what lets someone else (or you, later) know where the coverage gap is.

**4. Distinguish corroboration from repetition.** Before counting "multiple sources say X" as a stronger signal, check whether those sources are actually independent or whether they're all citing (or silently copying) the same original claim. A claim traced back to one primary source repeated by five blogs is one data point, not five.

**5. State confidence explicitly in the synthesis**, not just the claim itself: "confirmed against official docs" reads very differently from "widely repeated across blogs, original source not found" — both are worth reporting, but not with the same weight.

## Common mistakes

1. Stopping the search the moment something plausible turns up, instead of checking whether it's actually the best available source.
2. Treating "I found several sources agreeing" as strong corroboration without checking whether they're independent or all downstream of the same original claim.
3. Not recording which parts of a broad question were actually researched vs. skipped for time — leaves a false impression of completeness.
4. Skipping primary sources entirely in favor of secondary summaries because they're faster to read, even when the specific fact matters enough to check the original.
5. Applying this much rigor to a trivial lookup — over-applying process is its own failure mode; match the discipline to the stakes of the question.

## Known limitations

- This is a process discipline, not a fact-checker — following it well over bad sources still produces a wrong conclusion. Pair with [claim-citation-check](../claim-citation-check/SKILL.md) on the finished draft for the verification half.
- Source-quality tiers above are a general starting heuristic; some domains have their own established hierarchy (e.g. peer-reviewed journals vs. preprints in academic contexts) that should override the generic table when it applies.
