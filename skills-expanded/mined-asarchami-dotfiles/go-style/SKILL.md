---
name: go-style
description: "Go code style and naming — write and review clear Go: MixedCaps identifiers, flat happy paths, short focused functions, intentful declarations, error and enum conventions. Use when writing Go code, reviewing style or naming, configuring style linters, or establishing project standards."
license: MIT
---

# Go Style

**Leading word: clear.** Style rules that require human judgment — linters handle formatting, this skill handles clarity. The discipline: every identifier, branch, and declaration is chosen so the code reads its intent at a glance. "Clear is better than clever." — Go Proverbs.

## Steps — write clear code

1. **Name identifiers by scope and convention.** MixedCaps, never underscores (Go's export mechanism and tooling depend on it); name length matches scope (`i` in a 3-line loop, descriptive at package level); avoid stuttering — the package name is already at the call site (`http.Client`, not `http.HTTPClient`); no `Get` prefix on getters (`user.Name()`, keep `Is`/`Has`/`Can` for booleans); acronyms all caps or all lower (`URL`, `HTTPServer`, `xmlParser`).

   *Done when: every identifier on the changed lines is MixedCaps, correctly scoped, stutter-free, and convention-matching.*

2. **Keep the happy path flat.** Return early on errors and edge cases; drop `else` after `return`/`break`/`continue` (default-then-override); use `switch` over if-else chains when comparing the same value; extract complex `if` conditions (3+ operands) into named booleans.

   *Done when: no happy-path line is nested under an error branch, no else-if chain compares one value, and no bare 3+ operand condition remains.*

3. **Shape signatures for one job.** `context.Context` first, then inputs, then outputs; ≤4 parameters — an options struct beyond that; break long calls at semantic boundaries, one argument per line.

   *Done when: every function does one job and takes ≤4 params or an options struct.*

4. **Declare with intent.** `:=` for non-zero values, `var` for zero-value init; slices and maps always initialized, never nil (nil maps panic on write; nil slices serialize to `null`); named fields in composite literals so positional order can't break on type change.

   *Done when: no nil map is written, no nil slice is serialized, and no new positional literal or zero-value `:=` is added.*

5. **Write errors, enums, and booleans that read clearly.** Error strings fully lowercase with no trailing punctuation, acronyms too (`"invalid message id"`); sentinel errors `Err`-prefixed, error types `Error`-suffixed (`ErrNotFound`, `PathError`); enum zero value is an `Unknown` sentinel, never a real state; unexported booleans use `is`/`has`/`can`, exported getters keep the prefix (`IsConnected()`); `WithContext` is the standard context suffix.

   *Done when: every new error, enum, and boolean follows these conventions, each with a reason.*

6. **Let the machine enforce the mechanical 90%.** gofmt/gofumpt, goimports, gocritic, revive, wsl_v5, predeclared, misspell, errname automate most rules; when a rule must be ignored, say why in a comment on the code.

   *Done when: style linters pass and every ignored rule carries a justification comment.*

## Steps — review style

1. **Scan by concern, not by file.** Walk control flow, function design, variable declarations, string handling, and code organization in turn; on a large codebase, run up to 5 parallel sub-agents, one concern each.

   *Done when: each concern is judged against the code-style and naming references, not just the diff.*

2. **Judge against the references.** Match each questionable identifier, signature, and literal against the rationale in `naming.md` and `functions-methods.md` before flagging it; say why the code is unclear, not just "rename it".

   *Done when: every flagged item names the rule it violates and why clarity suffers.*

## Reference

- **[Code Style Guide](./references/code-style.md)** — full style rules: line breaking, declarations, value vs pointer params, string handling, type conversions, code organization, philosophy
- **[Naming Conventions](./references/naming.md)** — full naming rules with rationale: stuttering, constructors, booleans, error casing, enums, subtest names
- [Packages, Files & Import Aliasing](./references/packages-files.md)
- [Variables, Booleans, Receivers & Acronyms](./references/identifiers.md)
- [Functions, Methods & Options](./references/functions-methods.md)
- [Types, Constants & Errors](./references/types-errors.md)
- [Test Naming](./references/testing.md)
- [Complex Conditions & Init Scope details](./references/details.md)

## Watch for

| Mistake | Fix |
| --- | --- |
| `ALL_CAPS` constants | Go reserves casing for visibility — use MixedCaps (`MaxRetries`) |
| `GetName()` getter | `user.Name()`; keep `Is`/`Has`/`Can` for booleans |
| `Url`, `Http`, `Json` | All caps or all lower — `URL`, `HTTPServer` |
| `this`/`self` receiver | 1-2 letter abbreviation, consistent per type (`s` for `Server`) |
| `util`, `helper` packages | Name describes content, not a category |
| `http.HTTPClient` stutter | `http.Client` |
| `user.NewUser()` | `user.New()` for a single primary type |
| `connected bool` | `isConnected` reads as a question |
| `"invalid message ID"` | Lowercase incl. acronyms — `"invalid message id"` |
| `StatusReady` at iota 0 | `StatusUnknown` at 0 catches uninitialized values |
| `"not found"` | Sentinel errors carry the package prefix — `"mypackage: not found"` |
| `snake_case` identifiers | `mixedCaps` — underscores conflict with Go conventions |
| Naming constants by value | Roles survive change, values don't — `DefaultPort` not `Port8080` |
| `FetchCtx()` | `WithContext` is the standard suffix — `FetchWithContext()` |

## Cross-references

- → See `go-structs-interfaces` for receiver design and value vs pointer receivers
- → See `go-patterns` for constructors, functional options, and design patterns
- → See `go-lint` for automated enforcement
