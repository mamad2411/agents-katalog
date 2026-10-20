---
name: retention-review
description: "Review why people actually leave and what keeps them — regretted-attrition analysis over time rather than one exit interview, themes aggregated across departures, stay interviews that surface a risk before the resignation, flight-risk signals, engagement-survey results turned into a few owned actions, and a counter-offer policy agreed in advance. Use this skill whenever someone asks why people are leaving, how to reduce attrition, what a stay interview or exit interview should ask, whether to counter an offer, how to read an engagement survey, or how to spot who is at risk of leaving — including phrasings like \"two people quit this quarter\" or \"we keep losing seniors\". Do not use it for onboarding a joiner (onboarding-plan), the pay mechanics behind a retention case (compensation-benchmarking), team delivery health (delivery-review), or writing up an incident (postmortem)."
allowed-tools: Read, Write, Grep, Glob
---

# Retention Review

A retention review is done well when it rests on aggregated evidence rather than on the last departure, ends in a small number of changes with owners and dates, and holds the stay conversation early enough that the resignation is not the first signal. The output is what you will change, who owns it, and how you will know it worked.

The job is hard because the evidence arrives late, polite and unrepresentative. The exit interview happens after the decision is irreversible, is often conducted by the very manager whose team the person is leaving, and is answered with a version of the truth that protects the leaver's references. The people most at risk rarely announce it; they go quiet, then resign. Meanwhile the engagement survey produces a score, the score is presented, and nothing changes — which teaches the team that saying something is pointless and makes the next survey worse. Attrition is felt as one dramatic story and measured as a rate, and the story usually wins, so the fix chases the loudest departure while the structural cause — a level with no growth path, a band that fell behind, one team absorbing all the churn — keeps producing the next one. This skill exists to read the aggregate, to ask before rather than after, and to convert the finding into a handful of changes somebody owns.

## Scope

Use for: analysing why people leave and who is at risk; designing exit and stay interviews; reading attrition data by team, level, tenure and manager; turning an engagement survey into owned actions; setting counter-offer policy; the retention conversation with someone you want to keep.

Do not use for: onboarding a new joiner (`onboarding-plan`); the pay structure and benchmarking behind a retention case (`compensation-benchmarking`); team delivery health (`delivery-review`); or writing up an incident (`postmortem`).

## Workflow

### 1. Separate the kinds of attrition

A single attrition rate mixes things that need different responses. Split it first.

| Dimension | Why it matters |
| --- | --- |
| Regretted or not | Losing someone you wanted to keep is the signal; a managed exit is a different event |
| Voluntary or involuntary | Only voluntary regretted loss is what retention addresses |
| Level and role | Losing seniors and staff is usually structural; losing juniors is often ramp and management |
| Team and manager | A cluster is a signal to investigate management practices, support, team size, pay, level mix, cohort and recent reorganisation before attributing a cause |
| Tenure at exit | Under a year is hiring and onboarding; two to four years is growth and pay |

Compute each over comparable periods with headcount denominators, ideally at least a year, and against the team's own baseline rather than a company-wide figure that hides the cluster.

### 2. Aggregate the exit data over time

One exit interview is limited evidence, but a credible individual report can warrant action now. Aggregate exits to test recurring patterns; mark uncertainty when samples are small and do not wait for a fixed count before addressing a plausible risk.

- Collect the reasons in a fixed set of categories, so the counts are comparable year to year.
- Separate the stated reason from the probable one. "Better opportunity" is what people say; the follow-up question is what the opportunity offered that this role did not.
- Look for the cluster: is it one team, one level, one manager, one recent change?
- Read the regretted losses on their own. The pattern in the people you wanted to keep is the retention finding; the pattern across all leavers is diluted by the exits you did not mind.

`references/attrition-review.md` has the categorisation, the questions that get past the polite answer, and a worked aggregation.

### 3. Ask before, not after

The exit interview is a postmortem on a decision already made. The stay interview is the preventive half, and it is the one that changes outcomes.

Run a stay interview at a deliberate moment — a work anniversary, a change of manager, the end of a project, or when a signal appears — not only when you suspect trouble. Ask what keeps them, what would make them consider leaving, what they want next and whether they can see it here. Then act on the answer, because a stay interview followed by no change is worse than none: it has told the person that even when asked directly, nothing moves.

`references/stay-interviews.md` has the question set, who should run it, and how to respond to the three kinds of answer.

### 4. Read the flight-risk signals

No one signal predicts a departure; a cluster of them does. Watch for these, and treat a change in any one as a prompt for a conversation rather than a conclusion.

- **A drop in discretionary effort** — quieter in reviews, less mentoring, doing the defined job and no more.
- **A band that has fallen behind** the market or a peer, or a level with no visible next step.
- **A manager change** or a reorg that moved the person's work or sponsor.
- **A project ending** with nothing named as next.
- **A skill that is suddenly more marketable** than the role rewards — the person has grown past the job.
- **Life events** that change what the job has to be: a move, a caring responsibility, a partner's job.

None of these is a reason to act on the person's behalf or to assume the decision. Each is a reason to have the conversation in step 3 while it still matters.

### 5. Turn the survey into a few owned actions

An engagement survey is useful only up to the point it produces changes. A score presented without a decision is how a survey stops being answered honestly.

- Pick two or three themes, at most, and say why those. A team cannot act on twelve.
- Convert each into a change with an owner and a date, and say what will be different and when.
- Separate what the team controls from what the company controls. For the company-level items, say plainly that they are outside the team's control rather than pretending to fix them.
- Close the loop: report back what changed and what did not, before the next survey. This is the step that keeps the data honest.

### 6. Set counter-offer policy in advance

Deciding each counter-offer under pressure is how a structure erodes and how a team learns that outside offers are the path to a raise. The pay mechanics belong to `compensation-benchmarking`; the retention policy belongs here.

- Decide in advance what is counterable — usually pay that fell behind the band, or a level never recognised — and what is not.
- A counter is a retention case with its own reason and budget line, not a quiet band breach.
- Ask why they looked. The external offer is rarely the whole reason, and a counter that ignores the real reason buys months.
- Expect the lesson to spread: whatever you reward, you will get more of.

### 7. Act, then close the loop

The review ends in a small number of changes, each with an owner and a date, plus the retention conversations worth having now. Then tell the team what changed and what did not — the loop back is what makes the next review's data trustworthy.

If the finding is that the pay structure, not the manager, is the cause, hand the structural part to `compensation-benchmarking`; if it is that a level has no growth path, the case is `growth-review`'s.

## Output format

```markdown
## Retention review — [team / group], [period]

### The attrition, separated
[Regretted voluntary, by level, team and tenure, against the baseline. The cluster named.]

### What the leavers said, and what it probably meant
[Aggregated themes with counts, over at least a year. The stated reason beside the
probable one.]

### Who is at risk, and why
[Signals observed, per person or cohort. Explicitly not a conclusion about any
individual's decision.]

### Stay-interview findings
[What people said keeps them, what would make them leave, and what they want next.]

### What we will change
[Two or three items: the change, the owner, the date, and how we will know.]

### Counter-offer policy
[What is counterable and what is not, decided in advance.]

### What is outside our control
[Company-level items, stated plainly rather than promised.]
```

## Anti-patterns

**Acting on one dramatic exit.** The most recent or most senior departure sets the whole response, and the structural cause that produced it — and will produce the next one — is never examined. Aggregate first.

**The exit interview run by the leaver's own manager.** The person will not tell the truth to the person they are leaving, and the manager is the party with an interest in the answer. Have someone else run it, or accept that the data is thin.

**Stated reasons taken at face value.** "Better opportunity" and "personal reasons" are the polite defaults. The useful answer is behind one more question.

**A survey with no actions.** The score goes up on a slide, nothing changes, and the next survey is answered less honestly because the team learned that saying something has no effect.

**Stay interviews only when trouble is suspected.** The conversation arrives as a signal that the person is already a problem, so they answer defensively, and the tool that was meant to prevent a departure becomes the thing that precipitates it.

**Counter-offers as the retention strategy.** It teaches the team that the route to a raise is an outside offer, and it fixes the symptom while the reason they looked remains. Set the policy before the pressure.

**Confusing attrition with performance management.** A regretted loss and a managed exit are different events with different causes. Mixed into one number, neither can be read.

## Reference files

- `references/attrition-review.md` — read when analysing departures: the fixed reason categories, the questions that get past the polite answer, how to separate stated from probable reasons, the cohort cuts that reveal a cluster, and a worked year of aggregated attrition.
- `references/stay-interviews.md` — read before running a stay interview: who should run it and when, the question set, how to respond to a happy, an ambivalent and a ready-to-leave answer, and the follow-through that keeps the next one honest.
