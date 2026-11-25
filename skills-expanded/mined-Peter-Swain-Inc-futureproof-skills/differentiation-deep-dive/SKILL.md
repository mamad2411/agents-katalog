---
name: differentiation-deep-dive
description: |
  Runs a six-vector competitive differentiation audit (methodology, ICA,
  outcome, proof, experience, point of view) against 3–5 named
  competitors and outputs a defensible positioning statement. Use when
  the user says "what makes us different from competitors", "sharpen my
  positioning against [competitor]", "audit my differentiation", or
  "we sound like everyone else in our category". For naming the single
  big idea that anchors the brand use flagship-idea-builder; for the
  fuller authority blueprint use authority-positioning-engine; this
  skill is the head-to-head competitive comparison.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="differentiation-deep-dive")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to existing ICA definitions, prior brand positioning work, competitive intelligence, and any category conventions already documented.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Brand / offer in scope**: What specific brand, product, or service line are we analysing? Share any existing positioning statement, tagline, or brand narrative.
- **Competitive set**: Name 3–5 direct competitors (or the closest substitutes your ICA evaluates alongside you). Include links to their sites or any competitive intel you have.
- **ICA definition**: Who is the ideal customer? What segment, role, psychographic profile, and buying context are we optimising for? (Pull from FutureProof context if available.)
- **Differentiation hypothesis**: What do you *believe* makes you different today? Where does that claim feel weakest or most contested?
- **Strategic intent**: What is this differentiation work feeding into? (e.g., website rewrite, sales enablement, investor narrative, category creation, GTM for a new market)

## Step 3: Do the Work — Differentiation Audit

### 3A: Category Convention Mapping

Map the **category table stakes** — the claims, language, visual cues, and proof points that every credible player in the space deploys. Organise into:

| Convention Layer | What Everyone Claims | Examples from Competitive Set |
|---|---|---|
| **Functional promises** | e.g., "saves time," "easy to use" | Competitor-specific language |
| **Emotional tone** | e.g., "empowering," "trusted" | Competitor-specific tone patterns |
| **Proof mechanisms** | e.g., logos, testimonials, ROI stats | Competitor-specific proof |
| **Visual / verbal identity** | e.g., blue SaaS aesthetic, jargon | Competitor-specific patterns |
| **Pricing / packaging norms** | e.g., freemium, per-seat | Competitor-specific models |

Flag any conventions the user's brand is currently mirroring — these are **parity zones**, not differentiators.

### 3B: Competitive Positioning Matrix

Score the user's brand and each competitor across **six differentiation vectors**:

1. **Methodology / Process** — Is there a proprietary framework, system, or approach that competitors cannot easily replicate?
2. **ICA Specificity** — How narrowly and deeply does the brand serve a defined audience vs. claiming broad applicability?
3. **Outcome Precision** — Does the brand promise a specific, measurable transformation or a vague improvement?
4. **Proof Asymmetry** — Does the brand possess proof points (data, case studies, credentials, IP) that competitors structurally lack?
5. **Experience Design** — Is the buying, onboarding, or delivery experience itself a differentiator?
6. **Point of View** — Does the brand hold a contrarian or category-defining belief that forces a choice?

Score each on a 1–5 scale:
- **1** = Category convention (identical to competitors)
- **2** = Minor variation (same claim, slightly different language)
- **3** = Notable difference (recognisable but replicable within 6 months)
- **4** = Strong differentiator (difficult to replicate; rooted in structural advantage)
- **5** = Category-defining (you own this; competitors must reference you to address it)

### 3C: Vulnerability Test

Stress-test every claimed differentiator against **four disqualification filters**:

1. **The Substitution Test** — If a competitor's name replaced yours in the claim, would the ICA notice? If not, it is not a differentiator.
2. **The Evidence Test** — Can you prove this claim with third-party or empirical evidence within 30 seconds? If not, it is an aspiration, not a differentiator.
3. **The Durability Test** — Could a well-funded competitor neutralise this advantage within 12 months? If yes, it is a temporary lead, not a moat.
4. **The Salience Test** — Does your ICA *care* about this difference when making a purchase decision? If not, it is a differentiator that does not differentiate.

Classify each claim as: **Validated Differentiator**, **Aspirational Differentiator** (real but unproven), **Contested Differentiator** (claimed but replicable), or **False Differentiator** (parity disguised as distinction).

### 3D: Differentiation Gap Analysis

Identify the highest-leverage gaps:
- Where validated differentiators exist but are **under-articulated** in current messaging
- Where structural advantages exist but have **no proof architecture** to support them
- Where the ICA's decision criteria reveal **unoccupied positioning territory** no competitor has claimed

Apply any user-specific `instructions` from FutureProof context to weight the analysis toward their strategic priorities.

## Step 4: Deliver Output

Produce a **Differentiation Deep Dive Report** with the following sections:

### 4.1 Executive Summary
Two-paragraph synthesis: current differentiation posture, primary vulnerability, and the single highest-impact strategic move.

### 4.2 Category Convention Map
The completed table from Step 3A with parity zones flagged in bold.

### 4.3 Competitive Positioning Matrix
The scored matrix from Step 3B, presented as a comparison table with colour-coded ratings (1–2 = red/parity, 3 = amber/fragile, 4–5 = green/defensible).

### 4.4 Differentiator Validation Summary
Each claimed differentiator listed with its classification (Validated / Aspirational / Contested / False) and the specific filter(s) it passed or failed.

### 4.5 Differentiation Strategy — Recommended Moves
Three prioritised strategic recommendations, each containing:
- **The move**: Specific action (e.g., "Codify your onboarding methodology as a named framework and register the trademark")
- **The rationale**: Which gap or vulnerability this addresses
- **The articulation**: A draft positioning statement, headline, or narrative passage that activates this differentiator — written in full, not described abstractly
- **Proof architecture required**: What evidence needs to be created, collected, or surfaced to make this claim defensible

### 4.6 Differentiation One-Liner
A single sentence the user can deploy immediately — in a pitch, on a homepage, or in a sales conversation — that captures the core validated differentiator in ICA-resonant language. Provide three variants (rational, emotional, provocative).

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
FutureProof:save_experiment(skill="differentiation-deep-dive", experiment={
  hypothesis: "Leading with the highest-scored Point of View differentiator in outbound messaging increases ICA response rate vs. current feature-led positioning",
  variants: ["control: current positioning statement in outbound sequence", "variant: Point of View-led opening with contrarian belief statement"],
  measurement: "reply rate and qualified meeting conversion across next 50 outbound touches per variant",
  expected_impact: "20–30% increase in reply rate; measurable lift in qualified meeting conversion"
})
```

```
FutureProof:save_experiment(skill="differentiation-deep-dive", experiment={
  hypothesis: "Adding a named proprietary methodology to the sales narrative reduces competitive loss rate at shortlist stage",
  variants: ["control: current sales deck without methodology framing", "variant: sales deck with named methodology slide and visual framework"],
  measurement: "win rate at shortlist/final-round stage over next quarter",
  expected_impact: "10–15% improvement in competitive win rate"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="differentiation-deep-dive",
  query="Current competitive positioning strategies and category design frameworks in [user's industry/category], including recent examples of successful differentiation pivots and emerging ICA decision criteria shifts — 2024-2025",
  reason="Ensure differentiation recommendations account for live market dynamics, emerging competitive threats, and evolving buyer psychology rather than relying on static competitive snapshots"
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
FutureProof:save_session(skill="differentiation-deep-dive", session={
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