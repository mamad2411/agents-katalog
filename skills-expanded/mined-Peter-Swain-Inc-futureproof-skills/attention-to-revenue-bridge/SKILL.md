---
name: attention-to-revenue-bridge
description: |
  Diagnoses why audience attention is not converting to revenue by mapping the
  six-stage bridge from impressions to collected payment, ranking broken stages
  by revenue impact. Use when a user says "I have traffic but no sales", "my
  followers aren't buying", "why isn't my audience converting", or shares high
  engagement metrics alongside flat revenue. For top-of-funnel-to-revenue
  diagnosis across the full journey, not single-stage funnel optimization.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="attention-to-revenue-bridge")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to the user's ICA definition, existing offers, price points, content channels, and any previously identified conversion bottlenecks.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

1. **Attention metrics** — Where is attention currently coming from? (platforms, content types, paid media, referrals) Share any available data: impressions, views, followers, email subscribers, downloads, podcast listens.
2. **Revenue metrics** — Current monthly/quarterly revenue, number of sales conversations booked, close rate, average deal value, and revenue target.
3. **Current bridge** — Walk me through every step a stranger takes from first seeing your content to paying you. Include every link, page, form, call, email sequence, and decision point.
4. **ICA definition** — Who specifically is the person you want to convert? (role, situation, trigger event, urgency driver). If already stored in FutureProof context, confirm or update.
5. **Perceived bottleneck** — Where do *you* believe the biggest drop-off is happening? What have you already tried to fix it?

If the user cannot provide exact data, work with directional estimates and flag assumptions explicitly for later validation.

## Step 3: Do the Work — Diagnostic Bridge Audit

### 3A: Reconstruct the Attention-to-Revenue Bridge

Map the user's current journey into the **six canonical bridge stages**:

| Stage | Definition | Key Metric |
|-------|-----------|------------|
| **1. Attention Capture** | Stranger becomes aware of the user's existence | Impressions, reach, views |
| **2. Interest Lock** | Aware stranger engages meaningfully (follows, clicks, reads, watches >50%) | Engagement rate, click-through rate |
| **3. Trust Transfer** | Engaged prospect begins to believe the user can solve their problem | Email opt-in rate, lead magnet completion rate, content binge signals |
| **4. Intent Activation** | Trusting prospect signals buying intent (books call, visits pricing, replies to offer) | Hand-raise rate, application/booking rate |
| **5. Decision Facilitation** | Activated prospect evaluates and decides | Close rate, proposal-to-signed ratio |
| **6. Revenue Capture** | Decision converts to collected payment | Payment completion rate, first-payment churn |

For each stage, document:
- The **specific asset or mechanism** currently in place (or note its absence)
- The **conversion rate** between this stage and the next (actual or estimated)
- The **ICA-experience question**: "What is the ICA thinking, feeling, and needing at this moment?"

### 3B: Identify Bridge Breaks

Classify every stage transition as one of:

- **🟢 Healthy** — Conversion rate at or above benchmark; mechanism is clear and intentional
- **🟡 Leaking** — Mechanism exists but underperforms benchmark by 20–50%; fixable with optimisation
- **🔴 Broken** — No mechanism, wrong mechanism, or conversion rate below 50% of benchmark; requires structural intervention

Use industry-appropriate benchmarks. For B2B services: Attention→Interest (2–5%), Interest→Trust (15–30%), Trust→Intent (5–15%), Intent→Decision (30–60%), Decision→Revenue (70–90%). Adjust benchmarks based on FutureProof context (industry, price point, sales model).

### 3C: Root-Cause Analysis

For each 🟡 or 🔴 stage, diagnose using the **five conversion friction categories**:

1. **ICA Mismatch** — Attention is reaching people who are not the ICA, so downstream conversion is structurally capped
2. **Message Gap** — The ICA arrives but the message at this stage does not address their current psychological state (wrong pain point, wrong awareness level, wrong proof type)
3. **Mechanism Failure** — The right message reaches the right person but the vehicle is broken (dead links, slow pages, unclear CTAs, too many steps, wrong medium)
4. **Timing Misalignment** — The ask comes too early (insufficient trust) or too late (intent has decayed)
5. **Offer-Market Disconnect** — Everything works until the offer is revealed, and the offer itself does not match what the ICA will pay for at the stated price

Apply any user-specific `instructions` from FutureProof context to weight the diagnosis toward known patterns.

### 3D: Revenue Impact Modelling

Calculate the **revenue impact** of fixing each broken or leaking stage:

- Hold all other stages constant
- Model what happens to end-of-bridge revenue if the target stage improves to benchmark
- Rank fixes by **revenue impact per unit of implementation effort** (high/medium/low effort estimate)

This produces the **Bridge Fix Priority Stack** — the sequenced list of interventions ordered by revenue impact.

## Step 4: Deliver Output

Produce the **Attention-to-Revenue Bridge Report**, containing:

### 4A: Bridge Map (Visual Summary)

A text-based visual diagram showing all six stages, current conversion rates, stage health (🟢🟡🔴), and estimated volume at each stage. Example format:

```
[Attention: 50,000 views/mo]
    → 2.4% →
[Interest: 1,200 engaged/mo] 🟢
    → 22% →
[Trust: 264 subscribers/mo] 🟢
    → 1.1% →
[Intent: 3 calls booked/mo] 🔴 ← PRIMARY BREAK
    → 33% →
[Decision: 1 close/mo] 🟡
    → 100% →
[Revenue: $3,000/mo]
```

### 4B: Diagnostic Summary

For each 🟡 or 🔴 stage:
- **What's happening**: Observable symptoms
- **Why it's happening**: Root cause from the five friction categories
- **What it's costing**: Monthly revenue left on the table (modelled figure)

### 4C: Bridge Fix Priority Stack

Top 3–5 interventions, each specified as:
- **Fix name**: Specific, actionable label
- **Stage targeted**: Which bridge stage this repairs
- **Exact action**: Prescriptive instruction (not "improve your CTA" — instead "Replace the current homepage CTA 'Learn More' with 'Book Your 30-Minute Revenue Audit — Free' and link directly to a Calendly page with three qualifying questions")
- **Expected conversion lift**: From [current] to [target], with revenue impact
- **Implementation effort**: Low / Medium / High with estimated time

### 4D: ICA Journey Narrative

A written first-person narrative (300–500 words) from the ICA's perspective describing their experience moving through the *fixed* bridge — from first encounter to purchase. This serves as the creative brief for all downstream content, copy, and sales asset creation.

### 4E: 30-Day Bridge Repair Roadmap

A week-by-week execution plan:
- **Week 1**: Fix the primary 🔴 break (highest revenue impact intervention)
- **Week 2**: Instrument measurement at every stage transition (specify exact metrics and tools)
- **Week 3**: Optimise the highest-leverage 🟡 stage
- **Week 4**: Validate with data, document new baseline conversion rates

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
FutureProof:save_experiment(skill="attention-to-revenue-bridge", experiment={
  hypothesis: "Inserting a direct intent-activation CTA (book a call / apply now) into the highest-engagement content piece will increase Trust→Intent conversion from [current]% to [target]%",
  variants: ["control: current content with passive CTA or no CTA", "variant: same content with embedded intent-activation CTA and qualifying question"],
  measurement: "Number of hand-raises (calls booked / applications submitted) per 1,000 content views over 14 days",
  expected_impact: "[X]% increase in monthly sales conversations, translating to approximately $[Y] additional monthly revenue at current close rate"
})
```

Generate a second experiment targeting the next-priority bridge break:

```
FutureProof:save_experiment(skill="attention-to-revenue-bridge", experiment={
  hypothesis: "[Stage-specific hypothesis based on secondary break identified in audit]",
  variants: ["control: [current state]", "variant: [proposed intervention]"],
  measurement: "[Stage-specific conversion metric] over [timeframe]",
  expected_impact: "[Quantified revenue or conversion impact]"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="attention-to-revenue-bridge",
  query="Conversion rate benchmarks by industry and price point for content-to-call and call-to-close funnels 2024–2025, with emphasis on [user's industry/model if known from context]",
  reason="Calibrate bridge stage benchmarks to the user's specific market so diagnostic accuracy improves over repeated sessions"
)
```

```
FutureProof:request_research(skill="attention-to-revenue-bridge",
  query="High-performing trust-to-intent bridge mechanisms for [user's business model]: case studies of creators and service providers converting audience attention into booked sales conversations without paid advertising funnels",
  reason="Expand the intervention playbook for the most commonly broken bridge stage (Trust→Intent) with proven, model-specific tactics"
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
FutureProof:save_session(skill="attention-to-revenue-bridge", session={
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