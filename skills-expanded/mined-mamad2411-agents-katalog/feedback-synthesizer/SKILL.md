---
name: feedback-synthesizer
description: Turn inbound advisor, collaborator, or reviewer feedback into structured project updates. Use when meeting notes, emails, or review comments need to become claim updates, risk entries, action items, and experiment decisions — distinct from rebuttal writing for formal reviews.
argument-hint: "[project-dir] [--source advisor|collaborator|reviewer|committee] [--mode synthesize|triage|update]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Feedback Synthesizer

Convert unstructured inbound feedback into durable project memory. This skill answers: given what an advisor, collaborator, or reviewer said, what should change in claims, risks, experiments, writing, or decisions?

Use this skill when:

- an advisor meeting produced suggestions, concerns, or directions that need to become action items
- a collaborator sent comments on a draft, method, or results that need to be classified
- an informal reviewer or colleague shared pre-submission feedback
- committee meeting notes need to be turned into a structured decision record
- feedback is scattered across emails, documents, and notes and needs to be consolidated
- you want to update project memory after feedback without losing or misinterpreting the signal

Do not use this skill for formal review responses after a submission decision — use `rebuttal-strategist`. Do not use this skill to write the feedback update reply — use `advisor-update-writer`.

Pair this skill with:

- `rebuttal-strategist` for formal reviewer responses after an acceptance/rejection decision
- `advisor-update-writer` to write the follow-up update or reply after synthesis is done
- `research-project-memory` to propagate synthesized decisions to memory boards
- `experiment-design-planner` or `result-diagnosis` when feedback calls for new experiments or reinterpretation

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── templates/
    └── feedback-record.md
```

## Progressive Loading

- Read `memory/claim-board.md`, `memory/risk-board.md`, and `memory/action-board.md` before synthesizing — feedback must be checked against existing project state.
- Read `paper/.agent/paper-evidence-board.md` when feedback touches paper claims or results.
- Read `templates/feedback-record.md` before writing a feedback record.

## Core Principles

- Not all feedback is equal: distinguish must-address from should-address from noted.
- Feedback that challenges a core claim requires a stronger response than feedback about presentation.
- Scope matters: advisor feedback about direction is different from collaborator feedback about a figure.
- Record the source and date of every synthesized feedback item.
- Avoid over-promising: only commit to experiments or rewrites that are in scope for the current phase.
- Incoherent or contradictory feedback should be flagged, not silently resolved.

## Step 1 — Gather Feedback Source

Collect:

- the raw feedback: meeting notes, email text, document comments, or voice memo
- the source: advisor, collaborator, committee member, informal reviewer
- the date
- the context: draft reviewed, result presented, meeting type

Identify what artifact or claim the feedback is responding to.

## Step 2 — Triage Feedback Items

For each distinct feedback point, classify:

| Field | Value |
|---|---|
| Feedback item | (quoted or paraphrased) |
| Source | advisor / collaborator / informal-reviewer / committee |
| Target | claim / experiment / writing / method / data / framing / scope |
| Tone | concern / suggestion / direction / question / praise |
| Priority | must-address / should-address / noted / disagree |
| Affects submission | yes / no / unclear |

Priority rules:

- `must-address`: core claim is challenged, fatal weakness identified, or advisor/supervisor explicitly directed a change
- `should-address`: valid concern that weakens the paper or wastes compute if ignored
- `noted`: stylistic preference, minor suggestion, or nice-to-have
- `disagree`: feedback that conflicts with existing evidence, is based on a misunderstanding, or the team has deliberated and decided not to follow

## Step 3 — Link to Project Memory

For each must-address or should-address item:

- **Claim impact**: Does this feedback challenge or support an existing claim in `memory/claim-board.md`? Update claim strength, wording, or evidence requirements.
- **Risk**: Does this create or heighten a risk? Add or update `memory/risk-board.md`.
- **Action**: Does this require an experiment, rewrite, data collection, or analysis? Add to `memory/action-board.md` with priority.
- **Decision**: Does this change a design or scope decision? Add to `memory/decision-log.md`.
- **Evidence**: Does this identify a missing evidence slot? Add to `memory/evidence-board.md` with status `missing` or `planned`.

For `disagree` items: record the disagreement and the rationale for not acting. This protects the project if the same concern reappears.

## Step 4 — Write the Feedback Record

Use `templates/feedback-record.md`.

Save to:

```text
memory/feedback/<YYYY-MM-DD>-<source>-<topic>.md
```

The record should include:

- meeting / feedback context
- triage table with all items classified
- memory updates made
- open decisions or experiments triggered
- disagreements logged with rationale
- follow-up actions and owner

## Step 5 — Route Follow-Ups

- `advisor-update-writer`: draft the reply or follow-up update after synthesis
- `experiment-design-planner`: plan experiments triggered by must-address feedback
- `result-diagnosis`: reinterpret existing results in light of new concerns
- `paper-evidence-board`: update claim/evidence alignment when feedback changes what the paper needs to prove
- `paper-writing-assistant`: revise specific sections flagged by feedback
- `rebuttal-strategist`: if formal reviews arrive with an acceptance/rejection decision

## Final Sanity Check

Before finishing:

- every must-address item has an action, risk entry, or decision
- every claim-level challenge has been checked against existing evidence
- disagreements are documented with rationale, not silently dropped
- feedback record is saved in `memory/feedback/` with date and source
- next action is clear
