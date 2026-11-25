---
name: candidate-evaluation
description: Use this skill when the user asks to evaluate a candidate against a rubric, write a structured interview debrief, calibrate an interview panel, or produce a hire or no-hire decision memo. Trigger phrases include "evaluate this candidate", "score this interview", "write the debrief", "hire or no-hire", "evaluar al candidato", "escribir el debrief", "panel debrief", "interview scorecard". Produces a scorecard tied to concrete evidence and a decision memo, with role-specific rubric overrides supported.
---

# candidate-evaluation

> **Anchor:** Hire for fluency under failure, not for polish under easy conditions.

## When to use

Use this skill when the user needs a structured read of one or more candidates. Works for:

- An interview debrief after a panel.
- A scorecard on a take-home or work sample.
- A decision memo before an offer.
- A calibration session across interviewers who disagree.
- A retrospective on a bad hire to refine the rubric.

Do not use when:

- The user is writing a job description. That is a different task.
- The user is deciding which candidates to interview from a pile of resumes. That is sourcing.
- The user is scoring a vendor. Use `vendor-evaluation`.

## Philosophy

Hiring is a bet under uncertainty, and the cost of a bad hire is paid by the team that joins them. Two handbook concepts apply. **No heroes, no blame:** if the rubric rewards people whose strengths depend on the team compensating for their weaknesses, the hire will look great for six months and structurally fragile after that. **Cultural signals are delivery:** the candidate's register, how they talk about past teammates, and how they handle disagreement are not soft signals. They are the quality of the next year of the team's meetings. Score them like you score anything else that moves delivery.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: hiring panel, scorecard, debrief, take-home, IC, staff, manager, bar, no-hire, hire, calibration, signal, blind spot, red flag.
- **EN.** Direct US business register. Evaluations get read by people who will act on them; do not write them as persuasion.
- Candidate names and role names stay in the language they are used internally.

## Method

### Step 1. Define the role, not the title

A job title is not a role. Write:

- **What the person does day to day.** The top three activities by time.
- **What changes when they join.** What the team gains, what the team stops doing.
- **Seniority expected.** As observed behavior, not as years.
- **Team shape.** Whose work they depend on. Who depends on theirs.

An evaluation against a vague role produces a vague decision.

### Step 2. Pick the rubric

Default rubric has nine dimensions:

1. **Judgment under ambiguity.** How the candidate navigates when the right answer is not given.
2. **Delivery track record.** Evidence of having shipped real things in real conditions.
3. **Technical depth vs breadth.** The correct mix for this role.
4. **Ownership signal.** Whether work is treated as theirs or someone else's.
5. **Failure fluency.** How cleanly the candidate discusses things that went wrong.
6. **Scope compression.** Ability to cut work to what matters.
7. **Communication density.** Signal per sentence.
8. **Political literacy.** Reading the room, anticipating stakeholder reactions.
9. **Learning velocity.** Pace of absorbing new domains.

For each role, remove what does not apply and add what does. A customer-facing role adds "customer register". A highly technical IC role adds "debugging velocity". Keep the rubric under 10 dimensions.

Full scoring anchors per dimension are in `references/rubric-en.md` and `references/rubric-es.md`.

### Step 3. Set the bar before the interview

Write the bar for this role before any candidate has been seen. For each rubric dimension:

- **Bar.** The minimum score for hire.
- **Strong signal.** The score that suggests the candidate should be accelerated.
- **Disqualifier.** The score or behavior that ends the process regardless of other signals.

Setting the bar after the interview is how bias enters.

### Step 4. Gather evidence with deliberate exercises

Each interview stage is designed to produce evidence on specific dimensions. Do not run interviews that "learn about the candidate in general".

- **Resume walk or life review.** Signal on delivery, ownership, failure fluency.
- **Work sample or take-home.** Signal on technical depth, scope compression.
- **Case or design interview.** Signal on judgment under ambiguity, communication density.
- **Manager or peer interview.** Signal on political literacy, ownership.
- **References.** Signal on all dimensions, calibrated against the candidate's self-report.

Every interviewer knows, before the interview, which dimensions they are scoring.

### Step 5. Score with evidence, not impression

Each dimension gets a score and a quote or a specific behavior.

- **Score.** 1 to 5 per dimension, using the anchors in `references/rubric-en.md`.
- **Evidence.** At least one concrete moment. "When asked about X, said Y. When pushed, revised to Z." "Shipped W in N months. Described the specific trade-off between A and B."

A score without evidence is an opinion dressed up as data. Call out impression as impression when it appears, and demote it in the synthesis.

### Step 6. Calibrate across interviewers

After all interviews, before the debrief:

- Each interviewer posts their scores with evidence, blind to the others.
- The hiring manager looks for inconsistencies.
- Disagreements of two or more points on a dimension get flagged for discussion.

Scores that drift to consensus in the live debrief without new evidence are a calibration problem, not agreement.

### Step 7. Run the no-heroes check

Ask explicitly:

- Is any dimension's high score the kind of strength that only works when the team compensates for weaknesses elsewhere.
- Is any low score the kind of weakness this team specifically cannot absorb.
- Is any strength dependent on a unique situation the candidate was in, not transferable to the role.

A candidate whose top dimensions all require heroics to shine is not a fit for most teams. Write the concern even if the overall signal is positive.

### Step 8. Watch the cultural signals

Distinct from dimension 8 (political literacy). Specifically:

- **How the candidate talks about former teammates.** Blame, respect, curiosity.
- **How the candidate handles disagreement inside the interview.** With you, with other candidates if visible, with their own earlier statements.
- **How the candidate responds to being wrong.** In real time, when caught.

These show up in every meeting the team will have for the next two years. Score them.

### Step 9. Write the decision memo

The memo answers one question: hire or no-hire. The rest is justification. Structure:

- **Recommendation.** Hire, no-hire, or hire for a different role.
- **Summary.** Two sentences on why.
- **Scorecard.** Dimension by dimension. Score and single-sentence summary of evidence.
- **Concerns.** Even for hires, at least two. A memo with zero concerns is either untrusted or a rubber stamp.
- **Onboarding notes if hired.** What this specific person will need in their first 30 days that is not generic.
- **Conditions if hired.** If the recommendation is hire at a different level or with a specific team placement, say so.

### Step 10. Close the loop

After the hire:

- Record which dimensions the rubric scored accurately and which missed.
- Six months later, compare the predicted strengths and concerns to observed behavior.
- Update the rubric for the next hire in the same role.

This is the slowest feedback loop in product work. Most teams skip it. That is why rubrics rot.

## Templates

- `templates/en/scorecard.md`: per-candidate scorecard with evidence.
- `templates/en/decision-memo.md`: hire or no-hire decision memo.
- `templates/es/scorecard.md`: scorecard por candidato con evidencia.
- `templates/es/decision-memo.md`: memo de decisión hire o no-hire.

## References

- `references/rubric-en.md`: full scoring anchors per dimension, in English.
- `references/rubric-es.md`: anchors de scoring por dimensión, en castellano.

## Related skills

- `vendor-evaluation`: use it when scoring a commercial provider, not a person.
- `red-team-review`: run it on the rubric when you suspect it rewards fragile strengths.
- `post-mortem`: use it to run a blameless retro on a bad hire and refine the rubric.

## Anti-patterns

This skill must never produce:

- A score without evidence.
- A memo that says "smart and nice".
- A hire recommendation with zero concerns.
- A debrief that ignored a strong disagreement between interviewers.
- A rubric silently changed during or after interviews.
- A candidate evaluated against a role the hiring manager never wrote down.
- A memo that conflates "I liked this person" with "this person is above the bar".
- A memo that uses "culture fit" without specifying which cultural signals.
- A rubric score that requires the team to work around the candidate's weaknesses to function.

## Checklist before delivery

- [ ] Role is written as activities, not title.
- [ ] Rubric is chosen with role-specific overrides.
- [ ] Bar, strong signal, and disqualifier are set per dimension.
- [ ] Every score has at least one concrete evidence item.
- [ ] Disagreements of two or more points are flagged and discussed.
- [ ] No-heroes check is run.
- [ ] Cultural signals are scored, not just mentioned.
- [ ] Memo contains a recommendation, summary, scorecard, concerns, and onboarding notes if hired.
- [ ] No buzzwords from the voice rules appear.
