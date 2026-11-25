---
name: invisible-demand-detector
description: |
  Detects latent, unarticulated demand signals competitors overlook and
  surfaces invisible market needs before they harden into visible trends.
  Use when a user asks "what unmet needs exist in my market", "where's the
  whitespace", "what are people struggling with that nobody's solving", or
  "there's demand we're not seeing". Surfaces present-tense unmet needs —
  for future audience shifts use invisible-trends-forecaster.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="invisible-demand-detector")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any existing ICA profiles, market positioning, prior demand hypotheses, and validated/invalidated experiments from previous runs.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Market scope**: What industry, niche, or vertical are we investigating? (e.g., "B2B fintech for mid-market CFOs," "DTC wellness for millennial women")
- **ICA definition**: Who is the ideal customer? Share any existing ICA profiles, or describe the person/organisation whose invisible pain we're hunting for
- **Current offer landscape**: What do you currently sell, and what do your top 3–5 competitors offer? (links, descriptions, or summaries accepted)
- **Signal sources available**: Do you have access to any of the following — support tickets, community forums, sales call recordings, social listening data, review/NPS data, search console queries, refund/cancellation reasons?
- **Constraint boundaries**: Any markets, segments, or problem spaces explicitly out of scope?

If the user has prior sessions in FutureProof context, pre-populate known answers and ask only for confirmation or updates.

## Step 3: Map the Signal Landscape

Conduct a **five-layer signal audit** to identify where invisible demand hides. For each layer, categorise signals as _strong_, _moderate_, or _weak_ based on frequency, emotional intensity, and absence of existing solutions.

### Layer 1: Complaint Mining (Expressed Frustration)
- Analyse language patterns in reviews, support tickets, and community posts for the ICA's market
- Identify **high-emotion, low-resolution complaints** — problems people raise repeatedly but accept as unsolvable
- Flag vocabulary clusters: words and phrases the ICA uses that no vendor currently mirrors in positioning

### Layer 2: Workaround Detection (Behavioural Signals)
- Identify DIY solutions, spreadsheet hacks, duct-tape integrations, and manual processes the ICA uses to compensate for missing products/features
- Map **tool-stacking patterns** — where the ICA combines 3+ tools to solve one job-to-be-done, indicating a consolidation opportunity
- Surface "I just wish..." and "does anyone know how to..." patterns from forums, Reddit, Slack communities, and Q&A sites

### Layer 3: Adjacent Demand Bleed (Cross-Market Signals)
- Identify demand that is **clearly expressed in adjacent markets** but has not yet been addressed in the user's target market
- Apply analogical transfer: what solutions are thriving in parallel verticals that could be adapted?
- Detect **category creation signals** — terminology the ICA is inventing because no existing category label fits their need

### Layer 4: Negative Space Analysis (What's Conspicuously Absent)
- Audit competitor positioning for **uniform blind spots** — problems every competitor ignores or explicitly deprioritises
- Identify ICA jobs-to-be-done that appear in no competitor's messaging, feature set, or content strategy
- Map the **"nobody talks about this" zone** — topics with high private search volume but low published content density

### Layer 5: Temporal Demand Forecasting (Emerging Signals)
- Identify regulatory, technological, demographic, or cultural shifts that will **create demand within 6–18 months** but are not yet broadly felt
- Detect early-adopter behaviour changes that predict mainstream demand curves
- Flag **rising search trends, new subreddit growth, emerging hashtags, and legislative pipelines** relevant to the ICA's world

Apply any user-specific `instructions` from FutureProof context to weight layers appropriately (e.g., if the user has previously indicated they prioritise near-term revenue, weight Layers 1–2 more heavily).

## Step 4: Synthesise Demand Hypotheses

For each signal cluster identified, formulate a **Demand Hypothesis** using this structure:

> **Hypothesis ID**: IDD-[sequential number]
> **Signal Layer**: [which of the 5 layers]
> **Demand Statement**: "[ICA segment] needs [specific outcome] because [root cause], but currently [workaround or unmet state]."
> **Evidence Density**: [number of independent signals supporting this]
> **Confidence Level**: High / Medium / Low
> **Competitive Vacuum Score**: 1–10 (10 = no competitor addresses this at all)
> **Monetisation Proximity**: Immediate / Near-term (3–6 months) / Emerging (6–18 months)
> **ICA Emotional Register**: [the dominant emotion — frustration, anxiety, aspiration, shame, urgency]

Rank all hypotheses in a **prioritisation matrix** using:
- **X-axis**: Competitive Vacuum Score (higher = more whitespace)
- **Y-axis**: Evidence Density × Monetisation Proximity (higher = more actionable)

Identify the **top 3 invisible demand opportunities** — the highest-conviction, highest-impact hypotheses.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver Output

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce the **Invisible Demand Report** — a structured deliverable containing:

### Section A: Executive Summary
- 1-paragraph market context statement
- Top 3 invisible demand opportunities ranked by priority
- Recommended immediate action for each

### Section B: Signal Evidence Map
- Full five-layer audit findings with specific quotes, data points, and source references
- Visual-ready matrix data (hypothesis ID, vacuum score, evidence density, monetisation proximity)

### Section C: Demand Hypothesis Cards
- Complete hypothesis cards for all identified opportunities (minimum 5, maximum 12)
- Each card includes: demand statement, evidence trail, competitive vacuum assessment, ICA emotional register, and a **one-line offer concept** that could address the demand

### Section D: Validation Playbook
For each top-3 hypothesis, provide:
- **Fastest validation method**: the cheapest, fastest way to test if this demand is real (e.g., landing page test, 5-question ICA interview script, social post probe, waitlist signup)
- **Validation success criteria**: specific metric and threshold that confirms or kills the hypothesis
- **Estimated validation timeline**: days/weeks to signal

### Section E: Strategic Recommendations
- Which hypotheses to pursue, sequence, and kill
- How findings integrate with the user's existing offer suite and positioning
- Specific language and messaging angles derived from ICA vocabulary clusters discovered in Layer 1

Format the report with clear headers suitable for sharing with leadership, investors, or product teams.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="invisible-demand-detector", experiment={
  hypothesis: "[Top-ranked demand hypothesis demand statement]",
  variants: [
    "control: current market positioning with no reference to invisible demand signal",
    "variant A: landing page / social post / email sequence explicitly addressing the identified latent need using ICA vocabulary from signal audit"
  ],
  measurement: "engagement rate (click-through, reply rate, or waitlist signup) comparing control vs variant over 14-day window",
  expected_impact: "20–40% engagement lift on variant A if demand hypothesis is valid; sub-5% lift signals hypothesis should be deprioritised"
})
```

Save additional experiments for the #2 and #3 ranked hypotheses if the user has capacity to run parallel tests.

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="invisible-demand-detector",
  query="Emerging unmet needs and underserved jobs-to-be-done in [user's specific market/vertical] — community sentiment analysis, rising search trends, and regulatory pipeline changes 2024–2025",
  reason="Refresh signal landscape for next session; validate or invalidate temporal demand forecasts from Layer 5; surface new signals that have emerged since this analysis"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="invisible-demand-detector", session={
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