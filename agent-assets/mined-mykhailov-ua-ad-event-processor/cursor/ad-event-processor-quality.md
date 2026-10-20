---
description: Go receivers and verification honesty - always applied on every edit
alwaysApply: true
---

# Code Quality - Receivers

## Purpose

Always applied on every agent turn. Go method receivers and verification honesty. Comments: `comments.mdc`. File layout: `code-style.mdc`.

Agents must not invent environment, generated artifacts, or benchmark runs.

## Verification honesty (summary)

Before claiming done, see `anti-slop.mdc` (lie modes, CI gates, agent checklist, **Compile and test ritual ban**):

1. New symbols: default `read_lints`, `grep`, `gofmt -e` on edited paths — not `go build ./...` or package `go test -c` unless operator asked or you cite a named gate.
2. Hot path does not import cold fraud scoring.
3. Explain why scripts/tests changed.
4. Paste command + exit code for runs actually executed; if none, say **not run** and which lightweight check you used.
5. Add a holdout test that fails without the change when behavior is non-obvious (`testing.mdc`).

## Method receivers

### Default: 1-2 letters

Receiver is **1-2 lowercase letters** derived from the type name. Use the **same** receiver on every method of that type.

| Type | Receiver | Banned |
| :--- | :--- | :--- |
| `Service` | `s` | `service`, `svc`, `self` |
| `HTTPHandlers`, `*Handlers` | `h` | `handlers`, `ops`, `billHandlers` |
| `Store` | `st` | `store` |
| `Worker` | `w` | `worker`, `outboxWorker` |
| `Client` | `c` | `client` |
| `Registry` | `r` | `registry`, `modelRegistry` |

Derivation: first letter of the type; add a second when the type is compound (`HTTPHandlers` -> `h`, `LGBMScorer` -> `lg`). Never use the **full type name** or a **word-long** receiver (`campaigns`, `reconService`, `webhookHandler`).

### Collision in one file

Two method sets would share the same letter (e.g. two `Store` types) -> `bst` / `pst` or split files.

### Pointer vs value

- **Pointer receiver** when methods mutate state, call mutating deps, or struct is non-trivial size.
- **Value receiver** only for small immutable types or intentional copy semantics.

### Unused receiver

- Test/bench helpers must not take `*testing.B` unless they call `b`.
- If a method does not need the receiver, use a package function. No `_ = s` to silence unused receiver.

### Benchmark loops

Use `for b.Loop() { ... }` (Go 1.24+), not `for i := 0; i < b.N; i++`.

### CI gate

`bash scripts/ci/naming/legacy_naming.sh` rejects production method receivers with **3+ letter** names (`func \([a-z]{3,} `, excludes `*_test.go`).

## Related rules

`anti-slop.mdc`, `code-style.mdc`, `comments.mdc`, `naming.mdc`, `hot-path.mdc`.
