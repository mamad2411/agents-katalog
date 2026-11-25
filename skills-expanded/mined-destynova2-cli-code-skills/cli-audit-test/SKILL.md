---
name: cli-audit-test
metadata:
  author: clement
description: "Audit test plan quality and maturity. Scores coverage, techniques, pyramid balance, negative testing, NFR, automation, CI integration. Use when reviewing a test plan, test strategy, test suite structure, or saying 'audit tests', 'test quality', 'test plan review', 'test maturity', 'are my tests good enough', 'test scoring', 'test pyramid'. Also triggers on 'test coverage', 'test gaps', 'missing tests'."
argument-hint: "[test-plan-file-or-tests-directory]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the report in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Audit Test — Test Plan Quality & Maturity Scorer

Evaluate a test plan or test suite against ISTQB standards, TMMi maturity model, and industry best practices.

> "A test plan that only says 'we will test' without specifying *which techniques* and *why* is a major red flag."
> — ISTQB Foundation Level Syllabus v4.0

## Core Principle

**A test plan is a contract with quality.** Every dimension left vague is a risk accepted silently. This skill measures how explicitly and completely that contract is defined, using a 12-dimension framework calibrated on ISTQB, TMMi, and proven industry patterns.

## Input

`$ARGUMENTS` is the target to audit:

- **Test plan document** (`.md`, `.txt`, `.adoc`, `.pdf`): audit the plan as written
- **Tests directory** (`tests/`, `tests/e2e/`, etc.): infer the plan from the test structure, files, and config
- **Empty**: search for test plans in the project root, then fall back to `tests/` directory analysis

### Input Discovery

1. Glob for test plan documents: `**/test-plan*`, `**/test-strategy*`, `**/TESTING*`
2. Glob for test directories: `**/tests/**`, `**/test/**`, `**/e2e/**`, `**/spec/**`
3. Glob for CI config: `.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, `justfile`
4. Glob for test config: `**/pict/**`, `**/fixtures/**`, `**/mocks/**`, `**/toxiproxy*`
5. Read project manifest (Cargo.toml, package.json, etc.) for test dependencies

## 13-Dimension Framework

Score each dimension **0-4**, then compute a weighted final score. Read `references/dimensions.md` for detailed scoring criteria, evidence patterns, and per-dimension guidance.

> A test plan's reach can be read against the shared **T0-T4/M0 ladder** (`../shared/gate-ladder.md`): how far up the rungs (static contract → component → fresh deploy → day-2 ops → stress) does the suite actually go? Most plans stall at T1-T2.

| # | Dimension | Weight | Key question |
|---|-----------|--------|-------------|
| D1 | Scope & Objectives | 7% | Is what's tested (and what's not) explicit? |
| D2 | Test Design Techniques | 12% | Are recognized techniques (EP, BVA, pairwise...) used? |
| D3 | Pyramid Balance | 7% | Is the unit > integration > E2E ratio healthy? |
| D4 | Coverage & Traceability | 11% | Can you trace each requirement to a test? |
| D5 | Negative Testing & Security | 8% | Are error paths and security invariants tested? |
| D6 | Non-Functional Testing | 9% | Performance, security, accessibility, reliability? |
| D7 | Risk Analysis & Prioritization | 7% | Do critical features get more test effort? |
| D8 | Automation Strategy | 9% | What's automated vs manual, and why? |
| D9 | CI/CD Integration | 7% | Do tests run on commit with quality gates? |
| D10 | Entry/Exit Criteria | 5% | When is testing "done"? Measurable thresholds? |
| D11 | Exploratory Testing | 5% | Structured charters and time-boxed sessions? |
| D12 | Environment & Data | 5% | Automated setup, deterministic data, mocks? |
| D13 | Semantic Drift Detection | 8% | Are silent behavioral changes caught before merge? |

## Workflow

### Step 1 — Discover test assets

Glob for test files, CI configs, test frameworks. Build a test inventory: total files by type, directories and purpose, CI jobs, frameworks detected.

### Step 2 — Classify test files

For each test file/directory, classify by level (unit/integration/E2E/acceptance), technique, type (functional/security/performance), and polarity (positive/negative). Read `references/techniques.md` for technique detection heuristics.

### Step 3 — Score all 13 dimensions

For each dimension: collect evidence (file references, counts, patterns), assign score 0-4 with justification, note strengths and gaps. Read `references/dimensions.md` for detailed scoring criteria.

### Step 4 — Detect anti-patterns

Read `references/anti-patterns.md` for the 11 anti-patterns with detection rules and recommendations. Flag with severity and evidence.

### Step 5 — Compute final score

```
Final Score = Σ (dimension_score / 4 × weight × 100)
```

Normalize to 0-100 scale. Read `references/scoring-framework.md` for TMMi mapping and benchmarks.

### Step 6 — Generate report

Use the output format below. Finding tier and confidence semantics are canonical in `../shared/triage.md` (Tier 3/2/1 + GRADE + triangulation). D-dimension findings carry tier and confidence so `cli-cycle` can aggregate without re-parsing.

## Output Format

```markdown
# Test Plan Quality Audit — {project-name}

**Date:** {date}
**Target:** {what was audited}
**Final Score:** {X}/100 — {verdict}
**TMMi Equivalent:** Level {N}

## Test Inventory

| Type | Count | Examples |
|------|-------|---------|
| Unit tests | N | `src/*/tests.rs` |
| Integration tests | N | `tests/integration/` |
| E2E tests | N | `tests/e2e/tests/` |
| Total | N | |

### Test Pyramid Visualization
(ASCII pyramid showing shape: Pyramid|Diamond|Ice Cream Cone|Inverted)

## Dimension Scores

| # | Dimension | Weight | Score | /4 | Weighted | Verdict |
|---|-----------|--------|-------|----|----------|---------|
| D1-D13 rows... |
| | **Total** | **100%** | | | **X.X** | |

### Techniques Detected
(Table: Technique | Evidence | Applied to)

## Anti-Patterns Detected
(Table: Anti-Pattern | Severity | Evidence | Recommendation)

## Strengths / Gaps & Recommendations / Maturity Assessment
```

### Quality Thresholds

| Range | Verdict |
|-------|---------|
| 86-100 | Excellent — Comprehensive, mature, CI-integrated |
| 71-85 | Good — Solid plan with minor gaps |
| 51-70 | Acceptable — Functional but needs improvement |
| 26-50 | Insufficient — Major gaps, significant risk |
| 0-25 | Critical — Plan needs complete rework |

## Rules for the Auditor

1. **Evidence-based**: Every score needs a file reference, count, or concrete observation.
2. **Proportional**: Scale judgment to project size. A 5-test project differs from a 118-test enterprise suite.
3. **Technique-aware**: Recognize techniques even when not explicitly named. `tests/budget/` with 79%, 80%, 100%, 101% values IS BVA.
4. **Structure over documentation**: A well-organized test directory IS a test plan. Judge by substance, not ceremony.
5. **Score honestly**: 100/100 means world-class. 70/100 is genuinely good. 50/100 is typical.
6. **Anti-patterns > missing features**: Detecting an ice cream cone is more valuable than noting a missing charter.
7. **Actionable output**: Every gap must come with a concrete, sized recommendation.
8. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes.

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-audit-xray` | Produces optimization cards whose validation methods become concrete unit, property, benchmark, or trace-comparison test requirements |
| `cli-audit-code` | Scores code quality. cli-audit-test scores **test quality** |
| `cli-audit-doc` | Scores doc quality. cli-audit-test checks **test documentation** |
| `cli-audit-drift` | Checks behavioral conformity via contracts. cli-audit-test checks **test-level** drift detection (D13) |
| `cli-audit-sync` | Verifies doc-code coherence. cli-audit-test verifies **test-requirement coherence** |
| `cli-forge-schema` | Can visualize test plan as diagrams (pyramid, state machines) |
| `cli-forge-perf` | D6 (NFR) and D7 (risk) cover perf as *intent*; `cli-forge-perf` provides the executable bench harness (A/B, distribution, permutation test) that turns the intent into a non-regression gate |
| `cli-cycle` | Calls cli-audit-test as part of the full project review; emit `.claude/cli-audit-test.json` per `../shared/result-schema.md` for orchestrator aggregation |
| `cli-audit-data` | Defines PostgreSQL-specific proof cases; this skill scores their place in the overall test strategy |

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Tests cover performance intent but no concrete code path or rewrite candidate is identified | `/cli-audit-xray` | Find the semantic hot path and produce validation-ready optimization cards |
| No negative tests for security features | `/cli-audit-code` on security modules | Verify C9 coverage |
| Test pyramid inverted (too many E2E, few unit) | `/cli-audit-tangle` | Find god functions that resist unit testing |
| Missing drift detection in tests (D13 low) | `/cli-audit-drift` | Bootstrap CONTRACTS.md |
| CI has no test stage | `/cli-forge-pipeline` | Add test jobs to pipeline |
| D6 (perf/NFR) low or no perf budget gate | `/cli-forge-perf` | Catalogue + harnais A/B exécutable pour transformer le SLO en test de non-régression |
| PostgreSQL/SQLx tests use only mocks/SQLite or omit synchronized concurrency and N-1 migrations | `/cli-audit-data` | Derive the required database proof from criticality and invariants |

**Rule:** Recommend, don't auto-execute.

## What this skill does NOT do

- **Does not run tests** — it audits the plan/structure
- **Does not generate tests** — it identifies gaps
- **Does not replace manual review** — it provides a structured framework
- **Does not check test correctness** — it checks test *strategy*

## Reference Sources

- ISTQB Foundation Level Syllabus v4.0 (2023)
- TMMi Framework R1.2
- ISO 25010
- La Taverne du Testeur — niveaux de test, pyramide, smoke tests, Cassandre
- Codepipes — 13 Software Testing Anti-patterns
- Mike Cohn — Test Pyramid
