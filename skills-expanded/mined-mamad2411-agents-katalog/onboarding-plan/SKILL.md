---
name: onboarding-plan
description: "Plan and run the first ninety days for a new engineer — access working before day one, a briefed buddy, a merged change in week one, 30/60/90 expectations as capabilities, the context that is not in the code, and check-ins that capture confusion while it is still visible. Use this skill whenever someone is joining or has just joined: writing an onboarding or ramp plan, preparing for a start date, choosing a first task, assigning a buddy, onboarding a remote joiner, deciding when a new hire goes on call, or working out why a ramp has stalled — including phrasings like \"she starts monday and nothing is set up\", \"what should his first ticket be\", or \"is he ramping too slowly\". Do not use it for interview loops or hire decisions (that is hiring-loop), reviews and promotion cases for established people (that is growth-review), team meeting structure (that is design-team-cadence), or goal setting (that is okr-planning)."
allowed-tools: Read, Write, Grep, Glob
---

# Onboarding Plan

Onboarding has worked when the new engineer has merged something that mattered, can name the systems and the people their work depends on, and would still tell a friend they made the right decision. The third one is the one that decides whether they are here in a year, and it is the one almost always left to chance.

The job is hard because the cost of doing it badly is deferred and quiet. `hiring-loop` ends at a signed offer, and the months of panel time that produced it are recovered or wasted in the six weeks that follow — but nothing fails visibly. A new engineer who spends four days waiting for a repository grant does not complain; they form a private conclusion about how the place is run, and that conclusion is durable. A team that absorbed its context orally over three years cannot see what a newcomer does not know, so it hands over a reading list and calls it onboarding. And a slow first month reads to a manager as a doubt about the hire, exactly when the honest reading is usually a doubt about the environment. Onboarding is a system you are responsible for, and the new person is the only instrument you have for measuring it.

## Scope

Use for: the pre-start setup, the first-week plan, choosing a first task, assigning and briefing a buddy, writing 30/60/90 expectations, transferring undocumented context, running early check-ins in both directions, onboarding remote joiners, sequencing the first on-call rotation, and diagnosing a ramp that is not progressing.

Do not use for: designing the interview loop or making the hire decision (that is `hiring-loop`), performance reviews, promotion cases, levelling and development plans for established employees (that is `growth-review`), designing the team's standing meetings and forums (that is `design-team-cadence`), or setting team goals and key results (that is `okr-planning`).

Employment paperwork, right-to-work checks, payroll and mandatory training belong to whoever owns them. Confirm they are handled, then leave them alone. This skill covers getting the person productive and oriented.

## Workflow

### 1. Be clear what the first month is buying

Three things, in this order. The order matters, because the first is the one that gets skipped and the one that carries the most risk.

| Purpose | How you know it worked | Cost of skipping it |
| --- | --- | --- |
| The person concludes they made the right decision | They say so unprompted; they start volunteering for things nobody assigned them | The most expensive kind of attrition — a good hire leaving in month seven, after you have paid the full cost of the loop and none of the return |
| They make a real contribution early | Something they wrote is in production and someone depended on it | Long confidence-free ramps; a person who has been busy for six weeks and cannot name anything they did |
| They build the map of systems and people | They route a question to the right person without asking you | Every future question routes through you, permanently |

Confidence is not a by-product of the other two. It is built by things being ready, questions being welcome, and the first week having a shape rather than a shrug. Plan for it explicitly.

### 2. Do the setup before they arrive, and verify it works

Every hour a new person spends waiting for a credential is an hour spent forming an impression of how the place is run, and it is unrecoverable. Work backwards from the start date; most of these have a lead time longer than a day.

| Item | Ready by | Verified how |
| --- | --- | --- |
| Accounts, SSO, group membership, repository and cloud access | Day minus 3 | Someone logs in as them, or the grant is confirmed in the console — not requested |
| Machine that boots, with the toolchain installed or a scripted setup that has been run this quarter | Day minus 2 | A colleague runs the setup on a clean machine |
| Buddy assigned and briefed, and available in week one | Day minus 5 | The buddy has confirmed, and has the week's load reduced |
| First task chosen and left unclaimed | Day minus 3 | It is in the tracker with their name on it |
| First week in the calendar: pairing sessions, system walkthroughs, the team's standing meetings, the manager one-to-one | Day minus 2 | Invitations sent, not intended |
| Named owner for each system they will touch | Day minus 2 | Written down where they can read it |

Ask for the access the role actually needs rather than the access that is convenient to grant, and say so in the request. Cross-reference `access-review`: a joiner copied from the permission set of whoever left last is how standing production access spreads through a team, and it is far harder to take back than to grant narrowly and widen on request.

`references/pre-start-checklist.md` — read this when a start date is confirmed and you are working out what has to be requested when, including the items with multi-week lead times.

### 3. Ship something small in the first week

Choose a task whose value is that it goes all the way through: a small fix, a copy change, a missing log line, a flaky test. Merged and deployed matters more than important.

A change that reaches production proves the whole path works — environment, credentials, review, CI, deploy — and it fails at the exact step that is broken for everyone else too. That step will be a workaround the team stopped noticing a year ago and left out of the setup document. Have the new person fix the document as they hit each problem, in the same week, because they are the only person who can still see what is missing. In four weeks they will have absorbed the workarounds and lost the ability, permanently.

Pair on it rather than assigning it. The goal is not the change; it is that they have now used the tools, opened a pull request, seen the review culture, and watched a deploy.

### 4. Assign a buddy, and keep the two roles apart

The buddy and the manager do different jobs, and merging them removes the safe channel.

- **Buddy** — answers the questions that are embarrassing to ask a manager: what the abbreviation means, why the build takes eleven minutes, whether this is normally broken, who to actually ask. Daily contact in week one, then tapering. Nothing they hear is reported upwards.
- **Manager** — owns the arc: the expectations, the feedback, the first task, the check-ins, and whether the ramp is on track.

A good buddy is someone who joined recently enough to remember being confused, is patient with repeated questions, and knows where things are without being the person everyone already depends on. That last point is the trap: the most knowledgeable engineer is usually the most loaded one, and the buddy who is too busy to answer teaches the new person not to ask. Reduce the buddy's other commitments for the first two weeks, or pick someone else.

### 5. Write 30/60/90 expectations as capabilities, and give them to the person

Write what they should be able to do, not what they should have delivered. "Can pick up a bug in the billing service, find the cause, and ship a fix without help" is a capability. "Closed twelve tickets" measures the tickets.

| Milestone | Shape of the expectation |
| --- | --- |
| 30 days | Environment fluency and a first contribution: can build, test, review and deploy; has shipped something small; knows who owns what |
| 60 days | Independent on defined work: picks up a normal task and finishes it without needing it shaped for them; reviews other people's changes usefully |
| 90 days | Trusted with ambiguity in a slice of the system: handles a problem statement rather than a task, and is on call or ready to be |

Then say honestly, in the document and out loud, that these are a starting point rather than a standard. Ramp time varies with seniority, with how much domain the system carries, with the state of the codebase, and with how much of it is written down. A ninety-day expectation in a well-documented service and the same expectation in a fifteen-year-old billing system are different asks. Adjust the dates at the first check-in when the codebase turns out to be worse than you remembered, and tell the person you are adjusting them — unrevised expectations that the person is silently missing are worse than none.

Share the document with them in week one. Expectations they cannot read are expectations they cannot meet.

### 6. Transfer the context that is not in the code

The code says what the system does. None of the following is in it, and all of it is load-bearing.

| Context | The question it answers | Where it should live |
| --- | --- | --- |
| Why the system is shaped this way | Which constraints are historical and which are still real | Decision records |
| Which decisions are load-bearing | What you must not casually undo | Decision records, named explicitly |
| Who owns what, and who to ask | Where a question goes | An ownership table, kept current |
| Where the bodies are buried | Which service breaks under load, which migration was never finished | Said out loud, then written down |
| The team's vocabulary | What the internal names mean | A glossary, appended to as the new person asks |

Point at `decision-record` for the durable form. A team with no written decisions is running onboarding as an oral tradition: every joiner reconstructs the same reasoning by interrupting the same three people, the answers drift with each retelling, and the reasoning leaves when they do. If nothing is written, have the new person write the first few decision records from what they are told. It is a genuine contribution, it forces the answers to be made explicit, and it is the one time somebody has an incentive to do it.

Walk the system architecture with them in person, on a whiteboard, in the first week. Then have them redraw it from memory in week three and correct where it is wrong — what they got wrong is a map of what the walkthrough failed to convey.

### 7. Ask what was confusing, weekly, while they can still see it

Fifteen minutes at the end of each of the first four weeks, separate from any status conversation.

Feedback runs both ways in these. Yours: what is going well, specifically, and anything to adjust now rather than at day thirty. Theirs: what was confusing, what took longer than it should have, what they expected to find and did not, what the setup document got wrong.

A new person's confusion is free information about your systems, and it expires in about a month — after that they have adapted, and the friction becomes invisible to them too. Capture it in writing as it arrives, and fix the top item before the next joiner. Ask specifically: "what took longest this week", "what did you have to ask somebody because it was not written down", "what surprised you". General invitations to share feedback return nothing from someone six weeks into a new job.

### 8. Onboard remotely on purpose, because nothing happens by accident

Remote onboarding fails through absence, not through anything going wrong. The overheard context, the corridor introduction, the moment somebody notices you are stuck and swivels round — all of that is a default in a room and does not exist otherwise. Substitutes have to be scheduled.

| What stops happening | The deliberate substitute |
| --- | --- |
| Being introduced to people incidentally | A booked fifteen-minute call with each person they will work with, scheduled by you in week one, with a stated reason for each |
| Someone noticing they are stuck | A standing pairing block, daily in week one; an explicit "ask after fifteen minutes" rule so waiting is not the default |
| Overhearing why a decision was made | Discussion moved into public channels rather than direct messages, and a weekly written note from you on what changed and why |
| Reading the room | Saying out loud what the team's norms are: response times, camera expectations, what is urgent and what is not, when people are actually offline |

Timezone spread compounds all of this. If the joiner overlaps the team by three hours, the first week has to be built around that overlap, and asynchronous answers have to be written rather than promised.

### 9. Make the first on-call shift a milestone with prerequisites, not a date

Add someone to the rotation when the prerequisites hold, whatever the calendar says.

- They have shadowed at least one full rotation, including one real page.
- They can find the runbooks, the dashboards and the escalation path without asking.
- They have deployed and rolled back a change themselves.
- They know what they are allowed to do at 3am without permission, stated explicitly.
- Someone is named as their backup for the first two shifts, and knows it.

Then make the first shift a real one and debrief it. Putting someone on call before this is how you get a well-intentioned engineer making an incident worse and concluding it was their fault.

### 10. When it is not working, diagnose before you conclude

Slow ramps and mismatches look identical for the first month and require opposite responses. The difference is in the trend and in the type of difficulty, not in the pace.

| Signal | Usual reading | Action |
| --- | --- | --- |
| Few questions, little visible progress | Does not feel safe asking | Ask directly what they are stuck on; make your own not-knowing visible |
| Questions that are all about the environment | The setup is broken, not the person | Fix the environment; this is your defect, not theirs |
| Work completed but always shaped by someone else | Not enough context to shape it themselves | More context transfer, not more supervision |
| Same explanation needed repeatedly on the same concept | Genuine capability gap — or an unwritten concept nobody has explained properly once | Write it down once, then observe whether it holds |
| Confident output that is consistently wrong in the same way | Real concern; investigate specifically | Concrete feedback now, in the terms `growth-review` uses |
| Progress that is slow but improving week over week | A normal ramp in a hard codebase | Adjust the dates, say so, and leave them alone |

Before concluding it is the person, answer honestly: were expectations written and shared, was the context transferred or assumed, was the first task the right size, was the buddy available, and did they get feedback in week one rather than week eight. Where any of those is no, that is your part, and it belongs in the record.

If a real mismatch remains after that, act early and specifically rather than waiting for the probation date to force it. Hand off to `growth-review` for the ongoing performance conversation; it starts from the same evidence discipline, and a conversation held at week six is still a conversation about ramping rather than a formal process.

`references/ramp-signals.md` — read this when a ramp looks stalled and you are trying to separate a slow start from a genuine mismatch, or before an early conversation about performance.

## Output format

```markdown
## First week — [name], starting [date]

### Before day one
[Item | owner | ready by | verified. Access, machine, buddy, first task,
calendar, ownership list. Anything unverified is not ready.]

### Day one
[Who they meet, what they are told, what they are asked to do. Ends with the
environment building on their machine.]

### Days two to five
[Per day: the pairing block, the walkthrough, the first task, the meeting they
sit in on. Name the person for each, not the team.]

### The first change
[The task, why it is small, what path it exercises, who pairs on it.]

### Buddy
[Who, why them, what their load looks like this week, what they are for.]

### What we expect them to fix as they go
[The setup documentation. Name the file.]
```

```markdown
## 30/60/90 — [name], [role], [team]

### What this is
[Capabilities, not deliverables. A starting point to adjust, not a standard.
Say what would move the dates: codebase state, domain depth, seniority.]

### 30 days — can do
[Three or four capabilities. Each one checkable by observation.]

### 60 days — can do
[Three or four. Independence on defined work.]

### 90 days — can do
[Three or four. Ambiguity in a defined slice, and the on-call prerequisites.]

### Context to transfer, and who owns transferring it
[System | what they need to know that is not in the code | who explains it | when]

### Check-ins
[Dates for weeks one to four, then 30, 60 and 90. What each one asks.]

### Adjusted
[Every revision, with the date and the reason. An unrevised plan that reality
has overtaken is worse than no plan.]
```

## Anti-patterns

**Access requested on day one.** Multi-day approval chains mean the first week is spent waiting, and the person's first lesson about the company is that it cannot organise itself. It is also the cheapest problem on this list to avoid.

**A reading list instead of a task.** Reading without a task to apply it to produces the feeling of learning and none of the retention, and it delays the moment the person discovers what is actually broken in the setup path. Two weeks of documentation is two weeks of no contribution and no confidence.

**The buddy who is the busiest person on the team.** Choosing the most knowledgeable person means choosing the least available one. Unanswered questions teach the new person to stop asking, and that habit outlasts the onboarding by years.

**30/60/90 written and never opened.** Expectations the person has not read cannot be met, and expectations nobody revisits become a document you produce at the end to justify a conclusion you reached by feel.

**Waiting for them to ask.** A person six weeks into a new job asks for far less than they need, because asking feels like evidence they were a mistake. Silence is not a signal that things are fine; it is the absence of a signal.

**Onboarding documentation nobody has followed since it was written.** It describes an environment that has drifted, and every step that no longer works costs the joiner an hour and a small amount of confidence. The only reliable fix is that each new person edits it as they go, while they can still see what is missing.

**Assuming a slow ramp is a bad hire.** The usual causes are a broken environment, missing context and absent feedback, all of which belong to the manager. Concluding it is the person means fixing nothing, and the next hire ramps exactly as slowly.

## Reference files

- `references/pre-start-checklist.md` — read when a start date is confirmed: the full before-day-one list with owners, lead times and how each item is verified.
- `references/ramp-signals.md` — read when a ramp looks stalled: separating a slow start from a broken environment from a genuine mismatch, and what to do about each.
