---
name: content-repurposer
description: Takes one long-form piece (article, video transcript, talk, research brief) and produces a repurposing matrix — LinkedIn post, X thread outline, newsletter blurb, and 3 short-video hooks — each adapted to platform norms, never copy-pasted. Use when the user asks to "repurpose this", "turn this into social content", "spread this across platforms", "atomize this post", or "get more out of this piece". Don't use for producing the final polished posts — this skill outlines; hand cells to linkedin-content-pack or x-thread-builder.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, Repurposing, Multi-Platform, Social]
    related_skills: [deep-research-brief, brand-voice-guardian, linkedin-content-pack, x-thread-builder, newsletter-assembler]
---

# Content Repurposer

Extracts the reusable core of one long-form piece and re-expresses it natively for four destinations: a LinkedIn post, an X thread outline, a newsletter blurb, and 3 short-video hooks. The test for every cell of the matrix: it must read like it was born on that platform, not exported to it. Everything ships as drafts.

## When to Use

- A finished long-form piece exists and the user wants multi-platform mileage from it.
- A `deep-research-brief` deserves distribution beyond one channel.
- **Not for:** producing the final polished LinkedIn pack or full X thread (this skill outlines; hand cells to `linkedin-content-pack` or `x-thread-builder` for full builds), or drafting the source piece itself.

## Quick Reference

| Action | Command / Call |
|---|---|
| Word-count source | `python3 -c "print(len(open('/tmp/source.txt').read().split()))"` |
| Extract idea inventory | 5–8 atomic ideas, each quotable alone (step 2) |
| Platform fit rules | LinkedIn = professional lesson; X = punchy sequence; newsletter = editorial take; video = spoken hook |
| Char-check any cell | `python3 -c "print(len('''TEXT'''))"` |
| Full builds | Route to `linkedin-content-pack` / `x-thread-builder` / `newsletter-assembler` |

## Procedure

1. **Precheck** — confirm you have the full source text (save to `/tmp/source.txt`; run the word count — under ~400 words means it's not long-form, so tell the user a single-platform skill fits better). Confirm audience and which platforms matter; default to all four.
2. **Build the idea inventory** — read the whole piece, then list 5–8 atomic ideas: each a standalone claim, stat, story, or framework with a line reference to where it lives in the source. This inventory — not the source's structure — feeds every platform. No idea in the inventory, no idea in the matrix.
3. **LinkedIn post** — pick the idea with the strongest professional "lesson learned" or contrarian-but-defensible angle. Draft hook-first (line 1 ≤200 chars, python3-checked), short paragraphs, substance in-post, no engagement bait, link reserved for a first comment. This is a different idea-framing than the X thread uses — if two cells lead with the same sentence, one is wrong.
4. **X thread outline** — pick the idea that decomposes into a sequence (steps, escalating list, before/after). Write the opener tweet in full (≤280 chars, python3-checked) plus one-line summaries for 5–9 body tweets and the CTA close. Punchier and more concrete than the LinkedIn framing.
5. **Newsletter blurb** — 60–120 words of editorial take for an existing newsletter section: why the piece matters to that reader, one specific takeaway, then the link. Written as the curator's voice about the piece, not a summary of it.
6. **3 short-video hooks** — three distinct spoken opening lines (≤2 sentences each) for Reels/Shorts/TikTok, each from a DIFFERENT inventory idea. Written for the ear: present tense, direct address, concrete stakes in the first sentence. Banned: "Wait for it", "You won't believe", "Stop scrolling".
7. **Assemble & deliver** — fill the matrix template, noting which inventory idea each cell used (prove no copy-paste: no sentence appears verbatim in two cells). Recommend `brand-voice-guardian` for a voice pass and the sibling skills for full builds of any cell.

## Output Template

```
# Repurposing Matrix: [source title]
**Source:** [link/file] | **Audience:** [who]

## Idea inventory
1. [atomic idea] (source ref)
... (5–8 total)

## LinkedIn post (idea #x) — full draft
[hook / body / close]

## X thread outline (idea #y)
1/ [full opener, char-checked]
2/–n/ [one-line per tweet]
n+1/ [CTA close]

## Newsletter blurb (idea #z) — 60–120 words
[take + link]

## Short-video hooks
A. (idea #_) "[spoken line]"
B. (idea #_) "[spoken line]"
C. (idea #_) "[spoken line]"

## Next steps
- Full builds: linkedin-content-pack / x-thread-builder / newsletter-assembler
```

## Pitfalls

- **Copy-paste with line breaks** — the "X thread" is just the article's paragraphs chopped at 280 chars. Recovery: return to the idea inventory and re-express the idea in platform-native rhythm; if a cell shares a verbatim sentence with the source or another cell, rewrite it from the idea, not the text.
- **Same angle everywhere** — all four cells lead with the same framing, so cross-platform followers see reruns. Recovery: step 2's inventory exists precisely for this — assign different lead ideas per cell and record the assignment in the output.
- **Video hooks written for the eye** — subordinate clauses and semicolons nobody can speak. Recovery: read each hook aloud; if it takes a breath mid-sentence or sounds like prose, shorten to how a person actually talks.
- **Inventory drift** — a matrix cell contains a claim that isn't in the source. Recovery: every cell cites its inventory idea number; audit each cell against its cited idea and cut anything the source doesn't support.

## Verification

- [ ] Idea inventory has 5–8 entries, each with a source reference
- [ ] Every matrix cell cites which inventory idea it used; no two cells share a lead idea
- [ ] No sentence appears verbatim in more than one cell or copied from the source
- [ ] LinkedIn hook and X opener char-checked via python3 (counts reported)
- [ ] All cells delivered as drafts; full-build handoffs to sibling skills noted
