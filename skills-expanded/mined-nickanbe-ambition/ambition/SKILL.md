---
name: ambition
description: "Find the more ambitious version of a task, plan or feature, with ranked upgrades that each name an outside judge, plus a rewritten brief. Use on /ambition or when asked to think bigger."
license: MIT
---

# Ambition

Based on Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models" (2026-10-13):
https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
The four types of ambition and the techniques under them are his. The steps, modes and output format are this skill's adaptation. Packaged by Nick Beaird.

## The one rule

Ask for a deeper version of the task, not a bigger one. Every upgrade names what will prove it worked, and that judge is never the model itself.

## Inputs

- The task as stated.
- `mode`: planning | research | feature. Infer it; ask only if truly ambiguous.
- `size`: light | full. If the person says one, use it. Otherwise use light, and switch to full when the result feeds a decision that is costly to reverse (money, headcount, a launch, a public claim).
- What is in reach: data, files, connectors, environments, and whether the model can install software and run code. Every type of ambition depends on this, so note what is missing.

If the task is trivial (a model finishes it in minutes and nothing depends on it) and the person did not invoke this skill by name, say so in one line and do the task. When they did invoke it, run the pass anyway. Small is not trivial: a task is trivial only when the pass finds nothing worth adopting (a rename, a lookup, a one-line message). Then keep the Recommended brief to the task as asked plus at most one cheap check, and list anything bigger only as an upgrade to pick; a trivial task made heavy is not ambition. If the pass finds neighbouring failures or a wrong assumption, the task is not trivial and the brief adopts the top upgrades as usual.

In full mode, if you do not know what decision or outcome the work feeds, ask that one question before starting any subagents.

## Step 0: Baseline (Speed)

Felix skips Speed ("the same work in less time") because it takes no creativity. Here it is the control: write the literal task in one sentence and the fastest competent way to do it. Every upgrade is described as a change from this baseline.

## Step 1: Altitude

Go up in abstraction: the outcome, not the task. A task is someone's best guess at how to reach an outcome.

- What should happen after this is done? What is the goal beyond the goal?
- What decision, meeting or person does this feed? If people will hold meetings about it, Altitude is a good fit.
- What would owning the outcome continuously look like, instead of doing the task once? ("Fix this crash" becomes "keep the app crash-free.")
- What plumbing would let that run without anyone re-prompting: data feeds, environment access, version-to-commit mapping, a way to reproduce and verify independently?

Output a ladder of 2 to 3 reframes from the current task to the most ambitious, each with the access it needs.
Stop climbing where the outcome can no longer be measured or acted on with the access available. "Go make money" is past that point.
Go light on this step for creative work that has no ultimate outcome.

## Step 2: Depth

Do the task the way a field-leading expert would, one layer below where it was asked, and keep going until those experts might learn something.

Answer the four questions from Felix's prompt "I want a deeper version of this task, not a bigger one":

1. What would a top professional in this field do here that was not asked for?
2. What is the rawest material they would start from, instead of what has already been digested?
3. Which specific methods and tools would they use? Name them concretely (a database and a survival model, not a markdown table). Changing vocabulary without changing method is a failure.
4. What, other than the model or the user, would show the result is right? (test suite, holdout data, benchmark, profiler, external reviewer, real users)

Then add:

- **Stretch target:** a number or a pass/fail test, set far past the stated one, and treat it as reachable. A page asked to load in 5 s instead of 10 s gets a 200 ms target; "find out why sales dropped" becomes "explain 90% of the drop with named causes, each confirmed outside this analysis". If you know of something comparable that has been done, cite it; seeing it done is the strongest argument that it can be. Never invent a precedent.
- **Challenge an assumption:** name the belief the task rests on and how to try to reproduce it from raw data.
- **New knowledge:** one thing the work could find that nobody knows yet, and how to show it holds on data it has not seen.

## Step 3: Range

Bring in fields beyond the obvious one.

- **Nouns to verbs** (a trick from Kelley and Littman's *The Art of Innovation*): rewrite the deliverable as what it does. "A QBR deck" becomes "get busy people to believe a story about cause and effect, and decide under uncertainty, in 30 minutes."
- **Assemble the crew:** pick 3 to 5 fields the verbs call for, with at least one adversarial (short seller, forensic accountant, auditor, pen tester, opposing counsel).
- For each field, state the method it applies and the artifact it produces. Do what the field does; never write in a character's voice. Role-play makes transcripts weirder without improving outcomes.
- In full mode, when subagents are available and raw material is in reach, run each field as a parallel read-only subagent on it. Each returns its method, its first finding and what it would need to go further, in under 150 words. If no raw material is in reach yet, skip the subagents and add a Needs column to the crew table.

## Lead type by mode

| Mode | Lead | Why |
|---|---|---|
| planning | Altitude | Plans feed decisions and meetings; the outcome and the durable workflow matter most |
| research | Depth | Raw data, challenged assumptions, new knowledge, held-out validation |
| feature | Depth, then Altitude | Tests, benchmarks or a profiler as the outside judge; then owning the outcome (crash-free, not one crash fixed) |

All four types still run in every mode; the lead gets the most space. Never skip Range: it is the easiest to under-weight and often where the surprise is.

## Step 4: Synthesis

Output in Markdown:

```
## Ambition: <task in under ten words> [<mode>] [<size>] <YYYY-MM-DD>

### Baseline
<one sentence>

### Passes
<light: one line each for Altitude, Depth and Range>
<full: the Altitude ladder, the four Depth answers plus stretch target, assumption and new knowledge, and the Range crew as a Field | Method | Artifact table (add Needs when subagents were skipped)>

### Upgrades (ranked)
| # | Type | Upgrade | Cost | Payoff | Judge |
|---|---|---|---|---|---|

### Recommended brief
<the task rewritten as a prompt that adopts the top upgrades, ready to run. It must stand alone: whoever runs it may see nothing else, so restate every explicit requirement of the original (files, formats, schemas, deadlines) word for word, and never point to the upgrades table by number>

### Needs from you
- <access, data, environments, decisions>
```

The brackets in the header are literal, for example `## Ambition: Add CSV export [feature] [light] 2026-10-16`.

- **Cost** is model time (rounded to minutes, hours or days of agent work; do not fake precision), plus what a person must supply (access, data, a decision, their own time in a meeting), plus elapsed time when the judge needs it ("two weekly sends"). Never estimate the work itself in human work-days; that anchors on how long it took before models and talks the plan down. List every prerequisite (keys, purchases, access) and count the person's back-and-forth steps; those run long far more often than agent time does.
- **Payoff** is what changes for the person if the upgrade works, in one phrase.
- **Rank** by payoff against cost, favoring the lead type. Types may repeat or be missing from the list; do not force one upgrade per type.
- **Judge** is something that can actually run. It may run later (a 90-day review, the next three sends) if it names who runs it, when, and how the result comes back to the person; put the wait under Cost. A sign-off with no owner or date is not a judge. When the access it needs is unknown, keep the upgrade and put the access under "Needs from you".

Then stop. The person picks which upgrades to adopt. Never expand scope on your own, and start no further research or subagents before they pick.

## Light vs full

- **Light:** one line per type under Passes, naming that type's strongest move rather than answering every question in its step. Exactly 3 upgrades, no subagents, under 450 words in total; count before finishing and cut Passes first. Keep table cells short.
- **Full:** every question answered, the crew run as subagents when available, top 5 upgrades, a brief ready to execute. Stay under about 1,200 words; cut anything that does not change the ranking or the brief.

## Example: Felix's running example, a quarterly business review

The Altitude row is his three-step escalation. The Depth and Range rows arrange his techniques by level, and the Speed row is the baseline this skill adds.

| Type | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| Speed | Fill last quarter's template with this quarter's numbers. | Pull every figure from source systems and draft all slides. | Full deck from live data, ready for review within the hour. |
| Altitude | Explain what changed this quarter, why, and what to do about it. | Find the three most urgent decisions and argue each side. | Design something that catches problems earlier than a quarterly deck, prove it on past data, run it beside the deck for a quarter. |
| Depth | Analyze churn in a real database with a statistical model. | Test "churn is an onboarding problem" against raw event logs. | Simulate last year's customers, find an unknown churn signal, show it predicts an unseen quarter. |
| Range | Restate the review as verbs: get busy people to believe a story and decide in 30 minutes. | An analyst, a journalist and an editor each do their real job on the story. | A short seller and a forensic accountant try to break it before leadership sees it. |

## Guardrails

- No self-grading. An upgrade with no outside judge is cut or flagged as unverified.
- No role-play; fields contribute methods, not voices.
- Stretch targets are held honestly: when the work runs, report the measured result next to the target. If one proves infeasible after a real attempt, say what blocked it and propose the next-best target.
- Show cost beside every upgrade, and do not let cost talk the plan down.
