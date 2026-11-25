---
name: sdd-self-improvement-assistant
description: Use alongside subagent-driven-development to add evidence-based project memory, recurring-issue learning, false-positive adjudication, safer future task dispatches, and propose-only universal skill improvements during plan execution
---

# SDD Self-Improvement Assistant

Use this skill only as a companion to `subagent-driven-development`. It does not replace the main execution workflow. The main skill still controls task dispatch, implementer subagents, task reviews, fix loops, final branch review, and finishing the development branch.

This assist skill adds a durable Self-Improvement System that learns from each completed task, reviewer finding, blocker, human decision, test failure, false positive, and final review result. The goal is to make later task dispatches more accurate, reduce repeated mistakes, prevent context bloat, and preserve project-specific knowledge across compaction or future sessions.

## Core Principle

Subagent-driven-development gives each task a fresh subagent. This skill gives the controller a durable project memory.

Fresh subagent per task remains mandatory. The memory is not dumped wholesale into subagents. The controller reads it, extracts only the relevant evidence-backed notes, and passes the smallest useful context into each task brief, reviewer prompt, or fix dispatch.

## Relationship With subagent-driven-development

This skill extends these existing SDD checkpoints:

1. Before Task 1: read existing SDD progress and learning memory.
2. During pre-flight plan review: check whether the plan conflicts with known project conventions or previous human decisions.
3. Before each implementer dispatch: inject only task-relevant learnings.
4. After each implementer report: record concerns, test commands, touched areas, and useful implementation facts.
5. After each reviewer report: record repeated issues, false positives, quality patterns, and unresolved Minor findings.
6. After each fix loop: record root cause and prevention rule.
7. After final whole-branch review: summarize branch-level lessons and update future audit rules.
8. Before finishing the branch: ensure learning memory is updated, concise, and evidence-based.

This skill must never weaken SDD quality gates. It must not bypass task review, skip fix loops, silence reviewers, or pre-judge review findings.

## Compatibility Matrix

This skill is designed primarily for Claude Code environments that support `subagent-driven-development`, file handoffs, task reviewers, and progress ledgers.

Use this compatibility model:

| Environment | Support Level | Rule |
|---|---:|---|
| Claude Code with `subagent-driven-development` | Native | Use the full workflow. |
| Claude Code without the official SDD skill | Partial | Use only the memory and review-learning parts; do not pretend SDD tooling exists. |
| Codex or other coding agents | Adapter required | Treat this file as a process pattern. Translate subagent, context compaction, review package, and ledger concepts into the host tool's actual capabilities. |
| Generic chat assistant | Conceptual only | Use for planning and reporting; do not claim durable automation unless files can actually be read and written. |

Never claim cross-agent compatibility has been validated unless it has been tested in that agent environment. If a host tool cannot create fresh subagents, persist ledger files, or run task-scoped reviewers, downgrade to the closest safe manual workflow.

## Operating Modes

Choose the lightest mode that preserves safety for the plan. Record the chosen mode in the controller's opening notes or progress ledger.

### Light Mode

Use for small, low-risk tasks.

- Read existing memory only if it is directly relevant.
- Update memory only at the end of the plan or after a major blocker.
- Do not perform per-task memory maintenance unless a durable lesson is obvious.

### Standard Mode

Default for normal SDD plan execution.

- Read memory during pre-flight.
- Inject small relevant context into dispatches.
- Update memory after approved task reviews when there is durable evidence-backed learning.
- Clean memory at the end of the plan.

### Strict Mode

Use for security-sensitive changes, migrations, large refactors, production-critical work, or repeated failures.

- Use all checkpoints in this skill.
- Record blocker root causes, important review findings, false-positive adjudications, and final-review lessons.
- Require stronger evidence before trusting older memory.
- Prefer human approval before changing memory tracking policy or proposing skill upgrades.

## Self-Upgrade Boundary: Universal Skill vs Project Memory

This skill may propose improvements to its own instructions, but it must not directly self-edit by default. Self-improvement must be propose-only unless the human explicitly authorizes editing the canonical skill source file.

The skill file itself is not project memory. Do not store repository-specific facts, file paths, module names, framework quirks, product decisions, bug details, secret-handling incidents, task outcomes, or human choices from the current project inside this `SKILL.md` file.

The agent that discovers a possible upgrade must not be the only reviewer of that upgrade. A proposed skill patch needs either explicit human approval or review by a separate reviewer agent before it is applied.

Use this strict separation:

```text
SKILL.md = universal operating system for the assistant
.superpowers/sdd/*.md = project-specific learning for the current repo
```

Only propose patches against the canonical, version-controlled skill source. Never self-upgrade an installed cache copy, generated copy, or tool-specific plugin cache, because that creates drift between Claude, Codex, and other environments.

### Allowed Self-Upgrades

A self-upgrade to this skill is allowed only when the new rule is broadly applicable to future projects.

Allowed examples:

- better rules for separating project memory from skill behavior
- improved evidence standards
- better prompt handoff patterns
- better safety gates before updating memory
- clearer reviewer-context rules
- improved blocker classification
- better prevention of context bloat
- better hygiene rules for memory files
- improved criteria for deciding whether a lesson is durable
- better rules for avoiding false positives without silencing reviewers

### Forbidden Self-Upgrades

Never add any of the following to this skill file:

- names of the current repo, product, client, company, feature, branch, module, table, route, class, component, endpoint, or file
- instructions that only make sense for the current framework or codebase
- one-off fixes from a single task
- current project architecture notes
- current project test commands
- current project deployment assumptions
- current project human decisions
- current project reviewer findings
- current project false positives
- credentials, secrets, URLs, tokens, private paths, or sensitive data
- rules that tell future reviewers to ignore a class of issues globally

Project-specific information must go into the project memory files, not into the skill.

## Universalization Test

Before editing this skill, run this test mentally and record the result in the proposed change summary:

1. Would this rule help on an unrelated repo with a different language or framework?
2. Can this rule be stated without mentioning the current repo, files, names, tasks, or business domain?
3. Is this a process improvement rather than a project fact?
4. Would it still be valid after the current project is deleted?
5. Does it preserve all `subagent-driven-development` quality gates?

Only update the skill if the answer is yes to all five.

If any answer is no, write the lesson to the correct project memory file instead.

## Self-Upgrade Trigger Rules

Consider updating this skill only at stable checkpoints:

- after a plan execution completes
- after the final branch review
- after repeated process friction is observed
- after the human explicitly asks to upgrade the skill
- after discovering a general safety or quality rule that prevents future mistakes

Do not update the skill during the middle of a task implementation or while a review loop is unresolved.

## Self-Improvement Proposal Procedure

When a possible universal improvement is found, create a proposal first. Do not apply it automatically.

1. Classify the lesson:
   - Universal Skill Improvement
   - Project Memory
   - Human Decision
   - Review Pattern
   - False Positive
   - Temporary Observation

2. If it is not a Universal Skill Improvement, do not edit or propose changes to this skill. Store it in the correct memory file or discard it.

3. If it is a Universal Skill Improvement, produce a proposed patch against the canonical `SKILL.md`, not against an installed/cache copy.

4. The proposal must include:
   - problem statement
   - why this is universal rather than project-specific
   - Universalization Test answers
   - risk of the change
   - rollback note
   - minimal diff or exact replacement text

5. Do not apply the patch unless the human explicitly says to apply it, or a separate reviewer agent approves it and the current workflow allows reviewer-approved skill edits.

6. Keep the patch small and principle-based.

7. Add a changelog entry under `Skill Changelog` only after the patch is approved and applied.

8. Ensure the update does not weaken any SDD requirements:
   - fresh subagent per task
   - task-scoped review
   - fix loop for Critical/Important findings
   - final whole-branch review
   - progress ledger
   - file handoffs instead of pasted bulk context

9. Run a self-review of the proposed skill patch using this checklist:

```text
[ ] This is a proposal or explicitly approved edit, not an unapproved self-edit.
[ ] The patch targets the canonical skill source, not a cache/installed copy.
[ ] No current repo names or paths were added.
[ ] No current project-specific rule was added.
[ ] No secrets or private data were added.
[ ] The rule is useful across multiple repositories.
[ ] The rule does not silence reviewers.
[ ] The rule does not bypass SDD quality gates.
[ ] The rule keeps project memory separate from skill behavior.
[ ] The changelog entry is concise and generic, if the patch is applied.
```

10. If the proposal fails any checklist item, do not apply it. Store the lesson in project memory instead, or discard it if it is not durable.


## Cross-Agent Distribution Check

If this skill is installed in more than one agent environment, an approved skill change is not complete until the canonical skill source and all intended installed copies are synchronized.

After an approved skill patch is applied:

1. Identify the canonical `SKILL.md` source that should be treated as the source of truth.
2. Copy or package the approved version into each intended agent environment only when that environment should receive the change.
3. Run a `diff` or equivalent comparison to confirm the copies are identical where identical behavior is expected.
4. If environments intentionally differ, document the difference as an adapter note, not as an accidental fork.

Never treat an edit to a tool cache, generated copy, or one agent's local installation as a universal upgrade. That creates cross-agent drift.

## Upgrade Decision Matrix

Use this matrix when deciding where a lesson belongs:

| Lesson Type | Destination |
|---|---|
| General rule for better subagent dispatch | `SKILL.md` |
| General rule for better evidence, safety, or review quality | `SKILL.md` |
| General rule for memory hygiene | `SKILL.md` |
| Current repo framework convention | `.superpowers/sdd/project-memory.md` |
| Current repo test/build command | `.superpowers/sdd/project-memory.md` |
| Human decision about current plan | `.superpowers/sdd/decision-log.md` |
| Repeated reviewer issue in current repo | `.superpowers/sdd/review-patterns.md` |
| Proven false positive in current repo | `.superpowers/sdd/false-positives.md` |
| Temporary task note | Do not persist unless it affects future work |

## Skill Changelog

Add only generic self-upgrade entries here.

### 2026-07-02

- Added explicit separation between universal skill upgrades and project-specific memory.
- Added universalization test before modifying the skill itself.
- Added self-upgrade procedure, safety checklist, and destination matrix to prevent repo-specific contamination.
- Revised self-upgrade into propose-only self-improvement to avoid self-approved instruction changes.
- Added compatibility matrix, operating modes, memory durability rules, and stronger evidence priority rules.
- Added cross-agent distribution check to prevent Claude/Codex skill drift after approved updates.
- Added repeated false-positive escalation rule to avoid endless reviewer/adjudication loops.

## Durable Memory Files

Create and maintain these files inside the repository:

```text
.superpowers/sdd/progress.md
.superpowers/sdd/project-memory.md
.superpowers/sdd/decision-log.md
.superpowers/sdd/review-patterns.md
.superpowers/sdd/false-positives.md
```

If the project already has a different SDD scratch directory, use the same directory as the main SDD ledger.

### Memory Durability and Git Safety

These memory files may be local scratch files. If they are ignored by Git, commands such as `git clean -fdx` can delete them. Treat this as a known risk.

At skill start, classify memory durability:

```text
[ ] Tracked memory: files are committed or intended to be committed.
[ ] Local memory: files are ignored/local-only and may be deleted by clean commands.
[ ] Unknown: tracking policy is unclear.
```

If tracking policy is unknown, default to local-memory caution and warn before destructive clean commands.

Before running or recommending destructive cleanup commands such as `git clean -fdx`, export or summarize important memory to a safe location if the memory is still needed. Do not commit memory files automatically; ask first, because they may contain project-sensitive information.

Recommended policy:

- For private/client repos: keep memory local or sanitize heavily before committing.
- For long-running internal repos: tracked sanitized memory can be useful.
- For one-off tasks: local memory is usually enough.

### progress.md

Owned by the main SDD workflow. Do not replace it. Append only compact task completion entries required by subagent-driven-development.

### project-memory.md

Stores stable project knowledge that helps future tasks.

Examples:

- framework conventions
- important folders
- dynamic loading patterns
- route conventions
- test commands that worked
- build commands that worked
- generated files that should not be edited manually
- fragile modules
- integration boundaries
- naming conventions
- environment/config assumptions
- files that look unused but are required at runtime

### decision-log.md

Stores explicit human decisions and plan conflict resolutions.

Examples:

- human chose plan text over reviewer recommendation
- human approved a risky refactor
- human confirmed a dynamic file is required
- human decided a temporary compatibility layer must remain

### review-patterns.md

Stores recurring reviewer findings and prevention rules.

Examples:

- repeated missing edge-case tests
- repeated mismatch between plan wording and implementation
- recurring type-safety issue
- recurring route naming issue
- repeated untested migration behavior

### false-positives.md

Stores findings that looked like issues but were proven safe or intentional.

Examples:

- file appears unused but is loaded by framework convention
- reviewer flagged duplication but plan required exact compatibility
- asset appears unreferenced but is loaded by CMS/admin config
- route appears dead but is accessed by external webhook

### False-Positive Adjudication Rule

False-positive memory must not suppress reviewer independence. Do not tell a reviewer to ignore a category of findings globally.

Use false-positive memory only as post-review adjudication help:

1. Let the reviewer review normally.
2. If the reviewer raises a finding similar to a stored false positive, compare the new finding with the stored evidence.
3. If it matches the same condition and current code still supports the old evidence, mark it as previously adjudicated and explain why.
4. If the surrounding code, plan, runtime behavior, or risk changed, re-review it as a new finding.

A false-positive entry expires after relevant refactors, dependency upgrades, framework changes, routing/build/test rewrites, or any change that invalidates its original evidence.

## Memory Entry Format

Every memory entry must be evidence-based. Never write vague memory such as “this module is important” without explaining why.

Use this format:

```md
## YYYY-MM-DD - Short Title

- Type: Project Convention | Human Decision | Review Pattern | False Positive | Test Command | Risk Area | Cleanup Rule
- Scope: file, folder, module, feature, or task number
- Confidence: High | Medium | Low
- Evidence: commit range, task number, review package path, report path, test output, or human decision
- Rule for future agents: concise instruction that helps future tasks
- Expiry: Keep | Re-check after refactor | Re-check after date/version/task
```

## Evidence Rules

A memory entry may be created only if one of these exists:

- a completed task report
- a reviewer finding
- a fix report
- a test/build/lint result
- a final review finding
- a human decision
- a visible code/config convention verified in the repo
- a recurring pattern seen in at least two tasks

Do not create memory from guesses, vibes, or one-off speculation.

Use evidence labels when useful:

- Static Evidence: code/config inspection only.
- Test Evidence: a named test command passed or failed.
- Runtime Evidence: behavior was observed by running the app, script, or integration.
- Human-Confirmed Evidence: the human explicitly confirmed the rule or decision.

Prefer Test Evidence, Runtime Evidence, or Human-Confirmed Evidence over Static Evidence when memory affects deletion, security, migration, auth, payments, deployment, data, or production behavior.

## Pre-Flight Memory Review

Before Task 1, do this after reading the implementation plan and before dispatching the first implementer:

1. Read `.superpowers/sdd/progress.md` if it exists.
2. Read `.superpowers/sdd/project-memory.md` if it exists.
3. Read `.superpowers/sdd/decision-log.md` if it exists.
4. Read `.superpowers/sdd/review-patterns.md` if it exists.
5. Read `.superpowers/sdd/false-positives.md` if it exists.
6. Compare the plan against stored human decisions and stable project conventions.
7. If there is a real contradiction, batch it into the main SDD pre-flight question.
8. If there is no contradiction, proceed without extra narration.

Do not stop execution only because memory exists. Memory informs execution; it does not replace the plan.

## Priority Rules

When plan, memory, reviewer, and implementation disagree, apply this order:

1. Explicit human decision in the current session.
2. Current implementation plan and global constraints.
3. Passing tests, build output, or observed runtime behavior from the current repo.
4. Current code/config evidence, with confidence lowered for dynamic loading, reflection, runtime injection, environment-specific branches, service containers, plugin systems, generated code, or side effects.
5. Existing project-memory.md entries with High confidence and current evidence.
6. Existing project-memory.md entries with Medium or Low confidence.
7. Assumptions.

Do not treat AI-read static code behavior as fully verified runtime behavior. Memory is a hint and acceleration layer, not an authority.

If memory conflicts with the current plan, do not silently follow memory. Raise the conflict during pre-flight or at the moment it becomes blocking.

## Context Injection Rules

Do not paste the entire memory file into subagent prompts.

Before each task dispatch, extract at most the relevant notes:

- max 5 project-memory entries
- max 3 review-pattern entries
- max 3 false-positive entries
- any directly relevant human decision

Only include entries that directly affect the task’s files, module, interface, tests, or risks.

The dispatch should include a small block like this:

```md
Relevant Project Memory:
- [High] This app uses dynamic route registration in `...`; do not mark routes unused based only on direct imports. Evidence: Task 3 review.
- [Medium] Tests for this module require `...` before `...`. Evidence: Task 5 report.
```

Never use project memory to instruct reviewers not to flag something. If a known false positive might recur, provide it as context with evidence, not as a command to ignore.

Bad:

```md
Do not flag duplicate validation logic.
```

Good:

```md
Context: Task 4 established that duplicate validation in `legacy/*` exists for backward compatibility. If you believe the current diff worsens this, flag it with evidence.
```

## Per-Task Learning Cycle

After every task review is approved and before moving to the next task, update memory if useful.

Append only durable information. Do not record noise.

Record:

- test commands that passed and are likely useful later
- files or modules discovered to be dynamically loaded
- fragile integration boundaries
- reviewer findings that required fixes
- root cause of Critical or Important issues
- Minor findings that should be considered by final review
- false positives proven by code or tests
- human decisions

Do not record:

- generic task summaries already in progress.md
- every file touched
- temporary local errors that have no future value
- long pasted diffs
- obvious facts such as “React components are in components/” unless the repo uses a non-obvious convention

## Reviewer Finding Learning

When a task reviewer finds an issue:

1. Classify the finding:
   - Spec Gap
   - Code Quality
   - Test Gap
   - Integration Risk
   - Security Risk
   - Performance Risk
   - Maintainability Risk
   - False Positive Candidate

2. If Critical or Important:
   - dispatch a fix subagent according to the main SDD workflow
   - require covering tests in the fix report
   - after re-review passes, add a prevention rule to `review-patterns.md` if the issue may recur

3. If Minor:
   - record it in the progress ledger or `review-patterns.md` only if it could matter in final review
   - do not block the next task unless the main SDD rules say it blocks

4. If false positive:
   - verify using code, tests, plan text, or human decision
   - add a clear entry to `false-positives.md`
   - do not tell future reviewers to ignore the category globally
   - if the same false positive recurs across multiple tasks despite being documented, escalate instead of repeatedly re-documenting it. The memory entry may be stale, the reviewer context may be insufficient, or the finding may be a real risk that was misclassified.

## Blocker Learning

When an implementer returns BLOCKED or NEEDS_CONTEXT:

1. Resolve it using the main SDD status rules.
2. If the blocker was caused by missing context that will likely recur, add it to `project-memory.md`.
3. If the blocker was caused by task size, update `review-patterns.md` with a planning warning.
4. If the blocker was caused by plan ambiguity, record the final human decision in `decision-log.md`.

## Final Review Learning

After the final whole-branch review:

If the final review is clean:

- add a short branch lesson summary to `project-memory.md` only if there are durable lessons
- record final test/build command set that proved the branch
- record any modules that need extra care in future work

If the final review finds issues:

- dispatch one fix subagent with the complete findings list, as required by SDD
- after fixes and re-review, record root causes and prevention rules
- update `review-patterns.md` with any pattern that slipped through per-task review

## Memory Hygiene

At the end of each plan execution, clean memory files:

- remove duplicates
- merge repeated rules
- downgrade stale Low-confidence entries
- mark entries that must be re-checked after refactor
- keep each file readable and compact

Do not let memory become a second giant plan file.

Before trusting a memory entry that may be stale, re-check it against current code or tests. Staleness triggers include major refactors, dependency upgrades, framework upgrades, routing/build/test rewrites, migration changes, or long gaps since the memory was written.

Recommended maximums:

- `project-memory.md`: 80 durable entries
- `decision-log.md`: no hard limit, but keep entries short
- `review-patterns.md`: 50 active patterns
- `false-positives.md`: 50 active entries

If a file grows too large, archive older entries under:

```text
.superpowers/sdd/archive/
```

## Safety Rules

Never use memory to bypass current specs.

Never apply a skill self-upgrade without explicit approval or separate review. Produce a proposal first.

Never self-upgrade an installed/cache copy of the skill. Patch only the canonical source.

Never use memory to silence reviewers.

Never add memory without evidence.

Never pass whole memory files to subagents unless the task is explicitly about auditing or maintaining the memory system.

Never record secrets, tokens, private credentials, or sensitive user data in memory. If such data appears in reports, write only a sanitized description.

Never include large diffs, full logs, or private environment values in memory.

Never mark a risky convention as permanent if it is only inferred from one task.

Never update memory in a way that contradicts the current human decision.

## Controller Checklist

At skill start:

```text
[ ] Choose Light, Standard, or Strict mode.
[ ] Read SDD progress ledger.
[ ] Classify memory durability: tracked, local, or unknown.
[ ] Read project memory files if present and relevant to the chosen mode.
[ ] Identify relevant memory for current plan.
[ ] Check plan-memory contradictions during pre-flight.
```

Before each implementer dispatch:

```text
[ ] Extract only relevant memory.
[ ] Keep task brief as the single source of exact requirements.
[ ] Include only interfaces, prior decisions, and risks needed for this task.
[ ] Avoid accumulated session history.
```

After each implementer report:

```text
[ ] Check status.
[ ] Review concerns if any.
[ ] Preserve useful test command evidence.
[ ] Do not mark complete before task review passes.
```

After each task review:

```text
[ ] Fix Critical/Important findings.
[ ] Re-review fixes.
[ ] Resolve Cannot Verify items personally.
[ ] Append progress ledger entry when clean.
[ ] Add durable learning only when evidence-backed.
```

After final review:

```text
[ ] Fix final findings in one consolidated fix dispatch if needed.
[ ] Record branch-level prevention rules.
[ ] Clean memory files.
[ ] Leave concise future instructions.
```

## Suggested Prompt Add-On for Implementer Dispatch

Use this small add-on inside implementer dispatches when relevant:

```md
Relevant Self-Improvement Memory:
Read only the notes below. Do not search memory files unless asked.

- [Confidence] Rule or known project convention. Evidence: task/report/commit.
- [Confidence] Test command or fragile integration note. Evidence: task/report/commit.

Use these notes as context, but the task brief and current plan remain authoritative.
If a memory note conflicts with the task brief, stop and report NEEDS_CONTEXT.
```

## Suggested Prompt Add-On for Reviewer Dispatch

Use this small add-on inside reviewer dispatches when relevant:

```md
Relevant Project Context:
The notes below may help interpret the diff. They are not instructions to ignore issues.

- [Confidence] Known convention or prior decision. Evidence: task/report/commit.

Review normally. If the diff violates the task brief, global constraints, or code quality standards, flag it even if a memory note seems related.
```

## Suggested Memory Update Prompt

When updating memory, use this prompt to yourself:

```md
Update the SDD self-improvement memory only with durable, evidence-backed lessons from this task.
Do not summarize the whole task.
Do not paste diffs.
Do not store secrets.
Prefer concise rules that prevent future mistakes.
If there is no durable lesson, write nothing.
```

## Done Definition

This assist skill is done for a plan execution when:

- the main SDD workflow completed all tasks or stopped for a valid blocker
- progress.md accurately reflects completed tasks
- project-memory.md contains only useful durable learning
- decision-log.md records explicit human decisions
- review-patterns.md records recurring or important prevention rules
- false-positives.md records proven false positives without silencing future reviewers
- no memory file contains secrets, huge logs, or raw diffs
- any proposed skill improvement remains a proposal unless explicitly approved
- memory durability/tracking status is known or documented as unknown/local-risk
