# Rust Ownership Model

## Summary

**One-sentence:** Ownership / borrowing / lifetimes rules: single owner, & vs &mut, no clone-as-shortcut, no Rc<RefCell> in multi-thread, audit clone() in CI.

**One-paragraph:** Rust's ownership system enforces memory safety without GC: each value has one owner, borrows are either multiple shared (&T) or one exclusive (&mut T), and lifetimes express reference validity across scope boundaries. Clone() is forbidden as a shortcut around the borrow checker; Rc<RefCell> is forbidden across thread boundaries (use Arc<Mutex> / Arc<RwLock>). Output is an audit-clones.sh script + per-file annotations on hot paths.

**Ефективно для:**

- Auditing a crate for gratuitous .clone() that papers over borrow issues.
- Reviewing async code for incorrect Send / Sync boundaries.
- Replacing Rc<RefCell<T>> with Arc<RwLock<T>> when crossing tokio threads.
- Teaching new contributors the borrow checker without one-page tutorials.

## Applies If (ALL must hold)

- Rust service or library with hot paths sensitive to memory allocation.
- Codebase already has > 5 .clone() calls per 100 lines (smell signal).
- Async code crosses spawn boundaries with shared state.
- Team is willing to enforce ownership rules in code review.

## Skip If (ANY kills it)

- Prototype code where compile-now ergonomics matter more than allocations.
- Library is pure value-type computation with no shared mutable state.
- Embedded code with no heap (clone simply does not apply).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hot-path list | md | team |
| Profiler output | flamegraph / pprof | ops |
| CI runner | config | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-clones` | sonnet | Each clone needs judgement: required, removable, or fix the design. |
| `rewrite-hot-paths` | sonnet | Borrowing rewrites need design judgement. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-clones.sh` | Surface gratuitous clone() calls for review |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-ownership.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[rust-error-handling]]
- [[rust-backend]]
- [[rust-project-structure]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/audit-clones.sh`

```bash
# Surface gratuitous clone() calls in a crate for review.
# Usage: bash scripts/audit-clones.sh
set -euo pipefail

cargo clippy --all-targets -- \
  -W clippy::needless_clone \
  -W clippy::redundant_clone \
  -W clippy::clone_on_copy \
  -W clippy::implicit_clone 2>&1 | tee target/clippy-clones.txt

echo "--- Clone call count in src/ ---"
grep -rn '\.clone()\|\.to_string()\|\.to_owned()' src/ | wc -l

echo "--- clippy-clones.txt written to target/ ---"
```
