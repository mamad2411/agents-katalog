---
name: canon-review
description: |
  Unified engineering standards review combining code-level review (canon-pr-review)
  and architecture-level design review (canon-design-review). Evaluates 35 Tier 2
  best practices drawn from 35 seminal engineering books.

  Auto-invoke when the user asks to:
  - "canon review", "full review", "engineering review", "review PR"
  - "review code and architecture", "check against best practices"
  - "score this PR", "run canon review"

  Supports three modes:
  1. Code Review (20 practices: Code Quality, Module Design, Reliability, Maintainability)
  2. Design Review (15 practices: Structural Integrity, Resilience, Evolutionary Design)
  3. Full Review (Both 20-practice code review and 15-practice design review)

category: development
user-invocable: true
allowed-tools: Bash, Read, Edit, Write, Glob
argument-hint: "[pr_url_or_number] [--mode code|design|full|auto]"
---

# Canon Review — Unified Code & Design Review

The **Canon Review** skill provides a single entry point for evaluating code changes against canonical software engineering best practices drawn from seminal literature (*Code Complete*, *Clean Code*, *A Philosophy of Software Design*, *Refactoring*, *Release It!*, *Designing Data-Intensive Applications*, *Domain-Driven Design*, *Team Topologies*, etc.).

It unifies:
- **Code Review** ([`canon-pr-review`](../canon-pr-review/SKILL.md)): 20 Tier 2 practices covering implementation quality, module design, line-level reliability, and maintainability.
- **Design Review** ([`canon-design-review`](../canon-design-review/SKILL.md)): 15 Tier 2 practices covering structural integrity, distributed resilience, and evolutionary architecture.

---

## Phase 0: Auto-Routing & Mode Selection

Identify the review scope and select the review mode:

```bash
# 1. Fetch PR diff and file list if PR number/URL provided
gh pr view <NUMBER> --json title,body,changedFiles,baseRefName,headRefName
gh pr diff <NUMBER>
```

### Routing Rules

| Input / Signal | Target Mode | Description |
|---|---|---|
| `--mode code` OR "code review" | **Code Review** | Evaluates 20 line-level & module practices (`canon-pr-review`). |
| `--mode design` OR "design review" | **Design Review** | Evaluates 15 system/architecture practices (`canon-design-review`). |
| `--mode full` OR "full review" OR "both" | **Full Review** | Evaluates both Code Review (20 practices) and Design Review (15 practices). |
| `--mode auto` (default) | **Auto-Selected** | Automatically chooses mode based on changed files (see Auto-Detection below). |

### Auto-Detection Logic (`--mode auto`)

1. Inspect changed file paths from the diff:
   - If any file touches architecture directories (`services/`, `infrastructure/`, `platform/`, `domain/`, `core/`), API contracts (`**/api/*`, `**/schema*`, `*.proto`), database migrations (`**/migrations/*`), or architecture docs (`**/architecture*`, `**/design*`, `**/adr/*`):
     - **Select Full Review** (runs both Code and Design evaluations).
   - Otherwise (standard feature PRs, bugfixes, utility changes):
     - **Select Code Review**.

---

## Phase 1: Code Review Evaluation (20 Practices)

Evaluates the 4 dimensions from [`canon-pr-review`](../canon-pr-review/SKILL.md). Each practice is scored 0–5.

### Dimension 1: Code Quality
- **CC-003 — Intention-Revealing Names**: No cryptic abbreviations or single-letter variables (except loop indices). Names reflect purpose.
- **CC-005 — Single Responsibility (Function)**: Functions do one thing without needing "and"/"or" descriptions.
- **CC-006 — DRY (No Knowledge Duplication)**: Core business rules defined in a single authoritative place.
- **CC-011 — Guard Clauses / Early Returns**: Happy path at leftmost indentation; preconditions fail fast.
- **CC-021 — Eliminate Code Smells**: No long methods (>50 lines), large classes (>300 lines), feature envy, or data clumps.

### Dimension 2: Module Design
- **CC-027 — Deep Modules**: Simple interfaces hiding significant internal complexity; no shallow wrappers.
- **CC-015 — Composition Over Inheritance**: Prefer composition over multi-level inheritance hierarchies.
- **CC-028 — Interface Comments**: Docstrings explain *what* and *why*, preconditions, errors, and non-obvious behavior.
- **CC-017 — Encapsulate What Varies**: Isolate variation points in data structures or strategy objects, not hardcoded switch chains.

### Dimension 3: Reliability
- **CC-014 — Explicit Error Handling**: Never swallow exceptions (`except: pass`); transform to domain exceptions with context.
- **CC-048 — Idempotency Across Network Boundaries**: Mutating operations (POST/PUT, payments, retries) use idempotency keys or deduplication.
- **CC-056 — Circuit Breakers**: External dependency calls wrapped in circuit breakers to isolate failure.
- **CC-058 — Explicit Timeouts**: Every network call specifies explicit connect and read timeouts.
- **CC-060 — Graceful Degradation**: Non-critical dependency failures fall back gracefully rather than crashing the primary operation.

### Dimension 4: Maintainability
- **CC-019 — Small Refactoring Steps**: Refactoring and feature changes isolated in behavior-preserving commits.
- **CC-031 — Tests Before Legacy Changes**: Modified code paths protected by characterization/unit tests.
- **CC-093 — Fix Broken Windows**: No untracked TODOs, unexplained `# noqa` suppressions, or skipped tests.
- **CC-107 — Regression Tests**: Bug fixes include a failing test that reproduces the issue before fixing.

---

## Phase 2: Design Review Evaluation (15 Practices)

Evaluates the 3 assessment areas from [`canon-design-review`](../canon-design-review/SKILL.md). Each practice scored PASS / WARN / BLOCK / N/A.

### Area 1: Structural Integrity
- **Practice 1 — Bounded Context Alignment (CC-035)**: Explicit Anti-Corruption Layers (ACLs) or DTOs across context boundaries; no direct entity imports across services.
- **Practice 2 — Layer Separation (CC-040)**: Handlers delegate to domain services; domain objects decoupled from raw DB/HTTP concerns.
- **Practice 3 — Dependency Direction (CC-026)**: Dependencies point inward toward core domain; infrastructure implements domain interfaces.
- **Practice 4 — Interface Segregation (CC-025)**: Narrow, caller-focused interfaces; no wide interfaces with stubbed implementations.
- **Practice 5 — Cohesion (CC-119, CC-151)**: High cohesion within modules; single responsibility at module/service boundaries.

### Area 2: Resilience & Operations
- **Practice 6 — Circuit Breakers on External Dependencies**: Fault-isolation wrapping for external services/databases.
- **Practice 7 — Bulkheads (Isolated Failure Domains)**: Separate thread/connection pools per workload type; resource isolation.
- **Practice 8 — Explicit Consistency Model**: Documented consistency model (strong, eventual, saga/outbox pattern).
- **Practice 9 — Backpressure Mechanisms**: Bounded queues (`maxsize`), load-shedding, or rate-limiting for producers/consumers.
- **Practice 10 — Health Checks & Graceful Shutdown**: Liveness/readiness probes reflecting real health; SIGTERM handling with bounded connection draining.

### Area 3: Evolutionary Design
- **Practice 11 — Shearing Layers (CC-098)**: Fast-changing concerns (business rules, flags) separated from slow-changing concerns (schema, platform).
- **Practice 12 — Start Simple / Gall's Law**: Complex working systems evolved from simple working systems; no premature abstraction or distributed complexity.
- **Practice 13 — Cognitive Load per Team**: Service complexity fits single-team ownership without requiring deep knowledge of >3 external services.
- **Practice 14 — API Versioning & Backward Compatibility**: Non-breaking public API evolution; breaking changes versioned with deprecation windows.
- **Practice 15 — ADR for Significant Decisions (CC-132)**: Architecture Decision Records recorded for significant technical choices (new DBs, service splits, consistency trade-offs).

---

## Phase 3: Verdict Determination

### Code Review Verdict Rules
- **BLOCK**: Any dimension score < 1, OR any individual Reliability practice scores 0.
- **REQUEST_CHANGES**: Any dimension score < 3 (with no BLOCKs).
- **APPROVE**: All four dimension scores ≥ 3.

### Design Review Verdict Rules
- **BLOCK**: Any practice receives a BLOCK verdict.
- **REQUEST_CHANGES**: Any practice receives a WARN verdict (and 0 BLOCKs).
- **APPROVE**: All practices receive PASS or N/A.

### Unified Verdict (Full Review Mode)
- **BLOCK**: If either Code Review OR Design Review yields BLOCK.
- **REQUEST_CHANGES**: If either Code Review OR Design Review yields REQUEST_CHANGES (and neither yields BLOCK).
- **APPROVE**: If both Code Review AND Design Review yield APPROVE.

---

## Phase 4: Output Format

Post or render the review using the unified markdown structure:

```markdown
## Canon Engineering Review — [PR Title or Component Name]

**Mode Executed**: [Code Review | Design Review | Full Review (Auto-Selected)]
**Scope**: [files reviewed]
**Overall Decision**: **[APPROVE / REQUEST_CHANGES / BLOCK]**

---

### Part 1: Code Review Scorecard (20 Practices)

| Dimension | Score | Gate | Key Findings |
|-----------|-------|------|--------------|
| **Code Quality** (naming, SRP, DRY, guard clauses, smells) | X/5 | ✅/⚠️/🚫 | [summary] |
| **Module Design** (deep modules, composition, docs, encapsulation) | X/5 | ✅/⚠️/🚫 | [summary] |
| **Reliability** (error handling, idempotency, circuit breakers, timeouts, degradation) | X/5 | ✅/⚠️/🚫 | [summary] |
| **Maintainability** (small steps, test coverage, broken windows, regression tests) | X/5 | ✅/⚠️/🚫 | [summary] |

---

### Part 2: Design Review Scorecard (15 Practices)

#### Structural Integrity
| # | Practice | Status | Notes / Evidence |
|---|----------|--------|------------------|
| 1 | Bounded Context Alignment | PASS / WARN / BLOCK / N/A | [finding] |
| 2 | Layer Separation | ... | ... |
| 3 | Dependency Direction | ... | ... |
| 4 | Interface Segregation | ... | ... |
| 5 | Cohesion | ... | ... |

#### Resilience & Operations
| # | Practice | Status | Notes / Evidence |
|---|----------|--------|------------------|
| 6 | Circuit Breakers | ... | ... |
| 7 | Bulkheads | ... | ... |
| 8 | Explicit Consistency Model | ... | ... |
| 9 | Backpressure | ... | ... |
| 10 | Health Checks + Shutdown | ... | ... |

#### Evolutionary Design
| # | Practice | Status | Notes / Evidence |
|---|----------|--------|------------------|
| 11 | Shearing Layers | ... | ... |
| 12 | Start Simple (Gall's Law) | ... | ... |
| 13 | Cognitive Load per Team | ... | ... |
| 14 | API Versioning | ... | ... |
| 15 | ADR for Significant Decisions | ... | ... |

**Design Score**: [PASS*100 + WARN*50] / [(15 - N/A) * 100] * 100 = [XX]%

---

### Specific Violations & Actionable Fixes

#### [Practice ID / Name] — Location: `path/to/file.py:line`
- **Issue**: [Description]
- **Offending Code**:
  ```language
  [verbatim code excerpt]
  ```
- **Suggested Improvement**:
  ```language
  [remediation example]
  ```

---

### To Unblock / Action Items

1. [Action item 1]
2. [Action item 2]
```

---

## Iron Laws & Anti-Rationalization

1. **Concrete Evidence Required**: Every violation (WARN or BLOCK) must quote verbatim code and cite `file:line`.
2. **No Skipping Dimensions**: In Full Review mode, evaluate both Code Quality and Design Architecture without ignoring either layer.
3. **Falsifiability**: Theoretical risks are not violations; violations must be demonstrably present in the diff or immediately affected context.
