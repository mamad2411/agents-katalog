---
name: "executing-jira-task"
description: 'Execute a single task from a Jira task plan using pre-produced planning artifacts and a structured pipeline of specialist subagents: implementation, documentation, requirements verification, code-quality review, architecture review, and security audit. The user must specify which task number to execute. Use when the user says "execute task 3", "work on task 2", "implement task 1", "start task 5 for PROJECT-1234", or "run task N". Also triggered by the orchestrating-jira-workflow skill as Phase 7 of the end-to-end pipeline (called once per task). Requires that the task plan exists at docs/<TICKET_KEY>-tasks.md AND that planning artifacts exist (execution brief, execution plan, test spec, refactoring plan) — produced by the planning-jira-task skill in Phase 5. Executes ONLY the specified task — never continues to the next one without explicit user approval.'
---

# Executing Jira Task

## Purpose

Execute exactly ONE task from the task plan using planning artifacts produced
by the `planning-jira-task` skill (Phase 5) and critiqued by the
`clarifying-assumptions` skill (Phase 6). The planning decisions have already
been made and confirmed by the user — this skill implements them.

The pipeline ensures tasks are completed with proper implementation, test
coverage, clean code practices, sound architecture, verified security, and
confirmed requirements before moving on.

## Platform Compatibility

This skill works across multiple AI coding tools. Each platform uses a
different syntax for dispatching subagents:

| Platform        | Dispatch syntax                                                     |
| --------------- | ------------------------------------------------------------------- |
| Claude Code CLI | `agent <subagent-name> "<prompt>"` — native subagent via Agent tool |
| Cursor IDE      | Place `.md` files in `.cursor/agents/` or `@`-mention the subagent  |
| OpenCode CLI    | Subagents invoked via Task tool or `@`-mention in messages          |

If your platform does not support native subagent dispatch, read the subagent
file and execute its instructions directly, keeping the subagent's output
contract intact so downstream steps can consume it.

## Inputs

| Input         | Source              | Required | Example    |
| ------------- | ------------------- | -------- | ---------- |
| `TICKET_KEY`  | User / `$ARGUMENTS` | Yes      | `JNS-6065` |
| `TASK_NUMBER` | User / `$ARGUMENTS` | Yes      | `3`        |

Both the ticket snapshot (`docs/<TICKET_KEY>.md`) and the task plan
(`docs/<TICKET_KEY>-tasks.md`) must exist.

### Required planning artifacts (produced by planning-jira-task, Phase 5)

These files must exist before this skill runs. If any are missing, tell the
user to run the `planning-jira-task` skill first.

| Artifact                                  | Produced by         | Required |
| ----------------------------------------- | ------------------- | -------- |
| `docs/<KEY>-task-<N>-brief.md`            | execution-prepper   | Yes      |
| `docs/<KEY>-task-<N>-execution-plan.md`   | execution-planner   | Yes      |
| `docs/<KEY>-task-<N>-test-spec.md`        | test-strategist     | Yes      |
| `docs/<KEY>-task-<N>-refactoring-plan.md` | refactoring-advisor | Yes      |

Additionally, the per-task decisions file may exist if Phase 6 critique
resolved any concerns:

| Artifact                           | Produced by            | Required |
| ---------------------------------- | ---------------------- | -------- |
| `docs/<KEY>-task-<N>-decisions.md` | clarifying-assumptions | No       |

### Input contract (produced by upstream skills)

The task plan file `docs/<TICKET_KEY>-tasks.md` must contain:

| Required section / element                  | Produced by                | Why                                             |
| ------------------------------------------- | -------------------------- | ----------------------------------------------- |
| `## Task <N>:` with all 8 subsections       | planning-jira-tasks        | Source content for implementation               |
| `## Decisions Log`                          | clarifying-assumptions     | Resolved decisions for implementation context   |
| `## Jira Subtasks` table with keys          | creating-jira-subtasks     | Maps task number to Jira subtask key            |
| `Jira Subtask: <KEY>` in each task section  | creating-jira-subtasks     | Identifies which Jira issue to transition       |
| `**Status:**` on previously completed tasks | executing-jira-task (self) | Checks whether dependencies are marked complete |

## Subagent Registry

| Subagent                | Path                                   | Purpose                                                                                         |
| ----------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `task-executor`         | `./subagents/task-executor.md`         | Performs the actual implementation work based on the planning artifacts — cautious by design    |
| `documentation-writer`  | `./subagents/documentation-writer.md`  | Documents changes, commits implementation work, handles post-execution tracking                 |
| `requirements-verifier` | `./subagents/requirements-verifier.md` | Pre-gate coverage check — confirms all requirements are met before quality gates run            |
| `clean-code-reviewer`   | `./subagents/clean-code-reviewer.md`   | Reviews for Clean Code and SOLID principles compliance                                          |
| `architecture-reviewer` | `./subagents/architecture-reviewer.md` | Reviews for DDD and functional programming principles. Explicitly does NOT enforce OOP patterns |
| `security-auditor`      | `./subagents/security-auditor.md`      | Audits for security vulnerabilities, credential leaks, and insecure patterns                    |

Before delegating, read the subagent file to understand its contract (expected
input format, output format, and rules). The path is relative to this skill's
directory.

### Skill Dependencies

| Subagent                | Depends on                     | Level    | Install command                                                                 |
| ----------------------- | ------------------------------ | -------- | ------------------------------------------------------------------------------- |
| `task-executor`         | `/executing-plans`             | Required | `skills install obra/superpowers/executing-plans`                               |
| `documentation-writer`  | `/commit-work`                 | Required | `skills install softaworks/agent-toolkit/commit-work`                           |
| `documentation-writer`  | `/humanizer`                   | Required | `skills install blader/humanizer`                                               |
| `clean-code-reviewer`   | `/clean-code`                  | Required | `skills install sickn33/antigravity-awesome-skills/clean-code`                  |
| `architecture-reviewer` | `/architecture-patterns`       | Required | `skills install wshobson/agents/architecture-patterns`                          |
| `security-auditor`      | `/api-security-best-practices` | Required | `skills install sickn33/antigravity-awesome-skills/api-security-best-practices` |
| Quality gates (all 3)   | `context7` MCP                 | Required | Connect context7 MCP in your IDE/CLI settings                                   |

## Output

- Implemented code / configuration changes for the specified task.
- Tests covering business requirements.
- Documentation for all changes.
- Atomic commits for all implementation changes (via /commit-work skill).
- Updated task plan with execution status (on disk, NOT committed to git).
- Jira subtask transitioned (if Jira MCP available and subtask keys present).

### Artifact preservation rules

**Category A — Orchestration artifacts** (NEVER committed to git):

- `docs/<KEY>.md`, `docs/<KEY>-tasks.md`, `docs/<KEY>-progress.md`
- `docs/<KEY>-stage-*.md`
- `docs/<KEY>-task-<N>-brief.md`, `docs/<KEY>-task-<N>-execution-plan.md`
- `docs/<KEY>-task-<N>-test-spec.md`, `docs/<KEY>-task-<N>-refactoring-plan.md`
- `docs/<KEY>-task-<N>-decisions.md`

**Category B — Implementation output** (committed normally):

- Source code files
- Test files
- Updated inline docs, docstrings, comments in source files
- Config changes

The `documentation-writer` subagent updates Category A files on disk (status,
implementation summary, files changed) but MUST NOT `git add` or commit them.
Only Category B files are staged and committed.

### Output contract (consumed by orchestrator and self)

After this skill completes for a given task, the plan file must contain these
updates (on disk, not in git):

| Addition                                        | Consumed by        | Why                                            |
| ----------------------------------------------- | ------------------ | ---------------------------------------------- |
| `**Status:** ✅ Complete (<date>)` on task      | orchestrator, self | Orchestrator tracks progress; self checks deps |
| `**Implementation summary:**` on task           | orchestrator       | Progress file gets a concise summary           |
| `**Files changed:**` list on task               | orchestrator       | Progress reporting                             |
| `## Jira Subtasks` table status updated to Done | orchestrator       | Reflects current state                         |

---

## Quality Gate Architecture

Three subagents serve as mandatory quality gates. ALL THREE must return a PASS
verdict for the task execution to be considered complete. The
`requirements-verifier` runs before the gates (step 2) to confirm coverage
is complete — the gates then review code that is known to address all
requirements.

| Gate                    | Concern                                              | Runs after              |
| ----------------------- | ---------------------------------------------------- | ----------------------- |
| `clean-code-reviewer`   | Clean Code, SOLID, test quality, documentation       | `requirements-verifier` |
| `architecture-reviewer` | DDD, functional programming, bounded contexts        | `clean-code-reviewer`   |
| `security-auditor`      | Vulnerabilities, credential leaks, insecure patterns | `architecture-reviewer` |

### On quality gate failure — targeted fix cycle

If ANY gate returns a verdict other than PASS, the pipeline does NOT re-run
from the beginning. Instead, a **targeted fix cycle** is triggered:

1. The failing gate's feedback (specific issues, file paths, and recommended
   fixes) is collected.
2. The `task-executor` subagent is re-dispatched with the original planning
   artifacts PLUS the gate feedback as additional context. The executor
   addresses only the issues raised by the failing gate — it does not redo
   the entire implementation.
3. The `documentation-writer` subagent is re-dispatched to commit the fixes
   as atomic commits.
4. The failing gate is re-run to verify the fixes.

If multiple gates fail in the same run, all gate feedback is collected and
passed to the task-executor together, so all issues are addressed in one fix
cycle. After the fixes are committed, ALL previously failing gates are re-run
in their original order.

**Fix cycle limit:** Maximum 3 targeted fix cycles per task. If the quality
gates still do not pass after 3 fix cycles, escalate to the user with the
accumulated gate feedback and ask how to proceed.

The quality gates also enforce a **commit discipline rule**: if any gate
detects uncommitted changes in the working tree, it MUST stop immediately and
report this to the orchestrator. The orchestrator will then require the
`documentation-writer` subagent to commit all pending changes before the gates
can re-run. This ensures that reviewers always review committed, traceable code.

---

## Execution Steps

### 1. Dispatch: Task Executor

Read `./subagents/task-executor.md` and dispatch the task-executor subagent
with the paths to all planning artifacts:

- `docs/<KEY>-task-<N>-brief.md` (execution brief)
- `docs/<KEY>-task-<N>-execution-plan.md` (execution plan)
- `docs/<KEY>-task-<N>-test-spec.md` (test specification)
- `docs/<KEY>-task-<N>-refactoring-plan.md` (refactoring plan)
- `docs/<KEY>-task-<N>-decisions.md` (per-task decisions, if exists)

The task executor operates under a **cautious execution model**: it will STOP
and report back to the orchestrator whenever it encounters ambiguity, unclear
intent, uncertain architectural decisions, or any situation where the correct
course of action is not explicitly documented in its inputs. The orchestrator
must then resolve the ambiguity and re-dispatch the task-executor with updated
guidance.

The task executor will:

- Apply any recommended refactoring first.
- Implement the task following the execution plan and recommended skills.
- Write and run the tests from the test specification.
- STOP and escalate if anything is unclear — it does NOT guess or assume.
- Produce an execution report.

Collect its output as the `EXECUTION_REPORT`.

**If the task-executor stops due to ambiguity:**

1. Review the reported ambiguity.
2. Resolve it with the user if needed.
3. Update the execution brief with the resolution.
4. Re-dispatch the task-executor with the updated brief and the
   `PARTIAL_EXECUTION_REPORT` from the previous run.

**Note:** The task-executor does NOT write documentation — that is handled
separately by the documentation-writer subagent.

### 2. Dispatch: Documentation Writer

Read `./subagents/documentation-writer.md` and dispatch the documentation-writer
subagent with the `EXECUTION_REPORT`, `TICKET_KEY`, and `TASK_NUMBER`.

The documentation writer will:

- Review all changes made by the task-executor.
- Add or update code comments, docstrings, and inline documentation ONLY in
  files that the task-executor changed.
- Use the `/humanizer` skill to ensure all written text reads naturally.
- Use the `/commit-work` skill to commit **only Category B files**
  (implementation code, tests, documentation in source files) as atomic,
  logically scoped commits. It does NOT ask for user confirmation.
- **Update Category A files on disk** (task plan with completion status,
  implementation summary, files changed; Jira Subtasks table) but MUST NOT
  `git add` or commit them.
- **Transition the Jira subtask** to "Done" (if MCP available and subtask key
  present).
- Produce a documentation report including commits, tracking updates, and any
  issues.

**Critical:** The documentation-writer MUST NOT stage or commit any file
matching `docs/<KEY>*.md`. These are orchestration artifacts. Only source code,
test files, and config changes are committed.

Collect its output as the `DOCUMENTATION_REPORT`.

### 3. Dispatch: Requirements Verifier (pre-gate coverage check)

Read `./subagents/requirements-verifier.md` and dispatch the
requirements-verifier subagent with:

- The execution brief path
- The test spec path
- The `EXECUTION_REPORT`
- The `DOCUMENTATION_REPORT`

The requirements verifier will cross-check every Definition of Done item
against the actual changes.

**If the verdict is FAIL:** Report the gaps to the user and ask whether to
address the missing requirements before running the quality gates, or proceed
with the gates on the current implementation.

**If the verdict is PASS:** Proceed to the quality gates.

Collect its output as the `VERIFICATION_RESULT`.

### 4. Dispatch: Clean Code Reviewer (Quality Gate 1/3)

Read `./subagents/clean-code-reviewer.md` and dispatch with the execution
brief path, test spec path, refactoring plan path, `EXECUTION_REPORT`,
`DOCUMENTATION_REPORT`, and `VERIFICATION_RESULT`.

Collect the output as the `CODE_REVIEW`.

### 5. Dispatch: Architecture Reviewer (Quality Gate 2/3)

Read `./subagents/architecture-reviewer.md` and dispatch with the execution
brief path, execution plan path, `EXECUTION_REPORT`, `DOCUMENTATION_REPORT`,
`VERIFICATION_RESULT`, and `CODE_REVIEW`.

Collect the output as the `ARCHITECTURE_REVIEW`.

### 6. Dispatch: Security Auditor (Quality Gate 3/3)

Read `./subagents/security-auditor.md` and dispatch with the execution brief
path, `EXECUTION_REPORT`, `DOCUMENTATION_REPORT`, `VERIFICATION_RESULT`,
`CODE_REVIEW`, and `ARCHITECTURE_REVIEW`.

Collect the output as the `SECURITY_AUDIT`.

### 6a. Targeted fix cycle (if any gate returned NEEDS FIXES)

After all three gates have run, check whether any returned NEEDS FIXES. If
all three passed, skip to step 7.

If one or more gates returned NEEDS FIXES:

1. **Collect all feedback.** Merge the NEEDS FIXES feedback from every failing
   gate into a single consolidated fix brief.
2. **Re-dispatch the task-executor.** Pass the original planning artifacts PLUS
   the consolidated fix brief. The executor addresses only flagged issues.
3. **Re-dispatch the documentation-writer.** Commit fixes as atomic commits
   (Category B only — no Category A files committed).
4. **Re-run only previously failing gates.**
5. **Check results.** If all pass, continue to step 7. If still failing, repeat.

**Fix cycle limit:** Maximum 3 cycles. After 3, escalate to user.

### 7. Report to user

```
Task <N> complete: <Title>

Summary: <what was done in 2-3 sentences>

Pipeline results:
- Implementation: <files changed count>
- Documentation: <what was documented>
- Commits: <N atomic commits created>
- Tracking: <plan updated on disk, Jira transitioned>
- Requirements verification: <PASS/FAIL>
- Code review: <PASS/PASS WITH NOTES>
- Architecture review: <PASS/PASS WITH NOTES>
- Security audit: <PASS/PASS WITH ADVISORIES>

Commits:
- <short hash> — <commit message>
- <short hash> — <commit message>

Files changed:
- <list>

Jira subtask <KEY>: transitioned to Done.

⚠️ Remaining items (if any):
- <anything that could not be fully resolved>

Ready for the next task? Let me know which one to tackle.
```

## Safety Rules

- **One task at a time.** Never auto-continue to the next task.
- **Scope discipline.** Do not implement anything outside the task's scope.
- **Fail loudly.** Surface ambiguities to the user immediately.
- **Preserve the plan.** The task plan is the source of truth. If execution
  reveals the plan needs changes, propose the change to the user.
- **Respect the pipeline order.** Do not skip subagent steps or reorder them.
- **Limit retries.** Task-executor: max 3 retry cycles for ambiguity. Targeted
  fix cycle: max 3 iterations. Full pipeline re-runs require user approval.
- **Quality gates are non-negotiable.** All three must pass. No override.
- **Never commit orchestration artifacts.** Files matching `docs/<KEY>*.md` are
  updated on disk but never staged or committed to git.
- **Never delete artifacts.** No orchestration artifact is deleted at any point
  in the pipeline.

## Handling BLOCKED Verdicts (Missing Required Skills)

Same as the `planning-jira-task` skill — present install commands, wait for
user confirmation, re-dispatch from the beginning.
