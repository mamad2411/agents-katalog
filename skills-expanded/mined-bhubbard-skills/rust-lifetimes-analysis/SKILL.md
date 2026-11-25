---
name: rust-lifetimes-analysis
description: >
  Adds Rust lifetimes and ownership to code being ported from a manually-
  memory-managed or garbage-collected language (Zig, C, C++, Go) by
  tracing every struct field's actual control flow and recording the
  decision in a LIFETIMES.tsv before translation. Use when porting to Rust
  and struggling with "how do I express this pointer's lifetime", when the
  borrow checker is fighting a mechanical port, when planning how to model
  ownership for a codebase that used raw pointers / arenas / refcounting /
  a GC, or when the user asks "how do I add lifetimes to manually managed
  memory". Part of the port-to-rust-playbook; do this before
  porting-workflow-loops translates the code.
---

# Rust lifetimes analysis

When porting into Rust from a language that manages memory manually (Zig, C, C++) or via a garbage collector (Go, or a codebase embedding a GC'd runtime), the single hardest question is: **what is the lifetime and owner of every long-lived value?** In the source language this was implicit — a raw `*T` passed around, an arena, a refcount, or "we pay close attention." Rust demands you make it explicit in the type system. Answering this *before* translation is what keeps the borrow checker from turning the port into a fight.

## Do the analysis before the code

Mechanical translation goes badly if each worker invents an ownership model per file — you get inconsistent, conflicting choices that don't compose. Instead, run a dedicated **lifetimes analysis pass** up front and serialize the results, so every worker translating a file reads the same decisions.

The workflow that produced Bun's `LIFETIMES.tsv`:

1. **Read every struct field in every file** and trace its control flow — where it's created, who holds it, who reads it after the creating function returns, and where it's freed.
2. **Find the fields with non-trivial lifetimes** first — the ones that escape their creating scope, are shared, or outlive the obvious owner. Trivial owned-by-value fields need no special treatment.
3. **Propose a lifetime / ownership model** for each such field (see the options below).
4. **Review each proposal with two adversarial reviewers** (see `adversarial-code-review`) whose job is to find where the proposed lifetime is wrong or unsound.
5. **Apply feedback and serialize into `LIFETIMES.tsv`** — one row per field, machine-readable so other workers can look it up while translating.
6. **Reconcile with `PORTING.md`.** Run a combined adversarial pass over the lifetime guide and the pattern-mapping guide together to fix conflicting suggestions, then read it over yourself.

## Choosing an ownership model per field

Map the source's implicit strategy to an explicit Rust one. Common cases:

- **Clear, non-escaping scope (arena-friendly):** if a value doesn't outlive the function that builds it — e.g. parser AST nodes that don't escape the parse — a borrowed lifetime `&'a T` or an arena allocation expresses it directly. This is the cleanest case; identify it aggressively.
- **Shared, indeterminate lifetime:** where the source used reference counting (or a homegrown smart pointer), use `Rc<T>` / `Arc<T>`, or `Rc<RefCell<T>>` when shared mutability is needed. Match the source's sharing semantics rather than inventing new ones.
- **Single clear owner + borrowers:** one struct owns the value (`T` or `Box<T>`), others hold `&'a T` tied to the owner's lifetime. Prefer this whenever a single owner exists.
- **Escapes into a callback / FFI / async:** the value is handed to something that outlives the current scope (a libuv close callback, a C library, an async task). This is where naive `Drop` causes use-after-free — the local must **not** drop the value while the foreign side still holds it (e.g. `Box::leak` before an async `uv_close`, with the callback reclaiming it). Flag every such field explicitly; these are the highest-risk lifetimes.
- **Interior back-references / cycles:** self-referential structs and cycles don't map to plain borrows. Note them for special handling (`Weak<T>`, indices into a slab/arena, or `unsafe` with a documented invariant) rather than forcing a lifetime that can't be expressed.

## The mechanical-first tradeoff

You are not trying to produce beautiful idiomatic Rust in this pass. A mechanical port that mirrors the source's structure will use **more `unsafe` and more explicit lifetimes than idiomatic Rust would** — that's acceptable and expected. The goal is a correct, reviewable ownership model that behaves like the original. Reducing `unsafe` and refactoring toward idiomatic ownership is a *later* pass, done after the test suite is green and behavior is locked (see `port-to-rust-playbook`). Trying to do both at once means debugging two hard problems simultaneously.

## `LIFETIMES.tsv` shape

Keep it simple and machine-readable so translators can grep it. One row per interesting field, e.g.:

```
file<TAB>struct<TAB>field<TAB>ownership_model<TAB>lifetime<TAB>notes
src/parser.zig	Parser	nodes	arena	'a	does not escape parse(); tie to parser arena
src/http.zig	Subprocess	stdout_pipe	escapes-to-callback	'static	Box::leak before uv_close; on_pipe_close reclaims
src/cache.zig	Resolver	interned	Rc	-	shared across resolution passes; was refcounted in source
```

Only fields with non-trivial lifetimes need rows; owned-by-value fields are the default and don't. The value of the file is that every worker resolves an ownership question the same way the reviewed analysis decided, instead of guessing per file.
