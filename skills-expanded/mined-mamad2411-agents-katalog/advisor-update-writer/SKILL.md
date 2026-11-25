---
name: advisor-update-writer
description: Write decision-oriented advisor, mentor, lab meeting, or research progress updates from project memory, experiment reports, papers, code changes, logs, and notes. Use this skill whenever the user needs a weekly update, advisor email, meeting note, progress memo, decision request, blocker summary, project status report, or concise research update that connects evidence, risks, options, asks, and next actions.
argument-hint: "[project-dir] [--audience advisor|lab|collaborator] [--mode weekly|decision|meeting|email]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Advisor Update Writer

Write concise research updates that help an advisor, mentor, collaborator, or lab audience make decisions.

Use this skill when:

- the user needs a weekly update, advisor email, lab update, meeting memo, or collaborator status note
- experiment results, writing progress, reviewer risks, or implementation blockers need to be summarized
- the update should ask for a decision, feedback, resources, compute, paper-positioning advice, or priority choice
- project memory should be turned into a human-readable progress report
- several feedback loops need to be reconciled: algorithm, experiments, writing, review, rebuttal, artifact, or release

Do not use this skill for a full experiment report. Use `experiment-report-writer` when the main artifact is a detailed technical report. Use this skill when the main artifact is a decision-oriented communication.

Pair this skill with:

- `research-project-memory` to recover current status, decisions, claims, evidence, risks, and actions
- `experiment-report-writer` when detailed experiment evidence needs a source report
- `figure-results-review` when plots or tables will be shown to an advisor
- `result-diagnosis` when negative or ambiguous results need a decision
- `paper-positioning-planner` when the update asks for paper-story or target-venue feedback
- `paper-evidence-board` when writing and experiment gaps need a synchronized action list
- `work-timeline-planner` when the update needs retrospective timeline evidence

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── decision-framing.md
    ├── memory-writeback.md
    └── update-template.md
```

## Progressive Loading

- Always read `references/decision-framing.md` and `references/update-template.md` before drafting a saved or high-stakes update.
- Read `references/memory-writeback.md` when the update creates decisions, actions, or durable feedback that should persist.

## Core Principles

- Start with the decision-relevant delta since the last update.
- Separate facts, interpretation, risks, and asks.
- Do not bury the request. Make the advisor's needed input explicit.
- Compress raw experiment detail into evidence and implications; link to detailed reports when needed.
- Include negative results when they change the project decision.
- Turn feedback into actions and memory updates after the meeting or response.
- Match the audience: advisor updates are direct and decision-heavy; lab updates need more context; collaborator notes need ownership and handoff.

## Step 1 - Classify the Update

Choose the mode:

- `weekly`: progress since last update, current blockers, next week plan
- `decision`: options, evidence, recommendation, explicit ask
- `meeting`: agenda, discussion points, decisions needed, notes after meeting
- `email`: concise message with context, status, ask, and attachments
- `lab`: broader context, key result, what the audience should remember

Identify:

- audience and expected length
- deadline or meeting time
- project phase
- key evidence since last update
- unresolved decisions
- desired advisor action
- save path, if a file is requested

If saving and no path is given, use:

```text
docs/updates/advisor_update_YYYY-MM-DD.md
```

## Step 2 - Gather Current State

Prefer project memory when available, then primary files.

Look for:

- `memory/current-status.md`
- `memory/decision-log.md`
- `memory/claim-board.md`
- `memory/evidence-board.md`
- `memory/risk-board.md`
- `memory/action-board.md`
- experiment reports, paper drafts, reviewer notes, rebuttal notes, and recent git commits

Extract:

- what changed
- what evidence supports the change
- what failed or remains uncertain
- what decision is now required
- what the user recommends
- what happens next

## Step 3 - Frame the Decision

Read `references/decision-framing.md`.

For each decision, produce:

- decision question
- options
- evidence for and against each option
- risks if delayed
- recommended option
- exact advisor ask
- next action after a yes/no/alternative answer

If there is no decision needed, frame the update around progress, risks, and next actions.

## Step 4 - Draft the Update

Read `references/update-template.md`.

Default structure:

- one-line status
- key progress
- evidence and interpretation
- blockers or risks
- decision/ask
- next actions

For email, make the first paragraph enough to answer "what do you need from me?"

For meeting notes, include both agenda and post-meeting decisions if the meeting has already happened.

## Step 5 - Check the Update

Before finalizing:

- every important claim has evidence or is marked as interpretation
- the ask is explicit
- blockers have owners or proposed next steps
- negative results are not hidden if they affect direction
- the update is short enough for the audience
- attachments or links are named
- any decisions or feedback are ready for memory writeback

## Step 6 - Write Back After Feedback

Read `references/memory-writeback.md` when memory exists.

Update decisions, actions, risks, and status after the advisor responds or after meeting notes are finalized.
