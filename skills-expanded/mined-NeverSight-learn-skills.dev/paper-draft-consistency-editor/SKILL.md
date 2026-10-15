---
name: paper-draft-consistency-editor
description: Edit ML/AI paper drafts for internal consistency. Use after sections exist to align claims, terminology, figures, tables, captions, limitations, and conclusion.
argument-hint: "[paper-dir] [--mode audit|edit|report] [--scope full|claims|terms|figures|results]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Paper Draft Consistency Editor

Check and fix whether a paper draft is internally coherent. This skill is an editor pass, not a reviewer simulation and not a first-draft writer. It makes the title, abstract, introduction, methods, results, figures, tables, captions, related work, limitations, and conclusion agree with the paper's active claims and evidence.

Use this skill for:

- title/abstract/intro/conclusion consistency
- contribution bullet to experiment mapping
- claim strength drift across sections
- terminology, method name, dataset name, baseline name, metric name, and notation consistency
- figure/table/caption/main-text alignment
- result prose that no longer matches updated numbers
- unresolved `PROVISIONAL-RESULT` or `PR-###` placeholders
- checking whether the draft follows `paper/.agent/writing-contract.md`
- producing a consistency report or directly editing narrow inconsistencies

Do not use this skill to decide the paper's positioning from scratch. Use `paper-positioning-planner` for that. Do not use it to write major new prose. Use `paper-writing-memory-manager` to record stale locations, dependency conflicts, and open writing threads found during consistency checks. Use `paper-writing-assistant` after consistency issues are identified. Do not simulate hostile reviewers; use `paper-reviewer-simulator` for acceptance-risk critique.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── consistency-rules.md
│   └── edit-protocol.md
└── templates/
    └── consistency-report.md
```

## Progressive Loading

- Always read `references/consistency-rules.md`.
- Read `references/edit-protocol.md` before editing paper source.
- Use `templates/consistency-report.md` for substantial reports.
- Read `paper/.agent/writing-contract.md` when present.
- Read `paper/.agent/writing-memory/`, `paper/.agent/paper-evidence-board.md`, `paper/.agent/provisional-results.md`, and root `memory/claim-board.md` / `memory/evidence-board.md` when present.
- Read figure/table maps or visual-style files when checking figures and tables.

## Core Principles

- Preserve the selected paper story. Do not silently reposition the paper.
- Distinguish inconsistency from scientific weakness. The goal is coherence, not acceptance-risk scoring.
- Prefer the current writing contract and evidence board over local inference.
- Fix low-risk naming, reference, and wording drift directly when requested.
- For claim or evidence drift, report the issue and propose the smallest safe edit.
- Do not strengthen claims to resolve inconsistencies. Weaken, narrow, or route to missing evidence instead.
- Preserve LaTeX commands, labels, citations, math, macros, comments, and formatting unless the edit directly concerns them.

## Step 1 - Locate Draft and Contract

Find:

- paper root: `paper/`, current directory, or user-provided path
- `paper/.agent/writing-contract.md` or `.agent/writing-contract.md`
- `paper/.agent/paper-evidence-board.md`
- `paper/.agent/provisional-results.md`
- source files: `main.tex`, `paper.tex`, `sections/*.tex`, appendix, figure wrappers, table files
- root memory: `memory/claim-board.md`, `memory/evidence-board.md`, `memory/action-board.md`

If no writing contract exists, still run the consistency pass from the draft, but recommend `paper-writing-contract-planner`.

## Step 2 - Choose Mode and Scope

Modes:

- `audit`: produce a report with issues and proposed fixes
- `edit`: make narrow source edits for clear inconsistencies
- `report`: save a report under `paper/.agent/draft-consistency-report.md`

Scopes:

- `full`: all checks
- `claims`: title/abstract/intro/result/conclusion claim alignment
- `terms`: names, notation, metrics, datasets, baselines
- `figures`: figures, captions, callouts, visual jobs
- `results`: tables, numbers, result prose, provisional placeholders

Default to `audit` and `full` unless the user asks for direct edits.

## Step 3 - Build the Draft Story Map

Extract a compact map:

```markdown
## Draft Story Map
- Title promise:
- Abstract claims:
- Intro thesis:
- Contribution bullets:
- Method claims:
- Experiment claims:
- Figure/table takeaways:
- Limitation scope:
- Conclusion claims:
- Active contract:
```

Mark claim IDs such as `CLM-###` when available. If IDs are missing, use local labels like `CLM-DRAFT-001`.

## Step 4 - Run Consistency Checks

Read `references/consistency-rules.md`.

Check:

- Does the title promise match the abstract and intro thesis?
- Do abstract results appear in the experiments/results section?
- Do intro contribution bullets map to experiments, figures, tables, theorem, citation, or artifact evidence?
- Are claim strengths consistent across abstract, intro, results, conclusion, and limitations?
- Do method names, dataset names, baseline names, metric names, symbols, and notation stay consistent?
- Are figure/table captions aligned with main-text interpretation?
- Are result numbers and directions consistent across tables, captions, and prose?
- Are provisional placeholders still present?
- Does related work define the same novelty boundary as intro contributions?
- Do limitations narrow exactly the right claims?

Classify each issue:

- `blocking`: could make the draft misleading or unsupported
- `major`: materially confuses the paper story
- `minor`: naming, wording, or local flow inconsistency
- `style`: polish issue that does not affect meaning

## Step 5 - Propose or Apply Edits

Read `references/edit-protocol.md`.

For each issue, choose:

- `direct-edit`: safe local wording/name/reference fix
- `rewrite-request`: needs `paper-writing-assistant`
- `contract-update`: needs `paper-writing-contract-planner`
- `evidence-update`: needs `paper-evidence-board`
- `writing-memory-update`: needs `paper-writing-memory-manager` to record dependency conflicts, stale locations, or closed threads
- `experiment-action`: needs `experiment-design-planner`
- `diagnosis`: needs `result-diagnosis`
- `leave-note`: intentional inconsistency or unresolved decision

When editing:

- edit the smallest relevant TeX or Markdown file
- keep citations, labels, refs, macros, and math intact
- avoid broad paragraph rewrites unless explicitly requested
- do not replace provisional placeholders with unverified final prose

## Step 6 - Produce Report

Use `templates/consistency-report.md` for substantial audits.

If saving and no path is specified, use:

```text
paper/.agent/draft-consistency-report.md
```

Report:

- summary of draft story
- issue table sorted by severity
- direct edits made, if any
- unresolved consistency risks
- required contract/evidence/writing follow-ups
- provisional placeholders found

## Final Sanity Check

Before finalizing:

- no claim was strengthened without evidence
- source edits are narrow and traceable
- unresolved issues are routed to the right skill
- provisional placeholders are listed
- the final response distinguishes edits made from recommendations
