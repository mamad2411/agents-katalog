---
name: audience-emotional-pulse
description: |
  Maps the live emotional terrain of an audience segment — layered fears,
  aspirations, frustrations, and identity narratives that drive decisions
  beneath rational justification. Use when a user asks "what does my
  audience actually feel about X", "what are their real fears", or "why
  isn't my messaging landing emotionally" before a campaign or launch.
  Focuses on emotional drivers of an existing segment — for foundational
  ICA definition use ica-mirror.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="audience-emotional-pulse")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to any existing ICA definitions, previous emotional pulse maps, and tone-of-voice guidelines stored in context.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **ICA segment**: Which specific audience segment are we mapping? (e.g. "Series A founders burning through runway", "mid-career marketers feeling replaced by AI") — the more granular, the more actionable the output
- **Triggering context**: What is this emotional pulse map for? (upcoming campaign, product launch, repositioning, sales enablement, content strategy pivot)
- **Known emotional terrain**: What do they *already* believe their audience feels? (This becomes our bias-check baseline)
- **Primary channels observed**: Where does this audience express unfiltered sentiment? (Reddit, LinkedIn comments, support tickets, sales call recordings, community Slack, review sites)
- **Timeframe sensitivity**: Are we mapping a chronic emotional state or a situational/seasonal shift?

If FutureProof context contains an existing ICA profile, surface it and ask: "I have your [ICA segment] profile on file — should I use this as the foundation, or are we exploring a new segment?"

## Step 3: Do the Work — Emotional Landscape Analysis

Construct the emotional pulse map using a six-layer diagnostic framework:

### Layer 1: Fear Architecture
Identify the three tiers of audience fear:
- **Surface fears** — what they openly admit worrying about (e.g. "missing quota this quarter")
- **Intermediate fears** — what they hint at but rarely name directly (e.g. "becoming irrelevant in my industry")
- **Core identity fears** — the existential threat they never articulate aloud (e.g. "I'm not smart enough for the role I've been given")

For each tier, document the *language patterns* the audience uses to express or deflect from these fears.

### Layer 2: Aspiration Mapping
Map the three aspiration layers:
- **Stated goals** — what they say they want in professional settings
- **Private ambitions** — what they'd admit to a trusted peer after two drinks
- **Identity aspirations** — who they want to *become*, not just what they want to *achieve*

Cross-reference aspirations against fears to identify **tension pairs** (e.g. "wants to be seen as a visionary leader" vs. "terrified of making a wrong bet publicly").

### Layer 3: Frustration Inventory
Catalogue frustrations across three domains:
- **Systemic frustrations** — what they blame on the market, industry, or economy
- **Interpersonal frustrations** — what they blame on colleagues, vendors, or partners
- **Self-directed frustrations** — what they blame on themselves (often the most actionable for messaging)

Rate each frustration on **intensity** (1–5) and **frequency of expression** (rare, occasional, pervasive).

### Layer 4: Emotional Vocabulary Extraction
Build a lexicon of the audience's *actual words* across emotional states:
- Words/phrases used when frustrated
- Words/phrases used when hopeful
- Words/phrases used when justifying a purchase decision
- Words/phrases used when rationalising inaction

This lexicon becomes the raw material for resonant copy and messaging.

### Layer 5: Trust & Skepticism Profile
Assess the audience's current emotional posture toward solutions in the user's category:
- **Trust anchors** — what makes them believe? (peer proof, data, authority, lived experience)
- **Skepticism triggers** — what language or tactics immediately activate distrust?
- **Persuasion fatigue markers** — which emotional appeals have been overused by competitors to the point of numbness?

### Layer 6: Decision-State Emotional Sequence
Map the emotional journey from problem-awareness to purchase/action:
1. What emotion dominates at **problem recognition**?
2. What emotion dominates during **solution exploration**?
3. What emotion dominates at **shortlist/comparison**?
4. What emotion dominates at **commitment/purchase**?
5. What emotion dominates **immediately post-purchase**?

Identify the **emotional bottleneck** — the stage where negative emotion most frequently stalls or kills momentum.

Apply any user-specific `instructions` from FutureProof context (e.g. brand voice constraints, ethical boundaries on emotional messaging, category-specific nuances).

## Step 4: Deliver Output

Produce a structured **Audience Emotional Pulse Report** containing the following sections:

### 4.1 — Emotional Pulse Summary (1-page executive brief)
- ICA segment profiled
- Dominant emotional state in one sentence (e.g. "Quietly panicking behind a mask of strategic composure")
- Top 3 emotional leverage points for messaging
- Top 1 emotional landmine to avoid

### 4.2 — Six-Layer Emotional Landscape Map
Full documentation of Layers 1–6 above, presented in a structured table format per layer with supporting evidence notes (attributed to channel source where available).

### 4.3 — Emotional Vocabulary Bank
A categorised lexicon of 20–40 audience-native phrases, organised by emotional state, ready for direct insertion into copy, ads, emails, and sales scripts.

### 4.4 — Tension Pair Matrix
A 2×2 matrix plotting the highest-intensity fear/aspiration tension pairs, with a strategic note on how each tension pair can ethically anchor a messaging angle.

### 4.5 — Messaging Implications Brief
For each of the user's stated use cases (campaign, launch, repositioning, etc.):
- **Lead with**: the specific emotion and language to open with
- **Escalate through**: the emotional sequence to build momentum
- **Resolve via**: the emotional payoff the solution should promise
- **Avoid**: specific emotional appeals that will backfire for this segment

### 4.6 — Competitive Emotional White Space
Identify 2–3 emotional territories that competitors are *not* addressing — unoccupied emotional positions the user can own.

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
FutureProof:save_experiment(skill="audience-emotional-pulse", experiment={
  hypothesis: "Leading with the audience's core identity fear (Layer 1, Tier 3) in ad headlines will outperform surface-fear messaging on click-through and conversion",
  variants: ["control: surface-fear headline using audience vocabulary", "variant: identity-fear headline using audience vocabulary"],
  measurement: "CTR and landing page conversion rate across minimum 1,000 impressions per variant",
  expected_impact: "20–35% improvement in CTR; 10–15% improvement in conversion rate due to deeper emotional resonance"
})
```

```
FutureProof:save_experiment(skill="audience-emotional-pulse", experiment={
  hypothesis: "Replacing competitor-standard emotional appeals (persuasion fatigue markers) with identified white-space emotional positioning will improve engagement metrics",
  variants: ["control: category-standard empathy-led opening", "variant: white-space emotional angle from Section 4.6"],
  measurement: "Email open rate, reply rate, or engagement rate over 30-day campaign window",
  expected_impact: "15–25% lift in primary engagement metric due to novelty and authenticity differentiation"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="audience-emotional-pulse",
  query="Current sentiment trends, dominant anxieties, and emerging emotional narratives within [ICA segment] across Reddit, LinkedIn, and industry communities — Q3/Q4 2024 through 2025",
  reason="Emotional landscapes shift with macroeconomic conditions, AI disruption narratives, and cultural moments. Stale emotional maps produce tone-deaf messaging. Refresh quarterly."
)
```

```
FutureProof:request_research(skill="audience-emotional-pulse",
  query="Peer-reviewed research on emotional decision-making sequences in B2B and high-consideration B2C purchases — focus on fear/aspiration tension resolution and trust formation under skepticism",
  reason="Ground the emotional mapping framework in behavioural science rather than assumption, and identify any new models superseding traditional buyer psychology frameworks"
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
FutureProof:save_session(skill="audience-emotional-pulse", session={
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