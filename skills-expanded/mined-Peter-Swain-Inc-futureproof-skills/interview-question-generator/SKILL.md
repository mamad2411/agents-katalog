---
name: interview-question-generator
description: |
  Generates a structured, role-specific interview question set with behavioral,
  competency-based, and culture-fit prompts mapped to the hiring scorecard. Use
  when the user says "generate interview questions for this role", "help me
  prepare for an interview with a candidate", "design a structured interview
  guide", or "give me behavioral questions for a senior engineer". For producing
  the questions before the interview, not scoring candidates afterward
  (candidate-screening-scorer).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="interview-question-generator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including prior role profiles, organisational values, competency frameworks, hiring stage preferences, and any established question bank patterns.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Role details** — job title, level (individual contributor / manager / executive), department, and a brief description or job specification
- **Interview stage** — which stage is this question set for? (screening call, hiring manager interview, technical deep-dive, culture-add panel, final/executive round)
- **Key competencies** — what are the 3–5 non-negotiable competencies or attributes for success in this role? (e.g., stakeholder management, analytical rigour, ambiguity tolerance, commercial acumen)
- **Team & culture context** — any specific team dynamics, leadership style, or organisational values the questions should probe for?
- **Constraints** — interview duration, number of interviewers, any compliance or DE&I guidelines to observe (e.g., structured interview mandates, prohibited question categories by jurisdiction)
- **Known hiring pitfalls** — have previous hires in this role or team failed? If so, what went wrong?

## Step 3: Do the Work

### 3a: Role & Competency Mapping

Construct a **Role Success Profile** by mapping the provided inputs against a four-layer competency architecture:

1. **Functional competencies** — technical knowledge and domain-specific skills required to perform the role (e.g., financial modelling, full-stack development, employment law)
2. **Behavioural competencies** — observable behaviours that predict sustained performance (e.g., structured problem-solving, cross-functional influence, resilience under ambiguity)
3. **Culture-add indicators** — attributes that complement and strengthen existing team composition rather than replicate it (e.g., constructive dissent, diverse perspective-taking, initiative beyond scope)
4. **Role-specific risk factors** — failure modes observed in the role archetype or flagged by the user (e.g., inability to manage up, over-indexing on execution vs. strategy, poor delegation at managerial level)

### 3b: Question Design Methodology

For each competency in the Role Success Profile, generate questions using the following hierarchy (in order of predictive validity):

| Question Type | When to Use | Structure |
|---|---|---|
| **Behavioural (STAR-anchored)** | Default for all behavioural and culture-add competencies | "Tell me about a time when…" — requires Situation, Task, Action, Result |
| **Situational / Hypothetical** | When the candidate may lack direct prior experience (e.g., first-time managers, career pivots) | "Imagine you are faced with…" — evaluates reasoning framework and judgment |
| **Technical / Case-based** | For functional competencies requiring demonstrable skill | Role-relevant scenario with a defined problem to solve or analyse |
| **Motivational / Values-based** | For culture-add and intrinsic driver assessment | "What matters to you about…" — probes alignment with organisational purpose |
| **Contrary evidence probes** | Mandatory follow-up for every lead question | "Now tell me about a time that didn't go as planned…" — mitigates confirmation bias |

Apply the following quality filters to every question:

- **Legality check** — exclude any question that directly or indirectly solicits information about protected characteristics (age, marital status, religion, disability, national origin, etc.) under applicable jurisdiction
- **Bias mitigation** — avoid questions that advantage candidates from specific socio-economic, educational, or cultural backgrounds without job-relevant justification
- **Differentiation power** — discard any question where a mediocre and exceptional candidate would likely give indistinguishable answers
- **Scorability** — each question must be paired with an evaluation rubric enabling consistent scoring across interviewers

Apply any user-specific `instructions` from FutureProof context (e.g., preferred question styles, banned clichés, company-specific competency language, interviewer experience level adjustments).

### 3c: Interview Architecture

Structure the question set into a coherent **Interview Flow** appropriate to the stated stage and duration:

1. **Opening frame** (2–3 min) — rapport-building opener and agenda-setting language for the interviewer
2. **Core competency blocks** — 2–4 blocks, each containing a lead question, a planned follow-up probe, and a contrary evidence probe, mapped to specific competencies
3. **Candidate questions window** — suggested time allocation and guidance on evaluating the quality of questions the candidate asks
4. **Closing frame** — next-steps language and candidate experience best practices

## Step 4: Deliver Output

Produce a structured **Interview Question Guide** containing:

### A. Role Success Profile (1-page summary)
- Role title, level, stage
- Competency matrix across the four layers with priority weighting (critical / important / nice-to-have)
- Identified risk factors

### B. Interview Question Set
For each competency block:
- **Competency assessed**: named and defined
- **Lead question**: full wording
- **Planned follow-up probe**: specific dig-deeper question
- **Contrary evidence probe**: full wording
- **Evaluation rubric**: 3-level scoring guide (Strong / Acceptable / Concern) with behavioural indicators for each level
- **Red flags**: specific responses or patterns that should trigger concern
- **Green flags**: specific responses or patterns that indicate exceptional fit

### C. Interviewer Briefing Notes
- Suggested time allocation per block
- Scoring instructions (independent scoring before debrief to prevent anchoring bias)
- Legal and compliance reminders relevant to the stated jurisdiction
- Calibration notes: what "good" looks like for this specific role and level

### D. Scorecard Template
- Tabular format: competency | score (1–5) | evidence notes | flags
- Overall recommendation field: Advance / Hold / Decline
- Space for interviewer confidence rating on each competency

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
FutureProof:save_experiment(skill="interview-question-generator", experiment={
  hypothesis: "Adding a contrary evidence probe to each competency block reduces false-positive hire rates by surfacing candidate limitations earlier",
  variants: ["control: standard behavioural questions only", "variant: behavioural + mandatory contrary evidence probe per block"],
  measurement: "Interviewer confidence-to-outcome correlation and 90-day new hire performance ratings across next 20 hires using each format",
  expected_impact: "25% reduction in regretted hires within first 6 months"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="interview-question-generator",
  query="Latest structured interviewing research 2024: predictive validity of behavioural vs situational questions by role level, emerging DE&I-compliant assessment techniques, and high-signal question patterns from IO psychology literature",
  reason="Ensure question design methodology reflects current evidence on interview predictive validity and evolving legal and ethical standards in talent assessment"
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
FutureProof:save_session(skill="interview-question-generator", session={
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