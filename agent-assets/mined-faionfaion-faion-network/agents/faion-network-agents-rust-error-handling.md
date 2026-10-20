# Rust Error Handling

## Summary

**One-sentence:** thiserror at crate level + anyhow at binary boundaries; one AppError per service; ? wraps via From; no unwrap/expect in non-test code.

**One-paragraph:** Use thiserror for library/crate-level typed error enums and anyhow at application binary boundaries. Service code defines one AppError per crate; every fallible function returns Result<T, E>; ? propagates via thiserror From conversions; unwrap/expect are banned outside tests and main glue. Output is a check-errors.sh CI script plus the AppError module.

**Ефективно для:**

- Standardising error types across a Rust service in one AppError enum.
- Replacing scattered Result<T, Box<dyn Error>> with typed errors at crate boundaries.
- Wiring anyhow at the binary boundary while keeping libraries cleanly typed.
- Adding a clippy-based CI gate that blocks unwrap/expect in non-test code.

## Applies If (ALL must hold)

- Rust crate or service authoring fallible APIs.
- Team is willing to ban unwrap/expect in production paths.
- CI can run cargo clippy with custom denies.
- Project mixes library crates + binary crate.

## Skip If (ANY kills it)

- Tiny CLI scripts where anyhow + bubble-up is enough end to end.
- Experimental code intentionally panicking on invariants.
- Embedded / no_std where thiserror and anyhow do not apply unchanged.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Crate / binary layout | Cargo.toml | team |
| Domain error list | md | team — every observable failure |
| CI runner | GitHub Actions / GitLab CI | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems/rust-backend/AGENTS.md` | AppError lives in the service layout |

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
| `design-app-error` | sonnet | Enum variant choices need judgement. |
| `write-check-errors-script` | sonnet | CI script benefits from sonnet. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/check-errors.sh` | CI script: fail PR if forbidden error patterns appear |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-error-handling.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[rust-backend]]
- [[rust-http-handlers]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/check-errors.sh`

```bash
# CI script: fail PR if forbidden error-handling patterns appear.
# Usage: bash scripts/check-errors.sh
set -euo pipefail

cargo clippy --all-targets --all-features -- \
  -D clippy::unwrap_used \
  -D clippy::expect_used \
  -D clippy::panic \
  -D clippy::todo \
  -D clippy::unimplemented \
  -W clippy::missing_errors_doc

# Forbid Box<dyn Error> in public function signatures
if grep -rn 'pub\s\+fn\b.*Box<dyn\s\+\(std::error::\)\?Error' src/; then
  echo "ERROR: Box<dyn Error> in public API — use a typed error enum"
  exit 1
fi

echo "Error handling checks passed."
```
