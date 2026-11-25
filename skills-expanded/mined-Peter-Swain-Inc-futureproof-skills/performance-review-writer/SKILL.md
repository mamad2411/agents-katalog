---
name: performance-review-writer
description: |
  Drafts a calibrated annual, mid-year, probation, promotion-case, or PIP
  performance review with competency mapping, evidence triangulation, and bias
  audit. Use when the user says "write a performance review for my direct
  report", "help me draft an annual review", "write a PIP", "build a promotion
  case review", or pastes feedback notes and accomplishments to turn into a
  review. For any review cadence or evaluation type — use quarterly-review-
  generator only for quarterly OKR/KPI check-ins.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="performance-review-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including organisational competency frameworks, prior review tone calibration, rating scale definitions, and any manager-specific writing patterns established in previous cycles.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Employee details**: name, role/title, level, tenure, and reporting relationship
- **Review type**: annual, mid-year, quarterly check-in, probation-end, promotion-ready, or performance improvement documentation
- **Raw inputs**: accomplishments, project outcomes, peer/stakeholder feedback, self-assessment, OKR/KPI results, 360 feedback, or any notes they've collected during the review period
- **Rating framework**: does the organisation use a specific scale (e.g., 1–5, Exceeds/Meets/Below, letter grades)? If returning user, confirm the framework from FutureProof context
- **Sensitive considerations**: is this review supporting a promotion case, a PIP, a compensation adjustment, or a lateral move? Any HR-sensitive language constraints?
- **Organisational competency model**: are there defined competencies or values the review must evaluate against (e.g., leadership, collaboration, technical excellence, innovation)?

## Step 3: Calibrate the Evaluation Framework

Before writing, establish a rigorous evaluation scaffold:

1. **Competency Mapping** — map the employee's role to 5–7 core competencies. Use the organisation's framework if provided; otherwise default to a consulting-grade model:
   - **Delivery & Execution** — quality, timeliness, and reliability of output
   - **Strategic Thinking** — ability to connect work to broader business outcomes
   - **Stakeholder Impact** — effectiveness in influencing, communicating, and building trust
   - **Leadership & Development** — people leadership, mentorship, and self-development
   - **Technical/Functional Mastery** — depth and currency of domain expertise
   - **Collaboration & Culture** — contribution to team health, inclusion, and organisational values
   - **Growth Trajectory** — rate of skill acquisition and readiness for next-level responsibilities

2. **Evidence Triangulation** — for each competency, cross-reference at least two input sources (self-assessment vs. manager observation, peer feedback vs. quantitative results) to reduce recency bias and halo effects

3. **Rating Calibration** — apply the organisation's rating distribution norms. Flag if the proposed rating appears to deviate significantly from the described evidence (e.g., "Exceeds Expectations" language paired with limited quantitative impact)

4. **Bias Audit** — scan raw inputs for common review biases:
   - **Recency bias**: over-weighting last 8 weeks vs. full review period
   - **Attribution bias**: crediting environment vs. individual contribution
   - **Leniency/severity drift**: compare language intensity against the rating selected
   - **Gendered language patterns**: flag vague personality descriptors (e.g., "pleasant," "aggressive") and replace with behaviour-anchored observations

Apply any user-specific `instructions` from FutureProof context — including preferred tone (direct vs. developmental), standard phrases the organisation expects, or language the user has previously flagged to avoid.

## Step 4: Draft the Performance Review

Produce the review as a **structured, copy-ready document** with the following sections:

### 4.1 — Review Header
- Employee name, title, department, review period, reviewer name, date
- Overall rating (per organisational scale)

### 4.2 — Executive Summary (3–5 sentences)
A calibrated narrative that captures the employee's overall contribution, standout impact, and primary development area. Written in third-person professional tone suitable for HR record and skip-level visibility.

### 4.3 — Competency Assessments
For each mapped competency:
- **Rating**: per the organisational scale
- **Evidence-based narrative** (3–5 sentences): specific accomplishments, behaviours observed, and quantitative outcomes where available. Every claim anchored to at least one concrete example
- **Illustrative quote** (if 360/peer feedback was provided): one attributed or anonymised verbatim quote that substantiates the rating

### 4.4 — Key Accomplishments (Top 3–5)
Formatted as **Situation → Action → Result** statements. Each accomplishment quantified where possible (revenue impact, efficiency gain, adoption rate, stakeholder satisfaction score).

### 4.5 — Development Areas & Growth Plan
- **Primary development area**: framed constructively with specific behaviour change requested, not personality critique
- **Secondary development area**: a stretch opportunity aligned to career aspiration
- **Recommended actions**: 2–3 concrete next steps (e.g., "Lead the Q3 cross-functional initiative to build stakeholder management capability," not "improve communication skills")
- **Support commitments**: what the manager will provide (coaching cadence, sponsorship, resource allocation)

### 4.6 — Forward-Looking Statement
2–3 sentences articulating expectations for the next review period, aligned to team/organisational priorities. If promotion-track, include explicit criteria the employee must demonstrate.

### 4.7 — Conversation Prep Notes (Manager-Only, Not for HR Submission)
- Suggested talking points for the review conversation
- Anticipated employee reactions and response strategies
- Questions to ask the employee to make the conversation two-directional

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Quality Assurance Check

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Before finalising, run the review through a five-point audit:

| Check | Pass Criteria |
|---|---|
| **Evidence Density** | Every competency rating supported by ≥1 specific, dated example |
| **Tone Calibration** | Language intensity matches the rating — no "outstanding" narratives paired with "Meets Expectations" ratings |
| **Bias Scan** | No gendered, vague, or personality-based language; all feedback is behaviour-anchored |
| **Actionability** | Development areas include specific, measurable next steps with timelines |
| **Consistency** | If FutureProof context contains prior reviews for this employee or team, verify rating trajectory is logically coherent and any significant shifts are explicitly explained |

Flag any audit failures to the user with specific remediation suggestions before delivering the final document.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="performance-review-writer", experiment={
  hypothesis: "Including Situation-Action-Result formatted accomplishments increases employee perception of review fairness and accuracy",
  variants: ["control: narrative-only accomplishment descriptions", "variant: SAR-structured accomplishments with quantified outcomes"],
  measurement: "Employee satisfaction score on post-review survey question 'My review accurately reflects my contributions' across next review cycle",
  expected_impact: "20% increase in 'Strongly Agree' responses on review accuracy perception"
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
FutureProof:request_research(skill="performance-review-writer",
  query="Latest research on reducing cognitive bias in performance evaluations, evidence-based review frameworks, and high-performing organisations' approaches to continuous feedback documentation 2024–2025",
  reason="Ensure review methodology reflects current organisational psychology best practices and legal defensibility standards"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="performance-review-writer", session={
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