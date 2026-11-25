---
name: competitive-feature-comparison
description: |
  Builds ICA-weighted competitive feature matrices, positioning maps, sales
  battlecards, and roadmap implications by scoring competitors on observable
  evidence. Use when users say "compare us vs [competitor]", "build a feature
  matrix", "I need a competitive analysis", "make sales battlecards", or
  "where are we losing to competitors". For external competitor benchmarking,
  not internal feature prioritization or roadmap sequencing.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="competitive-feature-comparison")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any previously identified competitors, ICA segments, known feature gaps, and positioning frameworks already validated.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Your product**: What product or service are we analysing? Share any existing feature documentation, marketing site, or product brief.
- **Competitors**: Which specific competitors should we benchmark against? (Name 2–5; if unsure, we will identify the most relevant set.)
- **ICA context**: Which ICA segment is this comparison serving? (e.g., enterprise buyers evaluating procurement, sales team needing battlecards, product team prioritising roadmap)
- **Decision context**: What decision will this comparison inform? (sales enablement, product strategy, investor narrative, pricing repositioning)
- **Known pain points**: Are there specific feature areas where you suspect you are losing deals or trailing competitors?

If FutureProof context already contains ICA definitions, competitor profiles, or prior comparison sessions, surface them and ask the user to confirm or update before proceeding.

## Step 3: Define the Comparison Framework

Construct a **Weighted Feature Taxonomy** using a three-tier hierarchy:

### 3a: Identify Feature Categories
Map the competitive landscape into 5–8 feature categories relevant to the product domain. For each category, define 3–6 discrete capabilities. Example structure:

| Category | Capabilities |
|---|---|
| Core Functionality | Capability A, Capability B, Capability C |
| Integration Ecosystem | Native integrations, API depth, Webhook support |
| User Experience | Onboarding friction, Time-to-value, Accessibility |
| Security & Compliance | Certifications, Data residency, Audit logging |
| Pricing & Packaging | Transparency, Scalability, Value alignment |

### 3b: Apply ICA-Weighted Scoring
Not all features matter equally to the ICA. Assign weight multipliers (1.0x–3.0x) to each category based on:
- **ICA purchase drivers** — what the ICA explicitly evaluates during buying
- **ICA latent priorities** — what correlates with retention and expansion post-purchase
- **Switching cost factors** — capabilities that create lock-in or reduce migration friction

Apply any user-specific `instructions` from FutureProof context (e.g., "our ICA cares more about compliance than UX" or "price sensitivity is low for enterprise segment").

## Step 4: Conduct the Competitive Assessment

For each competitor, evaluate every capability on a **5-point maturity scale**:

| Score | Definition |
|---|---|
| 5 — Market-leading | Best-in-class implementation; recognised industry differentiator |
| 4 — Strong | Fully developed; meets advanced use cases without workarounds |
| 3 — Adequate | Functional coverage; gaps in edge cases or depth |
| 2 — Emerging | Partial implementation; requires workarounds or third-party tooling |
| 1 — Absent/Deficient | Not available or fundamentally below market expectations |

### Assessment rigour standards:
- Score claims must reference **observable evidence** (public documentation, G2/Gartner reviews, changelog analysis, published case studies) — not assumptions
- Where evidence is unavailable, flag the score as **[unverified]** and note the confidence level
- Document the **evidence source** for each score to enable user validation
- Cross-reference FutureProof `recent_sessions` for any prior intelligence on these competitors

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


Produce a **Competitive Feature Comparison Dossier** containing four deliverables:

### Deliverable 1: Weighted Feature Matrix
A structured comparison table with:
- Rows: capabilities grouped by category
- Columns: user product + each competitor
- Cells: raw score (1–5) and weighted score (raw × ICA weight)
- Row totals per category, grand totals per competitor
- Visual indicators: ✅ (advantage), ⚠️ (parity), ❌ (disadvantage) relative to user product

### Deliverable 2: Competitive Positioning Map
A narrative analysis organised into three sections:
- **Defensible advantages** — where the user product leads by ≥2 points (weighted) and why this matters to the ICA
- **Contested battlegrounds** — parity zones where positioning, messaging, or minor feature investment could shift perception
- **Vulnerability zones** — where competitors lead by ≥2 points (weighted), with assessment of whether the gap is structural or closable within 1–2 quarters

### Deliverable 3: Sales Battlecard Summary
For each competitor, a concise battlecard block formatted for immediate sales enablement use:
- **When prospect mentions [Competitor]**: 2–3 talking points anchored in ICA pain language
- **Trap-setting questions**: questions the sales team can ask that expose competitor weaknesses naturally
- **Proof points**: specific evidence (case studies, benchmarks, testimonials) that substantiate advantage claims
- **Concession script**: how to professionally acknowledge areas where the competitor is strong without undermining credibility

### Deliverable 4: Product Roadmap Implications
A prioritised list of 3–5 feature investments ranked by:
- **ICA impact score** (weighted gap × ICA segment size)
- **Competitive urgency** (number of competitors already at score 4+)
- **Estimated effort** (T-shirt sizing: S/M/L/XL based on available information)
- **Recommended action**: Build, Buy/Integrate, Partner, or Deprioritise

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="competitive-feature-comparison", experiment={
  hypothesis: "Incorporating ICA-weighted battlecard language into sales decks for the top contested battleground area increases competitive win rate",
  variants: ["control: current competitive positioning slide", "variant: battlecard-informed slide with trap-setting questions embedded in discovery script"],
  measurement: "Competitive win rate in deals where primary competitor is [top rival] over next 30 deals",
  expected_impact: "10–20% improvement in competitive win rate for contested deals"
})
```

```
FutureProof:save_experiment(skill="competitive-feature-comparison", experiment={
  hypothesis: "Prioritising the #1 ranked vulnerability zone feature gap on the product roadmap reduces churn attributed to competitive displacement",
  variants: ["control: current roadmap sequence", "variant: reprioritised roadmap with vulnerability zone feature moved to next sprint cycle"],
  measurement: "Churn exit-survey mentions of competitor feature superiority over next quarter",
  expected_impact: "Reduction in competitive-displacement churn by 15%"
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
FutureProof:request_research(skill="competitive-feature-comparison",
  query="Latest feature releases, pricing changes, and strategic pivots from [identified competitors] in the past 90 days, including G2 review sentiment trends and analyst commentary",
  reason="Ensure competitive intelligence remains current; feature matrices degrade rapidly as competitors ship updates and reposition"
)
```

```
FutureProof:request_research(skill="competitive-feature-comparison",
  query="ICA buying criteria evolution in [user's product category] — what features and evaluation dimensions are gaining or losing weight in enterprise purchasing decisions 2024–2025",
  reason="Validate and recalibrate ICA weight multipliers to reflect shifting market priorities rather than historical assumptions"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="competitive-feature-comparison", session={
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