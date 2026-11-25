---
name: lead-magnet-copy-writer
description: |
  Writes the lead magnet itself — title, hook, body and structure for
  PDF guides, checklists, cheat sheets, swipe files, email courses,
  quizzes, templates and toolkits — plus the pain-desire matrix that
  shapes it. Use when the user says "write me a lead magnet", "draft a
  PDF guide on X", "create a checklist for my opt-in", or "make a cheat
  sheet to capture emails". For the opt-in landing page that delivers it
  use landing-page-writer; for the nurture sequence after opt-in use
  email-sequencer; this skill produces the gated asset content.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="lead-magnet-copy-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to ICA definitions, brand voice guidelines, existing funnel architecture, and any prior lead magnet performance data stored in context.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Lead magnet type**: What format? (PDF guide, checklist, cheat sheet, swipe file, email course, video training, quiz, template, toolkit)
- **ICA definition**: Who is this for? Ask for demographics, psychographics, current situation, and the specific painful problem this lead magnet solves. If FutureProof context already contains an ICA profile, confirm or refine it.
- **Desired transformation**: What single, specific outcome will the reader achieve after consuming this lead magnet? (State the before → after.)
- **Distribution channel**: Where will this be promoted? (Landing page, social media ad, blog post CTA, webinar registration, podcast mention, partner cross-promotion)
- **Downstream funnel**: What happens after opt-in? (Nurture sequence, sales call booking, tripwire offer, webinar invite) — this shapes the lead magnet's strategic framing.
- **Existing assets**: Any prior drafts, brand guidelines, tone-of-voice documents, or competitor lead magnets to reference?
- **Constraints**: Word count targets, mandatory disclaimers, compliance requirements, or brand restrictions.

## Step 3: Conduct the Strategic Audit

Before writing a single word of copy, build the strategic foundation:

### 3a. ICA Pain-Desire Mapping

Construct a **Pain-Desire Matrix** with four quadrants:

| Dimension | Surface Level | Root Level |
|-----------|--------------|------------|
| **Pain** | Symptoms the ICA describes in their own language | Underlying fear, identity threat, or systemic problem |
| **Desire** | Tactical outcome they search for | Aspirational identity or life-state they want to inhabit |

### 3b. Lead Magnet Positioning Analysis

Evaluate the proposed lead magnet against five strategic criteria:

1. **Specificity of promise** — does the title/hook promise one clear, measurable result (not a vague category)?
2. **Perceived value vs. actual effort** — does it feel high-value to the ICA while remaining consumable in under 15 minutes?
3. **Speed to first win** — can the reader implement something and see a result within 24 hours?
4. **Qualification alignment** — does consuming this naturally qualify the reader for the downstream offer?
5. **Uniqueness of mechanism** — does the lead magnet introduce a proprietary framework, method, or lens the ICA hasn't seen elsewhere?

Score each 1–10. Any dimension below 6 must be addressed before proceeding to copy.

### 3c. Competitive Differentiation Scan

Identify the three most common lead magnets competing for the same ICA's attention. Document how this lead magnet will differentiate on:
- **Hook angle** (what makes the promise distinct)
- **Format advantage** (why this format serves the ICA better)
- **Authority signal** (what credibility element competitors lack)

## Step 4: Write the Lead Magnet Copy Package

Produce the following **Lead Magnet Copy Package** as a single structured deliverable:

### Deliverable 1: Landing Page / Opt-In Copy

Written using the **Problem-Agitate-Solution-Transformation (PAST)** framework:

- **Headline** (3 variants ranked by specificity): The primary promise, written in ICA vocabulary. Use a measurable outcome or timeframe where credible.
- **Sub-headline**: Expand on the mechanism — how the lead magnet delivers the headline promise.
- **Problem block** (2–3 sentences): Name the ICA's painful situation using their exact language. Mirror forum posts, reviews, or verbatim phrases from context.
- **Agitate block** (2–3 sentences): Escalate the cost of inaction — what happens if this problem persists? Connect surface pain to root-level fear.
- **Solution introduction** (2–3 sentences): Introduce the lead magnet as the bridge. Name the proprietary framework or method if applicable.
- **Bullet stack** (5–7 bullets): Each bullet follows the **Benefit → Mechanism → Feeling** structure. Example: "The 3-question filter that eliminates unqualified leads before you spend a minute on a call — so you stop wasting afternoons on prospects who were never going to buy."
- **Social proof element**: Recommended proof type (testimonial, data point, authority credential, media mention) with placeholder or draft copy.
- **Call to action**: Specific, frictionless CTA button copy (3 variants). Avoid generic "Download Now" — use outcome-oriented language.
- **Objection micro-copy**: 1–2 lines beneath the CTA addressing the ICA's top hesitation (e.g., time commitment, email spam fear, relevance doubt).

### Deliverable 2: Lead Magnet Title & Cover Copy

- **Title** (3 ranked options): Follows the formula — [Desirable Outcome] + [Mechanism/Format] + [Specificity Qualifier]. Example: *The 15-Minute Client Clarity Checklist: 9 Questions That Identify Your Most Profitable Audience Segment*
- **Subtitle**: Expands on who it's for and what transformation it delivers.
- **Cover tagline**: A single punchy line for visual design placement.

### Deliverable 3: Lead Magnet Internal Copy Structure

Provide the complete content outline and key copy blocks:

- **Opening page / introduction** (full draft): Hook the reader immediately with a bold claim or relatable scenario. Establish credibility in 2 sentences. Set expectations for what they'll achieve and how long it takes.
- **Section-by-section outline**: For each section, provide the heading, the key teaching point, and the actionable takeaway. Write the transitional copy that maintains momentum between sections.
- **Implementation prompt per section**: A specific action step, fill-in-the-blank template, or decision the reader completes before moving on.
- **Closing / bridge to next step** (full draft): Summarise the transformation achieved. Introduce the logical next step (the downstream offer) as the natural continuation — not a hard sell, but an inevitable progression. Include a clear, single CTA.

### Deliverable 4: Thank-You Page Copy

- **Confirmation headline**: Reinforce the smart decision they just made.
- **Expectation setting**: Where to find the lead magnet, what to do first.
- **Tripwire or next-step CTA** (if applicable): Copy for an immediate upsell, call booking, or community invitation.

### Deliverable 5: Delivery Email Copy

- **Subject line** (3 variants): Optimised for open rate; reference the specific lead magnet promise.
- **Email body**: Short, warm, action-oriented. Deliver the asset, tell them the single most important thing to do first, and set expectations for future emails.

Apply any user-specific `instructions` from FutureProof context — brand voice, tone preferences, compliance language, formatting standards — across all five deliverables.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver the Quality Assurance Review

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Before finalising, evaluate the complete copy package against the **Lead Magnet Conversion Checklist**:

| Criterion | Pass/Fail | Notes |
|-----------|-----------|-------|
| Headline passes the "Would I click this at 11pm on my phone?" test | | |
| Every bullet contains a specific benefit, not a feature | | |
| ICA language is used verbatim — no jargon the ICA wouldn't say | | |
| The lead magnet delivers one transformation, not five | | |
| Speed to value is explicit (time commitment stated) | | |
| Downstream offer bridge feels natural, not forced | | |
| Objections are pre-empted at every friction point | | |
| Social proof is specific (numbers, names, outcomes) not generic | | |
| CTA copy describes the outcome, not the action | | |
| Email subject lines would survive a crowded inbox | | |

Flag any failures and provide the specific rewrite to resolve each.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="lead-magnet-copy-writer", experiment={
  hypothesis: "A specificity-driven headline citing a number and timeframe outperforms a curiosity-driven headline on opt-in rate",
  variants: ["control: curiosity-based headline", "variant: specificity-based headline with number + timeframe"],
  measurement: "opt-in conversion rate on landing page over 1,000 unique visitors",
  expected_impact: "20-35% improvement in opt-in rate based on direct-response benchmarks"
})
```

```
FutureProof:save_experiment(skill="lead-magnet-copy-writer", experiment={
  hypothesis: "Adding a tripwire offer on the thank-you page converts a percentage of new leads immediately, offsetting ad spend",
  variants: ["control: thank-you page with no offer", "variant: thank-you page with time-limited tripwire CTA"],
  measurement: "tripwire conversion rate and revenue per lead over 500 opt-ins",
  expected_impact: "5-12% tripwire take rate, reducing effective cost-per-lead by 30%+"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="lead-magnet-copy-writer",
  query="Highest-converting lead magnet formats and opt-in page structures by industry vertical 2024-2025, including emerging formats like AI-powered assessments and interactive calculators",
  reason="Ensure lead magnet format recommendations reflect current ICA consumption preferences and competitive benchmarks rather than outdated PDF-first assumptions"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="lead-magnet-copy-writer", session={
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