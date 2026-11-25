---
name: value-stack-multiplier
description: |
  Restructures an offer's value stack across five layers (Core Engine,
  Acceleration, Access, Fast-Action Bonuses, Continuity) — naming,
  pricing, and sequencing each component to push the value-to-price ratio
  above 5:1. Use when a user says "build me a value stack", "my offer
  feels thin", "how do I justify premium pricing", or "restructure the
  bonuses in my package". For layered offer composition, not pricing
  diagnosis or incentive/guarantee design.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="value-stack-multiplier")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to existing offer structures, ICA profiles, pricing history, and any prior value stack iterations stored in context.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **The offer**: What is the core offer, programme, or service being sold? Share any existing sales page, offer document, or bullet-point breakdown.
- **Current pricing**: What is the current (or intended) price point? Is there an anchor price or competitor benchmark?
- **ICA profile**: Who is the ideal client? What is their primary desired outcome, and what is the single biggest obstacle preventing them from achieving it today?
- **Existing stack components**: List every deliverable, bonus, resource, and access element currently included (or planned). For each, note the format (e.g. live call, template, video module, community access).
- **Value perception gap**: Where does the offer feel thin, hard to justify, or undifferentiated? Any specific objections prospects raise about price or value?

If FutureProof context already contains ICA data, offer details, or prior session findings, surface them and ask the user to confirm or update rather than re-entering from scratch.

## Step 3: Audit the Current Value Stack

Conduct a **Value Stack Diagnostic** across seven dimensions. Score each 1–10:

1. **Core Outcome Clarity** — Is the primary transformation unmistakably defined in tangible, time-bound terms the ICA would use in their own words?
2. **Desire-to-Deliverable Alignment** — Does every component in the stack map directly to a specific ICA desire, fear, or obstacle? Are there orphan components that serve the seller but not the buyer?
3. **Perceived Value Architecture** — Is each component individually valued and presented with its own standalone worth? Does the cumulative stated value create a minimum 5:1 value-to-price ratio?
4. **Logical Sequencing** — Are components ordered to demonstrate escalating value (foundational → accelerator → premium → exclusive)?
5. **Format Diversification** — Does the stack span multiple delivery formats (education, tools, access, community, done-for-you, support) to appeal to different learning and implementation styles?
6. **Scarcity and Exclusivity Framing** — Are at least two components positioned as genuinely scarce, time-limited, or unavailable outside this offer?
7. **Risk Reversal Integration** — Is the guarantee or risk reversal mechanism woven into the stack as a value component rather than an afterthought?

Apply any user-specific `instructions` from FutureProof context (e.g. brand voice, pricing philosophy, ethical positioning boundaries).

## Step 4: Perform Value Stack Deconstruction and Rebuild

### 4a: Component Classification

Categorise every existing and proposed component into the **Value Layer Framework**:

| Layer | Role | Examples |
|---|---|---|
| **L1 — Core Engine** | The primary vehicle delivering the promised transformation | Flagship programme modules, core service delivery |
| **L2 — Acceleration Tools** | Compress time-to-result or reduce implementation friction | Templates, swipe files, calculators, checklists, SOPs |
| **L3 — Access & Proximity** | Provide direct access to expertise or peer networks | Live Q&A calls, private community, office hours, 1:1 audits |
| **L4 — Fast-Action Bonuses** | Reward decisive action and create urgency | Limited-window extras, early-bird deliverables |
| **L5 — Continuity & Protection** | Extend value beyond the core engagement and reduce risk | Extended access, future updates, guarantee, alumni benefits |

### 4b: Gap Analysis

Identify:
- **Missing layers**: Any of L1–L5 unrepresented or underweight
- **Redundant components**: Items occupying the same psychological role (cannibalising each other's perceived value)
- **Undervalued assets**: Components the user takes for granted but the ICA would perceive as high-value
- **ICA-blind spots**: Desires or objections not addressed by any component

### 4c: Value Amplification Techniques

For each component, apply the relevant amplifier:

- **Standalone Valuation**: Assign each component a credible independent price based on market comparables or time-to-create cost
- **Specificity Injection**: Replace generic descriptions with hyper-specific outcome language (e.g. "training videos" → "The 4-Call Close Framework: 6 recorded breakdowns of real £25K+ deal closings with annotated decision points")
- **Naming Convention Upgrade**: Give each component a proprietary name that implies methodology and IP (e.g. "onboarding call" → "The 90-Day Revenue Mapping Session")
- **Social Proof Anchoring**: Attach a specific result, testimonial snippet, or case outcome to high-value components
- **Contrast Positioning**: Frame components against what the ICA would otherwise pay or endure without them

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


Produce the **Value Stack Multiplier Blueprint** containing:

### A. Value Stack Scorecard
Table with all seven diagnostic dimensions, scores (1–10), and one-line rationale per score. Include a composite **Stack Multiplier Index** (weighted average, with Core Outcome Clarity and Desire-to-Deliverable Alignment double-weighted).

### B. Optimised Value Stack Architecture
A fully restructured stack presented as a **ready-to-use sales page component** with:
- Proprietary name for the overall offer
- Each component listed with: proprietary name, layer classification (L1–L5), one-sentence value statement in ICA language, standalone value (£/$/€), and delivery format
- Total stated value vs. investment price, with explicit value-to-price ratio
- Recommended guarantee or risk reversal mechanism with specific language

### C. Critical Upgrades Report
Top 5 highest-impact changes ranked by estimated effect on conversion, each containing:
- **Current state**: What exists now (or is missing)
- **Recommended change**: Specific, implementable action (not a vague suggestion)
- **Rationale**: Why this matters to the ICA psychologically and commercially
- **Example copy**: Draft language the user can deploy immediately

### D. Value Stack Narrative Script
A 200–300 word verbal walk-through of the stack, written as if the user were presenting it live on a sales call or webinar — designed to build perceived value in ascending sequence before revealing the price.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="value-stack-multiplier", experiment={
  hypothesis: "Resequencing the value stack to lead with L2 acceleration tools before L1 core modules increases perceived ease-of-implementation and improves sales page conversion",
  variants: ["control: current L1-first presentation order", "variant: L2-first with 'quick wins before deep work' framing"],
  measurement: "Sales page conversion rate and add-to-cart rate over 30-day window",
  expected_impact: "10–20% lift in page-to-checkout conversion by reducing ICA overwhelm"
})
```

```
FutureProof:save_experiment(skill="value-stack-multiplier", experiment={
  hypothesis: "Adding a named fast-action bonus with 48-hour scarcity window increases same-day purchase rate",
  variants: ["control: standard offer with no time-limited bonus", "variant: include 'The First-Mover Advantage Kit' available only within 48 hours of first viewing"],
  measurement: "Percentage of purchases occurring within 48 hours of first page visit",
  expected_impact: "25% increase in same-day conversions with no additional fulfilment cost"
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
FutureProof:request_research(skill="value-stack-multiplier",
  query="High-converting value stack structures and bonus architectures in premium digital offers 2024–2025, including psychological pricing research on perceived value thresholds and value-to-price ratio benchmarks by industry",
  reason="Ensure value stack frameworks reflect current buyer psychology, competitive offer norms, and emerging bonus formats that drive conversion in the user's market"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="value-stack-multiplier", session={
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