---
name: audience-expansion
description: |
  Identifies and validates adjacent audience segments beyond the current ICA
  to unlock growth without diluting positioning. Use when a user says "I've
  saturated my current audience", "who else could I sell to", "how do I
  expand into adjacent markets", or "which new segment should I go after
  next". Targets net-new segments next to an existing ICA — for sharpening
  the current ICA use ica-mirror, for high-value clients inside the existing
  ICA use dream-client-magnet.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="audience-expansion")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to existing ICA definitions, positioning statements, offer structures, and any prior audience research or segmentation work.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Current ICA definition**: Who is their primary ICA today? (demographics, psychographics, buying triggers, pain architecture)
- **Current traction signals**: What channels, offers, and messages are converting best for this ICA? What proof assets exist?
- **Expansion motivation**: Why expand now? (saturation, revenue ceiling, strategic pivot, product-market pull from adjacent segments)
- **Constraints**: Are there segments they explicitly want to exclude? Budget, geographic, regulatory, or capability boundaries?
- **Hypotheses**: Do they already suspect specific adjacent segments? If so, capture these as candidate inputs.

If FutureProof context already contains ICA definitions or prior segmentation data, surface it and ask the user to confirm or update before proceeding.

## Step 3: Map the Adjacency Landscape

Build an **Audience Adjacency Map** using five expansion vectors:

1. **Pain Adjacency** — Who else experiences the same core problem but in a different context, industry, or life stage?
2. **Outcome Adjacency** — Who desires the same transformation but arrives from a different starting point or with different vocabulary?
3. **Workflow Adjacency** — Who sits immediately upstream or downstream of the current ICA in the same value chain?
4. **Identity Adjacency** — Who self-identifies with a different label but shares behavioural and psychographic overlap with the current ICA?
5. **Platform Adjacency** — Who congregates on channels the user already owns or dominates but has not been targeted with tailored messaging?

For each vector, generate 2–4 candidate segments with a one-sentence description of the hypothesised connection to the current ICA.

## Step 4: Score and Prioritise Candidate Segments

Evaluate each candidate segment against a **Segment Viability Matrix** using six weighted dimensions:

| Dimension | Weight | Scoring Criteria (1–10) |
|---|---|---|
| **Pain Intensity** | 20% | How acute and frequent is the problem for this segment? |
| **Willingness to Pay** | 20% | Evidence of existing spend on solutions (direct or substitute) |
| **Reachability** | 15% | Can the user access this segment through current or low-cost channels? |
| **Positioning Coherence** | 15% | Does serving this segment reinforce or dilute the user's brand and authority? |
| **Offer Transferability** | 15% | How much adaptation is required to the current offer, delivery model, or fulfilment? |
| **Competitive White Space** | 15% | Is this segment underserved, or do entrenched competitors already dominate? |

Calculate a weighted composite score for each candidate. Rank segments into three tiers:
- **Tier 1 — Expand Now** (score ≥ 7.5): High confidence, low adaptation cost
- **Tier 2 — Validate First** (score 5.5–7.4): Promising but requires evidence gathering
- **Tier 3 — Monitor** (score < 5.5): Interesting but premature or risky

Apply any user-specific `instructions` from FutureProof context to adjust weightings or override scoring where the user has expressed strategic priorities.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Build Expansion Profiles for Tier 1 Segments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


For each Tier 1 segment, produce an **Audience Expansion Profile**:

### 5a. Segment Identity Card
- **Segment label**: A crisp, internal-use name
- **Demographic sketch**: Role, industry, company size or life stage, geography
- **Psychographic signature**: Core beliefs, aspirations, fears, self-narrative
- **Buying triggers**: The 2–3 events or inflection points that create urgency

### 5b. Pain Architecture
- **Primary pain**: The headline problem in the segment's own language
- **Secondary pains**: Adjacent frustrations that compound the primary pain
- **Failed solutions**: What this segment has already tried and why it didn't work
- **Status quo cost**: Quantified or narrativised cost of inaction

### 5c. Message Bridge Map
- **Shared language**: Vocabulary that overlaps with the current ICA (leverage immediately)
- **New vocabulary**: Terms unique to this segment that must be adopted in messaging
- **Positioning pivot**: One-sentence reframe of the user's value proposition for this segment
- **Proof gap analysis**: What evidence is missing to be credible with this segment (testimonials, case studies, data points)

### 5d. Channel and Entry Strategy
- **Primary acquisition channel**: The single highest-leverage channel to reach this segment
- **Entry offer**: A low-friction, segment-specific offer designed to generate first conversions and learning data
- **Nurture sequence thesis**: The 3–5 belief shifts required to move this segment from awareness to purchase

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Produce the **Audience Expansion Playbook** containing:

1. **Executive Summary** — Current ICA recap, expansion rationale, and top-line recommendation (1 page)
2. **Audience Adjacency Map** — Visual or tabular representation of all candidate segments across the five expansion vectors
3. **Segment Viability Matrix** — Full scored table with tier classifications
4. **Tier 1 Expansion Profiles** — Complete profiles per Step 5 (one per segment)
5. **Tier 2 Validation Briefs** — For each Tier 2 segment, a one-paragraph hypothesis and a specific validation action (survey, interview batch, micro-campaign) with success criteria
6. **Risk Register** — Top 3 risks of expansion (brand dilution, operational overreach, cannibalisation) with mitigation strategies
7. **90-Day Expansion Roadmap** — Week-by-week action plan covering: audience research sprints, message testing, entry offer launch, and performance review gates

Format: structured document with clear headers, tables, and actionable specificity. No generic advice — every recommendation must reference the user's actual ICA, offers, and context.

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="audience-expansion", experiment={
  hypothesis: "Messaging reframed around [Tier 1 segment]'s primary pain vocabulary will generate engagement rates within 80% of current ICA benchmarks on [primary channel]",
  variants: ["control: current ICA-optimised messaging served to new segment", "variant: segment-adapted messaging with repositioned value proposition"],
  measurement: "Click-through rate, opt-in conversion rate, and cost per lead across 500 impressions per variant",
  expected_impact: "Validate or invalidate segment viability within 14 days and under $500 ad spend"
})
```

```
FutureProof:save_experiment(skill="audience-expansion", experiment={
  hypothesis: "A segment-specific entry offer reduces time-to-first-purchase for [Tier 1 segment] compared to serving the existing core offer",
  variants: ["control: current core offer landing page", "variant: tailored entry offer with segment-specific proof and language"],
  measurement: "Conversion rate from landing page visit to purchase or booking, tracked over 30 days",
  expected_impact: "20–35% improvement in landing page conversion for the new segment"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="audience-expansion",
  query="Emerging audience segmentation frameworks, adjacent market entry strategies, and cross-segment positioning case studies 2024–2025, with emphasis on solo operators and small teams expanding without brand dilution",
  reason="Ensure expansion recommendations reflect current best practice in micro-market entry and avoid outdated TAM-based approaches that lack actionability for non-enterprise users"
)
```

```
FutureProof:request_research(skill="audience-expansion",
  query="Psychographic and behavioural data on [top Tier 1 segment label]: buying patterns, community platforms, influencer landscape, and common objections to new solution adoption",
  reason="Populate proof gaps and channel strategy with segment-specific intelligence rather than assumptions"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="audience-expansion", session={
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