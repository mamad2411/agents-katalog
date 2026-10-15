---
name: research-project-memory
description: Initialize, inspect, and maintain a hierarchical memory system for an ML research project across paper, code, worktrees, slides, reviewer simulation, rebuttal, experiments, claims, evidence, risks, and actions. Use this skill whenever the user wants cross-session project memory, project bootstrapping context, feedback-loop tracking, claim-evidence-risk-action alignment, worktree memory, or consistency between code results, paper writing, slides, reviews, and rebuttal.
argument-hint: "[project-root] [--bootstrap] [--closeout] [--check]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Research Project Memory

Maintain project memory as a layered system, not a flat notes file. This skill gives agents a shared protocol for remembering what a research project is trying to prove, what evidence exists, what risks remain, and which component owns each next action.

Use this skill when:

- a project needs cross-session memory beyond remote execution state
- the user wants memory across `paper/`, `code/`, worktrees, `slides/`, reviewer simulation, or rebuttal
- claims, experiments, figures, paper sections, reviewer risks, and actions need to stay aligned
- a session materially changes project direction, evidence, writing, review risks, or planned experiments
- a new agent session needs bootstrap context before acting
- the user asks for a memory system, project state graph, claim/evidence board, worktree memory, or closeout protocol

This is a coordination skill. It does not replace `remote-project-control`, `experiment-design-planner`, `conference-writing-adapter`, `paper-reviewer-simulator`, or `rebuttal-strategist`; it tells them where and how to persist trusted project state.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── closeout-protocol.md
│   ├── consistency-checks.md
│   ├── memory-architecture.md
│   ├── object-schemas.md
│   └── writeback-protocol.md
└── templates/
    ├── component/
    │   ├── component-status.md
    │   └── worktree-status.md
    └── memory/
        ├── action-board.md
        ├── claim-board.md
        ├── component-index.yaml
        ├── current-status.md
        ├── decision-log.md
        ├── evidence-board.md
        ├── project.yaml
        └── risk-board.md
```

## Progressive Loading

- Always read `references/memory-architecture.md`, `references/object-schemas.md`, and `references/writeback-protocol.md`.
- Read `references/consistency-checks.md` when asked to audit project state, prepare a milestone, submit, write, review, or rebut.
- Read `references/closeout-protocol.md` before ending a substantial session or updating memory after meaningful work.
- Use `templates/` as the source of truth when bootstrapping missing memory files.

## Core Principles

- Memory is coordination context, not execution truth.
- Stable claims, decisions, risks, and component mappings belong in repo memory.
- Volatile facts such as dirty git state, queue state, active jobs, and file existence must be re-verified.
- Every important claim should link to evidence, a paper location, and current risks.
- Every reviewer or rebuttal risk should link to an action, a decision to accept the risk, or a reason it is out of scope.
- Every worktree should have a purpose and an exit condition: merge, continue, park, or kill.
- Mark certainty: `observed`, `user-stated`, `inferred`, `stale`, or `needs-verification`.
- Write memory at the most specific layer that will help the next session.

## Step 1 - Locate the Project and Existing Memory

Detect the project root:

```bash
git rev-parse --show-toplevel 2>/dev/null || pwd
```

Then inspect likely memory files:

- `memory/project.yaml`
- `memory/component-index.yaml`
- `memory/current-status.md`
- `memory/decision-log.md`
- `memory/claim-board.md`
- `memory/evidence-board.md`
- `memory/risk-board.md`
- `memory/action-board.md`
- `paper/.agent/`
- `code/.agent/`
- `slides/.agent/`
- `reviewer/.agent/`
- `rebuttal/.agent/`

If the project uses another layout, adapt the component paths but keep the same memory roles.

## Step 2 - Bootstrap Missing Memory

If the user asks to initialize memory, or if memory is missing and the task depends on it, create the minimum useful files from templates:

- `templates/memory/project.yaml` -> `memory/project.yaml`
- `templates/memory/component-index.yaml` -> `memory/component-index.yaml`
- `templates/memory/current-status.md` -> `memory/current-status.md`
- `templates/memory/decision-log.md` -> `memory/decision-log.md`
- `templates/memory/claim-board.md` -> `memory/claim-board.md`
- `templates/memory/evidence-board.md` -> `memory/evidence-board.md`
- `templates/memory/risk-board.md` -> `memory/risk-board.md`
- `templates/memory/action-board.md` -> `memory/action-board.md`
- `templates/component/component-status.md` -> `<component>/.agent/<component>-status.md`
- `templates/component/worktree-status.md` -> `<code-worktree>/.agent/worktree-status.md` when a worktree needs its own memory

Ask only for fields that cannot be inferred safely:

- project name
- project root
- component paths
- current research question
- current target venue or milestone, if any
- whether memory files should be committed

## Step 3 - Build the Bootstrap Summary

Before substantial work, summarize:

- project name and root
- current research question and positioning
- target venue or milestone
- active components and paths
- current claim IDs
- current evidence IDs and latest reliable result
- top risks and blockers
- active actions and owners
- stale or missing memory
- facts that must be verified before acting

Keep the summary compact. Do not paste entire boards unless the user asks.

## Step 4 - Write to the Right Layer

Read `references/writeback-protocol.md`.

Use this routing:

- whole-project identity, target venue, component paths, memory policy -> `memory/project.yaml`
- current focus, active milestone, next session entry point -> `memory/current-status.md`
- durable project decisions and why -> `memory/decision-log.md`
- paper claims and their status -> `memory/claim-board.md`
- experiments, analyses, proofs, citations, and figures that support claims -> `memory/evidence-board.md`
- reviewer, novelty, baseline, writing, execution, and rebuttal risks -> `memory/risk-board.md`
- concrete next tasks and owners -> `memory/action-board.md`
- component-specific state -> `<component>/.agent/<component>-status.md`
- code worktree purpose and exit condition -> `<worktree>/.agent/worktree-status.md`

When in doubt, write a short pointer at the project layer and details in the component layer.

## Step 5 - Maintain the Claim-Evidence-Risk-Action Graph

Read `references/object-schemas.md`.

Use stable IDs:

- `CLM-###`: claim
- `EVD-###`: evidence item
- `EXP-###`: experiment or run family
- `FIG-###`: figure or table
- `RSK-###`: risk
- `ACT-###`: action
- `DEC-###`: decision
- `WTR-###`: worktree
- `REV-###`: review or rebuttal issue

Every major update should preserve links:

```text
CLM-001 -> supported_by EVD-003 -> visualized_by FIG-002 -> threatened_by RSK-004 -> resolved_by ACT-007
```

Avoid orphan objects. If a claim has no evidence, mark it as `planned`, `unsupported`, or `cut`.

## Step 6 - Run Consistency Checks

Read `references/consistency-checks.md` when auditing memory.

Check for:

- paper claims without evidence
- evidence without a claim or paper location
- reviewer risks without actions
- rebuttal promises without paper/code follow-up
- worktrees without exit condition
- stale results still used in writing
- slides that contradict paper status
- volatile state recorded as stable truth

Report mismatches as project risks or actions.

## Step 7 - Close Out the Session

Read `references/closeout-protocol.md`.

Before ending a substantial session, update:

- `memory/current-status.md`
- any changed claim/evidence/risk/action board
- relevant component status file
- worktree status file if code branch direction changed
- `memory/decision-log.md` if a durable decision was made

Closeout should answer: what changed, what is trustworthy, what is stale, what should the next agent verify, and what is the next concrete action.

## Final Sanity Check

Before finalizing:

- stable and volatile facts are separated
- new claims link to evidence or are marked unsupported
- new evidence links to a claim, component, and source path
- new risks link to actions or accepted-risk decisions
- worktree memory has a purpose and exit condition
- current-status gives the next session a clear starting point
- no private local path or credential is written into shared memory unless the user explicitly wants it
