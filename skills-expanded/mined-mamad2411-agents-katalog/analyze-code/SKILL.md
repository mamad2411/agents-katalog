---
name: analyze-code
description: Code-level quality analysis. Use when asked to review code for smells, security issues, implementation quality, or test coverage.
---

# Code Analysis (Zoom In)

Perform a code-level quality analysis of this project. Follow the procedural workflow
below; use the rubric sections as reference when interpreting findings.

## Ground Rules

- Assessment only: no code changes, pushes, workflow/release triggers
- No side effects: no installs/config edits/machine mutation; no paid API calls
  (mock or skip); dry-run or mock anything that publishes/deploys; verify commands
  exist and are spelled correctly, not their effect
- Reproduce before reporting: every finding needs repro or concrete trace, a
  file:line reference, and a concrete fix
- Probe validation gaps: construct an invalid state locally, check tooling/CI catches
  it

## Repo Shape

Emphasize different risk categories depending on what the repo is:

| Shape | Emphasize |
| --- | --- |
| App/service | authZ per route (ownership on account-scoped routes), auth token lifecycle (expiry/single-use/timing/enumeration), quota races, SSRF in fetchers/ingestion, prompt injection from untrusted content reaching an LLM, SQLi, CORS/rate limits |
| CI library/actions | script injection (untrusted context in `run:`), SHA pinning, egress, permission ceilings — a bad action ships unsafe CI to every consumer |
| Content/docs site | XSS (`set:html` / `innerHTML`, export paths), command validity in guides, currency of claims, link rot |
| Package index/tap | artifact checksum re-verification vs upstream, update-automation payload trust (dispatch payload -> file rewrite = RCE surface), version freshness |

## Usage

When asked to analyze code quality:

### 1. Static analysis

Run project-appropriate static checks (skip tools not present in the repo):

```bash
uv run lintro chk          # Python/JS/TS/YAML/etc. when lintro is configured
bunx tsc --noEmit          # TypeScript projects with tsconfig
cargo clippy -- -D warnings  # Rust projects
semgrep --config=auto .    # Security/quality patterns (install if missing)
```

Record every finding with file path and line number.

### 2. Security scan

Search for common vulnerability patterns:

```bash
# Hardcoded secrets (adjust paths as needed)
rg -n '(api[_-]?key|secret|password|token)\s*=\s*["\x27][^"\x27]+["\x27]' --glob '!*.{lock,sum}'

# Dangerous subprocess usage
rg -n 'shell\s*=\s*True' --type py

# SQL injection risk (string interpolation in queries)
rg -n '(execute|query)\s*\(\s*f["\x27]|\.format\s*\(' --type py

# Dependency vulnerabilities
uv run pip-audit           # Python with uv (pip-audit in dev deps)
bun audit                    # JavaScript/TypeScript with bun
```

Cross-check results against the Security Best Practices rubric below.

### 3. Workflow & supply-chain security

Search for CI/CD and supply-chain risk patterns:

```bash
# Untrusted GitHub context interpolated directly into a run: block
rg -n '\$\{\{\s*github\.(event|head_ref)' .github/workflows/ .github/actions/ action.yml action.yaml

# pull_request_target usage (runs with write-scoped secrets against untrusted code)
rg -n 'pull_request_target' .github/workflows/ .github/actions/ action.yml action.yaml

# Actions pinned to a tag/branch instead of a commit SHA
rg -n -P 'uses:\s*[^@]+@(?![0-9a-fA-F]{40}\b)' .github/workflows/ .github/actions/ action.yml action.yaml

# Write-scoped token permissions
rg -n 'permissions:' -A 3 .github/workflows/ .github/actions/ action.yml action.yaml
```

Prose checks (no single command catches these — inspect manually): injection via PR
titles/branches/bodies flowing into a shell step, cache poisoning between workflow
runs, and whether release automation can be triggered from a non-release commit or
by an untrusted actor.

### 4. Code smell detection

Use ripgrep and manual inspection for structural issues:

```bash
# Long functions (heuristic: functions with many lines — inspect top hits)
rg -n -U '^\s*(@\w+.*\n\s*)*(async\s+)?def\s+\w+' -t py
rg -n '^\s*(pub(\([^)]*\))?\s+)?(async\s+)?(unsafe\s+)?(const\s+)?fn\s+\w+' -t rust
rg -n '^\s*(export\s+)?(default\s+)?(async\s+)?function\s+\w+' -t ts -t js
rg -n '^\s*(export\s+)?(const|let|var)\s+\w+\s*=\s*(async\s+)?\(' -t ts -t js

# Dead code / unused imports (lint tools often catch these; supplement with:)
rg -n '# (noqa|type: ignore|allow dead_code)'  # existing suppressions worth reviewing
rg -n 'TODO|FIXME|HACK|XXX'                    # deferred cleanup

# Cross-file duplication (same pattern in 3+ files with minor variations)
bunx jscpd --min-tokens 50 .       # or replace `.` with the repo's actual source roots
```

Evaluate hits against the Code Smells rubric (long methods, dead code, duplication,
magic numbers, etc.). Duplication findings must name the files involved, the shared
pattern, and a suggested extraction point.

### 5. Rate and report findings

Lead with a TLDR verdict (one or two sentences: is this codebase in good shape,
needs attention, or has critical issues).

For each issue, assign severity:

- **Critical** — security vulnerabilities, data loss risk, broken auth, exploitable injection
- **Should Fix** — bugs, missing error handling, significant smells, vulnerable dependencies
- **Nice to Have** — style, minor duplication, documentation gaps

Include file paths, line numbers, concrete repro/trace evidence, and a concrete fix
suggestion for each finding. End
with a prioritized fix list ordered by impact. When this analysis runs as part of a
full audit alongside `analyze-project`, merge into that skill's single fix list
instead of reporting a separate one.

Cadence: run codebase-wide every ~20 PRs or monthly; prioritize cross-file duplication,
then idiom upgrades, then style polish; file findings via the `issue` skill.

---

## Reference — Implementation Quality

- Best practices adherence for the language/framework used
- Scalability and performance considerations
- Error handling—are failures handled gracefully and consistently?
- Resource management—are connections, file handles, streams properly closed?
- Concurrency/async correctness—race conditions, deadlocks, proper cleanup
- Type safety—is the type system leveraged well or worked around with `any`/casts?
- Dependency health—outdated, redundant, or vulnerable dependencies
- Hand-rolled utilities that duplicate existing stdlib/crate/package functionality
- Logging/observability—can issues be diagnosed in production?

## Reference — Code Smells

- Long methods/functions that do too much
- God classes or modules with too many responsibilities
- Feature envy—code that uses another module's data more than its own
- Primitive obsession—overuse of primitives instead of domain types
- Shotgun surgery—a single change requiring edits across many files
- Dead code, unreachable branches, or unused imports/variables
- Deeply nested conditionals or callbacks
- Magic numbers and hardcoded strings that should be constants
- Duplicated logic that violates DRY
- Inappropriate intimacy—modules tightly coupled to each other's internals

### LLM-Typical Idiomatic Smells

Code that compiles and passes linters but uses generic cross-language patterns instead
of the target language's constructs:

- Manual loops where built-ins exist (`any()`, `all()`, `.find()`, `.get()`,
  `.collect()`)
- Defensive flag-and-break variables instead of expression-based flow
- Over-cloning or owned `String` parameters to dodge borrow reasoning (Rust)
- `os.path` mixed with `pathlib` in one codebase (Python)
- Hand-rolled utilities duplicating stdlib/ecosystem solutions
- Copy-pasted logic across 3+ files that should be a shared helper
- Nested if/else unwrapping where dedicated syntax exists (`let-else`, `?`, `.ok_or()`)

When filing idiom findings, name the preferred replacement directly — language-standard
skills cover general style but not every smell above. Examples:

- Manual loop → `any()` / `all()` (Python), `.find()` / `.some()` (JS/TS), iterator
  chains with `.collect()` (Rust)
- `os.path` vs `pathlib` → standardize on `pathlib.Path` (Python)
- Nested unwrap chains → `let-else`, `?`, `.ok_or()` (Rust)
- Defensive flag-and-break → early return or expression-based flow
- Over-cloning → prefer `&str` / borrows over owned `String` parameters (Rust)
- Hand-rolled utility → name the stdlib module or ecosystem crate/function to use
- Copy-pasted logic → name the shared module or helper to extract into (see
  duplication section above)

For general language style, see `stand-py`, `stand-rust`, and `stand-ts`.

## Reference — Security Best Practices

- OWASP Top 10 exposure: injection (SQL, command, XSS), broken auth, SSRF, etc.
- Secrets management—no hardcoded credentials, tokens, or API keys in source
- Input validation and sanitization at system boundaries
- Proper use of cryptography—no weak algorithms, correct key/IV handling
- Dependency vulnerabilities—known CVEs in direct or transitive dependencies
- Least privilege—are permissions, scopes, and roles appropriately scoped?
- Secure defaults—are features opt-in safe (e.g., CORS, CSP, cookie flags)?
- Sensitive data handling—PII/secrets not leaked in logs, errors, or responses

## Reference — Testing (code-level)

- Test quality—flag any "nothing burger" tests that don't meaningfully validate behavior
- Use of parameterization where appropriate
- Coverage of edge cases and failure modes
- Are tests isolated and deterministic?
- Do tests cover the right layer (unit vs integration vs e2e)?

For deeper test-suite analysis, use the `analyze-tests` skill.
