---
name: autonomous-setup
description: Use when an approved product brief (project/BRIEF.md, status APPROVED) exists and the project should be set up without further user input — research, tech decisions, scaffold, backlog. Do not use while the brief is missing or DRAFT (→ project-onboarding).
model: opus
disallowed-tools: AskUserQuestion
---

# Autonomous Setup

## Principle
From here on, **no questions to the user**. Every open decision is made autonomously and logged in
`project/DECISIONS.md` as an ADR. Only exceptions: the escalation criteria from the
autonomy contract in `project/BRIEF.md`.

**No `AskUserQuestion` tool** (enforced): a reversible open decision → decide and log an ADR; an escalation criterion hit → stop with a decision memo. Never an interactive prompt.

## Precondition
`project/BRIEF.md` exists with status APPROVED. Otherwise abort and request `project-onboarding`.

## Phases

### 1. Research (timeboxed, parallel)
First read the global knowledge base (resolve: `$SKILLS_KNOWLEDGE_DIR` if set, otherwise the path
in `<skills-dir>/_shared/knowledge.path` — written by install.sh; if neither resolves → skip) —
documented learnings from earlier projects replace research and prevent repeat mistakes.

Then parallel read-only subagents in one invocation block, one per question:
- **Alternatives:** What already exists? What does it not do well enough? (confirms/sharpens the core contract)
- **Tech options:** 2–3 stack candidates fitting the must-have outcomes, target environment, and cost frame — with trade-offs, not with a winner
- **Risks:** legal, technical, and cost traps of the domain

Results go to `project/log/<date>-research-<topic>.md`. Research findings that suggest new features
go into `project/IDEAS.md` — **never** directly into scope.

### 2. Decide
Determine stack, architecture cut, and project structure: one ADR each in `project/DECISIONS.md`
(decision, alternatives, rationale, reversal cost). On a tie, the decider is: least
complexity for the must-have outcomes — not the most interesting technology.

### 3. Scaffold
- Initialize the repo (if not present), skeleton per the ADRs, `.gitignore`, minimal README.
- Create `project/PROFILE.md` from `_shared/templates/PROFILE.template.md`.
  **Enter each command (build, test, lint, run) only after it ran successfully once.**
- A walking skeleton is enough: buildable, testable, startable. No feature implementation during setup.

### 4. Backlog
- At least one WORK card per must-have outcome from the brief (`project/backlog/`, follow the template): P0 = critical path to MVP.
- Cut cards small and with disjoint claim zones where possible — that enables the loop to parallelize.
- Initialize `project/STATE.md` and `project/IDEAS.md` from the templates.

### 5. Finish
First commit (scaffold + project/ artifacts). Short setup report in `project/log/`.
Then start `autonomous-loop` directly — don't wait for confirmation.

## Red flags
- "I'll quickly ask the user which language they prefer" → violation: decide, log, continue.
- Research takes longer than the scaffold → timebox violated; decide with available knowledge.
- Commands in the profile that never ran → the profile lies, the loop breaks later.
- Setup already implements features → belongs in WORK cards and the loop.
