---
name: compiler-errors-as-work-queue
description: >
  Turns a mountain of compiler errors into a parallelizable work queue:
  dump errors to a file, group by module/file, divide among workers, fix,
  review, apply — module by module. Use after a large port or refactor
  leaves thousands of build errors, when the user faces an overwhelming
  compiler-error count and wants a systematic way to burn it down, when
  splitting a monolith into many modules/crates surfaces mass breakage, or
  when asking "how do I fix 16,000 compiler errors" / "how do I
  parallelize fixing build errors". Pairs with porting-workflow-loops. Do
  NOT use for deciding how to split code into crates or where crate
  boundaries go — that's rust-crate-decomposition; this skill is for
  clearing the errors that result.
---

# Compiler errors as a work queue

After a mechanical port, nothing compiles yet — and that's fine. Thousands of compiler errors are not a crisis; they're a **work queue**. A number that's insane for one human (Bun's rewrite surfaced ~16,000 errors after splitting into ~100 crates) is routine for many workers running in parallel. The compiler is doing your triage for free: it tells you exactly what's broken and where.

## The method

Work **module by module** (crate by crate, package by package — whatever the target language's compilation unit is), because errors within a unit are related and fixes are local.

For each module:

1. **Run the build once** (`cargo check`, `tsc`, `go build`, etc.) and write the errors to a file. Run it *once*, at the start — not repeatedly inside the loop, where it would serialize everything and freeze I/O for parallel workers.
2. **Group the errors** by file (and sub-group by symbol/function when a file is large).
3. **Fix** all the errors within the module.
4. **Review** the changes with two adversarial reviewers (see `adversarial-code-review`).
5. **Apply** accepted fixes with a fixer.
6. Commits land per module; only then do the counters move.

Then advance to the next module. Order modules leaf-first (dependencies before dependents) so you're not fixing against a still-broken foundation.

## Parallelize across modules

The error file is the queue; divvy it among workers. Bun ran 64 workers — 16 loops across 4 worktrees — each doing one-fixes / two-review / one-applies. Keep the same discipline as any parallel port (see `porting-workflow-loops`):

- **Build only at queue boundaries**, never inside the per-file loop. One stray `cargo check` in the loop, or one slow `grep`, can stall disk I/O for every worker on the machine.
- **No `git` except committing specific files by path.** No stash, no reset.
- Each worktree owns its shard so workers don't collide.

## The hard class: cyclic dependencies

The trickiest errors when splitting one compilation unit into many are **cyclic dependencies**. A codebase that was effectively one unit has no reason to be acyclic; carving it into modules exposes every cycle at once, and those show up as a wall of errors.

Don't hand-untangle cycles inline while also fixing everything else — that mixes two hard problems. Instead:

1. Run a **classification pass** first: a dedicated loop that decides where each piece of cyclic code should live, and writes the decisions down. Do the analysis before the surgery.
2. Run a **refactor pass** that executes the plan.
3. *Then* let the per-module error queue clean up what remains.

If a pre-port PR to break cycles turns out to be insufficient (it usually is), don't start over — layer these analysis-then-refactor passes on top of where you already are.

## Don't accept stubs

Watch for the failure mode where "get the modules to compile" gets read as "make the compiler stop complaining" — i.e. stubbing out or `todo!()`-ing the functions that don't compile, or gating real code behind a shim. That produces a green build that does nothing. Add an explicit rule against stubbing, and have reviewers reject:

- functions replaced with placeholders / `unimplemented!()` / empty bodies to silence errors,
- real implementations gated off behind a "temporary" shim,
- and any workaround that needs a paragraph-long comment to justify it — if it needs the paragraph, fix the code instead.

A compiler error is a task to *complete*, not to *suppress*. The whole value of using the error list as a queue is that it's a faithful checklist of remaining work — stubbing corrupts the checklist.
