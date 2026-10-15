---
name: skill-system-auditor
description: Audit a skill repository or installed skill collection for global consistency, lifecycle coverage, routing quality, documentation drift, memory writeback coverage, stale future-skill references, broken helper paths, and validation readiness. Use this skill whenever the user asks for a global consistency audit, skill taxonomy review, lifecycle audit, cross-skill routing audit, README or AGENTS inventory consistency check, or maintenance pass over a collection of agent skills.
argument-hint: "[repo-dir] [--mode audit|fix|report] [--scope lifecycle|docs|routing|memory|all]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Skill System Auditor

Audit a skill collection as a system rather than as isolated skill files.

Use this skill when:

- the user asks for a global consistency audit of a skill repository
- newly added skills may have made README, AGENTS, CLAUDE, lifecycle categories, or role categories stale
- cross-skill routing, pair-with guidance, or memory writeback expectations need alignment
- future-skill references, obsolete TODOs, or implemented-gap mentions need cleanup
- helper paths, templates, frontmatter, or validation scripts need a maintenance pass
- the user wants to decide what skills are missing next

Do not use this skill to design a single new skill from scratch. Use `skill-creator` for the skill design mechanics, then use this skill to check whether the resulting collection remains coherent.

Pair this skill with:

- `skill-creator` when audit findings lead to new or revised skill instructions
- `research-project-memory` when the skill collection's roadmap and decisions should persist
- `update-docs` when documentation drift is broad but not skill-specific
- `safe-git-ops` before committing or recovering from Git state issues

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── audit-rubric.md
    ├── doc-sync-map.md
    └── report-template.md
```

## Progressive Loading

- Always read `references/audit-rubric.md` and `references/doc-sync-map.md`.
- Read `references/report-template.md` before writing an audit report.
- If the repository has its own validation script or AGENTS instructions, read those before making edits.

## Core Principles

- Audit lifecycle behavior, not only file presence.
- A skill collection should have clear phase coverage, role coverage, routing, and handoff points.
- Top-level docs must match the actual inventory.
- "Future skill" references should not name skills that already exist.
- Memory writeback expectations should cover every skill that changes durable project state.
- Keep fixes surgical. Do not rewrite mature skills just to make wording uniform.
- Validate locally before commit, push, or reinstall.

## Step 1 - Recover Repository Rules

Read:

- `AGENTS.md`, `CLAUDE.md`, README, or equivalent repo guidance
- validation scripts
- skill directory layout
- recent audit reports or roadmap memory, if available

Record the expected install command, validation command, and documentation files that must stay synchronized.

## Step 2 - Inventory Skills

Build the actual inventory from `skills/*/SKILL.md`.

For each skill, capture:

- name
- description trigger
- lifecycle phase
- role category
- pair-with routing
- helper references
- memory writeback behavior
- whether it is planned, implemented, deprecated, or duplicated

Compare this with top-level tables in README, AGENTS, CLAUDE, manifests, and audit reports.

## Step 3 - Audit Lifecycle Coverage

Read `references/audit-rubric.md`.

Check:

- idea validation
- literature and positioning
- algorithm design
- project setup
- experiment design
- baseline choice
- experiment execution
- result diagnosis
- evidence capture
- writing and paper evidence
- reviewer simulation
- citation coverage and correctness
- submission
- rebuttal
- camera-ready
- artifact evaluation
- release and maintenance
- advisor or collaborator communication
- skill-system maintenance

Classify gaps as:

- `real-gap`: useful capability is missing
- `covered-by-existing`: existing skill covers it
- `not-in-scope`: outside repository purpose
- `hardening`: tests, examples, or docs needed rather than a new skill

## Step 4 - Audit Cross-Skill Routing

Check whether each skill routes to adjacent skills when its output naturally feeds another phase.

Look for missing or stale references around:

- literature -> baseline -> experiment design
- experiment result -> diagnosis -> paper evidence -> writing
- reviewer simulation -> evidence board -> experiments/writing
- rebuttal -> camera-ready -> artifact/release
- advisor feedback -> decisions/actions/memory
- audit findings -> skill creation/docs update

Do not add every possible cross-reference. Add only handoffs that change the user's next action.

## Step 5 - Audit Memory Writeback

Check that skills which create durable state update or route to memory:

- decisions
- claims
- evidence
- risks
- actions
- paper status
- code/worktree state
- reviewer and rebuttal state
- artifact and release state
- advisor feedback
- skill-system roadmap decisions

If a memory protocol exists, update it instead of duplicating memory rules across all skills.

## Step 6 - Audit Documentation and Stale References

Read `references/doc-sync-map.md`.

Search for:

- implemented skills still listed as future
- missing skills in top-level tables
- old lifecycle counts
- stale installation examples
- obsolete helper paths
- broken reference links
- duplicate table entries
- inconsistent skill names

Use repository validation scripts when available.

## Step 7 - Write the Audit Report

Read `references/report-template.md`.

If saving and no path is given, use:

```text
docs/audits/global-consistency-audit_YYYY-MM-DD.md
```

The report must include:

- scope
- inventory count
- lifecycle decision
- findings fixed
- findings left open
- real remaining gaps
- validation result
- recommended next skill or hardening step

## Step 8 - Fix, Validate, and Handoff

When the user asks to implement fixes:

1. Make the smallest edits that restore consistency.
2. Run the repo validation command.
3. Re-run targeted searches for stale skill names.
4. Summarize changed files and remaining risk.
5. Commit, push, and reinstall only if the user asks or the local workflow requires it.

## Final Sanity Check

Before finishing:

- actual skill inventory matches top-level docs
- lifecycle and role categories include all implemented skills
- cross-skill routing covers important feedback loops
- memory writeback covers state-changing skills
- future-skill references are accurate
- validation passes
- audit report separates fixed issues from remaining gaps
