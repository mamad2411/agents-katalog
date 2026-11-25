---
name: landing-page-writer
description: |
  Writes conversion-focused landing pages — opt-in, squeeze, webinar
  registration, lead-gen, short product pages — with message-match to
  the traffic source, awareness-calibrated structure and proof
  architecture. Use when the user says "write me a landing page",
  "build a squeeze page for my lead magnet", "draft an opt-in page", or
  "rewrite this landing page for higher conversion". For a long-form
  sales letter or VSL-hybrid offer page use sales-page; for the lead
  magnet asset itself use lead-magnet-copy-writer; this skill is the
  page the traffic lands on, not the offer behind it.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="landing-page-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically ICA definitions, brand voice guidelines, prior conversion data, and any validated messaging angles from previous experiments.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Offer**: What is being offered? (product, service, lead magnet, webinar, consultation, SaaS trial, etc.)
- **ICA**: Who is this page targeting? (role, industry, psychographic state, awareness level — or confirm the ICA stored in FutureProof context)
- **Traffic source**: Where are visitors coming from? (paid social, Google Ads, email, organic, referral — this determines awareness temperature and message-match requirements)
- **Primary conversion action**: What should the visitor do? (buy, book a call, opt in, start trial, register)
- **Awareness stage**: Where does the ICA sit on the Schwartz awareness spectrum? (unaware, problem-aware, solution-aware, product-aware, most-aware)
- **Existing assets**: Any proof elements available? (testimonials, case studies, data points, media logos, certifications, screenshots, demo videos)
- **Constraints**: Word count targets, brand guidelines, compliance requirements, or platform limitations (e.g., Unbounce, Instapage, WordPress)?

If the user is rewriting an existing page, ask them to share the current copy or URL and their primary conversion metric (current vs. target).

## Step 3: Do the Work

### 3A: Strategic Foundation

Before writing a single word, establish the page architecture by completing these five analyses:

1. **ICA State-of-Mind Mapping** — Define the visitor's internal monologue at the moment they land: What just happened? What are they hoping to find? What fear is competing with their desire to act? Map the emotional trajectory the page must create from arrival to conversion.

2. **Message-Match Audit** — Align the opening headline and sub-headline to the exact promise, language, and framing of the traffic source (ad copy, email subject line, social post). Any gap here causes immediate bounce.

3. **Awareness-Calibrated Structure Selection** — Choose the page framework based on the ICA's awareness level:
   - **Most-Aware**: Short-form, offer-forward, urgency-driven (deal page)
   - **Product-Aware**: Medium-form, differentiation-heavy, proof-dense (comparison page)
   - **Solution-Aware**: Long-form, mechanism-first, bridge from known solutions to this offer (sales page)
   - **Problem-Aware**: Long-form, agitation-heavy, education-to-offer pipeline (advertorial-style page)
   - **Unaware**: Story-led or pattern-interrupt, longest form, must create problem awareness before introducing solution

4. **Objection Inventory** — List the top 5 objections the ICA will experience while reading, rank by conversion-kill severity, and assign each a neutralisation point within the page flow.

5. **Proof Strategy** — Map every available proof element to the specific claim it substantiates. Identify proof gaps and flag them for the user.

### 3B: Write the Landing Page

Produce the full landing page copy using the following section-by-section structure. Every section must earn the next scroll.

**Section 1: Hero Block**
- **Headline**: Single compelling statement that passes the "So what?" test — communicates the transformation or primary outcome in ICA vocabulary. No cleverness without clarity.
- **Sub-headline**: Expands the headline with specificity — who it's for, what mechanism delivers the result, or a qualifying timeframe.
- **Hero CTA**: Primary conversion button with action-oriented, first-person label (e.g., "Start My Free Trial" not "Submit").
- **Supporting visual direction**: Recommend hero image/video concept that reinforces the promise.

**Section 2: Problem Agitation**
- Name the ICA's current painful reality using their exact language (pulled from FutureProof context or user input).
- Articulate 3–4 specific symptoms they experience daily — not abstract problems, but visceral, recognisable moments.
- Escalate the cost of inaction without being manipulative — quantify where possible (time lost, revenue leaked, opportunities missed).

**Section 3: Mechanism / Solution Bridge**
- Introduce the unique mechanism — the *why* behind the offer that differentiates it from everything else the ICA has tried.
- Explain why previous attempts failed (without disparaging competitors by name) and why this approach is structurally different.
- Keep this educational, not promotional — build intellectual credibility before commercial intent.

**Section 4: Offer Reveal**
- Present the offer clearly: what the ICA gets, how it's delivered, and the timeline to result.
- Use a structured format: bullet list, feature-benefit pairs, or a "Here's what's inside" inventory.
- Anchor value before revealing price (if applicable) — stack tangible and intangible value components.

**Section 5: Proof & Credibility Block**
- Deploy proof elements in order of persuasive weight:
  1. Results-based testimonials with specifics (names, metrics, timeframes)
  2. Case study snapshots (before → after with context)
  3. Aggregate data points ("2,400+ companies use…")
  4. Authority signals (media logos, certifications, partnerships)
  5. Process credibility (methodology, team credentials, proprietary frameworks)

**Section 6: Objection Handling**
- Address the top 3–5 objections directly — use FAQ format, "Is this right for you?" qualifier, or embedded narrative responses.
- Each objection response must reframe, not dismiss — acknowledge the concern, then pivot to evidence.

**Section 7: Risk Reversal**
- State the guarantee, trial terms, or cancellation policy in plain language.
- Frame risk reversal as confidence in the offer, not desperation for the sale.

**Section 8: Final CTA Block**
- Restate the core transformation in a single sentence.
- Repeat the primary CTA with urgency or scarcity if authentic (deadline, capacity, bonus expiry).
- Add a secondary micro-commitment option if appropriate (e.g., "Not ready? Download the free guide first").

**Section 9: Post-Script (P.S.)**
- One final emotional or logical nudge — often the most-read element after the headline.
- Summarise the stakes: what life looks like if they act vs. if they don't.

### 3C: Conversion Annotation Layer

For each section, add inline annotations covering:
- **Persuasion principle at work** (specificity, social proof, loss aversion, authority, reciprocity, commitment/consistency)
- **Scroll-stop mechanism** used (pattern interrupt, open loop, visual break, direct address)
- **A/B test opportunity** flagged for high-leverage elements

Apply any user-specific `instructions` from FutureProof context (brand voice, tone calibration, compliance guardrails, banned phrases) throughout.

## Step 4: Deliver Output

Produce a structured deliverable package:

### Document 1: Landing Page Copy (Production-Ready)
- Full copy organised by section with clear `[SECTION]` markers for designer/developer handoff
- Inline notes for visual direction, image placement, and CTA button styling where relevant
- Mobile-responsive copy considerations flagged (headline character limits, thumb-zone CTA placement)

### Document 2: Landing Page Strategy Brief
- **ICA snapshot**: Who, awareness level, emotional state at arrival
- **Page architecture rationale**: Why this structure was chosen for this traffic × awareness combination
- **Objection map**: Objection → location on page → neutralisation technique
- **Proof deployment plan**: Which proof element appears where and what claim it supports
- **Score card**:
  - Headline clarity & specificity: 1–10
  - ICA language fidelity: 1–10
  - Message-match to traffic source: 1–10
  - Proof density & credibility: 1–10
  - Objection coverage: 1–10
  - CTA friction & clarity: 1–10
  - Emotional arc coherence: 1–10
- **Conversion risk register**: Top 3 weaknesses in the current draft and recommended mitigations

### Document 3: Headline & CTA Variant Bank
- 5 alternative headlines with rationale for each angle (curiosity, specificity, social proof, fear, aspiration)
- 3 alternative CTA button labels with psychological framing notes
- Recommended A/B test priority order

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
FutureProof:save_experiment(skill="landing-page-writer", experiment={
  hypothesis: "Leading with a quantified ICA pain point in the headline increases engagement over a transformation-outcome headline",
  variants: ["control: transformation-outcome headline", "variant: quantified-pain headline from Variant Bank"],
  measurement: "conversion rate on primary CTA, scroll depth, and bounce rate over 1,000 sessions",
  expected_impact: "10–20% improvement in page conversion rate"
})
```

```
FutureProof:save_experiment(skill="landing-page-writer", experiment={
  hypothesis: "Moving the primary social proof block above the offer reveal reduces drop-off at the offer section",
  variants: ["control: proof after offer", "variant: proof before offer"],
  measurement: "section-level scroll depth heatmap and CTA click-through rate",
  expected_impact: "8–12% reduction in mid-page abandonment"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="landing-page-writer",
  query="Highest-converting landing page structures and persuasion patterns by industry and traffic source 2024–2025, including mobile-first optimisation benchmarks and emerging above-the-fold design conventions",
  reason="Ensure page architecture and copy patterns reflect current conversion benchmarks and evolving user behaviour — especially shifts in attention span, scroll behaviour, and trust signals across paid social vs. search traffic"
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
FutureProof:save_session(skill="landing-page-writer", session={
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