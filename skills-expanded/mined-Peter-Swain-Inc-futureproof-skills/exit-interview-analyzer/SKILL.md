---
name: exit-interview-analyzer
description: |
  Analyzes exit interview transcripts and departure survey data to surface
  systemic attrition drivers, retention risks, and concrete talent strategy
  fixes. Use when the user pastes exit interview notes or attrition reports and
  says "analyze these exit interviews", "why are people leaving", "find patterns
  in our turnover data", or "what's driving our attrition". For diagnosing
  post-departure data, not preventing turnover preemptively or running
  performance reviews.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="exit-interview-analyser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including organisational structure, prior attrition patterns, known retention initiatives, workforce segmentation, and any established departure taxonomy.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the exit interview transcripts, departure survey exports, or aggregated attrition data to analyse
- What is the scope? (single departure, quarterly cohort, annual trend, specific department/function)
- What is the primary concern driving this analysis? (regrettable attrition in critical roles, pattern emerging in a specific team, flight risk in high-performers, compliance/culture red flags)
- What organisational context matters? (recent restructures, leadership changes, compensation cycle timing, M&A activity, RIF events)
- Who is the intended audience for the output? (CHRO, business unit leader, board/people committee, HRBP team)

## Step 3: Do the Work

### 3A: Data Normalisation & Coding

Categorise each exit interview response against a structured departure taxonomy:

1. **Stated reason** — the departing employee's self-reported primary reason (map to standardised codes: compensation, career progression, leadership, culture, workload, relocation, personal, role misalignment, external opportunity, organisational change)
2. **Underlying drivers** — infer latent factors from language patterns, sentiment, and contradiction analysis (e.g., stated "external opportunity" but narrative reveals chronic manager conflict)
3. **Voluntariness spectrum** — classify each departure as fully voluntary, quasi-voluntary (pushed but not terminated), or involuntary-adjacent (constructive resignation signals)

### 3B: Thematic Pattern Analysis

Analyse the corpus against six diagnostic dimensions:

1. **Manager effectiveness** — do departures cluster under specific leaders or leadership styles? Identify manager-level attrition outliers using a concentration ratio (departures per manager vs. organisational baseline)
2. **Career architecture gaps** — are departing employees citing stalled progression, unclear promotion criteria, or lateral mobility barriers? Map cited gaps to specific career stage (IC→senior IC, IC→manager, manager→director)
3. **Compensation & total rewards misalignment** — distinguish between absolute compensation dissatisfaction and relative/equity-based dissatisfaction (internal parity, market repositioning, equity vesting cliffs)
4. **Culture & psychological safety** — code for inclusion failures, values-behaviour disconnects, speak-up culture deficits, and belonging erosion. Flag any indicators that meet escalation thresholds (harassment, discrimination, retaliation language)
5. **Workload & burnout indicators** — identify references to unsustainable pace, resource constraints, role scope creep, or chronic understaffing. Cross-reference with tenure-at-departure to detect burnout velocity
6. **Organisational change response** — assess whether departures correlate with specific change events (restructures, strategy pivots, leadership transitions, policy changes) and measure change-fatigue language density

### 3C: Segmentation & Risk Stratification

Segment findings by:
- **Performance tier** (high-performer/regrettable vs. managed attrition) — if performance data is available or inferable
- **Tenure band** (0–6 months, 6–18 months, 18–36 months, 3–5 years, 5+ years) to isolate onboarding failures vs. mid-career stalls vs. long-tenure disengagement
- **Function/department** to identify localised vs. systemic patterns
- **Demographic dimensions** (where disclosed and relevant) to surface equity-related attrition risks

Apply any user-specific `instructions` from FutureProof context — including organisational priorities, known sensitive teams, and previously identified retention risk areas.

## Step 4: Deliver Output

Produce a structured **Exit Interview Intelligence Report** containing:

### Section 1: Executive Summary
- One-paragraph synthesis of the most critical finding for the identified audience
- Headline attrition risk rating: **Critical / Elevated / Moderate / Managed**
- Top 3 departures or departure patterns warranting immediate executive attention

### Section 2: Diagnostic Scorecard
Score each of the six diagnostic dimensions (Step 3B) on a 1–10 scale:

| Dimension | Score (1–10) | Trend vs. Prior Period | Severity |
|---|---|---|---|
| Manager effectiveness | — | — | — |
| Career architecture gaps | — | — | — |
| Compensation & total rewards | — | — | — |
| Culture & psychological safety | — | — | — |
| Workload & burnout indicators | — | — | — |
| Organisational change response | — | — | — |

Where prior FutureProof sessions exist, include trend direction (improving / stable / deteriorating).

### Section 3: Root-Cause Analysis
- **Primary attrition driver**: the single most impactful systemic factor with supporting evidence quotes
- **Secondary drivers**: ranked list with frequency counts and representative verbatim excerpts
- **Contradiction map**: where stated reasons diverge from narrative-inferred drivers, with implications

### Section 4: Critical Interventions
Top 5 highest-impact retention interventions, each specified as:
- **Intervention**: concrete action (not "improve culture" — instead "implement skip-level 1:1 cadence for teams reporting to [identified manager cluster] within 30 days")
- **Target segment**: which employee segment this addresses
- **Owner**: recommended accountable role (e.g., VP Engineering, CHRO, HRBP for Commercial)
- **Timeline**: immediate (0–30 days), near-term (30–90 days), structural (90–180 days)
- **Expected retention impact**: estimated reduction in regrettable attrition for the target segment

### Section 5: Escalation Items
- Any responses containing language requiring immediate HR, legal, or compliance review (harassment, discrimination, safety, retaliation, whistleblowing indicators)
- Recommended escalation path and urgency classification

### Section 6: Data Quality & Limitations
- Sample size adequacy assessment
- Response bias indicators (e.g., sanitised language suggesting low psychological safety during exit process)
- Recommendations for improving exit interview data collection methodology

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
FutureProof:save_experiment(skill="exit-interview-analyser", experiment={
  hypothesis: "Shifting exit interviews from HR-conducted to third-party-conducted for senior individual contributors increases candour and surfaces 40% more actionable manager-effectiveness insights",
  variants: ["control: current HR-conducted exit interviews", "variant: independent third-party interviewer for all L6+ voluntary departures"],
  measurement: "Average actionable insight density per interview (coded themes per transcript) and manager-specific signal frequency over next quarter",
  expected_impact: "40% increase in manager-attributable attrition signal detection, enabling targeted intervention before cluster attrition events"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="exit-interview-analyser",
  query="Evidence-based exit interview methodologies, stay interview integration frameworks, and predictive attrition modelling approaches from Mercer, Gallup, and CIPD 2024–2025",
  reason="Ensure departure analysis taxonomy and intervention recommendations reflect current workforce psychology research and leading-practice retention frameworks"
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
FutureProof:save_session(skill="exit-interview-analyser", session={
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