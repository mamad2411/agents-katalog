---
name: port-planning
description: >
  Plans a large codebase port or rewrite from one language to another
  (e.g. Zig→Rust, Go→Zig, C→Rust, Python→Go, JS→TS) BEFORE any code is
  written. Decides incremental vs. big-bang, writes a PORTING.md pattern-
  mapping guide, and de-risks with a small trial run before committing to
  the full port. Use whenever the user talks about "porting", "rewriting",
  "migrating", "translating", or "reimplementing" a codebase or large
  module in a different language — even if they just say "should I rewrite
  X in Y" or "how do I move this project to another language". Pairs with
  porting-workflow-loops (execution), adversarial-code-review (review),
  and the Rust-specific port-to-rust-playbook when the target is Rust.
  This is the skill to reach for at the very start of a port, before the
  first file is translated.
---

# Port planning

The most expensive mistake in a large port is starting to translate code before you've decided *how* to translate it. This skill covers the decisions and artifacts that come first. It's based on the methodology Bun's team used to rewrite ~535k lines of Zig into Rust in 11 days (Claude Code + adversarial review), and it generalizes to any language pair.

Answer the two big questions below, produce the planning artifacts, run a trial, and only then hand off to `porting-workflow-loops` for the bulk translation.

## The two big questions

Everything else is tactics. Settle these first.

### 1. Incremental rewrite, or everything at once?

Default to **everything at once** for a whole-project port. An incremental rewrite forces you to write throwaway bridge code (FFI shims, dual data models, compatibility layers) that you *hope* gets deleted later, and it keeps two languages live in the same build for months. Bun's team chose all-at-once for exactly this reason — the same conclusion they'd reached years earlier porting esbuild from Go to Zig.

Choose **incremental** only when: the codebase is too large for one person/team to hold in context at once and there's no test oracle to catch regressions; the port must ship value continuously and can't freeze; or the two languages interoperate cheaply and the boundary is naturally narrow (e.g. porting one leaf library, not the core).

Write the decision down with its reasoning so reviewers and future contributors understand why.

### 2. How do you keep it the *same* system?

The goal of a de-risked port is a program that behaves identically to the original — same architecture, same performance envelope, same feature set — while gaining the target language's guarantees. The safest path is a **mechanical port**: translate structure-for-structure so the new code "looks like you transpiled the old code," with the minimum number of behavioral changes. Idiomatic refactors come *after* it ships and the test suite is green, not during.

Why mechanical first: a line-by-line correspondence means anyone who understands the original understands the port, reviewers can diff behavior directly, and you avoid conflating "translated it" with "redesigned it" — two failure modes at once. Note the tradeoff explicitly in the plan (e.g. "expect more `unsafe`/verbose code initially; schedule an idiomatic cleanup pass post-ship").

## Planning artifacts

Before writing code, produce these and review them (ideally with adversarial review — see `adversarial-code-review`). Spend real time here; a few hours of planning saves days of rework.

### PORTING.md — the pattern-mapping guide

Talk through, then serialize, a concrete mapping from source-language patterns and types to target-language patterns and types. This is the single most important artifact — every worker translating a file reads it, so it's what keeps 1,000+ files consistent.

A good PORTING.md covers:

- **Type mappings**: how each core type, container, string type, and error type in the source maps to the target (e.g. Zig `?T` → Rust `Option<T>`, Zig `!T` → Rust `Result<T, E>`, tagged unions → enums).
- **Cleanup/resource idioms**: how the source's resource management maps (e.g. Zig `defer`/`errdefer` → Rust `Drop`; C `goto cleanup` → RAII).
- **Control-flow and metaprogramming**: how compile-time constructs, macros, generics, and comptime map — and where a 1:1 mapping is impossible so behavior must be reproduced deliberately (see `semantic-porting-pitfalls`).
- **Naming conventions**: casing, module layout, file→file correspondence.
- **Explicit non-goals**: patterns you are *not* trying to improve in this pass.

Keep it a living document; update it when a translation reveals a case it didn't cover.

### Memory / lifetime analysis (if crossing an ownership boundary)

If the target language has stricter ownership than the source (manual memory → borrow checker, GC → manual, etc.), do a dedicated pass that traces how memory actually flows before translating. For a Rust target this is significant enough to have its own skill — see `rust-lifetimes-analysis` for producing a `LIFETIMES.tsv`. The general principle: the ownership model of every long-lived value should be decided and written down before the code that implements it, not discovered mid-translation.

## De-risk before you commit

If you're about to do something big and expensive, spend a little to prove it's viable first.

**Trial run.** Before translating all N files, translate ~3. For each, have one worker write the new file and two independent reviewers check that it matches the original's behavior and follows PORTING.md (and the lifetime guide, if any), then apply fixes. This surfaces gaps in PORTING.md, tells you whether the mapping is sound, and gives you a realistic sense of cost — all before you've spent the full budget.

**Expect false starts and plan to fix the process, not the output.** In a large parallel port, early runs will do surprising things (workers stepping on each other's git state, stubbing functions instead of implementing them, writing paragraph-long comments to justify hacks). Treat these as bugs in the *workflow*, not one-off messes to hand-clean. The fix is a prompt/rule edit that prevents the whole class — see `porting-workflow-loops`.

## Output

Produce, in order:

1. A short **decision record**: incremental vs. big-bang, and mechanical vs. idiomatic, each with its reasoning and its explicit tradeoff.
2. A **PORTING.md** draft (or an outline if the codebase hasn't been surveyed yet), reviewed for internal conflicts.
3. A **lifetime/ownership plan** if the port crosses an ownership boundary.
4. A **trial-run plan**: which 3 files, and the accept criteria.

Then hand off to `porting-workflow-loops` to execute the bulk translation.
