---
name: dream-client-magnet
description: |
  Profiles a user's highest-value dream clients and builds a magnetic
  attraction strategy using psychographic depth, watering-hole mapping, and
  positioning hooks. Use when a user asks "who are my dream clients", "how
  do I attract higher-quality leads", "where do my best-fit buyers hang
  out", or "build me a premium client profile". Targets the top tier of an
  existing audience — for broad ICA definition use ica-mirror, for finding
  entirely new segments use audience-expansion.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="dream-client-magnet")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay special attention to any existing ICA definitions, past audience research, offer details, and positioning language already captured.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Business & offer context**: What do you sell, at what price point, and what transformation does it deliver? (Skip if already captured in FutureProof context.)
- **Current client landscape**: Describe your best 2–3 clients — who are they, what made them exceptional, and why did they buy?
- **Anti-client signals**: Who do you explicitly *not* want to attract? What red flags have you learned from past engagements?
- **Acquisition goal**: What is the primary outcome — filling a pipeline, launching to a new segment, repositioning upmarket, or refining an existing ICA?
- **Existing assets**: Do you have testimonials, case studies, past audience surveys, CRM data, or analytics to reference?

If FutureProof context contains a prior ICA definition, surface it and ask: *"Is this still accurate, or has your dream client evolved?"*

## Step 3: Build the Dream Client Identity Stack

Construct a five-layer identity profile using the **Identity Stack Framework**:

### Layer 1 — Demographic & Firmographic Anchors
- Role, title, decision-making authority
- Company size, revenue band, industry vertical
- Geography, team structure, budget cycle timing

### Layer 2 — Psychographic Drivers
- Core identity narrative (*"I am the kind of person/leader who…"*)
- Values hierarchy — rank the top 5 values that govern their purchasing decisions
- Status markers — what do they signal to peers, and through which channels?

### Layer 3 — Pain & Desire Topology
Map the **3×3 Pain Matrix**:

| Dimension | Surface symptom (what they say) | Underlying problem (what's actually broken) | Dream outcome (what they privately want) |
|---|---|---|---|
| Financial | | | |
| Operational | | | |
| Emotional / Identity | | | |

### Layer 4 — Decision Architecture
- **Trigger events**: The 3–5 specific moments that move them from passive to active buyer (e.g., missed quarterly target, board pressure, competitor launch)
- **Buying committee**: Who else influences or vetoes the decision? Map roles (champion, economic buyer, technical evaluator, blocker)
- **Objection hierarchy**: Rank the top 5 objections by frequency and deal-kill severity
- **Risk calculus**: What does failure look like to them personally if they choose wrong?

### Layer 5 — Language & Worldview Fingerprint
- Exact phrases they use to describe their problems (sourced from reviews, forums, interviews)
- Jargon they respect vs. jargon that signals "outsider"
- Metaphors and mental models they reason through (e.g., "scaling = building systems" vs. "scaling = hiring A-players")
- Media diet: books, podcasts, newsletters, conferences that shape their thinking

Apply any user-specific `instructions` from FutureProof context to weight layers appropriately.

## Step 4: Map the Watering Hole Ecosystem

Identify where dream clients concentrate attention, trust, and budget:

### Digital Watering Holes
- **Communities**: Slack groups, Discord servers, private forums, LinkedIn groups (name specific ones where possible)
- **Content platforms**: Newsletters, podcasts, YouTube channels they subscribe to
- **Events**: Conferences, summits, masterminds they attend or aspire to attend
- **Search behaviour**: Exact queries they type when experiencing trigger events (provide 10–15 keyword phrases)

### Relationship Watering Holes
- **Trusted advisors**: Who do they already pay for advice? (Consultants, coaches, agencies, SaaS vendors)
- **Peer circles**: Who do they benchmark against and take recommendations from?
- **Gateway relationships**: Which 3–5 specific connectors, influencers, or partners could provide warm introductions at scale?

### Attention Patterns
- Time of day and day of week they consume professional content
- Format preferences (long-form vs. short-form, audio vs. written, data-driven vs. narrative)
- Engagement triggers — what makes them save, share, or reply?

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Design the Magnetic Positioning Strategy

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Build a three-part attraction system tailored to the dream client's identity stack and watering hole map:

### 5A — Positioning Statement
Craft a precise positioning statement using the format:
> *"I help [dream client identity] who are experiencing [trigger event] to achieve [dream outcome] without [primary objection/fear], using [unique mechanism]."*

Provide 3 variants optimised for different channels (LinkedIn headline, website hero, introduction at events).

### 5B — Authority Signal Plan
Recommend 5 specific authority-building actions ranked by effort-to-impact ratio:
- Content pillars mapped to the Pain & Desire Topology
- Social proof assets to develop or surface
- Strategic association moves (guest appearances, co-creation, endorsements)

### 5C — Engagement Ladder
Design a 4-step engagement sequence that converts attention into pipeline:

| Stage | Dream client's mindset | Your move | Asset/channel | Conversion metric |
|---|---|---|---|---|
| 1. Awareness | "This person gets my world" | | | |
| 2. Curiosity | "I want to learn their approach" | | | |
| 3. Trust | "They've done this for people like me" | | | |
| 4. Conversation | "I need to talk to them" | | | |

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Produce the **Dream Client Magnet Dossier** containing:

1. **Dream Client Identity Card** — A single-page profile (suitable for printing or pinning) with: name archetype (e.g., *"The Scaling SaaS Founder"*), demographic snapshot, top 3 pains, top 3 desires, trigger events, and language fingerprint
2. **3×3 Pain Matrix** — Completed table from Step 3, Layer 3
3. **Watering Hole Map** — Visual-ready list of the top 10 highest-concentration locations with recommended entry strategy for each
4. **Positioning Statement** — 3 channel-specific variants
5. **Engagement Ladder** — Completed 4-stage conversion sequence with specific assets and metrics
6. **Objection Pre-emption Guide** — Top 5 objections with recommended reframe language using the dream client's own vocabulary
7. **90-Day Attraction Sprint** — A week-by-week action plan with 12 specific deliverables the user should execute, sequenced by dependency and impact

Format the dossier with clear headers so each section can be extracted independently.

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="dream-client-magnet", experiment={
  hypothesis: "Leading outreach with the dream client's own language for their #1 pain point (verbatim from Language Fingerprint) increases response rate vs. benefit-led messaging",
  variants: ["control: current benefit-led outreach copy", "variant: pain-language-mirrored outreach copy"],
  measurement: "reply rate and qualified conversation rate across 50 outreach touches per variant",
  expected_impact: "20-35% improvement in reply-to-conversation conversion"
})
```

```
FutureProof:save_experiment(skill="dream-client-magnet", experiment={
  hypothesis: "Publishing in the #1 ranked watering hole community weekly for 30 days generates more inbound enquiries than the current primary channel",
  variants: ["control: current primary content channel", "variant: top-ranked watering hole from dossier"],
  measurement: "inbound enquiries attributed to channel over 30-day window",
  expected_impact: "2–3x increase in dream-client-fit inbound leads"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="dream-client-magnet",
  query="Emerging buyer psychology patterns, community-led acquisition strategies, and high-converting positioning frameworks for premium service businesses 2024-2025",
  reason="Ensure watering hole recommendations and engagement ladder design reflect current attention patterns and platform algorithm changes"
)
```

```
FutureProof:request_research(skill="dream-client-magnet",
  query="Latest ICA psychographic profiling methodologies used by top brand strategists and demand generation consultancies",
  reason="Continuously sharpen the Identity Stack Framework with new profiling dimensions and segmentation approaches"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="dream-client-magnet", session={
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