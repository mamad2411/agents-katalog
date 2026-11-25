---
name: implement-next-task
description: Select, claim, and set up the next eligible local task, then implement it through tdd-worker with TDD and focused validation while minimizing parent-context growth and avoidable wall time. Stops before review; the user then runs task-review, review-fix-worker, and finish-task manually.
---

# Implement Next Task

Select and implement one eligible task in full on its feature branch, then stop and hand off to the
manual review loop. Use one implementation workflow at a time in the current checkout. The master
plan controls order and status; the selected task file is the contract for what to build.

This skill covers selection, setup, and implementation. It does not review, update the README,
record final completion, or open a PR. When it ends, tell the user to run:

1. `/skill:task-review` — writes a findings file under `reviews/`;
2. `/skill:review-fix-worker` — fixes the findings one by one;
3. repeat 1–2 until the review is clean or only accepted/skipped findings remain;
4. `/skill:finish-task` — README, final proof, completion record, and PR.

Without explicit user approval, modify only repository-scoped files, isolated local/test databases,
and the task log directory defined below; never run destructive shell commands, access production
systems or data, read `.env` files, or delete or move anything else outside the repository root.

## Efficient evidence handling

Keep the main context for decisions, behavioral TDD evidence, targeted source inspection, and final
integration proof. Delegate broad, read-only interpretation to isolated subagents when available and
require concise structured results. Do not delegate primary RED-GREEN decisions, concurrent edits,
or stateful checks that share a database, port, simulator, fixture, generated output, or external
service.

Use the smallest evidence that proves a result. After branch checkout, broad commands and full test
output belong in the task-scoped log directory; return the exit status, duration, concise result,
relevant failure excerpt, and log path. Never create another workflow log location. Before checkout,
reconnaissance returns bounded results directly and does not retain full command output. For
searches, list matching files and counts first, then inspect matching lines only in selected files.
Batch independent tool calls in the same turn and read exact ranges instead of whole files when
possible.

Use stable names such as `unit.log`, `typecheck.log`, or `review-security.log` and overwrite a
superseded passing log instead of accumulating timestamped copies. Enforce the 5 MiB cap while each
command runs rather than writing an unbounded file and truncating it afterward. Retain the latest
output when truncation is necessary, and keep the task directory under 50 MiB by removing
superseded passing logs first. Never write secrets, credentials, environment contents, source files,
or database exports to these logs. Preserve current failure evidence until the failure is resolved.

## Local task model

Find the master plan through the most specific `AGENTS.md` `Active plan` entry, falling back to
`CLAUDE.md`. Task files live under `plans/tasks/`.

- `[ ]` means ready and unclaimed.
- `[~]` means in progress.
- `[>]` means complete with a CI-green PR open and awaiting merge.
- `[x]` means merged into the base branch; the task then moves to `plans/tasks/done/`.

A task is eligible only when its pointer is `[ ]` and every ordinal in its `(after ...)` suffix is
`[x]`. A dependency at `[ ]`, `[~]`, or `[>]` blocks it because the required code is not on the base
branch.

Accept an optional task ordinal or task-file path. If supplied, use that task only when it is
eligible. Otherwise choose the first eligible pointer. If none is eligible, report the blocking
tasks. When a `[>]` task appears to be the blocker, tell the user to verify whether its PR merged
and to complete the local lifecycle updates before continuing.

Accept an optional `--base <branch>` flag naming the integration branch that task branches start
from and merge back into. Resolution order: the flag; otherwise a `**Base branch**:` line in the
master plan's `Architectural decisions`; otherwise `main`. Everywhere below, "the base branch" means
this resolved value, and every `[x]` / eligibility / update rule reads against it instead of `main`.
When the base is not `main`, it must already exist locally or on the remote; if it does not, stop
and tell the user to create it (for example `git branch feature/memory main` plus a worktree for
it) rather than creating it silently. Update the base from its remote tracking branch when one
exists, otherwise use the local base as-is and say so.

Accept an optional `--worktree` flag. Without it, implement in the current checkout as before. With
it, implement in a dedicated git worktree created in step 4. Passing the flag authorizes creating
that one worktree directory outside the repository root, which the scope constraint above otherwise
forbids; it authorizes nothing else outside the repository.

## Workflow

### Mandatory execution checklist

Create this checklist in working context when the skill starts and keep it current. Check an item
only after completing the corresponding workflow section with evidence. If work stops, report the
first unchecked item and its blocker. Do not copy this process checklist into committed files;
record durable decisions and proof in the task file.

- [ ] Task selected, claimed, and read in full
- [ ] Current code and test reality inspected
- [ ] Outcome, branch, verification method, and task log directory confirmed
- [ ] Decisions and unexpected obstacles resolved through `talk-it-through`, or not applicable
- [ ] `tdd-worker` completed for coding behavior, or correctly skipped for non-coding work
- [ ] Implementation work completed within scope, with any discovered out-of-task work left undone
      and recorded
- [ ] Focused pre-review validation passed
- [ ] Manual review-loop handoff (task-review → review-fix-worker → finish-task) reported to the user

### 1. Select and claim the task

Read the master plan, choose the task, and immediately change its pointer from `[ ]` to `[~]`.
Read the architectural decisions and the selected task file in full. Read referenced decision
documents only when the task depends on them. Do not load the source PRD or neighboring tasks to
expand the task's scope.

Before broad repository exploration, inspect the selected task and base branch, then classify the
expected work as one of:

- `plan-only`: task and plan lifecycle content only;
- `documentation-only`: human-facing prose, diagrams, or examples with no executable surface;
- `dependencies`: manifests, lockfiles, patches, or dependency policy only;
- `configuration`: declarative tooling, workflow, or environment configuration without production code;
- `code`: production or test code;
- `mixed`: more than one material class.

Derive `validationTier` and `tddApplicable`, then check that both are consistent with the class.
Fail closed to `mixed` and `canonical` when ambiguity could hide executable behavior. Record the
result immediately. Classification never weakens security review or an explicit task acceptance
criterion.

If the task cannot be claimed or the current checkout already has another active implementation
workflow, stop and report the state.

### 2. Verify current reality

Inspect the code and tests before planning edits. Perform one broad reconnaissance pass, using an isolated read-only
subagent when available. Return a concise digest rather than raw command output,
containing:

- differences between the task's assumptions and the current code;
- relevant files and code ranges;
- existing test seams and conventions;
- the minimum excerpts needed for the first failing test and implementation.

Trust the code over stale task notes. Read directly only the exact source and test ranges needed for
editing or verification. Keep exact, bounded searches in the main context; delegate broad searches
requiring interpretation, such as migration, dead-code, caller, test-surface, or documentation
audits, when isolated subagents are available. Require every delegated audit to return `Status`,
`Actionable findings`, and `Expected or ignored matches`, with paths and line numbers only.

Check the task's shape while reading it. Only the sections `What to build`, `Decided`,
`Clarifications`, `Non-goals`, `Implementation work`, `Human checkpoints`, and `Acceptance criteria`
bind; `Context` is
background and creates no work. Stop and report instead of implementing when:

- `What to build` states a behavior that no `Implementation work` item and no acceptance
  criterion covers. The reviewer holds the diff to the prose while the worker builds the items,
  so this gap is a guaranteed finding;
- an output is a verdict, status, or classification and the task gives no decision table;
- an acceptance criterion needs production data, production credentials, or a command that does
  not pass on the base branch today;
- the binding sections clearly exceed one fresh implementation context (roughly 600 words or more
  than one primary output).

Report the gap with a proposed split or the missing sentence, and let the user amend the task
through `to-plan` or `talk-it-through`. Do not fill the gap yourself.

### 3. Confirm the selected task

State the task ordinal, title, independently verifiable outcome, branch, and verification method.

### 4. Create or check out the branch

Use the task's `**Branch**` value. Never implement on `main` or on the base branch itself.

**Without `--worktree` (default):** check out an existing local or remote branch when it matches the
task. Otherwise update the base branch and create the branch from it, in the current checkout.

**With `--worktree`:** leave the current checkout on its branch untouched and implement in a
dedicated worktree instead.

1. Refuse the flag when the session is already inside a worktree, or when the task's branch is
   already checked out in any worktree (`git worktree list`). Report the conflict instead.
2. Update the base branch first, so the new branch starts from its current tip. When the base is
   checked out in another worktree, fetch and read it there; never check it out twice.
3. Place the worktree in a `worktrees/` directory beside the repository, never inside it:
   `<parent of repository root>/worktrees/<branch-slug>`. A worktree nested in the repository ends
   up inside build contexts, editor indexes, and `git clean -xff` blast radius.
4. Create it with `git worktree add -b <branch> <path> <base>` for a new branch, or
   `git worktree add <path> <branch>` for one that already exists.
5. Enter it with `EnterWorktree` using `path`, so the session's working directory follows. Never
   `cd` into it: the session must actually move for later steps to operate on the right tree.
6. A fresh worktree contains tracked files only, so it has no installed dependencies. Install them
   only when the validation tier requires running tests, and say so before doing it.
7. Gitignored per-checkout files do not exist in a fresh worktree either — local env and secrets,
   the master plan when it is ignored, local corpora, and local tooling. Provision them before
   running anything.

   **Prefer a repository-provided setup script.** When the main checkout has one — conventionally
   `.local/sync-worktrees.sh` — run it and report its output rather than copying by hand. It lives
   in the main checkout, which is where a fresh worktree has not yet been provisioned from, so
   resolve it there rather than relative to the current directory:

   ```sh
   MAIN="$(git worktree list | head -1 | awk '{print $1}')"
   [ -x "$MAIN/.local/sync-worktrees.sh" ] && bash "$MAIN/.local/sync-worktrees.sh" "$PWD"
   ```

   The script is the project's own record of which ignored paths matter, so it stays correct as that
   list changes, and it is idempotent. Read it before the first run in an unfamiliar repository: it
   must only link or copy local files into the worktree, never write tracked files and never reach
   the network.

   **Otherwise copy by hand:** the originating checkout's ignored local env files (`.env.local`,
   `<package>/.env.local`, and siblings) to the same relative paths. Tracked config such as `.env`
   or `.npmrc` already travels with the worktree; do not copy it.

   Treat provisioning as required rather than optional: a missing local env file usually fails
   silently instead of loudly, and the common failure is a process falling back to a production
   service where the developer expected a local emulator. Afterwards `git status` in the worktree
   must be clean — a provisioned path that shows as untracked is not ignored, and committing it
   would leak local config or secrets.

When the master plan and task files are untracked or ignored by git, a new worktree will not contain
them; a setup script may already have provided them in step 7. Confirm `plans/` resolves in the
worktree. When it does not, symlink it to the originating checkout's `plans/` rather than copying,
so claims and `tasks/done/` moves have one home. Record the originating checkout's absolute path in
the task file. If a copy is unavoidable, pointer and status transitions (`[~]`, `[>]`, `[x]`) always
belong to the master plan in the originating checkout, never to the worktree's copy, so the
canonical plan stays single-source.

After checkout or worktree entry, create or reuse the deterministic task log directory. In a
worktree, `git rev-parse --show-toplevel` resolves to the worktree path, so its task log directory
is distinct from the originating checkout's by construction. Refuse to use any existing
symbolic link in its path:

```sh
LOG_ROOT=/tmp/agent-workflows
REPO_ROOT="$(git rev-parse --show-toplevel)"
BRANCH="$(git branch --show-current)"
REPO_KEY="$(printf '%s' "$REPO_ROOT" | git hash-object --stdin | cut -c1-12)"
BRANCH_KEY="$(printf '%s' "$BRANCH" | git hash-object --stdin | cut -c1-12)"
REPO_LOG_DIR="$LOG_ROOT/$REPO_KEY"
TASK_LOG_DIR="$REPO_LOG_DIR/$BRANCH_KEY"
for path in "$LOG_ROOT" "$REPO_LOG_DIR" "$TASK_LOG_DIR"; do
  if [ -L "$path" ]; then
    printf 'Refusing symbolic-link log path: %s\n' "$path" >&2
    exit 1
  fi
done
if [ -e "$TASK_LOG_DIR" ]; then
  [ -d "$TASK_LOG_DIR" ] && [ -f "$TASK_LOG_DIR/repo-root" ] && [ -f "$TASK_LOG_DIR/branch-name" ] &&
    [ "$(cat "$TASK_LOG_DIR/repo-root")" = "$REPO_ROOT" ] &&
    [ "$(cat "$TASK_LOG_DIR/branch-name")" = "$BRANCH" ] || {
      printf 'Refusing mismatched task log directory: %s\n' "$TASK_LOG_DIR" >&2
      exit 1
    }
else
  mkdir -p "$TASK_LOG_DIR"
  printf '%s\n' "$REPO_ROOT" > "$TASK_LOG_DIR/repo-root"
  printf '%s\n' "$BRANCH" > "$TASK_LOG_DIR/branch-name"
fi
```

Every validation command runs inside the checkout recorded in `TASK_LOG_DIR/repo-root`; the
working directory printed at the top of each log must sit under that path. A log produced from
another checkout (typically the originating checkout because the worktree had no dependencies) does
not count as validation of this branch: install dependencies in the worktree (step 6 above) and
run again.

Retain `TASK_LOG_DIR` in working context. Recompute it with the same commands when needed and pass
it explicitly to every subagent or child skill that may produce verbose output. Reuse an existing
directory only when both metadata files exactly match the current repository root and branch;
otherwise stop rather than writing into it. Keep the directory through implementation, the manual
review loop, PR creation, and CI so failures remain diagnosable. Remove it only after the task's PR
has merged and the local base branch is synchronized.

### 5. Resolve uncertainty and human checkpoints

If the task does not provide enough information to choose a safe implementation approach, stop
before writing affected code and invoke `talk-it-through`.

If implementation encounters an unexpected obstacle that the task does not address, stop and
invoke `talk-it-through` before changing scope, behavior, architecture, dependencies, or safety
assumptions. Explain the uncertainty or obstacle, discuss one decision at a time, recommend an
approach, wait for shared understanding, and record the decision in the task file. Do not invent
requirements, reinterpret the task, or expand its scope to bypass an obstacle. Continue routine
implementation choices autonomously when the task and repository conventions provide enough
direction.

Work you discover mid-implementation is not authorized by having found it. An unrelated defect, a
refactor the task does not require, a missing abstraction, an adjacent test worth tidying: record
each one, leave it undone, and report it at handoff for the user to decide. This applies when you
are not blocked at all and the change looks small, which is when scope grows unnoticed.

Resolve declared `[decision]` items through `talk-it-through` before writing code they affect.
Require explicit approval before `[confirm-db]` work on real, shared, destructive, persistent, or
ambiguous data and before `[confirm-security]` work that changes a trust boundary. Isolated local
or test-database work may proceed within the task's scope. Keep `[verify]` items for the final proof
step in `finish-task`.

### 6. Implement through tdd-worker

Invoke `tdd-worker` with the task-file path, the recorded classification (`change-class`,
`validation-tier`, `tddApplicable`), the reconnaissance digest, and `TASK_LOG_DIR`. `tdd-worker`
loads `tdd` when applicable, runs the red-green-refactor loop for every item under the task's
`Implementation work`, and runs the focused pre-review validation for the recorded tier.

For plan-only, documentation-only, dependency-only, or declarative configuration-only tasks,
`tdd-worker` skips `tdd` and verifies changes with targeted syntax, consistency, security,
configuration, or provider checks instead.

When `tdd-worker` returns `status: blocked-on-question`, put its one question to the user with
`AskUserQuestion`: the behavior or test it was writing, the options, the observable consequence of
each, the worker's recommendation first. One question per prompt. Never answer on the user's
behalf, never merge questions, never defer one to the handoff report. Append the question and the
answer under `## Clarifications` in the task file (create the section after `Decided` if absent;
it binds like `Decided`), then re-invoke `tdd-worker` with the same inputs. Repeat until it returns
done.

When `tdd-worker` returns done, confirm its reported evidence: every work item implemented, RED and
GREEN observed for each coherent behavior cycle, and the tier validation passing. Its result must
carry the `derived facts`, `boundaries`, and `questions` fields; if any is missing, or `boundaries`
is `None` while the diff parses or compares data it did not produce, re-invoke `tdd-worker` asking
for the field rather than accepting the result. Do not re-run its passing validation.

### 7. Hand off to the manual review loop

When implementation and focused validation are complete, commit the work on the feature branch with
`HUSKY=0` (the repository hook's full typecheck, lint, and artifact refresh are not run on
intermediate commits; the branch is squashed before it lands) and stop. Report:

- the task ordinal, title, and branch;
- what was built and the proof gathered;
- deferred decisions or obstacles, if any;
- out-of-scope work discovered and deliberately not done, for the user to accept or reject;
- additions not named in the task (flags, environment variables, heuristics, extra data sources,
  fallbacks), or `None`. Anything listed here should have been confirmed before it was built;
- clarifications recorded during the run, or `None`;
- the exact next commands: `/skill:task-review`, then `/skill:review-fix-worker`, repeating until
  clean, then `/skill:finish-task`.

Do not invoke `task-review`, update the README, run final proof, record completion, or open a PR in
this skill. Those belong to the manual review loop and `finish-task`.

## Rules

- Implement one task per invocation.
- Do not run multiple implementation workflows in the same checkout. Concurrent tasks are allowed
  only when each runs in its own worktree via `--worktree`.
- Never work on `main`.
- Do not start a dependency-blocked task.
- Stay within the selected task's independently verifiable behavior.
- Keep the mandatory execution checklist current and report the first unchecked item when blocked.
- Use `talk-it-through` for unresolved approach decisions and unexpected out-of-task obstacles.
- Stop for declared decisions, unresolved implementation uncertainty, unexpected out-of-task
  obstacles, destructive database actions, and security boundaries.
- End after implementation and focused validation; review, README, final proof, completion
  recording, and PR creation happen in `task-review`, `review-fix-worker`, and `finish-task`.
- Keep `[>]` distinct from `[x]`; a merged task is closed manually after the merge.
