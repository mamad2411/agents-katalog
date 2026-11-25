---
name: growth-review
description: "Prepare a performance or growth conversation from evidence rather than recency — a written review, a promotion case, a levelling or calibration argument, or a development plan. Enforces behaviour, impact and evidence for every claim, levelling against the ladder in use, no-surprise delivery, and keeping growth separate from compensation. Use this skill whenever the user is writing or reviewing a performance review, self-review, peer or 360 feedback, a promotion packet, a levelling or calibration argument, or a development plan — including casual phrasings like \"reviews are due friday\", \"is she ready for staff\", or \"how do I tell him it is a meets not an exceeds\". Do not use it for holding the conversation itself, including the early underperformance one (that is difficult-conversation), hiring decisions (hiring-loop), team delivery metrics (delivery-review), compensation (compensation-benchmarking), or building a paper trail for a decision already made."
allowed-tools: Read, Write, Grep, Glob
---

# Growth Review

A good review contains nothing the person has not already heard, every claim in it carries an example, and a stranger reading it in calibration can tell what the person actually did. The adjectives, the rating rationale that only restates the rating, the paragraph about "ownership" — that is padding, and it is the part that gets written when the evidence ran out.

The job is hard because the honest version is more work than the plausible one. Memory supplies the last six weeks and the one visible project, and an assistant will turn that into fluent prose about communication and impact that describes a personality rather than a person's work — reasonable-sounding to everyone except the person being reviewed. This writing also has a second life. It is read aloud in calibration, quoted in a promotion decision, attached to a compensation change, and occasionally read by a lawyer. So write only what you can evidence, name a judgement call as a judgement call, and where the evidence is thin leave the hole visible rather than filling it with confident sentences.

## Scope

Use for: written performance reviews, self-review and peer-feedback prompts, promotion cases, levelling and calibration arguments, development plans, and the early honest conversation with someone falling short of their level.

Do not use for: hiring decisions and interview loops (that is `hiring-loop`), team or programme delivery health (that is `delivery-review` — DORA and flow metrics measure the delivery system, and per-person they produce gaming rather than insight), or compensation benchmarking.

Also do not use it to assemble a retrospective case for a decision already taken. If the outcome is settled and the request is documentation that justifies it, say so plainly and stop. That is not a review; it is the specific artefact that turns a defensible people decision into an indefensible one, because the record shows the reasoning was written after the conclusion.

## Non-negotiables

**Every claim carries an example.** One behaviour, one consequence, one place a reader could go and check. A claim with no example cannot be defended in calibration, cannot be acted on by the person, and should not be written down. If the claim matters and the example is missing, write `[TK: example]` and go and find it before anything is shared.

**Do not invent evidence.** No supplied dates, ticket numbers, quotes or attributed peer comments means none go in. Fabricated corroboration in a document that affects someone's pay and level is a different order of mistake from a wrong figure in a design doc.

**Behaviour and impact, not character.** "Is abrasive" describes a person and gives them nothing to change. "Rewrote three pull requests from the same author without discussing the approach first; that author routed the next design around the team" describes behaviour, names the cost, and is arguable — which is what makes it useful and fair.

**Nothing in the review is new to the person.** A surprise in a written review is a management failure whatever the content, because it means the feedback was withheld until the point where it could no longer be acted on.

**Name the judgement calls.** Whether scope was sustained or one-off, which side of a rating boundary someone lands, whether ambiguity was handled or avoided — these are judgements, not measurements. Write "this is a judgement call, based on [TK: what]" rather than dressing it as a finding. A stated judgement is defensible; a judgement disguised as fact is not.

## Workflow

### 1. Name the artefact and the period

Review, promotion case, levelling argument, development plan, or underperformance conversation — they need different evidence and produce different documents. Then fix the period in dates. A review with no stated period silently becomes a review of the last six weeks.

### 2. Gather evidence across the whole period

Ask for these in one batch, with links where links exist.

| Source | What it gives you |
| --- | --- |
| The person's own self-review or written record | Their account first, so yours is not the only frame |
| Shipped work, and what happened after it shipped | Outcome rather than activity |
| Incidents handled, on-call weeks, escalations | Behaviour under load, which nothing else surfaces |
| Reviews and design feedback they gave | Influence on other people's work — usually the most under-counted evidence |
| Documents, ADRs, proposals they wrote | Reasoning quality and reach |
| Mentoring, onboarding, interviewing | Contribution that never appears in a delivery metric |
| Peer feedback, solicited with a specific question | The half you cannot observe directly |

Cover the whole period deliberately: walk it month by month and check you have something from each. If three months are empty, that is a finding about your record-keeping, not evidence the person did nothing.

The mechanism that makes this cheap is a running notes file per person, appended monthly rather than reconstructed quarterly — one line per notable thing, with a link, written the week it happened. Quarterly is already too coarse to beat recency. If no such file exists, start it now and say in the review that the earlier part of the period is thinner.

Solicit peer feedback with a specific question. "Any thoughts on Priya?" returns adjectives. "Priya ran the checkout migration design review in April — what did she do well, and what would you have wanted done differently?" returns behaviour you can use. Tell people how the feedback will be used before they give it.

### 3. Convert evidence into feedback units

When the raw feedback is more than a screen — a quarter of peer submissions, a 360 export — hand it to the `feedback-synthesiser` subagent instead of reading it here. It returns the themes, each with the number of independent sources and a quoted example, with observed behaviour separated from statements about personality, and keeps the submissions out of this conversation.

The unit is behaviour, then impact, then evidence. Build the table before writing any prose; the prose is a rendering of the table.

| Behaviour | Impact | Evidence |
| --- | --- | --- |
| Took the payments cutover design from a two-page sketch to a plan three teams signed off | Cutover ran in one window with no rollback | ADR-0031, 14 Mar; sign-off thread from the two dependent teams |
| Left the shared client library without a maintainer for the quarter after volunteering for it | Two teams forked it; the fork is still live | Fork commit history; retro notes, 2 Jun |

Rows with no evidence column do not become sentences. They become either a `[TK: example]` or a conversation you have verbally without writing it down.

### 4. Level against the ladder actually in use

If the organisation has a career ladder, quote its language for the level and map the evidence onto it clause by clause. Inventing a private standard is unfair to the person and indefensible in calibration, since everyone else is being measured against the published one.

Where no ladder exists, four axes carry most of the signal.

| Axis | The question | What raises it |
| --- | --- | --- |
| Scope | How large a problem can this person be handed and left with | From a task, to a service, to a system, to an area |
| Autonomy | How much shaping do they need before starting | From direction, to a goal, to a problem statement, to noticing the problem |
| Ambiguity | What do they do when the requirements are not there | From asking, to resolving, to defining what the question is |
| Blast radius | Who feels it when they are wrong | From their own work, to the team, to other teams, to customers or revenue |

Levelling is about the size of the problem someone can be trusted with, not the hours they put in or the volume they produce. A person working long weeks on well-defined tasks is doing valuable work at their current level; that is a fact about the work, not a case for the next one.

### 5. Build the promotion case

Four parts, in this order.

1. **The level's expectations**, quoted from the ladder, not paraphrased.
2. **Evidence they are already operating there**, sustained. At least two or three distinct instances across the period, not one large one. The question calibration will ask is whether this is how the person works now or whether it was a heroic quarter, and the case has to answer it directly.
3. **The counter-argument, stated honestly** — the strongest thing someone in the room will say against it, in their words rather than a weakened version. A case with no counter-argument reads as advocacy and gets treated as such.
4. **The gap plan if the answer is not yet** — what specifically is missing, the assignment that would demonstrate it, and when it is looked at again.

Promotion recognises scope already being carried sustainably. It is not a reward for tenure, and it is not a retention tactic: if the real driver is a competing offer, that is a compensation and retention decision, and running it through the promotion process corrupts the level of everyone already at that level. Name which one it is.

### 6. Prepare for calibration

Bring the ladder clauses, the behaviour-impact-evidence table, and the counter-argument. Do not bring adjectives; they lose every argument against someone else's concrete story.

Arguing for someone against a stronger-sounding narrative is mostly a matter of converting narrative back into evidence: ask what the other person actually did, over what period, and what the outcome was. A visible project is not the same as a hard one.

Bias shows up in reproducible ways, and naming it in the room is part of the job.

| Tell | What to do about it |
| --- | --- |
| One person is described in personality terms, another in outcomes | Ask for the behaviour and impact behind the personality words |
| The strongest cases all come from the one visible project | Ask who did the unglamorous work that project depended on |
| "Not ready" with no missing capability named | Ask which ladder clause is unmet and what would evidence it |
| Feedback that would not be given to a different person for the same behaviour | Say so directly; that is the whole substance of the problem |
| Warmth or polish standing in for scope | Return to the four axes |

Record the outcome and the reason. A decision people can trace is a decision they can accept.

### 7. Deliver it without surprises

Write it first and share it before the meeting — a day is usually enough — so the person can read a rating alone rather than perform a reaction in front of their manager.

Separate the growth conversation from the compensation conversation, in different meetings. Held together, the person hears the number and stops processing everything else, and the development plan is lost.

Be direct about the rating. "There is always room to grow" said in place of "this is a meets, not an exceeds" is not kindness; it removes the person's ability to make an informed decision about their own career, and it makes next cycle's conversation worse. State the rating, then the two or three things that would move it, then stop talking and listen.

### 8. Write a development plan that can be acted on

Two or three areas at most; more is a wish list nobody works on. Each area names a concrete next assignment rather than an adjective — not "be more strategic" but "own the schema migration end to end, including the sequencing conversation with the two dependent teams". Add what support they get, and a date the two of you look at it again.

### 9. Handle underperformance early and specifically

The kind thing and the defensible thing are the same thing here: say it early, in person, in specific terms, well before any formal process. Name the standard being missed and which ladder clause it comes from, give examples with dates, state what changed behaviour looks like, agree a real timeline with check-ins, and write down what was said and when.

Be explicit about your own share. Unclear expectations, a mismatch between the person and the work, missing context, no feedback for two quarters — where any of that is true, it belongs in the record, because it is both accurate and part of what has to change.

Involve HR or the equivalent before anything becomes formal, and follow the local process. Employment law varies by jurisdiction, and this skill does not substitute for advice from someone who knows yours.

## Output format

Fill these in; leave a `[TK: ...]` anywhere the evidence is not in hand.

```markdown
## Review — [name], [period start] to [period end]

### Summary
[Three or four sentences: what they were responsible for, what they delivered,
where they operate on the ladder, and the rating. No new information may appear
below this that the person has not already heard.]

### What went well
[Per item: behaviour, impact, evidence. Two to four items.]

### Where the work needs to change
[Same three-part unit. Two or three items, most important first. Each one has to
be actionable by the person, not a statement about who they are.]

### Level
[The ladder clauses that are met, with evidence. The clauses that are not, with
what would evidence them. Judgement calls named as judgement calls.]

### Rating
[The rating, stated plainly, and the two or three things that would move it.]

### Development plan
[Two or three areas. Per area: the concrete next assignment, the support, and the
check-in date.]

### Evidence gaps
[Periods or areas where the record is thin, and why. This section protects the
person as much as it flags the work.]
```

```markdown
## Promotion case — [name], [current level] to [proposed level]

### The expectation
[The target level, quoted from the ladder.]

### Evidence of operating at that level
[Per ladder clause: two or three distinct instances across the period, each with
behaviour, impact and a link. Note explicitly what makes this sustained rather
than a single quarter.]

### Counter-argument
[The strongest case against, stated in its strongest form, then the response —
or the concession, where it lands.]

### Judgement calls
[Where this rests on judgement rather than evidence, and whose.]

### If not yet
[The specific gap, the assignment that would close it, and the date it is
revisited. A promotion case without this section makes "no" mean "no reason".]
```

## Anti-patterns

**Recency.** Six weeks stand in for twelve months, so the person is reviewed on what they happened to be doing in November. The fix is mechanical: monthly notes, and a month-by-month sweep before writing.

**Feedback about the person, not the work.** "Abrasive", "not strategic", "low energy" give the person nothing to change and land differently depending on who they are — which is exactly why they are the phrases that show up in discrimination claims. Every one of them can be restated as a behaviour with an impact, or dropped.

**The surprise rating.** A rating the person could not have predicted from your last two months of conversations is a failure of management before it is a failure of the review.

**Promotion for tenure.** Rewards time served, quietly redefines the level downwards, and is unfair to everyone already holding it.

**Effort as evidence.** Long hours, weekend deploys and visible strain describe cost, not scope. Promoting on effort teaches the team that visible strain is the promotion path, and you get more of it.

**Softening a rating into ambiguity.** The person leaves reassured, the calibration record says something else, and the gap surfaces at the compensation conversation or the exit interview.

**A development plan made of adjectives.** "Be more senior", "improve communication", "show more ownership" cannot be started on Monday. An assignment can.

**Reverse-engineering the record.** Writing up evidence after the decision, or trawling for negatives once an outcome is chosen, produces a document whose dates and tone give it away — and it converts a defensible decision into an indefensible one.
