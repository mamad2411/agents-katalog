---
name: rust-compiler-diagnostics
description: Use when Rust code fails to compile, Clippy reports lints, borrow checker errors appear, lifetimes are unclear, or cargo diagnostics need systematic triage.
license: MIT
tags: [development, rust-compiler-diagnostics, rust]
metadata:
  source_references:
    - https://github.com/udapy/rust-agentic-skills
    - https://doc.rust-lang.org/rustc/
    - https://doc.rust-lang.org/clippy/
---

# Rust Compiler Diagnostics

Use this skill to resolve Rust compiler and Clippy diagnostics without guessing.

## Workflow

1. Run the narrowest command that reproduces the diagnostic, usually `cargo check -p <crate>` or a focused test.
2. Read the first real compiler error before secondary errors; later diagnostics are often consequences.
3. Identify the ownership, lifetime, type, trait, macro, feature, or lint category involved.
4. Inspect the definition site and the nearest caller before editing.
5. Prefer changing API shape only when the current contract is the real cause.
6. Re-run the same command after each fix, then broaden verification when the focused command is clean.

## Borrow Checker Triage

- Find who owns the value, who borrows it, and how long each borrow actually needs to live.
- Reduce borrow scope with blocks, local variables, or earlier extraction before adding clones.
- Split immutable data from mutable state when one large struct borrow blocks independent access.
- Move expensive or fallible work outside lock guards and mutable borrows.
- Use owned values for spawned tasks and cross-thread work; references rarely fit those lifetimes.

## Diagnostic Repair Examples

### End A Borrow Before Mutation

```rust
// Avoid: `self.items` is immutably borrowed while mutating `self`.
if let Some(item) = self.items.get(id) {
    self.record_access(item.name());
}

// Prefer: extract the needed owned value, ending the borrow.
let name = self.items.get(id).map(|item| item.name().to_owned());
if let Some(name) = name {
    self.record_access(&name);
}
```

### Move Out Of A Field Safely

```rust
if let Some(task) = self.pending_task.take() {
    task.cancel().await;
}
```

Use `Option::take` when a field must be moved out while leaving the struct in a valid state.

### Fix Escaping Borrow In Spawned Tasks

```rust
// Avoid: `&self` cannot be moved into a 'static task.
tokio::spawn(async move {
    self.refresh().await;
});

// Prefer: clone the owned handle needed by the task.
let client = self.client.clone();
tokio::spawn(async move {
    client.refresh().await;
});
```

## Clippy Triage

- Treat Clippy as design feedback, not only style feedback.
- Accept Clippy suggestions when they preserve readability and behavior.
- Add `#[allow(...)]` only near the smallest scope and include a short reason when the lint is intentionally violated.
- Do not silence `unwrap_used`, `expect_used`, `panic`, or lossy conversion lints in production paths without confirming the project policy.

### Prefer Targeted Allows

```rust
#[allow(clippy::too_many_arguments, reason = "constructor mirrors the wire protocol fields")]
pub fn from_wire(/* fields */) -> Self {
    // ...
}
```

## References

Read `references/error-triage.md` for common diagnostic families and repair patterns.
