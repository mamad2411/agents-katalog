---
name: rust-anyhow-source-study
description: "Use when continuing the learn-anyhow Rust study workflow in the learn-mine-cli repo: explain anyhow source code through small runnable Cargo examples, connect each concept to relevant Rust standard library source when useful, extract expert interview and industry pitfall angles, and persist lessons as examples plus notes under learn-anyhow."
---

# Rust Anyhow Source Study

## Overview

Use this skill to continue a source-driven Rust learning path centered on `anyhow`. The goal is not to summarize everything, but to turn each concrete confusion into a small runnable example, a focused note, and, when valuable, a trace into Rust standard library source.

## Repository Conventions

Work inside the current `learn-mine-cli` repository.

Use `learn-anyhow` as the learning package:

```text
learn-anyhow/
├── Cargo.toml
├── examples/
│   ├── mini-anyhow.rs
│   └── 02-main-error-printing.rs
├── 01-box-dyn-error.md
└── 02-main-error-printing.md
```

Add new lessons as paired files:

```text
learn-anyhow/examples/03-topic-name.rs
learn-anyhow/03-topic-name.md
```

Prefer Cargo commands:

```bash
cargo run --example 03-topic-name -p learn-anyhow
cargo check --example 03-topic-name -p learn-anyhow
```

## Learning Workflow

1. Start from the user's concrete confusion.

Example: "`main() -> Result<()>` 为什么用 Debug 打印？"

2. Identify the smallest relevant source path.

For `anyhow`, prefer local crate source:

```text
~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/anyhow-1.0.103/src/
```

For Rust source, prefer the checked-out submodule in this repo:

```text
learn-rust/
```

Standard library paths should normally be inspected under:

```text
learn-rust/library/
```

Examples:

```text
learn-rust/library/std/src/process.rs
learn-rust/library/std/src/fs.rs
learn-rust/library/core/src/result.rs
learn-rust/library/core/src/error.rs
```

Only fall back to the installed toolchain source when `learn-rust` is missing or clearly does not contain the needed file:

```bash
rustc --print sysroot
```

3. Explain the runtime or type-system path as a chain.

Good shape:

```text
read_to_string
  -> returns io::Result<String>
  -> ? converts io::Error into MiniError
  -> main returns Err(MiniError)
  -> std::process::Termination for Result<T, E>
  -> requires E: Debug
  -> prints Error: {err:?}
```

4. Build or extend one runnable example.

Keep examples small. A good example isolates one mechanism: `From`, `Display` vs `Debug`, `source()`, `Box<dyn Error>`, `downcast_ref`, or `Context`.

5. Persist the lesson in a paired Markdown note.

The note should include:

- the command to run
- the exact concept being demonstrated
- the relevant code excerpt
- the source-code chain
- the takeaway in beginner-friendly language
- a short expert/interview lens when the concept has real interview or production pitfalls

## Rust Source Study Heuristics

Prefer question-driven source reading over broad source tours.

Use these bridges from `anyhow` into Rust source:

- `?` and conversion: `learn-rust/library/core/src/result.rs`, `From`, `Try`, `FromResidual`
- `main() -> Result`: `learn-rust/library/std/src/process.rs`
- file reading: `learn-rust/library/std/src/fs.rs`, `std::fs::File`, `std::io::Read`
- error traits: `learn-rust/library/core/src/error.rs`, `std::error::Error`
- trait objects: `dyn Trait`, `Box`, pointer metadata, vtables
- downcasting: `Any`, `TypeId`, `Error::downcast_ref`

Do not over-explain compiler internals unless the user's question requires it. First give the practical mental model, then point to the source location that proves it.

## Expert Interview Lens

For each lesson, add expert-level context only when it sharpens the learning.

Good angles:

- what an interviewer may ask next after the basic answer
- what production bugs happen when the concept is misunderstood
- what tradeoff the library chose and what simpler alternative exists
- what is stable Rust surface area vs compiler/runtime implementation detail
- what should not be copied into ordinary application code

Keep this section short. Treat it as a reference point, not the main lesson.

Example for `main() -> Result`:

```text
Interview angle: main returning Result uses Termination and requires E: Debug. Display is not used by the runtime path. A strong answer names Termination, points to std::process, and explains why anyhow customizes Debug.
Production angle: relying on derived Debug for user-facing errors can leak noisy internal structure; application error reports usually need curated Display/Debug behavior.
```

## Anyhow Study Sequence

Let concrete questions change the sequence. The current path is:

1. `Box<dyn StdError + Send + Sync + 'static>` and type erasure
2. `main() -> Result` and `Debug` printing
3. manual `Debug` plus call-site error location
4. `?`, `From`, `map_err`, manual `match`, and `Ok(...)` evaluation order
5. `Option`, `Some`/`None`, `if let`, and borrowing versus moving
6. `'static`, borrowed versus owned data, and why error wrappers need stable storage
7. `macro_rules!`, macro expansion, and `file!`/`line!`/`column!` call-site metadata
8. `std::error::Error::source` and the coherence tradeoff behind generic `From<E>` wrappers
9. adding a `ContextError<C, E>` wrapper
10. `chain()` iteration
11. `downcast_ref` and `TypeId`
12. why real `anyhow::Error` uses its own thin pointer and vtable

## Style

Use Chinese explanations by default.

Keep each lesson concrete. Avoid saying "this is magic"; instead say which trait, impl, macro, or runtime hook is responsible.

When adding code, prefer examples that compile with stable Rust and require no external dependency unless the lesson is specifically about `anyhow` itself.

When validating, prefer targeted commands:

```bash
cargo check --example NAME -p learn-anyhow
cargo run --example NAME -p learn-anyhow
```

If the example is supposed to fail at runtime, use `cargo check` for validation and explain that `cargo run` should produce an error.
