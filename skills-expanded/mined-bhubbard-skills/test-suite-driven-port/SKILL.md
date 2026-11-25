---
name: test-suite-driven-port
description: >
  Uses an existing, language-independent test suite as the correctness
  oracle for a port or rewrite — the thing that lets you responsibly merge
  a huge machine-generated diff. Covers reusing the original test suite,
  the smoke-test → local-green → CI-green progression, sharding, test
  isolation for resource-hungry tests, and confirming tests actually run.
  Use when planning how to VERIFY a port is correct, when the user asks
  "how do I know the rewrite didn't break anything", "how do I get the
  test suite passing after a port", "how do I trust a million-line diff",
  or when setting up CI to gate a large migration. Pairs with
  porting-workflow-loops and port-verification-checklist.
---

# Test-suite-driven porting

You cannot read a million-line diff line by line. What lets you merge one responsibly is an external oracle that doesn't care how the code is written: a **comprehensive test suite with a large number of assertions**. If the original project has one, it's the most valuable asset in the whole port. The plan is to change *how* the code is written while proving *what* it does is unchanged.

## Reuse the original test suite unchanged

The least risky port keeps the exact test suite you already trust and makes the new implementation pass it. This works best when the suite is written in a language independent of the implementation:

- Bun's runtime moved from Zig to Rust, but its test suite is written in TypeScript — so it tested the ported runtime with zero changes.
- A CLI's tests written as shell/golden-file comparisons don't care whether the binary is Go or Rust.
- Any black-box suite (HTTP contract tests, CLI I/O snapshots, protocol conformance) transfers directly.

Guard this asset. **Do not skip, delete, weaken, or rewrite tests to get to green** — that's discarding the one thing proving correctness. Zero tests skipped or deleted is the standard to hold. If a test genuinely must change (e.g. it asserted an implementation detail that legitimately changed), call it out explicitly and review it as a behavioral change, not a convenience.

## The progression: smoke → local → CI

Get to green in stages; each stage is its own workflow loop (see `porting-workflow-loops`).

1. **Compile and link.** After the error queue clears (`compiler-errors-as-work-queue`), the binary still has to link and start. Expect linker errors, then an immediate panic on startup. Fix those first.
2. **Smoke tests.** Get the simplest invocation to run (`--version`), then one real subcommand (e.g. run a single test file). Loop over entry points / subcommands: save each failing stacktrace with its subcommand, one worker fixes, two review, one applies.
3. **Local suite green.** Loop over test files. Shard ~100 random files at a time across worktrees by directory. For each failing test, save the stacktrace and errors to a file, one worker proposes a fix, two review, one applies.
4. **CI green on every platform.** CI exposes platform-specific failures the local box hides. Loop on fixing CI failures per platform until each platform is fully green. Expect platforms to finish at very different times (Bun's Linux went green almost a full day before Windows) and to wobble back to red until the last flaky failures are fixed. Merge only when **all** platforms are green in the same build.

## Test isolation is not optional

Real suites contain tests that are hostile to a shared machine, and running them in parallel without isolation will crash the box:

- memory-leak tests and long integration tests (e.g. a dev-server HMR test that runs for over a minute) that **time out in slow/debug builds**,
- stress tests that exhaust the machine's TCP sockets,
- tests that read/write gigabytes to disk,
- tests that spawn ~10k processes.

Isolate them with OS mechanisms — `systemd-run`/cgroups for memory & CPU caps, pid-namespace isolation — not with "please." Even then, expect to hit disk-space limits and crash a few times; provision accordingly. Give debug builds longer timeouts than release, since safety checks and missing optimizations make them much slower.

## Treat the suite as behavior spec — including new failures

When the port *changes* a legitimate behavior, the suite will tell you, and that's a feature. Bun's recursive-descent parsers used less stack space in Rust, so a test asserting that a 25,000-deep nested TOML input throws `RangeError` (from stack exhaustion) started *passing* the parse instead — the improvement broke the test's assumption. Read such failures as "behavior moved, decide if that's intended," not "make it green." Sometimes the right fix is updating the test to match a genuine, intended improvement — done deliberately and reviewed, never silently.

## Before you trust green

A green suite only means something if the tests ran. Confirm they weren't skipped, stubbed, or gated off — see `port-verification-checklist`. Manually verify a sample actually executed and asserted. Only then is the green meaningful enough to merge on.
