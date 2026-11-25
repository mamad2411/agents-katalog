---
name: hiring-scorecard
description: "Creates structured interview scorecards with competency ratings, question banks, and evaluation rubrics for objective hiring decisions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Hiring Scorecard

## When to Use This Skill

Use this skill when you need to:
- Create a structured scorecard for evaluating job candidates consistently
- Define competency ratings and evaluation criteria for a specific role
- Build question banks aligned to role requirements
- Remove bias from hiring decisions with objective scoring

**DO NOT** use this skill for writing job descriptions, sourcing candidates, or building interview question banks (use interview-question-bank for that). This is for the evaluation scorecard used during and after interviews.

---

## Core Principle

HIRING WITHOUT A SCORECARD IS HIRING ON VIBES — A STRUCTURED SCORECARD FORCES OBJECTIVE EVALUATION AGAINST ROLE-SPECIFIC CRITERIA, REDUCING BIAS AND BAD HIRES.

---

## Phase 1: Role Requirements

Define what the role needs before building the scorecard.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Role title** | "What role are you hiring for?" | No default |
| **Employment type** | "Full-time, part-time, or contractor?" | Contractor |
| **Top 3 outcomes** | "What does this person need to achieve in the first 90 days?" | No default |
| **Must-have skills** | "What skills are non-negotiable?" | No default |
| **Nice-to-have skills** | "What skills would be a bonus but not required?" | No default |
| **Culture traits** | "What working style or personality traits matter for this role?" | Self-starter, communicative |

### Competency Framework

```
## Role Competencies: [Role Title]

### Must-Have (Weighted 70%)
| Competency | Description | How to Assess |
|-----------|-------------|---------------|
| [Skill 1] | [What good looks like] | [Interview question / portfolio / test] |
| [Skill 2] | [What good looks like] | [Assessment method] |
| [Skill 3] | [What good looks like] | [Assessment method] |

### Nice-to-Have (Weighted 20%)
| Competency | Description | How to Assess |
|-----------|-------------|---------------|
| [Skill 4] | [What good looks like] | [Assessment method] |

### Culture Fit (Weighted 10%)
| Trait | Description | How to Assess |
|-------|-------------|---------------|
| [Trait 1] | [Observable behavior] | [Behavioral question] |
```

**GATE: Confirm competencies before building the scorecard.**

---

## Phase 2: Build Scorecard

Create the evaluation instrument.

### Scorecard Template

```
## Hiring Scorecard: [Role Title]

**Candidate:** _______________
**Interviewer:** _______________
**Date:** _______________
**Interview stage:** [Screen / Technical / Final]

### Competency Ratings

| # | Competency | Weight | Score (1-5) | Weighted Score | Notes / Evidence |
|---|-----------|--------|-------------|---------------|-----------------|
| 1 | [Must-have 1] | [%] | [ ] | [ ] | |
| 2 | [Must-have 2] | [%] | [ ] | [ ] | |
| 3 | [Must-have 3] | [%] | [ ] | [ ] | |
| 4 | [Nice-to-have 1] | [%] | [ ] | [ ] | |
| 5 | [Culture trait 1] | [%] | [ ] | [ ] | |

### Scoring Guide

| Score | Definition |
|-------|-----------|
| 1 | No evidence of competency — significant concern |
| 2 | Below expectations — gaps in critical areas |
| 3 | Meets expectations — adequate for the role |
| 4 | Above expectations — strong evidence of competency |
| 5 | Exceptional — among the best candidates seen for this competency |

### Overall Assessment

**Total weighted score:** _____ / 5.0

**Recommendation:** [ ] Strong Hire  [ ] Hire  [ ] No Hire  [ ] Strong No Hire

**Top strengths:**
1.
2.

**Top concerns:**
1.
2.

**Additional notes:**

**Signature:** _______________ **Date:** ___
```

### Red Flag Checklist

```
## Automatic Disqualifiers

- [ ] Cannot verify claimed experience or credentials
- [ ] Disrespectful to interviewer or staff
- [ ] Unable to articulate relevant experience clearly
- [ ] Scores 1 on any must-have competency
- [ ] [Role-specific red flag]
```

**GATE: Present scorecard for review before adding interview questions.**

---

## Phase 3: Align Questions

Map interview questions to scorecard competencies.

### Question-Competency Map

```
## Interview Question Map

| Competency | Question | What to Listen For | Red Flag |
|-----------|---------|-------------------|----------|
| [Skill 1] | "Tell me about a time you [relevant scenario]" | [Specific evidence of competency] | [Vague or evasive answer] |
| [Skill 2] | "How would you approach [role-specific challenge]?" | [Structured thinking, relevant tools] | [No framework, just buzzwords] |
| [Culture] | "Describe your ideal working relationship with a manager/client" | [Alignment with your working style] | [Misalignment on communication or autonomy] |
```

### Scoring During Interview

- Write notes as the candidate speaks, not after
- Score each competency immediately after the relevant question
- Record specific examples and quotes, not general impressions
- Do not discuss scores with other interviewers until all scorecards are complete

---

## Phase 4: Decision Framework

Use scorecards to make consistent hiring decisions.

### Decision Matrix

```
## Hiring Decision Guide

| Weighted Score | Recommendation | Action |
|---------------|---------------|--------|
| 4.5-5.0 | Strong Hire | Make an offer quickly — this candidate will have other options |
| 3.5-4.4 | Hire | Solid candidate — proceed with offer |
| 2.5-3.4 | Maybe | Additional assessment needed — second interview or skills test |
| Below 2.5 | No Hire | Pass — do not lower the bar |
```

### Multi-Interviewer Calibration

If multiple people interview the same candidate:
1. Each interviewer completes their scorecard independently
2. Compare scores — discuss any competency where scores differ by 2+ points
3. Average the final scores
4. The hiring manager makes the final call

### Post-Hire Scorecard Validation

At 90 days, compare the hiring scorecard predictions to actual performance:
- Were the identified strengths confirmed?
- Did any concerns materialize?
- Use this data to calibrate future scorecards

---

## Anti-Patterns

- **No evidence, just feelings** — "I liked them" is not a hiring decision. Every score needs a specific example from the interview.
- **Halo effect** — one strong answer biases all other scores upward. Score each competency independently.
- **Lowering the bar** — if no candidate scores above 3.0, the role is unclear or the pipeline needs improvement. Do not hire a 2.5.
- **Ignoring red flags** — a 4.5 score with one automatic disqualifier is still a no hire. Red flags are non-negotiable.
- **Skipping the scorecard for "obvious" hires** — even obviously strong candidates should be scored. It validates the decision and creates documentation.

---

## Recovery

- **User has never used a scorecard:** Start simple — 3 must-have competencies scored 1-5. Add complexity after the first hire.
- **All candidates score similarly:** The questions may not be differentiating enough. Add a practical test or more specific behavioral questions.
- **Interviewer bias suspected:** Require written evidence for every score. "They seem nice" is not evidence. "They described a specific project where they..." is.
- **User is hiring quickly and wants to skip the process:** A 15-minute scorecard review saves weeks of dealing with a bad hire. Speed on hiring is expensive.
- **Candidate scored well but is underperforming:** Review which competencies were misjudged and refine the assessment methods for those areas.
