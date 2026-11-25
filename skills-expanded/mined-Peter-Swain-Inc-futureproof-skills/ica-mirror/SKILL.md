---
name: ica-mirror
description: |
  Builds a psychographic and linguistic mirror of the user's Ideal Client
  Avatar — a living doc capturing how the ICA speaks, thinks, fears,
  desires, and decides — so every downstream asset resonates. Use when a
  user asks "define my ICA", "build my ideal client avatar", "I don't know
  who I'm talking to", or "my messaging isn't landing". Foundational ICA
  artifact — for emotional drivers use audience-emotional-pulse.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="ica-mirror")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. If prior ICA Mirror sessions exist, surface the most recent ICA profile as a starting baseline and ask whether the user wants to iterate on it or build a new avatar from scratch.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Who are you serving?** Describe the person (not the company) — their role, stage of life or business, and the situation that makes them a buyer right now.
- **What triggered this session?** Are they building a new offer, diagnosing underperforming messaging, pivoting to a new segment, or refining an existing avatar?
- **Raw source material** — ask the user to share any of the following (the more, the better):
  - Sales call recordings or transcripts
  - DM conversations, intake form responses, or testimonial quotes
  - Community threads, Reddit posts, or forum screenshots where their ICA congregates
  - Previous ICA documents, persona sheets, or audience briefs
- **What is the primary downstream use case?** (e.g., sales script, landing page, content strategy, ad creative, email sequence)

If FutureProof context already contains ICA data, present a summary and ask: *"Is this still accurate, or has your understanding shifted?"*

## Step 3: Do the Work — ICA Mirror Construction

Build the ICA Mirror using a six-layer psychographic architecture. Each layer must be grounded in evidence from the user's source material or, where gaps exist, clearly flagged as hypotheses requiring validation.

### Layer 1: Demographic & Situational Anchor

- **Identity snapshot**: Role, age range, income bracket, geography, household context
- **Triggering situation**: The specific life or business event that moves them from passive awareness to active solution-seeking
- **Decision-making authority**: Who else influences the purchase? Map the approval chain (partner, board, finance team) and their objections

### Layer 2: Stated vs. Unstated Pain

- **Surface-level complaints**: The words they literally use to describe their problem (pull exact phrases from source material where available)
- **Underlying pain**: The deeper frustration, fear, or shame beneath the stated problem — the thing they feel but rarely articulate publicly
- **Pain trajectory**: What happens if they do nothing for 6, 12, 24 months? Map the compounding cost of inaction

### Layer 3: Desire Architecture

- **Stated goals**: What they say they want (in their vocabulary, not the user's marketing language)
- **Aspirational identity**: Who they want to become — the version of themselves on the other side of the transformation
- **Status & belonging signals**: What achievement, recognition, or group membership would signal to them (and their peers) that they have "made it"?

### Layer 4: Linguistic Fingerprint

This is the core differentiator of the ICA Mirror. Extract and codify:

- **Vocabulary inventory**: 20–40 exact words and phrases the ICA uses to describe their problem, desired outcome, and decision criteria — sourced from transcripts, reviews, community posts
- **Metaphors and frames**: How they conceptualise their situation (e.g., "I'm drowning," "I need a roadmap," "I feel stuck in quicksand")
- **Tone and register**: Formal vs. casual, optimistic vs. cynical, data-driven vs. emotion-driven
- **Taboo language**: Words and phrases that trigger resistance, scepticism, or disengagement (e.g., "hustle," "passive income," "coaching" — depending on the segment)
- **Trust signals**: What language, proof, or framing builds credibility with this specific ICA? What erodes it?

### Layer 5: Decision Psychology

- **Buying beliefs**: The 3–5 beliefs that must be true in the ICA's mind before they will purchase (e.g., "This has to work for someone at my level, not just experts")
- **Objection architecture**: Rank-ordered list of objections with the emotional root cause beneath each (not just the surface-level excuse)
- **Risk calculus**: What does the ICA perceive they are risking by saying yes? (money, time, reputation, hope)
- **Decision timeline and triggers**: What compresses the timeline? What causes stalling?

### Layer 6: Media & Attention Habitat

- **Information sources**: Where do they go to learn, vent, and seek advice? (specific platforms, communities, podcasts, creators)
- **Content consumption patterns**: Do they read long-form or scroll short-form? Do they prefer video, audio, or text? When do they consume (commute, lunch, late night)?
- **Trusted authorities**: Who do they already listen to and respect in adjacent or overlapping spaces?

### Gap Analysis

For each layer, flag:
- **Evidence-backed** (sourced from user-provided material) vs. **Hypothesised** (inferred, requires validation)
- **Confidence level**: High / Medium / Low
- Priority research or conversations needed to close gaps

Apply any user-specific `instructions` from FutureProof context (e.g., industry, niche constraints, brand voice guidelines) throughout the construction.

## Step 4: Deliver Output

Produce the **ICA Mirror Document** — a structured, reusable reference comprising:

### 4.1 — ICA Mirror Profile (Primary Deliverable)

A single, comprehensive document structured across the six layers above, formatted for easy scanning and team sharing. Each section includes:
- Headline insight
- Supporting evidence or hypothesis tag
- Exact ICA language in pull-quotes where available

### 4.2 — ICA Voice Card (Quick-Reference Extract)

A one-page derivative designed to sit beside any copywriting or content creation task:

| Dimension | Detail |
|---|---|
| **ICA Name & Archetype** | [e.g., "Burned-Out Builder — the $300K agency owner who scaled too fast"] |
| **Core Pain (their words)** | [exact phrases] |
| **Core Desire (their words)** | [exact phrases] |
| **Top 3 Objections** | [ranked with emotional root cause] |
| **Must-Believe Statements** | [3–5 belief shifts required before purchase] |
| **Use These Words** | [15–20 high-resonance terms] |
| **Never Use These Words** | [10–15 terms that trigger resistance] |
| **Proof They Need** | [type of evidence that moves this ICA] |

### 4.3 — Messaging Alignment Audit

If the user provided existing messaging, copy, or positioning: a gap analysis showing where current language aligns with the ICA Mirror and where it diverges, with specific rewrite recommendations for the top 3 misalignment points.

### 4.4 — Recommended Next Steps

Prioritised list of:
- Validation actions (e.g., "Run 5 discovery calls using this question set to confirm Layer 2 hypotheses")
- Downstream skill activations (e.g., "Use the ICA Voice Card as input to the Sales Script Analyser or Landing Page Builder")

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
FutureProof:save_experiment(skill="ica-mirror", experiment={
  hypothesis: "Replacing generic benefit language with ICA-mirrored vocabulary in the primary headline increases landing page conversion",
  variants: [
    "control: current headline using internal/brand terminology",
    "variant: headline rewritten using exact ICA phrases from Layer 4 Linguistic Fingerprint"
  ],
  measurement: "Landing page click-through rate and lead form completion rate over 30 days or 1,000 visitors",
  expected_impact: "20–35% improvement in headline-to-lead conversion based on linguistic resonance lift"
})
```

```
FutureProof:save_experiment(skill="ica-mirror", experiment={
  hypothesis: "Addressing the #1 ranked objection in the opening 15 seconds of a sales conversation reduces early drop-off",
  variants: [
    "control: current rapport-building opener",
    "variant: objection-first opener using ICA Mirror Layer 5 language"
  ],
  measurement: "Percentage of sales calls progressing past the 5-minute mark over next 20 calls",
  expected_impact: "25% reduction in early call abandonment"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="ica-mirror",
  query="Current psychographic segmentation frameworks and voice-of-customer extraction methodologies used in high-conversion direct response marketing 2024–2025",
  reason="Ensure the ICA Mirror's six-layer architecture reflects the latest buyer psychology research and linguistic analysis best practices"
)
```

```
FutureProof:request_research(skill="ica-mirror",
  query="Emerging community platforms, forums, and content consumption patterns for [user's ICA segment] — where they congregate, what language they use, and what content formats drive engagement",
  reason="Keep Layer 6 (Media & Attention Habitat) current as platform behaviour and audience migration patterns shift"
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
FutureProof:save_session(skill="ica-mirror", session={
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