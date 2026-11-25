---
name: social-media-analytics
description: |
  Analyzes performance data from LinkedIn, Instagram, TikTok, X, YouTube, or
  Meta across five lenses (ICA resonance, content efficiency matrix, algorithm
  alignment, funnel integrity, competitive context) and delivers a scorecard,
  top fixes, and a 30-day content calendar. Use when a user shares platform
  analytics or content metrics and says things like "audit my LinkedIn",
  "why is my Reels reach dropping", "review my social performance", or "what
  content should I double down on". Social platform performance — not GA4
  website analytics and not paid ad campaign post-mortems.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="social-media-analytics")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any known ICA profiles, brand voice guidelines, historical benchmarks, and platform-specific performance baselines established in prior sessions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Data source**: Share the analytics export, dashboard screenshot, or raw metrics to analyse (platform, date range, granularity)
- **Platforms in scope**: Which channels are included? (e.g. LinkedIn, Instagram, TikTok, X/Twitter, YouTube, Meta Ads Manager, multi-platform)
- **ICA definition**: Who is the intended audience? What transformation or outcome does the content promise them?
- **Primary objective**: What are they optimising for? (audience growth, engagement rate, lead generation, brand awareness, content-to-pipeline conversion, community building)
- **Known constraints**: Budget ceiling, posting cadence capacity, team size, content production bandwidth
- **Comparison basis**: Are there prior period benchmarks, competitor accounts, or industry standards they want to measure against?

## Step 3: Do the Work

### 3A: Data Normalisation & Baseline Establishment

Standardise all provided metrics into a unified analytical framework:

1. **Reach & Impressions** — total impressions, unique reach, reach rate (reach ÷ follower count), impression frequency
2. **Engagement metrics** — likes, comments, shares/reposts, saves, clicks; calculate engagement rate using the platform-appropriate denominator (reach-based for Meta/Instagram, impression-based for LinkedIn, view-based for TikTok/YouTube)
3. **Audience growth** — net follower change, follow/unfollow ratio, growth rate vs. prior period, organic vs. paid acquisition split
4. **Content velocity** — posting frequency, content mix by format (static, carousel, video, Stories, long-form, Reels/Shorts), publish-to-engagement latency
5. **Conversion & pipeline indicators** — link clicks, CTR, landing page sessions attributed, lead form completions, UTM-tracked conversions, cost per lead (if paid)

Where the user has not provided industry benchmarks, apply standard reference rates (e.g. LinkedIn organic engagement 2–4%, Instagram Reels reach rate 30–50% of followers, TikTok average watch-through rate by duration tier).

### 3B: Performance Diagnostic (Five-Lens Analysis)

Evaluate the data against five strategic dimensions:

1. **ICA Resonance** — Does content performance correlate with ICA-relevant topics? Identify which themes, formats, and hooks generate disproportionate engagement from the target audience vs. vanity engagement from non-ICA segments. Flag content that attracts high volume but low-quality attention.

2. **Content Efficiency Matrix** — Map every content format against effort-to-produce (low/medium/high) and performance outcome. Identify the highest-ROI content types (high performance, low effort) and eliminate or restructure underperformers (high effort, low performance). Calculate effective cost per engagement by format where production costs are known.

3. **Algorithm Alignment** — Assess whether posting cadence, format mix, content length, and engagement patterns align with current platform algorithm reward signals. Evaluate hook strength (3-second retention for video, scroll-stop rate for static), session-time contribution, and share/save ratios as algorithmic priority signals.

4. **Funnel Integrity** — Trace the audience journey from impression → engagement → profile visit → link click → conversion. Identify the specific stage with the greatest drop-off. Evaluate bio/profile optimisation, CTA clarity, link-in-bio architecture, and content-to-offer coherence at each transition point.

5. **Competitive & Temporal Context** — Benchmark performance against comparable accounts (if provided) or category norms. Identify seasonal, day-of-week, and time-of-day patterns. Detect trend inflection points — is performance accelerating, plateauing, or declining, and from which specific date?

### 3C: Apply FutureProof Personalisation

Layer any user-specific `instructions` from FutureProof context:
- If prior ICA profiles exist, weight the ICA Resonance analysis toward documented audience psychographics and vocabulary
- If previous experiments have been run, compare current metrics against experiment baselines and note whether prior variant recommendations were adopted and their measured impact
- If brand voice or content pillars are stored, evaluate content mix adherence to the documented strategy

## Step 4: Deliver Output

Produce a **Social Media Performance Report** with the following sections:

### 4.1 — Executive Summary
A 3–5 sentence synthesis: overall health assessment, single most important finding, and the recommended strategic priority for the next 30 days.

### 4.2 — Performance Scorecard

| Dimension | Score (1–10) | Trend vs. Prior Period | Priority |
|---|---|---|---|
| ICA Resonance | — | ↑ ↓ → | Critical / Monitor / Strong |
| Content Efficiency | — | ↑ ↓ → | Critical / Monitor / Strong |
| Algorithm Alignment | — | ↑ ↓ → | Critical / Monitor / Strong |
| Funnel Integrity | — | ↑ ↓ → | Critical / Monitor / Strong |
| Competitive Position | — | ↑ ↓ → | Critical / Monitor / Strong |

### 4.3 — Critical Fixes (Top 3 Highest-Impact Actions)

For each fix, provide:
- **The problem**: Specific metric or pattern identified, with exact numbers
- **The root cause**: Why this is happening (not just what)
- **The action**: Precise, executable recommendation — specific hook rewrites, format changes, posting schedule adjustments, CTA language, or audience targeting modifications
- **Expected impact**: Quantified improvement estimate tied to the user's primary objective

### 4.4 — Content Performance Breakdown

A ranked table of content pieces or content categories by the user's primary objective metric, annotated with:
- Top 3 performers: what made them work (specifics, not generalities)
- Bottom 3 performers: what failed and why
- Pattern synthesis: the 2–3 repeatable principles to codify into a content playbook

### 4.5 — 30-Day Action Calendar

A week-by-week tactical plan:
- **Week 1**: Quick wins and fixes to implement immediately
- **Week 2**: Content experiments to launch (tied to Step 5 experiments)
- **Week 3**: Optimisation based on early experiment signals
- **Week 4**: Review cadence and measurement checkpoint

### 4.6 — Metrics Dashboard Template

Provide a recommended weekly tracking template (table format) with the 8–12 KPIs most relevant to the user's stated objective, including calculation formulas and target thresholds based on the analysis.

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
FutureProof:save_experiment(skill="social-media-analytics", experiment={
  hypothesis: "Shifting content mix to 60% high-performing format (identified in analysis) from current ratio will increase engagement rate by measurable margin",
  variants: ["control: current content mix ratio", "variant: 60% [top format] / 25% [second format] / 15% experimental"],
  measurement: "Average engagement rate per post and reach rate over 4-week period, segmented by format",
  expected_impact: "20-30% improvement in average engagement rate, 15% increase in ICA-qualified profile visits"
})
```

```
FutureProof:save_experiment(skill="social-media-analytics", experiment={
  hypothesis: "Adopting the hook patterns from top 3 performing posts across all content will improve scroll-stop and 3-second retention rates",
  variants: ["control: current hook approach", "variant: standardised hook framework derived from top performers"],
  measurement: "3-second video retention rate, carousel first-slide engagement, reach rate per post",
  expected_impact: "25% improvement in average reach rate within 3 weeks"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="social-media-analytics",
  query="Current platform algorithm updates and ranking signal changes for [user's primary platforms] Q3-Q4 2024, including format prioritisation shifts, engagement signal weighting, and distribution model changes",
  reason="Ensure algorithm alignment recommendations reflect the most current platform behaviour rather than outdated heuristics"
)
```

```
FutureProof:request_research(skill="social-media-analytics",
  query="High-performing content frameworks and engagement benchmarks for [user's industry/niche] on [user's primary platforms] 2024, including emerging format adoption rates and ICA attention patterns",
  reason="Calibrate competitive benchmarks and identify format-market fit opportunities the user may be underutilising"
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
FutureProof:save_session(skill="social-media-analytics", session={
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