---
name: pre-push-review
description: >-
  Comprehensive pre-push review that FIXES issues before pushing — covering code
  smells, architectural patterns, security, scalability, and performance. MUST
  run BEFORE any `git push`, for EVERY project on EVERY branch. Reviews the
  diff to be pushed, fixes the findings, re-verifies, and only then pushes
  clean code.
  Trigger on "check before pushing", "run the pre-push check", "review
  before push", "pre-push review", the PRE-PUSH POLICY gate message, or
  proactively whenever about to run `git push` / the user asks to push.
---

# Pre-Push Review (fix-and-verify)

A gated review run against the commits about to be pushed. It does not just
report — it **fixes** the findings so the pushed code is free of code smells and
of security / scalability / performance problems.

## Step 1 — Decide whether the gate applies

```bash
git rev-parse --show-toplevel 2>/dev/null || { echo "not a git repo"; exit 0; }
```

The gate applies to EVERY project on EVERY branch. Only skip when there is
nothing to review (not a git repo, or an empty push diff in Step 2).

## Step 1b — The standard you mark against

Read the **`engineering-standards`** skill. It is the same list the code is written
from, so these findings are ones the author could have avoided rather than rules
invented at push time. It also defines the scope rule and the one-pass discipline.

## Step 2 — Collect the scope, once

Review what will be pushed, and the code it lives in:

```bash
git diff @{upstream}..HEAD              # if an upstream exists
git diff origin/main...HEAD 2>/dev/null || git diff main...HEAD   # new branch fallback
git diff --name-only <same range>       # scope to changed files
```

If the diff is empty, report "nothing to review" and allow the push.

Then widen once: read each changed file **in full** and find the direct callers and
callees. Findings split into **in this change** (fix all of them) and **pre-existing,
found while reading** (fix the small and safe ones; report the rest with a suggested
fix and let the author decide). Stop at callers and callees.

## Step 3 — Review across all five dimensions

Go through every changed hunk and find real issues (with `file:line`):

1. **Code smells & maintainability** — duplication, dead code, long/complex
   functions, deep nesting, magic numbers, unclear names, missing error
   handling, leaky abstractions, leftover TODO/FIXME/debug.
   - **Exhaustive failure handling (always):** every failure mode must be
     handled deliberately, per best practices — never silently swallowed. Flag
     any early-return / empty-catch / disabled-feature / falsy-response /
     `Promise.allSettled` rejection / external-call error that exits without a
     log, metric, or caller-visible signal. A "nothing happened" path that an
     operator can't see in logs and a user can't see in the UI is a bug, even
     when the types compile. Prefer: log at the right level (warn/error for
     unexpected, debug for benign), and surface terminal failures to the caller
     instead of leaving them hanging.
   - **Behavioural analytics (always):** a new feature, or a change to logic
     that already ships, emits its behaviour events in the same push. Flag any
     new user- or operator-visible flow whose entry, success, failure and
     drop-out paths report nothing, any event name invented outside the
     project's taxonomy, any event describing a mechanic the product does not
     have, and any tracking call that can fail the flow it measures. Unmeasured
     behaviour is a hole in the funnel that nobody notices until an analyst asks
     the question months later, and it costs almost nothing to close while the
     code is still being written. Fix it by emitting through the project's
     existing tracking service, with failures logged at warn rather than raised.
2. **Architectural patterns** — layer/boundary violations, wrong responsibility
   placement, tight coupling, circular deps, God objects, business logic in the
   wrong layer, breaking the project's established patterns.
3. **Security** — injection (SQL/command/path), unsanitized input, hardcoded
   secrets/tokens/keys, broken authn/authz, unsafe deserialization, sensitive
   data in logs, missing TLS/cert validation, over-broad permissions, CORS/CSRF.
4. **Scalability** — N+1 queries, unbounded loops/collections, missing
   pagination, in-memory growth with input, blocking calls on hot paths,
   non-idempotency, shared mutable state, lock contention.
5. **Performance** — needless allocations, O(n²) where O(n) is possible,
   repeated work that should be cached/memoized, sync I/O that should be async,
   chatty network calls, large payloads, missing indexes.

**Fan the five dimensions out as parallel subagents, in a single message with
five tool calls** — one lens each, then merge and dedup. Firing them one at a
time makes the review take the sum of the five instead of the slowest one; that
is the difference between about a minute and about five. Only skip the fan-out
when the diff is a handful of lines in one file, and then do all five inline in
one pass.

You may corroborate with `/code-review` and `/security-review`, but this skill
owns all five dimensions and the fixing.

## Step 4 — FIX the findings (this is the point of the skill)

For every confirmed finding, apply the fix in the working tree:

- **Auto-fix** anything concrete and behavior-preserving: code smells,
  injection/secret/logging security holes, N+1 / unbounded / blocking
  scalability issues, obvious performance fixes (caching, async, algorithmic).
- **Escalate to the user first** only when a fix would meaningfully change
  behavior, public API, or architecture, or when intent is ambiguous — explain
  the tradeoff and let them choose. Default to fixing; ask only when genuinely
  unsure.
- Keep each fix minimal and matched to the surrounding code style.

After fixing, **verify once**: build, tests, linter and formatter, plus a re-read of
the hunks you changed.

This is one pass, not a loop. Collect the scope once, analyse every dimension over it
once, dedup and verify, fix everything confirmed, then run the gate. Re-analysis only
if the gate fails, and only over what it flagged. Findings that appear while fixing
join the list rather than restarting the analysis — a review that keeps finding one
more thing is a review nobody trusts to be finished.

## Cost discipline

The measured cost of this review is dominated by waiting, not by analysis. Three
rules, in order of how much they save:

1. **Run the whole pass in one turn.** Review, fix, commit, approve and push
   without handing control back in the middle. Two thirds of the elapsed time of
   a typical run is the pass stopping and waiting for someone to say "continue".
2. **Escalate at most once, at the end.** If several findings need a decision,
   collect them into a single question after the pass is otherwise complete —
   never one question per finding, never mid-analysis. Nothing ambiguous blocks
   the fixes that are not.
3. **Reach the gate once.** Write the approval immediately after the final fix
   commit, in the same turn, so the gate is hit once rather than repeatedly. A
   run that trips the gate several times has re-read the same diff each time.

Command hygiene, which is pure overhead: use `git -C <root>` and absolute paths
instead of chains of `cd`, and put independent commands in one call rather than
one call each.

Then fold the fixes into the push: either `git commit --amend` (if fixing your
last commit is appropriate) or add a new commit (e.g. `fix: address pre-push
review findings`). The push must contain the cleaned code, not a follow-up.

## Step 5 — Verdict and push

Show a short summary: what was found, what was fixed, and anything escalated.

- **🟢 Clean** — no blocking findings remain. Proceed to push.
- **🟠 Needs a decision** — an escalated item is waiting on the user. Stop and ask.

When clean, record the one-shot approval and push. The approval script resolves
HEAD on its own — never type, echo, or ask anyone for a commit hash:

```bash
~/.claude/scripts/prepush-approve.sh   # path is also printed by the gate message
git push                                # the gate sees the approval and allows it once
```

Run it AFTER the final fix commit, so the approval covers the commit being pushed.


## Notes

- Scope strictly to the push diff and code it touches; don't refactor unrelated
  pre-existing code.
- Match severity to real impact — a style nit is not a blocker, but still fix
  cheap nits while you're there.
- Never push silently when an escalated decision is pending.
