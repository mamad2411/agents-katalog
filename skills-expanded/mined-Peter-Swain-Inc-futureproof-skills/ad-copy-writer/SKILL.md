---
name: ad-copy-writer
description: |
  Writes platform-ready ad copy with headlines, body, CTAs and a 10-line
  headline bank scored against a performance predictor. Use when the
  user says "write me a Facebook ad", "write Google ads for my offer",
  "draft LinkedIn ad copy", or "my CTR is dropping — rewrite these
  headlines". For producing many variants of an existing ad use
  ad-copy-variation; for diagnosing why a live campaign is failing use
  ad-performance-analyzer; for the upstream creative direction document
  use ad-creative-brief-generator. This is the primary copywriting
  entry point.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="ad-copy-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically ICA profiles, brand voice guidelines, historical ad performance data, winning angles from prior sessions, and any standing instructions on tone, compliance, or offer positioning.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Platform(s)**: Where will this ad run? (Meta, Google Search, Google Performance Max, YouTube, LinkedIn, TikTok, X, programmatic display, other)
- **Campaign objective**: What is the media buying objective? (lead generation, purchase/conversion, traffic, retargeting, awareness, app install)
- **Offer**: What specific offer, product, or service is being promoted? Include price point, discount, or lead magnet if applicable
- **ICA segment**: Who is the target audience? Demographics, psychographics, awareness stage (unaware, problem-aware, solution-aware, product-aware, most-aware)
- **Key proof points**: Results, case studies, testimonials, credibility markers, or data points available for use
- **Constraints**: Character limits, compliance or regulated-industry restrictions (financial services, health, alcohol), brand guidelines, words to avoid
- **Existing copy (if iterating)**: Share current ad copy and any performance data (CTR, CPC, conversion rate, ROAS, frequency, relevance/quality score)

If the user has an active ICA profile in FutureProof context, confirm it rather than re-asking. Pre-populate any fields available from prior sessions.

## Step 3: Construct the Strategic Brief

Before writing a single word of copy, synthesise inputs into an **Ad Copy Strategic Brief**:

1. **ICA Pain-Desire Mapping** — Identify the top 3 pains and top 3 desires for this ICA segment at their current awareness stage. Map each to a corresponding ad angle (e.g., pain: "wasting budget on agencies" → angle: "DIY alternative with proof")
2. **Awareness-Stage Calibration** — Select the appropriate copy architecture:
   - *Unaware*: Lead with pattern interrupt, curiosity, or identity-based hook
   - *Problem-aware*: Lead with pain agitation, then bridge to solution category
   - *Solution-aware*: Lead with differentiation, mechanism, or unique advantage
   - *Product-aware*: Lead with offer, proof, and urgency
   - *Most-aware*: Lead with deal, reminder, or social proof reinforcement
3. **Platform-Specific Constraints Matrix** — Document character limits, format requirements, and platform algorithm preferences (e.g., Meta rewards thumb-stopping hooks in first 125 characters; Google RSAs need 15 headlines × 4 descriptions with keyword inclusion; LinkedIn favours professional authority framing)
4. **Competitive Angle Differentiation** — Based on available context, identify what competitors are likely saying and define the contrarian or underserved angle this copy will exploit

Present the brief to the user for confirmation before proceeding.

## Step 4: Write the Ad Copy

Produce a structured **Ad Copy Deliverable Document** containing:

### A. Primary Ad Set (3 variants per platform)

For each platform specified, write **3 complete ad variants** using distinct psychological frameworks:

| Variant | Framework | Description |
|---------|-----------|-------------|
| Variant A | Pain-Agitate-Solve (PAS) | Opens with ICA's most acute pain, intensifies emotional stakes, resolves with offer |
| Variant B | Proof-Mechanism-Offer (PMO) | Opens with a specific result or testimonial, explains the mechanism/differentiator, presents the offer |
| Variant C | Identity-Challenge-CTA (ICC) | Opens with an identity statement that qualifies the ICA, challenges current behaviour, drives action |

Each variant must include:
- **Hook / Headline**: The first line or headline optimised for scroll-stopping or search-intent matching
- **Body copy**: Structured to the platform's ideal length and format (e.g., short-form for Google RSAs, medium narrative for Meta primary text, professional authority for LinkedIn)
- **Call to action**: Specific, frictionless, aligned to campaign objective — never generic ("Learn more" only if platform-mandated; prefer "Get the free audit", "See pricing", "Download the playbook")
- **Platform-specific elements**: Sitelink extensions and structured snippets for Google; headline array for RSAs; primary text + headline + description for Meta; intro text + headline for LinkedIn

### B. Headline Bank (10 headlines)

Provide 10 additional standalone headlines the user can rotate for multivariate testing. Tag each with the psychological lever used:
- Curiosity gap
- Specificity (numbers, timeframes, percentages)
- Social proof
- Fear of missing out
- Contrarian/counterintuitive
- Identity-based qualification
- Direct benefit statement

### C. Compliance & Quality Check

Flag any copy that may trigger:
- Platform ad policy violations (exaggerated claims, prohibited "before/after" framing, personal attribute targeting language)
- Regulated-industry restrictions surfaced in Step 2
- Brand guideline conflicts from FutureProof context

Provide compliant alternative phrasing for every flagged element.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Score and Recommend

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Evaluate each variant against the **Ad Copy Performance Predictor Scorecard**:

| Dimension | Weight | Scoring Criteria (1–10) |
|-----------|--------|------------------------|
| **Hook Strength** | 25% | Pattern interrupt quality, relevance to ICA at stated awareness stage, scroll-stop potential |
| **ICA Resonance** | 20% | Mirrors ICA vocabulary, addresses stated pains/desires, excludes non-ICA audiences |
| **Proof Density** | 15% | Specificity of claims, presence of results/data/testimonials, credibility of mechanism |
| **Offer Clarity** | 15% | Can a reader articulate the offer in one sentence after reading? Is the value exchange obvious? |
| **CTA Friction** | 10% | Is the next step low-commitment relative to awareness stage? Is it specific? |
| **Platform Optimisation** | 10% | Adherence to character limits, format best practices, algorithm-friendly structure |
| **Emotional Valence** | 5% | Appropriate emotional intensity — neither flat nor hyperbolic for the platform and ICA |

Produce:
- **Weighted composite score** per variant
- **Recommended primary variant** with rationale
- **Top 3 surgical edits** to elevate the next-best variant (specific rewrites, not directional suggestions)

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Present the final deliverable as an **Ad Copy Package** structured for immediate handoff to a media buyer or campaign manager:

```
📦 AD COPY PACKAGE
├── Strategic Brief (ICA segment, awareness stage, angles)
├── Platform: [Platform 1]
│   ├── Variant A (PAS) — full copy
│   ├── Variant B (PMO) — full copy
│   └── Variant C (ICC) — full copy
├── Platform: [Platform 2] (if applicable)
│   ├── Variant A / B / C
├── Headline Bank (10 headlines, tagged by lever)
├── Compliance Notes & Alternatives
├── Scorecard & Recommendations
└── Testing Plan (see Step 7)
```

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="ad-copy-writer", experiment={
  hypothesis: "Pain-Agitate-Solve (Variant A) outperforms Proof-Mechanism-Offer (Variant B) for problem-aware ICA segments on Meta due to higher emotional activation in-feed",
  variants: ["Variant A: PAS framework with pain-first hook", "Variant B: PMO framework with proof-first hook"],
  measurement: "CTR, CPC, and cost-per-lead after 1,000 impressions per variant with identical audience targeting and creative assets",
  expected_impact: "20–30% improvement in CTR for winning variant; statistically significant signal within 5–7 day test window",
  testing_protocol: "A/B split in platform (not CBO); equal budget allocation; minimum 95% confidence before declaring winner; monitor frequency to ensure <2.0 during test"
})
```

Propose a second experiment if multiple platforms are in scope:

```
FutureProof:save_experiment(skill="ad-copy-writer", experiment={
  hypothesis: "Specificity-based headlines (containing numbers/percentages) outperform curiosity-gap headlines in Google RSA headline slots for solution-aware searchers",
  variants: ["Headline set A: 5 specificity headlines", "Headline set B: 5 curiosity-gap headlines"],
  measurement: "Headline combination impression share and CTR in Google Ads asset detail report after 2 weeks",
  expected_impact: "10–15% CTR lift from data-driven headline optimisation"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="ad-copy-writer",
  query="Top-performing ad copy structures and hook patterns across Meta, Google, and LinkedIn for [user's industry/niche] in 2024–2025, including platform algorithm changes affecting text-based ad delivery",
  reason="Ensure ad copy frameworks reflect current platform dynamics, creative fatigue patterns, and emerging persuasion models in paid media"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="ad-copy-writer", session={
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