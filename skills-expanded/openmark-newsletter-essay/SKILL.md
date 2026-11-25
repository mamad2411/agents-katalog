---
name: openmark-newsletter-essay
description: Write a single-thesis narrative newsletter essay from Ahmad's OpenMark saves. Use when Ahmad wants a thoughtful long-form piece with one clear argument, not a roundup or news recap. Trigger phrases include "essay", "long-form", "think piece", "thoughtful post", "argue that", "make a case for", "/newsletter-essay". Output is one strong thesis sentence + 3–5 narrative sections + closing call-to-think, no tables, no bullets unless necessary.
metadata:
  type: composition
---

# OpenMark — Newsletter Essay

One thesis. Built over 600–900 words. Narrative paragraphs, not bullets. Each section advances the argument. Citations are inline `[phrase](URL)` links, NEVER footnotes.

## When to use vs other newsletter skills

| User intent | Skill |
|---|---|
| "Argue X" / "make the case for Y" | this one (essay) |
| Categorical recap | openmark-newsletter-roundup |
| Punchy analytical "this week mattered because" | openmark-newsletter |
| Compare A vs B side by side | openmark-newsletter-comparison |

## Get the thesis FIRST

If Ahmad didn't state a clear thesis, ASK once. ONE question:

> "What's the one sentence you want a reader to remember from this essay?"

Don't pull data until you have a thesis. The thesis dictates which bookmarks matter.

## Tool sequence

Once thesis is locked:

1. `search_semantic(query=<thesis as query>, n=20)` — your core net.
2. ONE of:
   - `search_by_community(query=<thesis>, n=15)` — if thesis spans a topic cluster
   - `search_by_category(category=<inferred>, query=<thesis>, n=15)` — if thesis maps to one category
3. `search_linkedin(query=<thesis>, n=10)` — for human voices that support or challenge the thesis.
4. Pick 5–8 anchor URLs that genuinely advance the argument. Drop hits that just match keywords but don't deepen the thesis.
5. `WebFetch` the top 3–5 to get quotable lines. If a fetch fails, drop it — no retries.

## Output format — NON-NEGOTIABLE

```
# {Title — a sharp claim, ≤ 8 words, NO subtitle}

> **{One-sentence thesis. The whole essay defends or develops this.}**

{Opening paragraph: 2–4 sentences. Concrete hook — a scene, a stat, a
recent event, or a personal moment. Sets up the thesis from below, not
above. NO "in this essay I will argue."}

## {Section heading 1 — phrased as a sub-claim, not a topic}

{Narrative paragraph. 3–6 sentences. At least one inline link to an
OpenMark anchor — `[descriptive phrase](URL)`. Build the argument; don't
list facts.}

{Optional second paragraph for the same sub-claim.}

## {Section heading 2}

(same pattern, 3–5 sections total)

## The counter

{One paragraph. State the strongest objection to the thesis. Cite at
least one bookmark that supports the counter. Then respond — concede
what's true, sharpen the thesis where the objection misses.}

## What this means for {audience}

{Closing paragraph. 2–4 sentences. Translate the thesis into a concrete
shift in behavior, belief, or decision. End on the sharpest line.}

## Sources cited

1. [{title}]({URL}) — {what it contributed}
2. [{title}]({URL}) — {what it contributed}
...

_{word_count} words · {N} sources · drafted from OpenMark + WebFetch_
```

### Formatting rules — strict

- **Single H1 at the top.** Title only — no subtitle.
- **The thesis is a blockquote (`> **...**`)** directly under the H1.
- **Section headings are sub-claims**, not topics. "Why most agent demos fail" beats "Agent failure modes".
- **Paragraphs are real paragraphs**, separated by blank lines. No bullet lists in the body.
- **Citations are inline.** `[descriptive phrase](URL)`. NEVER `[1]`, `[2]`, footnotes, or `(source)` parenthetical.
- **`## The counter` is mandatory** — every essay needs to face one objection.
- **End with `## Sources cited`** — flat numbered list. Required for auto-export.

## Voice

Declarative. Specific. Uses concrete examples from the cited bookmarks. Avoid:

- "I think" / "I believe" / "in my view"
- "This essay argues" / "this piece will explore"
- "It's worth noting that" / "interestingly"
- Tricolons / rule of three patterns ("X, Y, and Z")
- Em dashes used as commas (Ahmad's project rule)

Use:

- "X happened. Y is why."
- "Most people get this wrong: ..."
- "The argument falls apart when ..."
- Sentence fragments for emphasis. Sparingly.

## What NOT to do

- Don't write more than 900 words. Tighter is better.
- Don't include bullet lists in the body. If you find yourself making one, rewrite it as a paragraph.
- Don't pull from more sources than you cite. If a source isn't named, it doesn't go in `## Sources cited`.
- Don't fabricate quotes. Only quote what WebFetch returned verbatim.
