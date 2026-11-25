---
name: sales-page
description: |
  Writes long-form direct-response sales pages — full offer page, VSL
  hybrid or application funnel — with offer architecture, unique
  mechanism, deep proof stack, objection handling and risk reversal for
  high-ticket products, courses and programs. Use when the user says
  "write me a sales page", "long-form sales letter for my course",
  "rewrite my sales page", or "VSL script and page for my offer". For a
  short opt-in or squeeze page use landing-page-writer; for the lead
  magnet that fronts it use lead-magnet-copy-writer; this skill is the
  full bottom-of-funnel offer page.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="sales-page")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to existing ICA definitions, brand voice guidelines, offer positioning, pricing architecture, proof assets, and any prior conversion data from previous sales page sessions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Gather the following from the user — adapt based on what FutureProof context already provides:

**Offer Architecture**
- What is the product, service, programme, or course being sold?
- What is the price point and pricing structure (one-time, recurring, payment plan, tiered)?
- What is the primary call to action (buy now, book a call, apply, join waitlist)?
- What is the guarantee or risk-reversal mechanism?

**ICA Definition**
- Who is the Ideal Client Avatar — demographic, psychographic, and situational profile?
- What is the ICA's current painful state (specific language they use to describe it)?
- What is the ICA's desired future state (specific outcomes they want)?
- What has the ICA already tried that failed, and why do they believe those solutions didn't work?

**Proof & Authority Assets**
- Testimonials, case studies, or quantified results available?
- Credentials, media features, audience size, or authority markers?
- Specific before/after transformations from past clients?

**Competitive Context**
- What alternatives is the ICA evaluating (competitors, DIY, do nothing)?
- What is the unique mechanism — the proprietary method or differentiator that explains *why this works when other approaches didn't*?

**Constraints & Preferences**
- Desired page length or format (long-form, video sales letter hybrid, application funnel)?
- Brand voice parameters (e.g. provocative, warm, clinical, aspirational)?
- Any sections or approaches to avoid?

## Step 3: Do the Work

### 3A: Strategic Foundation

Before writing a single line of copy, construct the **Sales Page Strategy Brief**:

1. **ICA Awareness Level** — classify using Schwartz's 5 levels (Unaware, Problem-Aware, Solution-Aware, Product-Aware, Most Aware) to determine the correct opening strategy and page length
2. **Core Belief Shifts** — identify the 3–5 beliefs the ICA holds on arrival that must change before they will buy (e.g. "I've tried coaching before and it doesn't work" → "This methodology is structurally different because [unique mechanism]")
3. **Objection Map** — enumerate the top 5 purchase objections in priority order, with the specific page section where each will be neutralised
4. **Emotional Arc** — plot the reader's emotional journey from opening to CTA: agitation → empathy → possibility → credibility → clarity → urgency → action
5. **Proof Sequencing Plan** — assign each proof asset (testimonial, case study, credential) to the specific belief shift or objection it serves

### 3B: Sales Page Architecture

Construct the page using the following section-by-section framework. Each section has a defined strategic job:

| # | Section | Strategic Job | Key Technique |
|---|---------|--------------|---------------|
| 1 | **Pre-headline / Callout** | Filter for ICA, repel non-fits | Identity-based qualifier ("For [ICA] who [situation]") |
| 2 | **Headline + Sub-headline** | Stop the scroll, articulate the transformation | Outcome-first, specificity-loaded, matches awareness level |
| 3 | **Opening Story / Problem Agitation** | Build resonance, prove you understand | Mirror ICA's internal monologue using their exact vocabulary; name the failed alternatives |
| 4 | **The Bridge / Turning Point** | Transition from problem to possibility | Introduce the insight or discovery that changes everything |
| 5 | **Unique Mechanism Reveal** | Explain *why* this works when others didn't | Name the proprietary method; make it tangible and logical |
| 6 | **Outcome Painting** | Expand desire with specific future-state imagery | Concrete, sensory, time-bound outcomes — not vague promises |
| 7 | **Social Proof Block I** | Validate the transformation is real for people like the ICA | 2–3 testimonials/case studies mapped to the primary belief shift |
| 8 | **Full Offer Breakdown** | Make the value tangible, justify the price | Module-by-module or component-by-component with benefit-driven descriptions |
| 9 | **Bonus Stack** | Accelerate perceived value past the price threshold | Each bonus solves a secondary objection or adjacent pain |
| 10 | **Social Proof Block II** | Address remaining scepticism with diverse proof types | Results screenshots, media mentions, credentials, volume metrics |
| 11 | **Price Reveal + Anchoring** | Frame price as an asymmetric investment | Value stack total → price anchor → actual price → payment plan → ROI reframe |
| 12 | **Risk Reversal** | Eliminate the final purchase barrier | Guarantee with specific terms; make the guarantee itself a selling point |
| 13 | **Objection Handling / FAQ** | Neutralise remaining hesitations | Address top 5 objections directly; reframe each as a reason to buy |
| 14 | **Final CTA Block** | Convert | Summarise transformation, restate guarantee, single clear action |
| 15 | **Closing P.S. Section** | Catch skimmers, add urgency | Restate strongest proof point + scarcity/urgency element if authentic |

### 3C: Copy Execution

Write each section in full, applying these non-negotiable standards:

- **Voice fidelity**: match the brand voice parameters from Step 2; default to confident, direct, empathetic if none specified
- **ICA language**: use the exact words, phrases, and metaphors the ICA uses — never corporate abstractions
- **Specificity over superlatives**: replace every instance of "amazing," "incredible," "revolutionary" with a concrete claim, number, or example
- **One idea per paragraph**: short paragraphs (1–3 sentences), frequent subheadings, visual breathing room
- **Transition hooks**: every section ends with a micro-hook that compels the reader into the next section
- **Proof integration**: weave testimonials and proof inline (not just in dedicated blocks) to support claims at the moment of scepticism
- **CTA repetition**: embed secondary CTAs after sections 7, 10, and 12 in addition to the primary CTA block

## Step 4: Deliver Output

Produce the following structured deliverables:

### Deliverable 1: Sales Page Strategy Brief
A standalone document containing:
- ICA awareness level classification with rationale
- Core belief shift map (current belief → required belief → section that achieves the shift)
- Objection map with neutralisation strategy per objection
- Emotional arc diagram
- Proof sequencing plan

### Deliverable 2: Complete Sales Page Copy
The full sales page, section by section (Sections 1–15), with:
- Section headers clearly labelled for the user and their designer/developer
- Stage directions in `[brackets]` for visual elements, imagery, testimonial placement, and design cues
- Inline notes flagged with `⚡ CONVERSION NOTE:` explaining the strategic rationale behind key copy decisions
- Word count per section noted for layout planning

### Deliverable 3: Conversion Optimisation Checklist
A 15-point audit of the finished page scored against:

| Dimension | Score (1–10) | Notes |
|-----------|-------------|-------|
| ICA resonance (language mirror accuracy) | | |
| Headline stopping power | | |
| Unique mechanism clarity | | |
| Belief shift completeness | | |
| Proof density and diversity | | |
| Objection pre-emption coverage | | |
| Emotional arc coherence | | |
| Value-to-price perception | | |
| Risk reversal strength | | |
| CTA clarity and frequency | | |
| Readability and scannability | | |
| Urgency/scarcity authenticity | | |
| Brand voice consistency | | |
| Mobile readability | | |
| Logical flow (no dead zones) | | |

Include **top 3 priority refinements** with specific rewrites if any dimension scores below 7.

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
FutureProof:save_experiment(skill="sales-page", experiment={
  hypothesis: "Leading with the ICA's most emotionally charged failed-solution language in the headline increases scroll depth and time-on-page",
  variants: [
    "control: current outcome-first headline",
    "variant A: pain-first headline using ICA's exact failure language",
    "variant B: identity-callout headline that filters and qualifies"
  ],
  measurement: "scroll depth (25/50/75/100%), time on page, CTA click-through rate, conversion rate",
  expected_impact: "12–20% improvement in headline-to-first-CTA scroll-through rate"
})
```

```
FutureProof:save_experiment(skill="sales-page", experiment={
  hypothesis: "Placing the strongest case study immediately after the unique mechanism reveal (Section 6) reduces drop-off at the offer breakdown",
  variants: [
    "control: social proof in dedicated blocks at Sections 7 and 10",
    "variant: flagship case study embedded directly after Section 5 unique mechanism reveal"
  ],
  measurement: "section-by-section scroll depth heatmap, conversion rate",
  expected_impact: "8–15% reduction in mid-page abandonment"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="sales-page",
  query="High-converting sales page structures and headline formulas by awareness level (Schwartz framework) with 2024 conversion benchmarks across price points ($97–$10,000+)",
  reason="Calibrate page architecture and headline strategy to current market response patterns and buyer sophistication levels"
)
```

```
FutureProof:request_research(skill="sales-page",
  query="ICA objection evolution in digital product and service sales — emerging scepticism patterns, proof format preferences, and trust signals that move conversion in 2024",
  reason="Ensure objection handling and proof sequencing reflect current buyer psychology rather than outdated direct-response conventions"
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
FutureProof:save_session(skill="sales-page", session={
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