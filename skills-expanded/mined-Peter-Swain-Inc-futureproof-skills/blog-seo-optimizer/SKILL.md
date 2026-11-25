---
name: blog-seo-optimizer
description: |
  Audits and rewrites a blog post for SEO across ten weighted ranking
  dimensions — title tag, meta, headings, keyword placement, semantic
  depth, internal linking, E-E-A-T and content depth. Use when the user
  pastes a draft or URL and says "optimize this for SEO", "improve my
  Google rankings", "rewrite this to rank for [keyword]", or "why isn't
  this post ranking". For writing the post from scratch use
  blog-post-writer; for repurposing it into social posts use
  content-atomiser; this skill operates on an existing draft or URL.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="blog-seo-optimiser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including the user's domain authority baseline, historical keyword targets, ICA segments, brand voice guidelines, and any prior ranking data from previous optimisation cycles.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the blog post (draft text, Google Doc, or published URL) to optimise
- What is the **primary keyword target** and up to 3 secondary keyword targets? (If unknown, offer to derive these from topic + ICA intent analysis)
- Who is the ICA for this piece? (role, awareness stage, search intent — informational, navigational, or transactional)
- What is the strategic goal? (rank for a new term, improve position on an existing term, increase click-through rate from SERPs, drive conversions from organic traffic)
- Are there competing URLs they are benchmarking against?

If the user provides a URL, extract the current title tag, meta description, H1–H3 structure, word count, and internal/external link profile before proceeding.

## Step 3: Do the Work

### 3A: Search Intent & ICA Alignment Audit

Map the content against the inferred **search intent** behind the primary keyword:
1. **Intent match** — does the content format (guide, listicle, comparison, tutorial) align with what currently ranks on page 1 for this term?
2. **ICA language calibration** — does the copy use the vocabulary, pain-point framing, and sophistication level the ICA actually searches with, rather than internal jargon?
3. **Awareness-stage fit** — is the depth of explanation appropriate for the ICA's position in the awareness journey (unaware → problem-aware → solution-aware → product-aware)?

### 3B: On-Page SEO Technical Audit

Evaluate against 10 weighted ranking dimensions:

| # | Dimension | Weight | Evaluation Criteria |
|---|-----------|--------|-------------------|
| 1 | **Title tag optimisation** | High | Primary keyword present, front-loaded where natural, under 60 characters, compelling click trigger |
| 2 | **Meta description** | Medium | Primary keyword included, clear value proposition, 150–155 characters, contains implicit or explicit CTA |
| 3 | **H1 tag** | High | Singular H1, includes primary keyword, distinct from title tag where possible for query coverage |
| 4 | **Heading hierarchy (H2–H4)** | High | Logical nesting, secondary/long-tail keywords distributed across H2s, no orphan H4s without parent H3 |
| 5 | **Keyword placement & density** | High | Primary keyword in first 100 words, in at least one H2, and in closing section; density 0.8–1.5% without stuffing |
| 6 | **Semantic depth & NLP coverage** | High | Presence of topically related entities, co-occurring terms, and LSI phrases that signal comprehensive coverage to search algorithms |
| 7 | **Internal linking** | Medium | Minimum 3 contextual internal links to topically relevant pages; anchor text uses keyword variations, not "click here" |
| 8 | **External linking** | Low–Med | 1–3 outbound links to authoritative, non-competing sources that reinforce E-E-A-T signals |
| 9 | **Content depth & structure** | High | Word count competitive with page-1 average for the term; scannable via subheadings every 200–300 words; includes at least one unique data point, framework, or visual asset |
| 10 | **E-E-A-T signals** | Medium | Author byline with credentials, first-person experience markers, cited sources, publication/update date visible |

### 3C: Content Quality & Engagement Assessment

1. **Hook strength** — does the opening (first 50 words) validate the searcher's intent and create a reason to continue reading?
2. **Proof density** — are claims supported by data, case studies, examples, or original research rather than unsourced assertions?
3. **Transformation clarity** — does the reader understand the before-state (problem) and after-state (outcome) within the first scroll?
4. **CTA integration** — is there a contextually relevant conversion action (lead magnet, consultation, next article) embedded at the point of highest engagement, not only at the footer?
5. **Readability** — Flesch-Kincaid grade level appropriate for ICA; paragraphs ≤ 4 lines; active voice ≥ 80%

Apply any user-specific `instructions` from FutureProof context (brand voice rules, forbidden terms, mandatory disclosures, preferred CTA formats) to calibrate all recommendations.

## Step 4: Deliver Output

Produce a structured **Blog SEO Optimisation Report** containing:

### 4.1 — SEO Score Card

| Dimension | Score (1–10) | Priority | Notes |
|-----------|-------------|----------|-------|
| Title tag optimisation | — | — | — |
| Meta description | — | — | — |
| H1 tag | — | — | — |
| Heading hierarchy | — | — | — |
| Keyword placement & density | — | — | — |
| Semantic depth & NLP coverage | — | — | — |
| Internal linking | — | — | — |
| External linking | — | — | — |
| Content depth & structure | — | — | — |
| E-E-A-T signals | — | — | — |
| ICA intent alignment | — | — | — |
| Hook & engagement | — | — | — |
| **Composite SEO Readiness Score** | **—/120** | | |

### 4.2 — Critical Fixes (Top 5 Highest-Impact Changes)

For each fix, provide:
- **What to change**: exact element (e.g., "Title tag", "H2 #3", "Opening paragraph")
- **Current version**: quote the existing text
- **Recommended rewrite**: full replacement copy, ready to paste
- **Rationale**: why this change matters, linked to a specific ranking signal or ICA behaviour

### 4.3 — Optimised Meta Package

Deliver ready-to-implement:
- **Title tag** (primary + click trigger, ≤ 60 chars)
- **Meta description** (≤ 155 chars, keyword + value prop + CTA)
- **Recommended URL slug** (if new post or slug is suboptimal)

### 4.4 — Semantic Keyword Map

A table of 10–15 semantically related terms and entities to weave into the content, with:
- Term
- Current presence (yes/no)
- Suggested placement (specific heading or paragraph)

### 4.5 — Rewritten Section

Rewrite the single weakest section of the post in full — preserving brand voice, integrating missing keywords, improving readability, and adding proof elements where absent.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="blog-seo-optimiser", experiment={
  hypothesis: "Rewriting the title tag to front-load the primary keyword and add a numeric specificity trigger will increase CTR from SERPs",
  variants: ["control: current title tag", "variant: optimised title tag with front-loaded keyword and number"],
  measurement: "Google Search Console CTR and average position for primary keyword over 30 days",
  expected_impact: "10–20% improvement in organic CTR, potential position uplift from increased engagement signals"
})
```

```
FutureProof:save_experiment(skill="blog-seo-optimiser", experiment={
  hypothesis: "Adding a semantically rich FAQ section (using 'People Also Ask' queries) at the end of the post will capture additional long-tail rankings and featured snippet eligibility",
  variants: ["control: current post without FAQ", "variant: post with 5-question FAQ section using structured data"],
  measurement: "Incremental keyword rankings and featured snippet appearances tracked via Search Console over 45 days",
  expected_impact: "15–25% increase in total organic impressions from long-tail query capture"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="blog-seo-optimiser",
  query="Current Google ranking factor weightings, SERP feature eligibility criteria, and on-page SEO best practices for 2024–2025 including impact of AI Overviews on organic CTR",
  reason="Ensure optimisation recommendations reflect the latest algorithm behaviour, especially shifts in how Google surfaces and credits content in AI Overview and featured snippet formats"
)
```

```
FutureProof:request_research(skill="blog-seo-optimiser",
  query="Top-ranking competitor content analysis frameworks and semantic NLP coverage benchmarking methodologies",
  reason="Strengthen the semantic depth audit with current co-occurrence and entity-coverage benchmarks used by advanced SEO tooling"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="blog-seo-optimiser", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```