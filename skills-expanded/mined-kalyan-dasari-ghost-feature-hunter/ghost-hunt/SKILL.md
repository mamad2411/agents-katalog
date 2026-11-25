---
name: ghost-hunt
description: Context-aware codebase investigator and feature verification skill for AI coding agents. Discovers architecture, traces multi-language data flow, executes safe checks, audits whole repositories for ghost features and code hygiene, isolates confirmed defects, and verifies fixes end-to-end.
metadata:
  author: Ghost Feature Hunter contributors
  version: "0.3.0"
---

# Ghost Hunt (`ghost-hunt`)

> **DON'T TRUST THE FEATURE. VERIFY IT.**

Ghost Hunt is an open-source, context-aware Agent Skill for AI coding agents. When asked to inspect a project, audit a repository, or verify a feature, Ghost Hunt first locks the correct project scope, detects actual languages and frameworks, traces full-stack data flow, detects ghost features and unfinished implementations, executes safe checks, isolates confirmed defects with empirical evidence, and recommends targeted fixes.

---

## 🧭 Investigation Modes & Invocations

Ghost Hunt operates in five distinct skill modes:

| Mode | Invocation Syntax | Purpose |
|---|---|---|
| **Project Discovery** | `/ghost-hunt discover` | Static architecture inventory, language capability matrix, boundary detection. Zero runtime mutations. |
| **Feature Investigation** | `/ghost-hunt investigate <feature>` | End-to-end verification of a specific feature in the target application. |
| **Repository-Wide Audit** | `/ghost-hunt audit` | Whole-repository audit for ghost features, empty implementations, route mismatches, unused code, and duplication. |
| **Code Change Review** | `/ghost-hunt review [target]` | Review uncommitted, staged, branch, or commit changes and surrounding call graph for wiring defects, security risks, and test gaps. |
| **Post-Fix Verification** | `/ghost-hunt verify <feature>` | Re-verifies approved code fixes and runs regression checks against test suites. |

### Bare Invocation Protocol (`/ghost-hunt investigate` or `/ghost-hunt`)
When invoked without a feature argument:
1. **Identify Project Root:** Detect workspace root, Git root, and package manifests.
2. **Display Project Context:** Report project name, primary languages, and detected application roots.
3. **Isolate Examples & Fixtures:** Categorize `src/`, `lib/`, `app/` as primary application source; classify `examples/`, `fixtures/`, and `benchmarks/` separately. **Never silently choose an example or benchmark directory as the primary target.**
4. **Clarify Intent:** Ask one concise question to determine which feature to investigate, while explaining that a whole-project investigation is available via `/ghost-hunt audit`, and code review via `/ghost-hunt review`.

---

## 🔍 Agent-Native Investigation vs Optional CLI Engine

Ghost Hunt is an **open-source, reusable Agent Skill for AI coding agents**. The optional Python CLI companion is not required to use the skill.

### 1. Agent-Native Investigation (Primary Path)
When invoked inside an AI coding agent (Antigravity, Claude Code, Codex), use native agent tools:
- **Project & Package Bounds:** Read `package.json`, `go.mod`, `pom.xml`, `Cargo.toml`, `pyproject.toml`.
- **Language & Framework Conventions:** Trace controllers, endpoints, models, client calls, and UI components across any language (Python, TypeScript, Go, Java, C#, PHP, Ruby, Rust, Kotlin).
- **Test Reading & Execution:** Locate test files and run existing tests using terminal commands (`go test`, `npm test`, `cargo test`, `pytest`, `dotnet test`).
- **Safety Standard:** Treat static test references as candidates, never as verified runtime passes.

### 2. Optional Companion Python CLI
For deterministic CI/CD and scripted automation:
- Run `ghost-hunter discover`, `ghost-hunter map`, `ghost-hunter plan`, `ghost-hunter audit`, `ghost-hunter audit-repo`, `ghost-hunter review`.
- Discloses its static capability levels honestly (`deep-static`, `structural`, `inventory-only`).

---

## 📋 Mandatory Project Context & Capability Summary

Every Ghost Hunt audit or review report must begin with this standardized block:

```markdown
### Project Context Summary
- **Project Name:** `<project_name>`
- **Project Root:** `<path_to_project_root>`
- **Git Repository Root:** `<git_root_or_none>`
- **Selected Application Root:** `<app_root>`
- **Investigation Mode:** `<discover | investigate | audit | review | verify>`
- **Included Directories:** `<included_directories>`
- **Excluded Directories:** `<excluded_directories (e.g. examples, vendor, tests)>`
- **Available Capabilities:** `<native_tools_available (file, shell, curl, browser)>`
- **Limitations:** `<unsupported_runtimes_or_mocked_services>`

### Language & Framework Capability Matrix
| Language / Framework | Detected | Capability Level | Analysis Capability | Limitations |
|---|---|---|---|---|
| `<Language / Framework>` | Yes | `<deep-static | structural | inventory-only>` | `<Supported analysis>` | `<Explicit limitations>` |
```

*(Consult [references/language-support.md](references/language-support.md) for ecosystem capability specifications).*

---

## ⚖️ The Three-Status Evidence Standard

Classify every verification checkpoint into exactly one of three states. Never deviate from this logic:

| Status | Exact Meaning | Permissible Interpretation |
|---|---|---|
| **`PASS`** | A real check ran against uncontaminated state and its observed result affirmatively matched an authoritative expectation. | Proves **only** the executed assertion. Never infer unasserted behavior. |
| **`FAIL`** | An executed check directly contradicted an authoritative expected behavior. | Proves the feature broke at this specific checkpoint. |
| **`UNKNOWN`** | Prerequisites, permissions, runtimes, clean databases, or evidence were unavailable; or an inferred assumption is unconfirmed. | **Never relabel as PASS or FAIL.** Indicates an unverified check. |

---

## 🔬 The 11-Step Feature Investigation Protocol

When investigating a feature (`/ghost-hunt investigate <feature>`), execute these 11 steps:

```text
1. Scope & Project Lock ──> 2. Static Discovery ──> 3. Flow Tracing ──> 4. Requirements
                                                                               │
7. Defect Isolation <── 6. Safe Execution <── 5. Journey Checkpoints <─────────┘
│
└──> 8. Root Cause ──> 9. Minimal Fix ──> 10. Regression ──> 11. Evidence Report
```

### 1. Scope & Project Context Lock
Detect project root, git root, and target application. Distinguish application source from examples/fixtures. Explicit user paths take precedence over inferred roots. *(Consult [references/project-context.md](references/project-context.md))*

### 2. Discover Relevant Source Files
Statically inspect route definitions, backend controllers, database models, templates, and existing tests across the project's actual languages without importing or executing untrusted code. *(Consult [references/discovery-understanding.md](references/discovery-understanding.md))*

### 3. Trace End-to-End Data Flow
Trace data across all tiers: `User Action -> Route -> Controller -> Service Logic -> DB Mutation -> Response -> UI State`.

### 4. Analyze Requirements & Tag Sources
Classify all behavioral expectations into the 5-source taxonomy:
1. `user_requirement`: Constraints stated explicitly by the user in the prompt. **Must quote prompt.**
2. `product_documentation`: Specifications in README or docs. **Must cite file and section.**
3. `api_contract`: Formal schema, OpenAPI, or TypeScript types. **Must cite contract file.**
4. `existing_test`: Assertions verified by passing tests. **Must cite test file and function.**
5. `inferred_assumption`: Hypotheses deduced from code or patterns.

> [!IMPORTANT]
> **The Critical Rule for Inferred Assumptions:**
> Hypotheses must NEVER silently become authoritative requirements. If code differs from an inferred assumption, report it as an observation with status **`UNKNOWN`** and ask for confirmation. Never manufacture a `FAIL` simply because code differs from convention.

### 5. Define Journey Checkpoints
Structure discrete, ordered checkpoints covering happy paths, auth boundaries, persistence, and error paths. *(Use [templates/journey-template.json](templates/journey-template.json) or [references/journey-mapping.md](references/journey-mapping.md))*

### 6. Execute Relevant Safe Checks
- **Side-Effect Classification:** Inspect actual handler behavior before execution; do not assume GET is safe or POST is mutating.
- **Authorization Gate:** Request explicit user authorization before Level 3 runtime mutations.
- **Stateful Scenario Isolation:** Run state-dependent checks against fresh disposable databases (`tempfile`). Seed known initial state, record baseline initial values, execute approved actions, and record final observed values.
- **Contamination Guard:** Never continue on contaminated test state. If clean state cannot be established, mark **`UNKNOWN`**.
- **PASS Evidence Contract:** PASS requires affirmative match against authoritative expectation with uncontaminated evidence. Static inspection alone can NEVER prove runtime PASS. *(Consult [references/verification-playbook.md](references/verification-playbook.md))*

### 7. Identify Confirmed Defects
Record every discrepancy between authoritative expected behavior and actual observation as a confirmed defect (**`FAIL`**).

### 8. Investigate Root Cause
Trace backward from observed failure to exact source files and line ranges (`path/to/file.py:L42-L55`). Explain *why* the defect occurs. *(Consult [references/investigation-root-cause.md](references/investigation-root-cause.md))*

### 9. Recommend Targeted Fixes
Present the smallest surgical patch addressing the root cause. **NEVER modify source code without user authorization.**

### 10. Verify Fixes & Prevent Regressions
Upon user approval, apply the edit, rerun failing checkpoints to confirm resolution (**`PASS`**), and rerun adjacent test suites to prevent regressions. *(Consult [references/regression-verification.md](references/regression-verification.md))*

### 11. Produce an Evidence-Backed Report
Deliver a structured Markdown audit report starting with the Project Context Summary, capability matrix, checkpoint breakdown, before/after measurements, root causes, and limitations. *(Use [templates/report-template.md](templates/report-template.md) and [references/evidence-reporting.md](references/evidence-reporting.md))*

---

## 🏛️ The Whole-Repository Audit Protocol (`/ghost-hunt audit`)

When invoked with `/ghost-hunt audit`, inspect the complete repository with scope awareness:
1. **Architecture & Scope Inventory:** Map application boundaries, source-role classifications (`application_source`, `example`, `demo`, `test`, `fixture`, `documentation`, `configuration`), and the Language/Framework Capability Matrix.
2. **Scope-Segregated Findings:** Strictly separate primary application findings from intentionally broken examples (`examples/`), test suites (`tests/`), fixtures, and documentation.
3. **Route Connection Analysis:**
   - **Cross-Service & External Matching:** Distinguish local routes, cross-service routes within monorepos, and external service calls (`https://...`). Unmatched routes under reverse-proxy configs are marked as proxy candidates.
   - **Method / Path Mismatches:** Client dispatches an HTTP method or path differing from the registered handler.
   - **Potentially Unused Endpoints:** Routes with 0 callers in frontend, tests, or docs (candidates requiring owner confirmation).
   - **Route Test Coverage (Function-Level):** Evaluates whether individual test cases invoke the route and assert on the response (`test_assertion_candidate`, `test_reference_candidate`, or `testing_gap_candidate`). Never claims static `test_verified`.
4. **Ghost Feature Detection:** Identify broken chains across UI navigation, buttons, forms, client calls, routes, and services. *(Consult [references/ghost-features.md](references/ghost-features.md))*
5. **Empty & Unfinished Implementations:** Surface empty functions, placeholder handlers, unhandled exceptions, and silent error catches (excluding abstract methods, interfaces, and test mocks).
6. **Application Boundaries & Dependency Hygiene:** Attribute package manifests to owning application roots. Distinguish runtime vs dev/test/build dependencies. Disclose unsupported dependency ecosystems (Cargo, go.mod, etc.) as inventory-only.
7. **Structural Duplicate Logic:** Detect identical normalized function bodies across application source files without double-counting lines. *(Consult [references/repository-audit.md](references/repository-audit.md))*

---

## 🧐 Code Change Review Protocol (`/ghost-hunt review`)

When invoked with `/ghost-hunt review [target]`, inspect modified code and its surrounding call paths:
- **Review Targets:** Uncommitted changes (default), staged changes (`--staged`), branch comparison (`--branch <base>`), or specific commit/PR (`--commit <sha>`).
- **Scope of Review:** Inspect not just changed lines, but all callers, routes, consumers, error paths, and regression tests affected by the change.
- **Line-Range Defect Isolation:** Distinguish defects introduced on changed lines from pre-existing issues in surrounding unchanged code. In deletion-only and mixed diffs, accurately attribute findings without blaming pure deletions.
- **Automated Engine Checks:**
  1. *Broken Wiring & Disconnected Calls:* Client API calls targeting non-existent endpoints (parameter-aware matching with monorepo boundary isolation).
  2. *Route & Method Mismatches:* HTTP method discrepancies between client call and registered route handler (HTTP 405 risks).
  3. *Missing Authorization:* Sensitive route boundaries (`/admin`, `/delete`, mutative endpoints) lacking auth decorators or middleware.
  4. *Unvalidated Input & Injection Calibration:* Direct user-controlled input in SQL/shell sinks (Critical) vs defensive unparameterized construction patterns (Medium).
  5. *Persistence & Transaction Boundaries:* Function-scoped inspection of multiple database mutations lacking atomic transaction wrappers.
  6. *Error Handling Risks:* Silent exception swallowing (`except: pass`, empty `catch`).
  7. *Sensitive Data Exposure:* Hardcoded API keys, bearer tokens, or personal access credentials.
  8. *Unfinished Implementations:* Stubs, `TODO`, `panic("not implemented")`, or missing logic in touched files.
  9. *Regression Test Gaps:* Modified route handlers lacking response assertion tests.
- **Mandatory 7-Point Finding Structure:**
  1. What the code currently does.
  2. What can go wrong.
  3. Evidence with exact file and line locations.
  4. The likely root cause.
  5. A minimal recommended fix.
  6. The impact of leaving it unresolved.
  7. Why the finding could be a false positive.

---

## ⚡ Engineering Principles & Investigation Discipline

Ghost Hunt incorporates battle-tested engineering principles to deliver actionable, high-confidence investigations:

### 1. The Ladder of Minimal Intervention (Smallest Complete Solution)
Before recommending or writing code, evaluate through this progression:
1. **YAGNI (Eliminate):** Does this logic or abstraction need to exist at all? Dead flexibility is debt.
2. **Reuse:** Does an existing project utility, helper, or model already solve this?
3. **Stdlib / Platform Native:** Can the language standard library or runtime platform handle this without new dependencies?
4. **Smallest Complete Fix:** Recommend the most surgical patch that completely resolves the root cause. Never add speculative abstractions.

### 2. Caller / Callee Data Flow Tracing
Never evaluate code in isolation. Trace upstream callers (who provides the input?) and downstream callees (what sinks and mutations are triggered?). Verify parameter types, nullability, and error handling across every hop.

### 3. Workload, Concurrency & Transaction Reasoning
- **Data Risk:** Ensure multiple database mutations inside a single operation execute within an atomic transaction boundary.
- **Workload Impact:** Inspect loops for N+1 database queries or redundant HTTP requests.
- **Shared State:** Scrutinize concurrency hazards, unclosed connections, and resource leaks.

### 4. Concrete Failure Scenarios
Every finding must describe the exact, realistic scenario under which the failure manifests (e.g. "When a user submits the checkout form with a discount code, `items` is None, raising AttributeError: 'NoneType' object has no attribute 'total' and returning HTTP 500"). Never issue generic stylistic warnings.

### 5. Explicit Uncertainty & Calibrated Severity
- If a check cannot be proven due to missing test state, permissions, or environments, declare it **`UNKNOWN`**. Never guess.
- Distinguish confirmed defects (proven exploitability, broken routes) from defensive pattern candidates requiring owner confirmation.

---

## 🔗 Feature Connection Map & Cross-Layer Contracts

Ghost Hunt's signature differentiator is the end-to-end **8-Layer Feature Connection Pipeline**:

```text
1. UI Action ──> 2. Client Call ──> 3. Route Handler ──> 4. Controller
                                                                │
8. Test Check <── 7. Response UI <── 6. Database Model <── 5. Service
```

### Cross-Layer Contract Rules:
- **Application Boundary Isolation:** In monorepos, client calls in Application A are never satisfied by routes in unrelated Application B without an explicit gateway or proxy contract.
- **Method & Path Consistency:** Client HTTP verbs and URL paths must match backend route declarations exactly.
- **Verifiable Test Assertion Evidence:** Static test coverage requires explicit assertion statements or conditional checks on response status/body; passive reads or logging do NOT qualify as assertions.
- **Truthful Runtime Verification:** `PASS` requires uncontaminated execution against authoritative expectations. Static inspection never claims runtime verification.

---

## 🛡️ Safety Defaults & Operational Tiers

Ghost Hunt strictly enforces four operational safety levels:

| Tier | Category | Safety Policy | Permitted Actions |
|---|---|---|---|
| **Level 1** | **Source Inspection** | **Safe by default.** | Static file discovery, AST parsing, test reading. Never imports or executes untrusted code to discover structure. |
| **Level 2** | **Runtime Read-Only** | **Safe in test environments.** | Safe HTTP probes (`GET`, `HEAD`, `OPTIONS`) and read-only database queries (`SELECT` only, capped at 1,000 rows). |
| **Level 3** | **Runtime Mutations** | **Requires user authorization.** | State-altering HTTP methods (`POST`, `PUT`, `PATCH`, `DELETE`) and browser form submissions. Must target disposable test environments with synthetic data. |
| **Level 4** | **Database Writes** | **Strictly isolated.** | Direct database mutations (`INSERT`, `UPDATE`, `DELETE`). Strictly prohibited against production databases. Restricted to disposable temporary databases with cleanup and re-seeding. |

### Absolute Safety Guardrails:
- **Production Guardrail:** Block all checks against production environments by default.
- **Credential Redaction:** Automatically redact passwords, API keys, Bearer tokens, and email addresses from evidence logs.
- **No Code Edits Without Approval:** Always present proposed fixes as diffs for user approval before modifying code.

---

## 📚 Progressive Disclosure & Reference Index

Load only the reference documents needed for your specific task:

- [references/project-context.md](references/project-context.md) — Project detection, scope locking, and example isolation.
- [references/language-support.md](references/language-support.md) — Multi-language detection vs analysis support and capability matrix.
- [references/ghost-features.md](references/ghost-features.md) — Ghost feature detection playbook and 8-layer connection graph.
- [references/repository-audit.md](references/repository-audit.md) — Playbook for `/ghost-hunt audit` whole-repository inspections.
- [references/decision-tree.md](references/decision-tree.md) — Mode selection, native vs CLI tools, and safety gates.
- [references/discovery-understanding.md](references/discovery-understanding.md) — Codebase inspection and data flow tracing.
- [references/journey-mapping.md](references/journey-mapping.md) — Designing discrete journey checkpoints and expectation sources.
- [references/verification-playbook.md](references/verification-playbook.md) — Testing guides, scenario isolation, and PASS evidence contract.
- [references/investigation-root-cause.md](references/investigation-root-cause.md) — Root cause diagnosis, stack tracing, and minimal fix design.
- [references/regression-verification.md](references/regression-verification.md) — Post-fix regression verification procedures.
- [references/evidence-reporting.md](references/evidence-reporting.md) — Evidence sanitization, redaction, and reporting standards.
- [references/troubleshooting.md](references/troubleshooting.md) — Environment blockers, permissions, and tool recovery.
- [references/optional-cli.md](references/optional-cli.md) — Usage of the optional Python verification CLI engine.
- [templates/report-template.md](templates/report-template.md) — Reusable Markdown report template.
- [templates/journey-template.json](templates/journey-template.json) — Reusable JSON journey schema template.
- [examples/checkout-investigation.md](examples/checkout-investigation.md) — Real-world example investigation of a checkout feature.
