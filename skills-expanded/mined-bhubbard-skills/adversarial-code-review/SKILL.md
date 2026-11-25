---
name: adversarial-code-review
description: >
  Reviews code changes using a split-context adversarial method: the
  reviewer sees ONLY the diff (never the author's reasoning) and is tasked
  solely with finding bugs and reasons the code is wrong. Designed for
  reviewing large volumes of machine-generated or ported code where the
  author is biased toward shipping. Use when reviewing a port or rewrite,
  auditing AI-generated code, checking a big diff for correctness/
  regressions, when the user asks to "find bugs", "review this like an
  adversary", "poke holes", "red-team this change", or wants a second
  independent pass on code that already compiles. Especially valuable when
  the author and reviewer would otherwise be the same context. Pairs with
  porting-workflow-loops and semantic-porting-pitfalls.
---

# Adversarial code review

Code that compiles cleanly and *looks* plausible is exactly where correctness bugs hide. The person (or model) who wrote a change wants it merged, which biases them toward declaring it done. This skill removes that bias by structurally separating the roles: the reviewer's only job is to prove the code is wrong.

This is the review method Bun's team used to merge over a million lines of ported Rust with confidence. Three real bugs it caught — all of which compiled and looked right — are in the examples below.

## The core rule: split the context

Set up review as two distinct roles that do not overlap.

- **Implementer** — has full context: the original code, the port/design plan, its own reasoning. Writes the code. Does *not* review.
- **Adversarial reviewer** — gets **only the diff**, nothing else. None of the implementer's reasoning, none of its justifications. Is told to assume the code is wrong and to exhaustively enumerate the ways it breaks. Does *not* implement.

Use **two or more independent reviewers per implementer**. Independence is the point: reviewers who share the author's context inherit the author's blind spots. A reviewer who only sees the diff has to reconstruct correctness from the code itself, which is precisely the check you want.

Keep the roles clean: the implementer doesn't get to wave off findings, and the reviewer doesn't get to "just fix it" — a separate fixer applies accepted feedback. This prevents the reviewer from quietly adopting the implementer's frame.

## What the reviewer looks for

Instruct the reviewer to hunt specifically for the failure modes that survive compilation:

- **Semantic divergence from the original.** For ported code, does the new code actually do what the old code did, edge cases included? Syntactically-identical-but-semantically-different constructs are the top source of port bugs (see `semantic-porting-pitfalls`).
- **Eager vs. lazy evaluation.** Arguments that run when they shouldn't — e.g. `unwrap_or(expensive_or_panicking())` evaluates its argument even on the `Some` path; `unwrap_or_else(|| …)` stays lazy.
- **Lifetime / ownership across async or FFI boundaries.** Memory handed to a callback or C library that the local scope then frees — use-after-free and double-free. (E.g. a boxed handle passed to an async `close()` that drops at end of scope while the C side still holds the pointer.)
- **Numeric and sign edge cases.** Truncation vs. flooring for negatives, off-by-one on boundaries, odd-length slices, overflow, invalid intermediate states (e.g. a negative nanoseconds field).
- **Release-vs-debug behavior differences.** Assertions or checks that vanish in release builds; bounds checks present in one build mode and not another.
- **Error-path resource handling.** Leaks or double-frees in rarely-executed error branches.

## Reject workarounds, don't accept explanations

A powerful, generalizable review rule:

> If the code needs a paragraph-long comment to justify why a workaround is OK, the code is wrong — fix the code.

Long explanatory comments defending a hack are a signal the implementer talked itself into something. Reviewers should reject these and require the underlying code be corrected instead. This one rule shuts down a whole class of "technically compiles" cruft.

## Worked examples

Each of these compiled cleanly and looked correct. The reviewer had only the diff.

**Async use-after-free / double-free.**
```rust
StdioResult::Buffer(mut pipe) => {
    pipe.close(Subprocess::on_pipe_close) // pipe: Box<uv::Pipe>
}
```
`uv_close` is asynchronous — libuv keeps the raw pointer until the next loop tick, then calls `on_pipe_close`, which frees it. But `pipe` is a `Box` that drops at the end of this match arm, so libuv is left holding freed memory and the callback frees it a second time. Fix: `Box::leak(pipe).close(Subprocess::on_pipe_close)`.

**Truncation vs. floor on negative time.**
```rust
let sec = t.trunc();
TimeLike { sec: sec as i64, nsec: ((t - sec) * 1e9) as i64 }
```
For a file mtime before 1970 (negative, non-integer), `trunc` rounds toward zero: `-1.5` → `{sec: -1, nsec: -500_000_000}`. A negative `nsec` is an invalid timespec. Fix: `floor()` so `nsec ∈ [0, 1e9)`.

**Eager argument evaluation.**
```rust
let p1 = first.percentage.unwrap_or(1.0 - second.percentage.unwrap());
```
`unwrap_or` evaluates its argument eagerly, so `second.percentage.unwrap()` runs even when `first.percentage` is `Some` — panicking when only the second value is absent. Fix: `unwrap_or_else(|| 1.0 - second.percentage.unwrap())`.

## Output format

For each finding, report:

- **Location** — file and the specific construct.
- **The bug** — the concrete scenario that triggers it (inputs, build mode, timing), not a vague "this might be unsafe".
- **Severity** — crash/UB/data loss vs. cosmetic.
- **Fix** — the minimal correct change.

Prioritize findings that are reachable in real usage. A reviewer that only produces true, reachable bugs is worth far more than one that pads the list with hypotheticals — but when in doubt, surface it and let the fixer judge.
