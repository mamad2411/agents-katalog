---
name: hiring-loop
description: "Design and run a structured hiring loop for an engineering role — the scorecard first, then stages mapped to competencies, questions and written rubrics, work samples that respect the candidate's time, calibrated interviewers, and a debrief that decides on evidence. Use this skill whenever the user is hiring: writing a scorecard or role brief, designing or trimming an interview loop, writing interview or behavioural questions, setting a take-home or pairing exercise, building a rubric or debrief form, running a debrief, deciding hire or no-hire, or handling rejections and offers — including phrasings like \"what should we ask\", \"our loop is too long\", or \"the panel is split\". Do not use it for performance reviews or promotion cases (that is growth-review), compensation design (compensation-benchmarking), team delivery metrics (that is delivery-review), or preparing as the candidate (that is job-search)."
allowed-tools: Read, Write, Grep, Glob
---

# Hiring Loop

A good loop can say, for each competency it claimed to test, what evidence it collected and from where. The decision then follows from the evidence rather than from the last conversation in the room.

The job is hard because hiring feels like a skill everyone already has. Interviewers who have never seen a rubric are confident in their read; unstructured conversation feels perceptive and mostly measures how similar the candidate is to the interviewer; and a debrief run without written notes converges on whoever speaks first with conviction. The costs land unevenly — a weak loop is not merely inaccurate, it is inaccurate in a patterned way that favours people who resemble the incumbents, and that pattern is what a discrimination claim looks like from the outside. Structure is not bureaucracy here. It is the thing that makes the decision both better and defensible.

## Scope

Use for: writing a scorecard, designing or trimming an interview loop, writing questions and rubrics, choosing and scoping a work sample, calibrating interviewers, running a debrief, making a hire or no-hire call, and handling rejection, closing and offers.

Do not use for: performance reviews, promotion cases and levelling of existing employees (that is `growth-review`), compensation design and benchmarking, team delivery health (that is `delivery-review`), or helping someone prepare as the candidate (that is `job-search`).

Employment law on interviewing, record-keeping and rejection differs by jurisdiction. This skill encodes practice that is defensible in general; it does not replace advice from whoever owns hiring compliance where the role sits.

## Workflow

### 1. Write the scorecard before anything else

Not a job ad. A scorecard has three parts.

- **Outcomes** — what this person must have delivered by the end of their first year, stated so that success is checkable. "Own the payments integration and take it from one provider to three" is an outcome. "Be a strong backend engineer" is not.
- **Competencies** — the small number of capabilities that predict those outcomes. Four to six. Each has to be a capability that varies between plausible candidates; a competency every applicant would pass measures nothing and costs everyone an hour.
- **Evidence** — per competency, what would count as a strong signal, and which stage collects it.

Everything downstream derives from this: the stages, the questions, the rubric, the debrief form. Without it, each interviewer measures whatever they personally value, the debrief has no shared vocabulary, and the discussion resolves into who found the candidate most agreeable. Write it with the hiring manager and the people who will interview, before the role is posted.

If the team cannot agree on the outcomes, the loop is not the problem and running it will not help.

### 2. Choose structure over conversation, and know why

Structured interviews — the same questions, the same order, the same rubric, for every candidate — predict job performance substantially better than unstructured ones, and the gap is not marginal. An unstructured chat mostly measures rapport, which correlates with similarity to the interviewer.

So: same questions for everyone, scored against a written rubric, notes written down. Follow-up probes can differ, because probing is how you get depth; the opening questions and the scoring criteria may not.

### 3. Design the loop

| Stage | What it tests | Typical length |
| --- | --- | --- |
| Hiring-manager screen | Motivation, level, the constraints of the role stated honestly | 30-45 min |
| Practical exercise | The core craft of the job, on representative work | 60-90 min |
| Technical depth or system design, scoped to level | Judgement, trade-offs, how they handle not knowing | 60 min |
| Behavioural or values interview | Collaboration, conflict, ownership — as evidence, not assertion | 45-60 min |

Four stages is usually enough; five is defensible for a senior or leadership role. Every stage maps to at least one scorecard competency, and no stage duplicates another's competency — an overlapping stage spends the candidate's goodwill and the panel's hours to buy a second copy of a signal you already have.

State the total time cost to the candidate up front, including any exercise done in their own time, and publish the stages. A candidate who knows the shape of the loop performs closer to how they will perform in the job, which is the whole point.

### 4. Scope the work sample honestly

The exercise should resemble the actual work: reading and extending an existing codebase, debugging something broken, reviewing a pull request, shaping an ambiguous requirement. Puzzles and whiteboard algorithm rounds test preparation for interviews rather than the job, unless the job is genuinely that.

Prefer a short pairing session or a code-reading exercise over a take-home. It is time-boxed by construction, it shows how the person thinks and collaborates rather than only what they produce, and it does not tax whoever has the least free evening time — which reliably means candidates with caring responsibilities or a second job.

If a take-home is used: cap it at two to three hours, mean the cap, say plainly that you will not reward extra effort beyond it, and pay for the time where policy and local law allow. Score it against a written rubric produced before the first submission, and give every candidate the same brief.

Run the exercise pair-style where possible: the interviewer's job is to unblock, answer questions and observe reasoning, not to sit in silence taking marks off. Say at the start that questions are expected and cost nothing.

### 5. Interview behaviourally for evidence, not narrative

Ask for a specific instance, then drill in. "Tell me about a time you disagreed with a technical decision" gets a rehearsed story; the evidence is in the follow-ups.

- What was the situation, concretely, and when?
- What did you personally do — as distinct from what the team did?
- What did you decide, and what did you decide against?
- What happened as a result, and how do you know?
- What would you do differently?

Listen for "we" where "I" belongs, and ask. This is not a trap; a candidate who cannot separate their contribution from the team's often genuinely worked in a way that makes it hard, and that is itself worth knowing. Push for the specific instance whenever the answer arrives as a general policy: "how do you approach code review" is answerable from theory, "walk me through the last review where you asked for substantial changes" is not.

### 6. Run technical depth and system design for signal, not victory

Scope the problem to the level being hired. A staff-level design question given to a mid-level candidate measures nothing except your calibration.

The interviewer's job is to create the conditions where signal can appear: state the problem clearly, say which constraints matter, offer the missing domain context freely, and let the candidate drive. Interrupting to demonstrate your own preferred design, or holding back a constraint so it can be sprung later, produces a story about the interviewer and no information about the candidate. If a candidate stalls, unblock and note where they stalled — that is the datum, not the silence.

### 7. Calibrate the interviewers

An uncalibrated panel with a good rubric is still an uncalibrated panel.

- New interviewers shadow twice, then are shadowed twice before running a stage alone.
- Every stage has a written rubric with described levels, not a bare 1-4 scale. "Strong" has to mean something specific enough that two interviewers reach it from the same evidence.
- Notes are written within the hour, while recall is accurate, and before reading anyone else's. Reading first makes the loop converge on the first strong opinion, and the panel then mistakes that convergence for agreement.
- Notes record what the candidate said and did, then the score. A note that only records a conclusion cannot be revisited, cannot be argued with, and is the kind of record that reads badly if it is ever produced in a dispute.

### 8. Debrief on evidence

Independent written scores are submitted before the discussion opens. If someone has not submitted, the debrief waits.

Then discuss the disagreements first — they carry the information, and the agreements need only a minute. Ask what evidence produced each score, and be open to someone moving because of evidence they did not see rather than because the room leans.

Decide against the scorecard, competency by competency, and record the reason. A hire or no-hire is a judgement about evidence for specific competencies, never a vote on likeability, and never an average of numbers that were never meant to be averaged.

When "culture fit" appears, require it to be restated as a named behaviour with evidence — "did not engage with the reviewer's alternative design when it was better, twice" — or dropped from the discussion. As an unstated objection it is a veto that cannot be examined, and it is where affinity bias enters the room wearing a suit.

### 9. Guard against the predictable biases

| Trap | What it looks like | Counter |
| --- | --- | --- |
| Affinity | "I'd enjoy working with them"; shared school, employer or hobby doing the work | Ask which competency that is evidence for |
| Brand halo | A well-known employer standing in for demonstrated skill | Score the evidence they gave, not the logo |
| Career gaps | Reading a break as a risk | Ask about the work, not the gap; a gap is not a competency |
| Confidence for competence | Fluent delivery of a shallow answer scoring above a careful, correct one | Score the reasoning, not the presentation |
| Interviewing for polish | Communication weighted heavily in a role that does not need it | If it is not a scorecard competency, it does not score |
| Similarity to the panel's own path | "That's not how I'd have got here" | Compare against the scorecard, not the interviewer's career |

Where it is possible, build a panel that is not uniform, and give everyone the same questions in the same order. Both of those are also what makes the process explainable later.

### 10. Treat candidate experience as a deliverable

Every candidate meets the company here, and the market for any specific role is smaller than it looks. Reply within a stated window, give real timelines and update when they slip, tell candidates what the next stage is and who they will meet, and give a rejected candidate something specific enough to be worth having — the competency where the evidence was thin, in a sentence that would not surprise them.

Reject fast, in writing, and by a human. Silence after a final round is the single thing candidates talk about most, and it costs the next five hires from the same network. Do not offer detailed feedback you are not permitted to give; a short honest note beats an elaborate one that has been through three rewrites.

### 11. Close honestly

Sell the role that exists: the actual problems, the actual team, the constraints and what is genuinely unresolved. Overselling buys a signature and loses the person in month seven, having spent the whole loop's cost twice.

Make the offer clean at the level the evidence supports. An offer the person will have to renegotiate within a year — a title that undersells the scope, a number known to be below the band — buys a short peace and a hard conversation later, and it is remembered.

## Output format

```markdown
## Scorecard — [role], [level], [team]

### Mission
[One or two sentences: why this role exists and what it owns.]

### Outcomes (first 12 months)
[Three to five. Each checkable: what will exist or have changed.]

### Competencies
[Four to six. Per competency: what it means here, what strong evidence looks
like, what weak evidence looks like, and which stage collects it.]

### Deliberately not required
[What the loop will not test for, so nobody tests for it anyway. This is the
line that stops a role drifting into a wish list.]

### Loop
[Stage | competencies covered | format | length | interviewers]
[Total candidate time cost, including anything done in their own time.]
```

```markdown
## Debrief — [candidate], [role], [date]

### Scores (submitted independently, before discussion)
[Competency | interviewer | score | the evidence behind it]

### Disagreements
[Where scores diverged, what evidence each side had, and what changed after
the discussion — including nothing.]

### Decision
[Hire / no-hire / hire at a different level, per competency against the
scorecard, with the reason. Any competency with no evidence is named here as
a gap, not filled in with an impression.]

### Unresolved
[What the loop did not manage to test, and whether it matters enough to add a
stage — for this candidate, or for the next one.]

### Candidate feedback to send
[The specific, sendable version. Written now, while the evidence is in front
of you.]
```

## Anti-patterns

**No scorecard.** Every interviewer measures a different thing, so the debrief has no shared basis and resolves on who was most persuasive in the room. This is the root cause of most of the rest of this list.

**Unstructured chats.** They feel perceptive and mostly measure similarity to the interviewer. Different candidates get different questions, so the scores are not comparable and the process cannot be explained afterwards.

**The take-home that costs a weekend.** It filters for free time rather than skill, quietly excluding the candidates with the least of it, and the strongest people decline it outright.

**Debriefing before anyone has written anything down.** The first confident opinion becomes the group's, and the panel experiences that as consensus.

**Culture fit as an unstated veto.** An objection nobody has to evidence is an objection nobody can examine, and it is the most reliable route for affinity bias into a hiring decision.

**Interviewing for the interviewer's own path.** Testing the things this interviewer happens to be good at produces a team that is a copy of the panel, with the same blind spots.

**Ghosting.** A candidate who completed a loop and heard nothing tells everyone they know, accurately. It is the cheapest possible damage to avoid.
