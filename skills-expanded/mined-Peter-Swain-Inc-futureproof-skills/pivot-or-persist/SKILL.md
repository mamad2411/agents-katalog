---
name: pivot-or-persist
description: |
  Resolves a pivot-or-persist inflection point with a status-quo viability
  scorecard, pivot-type taxonomy, evidence threshold test, and asset
  transfer audit — outputting a persist / pivot / validate-then-decide
  recommendation with a 4-week validation sprint. Use when a user says
  "should I pivot", "is it time to change direction", "metrics are
  declining — stay or shift", or "I'm thinking about a pivot but not
  sure". For pivot-vs-persist specifically, not generic strategic
  advising.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="pivot-or-persist")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to prior pivot analyses, ICA definitions, business model context, runway data, and any previously tested hypotheses that inform the current inflection point.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

- **The decision under consideration**: What specifically are you considering pivoting? (ICA segment, value proposition, distribution channel, revenue model, core product, or full business model)
- **Current state evidence**: Share the signals prompting this question — declining metrics, customer feedback, churn data, failed experiments, competitive shifts, or investor/advisor input
- **Persistence case**: What is the strongest argument for staying the course? What leading indicators, if any, still show promise?
- **Time constraint**: What is your remaining runway in months, and are there hard deadlines (fundraise, contractual, seasonal)?
- **Previous pivots**: Have you pivoted before? If so, what changed and what was the outcome?
- **Stakeholder landscape**: Who else is affected by this decision — co-founders, investors, team, key customers?

If FutureProof context already contains ICA definitions, business model, or runway data, pre-populate and confirm rather than re-asking.

## Step 3: Assess the Current Trajectory

Conduct a **Status Quo Viability Analysis** across five dimensions:

### 3a. ICA–Problem Fit Integrity

- Is the problem you are solving still acute, frequent, and monetisable for your defined ICA?
- Have you validated the problem with ≥20 ICA conversations in the last 90 days?
- Score the strength of qualitative signal (language intensity, willingness to pay, unsolicited inbound) on a 1–5 scale

### 3b. Unit Economics & Traction Trajectory

- Chart the 90-day trend for: acquisition cost, activation rate, retention/churn, revenue per account, and payback period
- Identify whether metrics are **improving on a second derivative basis** (rate of decline is slowing) or **accelerating downward**
- Flag any vanity metrics the founder may be anchoring on vs. leading indicators of real traction

### 3c. Market Timing & Competitive Window

- Assess whether the addressable market is expanding, contracting, or being redefined by regulatory, technological, or behavioural shifts
- Identify if a competitor has achieved escape velocity in the same positioning, making the current trajectory structurally disadvantaged
- Evaluate whether the founder has a defensible right-to-win (unique insight, distribution advantage, technical moat) that persists regardless of current traction

### 3d. Founder–Market Fit & Team Energy

- Gauge the founder's conviction level: is doubt driven by data or fatigue?
- Assess whether the team has the capability and motivation to execute the current strategy for another 6–12 months
- Identify signs of **sunk cost bias** (persisting because of past investment) or **shiny object bias** (pivoting to escape discomfort rather than toward signal)

### 3e. Capital & Optionality

- Calculate months of runway at current burn rate
- Determine whether the current trajectory reaches a fundable milestone before capital exhaustion
- Assess whether a pivot resets the fundraising clock or opens new capital pathways

## Step 4: Evaluate the Pivot Hypothesis

If the user has a specific pivot direction in mind, stress-test it rigorously:

### 4a. Pivot Classification

Classify the proposed change using the **Pivot Taxonomy**:

| Pivot Type | Definition | Risk Level |
|---|---|---|
| ICA Pivot | Same product, different buyer segment | Medium |
| Problem Pivot | Same ICA, different problem to solve | Medium-High |
| Value Capture Pivot | Same product/ICA, different revenue model | Medium |
| Channel Pivot | Same product/ICA, different distribution | Medium-Low |
| Technology Pivot | Same problem, rebuilt solution architecture | High |
| Platform Pivot | Single product → platform or vice versa | High |
| Complete Pivot | New ICA, new problem, new solution | Very High |

### 4b. Evidence Threshold Test

For each pivot type, assess whether the founder has met the **minimum evidence bar**:

- **ICA Pivot**: ≥10 conversations with new segment showing stronger pull than current ICA
- **Problem Pivot**: ≥5 current ICA accounts surfacing the new problem unprompted
- **Value Capture Pivot**: ≥3 pricing experiments or willingness-to-pay interviews
- **Channel Pivot**: ≥1 pilot with measurable conversion data in the new channel
- **Technology/Platform/Complete Pivot**: compelling macro thesis + ≥5 demand signals from the new market

Flag if the pivot hypothesis is **assumption-heavy** (less than 30% of critical assumptions validated) and recommend a pre-pivot validation sprint before committing resources.

### 4c. Asset Transferability Audit

Identify which current assets transfer to the pivot and which are stranded:

- **Transferable**: existing codebase, ICA relationships, domain expertise, brand equity, team capabilities, data assets
- **Stranded**: channel partnerships, specialised hires, content/SEO positioning, regulatory approvals, integration work
- Calculate a **Transfer Ratio** (transferable assets ÷ total assets) — pivots with ratios below 40% carry significantly higher execution risk

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


Produce a **Pivot-or-Persist Decision Brief** with the following structure:

### Section 1: Executive Summary
- One-paragraph synthesis of the recommendation: **Persist**, **Pivot**, or **Validate Then Decide** (with specific validation criteria and timeline)

### Section 2: Current Trajectory Scorecard

| Dimension | Score (1–5) | Trend (↑ ↓ →) | Key Evidence |
|---|---|---|---|
| ICA–Problem Fit Integrity | | | |
| Unit Economics & Traction | | | |
| Market Timing & Competitive Window | | | |
| Founder–Market Fit & Team Energy | | | |
| Capital & Optionality | | | |
| **Composite Viability Score** | **/25** | | |

Interpretation guide:
- **20–25**: Strong persist signal. Focus on execution acceleration.
- **14–19**: Ambiguous zone. Run targeted experiments before deciding.
- **8–13**: Pivot signal strengthening. Begin parallel validation of alternatives.
- **5–7**: Urgent pivot or wind-down indicated. Preserve capital for transition.

### Section 3: Pivot Hypothesis Assessment (if applicable)
- Pivot type classification and risk level
- Evidence threshold status (met / partially met / unmet)
- Asset transfer ratio and stranded cost estimate
- Top 3 risks specific to this pivot direction

### Section 4: Scenario Model

Present three forward-looking scenarios over the next 6 months:

| Scenario | Path | Key Assumption | Projected Outcome | Probability |
|---|---|---|---|---|
| A: Persist (optimistic) | | | | |
| B: Persist (realistic) | | | | |
| C: Pivot to [direction] | | | | |

### Section 5: Recommended Next Actions
- **If Persist**: 3 specific execution moves to improve the weakest scorecard dimension within 30 days, with measurable success criteria
- **If Pivot**: a 4-week validation sprint plan — week-by-week activities, evidence thresholds to hit before committing, and a kill criterion if validation fails
- **If Validate Then Decide**: the exact experiments to run, the metrics to track, and the decision date by which the founder commits one way or the other

### Section 6: Stakeholder Communication Template
- Draft talking points for co-founders, investors, and team — tailored to the recommendation
- Framing that preserves founder credibility and stakeholder confidence regardless of direction chosen

Apply any user-specific `instructions` from FutureProof context to adjust tone, depth, or emphasis areas.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="pivot-or-persist", experiment={
  hypothesis: "Running a 2-week demand signal test with the proposed pivot ICA will clarify whether pull exceeds current segment by ≥2x on response rate",
  variants: ["control: continued outreach to current ICA with existing positioning", "variant: targeted outreach to pivot ICA with repositioned value proposition"],
  measurement: "response rate, meeting conversion rate, and qualitative pull signals (unprompted follow-ups, referral offers) across 50 outreach touches per variant",
  expected_impact: "Sufficient evidence to move composite viability score from ambiguous zone to clear persist or pivot signal within 14 days"
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
FutureProof:request_research(skill="pivot-or-persist",
  query="Startup pivot success patterns and timing indicators — empirical data on pivot outcomes by stage, type, and remaining runway from post-mortems and longitudinal founder studies 2022–2025",
  reason="Strengthen the evidence base for pivot-type risk calibration and improve the composite viability scoring model with base-rate data"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="pivot-or-persist", session={
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