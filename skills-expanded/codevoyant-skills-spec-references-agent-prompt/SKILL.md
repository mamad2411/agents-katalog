# Phase Agent Prompt

Use this prompt when launching each per-phase Task in the orchestration loop (Step O3). The `spec-executor` agent handles the persona and rules — this prompt provides only the execution context.

```
You are executing Phase {N} — {phase-name} of the spec plan "{plan-name}".

## Execution Context

Working directory: {EXECUTION_DIR}
Branch: {PLAN_BRANCH}
Worktree: {PLAN_WORKTREE or "(none)"}
Git commits allowed: {ALLOW_COMMITS}

Project checks:
Discover and run every build/test/lint/format command via the task skill (`/task detect`, then `/task list`) — the phase file carries no runner commands. Never call build/test tools directly and never invent shell equivalents.

## Completed phases (summary only)
{One line per completed phase: "Phase 1 (Setup) ✅ — 4/4 tasks, tests passing"}

## Annotations to apply first

Before starting any task, scan plan.md and implementation/phase-{N}.md for inline HTML-comment annotations (scan `<!-- >>` before `<!-- >`). The named forms map to these — see `skills/shared/annotations.md`:

- **`<!-- > instruction -->`** — minor annotation, standalone comment applying to the block below it (the named alias is `<!-- @edit: … -->`)
- **`content <!-- >> instruction -->`** — major annotation, inline suffix applying to that specific line (no `@`-named alias)
- **`<!-- @agent: … -->`** — guidance only, no mechanical effect; it is never a line-level edit

Apply each annotation (mark done, remove task, rewrite content, etc.) and delete the entire `<!-- ... -->` comment from the file. Log what you applied. If none found, continue silently.

## Your tasks — Phase {N}

{Paste Phase {N} task list from plan.md verbatim}

## Implementation spec — Phase {N}

{Full content of .codevoyant/spec/{plan-name}/implementation/phase-{N}.md}

## File paths

- Plan: .codevoyant/spec/{plan-name}/plan.md
- Execution log: .codevoyant/spec/{plan-name}/execution-log.md
- Registry: .codevoyant/README.md

## Execution log — required after every task

After completing each task, append to execution-log.md **before** moving to the next task:

```
[{ISO-8601 timestamp}] Phase {N} Task {T} — {task description}: DONE
  Changed: {comma-separated list of files modified}
  Validation: fmt ✓  lint ✓  typecheck ✓  tests ✓
```

If a task fails, write:
```
[{ISO-8601 timestamp}] Phase {N} Task {T} — {task description}: FAILED
  Reason: {one-line description}
  Action: {what you did to recover, or STOPPED}
```

At phase end, append:
```
[{ISO-8601 timestamp}] Phase {N} — {phase-name}: COMPLETE ({T}/{T} tasks)
```

## Git commit policy

{if ALLOW_COMMITS=false}
Do NOT run git commit, git add, or git push — and do NOT invoke the git skill's commit workflow. Make no commits of any kind.
{endif}
{if ALLOW_COMMITS=true}
Commit the completed phase through the git skill (`/git commit`). Never run raw `git commit`, `git add`, or `git push` yourself — the git skill owns staging, conventional commit messaging, the no-agent-self-attribution rule, and (when CI exists) the CI-green loop. Always pass `--yes` (you are an autonomous subagent and cannot prompt for confirmation).

Choose the invocation by environment:
- **No remote/upstream configured** → `/git commit --yes --no-push`. Commit locally only; no push, no CI check.
- **Remote configured, but no CI** (no `.github/workflows/` for GitHub, no `.gitlab-ci.yml` for GitLab) or **no matching CI CLI installed** (`gh` for GitHub, `glab` for GitLab) → `/git commit --yes`. The git skill pushes and reports "no CI to watch"; skip the CI check silently.
- **Remote configured, CI exists, and the matching CI CLI is installed** → `/git commit --yes --fix`. The git skill pushes, then blocks in its bounded fix-until-green loop (max 3 fix attempts).

**CI-green is a HARD per-phase gate** (only when CI exists): the phase is not complete while CI is red. If the git skill stops with CI still failing (its fix attempts exhausted), do NOT mark the phase complete and do NOT continue to the next task — stop, append a FAILED entry to execution-log.md, and report the phase as FAILED (not `ESCALATE`; escalation is for code-strength walls, not a red CI). A phase never fails for the absence of CI — it only fails when CI exists and stays red after the git skill's bounded attempts.
{endif}

Execute Phase {N} now. Report a summary when done.
```
