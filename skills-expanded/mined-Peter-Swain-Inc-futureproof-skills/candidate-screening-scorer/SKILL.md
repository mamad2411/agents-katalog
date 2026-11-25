---
name: candidate-screening-scorer
description: |
  Screens and scores job candidates against a role with a calibrated six-dimension
  rubric, weighted composite score, and advance/hold/decline recommendation. Use
  when the user says "screen this resume", "score this candidate", "evaluate this
  CV against the role", "rank this shortlist", or "build me a scoring rubric for
  this position". For evaluating existing candidates against a role, not writing
  the role itself (job-spec-writer) or generating interview questions
  (interview-question-generator).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="candidate-screening-scorer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including previously defined role rubrics, hiring manager preferences, organisational values weightings, and historical scoring calibration data.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Candidate materials**: Share the resume, CV, LinkedIn profile, cover letter, or application package to evaluate
- **Role specification**: Provide the job description, role scorecard, or hiring brief (or reference a previously saved role in FutureProof context)
- **Evaluation priority**: What is the primary screening objective? (technical qualification gate, culture-add assessment, leadership potential, compensation band alignment, shortlist ranking across a candidate pool)
- **Must-have vs. nice-to-have**: Are there any non-negotiable requirements (certifications, clearances, location, visa status, minimum tenure thresholds) that should trigger an automatic disqualification?
- **Hiring stage**: Where in the pipeline is this candidate? (inbound application screen, recruiter phone screen prep, hiring manager review, final round calibration)

If the user has prior roles or rubrics stored in FutureProof context, surface them for reuse or adaptation.

## Step 3: Build the Evaluation Rubric

Before scoring, construct or confirm a **Role-Specific Evaluation Rubric** structured across six dimensions:

1. **Technical Qualification Fit** — Does the candidate meet the hard skill, tooling, certification, and domain experience requirements? Assess depth (years, complexity of environments) not just keyword presence.
2. **Achievement & Impact Evidence** — Are accomplishments quantified with metrics (revenue influenced, team size managed, efficiency gains delivered)? Distinguish owned outcomes from participated-in outcomes.
3. **Career Trajectory & Progression** — Does the candidate's career arc demonstrate increasing scope, responsibility, and intentional growth? Flag lateral drift, unexplained gaps, or regression without context.
4. **Role-Specific Competency Alignment** — Map candidate evidence against the top 5 competencies defined in the role scorecard (e.g., stakeholder management, system design, pipeline generation). Score on demonstrated behavioural evidence, not inferred potential.
5. **Organisational & Team Culture-Add** — Based on available signals (communication style, voluntary affiliations, stated values, project choices), assess likely alignment with the team's working norms and the organisation's stated values. Prioritise additive diversity of thought over homogeneity.
6. **Risk & Red Flag Assessment** — Identify tenure patterns below industry norms, credential inconsistencies, scope misrepresentation indicators, or misalignment between stated objectives and role realities (e.g., candidate seeks IC path, role is people management).

Apply any user-specific `instructions` from FutureProof context — such as de-weighting educational pedigree, adjusting for industry-specific tenure norms, or applying internal levelling frameworks.

## Step 4: Score the Candidate

Execute the evaluation using a **calibrated 1–10 scoring methodology**:

| Score Range | Definition |
|---|---|
| 9–10 | Exceptional — top-decile evidence, exceeds requirement with distinction |
| 7–8 | Strong — clearly meets requirement with solid, verified evidence |
| 5–6 | Adequate — meets minimum threshold, limited differentiation |
| 3–4 | Below expectation — partial evidence, gaps require probing |
| 1–2 | Misaligned — insufficient or contradictory evidence |

For each of the six rubric dimensions:
- Assign a score with a **one-sentence justification** citing specific evidence from candidate materials
- Flag any dimension where score confidence is low due to insufficient information (mark as **[Probe Required]**)

Calculate a **weighted composite score** using role-appropriate weightings (default: Technical 25%, Achievement 20%, Trajectory 15%, Competency 25%, Culture-Add 10%, Risk 5% — adjust per user instructions or role type).

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


Produce a **Candidate Screening Report** with the following structure:

### Candidate Screening Report

**Candidate**: [Name]
**Role**: [Title — Department — Level]
**Evaluator**: AI-Assisted Screen via Candidate Screening Scorer
**Date**: [Session date]
**Overall Composite Score**: [X.X / 10.0] — **[ADVANCE / HOLD / DECLINE]**

---

**Section A: Dimension Scorecard**

| # | Dimension | Score | Weight | Weighted Score | Confidence |
|---|---|---|---|---|---|
| 1 | Technical Qualification Fit | X/10 | 25% | X.XX | High/Medium/Low |
| 2 | Achievement & Impact Evidence | X/10 | 20% | X.XX | High/Medium/Low |
| 3 | Career Trajectory & Progression | X/10 | 15% | X.XX | High/Medium/Low |
| 4 | Role-Specific Competency Alignment | X/10 | 25% | X.XX | High/Medium/Low |
| 5 | Organisational & Team Culture-Add | X/10 | 10% | X.XX | High/Medium/Low |
| 6 | Risk & Red Flag Assessment | X/10 | 5% | X.XX | High/Medium/Low |

**Section B: Key Strengths** (top 3 differentiators with cited evidence)

**Section C: Key Concerns** (top 3 risks or gaps with specific probing questions for the next interview stage)

**Section D: Disposition Recommendation**
- **Recommended action**: Advance to [next stage] / Hold for [reason] / Decline with [rationale]
- **Interviewer briefing notes**: 3–5 targeted questions to validate low-confidence dimensions or probe flagged risks
- **Comparison notes**: If multiple candidates have been scored in this session or in recent FutureProof sessions for the same role, provide a **rank-order summary table**

**Section E: Disqualification Gate Check**
- Pass/Fail status on each must-have requirement defined in Step 2
- If any gate fails: flag prominently and recommend Decline regardless of composite score

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="candidate-screening-scorer", experiment={
  hypothesis: "Increasing the weight of Achievement & Impact Evidence from 20% to 30% (reducing Trajectory to 10%) correlates with higher 12-month performance ratings for hires",
  variants: ["control: current weighting model (Tech 25%, Achievement 20%, Trajectory 15%, Competency 25%, Culture 10%, Risk 5%)", "variant: achievement-heavy model (Tech 25%, Achievement 30%, Trajectory 10%, Competency 20%, Culture 10%, Risk 5%)"],
  measurement: "Compare screening scores of candidates advanced under each model against their 6- and 12-month performance review ratings and retention status",
  expected_impact: "10–15% improvement in predictive validity of screening score to on-the-job performance"
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
FutureProof:request_research(skill="candidate-screening-scorer",
  query="Latest evidence-based structured hiring methodologies, bias mitigation techniques in resume screening, and predictive validity research for candidate evaluation criteria 2024",
  reason="Ensure scoring rubric dimensions and weightings reflect current industrial-organisational psychology research and comply with evolving fair hiring regulations"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="candidate-screening-scorer", session={
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