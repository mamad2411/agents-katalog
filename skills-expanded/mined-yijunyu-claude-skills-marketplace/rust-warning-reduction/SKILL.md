---
name: rust-warning-reduction
description: Use when the user wants to analyse, count, or reduce Clippy warnings in a Rust project. Triggers on "reduce warnings", "fix clippy warnings", "identify high-frequency warnings", "warning density", "warnings per KLOC", "warn-identify", "warn-reduce", or references to Li et al. 2310.11738 methodology.
version: 1.0.0
---

# Rust Warning Reduction

Implements the Li et al. (arxiv:2310.11738) iterative workflow for reducing Clippy warning density in Rust projects. Warnings follow a Pareto distribution — the top-5 lint types typically account for >80% of all warnings.

**Target threshold:** 18 warnings/KLOC (below the 21/KLOC crates-io average baseline from the paper).

---

## Phase 1 — Identify: `warn-identify`

Use this phase when the user asks to **analyse** or **count** warnings.

### Steps

1. Determine `FOLDER` from arguments or use `.`; confirm `Cargo.toml` exists.

2. Run warning count analysis:
   ```bash
   rust-diagnostics --folder FOLDER --count
   ```
   Output (sorted ascending): per-type counts, total, LOC, warnings/KLOC.

3. Run quick density check:
   ```bash
   rust-diagnostics --folder FOLDER --warning-per-KLOC
   ```

4. Re-sort counts **descending** and present as a ranked Pareto table:
   ```
   Rank  Count  Cumul%  Warning Type                  Fixable?
      1    NNN    XX%   default_numeric_fallback        [auto]
      2    NNN    XX%   arithmetic_side_effects
      ...
   ```

5. Highlight:
   - Top-1 and top-5 lint share
   - Current density vs 18/KLOC target and 21/KLOC crates-io average
   - Mark machine-applicable lints as `[auto-fixable]`

### Output Format
```
## Warning Analysis: FOLDER
Density: X.XX warnings/KLOC  [TARGET: ≤18/KLOC | crates-io avg: 21/KLOC]

Rank  Count  Cumul%  Type                    Fixable?
   1    NNN    XX%   lint_name               [auto]
   2    NNN    XX%   lint_name
   ...

Top-1 coverage: XX% | Top-5 coverage: XX%
Status: ABOVE / BELOW 18/KLOC threshold
```

---

## Phase 2 — Reduce: `warn-reduce`

Use this phase when the user asks to **fix** or **eliminate** warnings.

### Loop

Repeat until density ≤ 18/KLOC:

1. Run `rust-diagnostics --folder FOLDER --count`, pick `TOP_LINT` (highest count).
2. Apply the paper's fix strategy for `TOP_LINT` (see Strategies below).
3. Verify: `cargo build` must pass before continuing.
4. Recount: `rust-diagnostics --folder FOLDER --warning-per-KLOC`

**At 18/KLOC** — stop and ask the user:
> "Warning density has reached **X.XX/KLOC** (≤ 18/KLOC threshold, Li et al. 2310.11738).
> Remaining warnings are long-tail types.
> **Continue with long-tail warning removals?** (Yes / No)"

---

## Fix Strategies (Li et al.)

### `default_numeric_fallback` — Auto-fix (paper: 3,842 → 0)
The paper changed Clippy's tag to MachineApplicable. Try:
```bash
cargo clippy --fix --allow-dirty --allow-staged -- -W clippy::default_numeric_fallback
```
If unavailable, add explicit type suffixes: `0` → `0_i32`, `1.0` → `1.0_f64`.

### `arithmetic_side_effects` — Wrapping rewrites (paper: 1,919 → 682)
Li et al.'s three TXL rules translated to sed:
```bash
# eqAddFix: i += N  →  i = i.wrapping_add(N)
find . -name '*.rs' | xargs sed -i -E \
  's/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\+=\s*([0-9]+)\b/\1 = \1.wrapping_add(\2)/g'
# eqSubFix: i -= N  →  i = i.wrapping_sub(N)
find . -name '*.rs' | xargs sed -i -E \
  's/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*-=\s*([0-9]+)\b/\1 = \1.wrapping_sub(\2)/g'
# eqDivFix: i /= N  →  i = i.wrapping_div(N)
find . -name '*.rs' | xargs sed -i -E \
  's/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\/=\s*([0-9]+)\b/\1 = \1.wrapping_div(\2)/g'
# AddExpFix: varId + N  →  varId.wrapping_add(N)
find . -name '*.rs' | xargs sed -i -E \
  's/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\+\s*([0-9]+)\b/\1.wrapping_add(\2)/g'
```
Always `cargo build` immediately; revert any rule that breaks compilation.

Alternatively, use `.saturating_add` / `checked_div` for domain-appropriate semantics.

### `undocumented_unsafe_blocks` — SAFETY comments (paper: 806 → 5)
```bash
find . -name '*.rs' | while read f; do
  perl -i -0pe \
    's/(?<!\/ SAFETY[^\n]*\n)(\s*unsafe\s*\{)/\n    \/\/ SAFETY: TODO - verify invariants\n\1/g' \
    "$f"
done
```
Then replace generic `TODO` text with specific invariant descriptions.

### `missing_debug_implementations` — Derive Debug (paper: 160 → 8)
```bash
find . -name '*.rs' | while read f; do
  perl -i -0pe \
    's/(\n(?!#\[derive[^\]]*Debug))(pub\s+(?:struct|enum)\s)/\1#[derive(Debug)]\2/g' \
    "$f"
done
```
If a type contains a non-Debug field, implement `Debug` manually.

### `missing_errors_doc` / `missing_panics_doc`
Append `# Errors` or `# Panics` sections to doc comments of affected functions. Locate
exact positions using clippy output, then edit file-by-file.

### `unwrap_used` / `expect_used`
- Replace `.unwrap()` with `.expect("invariant: <reason>")`, or
- Propagate with `?` if the function returns `Result`, or
- Use `#[allow(clippy::expect_used)]` with justification when no recovery is possible
  (e.g., poisoned mutex on a global).

### `manual_checked_ops`
Replace `if x > 0 { a / x }` patterns with `a.checked_div(x)`.

### `cast_precision_loss` / `as_conversions`
For KLOC-style percentage math, replace float casts with fixed-point integer arithmetic:
```rust
// Instead of: total as f64 * 1000.0 / loc as f64
// Use fixed-point (2 decimal places):
let scaled = total.saturating_mul(100_000).checked_div(loc).unwrap_or(0);
println!("{}.{:02}", scaled / 100, scaled % 100);
```

### Any other lint (generic fallback)
1. Try `cargo clippy --fix --allow-dirty --allow-staged -- -W clippy::<lint>`
2. Apply clippy's suggestion text at each warning location
3. Last resort: `#[allow(clippy::<lint>)] // <justification>` on the specific item

---

## Safety Rules
- `cargo build` must pass after every batch — never proceed past a compile error
- Revert with `git checkout -- <file>` if a rewrite breaks a file
- Never use `#[allow(clippy::all)]` — only targeted allows with justification
- Verify `wrapping_*` semantics are appropriate for your domain
