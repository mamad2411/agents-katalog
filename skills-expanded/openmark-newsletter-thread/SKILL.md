---
name: openmark-newsletter-thread
description: Compose a short LinkedIn-post-style thread from Ahmad's OpenMark saves. Use when Ahmad wants a tight 200–400 word post he can paste into LinkedIn, X, or a short newsletter slot — NOT a long essay or full digest. Trigger phrases include "thread", "LinkedIn post", "short post", "tweet thread", "quick newsletter", "social post", "/newsletter-thread". Output is one strong hook + 4–7 short paragraphs + ONE link. Optimized for skim-reading on a phone.
metadata:
  type: composition
---

# OpenMark — Newsletter Thread

Short. Punchy. Phone-readable. ~250-400 words total. ONE link. No tables. No bullet lists.

## When to use vs other newsletter skills

| User intent | Skill |
|---|---|
| "Quick LinkedIn post" / "short post" / "tweet" | this one (thread) |
| Full newsletter, multiple sources | openmark-newsletter |
| Categorical recap | openmark-newsletter-roundup |
| Long-form argument | openmark-newsletter-essay |
| Side-by-side comparison | openmark-newsletter-comparison |

## Get the angle FIRST

Threads need ONE specific moment, idea, or claim — not a survey. If Ahmad
didn't give one, ASK once:

> "What's the ONE thing — a specific paper, take, tool, or moment — you
> want this post to be about?"

Threads about "AI in general" suck. Threads about "the one chart from
Anthropic's report that everyone missed" work.

## Tool sequence (tight budget)

You get 2-3 tool calls MAX. This is a short post.

1. `search_semantic(query=<the angle>, n=8)` — find the anchor bookmark.
2. `get_bookmark_full(url=<top hit's URL>)` — get the anchor's full context.
3. Optional: `WebFetch(url=<anchor URL>, prompt="Extract one verbatim quotable line and the single most surprising number/claim.")`

That's it. No expansion, no community walks. The post lives or dies on ONE source.

## Output format — NON-NEGOTIABLE

```
# {Hook — a specific 6–10 word claim, NO question marks}

{Paragraph 1: 1–2 sentences. State the surprising fact / claim / moment.
This is the line that stops scrolling. Concrete subject + concrete verb.}

{Paragraph 2: 1–2 sentences. Add the one piece of context the reader
needs to understand why paragraph 1 matters.}

{Paragraph 3: 2–3 sentences. The specific evidence — quote, number, or
named example from the anchor source. Cite inline as
`[descriptive phrase](URL)`.}

{Paragraph 4 (optional): 1–2 sentences. The "so what" — a concrete
implication, behavior change, or counter-take. Sharp, not preachy.}

{Paragraph 5 (closer): 1 sentence. The line you want re-tweeted.
Standalone, quotable, opinionated. NOT a question.}

---

## Sources cited

1. [{anchor title}]({anchor URL}) — {one short phrase on what it provides}

_~{word_count} words · thread style · 1 anchor source_
```

### Formatting rules — strict

- **Single H1.** That's the hook.
- **4-6 paragraphs total.** Not bullet points. Real sentences in paragraphs.
- **One blank line between every paragraph.** Otherwise the renderer collapses them.
- **Exactly ONE inline link** in the body — to the anchor source. No second link.
- **The closer (final paragraph) is ONE sentence.** No "in conclusion." Just the line.
- **`## Sources cited`** with just the one anchor. Required for auto-export.
- **No em dashes used as pause** (matches Ahmad's project rule). Use commas, parens, colons, or line breaks.

## Voice — calibrated for social

| Generic | Thread voice |
|---|---|
| "AI agents are evolving rapidly." | "Three weeks ago an agent shipped its own pull request. The maintainer didn't notice for a day." |
| "This paper is interesting." | "Most agent benchmarks measure the wrong thing. This paper proves it with seven numbers." |
| "Worth checking out." | "Read the abstract. Then read the footnotes. The footnotes are the paper." |
| "I think we should..." | "Stop doing X. Start doing Y." |

Sentence fragments: encouraged. Numbers: specific. Names: named.
Hedges ("might", "could", "perhaps"): banned.

## What NOT to do

- Don't exceed 400 words. If you hit 401, cut, don't trim.
- Don't include hashtags. The reader adds those when they post.
- Don't link to more than one URL. Threads with two links pull the reader two directions.
- Don't open with a rhetorical question. Open with a claim.
- Don't end with "Thoughts?" or "What do you think?". End with the line you want quoted.
- Don't number the paragraphs (no "1/", "2/" prefixes). Markdown handles flow.
