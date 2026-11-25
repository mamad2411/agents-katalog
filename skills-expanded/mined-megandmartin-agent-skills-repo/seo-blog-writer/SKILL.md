---
name: seo-blog-writer
description: Takes a keyword or content brief through search-intent analysis, an H2/H3 outline, and a full draft with E-E-A-T signals (first-hand experience, named sources), plus a meta title/description pair — no keyword stuffing, ever. Use when the user asks to "write a blog post", "SEO article", "rank for [keyword]", "draft from this content brief", or "outline a post". Don't use for landing/sales page copy — that's landing-page-copywriter.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, SEO, Blog, Writing, E-E-A-T]
    related_skills: [deep-research-brief, landing-page-copywriter, newsletter-assembler, content-repurposer, brand-voice-guardian]
---

# SEO Blog Writer

Produces posts that earn rankings the durable way: match the searcher's actual intent before writing a word, structure with scannable H2/H3s, prove experience and cite real sources, and write for a human who might link to it. The keyword appears where it belongs and nowhere else.

## When to Use

- The user has a target keyword, topic, or content brief and wants an outline or full draft.
- An existing post needs an intent-match or E-E-A-T upgrade.
- The user asks for "meta title and description", "blog outline", or "article that ranks".
- **Not for:** conversion-focused landing or sales pages (`landing-page-copywriter`), email content (`email-nurture-sequence`), or the underlying research when claims need sourcing first (`deep-research-brief`).

## Quick Reference

| Action | Rule |
|---|---|
| Intent check | Classify the keyword: informational / commercial / transactional / navigational — before outlining |
| Structure | One H1; H2s answer the sub-questions searchers have; H3s only under a parent H2 |
| Keyword use | Title, first 100 words, one H2, conclusion — then only where natural |
| E-E-A-T | ≥1 first-hand experience marker; ≥2 named, linkable sources; author-relevant framing |
| Density guard | `python3` count in step 6 — exact keyword >1.5% of words = rewrite |
| Meta pair | Title ≤60 chars with keyword front-loaded; description 140–155 chars with a reason to click |

## Procedure

1. **Classify intent** — from the keyword (and SERP notes if the user can share them), state the intent class and the searcher's real question in one sentence: "Someone typing X wants Y." If the brief's angle contradicts the intent (e.g., a sales pitch against an informational query), flag it and align before outlining — a mismatched post won't rank regardless of quality.
2. **Gather E-E-A-T raw material** — ask the user for: first-hand experience with the topic (what they've done, built, tested, measured), 2+ credible sources they trust, and who the author is. No experience available → write honestly from research and say so; never fabricate "when I tested this".
3. **Outline** — H1 (promise matching intent), then 4–8 H2s each answering one sub-question, H3s where a section splits. Include where the experience proof and each source lands. Deliver the outline for approval when the user asked for outline-first; otherwise proceed.
4. **Draft** — answer the searcher's question in the first 100 words (no "in today's digital landscape" wind-ups), then earn depth section by section. Short paragraphs (≤4 lines), specifics over abstractions, every claim either sourced, experienced, or clearly framed as opinion.
5. **Weave E-E-A-T** — experience markers in concrete form ("we ran this for 6 weeks; here's the number"), sources cited inline with name + link placeholder, and an author-context line if the platform shows bylines.
6. **Stuffing audit** — count it, don't feel it: `python3 -c "t=open('/tmp/draft.md').read().lower();w=t.split();k='KEYWORD';print(t.count(k), len(w), round(t.count(k)/max(len(w),1)*100,2))"`. Exact-match density above ~1.5%, or any sentence that exists only to hold the keyword, gets rewritten with variants or pronouns.
7. **Meta pair + deliver** — write meta title (≤60 chars, keyword early, promise clear) and meta description (140–155 chars, states the payoff, gives a click reason). Assemble the Output Template.

## Output Template

```
# [H1]

**Target keyword:** [kw] | **Intent:** [class] — "[searcher's real question]"
**Meta title (≤60):** ...
**Meta description (140–155):** ...

[Draft: answer-first intro → H2/H3 body with inline sources → conclusion + next step]

---
**E-E-A-T ledger**
- Experience markers: [where + what]
- Sources: 1) [Name — link] 2) ...
- Author context: [line or "n/a"]
**Density check:** [count]/[words] = [x.x]%
```

## Pitfalls

- **Intent mismatch** — a beautiful how-to guide targeting a keyword where searchers want a comparison. Recovery: redo step 1 honestly; restructure the outline to the dominant intent, keep the off-intent material as a section, not the spine.
- **Fabricated experience** — "when we tested this" appears with no test behind it. Recovery: strip every experience claim the user didn't actually confirm in step 2; replace with sourced third-party evidence or cut.
- **Keyword stuffing by enthusiasm** — the exact phrase lands in every H2 and image alt. Recovery: run the step 6 count; rewrite flagged sentences using natural variants; keep exact match only in the Quick Reference's four positions.
- **Wall-of-text sections** — 300-word paragraphs under a single H2. Recovery: split any H2 section >250 words with H3s or a list; re-scan for a ≤4-line paragraph rhythm.
- **Generic AI intro** — "In today's fast-paced world..." Recovery: delete the first paragraph; if the second paragraph answers the question, it's your new intro.

## Verification

- [ ] Intent class stated and outline visibly serves it
- [ ] First 100 words answer the searcher's question
- [ ] ≥1 real experience marker (user-confirmed) and ≥2 named sources with link placeholders
- [ ] Step 6 density check run and printed in the ledger; ≤1.5% exact match
- [ ] Meta title ≤60 chars, description 140–155 chars (character-counted, not guessed)
- [ ] No sentence exists solely to contain the keyword
- [ ] E-E-A-T ledger printed at the bottom of the deliverable (experience markers, sources, author context)
