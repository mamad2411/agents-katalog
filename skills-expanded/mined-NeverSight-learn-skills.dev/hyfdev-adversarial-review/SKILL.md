---
name: hyfdev-adversarial-review
description: Adversarial review (对抗 review) of a finished deliverable — a change ready for a PR, an investigation report, a recommendation, a batch of record edits — before it is reported to the user. Spawns fresh reviewer subagents briefed to disprove it from three directions (open, over-engineering, residue), verifies and fixes what holds, then reports. Run once per deliverable when it is considered done, and on request at level strong (强力) or max (极致). Not for answers to questions, lookups, or steps inside a task.
---

# Adversarial Review

Run this after a deliverable is finished and before it reaches the user. The goal is to disprove the deliverable with evidence and to find what the working session left in it, not to confirm it.

## Terms

- **Deliverable**: a complete unit the user will act on, merge, publish, or rely on — a change ready for a PR, an investigation report, a recommendation, a batch of record edits. A step inside a task, an answer to a question, a lookup, or a mechanical edit is not a deliverable.
- **Direction**: what a reviewer is told to look for. Three directions exist — open, over-engineering, residue — and their texts below are used verbatim.
- **Residue**: text in the deliverable that only a participant of the working session can resolve. The residue direction below lists its forms; the test is that a reader at HEAD with no access to the session can resolve every reference and verify every claim.
- **Brief**: what a reviewer receives — one or two directions and the facts needed to locate the work, nothing else.

## When

- Once per deliverable, when the main agent considers it done and before reporting it, and whenever the user invokes the skill.
- Invoking this skill is the request to spawn the reviewers; do not ask for a separate confirmation. Report the review in the deliverable's report; ask the user only when you are choosing not to run it.
- When no subagent can be spawned, do a bounded self-review against the three direction texts and say in the report that independent review was not available.

## Levels

The user names the level in the invocation or the message; without a name, run the default.

- **Default**: one round. Two fresh subagents in parallel — Reviewer A: open; Reviewer B: over-engineering and residue together. Fix, then report.
- **Strong (强力)**: two rounds. Round one as above, fix, then round two with new fresh subagents and the same briefs — they review the fixed deliverable and know nothing of round one — fix again, then one report covering both rounds.
- **Max (极致)**: strong, with two fresh subagents per direction in every round — four per round, eight in total. Reviewers of the same direction get the same brief and do not know of each other.

## Reviewers

A fresh subagent is a new agent with no inherited context, never a fork of the main agent; it has no access to the working session. It discovers the work itself: runs `git diff <base>...<head>`, reads the surrounding code or the whole report, runs checks when it needs them. Do not hand it the diff, a summary, or a list of places to look.

## The brief

Fill the template and add nothing outside it. The main agent's plan, reasoning, summary of what it did, self-assessment, the history of corrections, hints about weak spots, and other reviewers' output never enter a brief.

```text
Direction: <open | over-engineering + residue>
Deliverable: <code change | report | record edits>
Location: <worktree path with base and head refs | PR number | file paths>
Request: <the user's request, verbatim | issue #N | path to the file that states the task>
Return: pass, or at most five findings per direction, ranked by how much each would change the result. For each: location, evidence, why it matters.

<direction text, verbatim from this skill>
```

`Request` is the user's own words or a durable source they pointed at, never the main agent's restatement. When the user adopted an agent-written candidate by reference, their adopting message and the adopted candidate, both verbatim, are the request; a summary of what was agreed earlier is not. When the request already exists somewhere durable — an issue, a task file — point at it instead of quoting.

## Direction texts

### Open

Try to disprove this deliverable. Find anything that would make it wrong to accept as is: factual or logical errors, unsupported claims, missing evidence, behavior that differs from what was required, untested or broken paths, an overlooked alternative that would change the decision. Rank findings by how much they would change the result. Omit style. A missing defense against a threat the repository does not promise to handle is not a finding.

### Over-engineering

Find what this deliverable contains that the request did not require: scope beyond the ask; an abstraction, option, or parameter with a single consumer; configuration or fallbacks for situations nobody asked for; defensive code against threats the repository does not promise to handle; tests or documentation for behavior this change did not introduce; hand-rolled code where the repository already has a helper or dependency. For each item, name what it costs and what the smaller version is.

### Residue

Read every piece of text in the deliverable — code, comments, tests, docs, commit messages, PR title and body, report prose — as a reader at HEAD who has no access to the working session. Flag anything that reader cannot resolve or that speaks to someone who is not there: references to things removed or tried, narration of the change instead of the state, justification addressed to a reviewer, tests or comments that guard the absence of something, hedges and planning residue. For each, quote the sentence and give the present-tense restatement, or say "delete". Records whose subject is a decision or its history — decision records, decision ledgers, postmortems — state what was decided, tried, and why; that content is not residue.

## Synthesis

- Fix by default. Verify each finding against the evidence yourself and apply what holds without asking first. Two exceptions, and neither is a question to the user: an edit that the user's rules reserve for their approval is shown instead of applied; a finding that contradicts an instruction the user gave in this task is not applied, and the report says so.
- A theoretical, hostile-environment, or defense-in-depth finding is recorded, not implemented, unless the task includes that threat model or the repository already promises that resilience.
- Do not count votes. Two reviewers reporting the same finding is one finding, not stronger evidence; merge findings by content.
- Fix residue by restating in the present tense or deleting, never by adding a note that something was reviewed or removed.
- Report to the user after the fixes: what was found, what changed, what was not applied and why. For strong and max, one report for all rounds.
