---
name: pr-review
description: >
  Automated PR review and code quality analysis skill. Activate when the user asks to
  review a pull request, audit code quality, check a codebase, scan for bugs or security
  issues, or validate a plan before shipping. Fans out parallel sub-agents — one per
  review lens (security, architecture, performance, dependencies, logging, testing,
  documentation, accessibility) — then synthesises a structured severity-graded report
  with confidence scores, effort estimates, and actionable suggestions.
  Use when user says: review this PR, audit my code, check for security issues, review
  my changes, scan for bugs, quality check, code review, pre-ship audit.
  First response: "PR Review skill active. Paste the diff, file paths, or describe what
  to review. I'll run every lens in parallel and give you a structured report."
license: Apache 2.0
---

# Automated PR Review & Code Quality

A structured, multi-lens code review system. Eight lenses run in parallel so coverage
is deep, consistent, and fast. Output is always a severity-graded report with confidence
scores, effort estimates, and concrete before/after fixes — never vague observations.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/review` | Full review across all eight lenses |
| `/security` | Security lens only — OWASP Top 10, secrets, injection, auth |
| `/arch` | Architecture lens only — coupling, cohesion, SOLID, complexity |
| `/perf` | Performance lens only — N+1, memory leaks, Big-O, caching, async blocking |
| `/a11y` | Accessibility lens only — WCAG 2.1 AA, ARIA, keyboard, color contrast |
| `/deps` | Dependency lens only — outdated packages, license risk, supply chain |
| `/logging` | Logging & observability lens only — missing logs, PII leakage, trace IDs |
| `/testing` | Testing lens only — coverage gaps, brittle tests, missing edge cases |
| `/docs` | Documentation lens only — missing docstrings, stale comments, unclear APIs |
| `/fix <issue-id>` | Generate a ready-to-apply patch for a specific issue from the report |
| `/explain <issue-id>` | Educational deep-dive: why this is dangerous, not just how to fix it |
| `/issues` | Open GitHub issues for every P0 and P1 finding in the last report |
| `/pr-comment` | Post findings as inline GitHub PR review comments on specific lines |
| `/summary` | One-paragraph executive summary of the last report |
| `/tldr` | One-sentence summary for Slack/Discord notifications |
| `/diff` | New/resolved findings vs the previous review — compares against main branch baseline |
| `/iterate <issue-id>` | Fix an issue, then re-check just that code area — show what changed and confirm the fix |
| `/focus <issue-id>` | Deep dive on one finding: full context, step-by-step fix guide, before/after example |
| `/progress` | Show: findings fixed this session / findings still open / next priority |

---

## HIGH-LEVEL WORKFLOW

```
Input (diff / file paths / plan / repo)
    │
    ├─ Phase 0: Guardrails     ──  size check, privacy warning, load config
    │
    ├─ Phase 1: Reconnaissance ──  read files, understand intent, build context map
    │
    ├─ Phase 2: Fan-out        ──  launch all eight lenses in parallel (sub-agents)
    │     ├─ Lens A: Security
    │     ├─ Lens B: Architecture
    │     ├─ Lens C: Performance & Scalability
    │     ├─ Lens D: Dependencies
    │     ├─ Lens E: Logging & Observability
    │     ├─ Lens F: Testing
    │     ├─ Lens G: Documentation
    │     └─ Lens H: Accessibility (a11y)
    │
    ├─ Phase 3: Synthesis      ──  merge, deduplicate, confidence score, assign severities
    │
    ├─ Phase 4: Prioritization ──  effort estimates, CODEOWNERS tagging, team baseline
    │
    └─ Phase 5: Output         ──  structured report + optional CI/GitHub actions
```

---

## PHASE 0 — GUARDRAILS

Run before any other phase. Perform three checks and halt or warn as described.

### 0.1 Size Check

| Diff size | Behaviour |
| --- | --- |
| ≤20 files and ≤2 000 lines | Full review — all lenses, all severities |
| 21–100 files or 2 001–5 000 lines | High-signal mode — Security + Architecture + Performance only; P3 suppressed entirely |
| >100 files or >5 000 lines | Refuse full review. Respond: "This diff is too large for a full review. Specify files or lenses: `/review src/payments/ /security /arch`" |

In High-signal mode, always prioritise entry points (`main`, `index`, route handlers)
over utility/helper files regardless of diff order.

### 0.2 Privacy Warning

Before processing any code, display once per session:

```
⚠  Privacy notice: this review will process <N> lines of code through Claude.
   Confirm this repository is cleared for external analysis. [y/n]
```

Auto-approve for subsequent reviews in the same session.

Run a pre-flight secret scan (regex pass) and strip patterns matching:
- `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----`
- AWS key patterns (`AKIA[0-9A-Z]{16}`)
- Generic `password\s*=\s*"[^"]+"` assignments

Log the count of stripped patterns to the report footer. Security lens findings about
secrets are still raised based on the pattern match, without leaking the value.

### 0.3 Load Configuration

Look for `.pr-review.yml` in the repo root. If present, apply:

```yaml
# .pr-review.yml — all fields optional
ignore_paths:
  - "*.test.ts"
  - "migrations/"
  - "generated/"
severity_override:
  TRACE_ID_MISSING: P1      # escalate from default P2
max_findings: 25            # cap total findings to prevent review fatigue
lenses:                     # restrict lenses for this repo
  - security
  - performance
  - testing
confidence_threshold: medium  # suppress low-confidence findings
fail_on: p0_only            # CI exit-code threshold (default: p1)
```

Also read `CONTRIBUTING.md` and `STYLEGUIDE.md` if present to extract naming
conventions and testing requirements before flagging style deviations.

---

## PHASE 1 — RECONNAISSANCE

Before any lens fires, build a context map:

1. **Identify scope** — diff only, changed files, or entire repo?
2. **Detect language(s)** — infer from file extensions; load language-specific rules.
3. **Detect framework(s)** — React, Django, Spring, etc.; apply framework-specific checks.
4. **Read entry points** — `main`, `index`, `app`, route registrations.
5. **Understand intent** — read PR description, commit messages, linked issue titles.
6. **Check CODEOWNERS** — map changed files to owners for finding attribution.
7. **Flag obvious blockers** — syntax errors, merge conflicts, broken imports — report
   these immediately before continuing.

---

## PHASE 2 — REVIEW LENSES

### LENS A — SECURITY

> Goal: find every exploitable vulnerability before it ships.

**Checklist:**

- [ ] **Injection** — SQL, command, LDAP, XPath, template injection. Verify all user
  input is parameterised or sanitised before use.
- [ ] **Authentication & authorisation** — broken auth flows, missing `@login_required`
  / auth middleware, insecure direct object references (IDOR), JWT algorithm confusion.
- [ ] **Secrets & credentials** — hardcoded API keys, passwords, tokens in source or
  config files. Check `.env` handling; verify secrets are never logged.
- [ ] **Cryptography** — weak algorithms (MD5, SHA-1, DES, ECB mode), insufficient key
  lengths, predictable IVs, insecure random number generation.
- [ ] **Data exposure** — PII in logs, stack traces returned to clients, verbose error
  messages, over-permissive CORS, missing HTTPS enforcement.
- [ ] **CORS misconfiguration** — overly permissive `Access-Control-Allow-Origin: *` in
  production, credentials allowed with wildcard origin, missing `Vary: Origin`.
- [ ] **Deserialization of untrusted data** — `pickle.loads`, `yaml.load` (vs `safe_load`),
  Java `ObjectInputStream`, PHP `unserialize` on user-controlled input.
- [ ] **XXE (XML External Entity)** — XML parsers with external entity resolution enabled
  when processing user-supplied XML.
- [ ] **Path traversal in file operations** — user-controlled path components in `open()`,
  `fs.readFile()`, `File()` calls without normalisation and boundary checks.
- [ ] **Input validation** — missing length/type/range checks at system boundaries,
  unvalidated redirects.
- [ ] **Dependency vulnerabilities** — known CVEs in direct and transitive dependencies
  (cross-reference with dependency lens).
- [ ] **Supply chain** — typosquatted packages, unpinned versions, absent lockfile
  integrity checks.
- [ ] **SSRF / open redirect** — any URL constructed from user-controlled input that
  makes server-side HTTP requests.
- [ ] **Rate limiting & DoS** — unbounded loops driven by user input, missing pagination
  limits, expensive regex on untrusted strings (ReDoS).

**Severity mapping for this lens:**
- `P0 (Critical)` — exploitable without authentication or with low-privilege access.
- `P1 (High)` — exploitable with authenticated access or under specific conditions.
- `P2 (Medium)` — defence-in-depth gap; not directly exploitable but raises risk.
- `P3 (Low)` — best-practice deviation with minimal direct risk.

---

### LENS B — ARCHITECTURE

> Goal: identify structural problems that compound over time.

**Checklist:**

- [ ] **Single Responsibility** — functions/classes doing more than one job. Flag any
  function >30 lines that mixes concerns (I/O + business logic, for example).
- [ ] **Coupling** — tight coupling between unrelated modules, circular imports,
  god objects/classes, feature envy.
- [ ] **Cohesion** — modules with unrelated responsibilities, poor layer separation
  (e.g., database queries inside UI components).
- [ ] **Complexity** — cyclomatic complexity >10 in a single function, deeply nested
  conditionals (>3 levels), long parameter lists (>4 params without a data class).
- [ ] **Naming** — misleading names, abbreviations, Hungarian notation, generic names
  (`data`, `info`, `temp`, `manager`, `utils` with >15 methods).
- [ ] **Error handling** — swallowed exceptions (`except: pass`), bare `catch (e) {}`,
  missing error propagation, inconsistent error shapes across an API.
- [ ] **Transaction boundaries** — database transactions that span external HTTP calls,
  holding locks across the wire; missing rollback on partial failure.
- [ ] **Circuit breaker / retry logic** — external service calls with no timeout, no
  retry with backoff, and no circuit breaker — a single dependency failure takes down
  the entire system.
- [ ] **Idempotency** — mutation endpoints (`POST /charge`, `POST /send-email`) without
  an idempotency key, making safe client retries impossible.
- [ ] **DRY violations** — copy-pasted logic blocks >5 lines appearing more than once.
- [ ] **Dead code** — unreachable branches, unused exports, commented-out code blocks.
- [ ] **Abstraction level** — mixed abstraction levels inside a single function; leaky
  abstractions exposing implementation details to callers.

---

### LENS C — PERFORMANCE & SCALABILITY

> Goal: catch efficiency problems before they become production incidents under load.

**Checklist:**

- [ ] **N+1 queries** — ORM loop issuing one DB query per iteration; flag and suggest
  eager loading (`select_related`, `JOIN`, `$lookup`).
- [ ] **Synchronous I/O in async paths** — blocking file read, `requests.get()`, or
  `time.sleep()` inside an `async def` / event-loop context.
- [ ] **Unbounded memory growth** — appending to a list/dict in a loop with no size
  cap; loading an entire table into memory; accumulating results without streaming.
- [ ] **Missing pagination** — list endpoints returning all rows without `LIMIT`/`OFFSET`
  or cursor-based pagination.
- [ ] **Big-O inefficiency in hot paths** — O(n²) or worse algorithm where O(n log n)
  or O(n) alternative exists; nested loops over large collections.
- [ ] **Caching strategy gaps** — expensive computations (external API calls, heavy DB
  aggregations) called on every request with no memoisation or cache layer.
- [ ] **Database query plans** — missing composite indexes on multi-column `WHERE`
  clauses; `SELECT *` where specific columns suffice; non-SARGable predicates.
- [ ] **Async blocking** — `Promise.all` missing where sequential `await` chains could
  be parallelised; CPU-bound work on the event loop without offloading to a worker.
- [ ] **Memory leaks** — event listeners registered without cleanup, timers not cleared,
  closures retaining large objects, streams not destroyed on error.
- [ ] **Connection pool exhaustion** — opening new DB/HTTP connections per request
  instead of reusing a pool; pool size not configured for expected concurrency.

---

### LENS D — DEPENDENCIES

> Goal: keep the dependency tree lean, secure, and legally safe.

**Checklist:**

- [ ] **Outdated packages** — dependencies >1 major version behind their latest stable
  release; note breaking-change risk.
- [ ] **Unused dependencies** — packages imported in `package.json` / `requirements.txt`
  / `go.mod` but never `import`-ed in code.
- [ ] **Duplicate functionality** — two packages doing the same job (e.g., `axios` and
  `node-fetch` in the same project).
- [ ] **Bundle weight** — heavy packages pulled in for a single utility function
  (prefer tree-shakeable alternatives or inline the function).
- [ ] **License compliance** — GPL/AGPL in a proprietary project, license conflicts
  between dependencies.
- [ ] **Lockfile hygiene** — missing `package-lock.json` / `poetry.lock`, lockfile not
  committed, lockfile out of sync with manifest.
- [ ] **Pinning strategy** — overly loose (`*`, `>=1`) or overly strict (exact SHA for
  everything) pinning; recommend `~=` / `^` semantics where appropriate.
- [ ] **Deprecated / abandoned packages** — no commits in >2 years, archived repo,
  single-maintainer bus-factor risk; flag and suggest active alternatives.
- [ ] **Native dependency risk** — packages with native bindings (`.node`, `.so`, `.dll`)
  that may break across OS/architecture; flag for multi-platform deployments.
- [ ] **Peer-dependency mismatches** — declared peer deps not satisfied by installed
  versions.

---

### LENS E — LOGGING & OBSERVABILITY

> Goal: ensure the system is debuggable in production without leaking sensitive data.

**Checklist:**

- [ ] **Coverage** — every external call (HTTP, DB, queue, cache) has at least one log
  entry at the start and on error/success.
- [ ] **Log levels** — correct use of `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`.
  Avoid `INFO` for every message; avoid `DEBUG` left on in production code paths.
- [ ] **Structured logging** — logs are machine-parseable (JSON, key=value). No raw
  `print()` / `console.log()` in production paths.
- [ ] **PII leakage** — passwords, tokens, emails, PII must never appear in log output.
  Verify masking/redaction is applied before logging request/response bodies.
- [ ] **Trace & correlation IDs** — distributed transactions include a `trace_id` or
  `request_id` threaded through all log lines.
- [ ] **Error context** — exceptions are logged with full stack trace + request context,
  not just `"something went wrong"`.
- [ ] **Metrics & alerts** — critical paths (payments, auth, data mutations) emit
  a counter or histogram metric; alert thresholds are defined.
- [ ] **Silent failures** — code paths that catch exceptions and continue without any
  log entry.

---

### LENS F — TESTING

> Goal: find coverage gaps and brittle tests before they become production incidents.

**Checklist:**

- [ ] **Coverage gaps** — new code paths with no corresponding test; branches inside
  conditionals that are never exercised.
- [ ] **Happy-path only** — tests that only cover the success case; missing tests for
  error paths, boundary conditions, and empty/null inputs.
- [ ] **Edge cases** — off-by-one errors, empty collections, `null`/`undefined`,
  maximum-length inputs, concurrent access, timezone edge cases.
- [ ] **Test isolation** — tests sharing state via global variables, module-level side
  effects, or real external services (DB, HTTP) without mocking.
- [ ] **Brittle selectors** — UI tests using implementation-detail selectors (CSS class
  names, internal state) instead of accessible roles/labels.
- [ ] **Assertion quality** — `assert response` (truthy check) instead of
  `assert response.status_code == 200`; missing error message in assertion.
- [ ] **Test naming** — test names that don't describe the scenario
  (`test_1`, `testFoo`) making failures hard to diagnose.
- [ ] **Flaky tests** — tests with `sleep()` / fixed timeouts, order-dependent tests,
  tests seeded with wall-clock time.
- [ ] **Property-based testing gaps** — complex business logic (parsers, validators,
  financial calculations) without fuzz / property-based tests (Hypothesis, fast-check).
- [ ] **Contract testing** — API changes without consumer contract validation (Pact);
  service boundary regressions caught only in integration or staging.
- [ ] **Integration vs unit balance** — over-reliance on slow end-to-end tests for
  logic that could be unit-tested; or inverse: mocking so heavily that integration
  bugs are invisible.

---

### LENS G — DOCUMENTATION

> Goal: ensure the code is understandable by a new engineer without a walkthrough.

**Checklist:**

- [ ] **Public API docstrings** — every exported function, class, and method has a
  docstring explaining purpose, params, return value, and exceptions raised.
- [ ] **Inline comments** — complex business logic, non-obvious algorithms, and
  workarounds have a `# why` comment explaining intent, not just `# what`.
- [ ] **Stale comments** — comments that describe code that no longer exists or
  behaviour that has changed.
- [ ] **README coverage** — new environment variables, config options, CLI flags, or
  setup steps reflected in README / CONTRIBUTING docs.
- [ ] **Changelog / migration notes** — breaking changes in public APIs documented in
  CHANGELOG.md or a migration guide.
- [ ] **Type annotations** — typed languages: all public signatures have types; Python:
  all public functions have PEP 484 annotations.
- [ ] **Example usage** — complex utilities or SDK-style modules include at least one
  runnable example.
- [ ] **TODO hygiene** — `TODO`/`FIXME` comments have an owner and a linked issue; stale
  TODOs (>90 days old) are flagged.

---

### LENS H — ACCESSIBILITY (a11y)

> Goal: catch WCAG 2.1 AA violations before they create legal or UX debt.
> Skip this lens automatically for non-UI code (pure backend, CLI, IaC).

**Checklist:**

- [ ] **Missing alt text** — `<img>`, `<svg>`, and icon buttons without meaningful `alt`
  or `aria-label` attributes.
- [ ] **Improper ARIA roles** — `role` values that contradict native HTML element
  semantics; redundant `role="button"` on `<button>`; invalid role hierarchies.
- [ ] **Keyboard trap** — modal dialogs, dropdowns, or custom widgets that don't return
  focus to the trigger element on close, or trap Tab without an escape route.
- [ ] **Focus management** — programmatic focus not moved to newly opened dialogs,
  alerts, or route changes; invisible focus ring (`:focus { outline: none }` without
  a visible replacement).
- [ ] **Color contrast** — text/background combinations failing WCAG AA ratio (4.5:1
  normal text, 3:1 large text); information conveyed by color alone.
- [ ] **Form labelling** — inputs without associated `<label>`, `aria-label`, or
  `aria-labelledby`; required fields not marked with `aria-required`.
- [ ] **Interactive element sizing** — touch targets smaller than 44×44 px (WCAG 2.5.5).
- [ ] **Motion & animation** — animations not respecting `prefers-reduced-motion`;
  auto-playing video/audio without a pause control.
- [ ] **Language declaration** — missing `lang` attribute on `<html>`; mixed-language
  sections without a `lang` override on the containing element.
- [ ] **Semantic structure** — skipped heading levels (`<h1>` → `<h3>`); landmark
  regions (`<main>`, `<nav>`, `<aside>`) missing or misused.

---

## PHASE 3 — SYNTHESIS RULES

When merging findings from all lenses:

1. **Deduplicate** — if two lenses flag the same function, emit one finding with both
   lens tags.
2. **Promote severity** — a finding tagged by two or more lenses is promoted one
   severity level (e.g., P2 → P1).
3. **Group by file** — sort findings by file path, then by line number.
4. **Count totals** — report `P0 / P1 / P2 / P3` counts in the header.
5. **Confidence scoring** — assign `confidence: high | medium | low` to each finding:
   - `high` — definitive code evidence (e.g., f-string SQL query with user input).
   - `medium` — likely issue but context-dependent (e.g., missing auth check that may
     be covered by middleware not visible in the diff).
   - `low` — pattern match with high false-positive rate; surface as "Consider
     checking…" not as a hard assertion.
6. **Apply configuration** — honour `ignore_paths`, `severity_override`, and
   `max_findings` from `.pr-review.yml` if loaded in Phase 0.
7. **Trim noise** — suppress P3 findings if total finding count >30 (or `max_findings`
   config value). Always append `(N P3 findings suppressed — run /full to see all)` to
   the report footer when any P3s are trimmed.
8. **Respect suppression comments** — if a flagged line carries a `# pr-review-ignore: REASON`
   comment, omit the finding from the report and record the suppression in the footer:
   `Suppressed: <ID> — <REASON>`.

---

## PHASE 4 — PRIORITIZATION

After synthesis, annotate each finding with:

### Effort Estimate

| Tag | Meaning |
| --- | --- |
| `effort: trivial` | <5 min — rename, add a comment, single-line fix |
| `effort: small` | <30 min — replace one function, add one test case |
| `effort: medium` | Hours — refactor a module, add a feature flag |
| `effort: large` | Refactor — multi-file change, requires design discussion |

### CODEOWNERS Attribution

If a `CODEOWNERS` file exists in the repo root or `.github/`, append the responsible
owner handle to each finding:

```
│  Owner   : @payments-team
```

### Team Baseline

If previous review reports exist in the conversation, compute and append to the
report footer:

```
Trend: this PR introduces N P1s. Session average: M P1s per review.
```

---

## PHASE 5 — OUTPUT FORMAT

### Report Header

```
═══════════════════════════════════════════════════════════
  PR REVIEW REPORT
  Scope   : <files reviewed / diff size>
  Mode    : <full | high-signal>
  Lenses  : <active lenses> [<skipped lenses> skipped]
  Summary : <P0_count> critical  <P1_count> high  <P2_count> medium  <P3_count> low
═══════════════════════════════════════════════════════════
```

### Finding Block (one per issue)

```
┌─ [<ID>] <SEVERITY> · <LENS>
│  File       : path/to/file.ext  (line <N>–<M>)
│  Issue      : <one-sentence description of the problem>
│  Impact     : <what goes wrong if this is not fixed>
│  Confidence : <high | medium | low>
│  Effort     : <trivial | small | medium | large>
│  Owner      : <@handle from CODEOWNERS — omit if no CODEOWNERS file>
│  Fix        : <concrete, actionable suggestion — include code snippet when helpful>
│  Refs       : <OWASP link / CWE / RFC / relevant doc — only when directly applicable>
└──────────────────────────────────────────────────────────
```

### Severity Legend

| Severity | Emoji | Meaning | Expected action |
|---|---|---|---|
| `P0 Critical` | 🔴 | Exploitable, data-loss, or outage risk | Block merge immediately |
| `P1 High` | 🟠 | Significant bug or security gap | Fix before merge |
| `P2 Medium` | 🟡 | Quality or maintainability debt | Fix in follow-up PR |
| `P3 Low` | 🔵 | Style, minor inconsistency, nice-to-have | Backlog or skip |

### Report Footer

```
───────────────────────────────────────────────────────────
  RECOMMENDED ACTIONS
  1. Address all P0s before merge.
  2. <specific top recommendation based on findings>
  3. <second specific recommendation>
  Run `/fix <ID>` for a ready-to-apply patch on any finding.
  Run `/explain <ID>` for an educational deep-dive on any finding.
  Run `/issues` to open GitHub issues for P0 + P1 findings.
  Run `/pr-comment` to post findings as inline review comments.
  <Trend line if prior reports exist in session>
  <Suppression notes: Suppressed: <ID> — <REASON>>
  <Pre-flight secret strips: N patterns redacted before analysis>
  <P3 suppression note if applicable>
───────────────────────────────────────────────────────────
```

---

## GITHUB INTEGRATION

When the user runs `/issues` after a report:

1. **Authenticate** — use the available GitHub tool or confirm the user's `gh` CLI is
   authenticated (`gh auth status`).
2. **One issue per finding** (P0 and P1 only by default; ask before opening P2).
3. **Issue title format**: `[pr-review][<SEVERITY>] <one-sentence description>`
4. **Issue body template**:

```markdown
## Finding

**ID**: <report-ID>
**Severity**: <P0/P1>
**Lens**: <lens name>
**File**: `path/to/file.ext` (line N–M)

## Problem

<Issue description from report>

## Impact

<Impact description from report>

## Suggested Fix

<Fix description from report — include code snippet>

## References

<Refs from report>

---
*Opened automatically by the `pr-review` skill.*
```

5. **Label issues** using this mapping:
   - P0 → `bug`
   - P1 Security lens → `security`
   - P1 other lenses → `enhancement`
   - P2/P3 → `tech-debt`
6. **Report back** with a list of created issue URLs.

### `/pr-comment` — Inline Review Comments

Post findings as inline review comments directly on the PR diff:

1. Create a pending review via the GitHub API
   (`POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews`).
2. For each finding with a line number, add a comment at that exact diff line.
3. For findings without a precise line (e.g., architectural patterns), add a top-level
   review comment.
4. Submit the review with body: `PR Review skill — <summary line from report>`.
5. P0 findings → submit as `REQUEST_CHANGES`; P1/P2 → `COMMENT`; P3 → omit from
   inline comments (include only in the submitted review body).

---

## FALSE POSITIVE MANAGEMENT

Developers will abandon automated review tools if they can't suppress noise.

### In-code Suppression

Place a comment on the flagged line to suppress a specific finding:

```python
# pr-review-ignore: intentional MD5 — used for cache key only, not security
cache_key = hashlib.md5(url.encode()).hexdigest()
```

Rules:
- The comment must include a `REASON` after the colon.
- The finding is omitted from the report and recorded in the footer.
- Suppressions without a reason are rejected and reported as a new `P3` finding.

### Confidence-Based Behaviour

| Confidence | Report behaviour |
| --- | --- |
| `high` | Full finding block with all fields |
| `medium` | Full finding block; prefix Issue with "Likely:" |
| `low` | Compact one-liner only, grouped in a `CONSIDER CHECKING` section at the bottom |

Low-confidence findings are never mixed with high/medium findings. The `CONSIDER
CHECKING` section is collapsible and does not contribute to the P0/P1/P2/P3 totals
in the header.

### Pattern Learning

When the user responds "not an issue" or dismisses a finding during the session,
record the suppression in session state:

```
Dismissed: <lens> · <file-pattern> · <code-pattern>
```

Apply suppression to the same pattern in subsequent `/review` calls within the session.

---

## CI/CD INTEGRATION

### Exit Codes (for scripted / pipeline use)

| Condition | Exit code | Behaviour |
| --- | --- | --- |
| P0 finding(s) present | `1` | Always blocks CI |
| P1 finding(s) present | `1` (default) / `0` (if `fail_on: p0_only` in config) | Configurable |
| P2/P3 only | `0` | CI passes |
| Review error / timeout | `2` | Infrastructure failure — do not block merge |

### SARIF Output

Run `/review --sarif` to emit findings in SARIF 2.1.0 format, compatible with
GitHub Advanced Security, GitLab SAST, and the VS Code SARIF Viewer extension:

```json
{
  "version": "2.1.0",
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "runs": [{
    "tool": { "driver": { "name": "pr-review", "version": "2.0.0" } },
    "results": [{
      "ruleId": "SEC-001",
      "level": "error",
      "message": { "text": "<issue description>" },
      "locations": [{
        "physicalLocation": {
          "artifactLocation": { "uri": "src/api/users.py" },
          "region": { "startLine": 42, "endLine": 44 }
        }
      }]
    }]
  }]
}
```

Upload to GitHub Advanced Security:

```yaml
# .github/workflows/pr-review.yml
- name: PR Review
  run: claude --skill pr-review --review --sarif > results.sarif
- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```

---

## LANGUAGE-SPECIFIC RULE EXTENSIONS

Load additional rule sets based on detected language:

| Language | Extra checks to apply |
|---|---|
| **Python** | Type annotations (PEP 484), `__all__` exports, mutable default args, `except Exception` breadth |
| **TypeScript / JS** | `any` overuse, missing `null` checks, `async` without `await`, prototype pollution |
| **Java / Kotlin** | Checked exceptions swallowed, thread-safety of shared state, `equals`/`hashCode` contract |
| **Go** | Error return ignored (`_`), goroutine leak, unbuffered channel in hot path |
| **SQL** | Implicit type coercions, missing `WHERE` on `UPDATE`/`DELETE`, non-SARGable predicates |
| **Terraform / IaC** | Public S3 buckets, wildcard IAM policies, unencrypted storage, missing state locking |

---

## DIFF MODE

When the user runs `/diff`, compare the current review against the main branch baseline
and any prior review in the session:

1. **Require baseline** — if no prior report exists, respond:
   `"No previous report found. Run /review first, make your changes, then run /diff."`
2. **Main branch comparison** — compare findings against the pre-existing state of `main`:
   - Pre-existing debt on `main` that the PR did not introduce → label `[PRE-EXISTING]`,
     surface as `P3` only (do not block merge for inherited debt).
   - New issues introduced by this PR → label `[NEW]`.
3. **Identify resolved findings** — findings in a prior session report absent from the
   current report. Mark with `[FIXED]`.
4. **Regression detection** — automatically escalate severity by one level if:
   - A test file was deleted or a test function was removed in the diff.
   - An authentication/authorisation check was deleted in the diff.
   - A rate-limit or input-validation call was removed in the diff.
5. **Identify unchanged findings** — present in both reports. Compact one-liner only:
   `[UNCHANGED] <ID> · <severity> · <one-line description>`
6. **Output format** — standard finding block for `[NEW]`; compact one-liner for
   `[UNCHANGED]`; ~~strikethrough~~ summary line for `[FIXED]`; italic note for
   `[PRE-EXISTING]`.
7. **Summary line**: `Delta: +N new  −M resolved  = K unchanged  (P pre-existing)`

---

## BEHAVIOUR RULES

- **Never be vague.** Every finding must name the exact file, line range, and fix.
- **Show code.** When suggesting a fix, always include a before/after snippet.
- **No false praise.** Do not comment on things that are fine; silence means approval.
- **Stay in scope.** Only flag what is in the diff or the explicitly specified files
  unless a cross-file dependency is directly relevant to a finding.
- **Respect intent.** Read the PR description and linked issue before flagging style
  deviations — the author may have had a reason.
- **Be fast.** Use parallel sub-agents for all eight lenses. Do not serialise lens
  execution unless there is a dependency.
- **One finding, one fix.** Do not bundle multiple problems into a single finding block.
- **Respect suppression.** Never re-raise a finding suppressed with `# pr-review-ignore`.
  Record suppressions in the footer for transparency.
- **Confidence transparency.** Never assert a low-confidence finding as fact. Use
  "Consider checking…" phrasing for low-confidence items.
- **Skip inapplicable lenses.** Do not run the a11y lens on pure backend code; do not
  run the performance lens on a README-only change. Log skipped lenses in the header.

---

## EXAMPLES

### Example: invoking a full review

> User: "Review this PR — here's the diff: [paste diff]"

Claude fans out eight parallel lens sub-agents, then synthesises:

```
═══════════════════════════════════════════════════════════
  PR REVIEW REPORT
  Scope   : 4 files changed, +312 −47 lines
  Mode    : full
  Lenses  : Security · Architecture · Performance · Deps · Logging · Testing · Docs · a11y
  Summary : 1 critical  3 high  5 medium  8 low
═══════════════════════════════════════════════════════════

┌─ [SEC-001] 🔴 P0 Critical · Security
│  File       : src/api/users.py  (line 42–44)
│  Issue      : Raw SQL query constructed with f-string from user input — SQL injection.
│  Impact     : Attacker can dump or delete the entire users table.
│  Confidence : high
│  Effort     : trivial
│  Fix        : Replace with parameterised query:
│               # Before
│               db.execute(f"SELECT * FROM users WHERE id = {user_id}")
│               # After
│               db.execute("SELECT * FROM users WHERE id = %s", (user_id,))
│  Refs       : OWASP A03:2021 — Injection · CWE-89
└──────────────────────────────────────────────────────────

...

───────────────────────────────────────────────────────────
  RECOMMENDED ACTIONS
  1. Address all P0s before merge.
  2. Replace MD5 password hashing with bcrypt (SEC-002).
  3. Add structured logging; remove plaintext password from log line (LOG-001).
  Run /fix <ID> for a ready-to-apply patch on any finding.
  Run /explain <ID> for an educational deep-dive on any finding.
  Run /issues to open GitHub issues for P0 + P1 findings.
  Run /pr-comment to post findings as inline review comments.
  Trend: this PR introduces 4 P1s. Session average: 1.2 P1s per review.
───────────────────────────────────────────────────────────
```

### Example: targeted security scan only

> User: "/security src/payments/"

Claude runs only the Security lens against all files under `src/payments/`.

### Example: generating a fix

> User: "/fix SEC-001"

Claude produces a complete, ready-to-apply patch in unified diff format.

### Example: educational mode

> User: "/explain SEC-001"

Claude explains SQL injection from first principles — what it is, why parameterised
queries prevent it, real-world breach examples, and links to OWASP and CWE.

---

## PROGRESS TRACKING AND ITERATION LOOP

### Session Progress Header

Every `/review`, `/fix`, `/iterate`, and `/progress` output begins with:

```
SESSION PROGRESS
  Fixed this session: [N] findings  |  Still open: [P0: X · P1: Y · P2: Z]
  Next priority: [issue-id] — [one-line description]
```

### `/iterate <issue-id>` Protocol

1. Show the before-state (the exact code that was flagged).
2. Ask the user to apply the fix (or apply it directly if the diff is accessible).
3. Re-scan only the affected file and line range — not the full diff.
4. Report the result: `[FIXED]` or `[STILL PRESENT]` or `[NEW ISSUE INTRODUCED]`.
5. Immediately show the next highest-priority finding.

```
ITERATE: SEC-001
  Before : db.execute(f"SELECT * FROM users WHERE id = {user_id}")
  Fix    : db.execute("SELECT * FROM users WHERE id = %s", (user_id,))
  Status : [FIXED] — SQL injection vector removed

  SESSION PROGRESS: 1/4 P0s fixed
  → Next: /iterate SEC-002 (hardcoded API key in config.py line 18)
```

### `/focus <issue-id>` Protocol

When the user needs to deeply understand a finding before fixing it:

1. Full context: what does this code do, why is this specific pattern dangerous?
2. Exploitation scenario: concretely, how would an attacker use this?
3. Step-by-step fix: each change needed, in order, with code snippets.
4. Verification: how to confirm the fix worked (test case or observable check).
5. Related issues: any other findings in this report that relate to the same root cause.

Do not move to the next finding until the user confirms this one is resolved.

### Example: CI pipeline integration

```yaml
# .github/workflows/pr-review.yml
- name: PR Review
  run: claude --skill pr-review --review ${{ github.event.pull_request.diff_url }}
  # Exits 1 on P0/P1 findings (configurable via fail_on), 0 on P2/P3 only

- name: PR Review (SARIF upload)
  run: claude --skill pr-review --review --sarif > results.sarif
- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```
