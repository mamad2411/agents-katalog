---
name: tdd-worker
description: Implement a claimed task's work items with the cost-aware TDD red-green-refactor loop and focused tier validation. Invoked by implement-next-task with a reconnaissance digest, or standalone with a task-file path when the branch and classification already exist.
---

# TDD Worker

Implement the `Implementation work` of one already-claimed task through test-driven development,
then run the focused pre-review validation for the recorded tier. This skill owns only building and
focused verification. It does not select or claim tasks, create branches, review, update the README,
record completion, or open PRs.

Without explicit user approval, modify only repository-scoped files, isolated local/test databases,
and the task log directory defined below; never run destructive shell commands, access production
systems or data, read `.env` files, or delete or move anything else outside the repository root.

## Inputs

When invoked by `implement-next-task`, accept and use without asking:

- `task`: the task-file path;
- `change-class`: `plan-only`, `documentation-only`, `dependencies`, `configuration`, `code`, or `mixed`;
- `validation-tier`: `documentation`, `focused`, or `canonical`;
- `tdd-applicable`: whether `tdd` applies;
- `recon`: the reconnaissance digest from the current-reality pass;
- `TASK_LOG_DIR`: the deterministic task log directory.

When invoked standalone:

1. Resolve the task from a supplied path, or find the single `[~]` task in the master plan. With
   zero or multiple `[~]` tasks and no supplied path, stop and report the state.
2. Confirm the current branch matches the task's `**Branch**` value. If not, stop and report the
   mismatch; never create or switch branches here.
3. Re-derive `change-class`, `validation-tier`, and `tddApplicable` from the task and current diff.
   Fail closed to `mixed` and `canonical` when ambiguity could hide executable behavior.
4. Read the task file and the relevant code and test ranges before editing. Trust the code over
   stale task notes.
5. For coding work, load the project's own testing skill or conventions when one exists, found
   through the most specific `AGENTS.md`, falling back to `CLAUDE.md`. It owns the concrete answers
   this skill does not: which runner and config to use, where tests live, which seams the repository
   mocks, and which commands prove them. Follow it over nearest-neighbor code, and report a conflict
   with the task rather than silently resolving it. Never write to it.

   A repository can keep skills in **either `.claude/skills/` or `.agents/skills/`**, and the two
   trees are often not in sync — a skill present in one may be absent from the other, so the runtime
   may not offer it even though the docs name it. Check both directories before concluding a named
   testing skill does not exist:

   ```sh
   for d in .claude/skills .agents/skills; do
     find -L "$d" -maxdepth 2 -name SKILL.md -print 2>/dev/null
   done
   ```

   `-L` is required, not optional: one tree is often a set of symlinks into the other, and a plain
   `find` does not descend into a symlinked directory — it would report the skill as absent.

   When the skill exists on disk but is not invocable through the `Skill` tool, read its `SKILL.md`
   directly and follow it. Never skip documented testing conventions merely because the skill was
   not offered. When both trees hold the same skill name and their contents differ, prefer the one
   the project's `AGENTS.md`/`CLAUDE.md` points at, and report the divergence rather than silently
   picking one.
6. Recompute `TASK_LOG_DIR` with the commands below and refuse mismatched or symbolic-link paths.

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

## Efficient evidence handling

Keep the main context for decisions, behavioral TDD evidence, targeted source inspection, and final
integration proof. Delegate broad, read-only interpretation to isolated subagents when available and
require concise structured results. Do not delegate primary RED-GREEN decisions, concurrent edits,
or stateful checks that share a database, port, simulator, fixture, generated output, or external
service.

Use the smallest evidence that proves a result. Broad commands and full test
output belong in the task-scoped log directory; return the exit status, duration, concise result,
relevant failure excerpt, and log path. For
searches, list matching files and counts first, then inspect matching lines only in selected files.
Batch independent tool calls in the same turn and read exact ranges instead of whole files when
possible.

Use stable names such as `unit.log`, `typecheck.log`, or `review-security.log` and overwrite a
superseded passing log instead of accumulating timestamped copies. Enforce the 5 MiB cap while each
command runs rather than writing an unbounded file and truncating it afterward. Retain the latest
output when truncation is necessary, and keep the task directory under 50 MiB by removing
superseded passing logs first. Never write secrets, credentials, environment contents, source files,
or database exports to these logs. Preserve current failure evidence until the failure is resolved.

## Implement the task

Load `tdd` only when the validated classifier result sets `tddApplicable: true` for `code` or
`mixed` work that changes observable coding behavior, then follow its cost-aware red-green-refactor
loop. Do not invoke `tdd` for plan-only, documentation-only, dependency-only, or declarative
configuration-only tasks. Verify those changes with targeted syntax, consistency, security,
configuration, or provider checks instead. Loading `tdd` alone does not complete a coding step:
observe RED and GREEN for each coherent behavior
cycle and retain the command evidence in working context. Implement every item under
`Implementation work`, follow the architectural decisions, and stay within the selected task.
Automate any verification that can be automated. Keep coherent bulk documentation, configuration,
localization, fixture, or workflow edits in one sequential editing pass when they would otherwise
require many reads and full-file writes. Delegate that pass to one sequential subagent only when isolated editing is available. Pass
`TASK_LOG_DIR` and a unique, stable log filename for delegated work. The main workflow reviews
its diff and owns integration decisions.

### Check a new test's setup before escalating

When a new test fails somewhere other than the behavior it was written to test, first check the
fixture against the schema or contract the production code consumes. Confirm that execution
reached the intended path, then inspect the final producer of the missing output. Do this with
focused checks, not a broad investigation.

Do not infer a production defect, change adjacent code, or ask to expand task scope until those
checks rule out test setup. Report the failing assertion and the evidence that separates a fixture
error from a production error.

### When to derive and when to ask

Every fact the code leans on has a source you can name: the task's binding sections, `Decided`,
`Clarifications`, existing code, the producer's own source, a captured sample, or the human.
"Seems right" is not a source. When you cannot name one, you are holding a belief.

- The task is silent and existing code or repository convention answers it: derive, record the
  fact and its source in the result, continue. This is the normal case.
- The task is silent and the options differ in observable behavior (different output, file, exit
  code, data read, or skip): ask.
- The task contradicts itself (a sentence says X, the decision table or another sentence says Y):
  always ask. Never pick.
- You are typing a rule the task never stated — a threshold, heuristic, default, fallback, skip
  reason, required flag, or constraint — and cannot point to the task line demanding it: stop.
  Either ask for the line or delete the rule.
- You do not know the shape of something produced outside your code: you cannot ask, because you
  do not know what to ask. Go touch the real thing (see `Boundaries you did not write` below).

Asking: commit the tree at its last green state, then return to the caller with
`status: blocked-on-question` and exactly one question — the test or behavior you were writing,
the options, the observable consequence of each, and your recommendation. Standalone, ask the
human directly with the same shape, one question at a time. Two questions on a task is normal;
ten means you skipped derivation; zero on a task with an internal contradiction means you guessed.

Do not invent requirements, reinterpret the task, or expand its scope to bypass an obstacle, and
do not change architecture, dependencies, or safety assumptions without asking.

## Stay inside the task

In scope: the items under the task's `Implementation work`, whatever the acceptance criteria
require, and the code needed to make them pass.

Out of scope, and requiring the user's confirmation before you do it, even when it is trivial and
even when you are already in the file:

- fixing an unrelated defect you noticed;
- refactoring code the task does not change;
- adding an abstraction, wrapper, registry, config option, environment variable, or feature flag;
- renaming or moving anything the task does not require;
- broadening a type, signature, or public API beyond what the task needs;
- adding error handling, retries, fallbacks, caching, or graceful degradation for paths the task
  does not reach;
- upgrading or adding a dependency;
- tidying adjacent tests or fixtures;
- adding a CLI flag, an operator-tunable limit, an extra data source, or an optional mode the task
  does not name;
- inventing a detection heuristic (a regex catalog, a threshold, a shape-based guess) where the
  task states the behavior but not the rule. Ask for the rule, or return to the caller; a plausible
  heuristic that fires on real data the task never described is a defect, not initiative.

Noticing is not authorization. Record the observation, finish the task, and report it at the end so
the user decides. The tell that you have drifted: you are editing a file no acceptance criterion
names, or writing code no work item asked for.

Build against the task's binding sections only: `What to build`, `Decided`, `Non-goals`,
`Implementation work`, `Acceptance criteria`. `Context` explains the task and creates no work;
a known limit stated there is printed or documented only when a work item says so. When
`What to build` states a behavior that no work item covers, stop and return to the caller (or
report it when standalone) rather than either silently building it or silently skipping it: the
reviewer will judge the diff against that sentence.

### Boundaries you did not write

A boundary is anything whose shape you do not control: a library's return values, a database
driver, a stored record, a network API, a file format, another process's output. For each one the
diff touches, before writing the parser or comparison:

1. Find the code that already produces or consumes that shape — the library's own source in
   `node_modules`, an existing reader in the repository, its documentation — and mirror its
   handling. Name it.
2. Build the fixture from that side of the boundary: a captured sample, or an object assembled
   from the producer's code, never from your idea of the shape. A hand-written minimal object
   proves the happy path and hides every assumption about types, depth, optional fields, and
   ordering that real data breaks.
3. Run that fixture through the whole path end to end — adapter, transformation, schema — in one
   test, so a type mismatch between layers cannot hide behind unit tests that each use their own
   fixture.

When neither a sample nor the producer's code is obtainable locally, say so in the result and leave
the dependent criterion unchecked. Never substitute a hand-written object and report the path as
proven. This gate has no exceptions for "obvious" shapes: timestamps, JSON columns, and optional
fields are exactly where the obvious shape is wrong.

Write the simplest well-factored code that satisfies the acceptance criteria. Prefer the existing
structure when the change fits there cohesively; a new module for a genuinely new responsibility is
good engineering, not overengineering. Do not introduce an abstraction for a single consumer unless
it demonstrably improves testability or readability now, and never justify structure by a future the
task does not contain. Repository conventions, cohesive structure, clear naming, real error handling
for reachable failures, and tests remain mandatory: this bars unrequested machinery, not
craftsmanship.

## Verify the implementation

Run validation according to the recorded tier and store verbose output in `TASK_LOG_DIR`:

- `documentation`: `git diff --check` plus available document, link, or plan-consistency checks;
  never lint, typecheck, build, or test the application solely for this class;
- `focused`: only checks that parse, validate, audit, or exercise the affected dependency or
  configuration surface;
- `canonical`: focused tests and affected-area checks while working; the one final canonical
  validation is owned by `finish-task` after the manual review loop.

Do not run unchanged canonical full validation repeatedly. Fix current-task gaps and leave
unrelated repository improvements alone.

When the diff is stable, inspect `main...HEAD` and the working tree, then classify the actual change
again and update the validation plan. Run independent read-only
unit/component/lint/typecheck checks only when they do not share mutable state. Isolated subagents may run independent checks in parallel when available. Pass `TASK_LOG_DIR` and a distinct stable log
filename to each job so parallel commands never write the same file. Each returns command, status,
duration, failure names, a short relevant excerpt, and log path. Never parallelize database, port, simulator, fixture, or generated
output checks unless their isolation is proved. Wait for every validation job to finish and resolve
its failures before returning.

## Coverage map before commit

Before committing, walk `What to build` sentence by sentence and `Acceptance criteria` item by
item. For each, name the test or check that proves it. Three outcomes:

- proven: name the test;
- not proven and buildable: build it now, test-first;
- not proven and not buildable here (needs production data, a human, or a decision): leave the
  criterion unchecked and say why in the result.

Then walk the diff the other way: every new public function, flag, environment variable, data
source, and heuristic must trace to a work item or a `Decided` entry. Anything that does not is an
addition; remove it or list it under additions. Do not leave a module or code path with no test on
the grounds that it needs a network or a model: separate the pure construction from the call and
test the construction.

Three mechanical checks before the commit, each cheap and each a repeat review finding when skipped:

- after renaming any identifier, grep the old name across the whole repository, including tests,
  comments, and companion docs; commit only at zero hits;
- every comment that asserts an assumption or invariant ("this assumes X always holds") either has
  a test for the case where it does not hold, or the code is anchored so the assumption is no
  longer needed. An asserted-but-unenforced invariant is a bug report waiting for a reviewer;
- when the repository keeps a changelog with a prescribed entry format, diff the new entry against
  the template in the repository's agent instructions, field by field.

Comments in the diff follow one test: a comment earns its place only when it says what the code
cannot — why this choice over the obvious alternative, an invariant the code depends on, or an
external constraint such as an API quirk or a production incident. Never narrate what the next
lines do; if the code needs narration, rename or split it. One home per fact: when the docstring
explains it, no inline repeat, and the other way round. Inline comments are one line, two at most;
anything longer belongs in the docstring or the companion doc. Before committing, reread every
comment in the diff and delete each one that fails this test.

## Commit and return result

Commit the completed work on the task branch before returning. Partial work may be committed as
far as it is green; never return with a silently dirty tree. If work is incomplete, say so in the
result and leave the tree committed at the last green state.

Intermediate commits skip the repository's commit hooks: prefix each `git commit` with `HUSKY=0`
(or the repository's documented equivalent). The hook's full typecheck, lint, and generated-artifact
refresh run once in `finish-task` on the final commit; on a branch that is squashed at the end,
running them per commit costs minutes and proves nothing extra. The focused validation recorded in
`TASK_LOG_DIR` is the evidence for these commits. Never pass `--no-verify` and never edit or disable
the hook itself.

Return a concise structured result:

- task path, branch, and head SHA;
- work items implemented and any left incomplete, with reasons;
- the coverage map: each `What to build` behavior and acceptance criterion with its proving test,
  or the reason it is unproven;
- RED/GREEN cycles observed, with command evidence summaries;
- classification of the actual diff and any change from the expected class;
- validation commands run, status, duration, and log paths;
- decisions made or obstacles deferred to the caller;
- derived facts: each fact the task did not state that the code leans on, with its source
  (task line, `Decided`, `Clarifications`, file, library, sample), or `None`;
- boundaries: each external shape touched, the producer code or sample it was mirrored from, and
  the end-to-end test that runs it, or the reason it could not be obtained. Mandatory whenever the
  diff parses or compares anything it did not produce; `None` only when it touches no boundary;
- questions asked and their answers, or `None`;
- additions not named in the task (flags, environment variables, heuristics, data sources,
  fallbacks), or `None`. Anything here without a matching question is a defect;
- out-of-scope work observed and deliberately not done, or `None`;
- whether the diff is stable and ready for manual `task-review`.

Do not report success while any work item is unimplemented or any focused validation job is
failing. A result missing the `derived facts`, `boundaries`, or `questions` field is incomplete
and will be sent back.
