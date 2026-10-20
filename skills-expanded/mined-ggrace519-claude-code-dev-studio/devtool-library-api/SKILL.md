---
name: devtool-library-api
description: Library API specialist. Owns public API design at the code level: types, signatures, error types, nullability, generics, async surface. Auto-invoked when designing or changing a public library surface.
---

# DevTool Library API

Library APIs get embedded in a million call sites; a sloppy signature becomes
permanent. The types, error contract, and cancellation semantics *are* the product.

## When to reach for this

- Designing or changing any exported function, type, or class signature
- Defining the error hierarchy consumers will branch on
- Shaping the async surface: promises/tasks, cancellation, timeouts
- Reviewing a diff for accidental breaking changes to the public surface

## Principles

1. **Types first.** Write the signature (with defaults and doc comment) before the
   implementation — the signature is the spec, and it's cheaper to argue about.
2. **Typed errors with stable codes.** Consumers branch programmatically: a sealed
   error hierarchy or discriminated union with a string `code` field, plus `cause`
   chaining. Message text is for humans and may change; codes may not.
3. **Cancellation everywhere async.** Every async entry point accepts the platform
   idiom — `AbortSignal` (JS), `CancellationToken` (.NET), `context.Context` as first
   param (Go), cooperative `CancelledError` (Python asyncio). Retrofitting it later
   is a breaking change at every call site.
4. **Options objects scale; positionals don't.** At 3+ parameters, or any boolean
   parameter, switch to a named options object/struct — `fn(input, { retries: 3 })`
   survives growth; `fn(input, 3, true, false)` doesn't.
5. **Draw the public/internal line explicitly.** Explicit exports / `__all__` /
   `internal` visibility / `#[doc(hidden)]`. Internal can break daily; public breaks
   only with a major version. If you didn't mark it, consumers own it.
6. **Make breaking-change detection mechanical.** Type-level diff in CI — api-extractor
   (TS), cargo-semver-checks (Rust), apidiff (Go), Revapi (Java) — so a major-version
   bump is a tool's verdict, not a reviewer's memory.

## Surface design checklist

- [ ] Signature reviewed before implementation; defaults chosen deliberately
- [ ] No boolean positional parameters; options object at 3+ params
- [ ] Errors are typed, carry a stable `code`, and chain `cause`
- [ ] Every async API accepts cancellation and documents timeout behavior
- [ ] Nullability/optionality explicit in types (no implicit-null returns)
- [ ] Inputs accept wide types, outputs return narrow ones
      (e.g. accept `Iterable`, return `Array`)
- [ ] Public surface enumerated (exports map / `__all__`) — nothing public by accident
- [ ] API diff tool wired into CI; failures gate the merge
- [ ] Deprecations annotated with replacement + removal version, kept ≥1 minor release

## Pitfalls

- Exposing internal types in a public signature — they're now public forever
- Changing a default value and calling it non-breaking (it changes behavior at every
  existing call site)
- Throwing strings or a single generic `Error` so consumers parse message text
- Async APIs that swallow cancellation or keep running after the token fires
- Widening a return type or narrowing a parameter type in a minor release —
  both break callers in typed languages
- "Just one more overload" instead of an options object — overload sets become
  unreadable past three

---
*Related: `devtool-cli-ux` (when a CLI fronts this surface), `devtool-docgen`
(reference generated from these signatures), `devtool-packaging` (what actually
ships in the artifact), `api-design` (HTTP/wire contracts, distinct from in-process
APIs) · domain agent: `devtool-architect` (surface taxonomy, semver policy) ·
output/ADR format: `playbook-conventions`*
