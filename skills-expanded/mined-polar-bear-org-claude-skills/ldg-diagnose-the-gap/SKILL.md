---
name: ldg-diagnose-the-gap
description: Diagnoses one performance problem before anything is built, producing desired versus actual by task, a cause table that separates skill and knowledge from information, tools, incentives and process, an option per cause and a recommendation that can say "no training". Use for "run ldg-diagnose-the-gap", "performance gap analysis", "performance consulting", "is it a training problem", "root cause of a performance problem", "cause analysis", "why are people not doing it", "training did not fix it", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Diagnose the Performance Gap

## When To Use
Every performance problem becomes a training request, even when the manager, the process or the tools are the cause. Use this when a request came back "environment" or "unclear", or when a course has already run and the measure did not move. It answers: what is causing this gap, and which fix, training or not, fits each cause?

## When Not To Use
This is one problem and one diagnosis. For the picture across a whole role or team, use Assess the Training Needs. It also stops at a recommendation: the meeting where you take that recommendation to the person who asked is Prepare the Sponsor Conversation.

## Inputs
- The problem line from the request note, or the request with whatever evidence came with it (error counts, tickets, cycle times, complaints).
- What people in the role work with: the process, the tools, the guidance, the targets, and how good work gets noticed.
- The size of gap you consider worth acting on.
If you have none of this, I start from the problem line alone, mark every cause "assumed" and mark the output as a first draft.

## Approach
Performance analysis and cause analysis from the Human Performance Technology model attributed to ISPI (public university page), followed by choosing an intervention per cause. The judgement is to look at the conditions around the work before looking at the people in it. The failure it prevents: a refresher is built for a team that already knows the procedure, while the screen they work in still hides the one field they keep missing, and six weeks later the refresher is blamed.

## Workflow
1. Ask at most three questions: in which tasks does the gap show, which number or report shows it, and what size of gap is worth acting on?
2. Per task, write desired and actual in the same unit, then the gap. Mark each task "act" or "watch" against the threshold you set; a gap you cannot measure yet is "watch" with the measure to start collecting.
3. Build the cause table in two sides. Environment: information and feedback, tools and resources, incentives and consequences, process. Role side, never a person: skill and knowledge, capacity, motivation (what the work rewards). Start with the environment side, because it is the one requesters skip.
4. Give every cause its evidence, or mark it "assumed" with a way to check it: a report to pull, a question for you to ask people in the role, an hour of watching the task.
5. Ask the skill question per task: could people in the role do it correctly if conditions were right, or have they done it right before? If yes, it is not a skill gap, however firmly a course was asked for.
6. Choose one option per cause: job aid, process fix, feedback, tool, incentive change, manager conversation, training. Training only for skill and knowledge causes.
7. Write the recommendation. It combines options, says what training alone would not fix, and says "no training" in those words when that is what the evidence supports.

## Output Format
```markdown
# Performance Gap Diagnosis
Problem: [role] are [actual] and need to be [desired], shown by [measure] | Act threshold: [set by you]
## Gap by task
| Task | Desired | Actual | Gap | Act or watch | Could they do it if conditions were right? |
|---|---|---|---|---|---|
| [task] | [value, unit] | [value, same unit] | [difference] | [act / watch] | [yes: not a skill gap / no: skill gap / to check] |
## Causes
| Task | Cause | Side and category | Evidence or "assumed" | How to check |
|---|---|---|---|---|
| [task] | [cause] | [environment: information, tools, incentives, process / role: skill, capacity, motivation] | [source] | [check and who runs it] |
## Option per cause
| Cause | Option | Training? | Owner (role) |
|---|---|---|---|
| [cause] | [job aid, process fix, feedback, tool, incentive change, manager conversation, training] | [yes / no] | [role] |
## Recommendation
[The combined fix in three lines. What training alone would not fix. "No training" if that is the finding.]
## Decision
[Sponsor] decides with [L&D lead] which options go ahead, by [date].
```

## Done When
- Every task has desired and actual in the same unit and an "act" or "watch" call.
- Every cause has evidence, or says "assumed" and carries a way to check it.
- Every training option sits against a cause that passed the skill question.
- The recommendation states plainly what training alone would not fix.

## Quality Bar
- Thresholds and gap sizes are yours; Claude never supplies a norm or a typical figure.
- Motivation is read at role level (what the work rewards or punishes), never as a verdict on anyone's attitude.
- No "low performer" list, and no cause about a named person's capacity or motives.
- An assumed cause never carries a training option until someone has checked it.
- Claude drafts the diagnosis from your evidence; a named person decides whether anything gets built.

## Next
Run ldg-prepare-the-sponsor-conversation (Prepare the Sponsor Conversation) to take the diagnosis to the person who asked.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
