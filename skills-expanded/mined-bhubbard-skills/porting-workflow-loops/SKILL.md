---
name: porting-workflow-loops
description: >
  Structures the execution of a large code port or migration as parallel
  write→review→apply loops driven off a work queue, with git/worktree
  discipline that keeps many workers from stepping on each other. Use when
  actually carrying out a big port, rewrite, or mechanical translation
  across hundreds/thousands of files, when the user wants to parallelize
  code generation or migration across many agents/workers, when asking
  "how do I run many Claudes/workers on a codebase at once", or when a
  parallel run is corrupting git state or producing stubbed/half-done
  code. Follows port-planning (do that first) and uses
  adversarial-code-review for the review stage. See
  compiler-errors-as-work-queue and test-suite-driven-port for the
  specific queues that come after translation.
---

# Porting workflow loops

Most day-to-day engineering reduces to a loop: pull a task, do it, get it reviewed, apply the feedback. A large port is that same loop run thousands of times in parallel. This skill covers how to structure those loops so the work is fast, consistent, and safe to merge. It's drawn from Bun's Zig→Rust rewrite, which ran ~50 such loops over 11 days.

Do `port-planning` first — you need PORTING.md and (if relevant) a lifetime guide before the loops have anything to follow.

## The loop

```
let task
while (task = todoList.pop()) {
  const result   = task()                                  // implementer writes code
  const feedback = await Promise.all([review(result), review(result)])  // ≥2 reviewers
  await apply(feedback, result)                            // fixer applies accepted feedback
}
```

Each `task` carries its own context (a file to port, a crate's compiler errors, a failing test). The `result` is the code. `review` runs adversarial reviewers (see `adversarial-code-review`) whose only job is to find bugs. `apply` lands the accepted fixes. Keep implementer, reviewer, and fixer as separate roles — the separation is what makes the review honest.

Structure the whole port as a sequence of these loops, each with a different queue:

1. Generate the porting guide + lifetime guide (planning).
2. Mechanically translate every source file to a target file, following the guides.
3. Fix every module's compiler errors (see `compiler-errors-as-work-queue`).
4. Get each subcommand / entry point to run (smoke tests).
5. Get the full test suite passing locally, then in CI (see `test-suite-driven-port`).
6. Cleanup / refactor passes (reduce `unsafe`, dedupe, idiomatic pass) — after green.

## Parallelism without collisions

Throughput comes from running many workers at once, but shared state is where parallel runs self-destruct. Bun peaked at ~1,300 lines/min with dozens of workers; the enabling trick was strict discipline, not more machines.

**Git discipline — the single most important rule.** Workers sharing a working tree will stash, pop, and hard-reset over each other and destroy work. Forbid every git command that isn't committing a specific file:

- **Never** `git stash`, `git reset`, `git checkout` of shared state, or any command that touches files a worker didn't author.
- Commit **one specific file (or a tight set) at a time**, by explicit path. No `git add -A`.
- No `git reset --hard`, ever.

**Worktree sharding.** Give each shard its own git worktree, and run several workers inside each. A handful of worktrees (Bun used 4), each with ~16 workers, balances parallelism against disk: full per-worker worktrees on a large repo run you out of disk, and the changes eventually have to compile together anyway.

**Ban slow commands from the hot loop.** A single slow `grep`, or an unguarded `cargo`/`build` invocation, can freeze disk I/O for everyone on the box. Keep expensive commands (full builds, `cargo check`, broad searches) out of the per-file loop; run them once at a queue boundary and feed their output in as the next queue. Watch real disk IOPS — an underprovisioned volume will make a fast plan look mysteriously slow.

**Isolate resource-hungry tasks.** Tests or tasks that exhaust sockets, spawn thousands of processes, or write gigabytes need OS-level isolation (cgroups / `systemd-run`, pid namespaces, memory & CPU caps), not politeness. "Please don't use too much memory" is not isolation.

## Fix the process, not the output

When a parallel run misbehaves, resist hand-cleaning the mess. The mess is a symptom; the workflow prompt is the bug. Edit the rule that generated the whole class of problem, then resume. Examples that actually came up:

- Workers ran `git stash`/`git reset` and clobbered each other → added the git-discipline rules above to the workflow.
- "Get all the modules to compile" was interpreted as "stub out the functions that don't compile" → added a rule forbidding stubs, and had reviewers reject them.
- Workers wrote long comments to justify hacks → added the reviewer rule: *if it needs a paragraph-long comment to justify the workaround, the code is wrong — fix the code.*

Each was one prompt edit that eliminated the behavior going forward. Hand-fixing individual outputs doesn't scale to thousands of files; fixing the generator does.

## Monitor continuously

Even a well-tuned loop needs a human (or supervising agent) reading outputs the whole way through — spotting bugs, noticing when a worker has gone off the rails, and editing the loop to correct it. The loops are autonomous, but the *steering* isn't. Budget for active monitoring across the entire run, not just a check at the end.

## Building confidence to merge

A million-line diff is unreviewable line-by-line by a human. Confidence comes from three things working together, not from reading every line:

1. A **language-independent test suite** with a large number of assertions as the correctness oracle (see `test-suite-driven-port`).
2. **Adversarial review** on every change before it lands.
3. **Fixing the process** whenever something goes wrong, so bug classes are eliminated rather than patched.

Merge into the main branch when the suite is 100% green on all platforms *and* you've verified the tests are actually running (not skipped or stubbed — see `port-verification-checklist`). Note that merging to main is a commitment to the rewrite, not necessarily a versioned release; you can move to main before you're ready to ship to users.
