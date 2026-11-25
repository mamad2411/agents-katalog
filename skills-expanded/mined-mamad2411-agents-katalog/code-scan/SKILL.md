---
name: code-scan
description: 13-dimension comprehensive code scanner. Read-only — reports CODE_SCAN_INDEX without making changes. Language-agnostic with rubric augmentation via AUTO-DETECT.md.
---

# /code-scan

**Read-only** 13-dimension quality analysis. Scores every dimension, computes CODE_SCAN_INDEX, outputs pipeline markers. Makes zero edits.

## Target

If a path argument is provided, scan that file/directory.
If no argument, scan the code most recently discussed.
Multiple paths can be provided to scan a set of components.

## Step 0: Load Rubrics

Read `.claude/rubric/AUTO-DETECT.md`. Follow its instructions:

1. **Always load:** `base.md` + `product-quality.md`
2. **Auto-detect domain rubrics** by checking target files for signals (HTTP server, CLI tool, data persistence, microservice). Load every matching rubric.
3. Extract **Review Criteria** sections from each loaded rubric.

If a rubric file doesn't exist, skip it. The generic checklists below are the floor — rubric criteria raise the ceiling.

Record which rubrics were loaded for the summary.

## Step 1: Read Target Code

Read ALL files in the target scope completely. Do not skim.

## Step 2: Analyze — 13 Dimensions

Evaluate every file against all 13 dimensions. For each finding, assign a severity:

- **Critical** (3 pts) — Security vulnerabilities, obvious bugs, data loss risk, >50-line functions, >500-line files
- **Warning** (2 pts) — Suboptimal patterns, 25-50 line functions, 300-500 line files, minor clarity issues
- **Observation** (1 pt) — Improvement opportunities, style inconsistencies, minor suggestions

### Dimension 1: Structure

Generic checklist:
- [ ] Functions ≤25 lines, single responsibility
- [ ] Files ≤300 lines, single responsibility
- [ ] Main entry ≤100 lines
- [ ] Cyclomatic complexity ≤10 per function
- [ ] Nesting depth ≤3
- [ ] Parameters ≤4 per function

Rubric augments: base.md #12 (Architecture), #6 (Bounded Operations)

### Dimension 2: Clarity

Generic checklist:
- [ ] Names reveal intent (no abbreviations except standard: API, HTTP, JSON, URL, ID)
- [ ] No comments explaining WHAT — code is self-documenting
- [ ] WHY comments where behavior is non-obvious
- [ ] Boolean variables/params prefixed with is/has/should/can
- [ ] Consistent naming style throughout (camelCase, snake_case, etc.)

Rubric augments: base.md #9 (Structured Logging — naming/context)

### Dimension 3: Data Design

Generic checklist:
- [ ] Data structures match the domain
- [ ] No primitive obsession — use value objects / branded types
- [ ] Illegal states unrepresentable (discriminated unions, enums)
- [ ] Immutable by default, mutations explicit and justified
- [ ] Config externalized — no hardcoded URLs, ports, paths, connection strings

Rubric augments: base.md #8 (Config Externalization), product-quality.md #1 (Sensible Defaults)

### Dimension 4: Error Handling

Generic checklist:
- [ ] All error paths explicit — no ignored return values
- [ ] No swallowed exceptions or empty catch blocks
- [ ] Cause chains preserved (`{ cause: e }` or equivalent)
- [ ] Resource cleanup in finally blocks / defer / using
- [ ] Fail fast with actionable messages at boundaries
- [ ] I/O errors handled — no bare file/network calls

Rubric augments: base.md #5 (Error Handling), #7 (Atomic Writes), #10 (Actionable Error Messages); product-quality.md #2 (Interactive Fallbacks), #4 (Error UX); cli.md #1 (if CLI)

### Dimension 5: Security

Generic checklist:
- [ ] Input validation at every boundary (API, CLI, file, query)
- [ ] No injection vectors — parameterized queries, safe shell usage
- [ ] No path traversal — paths normalized against a root
- [ ] No secrets in code, logs, error messages, or stack traces
- [ ] No `eval()`, `new Function()`, or equivalent dynamic execution
- [ ] Output encoding where applicable

Rubric augments: base.md #1 (Input Validation), #2 (Injection Prevention), #3 (Secret Management), #4 (Auth Lifecycle); web-api.md (if HTTP); cli.md #4 (if CLI)

### Dimension 6: Framework Idioms

Generic checklist:
- [ ] Uses built-in solutions before adding dependencies
- [ ] Follows framework conventions and lifecycle patterns
- [ ] No anti-patterns for the detected framework
- [ ] Consistent with framework's error model and async model

Rubric augments: All loaded domain rubrics (web-api.md, cli.md, microservice.md, data-persistence.md)

### Dimension 7: Dead Code

Generic checklist:
- [ ] No orphaned files (defined but never imported)
- [ ] No unused exports (exported but never consumed)
- [ ] No unreachable code after return/throw/break
- [ ] No dead branches (conditions always true/false)
- [ ] No commented-out code blocks
- [ ] No unused variables, parameters, or imports

Rubric augments: product-quality.md #3 (No Orphaned Features)

### Dimension 8: AI Smells

Generic checklist:
- [ ] No single-use wrapper functions (inline the logic)
- [ ] No comment spam (comments restating what code does)
- [ ] No defensive paranoia (try/catch or null checks for impossible cases)
- [ ] No speculative features (code for requirements that don't exist)
- [ ] No over-abstraction (interfaces/generics with one implementation)
- [ ] No unnecessary type annotations where inference works

Rubric augments: base.md #11 (AI Code Smells)

### Dimension 9: Duplication

Generic checklist:
- [ ] No copy-paste blocks (≥5 similar lines across files)
- [ ] No same-name functions with near-identical bodies
- [ ] No repeated validation / guard / boilerplate sequences
- [ ] No duplicated string literals (use constants)
- [ ] No repeated error handling patterns that should be centralized

Rubric augments: (universal — no specific rubric reference)

### Dimension 10: Consistency

Generic checklist:
- [ ] Error handling follows one style throughout (throw vs return vs Result)
- [ ] Naming conventions uniform (no mixing camelCase and snake_case)
- [ ] Import style consistent (relative vs alias, order, grouping)
- [ ] Async style consistent (no mixing callbacks, promises, async/await)
- [ ] File organization follows a single pattern

Rubric augments: base.md #9 (Structured Logging — consistent context)

### Dimension 11: Type Safety

Generic checklist:
- [ ] No `any` / `object` / `dynamic` / untyped containers where a type is known
- [ ] Type assertions (`as`) replaced with type guards where possible
- [ ] No implicit type coercion (`==` instead of `===`, string + number)
- [ ] Return types explicit on public functions when not obvious
- [ ] Nullable values handled explicitly (no truthy/falsy shortcuts on non-booleans)

Rubric augments: (generic — domain rubrics add language-specific rules)

### Dimension 12: Dependency Health

Generic checklist:
- [ ] No circular imports between modules
- [ ] No unused dependencies in manifest (package.json, requirements.txt, etc.)
- [ ] No deprecated dependencies still in use
- [ ] Lockfile present and committed
- [ ] No vendored copies of available packages

Rubric augments: base.md #13 (Runtime Version)

### Dimension 13: Conversion Residue

Generic checklist:
- [ ] No TODO/FIXME comments referencing old frameworks or migrations
- [ ] No stale imports from previous framework/language
- [ ] No foreign idioms (patterns from a different framework used in current one)
- [ ] No dead compatibility shims or polyfills for removed dependencies
- [ ] No mixed old/new API usage where migration should be complete

Rubric augments: Domain rubrics (deviation from expected idiom = residue)

## Step 3: Score

**Per dimension:** Sum finding points (Critical=3, Warning=2, Observation=1), then cap at 10.

```
dimension_score = min(10, sum_of_finding_points)
```

A score of 0 = clean, 10 = severe.

**CODE_SCAN_INDEX:** Sum of all 13 dimension scores. Range 0-130 (lower is better).

```
CODE_SCAN_INDEX = sum(dimension_scores)  // 0-130
```

| Range | Rating |
|-------|--------|
| 0-10 | Excellent |
| 11-25 | Good |
| 26-50 | Moderate |
| 51-80 | Poor |
| 81-130 | Critical |

## Step 4: Report

Generate the report in this exact structure:

```markdown
## Code Scan: [target]

### Dimension Heatmap

| # | Dimension | Score | Findings | Worst Issue |
|---|-----------|-------|----------|-------------|
| 1 | Structure | N/10 | Nc Nw No | [brief] |
| 2 | Clarity | N/10 | Nc Nw No | [brief] |
| 3 | Data Design | N/10 | Nc Nw No | [brief] |
| 4 | Error Handling | N/10 | Nc Nw No | [brief] |
| 5 | Security | N/10 | Nc Nw No | [brief] |
| 6 | Framework Idioms | N/10 | Nc Nw No | [brief] |
| 7 | Dead Code | N/10 | Nc Nw No | [brief] |
| 8 | AI Smells | N/10 | Nc Nw No | [brief] |
| 9 | Duplication | N/10 | Nc Nw No | [brief] |
| 10 | Consistency | N/10 | Nc Nw No | [brief] |
| 11 | Type Safety | N/10 | Nc Nw No | [brief] |
| 12 | Dependency Health | N/10 | Nc Nw No | [brief] |
| 13 | Conversion Residue | N/10 | Nc Nw No | [brief] |

Findings column format: `Nc Nw No` = N critical, N warnings, N observations.
Use `—` in Worst Issue for dimensions scoring 0.

### Critical Issues

1. **[file:line]** [Dimension N] — [description]
   - Problem: [what's wrong]
   - Impact: [why it matters]
   - Fix: [how to fix]

### Warnings

1. **[file:line]** [Dimension N] — [description]
   - Concern: [what's questionable]
   - Consider: [improvement]

### Observations

1. **[file:line]** [Dimension N] — [observation]

### Summary

| Metric | Value |
|--------|-------|
| Files scanned | N |
| Total lines | N |
| CODE_SCAN_INDEX | N/130 (Rating) |
| Worst dimension | [name] (N/10) |
| Cleanest dimension | [name] (N/10) |
| Rubrics loaded | base, product-quality[, domain...] |

CODE_SCAN_INDEX: N/130 (Rating)
CODE_SCAN_DONE
```

## Rules

- **READ ONLY** — Do not edit any files
- **COMPLETE** — Read all target files fully, do not skim
- **SPECIFIC** — Cite file:line for every finding
- **ACTIONABLE** — Every critical/warning has a fix suggestion
- **NO EXTERNAL TOOLS** — Claude analysis only. No Gemini, Qodana, or MCP tool calls
- **DETERMINISTIC SCORING** — Same code, same scores. No rounding, no partial points
- **PIPELINE MARKERS** — Always emit `CODE_SCAN_INDEX: N/130 (Rating)` and `CODE_SCAN_DONE` at report end
