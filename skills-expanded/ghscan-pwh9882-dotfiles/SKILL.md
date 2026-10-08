---
name: pro-verify
description: Digest and analyze a Pro, Astra, or Codex review response. Evaluate its proposed directions, verify key facts, and produce an actionable strategy digest.
---

# Review Response — Digest & Verify

Analyze the supplied review response. The goal is to **understand the review, evaluate its proposed direction, and produce an actionable strategy digest**. The skill name `pro-verify` and the term "Pro" below retain the existing review workflow; they do not imply a particular model version.

Record the actual reviewer model, effort, and surface when known. Keep historical model labels accurate; mark missing provenance as unknown instead of relabeling older responses as Astra. If the user requests a new Codex follow-up review, default to `gpt-6-astra` with `medium` reasoning unless explicitly overridden, and follow the `codex` skill when available. Verification alone does not launch another reviewer.

## What This Skill Is Really For

The purpose of consulting Pro is to get **expert analysis, problem diagnosis, and strategic direction** from a powerful reasoning model. When we receive Pro's response, we need to:

1. **Understand the analysis** — What did Pro find? What patterns did it identify? What problems did it diagnose?
2. **Evaluate the direction** — Are the proposed directions sound? Do they align with our architecture? Are there risks?
3. **Verify key facts** — Spot-check important factual claims that underpin the analysis (but this is supporting work, not the main output)
4. **Produce actionable next steps** — What should we actually do based on this review?

**Common mistake to avoid**: Don't turn this into a fact-checking scorecard where the output is "X/Y claims CORRECT." That misses the point entirely. A review where Pro says 24 true things but gives bad direction is worse than one where Pro gets 2 facts wrong but provides brilliant strategic insight.

## Context Assessment — Ask vs Autonomous

- **Autonomous mode**: If you know the project, the review topic, and where the response file is — proceed directly.
- **Ask mode**: If the response file location is unclear or you lack project context, ask only what's missing.

## Workflow

### Step 1: Locate the Response

- If `$ARGUMENTS` is a file path, read that file directly.
- If `$ARGUMENTS` is a name/keyword, search `docs/reviews/response/` for matching files.
- If no arguments, find the most recently modified `.md` file in `docs/reviews/response/`.

### Step 2: Read and Understand the Full Response

Read the entire Pro response carefully. Identify:

1. **What questions were asked** (from the request document)
2. **What analysis Pro performed** — data exploration, pattern identification, root cause diagnosis
3. **Key findings** — the non-obvious insights that change how we think about the problem
4. **Strategic directions** — what Pro recommends and why
5. **Specific suggestions** — concrete implementation proposals

### Step 3: Fact-Check Key Claims (Supporting Work)

Verify the **important factual claims that Pro's analysis depends on**. Focus on:

- Claims that would change the direction if wrong (e.g., "metric_app.csv exists but is skipped" — if it doesn't exist, the suggestion to load it is moot)
- Quantitative claims used to prioritize (e.g., "27 cases have only datetime wrong" — if it's actually 5, the priority changes)
- Code/architecture claims that affect feasibility (e.g., "max_dur_ts is already computed" — if not, the effort estimate changes)

Don't exhaustively verify every statement. Focus on claims that **matter for decisions**.

### Step 4: Evaluate Directions Against Project Context

For each direction Pro proposes, assess:

1. **Alignment with architecture** — Read the reviewed project's current instructions and decisions, including protected artifacts and evidence boundaries. Apply those project constraints; do not transfer another project's rules merely because this skill was used there.
2. **Past experience** — Have we tried something similar? What happened? (Check `docs/reviews/`, `docs/experiments/`, memory)
3. **Model-divergence risk** — For prompt-level changes, check the project's per-model results and previous reviews. If behavior differs across models, retain that evidence and assess the relevant models separately. Do not assume divergence without evidence.
4. **Generality** — Would this work on an unseen domain, or is it benchmark-specific?
5. **Risk/reward** — What's the downside if it doesn't work? Can it make things worse?

Historical project-specific examples: the earlier V7 constraint allowed feature extraction but prohibited label emission; another instruction protected the overview, and earlier review work recorded opposite prompt effects across models on five occasions. These are discovery clues, not universal rules or independently verified results. Locate the originating project and evidence before applying or citing them. If unavailable, mark the background unverified rather than inventing provenance.

### Step 5: Write the Review Digest

Create `docs/reviews/{date}-{nn}-{topic}.md` (date `YYYY-MM-DD`, `{nn}` = per-day creation sequence starting at `01`; e.g. `2026-08-03-01-cross-replay-result.md`):

```markdown
# Review #{sequence}: {Title}

Date: {today}
Input: {archive or source description}
Reviewer: {actual model / effort / surface, or unknown}

## What Pro Analyzed

[Summary of the analysis Pro performed — what data it looked at, what patterns it found, what questions it answered]

## Key Findings

[The most important non-obvious insights from Pro's analysis. These are the things that change how we think about the problem.]

### Finding 1: {title}
[What Pro found, why it matters, and whether our fact-check confirms it]

### Finding 2: {title}
...

## Strategic Direction

[What overall direction Pro recommends and our assessment of it]

### Direction 1: {title}
**Pro's reasoning**: [why Pro suggests this]
**Our assessment**: [agree/disagree/modify, with reasons]
**Risk**: [what could go wrong]

### Direction 2: {title}
...

## Fact-Check (Key Claims)

[Only claims that matter for decisions. Brief table format.]

| Claim | Verified? | Impact on Direction |
|-------|-----------|-------------------|
| {important claim} | Yes/No/Partial | {how it affects our plans} |
| ... | ... | ... |

## Action Plan

[Concrete prioritized list of what to do next, synthesizing Pro's input with our own judgment]

| Priority | Task | Rationale | Effort | Risk |
|----------|------|-----------|--------|------|
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |

## Open Questions

[Things Pro raised that we need to think about more, or things Pro didn't address that we still need to figure out]
```

### Step 6: Present to User

After writing the report, present a **concise analytical summary** to the user:

- What were Pro's key insights? (top 2-3)
- What direction does Pro recommend and do we agree?
- What should we do first?
- What are we skeptical about and why?

**Tone**: Analytical and opinionated. Don't just relay what Pro said — add your own assessment. The user wants a thought partner, not a stenographer.

## Important Notes

- **File locations (fixed convention)**: all filenames start with `{date}-{nn}-` (date `YYYY-MM-DD`, `{nn}` = per-day creation sequence from `01`):
  - Pro responses: `docs/reviews/response/{date}-{nn}-{topic}-review-response.md`
  - Review digests: `docs/reviews/{date}-{nn}-{topic}.md`
  - Request docs & archives: `docs/reviews/request/`
- **Sequence numbering**: `{nn}` orders files created the same day in the same directory — check existing files with today's date prefix to pick the next number.
- **Past lessons matter**: If a suggestion resembles something tried before, flag it with what happened.
- **Model comparison**: For prompt changes, use the relevant project's per-model evidence; identify missing validation without asserting universal instability.
- **Be honest**: If you think Pro's direction is wrong, say so and explain why. "Accept unless baseless" means accept valid analysis, not blindly follow every suggestion.
- **Never skip fact-checking on decision-critical claims**: Even if a claim sounds right, verify it if the whole direction depends on it.
