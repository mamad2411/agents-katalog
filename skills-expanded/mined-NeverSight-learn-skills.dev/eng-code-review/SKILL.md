---
name: eng-code-review
description: Perform comprehensive technical code review across git diffs or full repositories with configurable profiles (standard or strict) and spec conformance checks. Use before committing changes, creating PRs, or conducting architecture and security audits.
---

# Code Review

Perform structured, high-signal technical code review with actionable feedback, concrete fix recommendations, and spec conformance verification.

## Review Philosophy & Core Rules

- **Correctness & Spec Alignment First**: Logic bugs, off-by-one errors, contract violations, and discrepancies against frozen specifications (`specs/<feature>/`) are top priority.
- **Security Always**: Validate input sanitization, authentication/authorization, secret leakage, and dependency risks.
- **Minimal, Actionable Feedback**: Provide concrete code snippets or diffs rather than vague complaints.
- **Zero Placeholder Policy (Strict Profile)**: In strict mode, reject any TODOs, mock data, stub implementations, or unhandled errors.

---

## Profiles & Scopes

- **Scopes**:
  - `diff` (Default): Review uncommitted changes or branch diff against base.
  - `staged`: Review staged git changes before commit.
  - `repo`: Review the entire codebase for architecture integrity and consistency.
- **Profiles**:
  - `standard` (Default): Fast, pragmatic review focusing on bugs, security, maintainability, and tests.
  - `strict`: Enforce spatial architecture integrity (acyclic graph, layer isolation), zero mocks, zero dead code, complete error coverage, and strict spec conformance.

---

## Review Process

### 1. Collect Review Context
1. Check git status and inspect diffs (`git diff`, `git diff --staged`, or `git log origin/main...HEAD`).
2. Identify changed files, primary business intent, and check for relevant `specs/<feature-name>/`.
3. Locate impacted entry points (APIs, routes, CLI, migrations).

### 2. Multi-Dimensional Evaluation
Evaluate changes across 6 key dimensions:
1. **Spec & Contract Conformance**: If `specs/<feature>/` exists, verify all acceptance criteria and API schemas are strictly satisfied without scope drift.
2. **Logic & Correctness**: Contract validation, null/undefined safety, race conditions, lifecycle cleanup.
3. **Security & Data Safety**: Injection vectors, authz bypasses, secret handling.
4. **Architecture & Spatial Integrity**: Layer boundaries, dependency direction, pattern consistency.
5. **Performance & Resources**: N+1 queries, memory leaks, unclosed handles/streams.
6. **Test Completeness**: Unit test coverage for new logic, boundary conditions, negative test cases.

### 3. Severity Categorization
- `[CRITICAL]`: Must be fixed before merge (causes crash, data loss, security flaw, or regression).
- `[WARNING]`: Potential bug, spec deviation, performance bottleneck, or edge case gap.
- `[SUGGESTION]`: Code readability, minor refactoring, or naming polish.

---

## Second Independent Review (Post-Fix Verification)

After `eng-review-fix` resolves findings, re-run review on the remediation diff with an **independent reviewer stance**: assume prior fixes may be incomplete, wrong, or introduce new issues. This pass differs from the first:

1. **Fresh eyes scope**: Review only the fix commits/diff against the original findings list.
2. **Fix quality checks**: Each fix actually addresses root cause (not symptom patch), matches codebase conventions, and adds regression coverage.
3. **No-regression sweep**: Verify fixes did not silently weaken tests, delete failing assertions, or narrow validation scopes.
4. **Verdict**: `[ALL RESOLVED]` closes the loop; any reopened finding loops back to eng-review-fix.

---

## Output Review Report

Save report to `.agents/eng-code-reviews/<timestamp>.md`:

```markdown
# Code Review Report

- **Scope**: <diff | staged | repo>
- **Profile**: <standard | strict>
- **Spec Reference**: `specs/<feature>/` (or N/A)
- **Target**: <Branch / Files reviewed>

## Summary Matrix
| Severity | Count | Status |
|---|---|---|
| 🚨 Critical | X | Action Required |
| ⚠️ Warning | Y | Review Needed |
| 💡 Suggestion | Z | Optional |

## Detailed Findings

### [CRITICAL] `src/services/auth.ts:42` - <Concise Title>
- **Category**: Security / Correctness / Spec Alignment
- **Description**: <Why this is an issue>
- **Recommended Fix**:
  ```diff
  - const user = await findUser(req.params.id);
  + const user = await findUserByIdAndTenant(req.params.id, req.tenantId);
  ```

### [WARNING] `src/controllers/order.ts:88` - <Concise Title>
...

## Verdict: [APPROVED | CHANGES REQUESTED]
```
---

## Checkable Completion Criteria

- [ ] Review covers all six dimensions relevant to the change surface (spec conformance, correctness, security, architecture, performance, tests).
- [ ] Every finding carries severity, category, file:line location, and a concrete diff-style recommended fix.
- [ ] Summary matrix counts match the detailed findings list exactly.
- [ ] Final verdict is explicit: APPROVED or CHANGES REQUESTED.
