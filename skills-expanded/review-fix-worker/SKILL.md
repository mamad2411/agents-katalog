---
name: review-fix-worker
description: Fix open findings from a reviews/ todo-list file one by one with TDD, checking each off in the file. Starts from a fresh context using only the self-contained review file. Handles skip decisions for minor findings and user decisions for security findings. Use manually after task-review.
---

# Review Fix Worker

Read one review file under `reviews/`, fix every `open` finding one by one, and mark each finding's
status in the file immediately after it is resolved. The review file is the complete contract: it
carries the repository root, branch, base, task path, change class, and validation tier, so this
skill works from a fresh context with no other input.

Invocation authorizes modifications to the branch named in the review file for non-security
remediation. Never expand scope beyond the frozen finding set. Never delete, stage, or commit review
files; they are ignored workflow state retained across review passes. `finish-task` removes all
review files associated with the completed task after its PR is CI-green.

## Efficient evidence handling

Keep the main context for decisions, behavioral TDD evidence, and targeted source inspection.
Delegate broad, read-only interpretation to isolated subagents when available and require concise
structured results. Do not delegate primary RED-GREEN decisions, concurrent edits, or stateful
checks that share a database, port, simulator, fixture, generated output, or external service.

Use the smallest evidence that proves a result. Broad commands and full test output belong in the
task log directory; return the exit status, duration, concise result, relevant failure excerpt, and
log path. Use stable names such as `unit.log` or `typecheck.log` and overwrite a superseded passing
log instead of accumulating timestamped copies. Enforce the 5 MiB cap while each command runs.
Never write secrets, credentials, environment contents, source files, or database exports to these
logs. Preserve current failure evidence until the failure is resolved.

## Workflow

### 1. Locate and load the review file

For each RED-GREEN cycle, run the narrowest executable target: one test name when the runner can
select it reliably, otherwise one test file, otherwise the smallest affected suite. Never run the
repository's full or canonical test command for an individual finding. Reuse a passing result only
while its relevant source, tests, configuration, and working-tree state remain unchanged; recording
or confirming existing proof does not by itself require another test invocation.

Accept an optional review-file path. Without one, search every checkout attached to this repository,
the main checkout included — review files are gitignored, so a file written inside a worktree exists
only there and is invisible from the main checkout:

```sh
# Every reviews/*.md in every checkout attached to this repository, main checkout included.
git worktree list --porcelain | awk '/^worktree /{ print $2 }' | while read -r wt; do
  [ -d "$wt" ] || continue
  find "$wt/reviews" -maxdepth 1 -name '*.md' -print 2>/dev/null
done
```

Use `find`, not a bare `*.md` glob: under zsh an unmatched glob is an error, so a checkout with no
`reviews/` directory would abort the search and produce a false "review loop is clean".

Skips worktrees not yet pruned. Key results by absolute path so two checkouts holding same-named
files stay distinct. The listing is identical from inside a worktree and from the main checkout, and
a repository with no linked worktrees yields exactly one path — so this collapses to plain
`reviews/` with no special case. Then select:

- exactly one file with `open` findings → use it;
- several → prefer the file whose `**Branch:**` matches the current branch; otherwise ask the user
  which to work on, naming the checkout each file came from;
- none → report that the review loop is clean and suggest `/skill:finish-task`.

Read the whole file. `**Repo:**` is authoritative. When it names a directory other than the current
repository root, **switch to that worktree** — `EnterWorktree` with that path when available,
otherwise supply that directory explicitly on every subsequent command. Never `git checkout` the
branch to reach it: git refuses to check out a branch already checked out in another worktree, which
is precisely the case here. Stop and report instead of guessing when the `**Repo:**` directory no
longer exists, or when `**Branch:**` is checked out in some worktree other than the one `**Repo:**`
names. Only when `**Repo:**` is the current root does the old rule apply: if the current branch
differs from `**Branch:**`, check out the named branch when it exists locally, otherwise stop and
report the mismatch.

### 2. Establish the task log directory

Do this **after** the worktree switch in step 1, never before. `REPO_ROOT` feeds `REPO_KEY`,
and inside a worktree `git rev-parse --show-toplevel` resolves to the worktree path — so
computing it first keys the logs to the wrong checkout.

Recompute the deterministic task log directory and refuse mismatched or symbolic-link paths:

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

### 3. Triage before fixing

List every `open` finding with id, axis, severity, and claim. Findings already marked
`deferred-task-decision` or `deferred-out-of-scope` are not work: list them once under "not in this
loop" and do not fix them unless the user explicitly reopens one, in which case set it to `open`
and treat it like any other finding. Findings tagged `Origin: task` are fixed like any other; the
tag is planning feedback, not an exemption. Then, before touching code:

- **Minor and nit findings:** present them as one list and ask the user which to fix and which to
  skip. For each skip, ask for a one-line reason, set the finding's status to `skipped-minor` with
  the reason, and append one line per skip to the task file named in the review header:
  `- skipped (minor): TR-4 — <claim> — <reason>`. Without a task file, record skips only in the
  review file.
- **Security findings:** before changing security-sensitive code, handle every security finding
  with the user. Explain in plain English:
  - the realistic scenario;
  - the likely consequence;
  - the exposure or probability;
  - what the fix would change.

  Wait for an explicit decision on each finding:
  - **Fix**: keep the finding in the work list.
  - **Accept**: set the finding's status to `accepted-security-risk`, and record the user's reason
    in the task file when one exists. Without a task file, keep the reason in the review file and
    return it to the caller for the PR risk section.

  Every security finding needs a user decision before this skill ends. An accepted finding remains
  visible in the final result.

### 4. Fix findings one by one

Work through the remaining `open` findings in severity order (blocker, major, then approved
minor/nit). A fix is judged by the same comment discipline as the original implementation:

Comments in the diff follow one test: a comment earns its place only when it says what the code
cannot — why this choice over the obvious alternative, an invariant the code depends on, or an
external constraint such as an API quirk or a production incident. Never narrate what the next
lines do; if the code needs narration, rename or split it. One home per fact: when the docstring
explains it, no inline repeat, and the other way round. Inline comments are one line, two at most;
anything longer belongs in the docstring or the companion doc. Before committing, reread every
comment in the diff and delete each one that fails this test.

Keep each regression test local to its finding. Prefer an existing narrow test seam. Do not
expand a shared scenario matrix or build a broader fixture unless the finding cannot be proved
otherwise; if that is necessary, explain why before doing it.

For each finding:

1. Inspect the cited location and the evidence that originally supported the finding.
2. Load `tdd` only for defects in production or test code with an observable behavioral seam:
   reproduce the finding as a failing test (RED), fix it (GREEN), refactor. Never invoke `tdd` for
   plan-only, documentation-only, dependency-only, or declarative configuration-only remediation;
   verify those with targeted syntax, consistency, or configuration checks instead.
3. Treat GREEN as the direct proof when it exercises the original failing scenario. Run only
   additional focused tests or checks needed for neighboring affected behavior that GREEN did not
   cover. Do not rerun the GREEN command solely as another proof, and do not run the full canonical
   suite after each finding.
4. Mark the finding `**Status:** fixed` in the ignored review file immediately, with one short line
   of proof (test name or check), then commit that finding's tracked fix on the review file's branch.
   Never stage the review file. One commit per finding keeps fixes individually revertable, while
   the local review file preserves crash- and context-reset recovery state. Prefix each of these
   commits with `HUSKY=0`: the repository hook's full typecheck, lint, and artifact refresh run once
   in `finish-task`; per-finding they add minutes and no evidence. Never `--no-verify`, never edit
   the hook.

If a new concern appears during remediation:

- Fix a failing test or direct regression caused by the remediation inside the same batch.
- Record an unrelated or minor concern as `deferred-out-of-scope` in the review file.
- Stop and ask the user when the concern is a new blocker, a new major issue, or requires a change
  to architecture, scope, or a trust boundary.

### 5. Verify the frozen findings

After all fixable findings are resolved:

1. For each finding identifier, confirm from still-valid retained evidence that the original failing
   scenario is covered by a focused test, static check, or direct diff evidence. Do not rerun a
   command solely to perform this confirmation.
2. Form the union of the focused tests and checks affected by all remediation, then run that batch
   once against the assembled diff.
3. Treat that batch as the review file's validation-tier check when it satisfies the tier. Run only
   distinct document/plan consistency or affected dependency/configuration proof that the batch did
   not already cover. For `canonical`, do not run the focused batch a second time; the one final
   canonical validation is owned by `finish-task`.
4. Store verbose output in `TASK_LOG_DIR`.

Do not search untouched parts of the diff for new minor findings. If targeted verification fails,
continue correcting the same frozen findings and rerun only the failed focused proof. If a fix
materially changed architecture, scope, or a trust boundary, finish this pass and recommend a fresh
`task-review` invocation; do not start it without user approval.

### 6. Report

All tracked remediation is already committed per finding. Commit any remaining tracked task-file
records for skip, accept, or defer decisions; never stage ignored review-file status updates. Confirm
no tracked task work remains uncommitted, then return a concise structured result:

- review file path, branch, and head SHA before and after remediation;
- each finding id with final status: `fixed`, `accepted-security-risk`, `skipped-minor`,
  `deferred-out-of-scope`, `deferred-task-decision`, or `unresolved`;
- the review file's planning feedback lines, repeated verbatim, so they reach the next `to-plan`;
- focused proof and validation commands, status, and log paths;
- accepted security risks and user reasons;
- whether a fresh `task-review` is recommended.

Tell the user the exact next command: `/skill:task-review` to re-review, or `/skill:finish-task`
when nothing remains open. Do not report success while any finding that the user did not explicitly
skip or accept remains open.
