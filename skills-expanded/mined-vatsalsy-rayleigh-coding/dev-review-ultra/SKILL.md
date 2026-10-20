---
name: dev-review-ultra
description: >
  Use when the user says "ultra review", "deep review", "code audit", "PR
  review", or a PR touches JS/UI needing runtime or a11y review. NOT for
  quick scans (code-review).
---

# Review Ultra

## Scope and Intent
- High-signal, severity-ordered code review. Not style critique — correctness, security, performance, robustness.
- Operate **read-only**: do not edit files or apply patches.
- Every finding must cite exact file + line and explain concrete impact.
- Describe fixes with enough precision that a developer can apply them independently.

---

## Review Layers (apply all, in order)

### Layer 1 — Correctness
- Does the code do what the PR description claims?
- Are all edge cases handled: empty input, null/nil, overflow, concurrency, out-of-order events?
- Are error return values checked? Are panics/exceptions properly handled?
- Off-by-one errors, boundary conditions, loop termination.
- State machine integrity — are all transitions valid? Are invalid states representable?

### Layer 2 — Security
- **Injection**: SQL, shell, template, LDAP, XPath, format string, path traversal
- **Authentication / authorization**: missing auth checks, privilege escalation, IDOR, JWT issues
- **Secret exposure**: hardcoded credentials, API keys, tokens in code or logs
- **Deserialization**: unsafe object hydration, type confusion
- **Cryptography**: weak algorithms, ECB mode, hardcoded IVs/salts, custom crypto
- **Supply chain**: new dependencies added? Pinned? Known CVEs?
- **Input validation**: user-controlled data reaching dangerous sinks without sanitization
- **Race conditions / TOCTOU**: file system, shared state, concurrent mutation

### Layer 3 — Robustness
- Network calls: timeouts configured? Retry with backoff? Partial failure handling?
- Resource cleanup: files, connections, goroutines, threads, locks — all closed/released?
- Graceful degradation: what happens when a dependency is unavailable?
- Idempotency: safe to retry? Safe to call multiple times?
- Data integrity: transactions? Rollback on failure? Partial write scenarios?

### Layer 4 — Performance
- O(n²) or worse in hot paths (nested loops over large data, repeated linear searches)
- Unnecessary allocations in tight loops
- Blocking I/O on the main thread or in async contexts
- N+1 query patterns (ORM loops, repeated DB calls in iteration)
- Large memory copies when a reference/slice would suffice
- Missing caching for expensive repeated computations

### Layer 5 — Test Coverage
- For every changed module/function: is there a test in the diff?
- What is the blast radius if this change is wrong? Is that path tested?
- Are edge cases tested (null, empty, boundary, concurrent)?
- Are error paths tested (what if the DB call fails? the network call times out?)
- Are there brittle tests that only pass in specific environments?

### Layer 6 — Maintainability (bugs, not style)
- Complex logic with no comments → future bugs
- Deeply nested conditions that obscure control flow
- Magic numbers / magic strings with no constant or explanation
- Duplicated logic that will drift out of sync
- API contracts that are easy to misuse (wrong argument order, unclear semantics)

---

## Severity Scale

| Level | Label | Meaning |
|---|---|---|
| 🔴 P0 | Critical | Must fix before merge. Data loss, security breach, crash in prod path, auth bypass. |
| 🟠 P1 | High | Should fix before merge. Significant bug, performance regression, missing error handling in critical path. |
| 🟡 P2 | Medium | Fix soon, not blocking. Robustness gap, missing test for important path, suboptimal pattern. |
| 🔵 P3 | Low / Info | Nice to fix. Minor inefficiency, clarity improvement, potential future issue. |

P0 or P1 findings → request changes. P2/P3 only → comment. No findings → approve.

---

## Workflow

1. **Scope identification**: read PR title, description, linked issues. What is this change trying to do?
2. **Diff inspection**: set `BASE_BRANCH` from the PR's actual base, then run
   `git diff "origin/${BASE_BRANCH}"...HEAD` to understand the change.
3. **CodeRabbit seed pass (optional but recommended)**: if the `coderabbit` CLI
   is available, run the repository-aware `code-review` guard with
   `--switch-org -- --base "${BASE_BRANCH}"` and hold its structured findings as a
   cross-check. CodeRabbit does **not** replace any of the six layers — use it
   to catch what the manual pass missed, reconcile its severities against the
   P0–P3 scale, and fold surviving findings into the report with attribution.
   Inspect only: report meaningful issues and leave any fix/follow-up cycle to
   the implementation owner. Discard findings that the manual pass proves false.
4. **High-risk file prioritization**: auth, config, migrations, serialization, network, parsing — inspect these first regardless of size.
5. **Apply all six layers** — do not skip layers even for small PRs.
6. **JS/UI runtime checklist** (when JS/UI is touched):
   - Load-order and initialization guards
   - State flag lifecycle (`isLoading`, `isPending` set/reset on ALL branches including error)
   - Nullish / default handling (`??`, fallbacks, empty state UI)
   - Async race conditions (double-submit, stale closures, missing abort controllers)
   - Clipboard, file upload, permission APIs — success + failure + denied paths
   - Basic a11y: keyboard access, focus management, aria labels, color contrast
7. **Findings compilation**: order by severity, group by layer.
8. **Missing test audit**: for each P0/P1, flag if there is no test covering it.
9. **Output**: structured report (see format below).

## Lead judgement and corroboration

The reviewer, not CodeRabbit or a panel of models, owns the final conclusion.
Use automated/model findings to choose where to inspect; accept a finding only
when the changed code and a concrete reachable path, violated contract, or
direct test evidence support it. Tool agreement raises priority for inspection
but is never truth.

Include a short decision ledger after findings:

- **Accepted:** severity, exact evidence, and the predicate a repair must
  satisfy.
- **Deferred:** a plausible issue outside the review's delivery boundary,
  with its evidence and unresolved gate.
- **Dismissed:** false positive, duplicate, or preference-only suggestion,
  with the contrary source evidence.

An unresolved P0/P1 cannot be deferred as a convenience. A report with no
accepted findings must still say what direct paths and evidence were checked.

---

## Output Format

```
## Review: <PR title> (<OWNER>/<REPO>#<N>)

### Summary
+<additions>/-<deletions> across <N> files. <1-2 sentence overview of the PR's intent and top risk.>

### Findings

#### 🔴 P0 — <Short title>
**File**: `path/to/file.py:142`
**Layer**: Security / Correctness / Robustness / Performance / Tests / Maintainability
**Impact**: <Concrete impact — what goes wrong, when, for whom.>
**Detail**: <Code excerpt or description of the problematic pattern.>
**Fix direction**: <Specific, actionable guidance — not "fix this" but "validate X before passing to Y; use parameterized query instead of string concatenation">

#### 🟠 P1 — <Short title>
…

#### 🟡 P2 — <Short title>
…

#### 🔵 P3 — <Short title>
…

### Missing Tests
- `module/foo.py` — error path in `process_batch()` untested (covers the P1 finding above)
- …

### Decision Ledger
- Accepted — `path:line`: <direct evidence and repair predicate>
- Deferred — <boundary, evidence, unresolved gate>
- Dismissed — <suggestion and contrary evidence>

### Verification Steps
<Commands or test cases that would catch these issues:>
- `pytest tests/test_foo.py -k "test_empty_batch"`
- `curl -X POST /api/v1/batch -d ''` — should return 400, currently returns 500
```

---


## Gotchas

1. **Vague findings are worse than no findings** -- every finding must cite exact file+line and explain concrete impact. 'This could be a security issue' is not a finding. If you cannot articulate the blast radius, investigate further before reporting.
2. **Style comments inflate noise and waste reviewer time** -- this is not a style review. Reject the urge to flag formatting, naming conventions, or personal taste unless they directly cause bugs or obscure security-relevant logic.
3. **Skipping layers on small PRs causes misses** -- one-line PRs have hit P0 findings before. Apply all six layers even for trivial diffs; the size of the change is unrelated to its risk.
4. **Approving a PR with unresolved P0/P1 is explicitly prohibited** -- if findings exist at those levels, set review state to 'request changes'; do not approve and leave a comment.

## Guardrails

- Do not modify files, even if the fix is trivial.
- No broad refactors or style-only comments — focus on correctness, security, performance, robustness, and missing tests.
- Run tests only when explicitly requested OR when they are low-risk and clearly relevant.
- If command output is required, run the smallest scoped command and summarize.
- Do not approve a PR with unresolved P0 or P1 findings.
- Do not leave findings vague — if you can't explain the concrete impact, investigate further before reporting.
