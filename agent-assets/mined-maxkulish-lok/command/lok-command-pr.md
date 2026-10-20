# Phase: Pull Request

**Purpose**: Run pre-flight CI checks, create a pull request, monitor CI, wait for and address bot + human reviews, and get approval for merge.

**Entry conditions**: `current_phase: pr`

**Mirror**: `.pi/orchestrator/phases/pr.md`. Both sides write the same workflow YAML and are gated by the same `PHASE_CONFIG` in `.pi/extensions/orchestrate/index.ts`, so the required exit state below is not optional on this side either - a `pr` phase completed here must still satisfy the pi state machine, or resuming the task under pi will fail its transition check.

---

## Required exit state

```yaml
phases:
  pr:
    status: complete
    pr_url: "https://github.com/maxkulish/lok/pull/[n]"
    pr_number: [n]
    ci_passed: true
    bot_review_wait_completed: true
    bot_review_wait_completed_at: "[ISO-8601]"
    reviews_addressed: true
    bot_rereview_head_sha: "[sha]"    # "none" only when no reviewer bots are installed, or Qodo is billing-blocked and the user approved proceeding
    bot_rereview_at: "[ISO-8601]"
    pre_merge_refetch_passed: true
    pre_merge_refetch_at: "[ISO-8601]"
    merged_at: "[ISO-8601]"   # optional
    merge_commit: "[sha]"     # optional
```

History events required: `pre_flight_checks_passed`, `pr_created`, `ci_passed`, `bot_review_wait_completed`, `review_addressed`, `bot_rereview_verified`, `pre_merge_refetch_passed`.

---

## Status: pending (no PR exists)

### Step 4.0: Pre-flight CI Checks (MANDATORY)

**Before creating a PR, ALL local CI checks must pass.** This prevents wasting CI time on formatting/lint/test failures.

Run all checks:

```bash
cargo fmt --check
cargo clippy -- -D warnings
cargo clippy --tests
cargo test
```

**Display checklist after completion:**

```
PRE-FLIGHT CI CHECKS
=====================

  [x] cargo fmt --check
  [x] cargo clippy -- -D warnings
  [x] cargo clippy --tests
  [x] cargo test

All checks passed. Ready to create PR.
```

**If any check fails:**
1. Fix the issue
2. Commit with message: `fix(CLO-XX): fix [formatting|lint|type|test] issues before PR`
3. Add history entry: `pre_flight_fix_applied`
4. **Re-run ALL checks from the beginning** (fixes may introduce new issues)
5. Repeat until all pass

After all pass:
- Add history entry: `pre_flight_checks_passed`
- Update state: `phases.pr.ci_passed: false` (this tracks remote CI, not local pre-flight)

### Step 4.0.5: Commit remaining artifacts

Check `git status --short` before pushing. The implement phase leaves workflow YAML updates, lessons files and review reports dirty; untracked files under `docs/status/` or the lessons stores are destroyed by the branch deletion in the complete phase. Commit them to the PR branch now. If dirty files belong to another task, stop and tell the user - that is a cross-task boundary.

### Step 4.1: Create Pull Request

1. **Invoke**: `/pr:create CLO-XX`
2. Update state:
   - `phases.pr.pr_url: [url]`
   - `phases.pr.pr_number: [number]`
   - `phases.pr.status: in_progress`
3. Add history entry: `pr_created`

### Step 4.2: Monitor CI Status

After PR creation, check CI status:

```bash
gh run list --branch [branch-name] --limit 1
```

- **If CI passes**: Update `phases.pr.ci_passed: true`, add history: `ci_passed`
- **If CI fails**:
  1. Identify failing jobs: `gh run view [run-id] --log-failed`
  2. Fix the issue locally
  3. Re-run pre-flight checks (Step 4.0)
  4. Push the fix
  5. Add history: `ci_fix_applied`
  6. Re-check CI status

**Note what a CI fix push does to the bot review.** `qodo-code-review` reviews on PR open and never on push (`handle_push_trigger = False`). Any commit pushed here leaves Qodo's review pinned to a commit that is no longer the head, and Step 4.3 has to ask for a fresh pass.

---

## Status: in_progress (PR exists)

### Step 4.3: Wait for the bot review (MANDATORY)

**CI presence and bot-reviewer presence are independent facts.** "No CI configured" is never a reason to skip review fetching - PR #4 merged with 7 unaddressed inline comments on exactly that reasoning. See `.pi/lessons/pr-review-failures.md` L1, L2, L6.

1. **Probe which bots are installed**: scan the last 10 PRs in any state *plus this PR's own issue comments* for `qodo-code-review|copilot-pull-request-reviewer`. A closed-PR-only scan reports "not installed" for a newly installed bot.
2. **If none are installed**: record `bot_review_wait_completed: true` with the absence rationale and skip to Step 4.4.
3. **If Qodo is billing-blocked**: this PR has a Qodo comment containing `<!-- qodo:billing-blocked -->` ("workspace is out of credits"). No review is coming, so do not poll. Block for user guidance at once. If the user approves proceeding without a bot review, record `bot_review_wait_completed: true` with that rationale, skip the re-review request in Step 4.4, and record `bot_rereview_head_sha: "none"`.
4. **If any is installed**: poll `repos/maxkulish/lok/pulls/[n]/reviews` for a review by that bot whose `commit_id` equals the **current** head SHA. A timeout is not proof that review is clean.
5. **If the poll times out and Qodo is installed**: post `/agentic_review` as a PR comment, keep the `created_at` GitHub returns, and poll again for a review on the current head submitted at or after that timestamp. This is the normal path whenever Step 4.2 pushed a CI fix.
6. **If still nothing**: block for user guidance. Do NOT record `bot_review_wait_completed`.

The full procedure is `.pi/skills/pr-review-cycle.md` steps 1-2. Its gates are executed by `.pi/scripts/pr-review-cycle.sh` (`probe-bots`, `wait-review`, `request-rereview`, `wait-rereview`), which is covered by `.pi/scripts/tests/pr-review-cycle.test.sh`. Invoke the script rather than reinventing the polling here: a non-zero exit from a wait subcommand **is** the gate failure, and the script exits 3 - not 1 - when `gh` or a response failed, so a broken gate is never mistaken for "no review arrived".

On success:
- `phases.pr.bot_review_wait_completed: true`
- `phases.pr.bot_review_wait_completed_at: [ISO-8601]`
- Add history entry: `bot_review_wait_completed`

### Step 4.4: Address reviews

1. **Invoke**: `/pr:review CLO-XX`
2. That command verifies each finding before acting, addresses what is real, declines what is not **with evidence**, replies to every comment, and requests re-validation with `/agentic_review`.
3. **Addressing Qodo**: mention `@qodo` only in a reply you want it to read - a decline or a question. It ignores replies that do not address it. A plain "fixed in SHA" needs no mention; the re-review is what confirms the fix.
4. Re-run pre-flight checks (Step 4.0) before pushing.
5. Update `phases.pr.reviews_addressed: true`; add history entry: `review_addressed`.
6. Record the re-validation separately once observed:
   - `phases.pr.bot_rereview_head_sha: [sha the bot reviewed]` (`"none"` when no bots are installed, or Qodo is billing-blocked and the user approved proceeding)
   - `phases.pr.bot_rereview_at: [ISO-8601]`
   - Add history entry: `bot_rereview_verified`

There is no `/gemini review` trailer. Gemini Code Assist is sunset and the marker triggers nothing.

### Step 4.5: Pre-merge re-fetch (MANDATORY)

Immediately before transitioning to `complete`, re-check three things:

1. `phases.pr.bot_rereview_head_sha` equals the current head SHA (or is `"none"`). A mismatch means the bot reviewed an earlier commit - go back to Step 4.4 and request a pass on the current head.
2. No inline comments created since the last `review_addressed` event.
3. No unresolved review threads (GraphQL `reviewThreads`, `isResolved == false`).

Bots sometimes post after the initial wait window; merging without this check is what shipped PR #4 and PR #24 with missed inline comments. The runnable version of this gate is `.pi/orchestrator/phases/pr.md` §5.0.

On pass:
- `phases.pr.pre_merge_refetch_passed: true`
- `phases.pr.pre_merge_refetch_at: [ISO-8601]`
- Add history entry: `pre_merge_refetch_passed`

---

## Review Cycle

1. After addressing reviews, ask:
   ```
   PR CHECKPOINT

   PR: [url]
   Reviews addressed: [count]
   CI Status: [passing|failing|pending]
   Bot re-review: [sha] at [timestamp]

   Options:
   1. [check-again] - Check for new comments
   2. [ready] - PR is approved, ready to merge
   3. [pause] - Pause workflow

   Your choice:
   ```

2. **If check-again**:
   - Re-check for new reviews
   - Loop back to Step 4.4

3. **If ready**:
   - Run Step 4.5 first - it is a gate, not a formality
   - Update state:
     - `phases.pr.approved: true`
     - `phases.pr.status: complete`
     - `workflow.current_phase: complete`
     - `workflow.status: in_progress`
   - Add history entry: `pr_approved`
   - **Continue to COMPLETE phase**

4. **If pause**:
   - Save state
   - Exit with resume instructions

---

## YAML Checkpoint (Required before transition)

Before signaling completion to the dispatcher, verify:
- `phases.pr.pr_url` and `phases.pr.pr_number` are set (non-null)
- `phases.pr.ci_passed: true`
- `phases.pr.bot_review_wait_completed: true` with `bot_review_wait_completed_at` set
- `phases.pr.reviews_addressed: true`
- `phases.pr.bot_rereview_head_sha` and `bot_rereview_at` are set
- `phases.pr.pre_merge_refetch_passed: true` with `pre_merge_refetch_at` set
- `phases.pr.status: complete`
- `git status --porcelain` is empty - the complete phase deletes this branch
- History contains `pre_flight_checks_passed`, `pr_created`, `ci_passed`, `bot_review_wait_completed`, `review_addressed`, `bot_rereview_verified`, `pre_merge_refetch_passed`
