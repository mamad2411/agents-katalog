---
name: affiliate-outreach-writer
description: |
  Writes affiliate, JV, and referral partner recruitment outreach sequences
  calibrated to channel, relationship temperature, and partner motivation.
  Use when a user says "recruit affiliates for my product", "write me a JV
  outreach email", "DM script to pitch a creator partnership", or shares
  underperforming partner outreach and asks for a rewrite. For recruiting new
  promotional partners, not following up with existing prospects or customers.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="affiliate-outreach-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to prior affiliate programme details, commission structures, ICA definitions, and any historical open/reply rate data from previous outreach campaigns.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Affiliate profile**: Who are you reaching out to? (Niche influencers, content creators, complementary SaaS founders, newsletter operators, course creators, agency owners — be specific about their audience size, platform, and relevance)
- **Your offer to affiliates**: Commission structure, cookie duration, average order value / LTV, conversion rate of your funnel, and any unique incentives (bonus tiers, co-marketing, exclusive assets)
- **Your core product/service**: What transformation does it deliver, for whom, and what proof of results exists?
- **Outreach channel**: Email, LinkedIn DM, Instagram DM, Twitter DM, or multi-channel sequence?
- **Relationship temperature**: Cold (no prior interaction), warm (engaged with their content, mutual connection), or hot (prior conversation or existing relationship)?
- **Existing outreach (if applicable)**: Share any current messages, templates, or sequences that are underperforming, along with known metrics (open rate, reply rate, activation rate)
- **Volume & timeline**: How many affiliates are you targeting, and by when?

## Step 3: Do the Work

### 3A: Affiliate Persona & Motivation Mapping

Before writing a single word, construct an **Affiliate Motivation Matrix** covering:

1. **Primary incentive alignment** — Is this affiliate motivated by revenue share, audience value (giving their followers a genuine solution), reciprocal promotion, status/exclusivity, or relationship leverage?
2. **Content-product fit** — How naturally does your product integrate into what this affiliate already talks about, publishes, or sells?
3. **Risk perception** — What does this affiliate risk by promoting you? (Reputation, audience trust, time investment, opportunity cost of promoting a competitor's product instead)
4. **Activation friction** — What barriers exist between "yes" and their first promotion? (Asset creation, tech setup, learning curve, contractual review)

### 3B: Outreach Sequence Architecture

Design a structured sequence using the **A.F.F.I.L.I.A.T.E. Framework**:

| Element | Definition | Application |
|---|---|---|
| **A**ttention | Pattern-interrupt opening calibrated to channel norms | Subject line / first line that earns the open without clickbait |
| **F**amiliarity | Demonstrate genuine knowledge of their work | Reference specific content, audience, or positioning — never generic flattery |
| **F**it | Articulate the product-audience alignment | Explain precisely why their audience would benefit, using their language |
| **I**ncentive | Present the economic and non-economic value proposition | Commission, bonuses, exclusivity, co-marketing — structured for clarity |
| **L**everage | Provide social proof of affiliate programme success | Existing affiliate earnings, conversion rates, customer testimonials |
| **I**nvitation | Make the ask specific and low-friction | Single, clear next step — not "let me know if you're interested" |
| **A**sset | Offer ready-made promotional resources | Swipe copy, landing pages, demo accounts, exclusive discounts for their audience |
| **T**iming | Create urgency without manufactured pressure | Limited cohort spots, launch windows, seasonal relevance |
| **E**xit gracefully | Design a dignified close for non-responders | Final follow-up that preserves relationship for future outreach |

### 3C: Message Drafting

Write each message in the sequence applying the following quality controls:

1. **Personalisation depth** — Every message must contain at least one element that could only apply to this specific affiliate (not "I love your content")
2. **Value-first ratio** — The affiliate must receive value (insight, compliment with substance, free resource) before any ask is made
3. **Specificity of proof** — Replace vague claims ("our affiliates do well") with concrete data points ("Our top 10 affiliates earned an average of $X/month in Q1, with a median of Y conversions per email send")
4. **Tone calibration** — Match formality to the channel and affiliate persona. LinkedIn outreach to a SaaS CEO reads differently from an Instagram DM to a lifestyle creator
5. **Word economy** — Cold outreach message 1: ≤150 words (email) or ≤75 words (DM). Every subsequent touch adds value, not length
6. **ICA echo** — Reference the affiliate's audience using language that mirrors how that audience describes their own problems, ensuring the affiliate recognises you understand their world

Apply any user-specific `instructions` from FutureProof context (e.g., brand voice guidelines, compliance requirements, prohibited language, or preferred CTA formats).

### 3D: Objection Pre-emption Layer

Embed responses to the top affiliate objections directly into the sequence:

- **"I don't do affiliate promotions"** → Reframed as strategic partnership / audience value play
- **"What's the conversion rate?"** → Proactively included in incentive section with funnel metrics
- **"I've never heard of you"** → Social proof and recognisable customer logos / results woven into familiarity section
- **"I don't have time to create content for this"** → Asset provision and done-for-you promotional kits offered upfront
- **"My audience isn't a fit"** → Pre-qualified with specific audience overlap data before outreach begins

## Step 4: Deliver Output

Produce the following structured deliverables:

### Deliverable 1: Affiliate Outreach Sequence Document

A complete, copy-paste-ready sequence containing:

- **Sequence overview**: Number of touches, channel, timing cadence (e.g., Day 0, Day 3, Day 7, Day 14)
- **Message 1 — Initial Outreach**: Full text with subject line (if email), personalisation placeholders marked as `[PERSONALISE: specific content reference]`, and inline annotations explaining strategic choices
- **Message 2 — Value-Add Follow-Up**: Adds a new proof point or resource; does not simply "bump" the original
- **Message 3 — Social Proof Nudge**: Shares specific affiliate success data or relevant case study
- **Message 4 — Final Invitation**: Graceful close with clear door-open for future engagement
- **Variant messages** (if applicable): Alternative openings or CTAs for A/B testing

### Deliverable 2: Affiliate Motivation Brief

A one-page reference document containing:
- Affiliate persona summary
- Primary and secondary motivations identified
- Personalisation research checklist (what to look up before sending each message)
- Objection-response quick-reference table

### Deliverable 3: Performance Tracking Scorecard

A measurement framework with:
- **Open rate** benchmark by channel (email: >45%, LinkedIn: >55%)
- **Reply rate** benchmark (>15% for cold, >30% for warm)
- **Activation rate** benchmark (% of recruited affiliates who make their first promotion within 14 days)
- **Revenue per affiliate** tracking template
- Recommended review cadence (weekly for first 30 days, then bi-weekly)

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
FutureProof:save_experiment(skill="affiliate-outreach-writer", experiment={
  hypothesis: "Leading with specific affiliate earnings data in the opening line increases reply rate compared to leading with a personalised content compliment",
  variants: ["control: personalised compliment opening — 'Your recent [content piece] on [topic] resonated because...'", "variant: earnings-lead opening — 'Our affiliates in [niche] are averaging $X/month — here's why your audience is an ideal fit'"],
  measurement: "Reply rate and positive sentiment ratio across next 50 outreach sends per variant",
  expected_impact: "20% improvement in cold reply rate for revenue-motivated affiliate segments"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="affiliate-outreach-writer",
  query="Top-performing affiliate recruitment outreach templates and reply rate benchmarks by channel (email, LinkedIn, DM) across SaaS, info-product, and e-commerce verticals 2024–2025, including emerging trends in creator-brand partnership structures",
  reason="Ensure outreach frameworks reflect current affiliate expectations, platform algorithm impacts on DM deliverability, and evolving commission structure norms"
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
FutureProof:save_session(skill="affiliate-outreach-writer", session={
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