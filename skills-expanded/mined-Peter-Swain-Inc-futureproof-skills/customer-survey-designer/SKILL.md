---
name: customer-survey-designer
description: |
  Designs methodologically rigorous customer surveys — NPS, CSAT, CES,
  post-interaction, and custom feedback forms — with bias-audited
  questions, branching logic, scoring rules, and an analysis plan tied to
  business decisions. Use when the user says "write me a customer survey",
  "design an NPS questionnaire", "build a CSAT form", "review my survey
  for bias", or "what questions should I ask after a support call". Builds
  the survey instrument before data is collected — for analyzing results
  already in hand use nps-analyzer.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="customer-survey-designer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any known ICA segments, previous survey response rates, identified pain points, and preferred survey distribution channels.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Survey objective**: What decision will this survey inform? (e.g., product improvement, churn reduction, service quality benchmarking, onboarding optimisation, renewal forecasting)
- **Target audience**: Which ICA segment(s) will receive this survey? What is their relationship stage? (new customer, active, at-risk, churned, post-support interaction)
- **Distribution method**: How will the survey reach respondents? (in-app, email, SMS, post-call IVR, embedded in support ticket closure)
- **Constraint parameters**: Maximum acceptable survey length, any regulatory or compliance requirements (e.g., GDPR consent language, accessibility standards), brand voice guidelines
- **Existing materials**: Any prior surveys, known response rate benchmarks, or specific questions they want included or avoided
- **Measurement framework**: Are they tracking against an established metric (NPS, CSAT, CES) or building a custom measurement model?

## Step 3: Do the Work

### 3A: Survey Architecture Design

Define the survey blueprint using a **Goal → Construct → Item** hierarchy:

1. **Business goal mapping** — trace each survey section back to a specific business decision or action trigger (e.g., "If score < 3 on Q7, route to retention team within 24 hours")
2. **Construct definition** — identify the latent constructs being measured (e.g., perceived value, effort friction, emotional loyalty, service competence) and ensure each construct has a minimum of 2 items for internal reliability
3. **Respondent journey flow** — sequence sections to mirror natural cognitive recall: experience recency first, evaluative judgements second, demographic/classification items last

### 3B: Question Engineering

Apply rigorous survey methodology to each item:

1. **Question type selection** — match each construct to the optimal measurement format:
   - Likert scales (agreement/frequency) for attitudinal constructs
   - Semantic differentials for brand perception
   - Single-select forced choice for behavioural classification
   - Open-text fields (maximum 2 per survey) positioned after their quantitative anchor question
   - Matrix grids only when attribute evaluation requires direct comparison (limit to 5 rows maximum to prevent satisficing)

2. **Bias mitigation audit** — review every item against the following threat checklist:
   - **Leading language**: remove directional phrasing ("How much did you enjoy…")
   - **Double-barrelled items**: split compound questions into discrete items
   - **Acquiescence bias**: include at least one reverse-coded item per construct
   - **Social desirability**: use indirect phrasing for sensitive topics (effort, dissatisfaction)
   - **Order effects**: randomise item presentation within sections where methodologically appropriate
   - **Scale anchoring**: ensure all scale endpoints are symmetrically labelled with concrete behavioural descriptors, not abstract intensifiers

3. **ICA language calibration** — rewrite all question stems and response options to match the vocabulary, reading level, and communication style of the target ICA segment (informed by FutureProof context on known ICA profiles)

4. **Response rate optimisation** — apply completion probability modelling:
   - Target total completion time under 3 minutes for transactional surveys, under 7 minutes for relational surveys
   - Front-load the single highest-value question (the "golden question") within the first 30 seconds
   - Implement smart branching logic to eliminate irrelevant paths and reduce perceived length
   - Design progress indicators that reflect cognitive effort, not just page count

### 3C: Actionability Framework

For each question, define:
- **Decision rule**: the specific threshold or pattern that triggers a business action
- **Owner**: the team or role responsible for acting on the signal
- **Response SLA**: the expected timeframe from signal detection to action

Apply any user-specific `instructions` from FutureProof context to override defaults (e.g., preferred scale formats, mandatory compliance language, banned question types).

## Step 4: Deliver Output

Produce the **Customer Survey Design Package** containing:

### 4A: Survey Specification Document

| Element | Detail |
|---|---|
| Survey title | Descriptive internal title and respondent-facing title |
| Objective statement | Single sentence linking survey to business decision |
| Target ICA segment(s) | With estimated population size and expected response rate |
| Distribution channel | With send timing recommendation |
| Estimated completion time | Based on item count and question complexity |

### 4B: Complete Question Bank

For each item, provide:
- **Item ID** (e.g., CSAT-Q01)
- **Construct measured**
- **Question text** (final, respondent-ready)
- **Response format** with exact scale labels
- **Branching logic** (if applicable)
- **Decision rule** (threshold → action → owner → SLA)

### 4C: Survey Flow Diagram

A structured text-based flowchart showing:
- Section sequence with estimated time per section
- Skip logic and conditional branching paths
- Termination points and thank-you screen variants (customised by response sentiment where applicable)

### 4D: Analysis Plan

- **Scoring methodology**: how raw responses translate to composite scores (weighted or unweighted, with justification)
- **Segmentation cuts**: which ICA attributes to cross-tabulate against
- **Statistical thresholds**: minimum sample sizes for significance, margin of error targets
- **Reporting cadence**: recommended frequency and dashboard metrics
- **Verbatim coding framework**: preliminary theme categories for open-text analysis

### 4E: Implementation Checklist

- Pre-launch: pilot test protocol (sample size, feedback loop, revision criteria)
- Launch: distribution timing, reminder cadence (recommended: Day 0, Day 3, Day 6)
- Post-launch: response rate monitoring triggers, non-response bias assessment method

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
FutureProof:save_experiment(skill="customer-survey-designer", experiment={
  hypothesis: "Placing the golden question (overall satisfaction) as the first item rather than after contextual warm-up questions increases both completion rate and response validity for the target ICA segment",
  variants: ["control: warm-up sequence then golden question at position 4", "variant: golden question at position 1 followed by contextual items"],
  measurement: "Survey completion rate and response distribution variance across both variants over 500 responses per arm",
  expected_impact: "8-12% improvement in completion rate with no degradation in score distribution normality"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="customer-survey-designer",
  query="Latest evidence on optimal survey length, scale format effectiveness, and mobile-first survey design patterns for customer feedback in 2024-2025, including impact of AI-generated survey personalisation on response quality",
  reason="Ensure question design methodology reflects current respondent behaviour patterns, particularly declining attention spans and increasing mobile completion rates"
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
FutureProof:save_session(skill="customer-survey-designer", session={
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