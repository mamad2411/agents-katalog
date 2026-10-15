---
name: windows-compat
description: >-
  Audit and harden this Rust repo (code-graph-mcp) for Windows correctness:
  path-spelling drift between producers, the 32,767-char command-line cap,
  index-key mismatches, and path predicates that assume one ecosystem's layout.
  Use whenever touching code that builds, compares, prints, or stores a
  filesystem path; that spawns a process with a variable number of arguments
  (rg, git); that matches an executable name; or that classifies files by path
  shape — and whenever triaging a bug that reproduces only on Windows,
  reviewing a diff that touches path handling, or adding a predicate that has a
  SQL mirror. Reach for it even when the change looks small and nobody
  mentioned Windows: every defect in its catalogue shipped past a green CI
  matrix that already included windows-latest.
---

# Windows compatibility (code-graph-mcp)

Three defects reached a Windows user from **one** root cause: two spellings of
the same path compared unequal. CI already ran `windows-latest` and caught none
of them, because nothing asserted on path spellings at all. Closing that gap is
what this skill is for.

## The invariant everything hangs off

`indexer::merkle::normalize_rel_path` stores every indexed path as a
**`/`-separated relative path**, rewriting separators only under
`#[cfg(windows)]`. So any path that becomes a lookup key, a dedup key, or
stdout must land in *exactly* that spelling.

Almost every defect below is one producer handing over a different spelling of
the same file. The producer table and the full catalogue are in
[references/failure-modes.md](references/failure-modes.md) — read it before
changing path-handling code. It is short and every entry is a real defect with
its shipped fix.

## The doctrine: platform is a parameter, not a `cfg!`

This is the single rule that makes everything else testable.

```rust
// NO — the Windows branch only runs on Windows, so the Linux and macOS legs
// prove nothing, and a Windows-only CI failure is expensive to debug.
fn normalize(path: &str) -> String {
    if cfg!(windows) { path.replace('\\', "/") } else { path.into() }
}

// YES — one thin cfg! entry point, all logic in a function taking the platform.
fn normalize(path: &str) -> String {
    normalize_on(path, cfg!(windows))
}
fn normalize_on(path: &str, backslash_is_sep: bool) -> String { ... }
```

Then assert **both** values from any platform:

```rust
assert_eq!(normalize_on(r"src\a.rs", true), "src/a.rs");   // Windows behaviour
assert_eq!(normalize_on(r"src\a.rs", false), r"src\a.rs"); // `\` is a legal Unix filename char
```

Live examples: `merkle.rs::normalize_rel_str_on` (the crate's single
separator-rewriting implementation — everything else delegates to it),
`cli.rs::normalize_path_display_on`, `cli.rs::relativize_path_on`.

Skip `dunce` / `path-slash` here. They do the right thing but decide internally
on `cfg(windows)`, forfeiting exactly the property that makes the Linux leg
useful.

## Before trusting a green suite, classify the fix

Where the correct Unix behaviour is the *identity* transform, no assertion can
go red on a Unix leg — reverting the fix changes nothing observable there. That
is not a weak test, it is a Windows-observable fix. Handle it by asserting the
**relation** (`produced key == merkle::normalize_rel_path(same input)`), so the
`windows-latest` leg carries a real regression test, and by making sure the
decision logic it delegates to is `_on`-tested, which every leg does run. D6 in
the reference is the worked example.

## Workflow

### 1. Scan

```bash
bash docs/skills/windows-compat/scripts/audit.sh src
```

Advisory, not a gate: exit 1 means "read these", not "these are bugs". The
patterns are deliberately tuned so a hit is worth a human read —
`worktree_main_root` is a *correct* site it flags, and it is worth reading as
the reference for the length-preserving pattern.

### 2. For each hit, answer three questions

1. **Where does this path come from, and where does it go?** Check the producer
   table in the reference. A path from `git` (always `/`) compared against one
   from `rg` (native separators) is defect D1.
2. **Does it become an index lookup key or reach stdout?** Then it must match
   `merkle::normalize_rel_path`'s spelling exactly. Rather than hand-tracing
   callers, use this repo's own index — `code-graph-mcp impact <fn>` answers
   "what does this reach" in one call, and it sees the whole repo rather than
   the files you happen to have open.
3. **Is it an argv operand that can grow with repo size?** Then bound it in
   **bytes** and batch. A count cap is not a length bound (D3).

### 3. Fix behind a platform parameter, then test both values

New path logic goes in a `_on(…, windows: bool)` function per the doctrine
above. A regression test that only runs on Windows is worth far less than the
same assertion running on every leg.

### 4. Prove the test has teeth

A passing test proves nothing until its failure has been observed. Break the fix
deliberately, watch the new test go red, restore, watch it pass:

```bash
# e.g. make normalize_path_display_on ignore its flag, then:
cargo test --lib normalize_path_display_leaves_unix_backslash
```

Mutate the **whole condition**, not one operand — `if false && a || b` still
matches via `b`, because `&&` binds tighter than `||`. A mutation that leaves
the test green has told you nothing about the test.

This step was decisive twice on the shipped fixes: the first `affected` test
passed even with the new classification legs disabled (an unrelated leg matched
it), and once mutated correctly, the output reproduced the bug report
symptom-for-symptom.

## When changing a path predicate that has mirrors

**Enumerate the mirrors before you edit. Do not trust a count — including this
one.** `domain::is_test_path` is reimplemented across several sites in two
languages and a SQL dialect; `domain.rs` carries a "Five sites must agree" note,
and the inventory doc it points at (`feedback_test_classifier_dual_sources.md`)
no longer exists, so the code comments are now the only record and they may
themselves be stale.

Find them yourself, every time:

```bash
# Search the WHOLE repo. Scoping this to src/ is how you miss mirrors — the
# Python ports under scripts/ and the JS one under claude-plugin/ are real
# must-agree sites, and an earlier draft of this command scoped away the former.
rg -l 'is_test_path|isTestPath|is_test_node_sql|TEST_SOURCE_FILTER'
```

Ports often announce themselves in a docstring (`"""Port of src/domain.rs..."""`),
so also try `rg -l 'Port of src/domain'` and the equivalent for whatever
predicate you are changing.

Then separate **consumers** (call the predicate — nothing to do) from
**reimplementations** (their own copy of the rules — these are the mirrors).
`code-graph-mcp callgraph is_test_path` settles which is which faster than
reading each file.

**Then decide per site, because some divergence is deliberate.** At the time of
writing: the Rust and SQL legs of `is_test_node_sql` must agree, but
`PROD_SOURCE_FILTER_AND` / `TEST_SOURCE_FILTER_OR` are documented as
intentionally narrower, and the closure in
`indexer::pipeline::resolve::refine_ambiguous_targets` is deliberately broader.
Blindly unifying all of them is its own bug. Read each site's comment first; if
it claims to be intentionally different, leave it and say so in your summary.

The one that is easiest to miss sits outside `src/` entirely:
`claude-plugin/scripts/pr-impact-comment.js::isTestPath`, whose test is named
`isTestPath mirrors domain::is_test_path patterns` — an explicit parity contract
that a Rust-only change silently breaks.

For the legs that must agree, generate both from the shared constants
(`PASCAL_TEST_EXTS` / `PASCAL_TEST_STEMS` / `INFIX_TEST_EXTS`) rather than
transcribing, and extend `test_is_test_node_sql_matches_rust`, which runs the
emitted SQL against in-memory SQLite to prove agreement. Watch GLOB
(case-sensitive, `_` literal) vs LIKE (case-insensitive, `_` wildcard) and pick
per leg to match the Rust semantics. Add near-miss negatives, not just
positives — `src/latest.cs`, `src/protest/api.cs` and `src/testing/api.cs` must
stay classified as production code.

## Verifying without a Windows machine

- Drive both branches of every `_on` function from unit tests (works anywhere).
- Drive size/limit logic through a test seam instead of materializing the real
  limit: `CODE_GRAPH_RG_ARGV_BUDGET` makes the 32 KB batching path reachable
  with a 40-byte budget (`tests/cli_e2e.rs::test_cli_grep_supplement_batches_across_argv_budget`).
- Leave genuinely OS-gated assertions to the `windows-latest` leg and keep them
  few — anything expressible as pure string logic belongs in an `_on` test.

## Done when

- Every audit hit is either fixed or consciously accepted as a correct site.
- New path logic takes the platform as a parameter, with both values asserted.
- At least one mutation was observed going red.
- Predicates with a SQL mirror were regenerated from shared constants, with
  near-miss negatives added.
