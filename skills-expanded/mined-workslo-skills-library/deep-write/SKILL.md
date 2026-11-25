---
name: deep-write
description: Recursive article writing and improvement. Use when the user wants to write a blog post, article, or long-form content — or says "deep write", "write an article", "blog post", "long-form", "write about", or wants to develop an idea into a full article. Applies autonomous iteration (research → draft → verify → improve → repeat) to produce publication-quality content.
---

# Deep Write

Autonomous loop for writing and recursively improving articles. Inspired by Karpathy's autoresearch — the same modify → verify → keep/discard → repeat cycle, adapted for content instead of code.

The core idea: a first draft is an experiment. Each revision pass has a specific lens. You verify mechanically against a rubric, keep what improves, discard what doesn't. You stop when the article converges — when a revision pass can't find anything worth changing.

## When This Activates

- User wants to write a blog post or article
- User has an idea they want developed into long-form
- User says "deep write", "write an article about X", "blog post about X"
- Workshop identifies an idea too big for a tweet — hand off here

## Relationship to Other Skills

- **workshop-x-posts** handles tweets and short-form. deep-write handles articles.
- **scout-x** feeds raw material that might become article topics.
- **writing-voice** still governs tone — but articles have more room than tweets. The voice rules apply; the length constraints don't.
- **humanizer** runs as a final pass before presenting any draft.
- **wiki** is your research base. Always check it before writing.

## Reference Files

- `references/quality-rubric.md` — The 10 dimensions that distinguish a great article. Every revision pass scores against this.
- `references/revision-lenses.md` — The specific lenses for each revision pass in the loop.

Onboard seeds the rubric's reference examples from the person's own favorites and representative posts in their space. Re-run onboard to refresh calibration.

## The Process

### Phase 1: Research

Before writing a word:

1. **Check the wiki** — read memories/wiki/index.md and any relevant topic pages. What do you already know?
2. **Check memories/raw/** — search memories/raw/articles/ and memories/raw/tweets/ for source material on the topic.
3. **Search the web** — fill gaps. Find primary sources, data, concrete examples, other perspectives. Save anything substantial to memories/raw/articles/.
4. **Update the wiki** — compile findings into the relevant wiki topic. This is your working outline.

Don't skip this. The research phase is what separates an article that teaches something from one that restates conventional wisdom. The goal is to have more material than you'll use — you want to be cutting, not stretching.

### Phase 2: Frame

Before drafting, get clear on three things:

1. **The one-sentence thesis** — what's the single claim this article makes? If you can't say it in one sentence, you don't have an article yet. You have two articles, or you have a vague gesture.
2. **The reframe** — what does the reader currently believe that this article will change? The best articles correct a misconception or reveal a hidden cost. If there's no reframe, the article is informational but not compelling.
3. **The audience** — who specifically benefits from reading this? Narrow is better than broad. "Developers" is too broad. Be specific enough to shape decisions about what to include and what to cut.

Present the frame to the user. Get confirmation before drafting. A bad frame produces a bad article no matter how many revision passes you run.

### Phase 3: Draft (Iteration 0)

Write the full first draft. Don't self-censor — get it all down. But follow these structural defaults:

- **Open with the reframe**, not a summary of what the article covers
- **One idea per section**, each with a concrete example or evidence
- **Product/company mentions come after the insight** — earn the right to reference them by first teaching something useful
- **End with implications**, not a recap — what should the reader do or think differently?
- **Right-size it** — match length to argument complexity. Don't pad a 500-word insight into 2000 words.

Save the draft to a working file in `/drafts/` on the root filesystem during the session — do NOT save it to `/memories/` yet. This is iteration 0.

### Phase 4: The Loop

```
LOOP (until converged or max iterations):
  1. Select the next revision lens (see references/revision-lenses.md)
  2. Read the current draft through that lens ONLY
  3. Score each rubric dimension 1-5 (see references/quality-rubric.md)
  4. Identify the weakest dimensions (any scoring ≤ 3)
  5. Make targeted revisions to address ONLY the weakest dimensions
  6. Re-score the changed dimensions
  7. DECIDE:
     - Scores improved → KEEP revisions
     - Scores same or worse → REVERT, move to next lens
     - All dimensions ≥ 4 → CONVERGED, exit loop
  8. Log: which lens, what changed, scores before/after
```

**Revision lenses cycle in order:**
1. Structure & argument (is the logic tight?)
2. Evidence & concreteness (are claims grounded?)
3. Voice & readability (does it sound right?)
4. Compression (can anything be cut?)

After cycling through all four lenses with no improvements to make, the article has converged.

**Bounded mode:** User can specify `Iterations: N` to cap the number of revision passes. After N passes, stop and present the current state with scores.

**Default: 4 passes** (one per lens) unless the user specifies otherwise or the article clearly needs more work.

### Phase 5: Present

When the loop exits:
- Run the draft through the **humanizer** skill as a final pass
- Present the final article
- Show the rubric scorecard (10 dimensions, each scored 1-5)
- Note what changed from draft to final (the delta)
- Flag any dimensions still below 4 — these are known weaknesses the user might want to address manually

## Where Drafts Live

- **During the session:** work on the draft in the thread or in `/drafts/` on the root filesystem. Do not save drafts to `/memories/`.
- **After posting or sharing:** once the piece is finalized and published, it can be saved to `/memories/` as reference.
- **Raw material and wiki updates:** those are reference, not drafts — fine to save to `/memories/` anytime during research.

## Rules

- Never publish without the user's explicit approval
- Research before drafting — always
- Frame before drafting — always
- One thesis per article — if there are two, split into two articles
- Revision passes have a single lens — don't try to fix everything at once
- The rubric is mechanical — score honestly, not generously
- When a revision doesn't improve scores, revert it. Don't keep changes just because you made them.
- Always run humanizer as a final pass before presenting
- Raw material captured during research goes to memories/raw/articles/ and follows wiki-markdown formatting
- Wiki updates from research follow the same rules as scout-x — rewrite sections to be current, don't just append

## What Deep Write Does NOT Do

- Does not handle tweets or short-form (that's workshop-x-posts)
- Does not scan for new topics (that's scout-x)
- Does not post without approval
- Does not update the voice profile (that's onboard — but flag calibration-worthy edits if the user rewrites significantly)
