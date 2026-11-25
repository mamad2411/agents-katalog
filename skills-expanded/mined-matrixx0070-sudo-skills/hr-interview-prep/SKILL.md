---
name: hr-interview-prep
version: 1.0.0
description: Build a structured, bias-resistant interview loop — competencies mapped to interviewers, calibrated questions, and 1/3/5 scorecards.
author: matrixx0070
tags: [interviewing, hiring, competencies, scorecards, structured-interview, calibration]
capabilities: []
---

## When to use

Reach for this when preparing an interview loop, standardizing questions across panelists, or designing a scorecard so decisions are evidence-based and comparable across candidates.

**Not for:** tracking candidates through stages (use hr-recruiting-pipeline), writing the offer (use hr-draft-offer), or after-hire ramp planning (use hr-onboarding).

## Method

1. **Derive competencies from the job** — pick 4-6 must-haves (technical + behavioral) tied to real responsibilities, not generic traits.
2. **Distribute across the loop** — assign each interviewer 1-2 competencies for complete, non-redundant coverage; name each interview type (screen, technical, behavioral, values, hiring-manager). Decision point: if a must-have competency has no owner, add a slot or reassign before finalizing.
3. **Write questions** — for each competency give a behavioral prompt (STAR "Tell me about a time…"), a situational prompt, and 2-3 probing follow-ups that reach depth.
4. **Define the rubric** — describe what a 1 (below), 3 (meets), and 5 (exceeds) answer looks like, with concrete observable signals for each.
5. **Build the scorecard** — competency → rating → evidence-notes field, ending in a recommendation (Strong Yes / Yes / No / Strong No) with required written justification.
6. **Add guardrails** — an interviewer briefing, a list of legally off-limits topics, and a debrief that shares evidence before scores. Decision point: run debrief evidence-first to reduce anchoring; if scores were shared early, re-poll after evidence.

## Example

Role: Customer Success Manager. Competency "de-escalation." Behavioral: "Tell me about a time a key account threatened to churn — what did you do?" Follow-ups: What was the root cause? What did you commit to and did you deliver? How did the relationship end up? Rubric — 1: blames the customer, no ownership; 3: describes a structured save with a clear plan; 5: shows the save plus a systemic fix that prevented recurrence. Owner: the hiring-manager interview. Scorecard captures quote-level evidence, then a rating and a written recommendation.

## Pitfalls

- Vague competencies ("culture fit", "smart") that invite bias and can't be scored consistently.
- Every interviewer asking the same questions — redundant coverage, blind spots elsewhere.
- Rubrics with adjectives ("strong", "weak") instead of observable behaviors.
- Scores collected before evidence in the debrief, anchoring the panel to the loudest voice.

## Output format

```
Role + competency map:
  competency | interviewer | interview type
Question bank (per competency):
  behavioral | situational | follow-ups
Scoring rubric (per competency): 1 anchor / 3 anchor / 5 anchor
Scorecard template: competency → rating → evidence → recommendation (SY/Y/N/SN) + justification
Debrief agenda: evidence-first order, roles, bias reminders
```

## Reference

### Competency question bank

Each entry gives a behavioral prompt, follow-ups that force depth, and the signals that separate a strong answer from a weak one. Score on evidence, not delivery polish.

**Ownership / drive**
- Prompt: "Tell me about a project you owned end-to-end where the outcome was in doubt."
- Follow-ups: What specifically was yours vs. the team's? What did you decide alone? What did you do when it slipped?
- Strong: uses "I" precisely, names a hard call they made, quantifies the result, owns a mistake. Weak: "we" throughout, no decision point, credits luck or blames others, vague outcome.

**Dealing with ambiguity**
- Prompt: "Describe a time you had to move forward without clear requirements."
- Follow-ups: How did you decide what to build first? What did you deliberately not do? How did you validate you were right?
- Strong: framed the problem, made explicit assumptions, shipped a small bet and checked it. Weak: waited for someone else to decide, or barreled ahead with no validation.

**Conflict / influence without authority**
- Prompt: "Tell me about a time you disagreed with a peer or your manager on something that mattered."
- Follow-ups: What was their view and why? What changed your mind or theirs? How's the relationship now?
- Strong: states the other side fairly, used data or a shared goal to move them, disagreed-and-committed. Weak: caricatures the opponent, "I was just right," or avoided the conflict entirely.

**Technical depth (adapt per role)**
- Prompt: "Walk me through the most technically challenging thing you've built."
- Follow-ups: What alternatives did you reject and why? Where did it break? What would you do differently?
- Strong: explains trade-offs, knows the failure modes, can go three layers deep unprompted. Weak: buzzwords without mechanics, can't explain why choice A over B, no discussion of limits.

**Learning / growth**
- Prompt: "Tell me about significant feedback you received and what you did with it."
- Follow-ups: How did you hear it? What did you actually change? How do you know it worked?
- Strong: non-defensive, concrete behavior change, evidence of durability. Weak: humble-brag ("I work too hard"), no real change, blames the messenger.

### STAR probing pattern

When an answer stays high-level, pull it down with: **S**ituation ("set the scene — when, where, who?") → **T**ask ("what was *yours* to solve?") → **A**ction ("what did *you* personally do, step by step?") → **R**esult ("what happened, and how did you measure it?"). The Action and Result are where signal lives; a candidate who can only narrate Situation and Task is describing proximity to work, not ownership of it.

### Scorecard rubric (1–3–5 anchors)

| Rating | Label | Anchor |
|---|---|---|
| 5 | Exceeds | Multiple concrete, verifiable examples; handled complexity beyond the level; taught or systematized. Clear, specific, unprompted depth. |
| 4 | Above | Solid example plus one strong signal of stretch; minor gaps. |
| 3 | Meets | One relevant, credible example matching the level; adequate depth on probing. |
| 2 | Below | Generic or secondhand example; needed heavy prompting; noticeable gap. |
| 1 | Well below | No real example, or a red flag (no ownership, blames others, misrepresents scope). |

Require written evidence (ideally a quote) for every rating. A rating with no evidence field filled is invalid — reject it in debrief.

### Recommendation scale

- **Strong Yes** — would fight to hire; clears the bar on all owned competencies, exceeds on some.
- **Yes** — meets the bar; hire if the loop agrees.
- **No** — a specific, evidenced gap on a must-have.
- **Strong No** — a values/integrity red flag, or a gap so large it's disqualifying regardless of other data.

Map to a decision rule up front: e.g., any Strong No blocks; two or more No's on distinct competencies blocks; ties break toward the raise-the-bar interviewer's evidence.

### Debrief protocol (anti-anchoring)

1. Each interviewer submits their scorecard **before** the debrief — no discussion first.
2. In the room, share **evidence before scores**, one competency at a time, starting with the most junior interviewer to reduce authority bias.
3. Reveal ratings, resolve divergence with evidence not seniority. If scores were leaked early, re-poll after evidence.
4. Decide against the pre-agreed rule; write the one-line rationale.

### Legally off-limits (US; adapt per jurisdiction)

Do not ask about: age/DOB, race/ethnicity/national origin, religion, sex/gender identity/sexual orientation, marital or family status/pregnancy/childcare plans, disability or health/medical history, genetic information, citizenship (you may ask work authorization), arrest record (conviction rules vary by locale), and — in many US states — current or prior salary. Keep every question tied to the job. If a candidate volunteers protected information, do not record it or let it influence the score.

### Loop design quick reference

Aim for 4–6 competencies, each owned by 1–2 interviewers with no more than light overlap. Typical loop: recruiter screen → hiring-manager screen → 3–4 focused interviews (technical depth, technical breadth/craft, behavioral/values, cross-functional partner) → optional final/exec. Keep each interview 45–60 min with 10 min reserved for candidate questions; brief every panelist on their competency and the off-limits list before the loop starts.
