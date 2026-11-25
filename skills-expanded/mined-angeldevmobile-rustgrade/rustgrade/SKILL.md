---
name: rustgrade
description: Systems-level Rust review and the defaults a senior Rust engineer writes by. Use when writing, reviewing, refactoring or optimizing Rust code, when asked to audit or grade a Rust crate, or when Rust code panics, clones, allocates or locks more than it should. Grounds every review in the rustgrade CLI's deterministic findings when it is installed.
---

# rustgrade

Two jobs: **write** Rust with systems-level defaults, and **review** Rust grounded
in the `rustgrade` scanner instead of vibes.

## Defaults when writing Rust

- **Borrow before you clone.** Take `&str`, `&[T]`, `&Path`, not `&String`,
  `&Vec<T>`, `&PathBuf`. Clone only to cross an ownership boundary.
- **No `.unwrap()` outside tests.** Propagate with `?`. Use
  `.expect("why this cannot fail")` only for a real invariant.
- **Libraries return typed errors** (a `thiserror` enum). Binaries may use
  `anyhow` with `.context(..)`.
- **Every `unsafe` block has a `// SAFETY:` comment** naming the invariant that
  makes it sound; every `unsafe fn` has a `# Safety` doc section.
- **Concurrency:** prefer one owner plus a **bounded** channel over
  `Arc<Mutex<_>>`. Never hold a std / parking_lot guard across `.await`.
- **No per-iteration allocation:** hoist buffers out of loops and `.clear()`
  them; use `with_capacity` when the size is known.
- **Measure before claiming speed** (criterion, flamegraph, dhat, `cargo asm`).

## Review workflow

1. **Check the CLI:** `rustgrade --version`. If it is missing, do a manual
   review (last section) and tell the user `cargo install rustgrade` makes
   reviews deterministic.
2. **Scan:** `rustgrade scan [path] --format json`. It honors `.gitignore` and
   `rustgrade.toml`. Exit code `2` is a tool error: show stderr, don't guess.
3. **Read the JSON** (schema below) and group findings by `category`.
4. **Load only the references for categories that came back:**

   | Category | Reference |
   |---|---|
   | `errors` | [references/errors.md](references/errors.md) |
   | `performance` | [references/performance.md](references/performance.md) |
   | `concurrency` | [references/concurrency.md](references/concurrency.md) |
   | `unsafe` | [references/unsafe.md](references/unsafe.md) |
   | `ownership`, `api-design` | [references/ownership.md](references/ownership.md) |
   | grading (`/rustgrade:audit`) | [references/rubric.md](references/rubric.md) |

5. **Judgment pass**, for what a syntax scanner cannot see: API shape, error
   taxonomy, whether a clone is actually cheap (`Arc`, `Copy`), lock
   granularity, algorithmic complexity, missing tests for risky code.
6. **Verify heuristic findings before fixing them** (see Limitations).
7. **Report** (format below), then offer fixes, lowest risk first. After
   fixing, rescan and run `cargo test` to confirm.

## JSON output (`"schema": 1`)

```json
{
  "schema": 1,
  "files_scanned": 12,
  "findings": [{
    "rule": "unwrap-outside-tests", "severity": "high", "category": "errors",
    "message": "`.unwrap()` panics on the error path",
    "span": { "file": "src/lib.rs", "line": 6, "column": 43, "end_line": 6, "end_column": 49 },
    "help": "propagate with `?`, handle the error, or document why it cannot fail"
  }],
  "suppressed": [{ "rule": "...", "...": "same fields as a finding", "reason": "validated in new()" }]
}
```

Severities, highest first: `critical`, `high`, `medium`, `low`, `info`.
Findings arrive sorted by severity, then location.

## Rules

| ID | Category | Flags |
|---|---|---|
| `undocumented-unsafe` | unsafe | `unsafe` block or impl without `// SAFETY:` |
| `unwrap-outside-tests` | errors | `.unwrap()` (high) / `.expect()` (medium) outside tests; `low` with a comment saying why it cannot fail, or on a lock result |
| `lock-across-await` | concurrency | sync lock guard alive at an `.await` |
| `unbounded-channel` | concurrency | `unbounded_channel()`, `unbounded()`, `std::sync::mpsc::channel()` |
| `anyhow-in-lib-api` | errors | public library fn returning `anyhow` errors |
| `clone-in-loop` | performance | `.clone()` / `.to_owned()` per iteration |
| `alloc-in-loop` | performance | `Vec::new`, `format!`, `.to_string()`, ... per iteration |
| `ref-owned-param` | api-design | `&String`, `&Vec<T>`, `&Box<T>`, `&PathBuf` params |
| `invalid-suppression`, `unused-suppression` | meta | malformed or stale `rustgrade: allow` comments |

`rustgrade rules` lists them. `rustgrade rules --explain <id>` prints a rule's
rationale with before/after code (add `--format json` to parse it); use it
before arguing with a finding. `--min-severity` filters findings;
`--fail-on <severity>` exits `1` when any finding reaches that severity.

## Grading

`rustgrade audit [path] --format json` runs the scanner, clippy pedantic and
`cargo test`, and returns an A–F grade computed with
[references/rubric.md](references/rubric.md). Treat its grade as authoritative;
your judgment findings are reported next to it, not mixed into it. Flags:
`--no-clippy`, `--no-tests`, `--fail-on <grade|severity>`.

## Commands

Three commands: `audit [path]` (graded review, see
[references/rubric.md](references/rubric.md)), `harden [path]` (survive hostile
input, proving each fix with a test that failed first) and `hot-path <fn>`
(benchmark-driven optimization). `rustgrade install` adds them as `/audit`,
`/harden` and `/hot-path` in Claude Code, Cursor, Gemini CLI, Copilot (VS Code)
and Windsurf; the Claude Code plugin names them `/rustgrade:audit` and so on.
Codex has no command files: when asked for one of these, follow the same steps
from this skill.

## Limitations: verify before you fix

The scanner reads syntax (`syn`), not types:

- `clone-in-loop` cannot tell a cheap `Arc` / `Rc` / `Copy` clone from a deep
  one. `Arc::clone(&x)` is never flagged; prefer it for refcount bumps.
- `lock-across-await` treats a `.lock()` / `.read()` / `.write()` that is not
  directly awaited as a synchronous lock. A guard moved into a function other
  than `drop` still counts as alive.
- Macro bodies are not analyzed: `println!("{}", x.unwrap())` is missed.
- `anyhow-in-lib-api` decides lib vs bin from the layout (`src/lib.rs`,
  `src/main.rs`, `src/bin/`).
- Loop rules don't count closures passed to iterator adapters
  (`.map(|x| x.clone())`), and look at one function at a time: a function that
  allocates, called from a loop, is not flagged at the call site.

A false positive is fixed with a suppression, never by contorting correct code.

## Suppressions

```rust
// rustgrade: allow(unbounded-channel) shutdown signal, at most one message per worker
let (stop_tx, stop_rx) = std::sync::mpsc::channel::<()>();

let id = ids.next().expect("non-empty"); // rustgrade: allow(unwrap-outside-tests) checked by caller
```

- The comment goes at the end of the finding's line, or on the line above the
  statement, which it covers to its `;` or the `{` of its block (other comments
  and attributes in between are fine; a blank line breaks it).
- The **reason is mandatory**. Suppress only when the code is right and the
  scanner cannot see why. Never suppress to make CI pass.
- `invalid-suppression` / `unused-suppression` findings mean malformed or stale
  annotations: fix or delete them.
- Project-wide settings live in `rustgrade.toml`:
  `allow = ["rule-id"]`, `exclude = ["generated/"]`, `hot = ["src/engine/"]`,
  `min_severity = "low"`.

## Report format

One line per finding, most severe first:

```
**[high]** src/server.rs:13 · lock-across-await — std guard `cache` is held while `fetch().await` runs → scope it in a block, or switch to `tokio::sync::Mutex`
```

- Lead with critical and high. Collapse lows into one summary line.
- Name the concrete fix, not the category. Include a code snippet for anything
  non-obvious.
- Do not pad a short report with nits. If the crate is clean, say so.
- Mention suppressed findings only if a reason looks wrong.

## Manual review (no CLI)

Apply the same rules by reading the code. Useful starting points:

```bash
rg -n '\.unwrap\(\)|\.expect\(' --type rust
rg -n 'unsafe' --type rust
rg -n 'unbounded|mpsc::channel\(\)' --type rust
rg -n '&String|&Vec<|&PathBuf|&Box<' --type rust
rg -n 'anyhow::' --type rust
```

Then read loops in hot code for clones and allocations, and every `async fn`
that touches a `Mutex`.
