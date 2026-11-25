---
name: pre-push-review
description: Reviews your local uncommitted changes before you push, in any language or framework (auto-detected), and scores Security, Performance, and Clean Code as Pass/Warn/Fail with an overall push-readiness recommendation. Use before pushing or committing — "check my changes before I push", "review my local diff", "is this safe to push?" — to get one Markdown report with evidence, impact, fixes, verification, references, and a per-measurement scorecard. Supports Quick, Standard, and Deep review modes. Do not use for feature implementation unless the user separately asks for fixes.
license: MIT
compatibility: Requires git. Stack-agnostic — auto-detects the language and framework from project manifests. GitHub CLI is not required. Designed for Codex and Claude Code using the Agent Skills open standard.
metadata:
  author: Ezzat Malak
  version: "1.0.0"
---

# Pre-Push Local Review

Review the user's **local changes before they are pushed** and write all results to exactly one Markdown report. Rate
**Security**, **Performance**, and **Clean Code** as **PASS / WARN / FAIL**, then give one overall **push
recommendation**. This skill is stack-agnostic: detect the language/framework first, then apply the right lens.

## Phase 0: Resolve inputs and review mode

Determine these before doing anything else, then echo them back in the report's Review Scope.

1. **Diff scope.** What counts as "local changes". Default to **uncommitted** — the working tree plus staged changes
   versus `HEAD`, including new untracked files. Honor an explicit request for another scope:
   - **uncommitted** (default) — working tree + staged + untracked. `scripts/local-diff.sh`
   - **staged** — only what is staged. `scripts/local-diff.sh --staged`
   - **unpushed** — commits not yet pushed, versus the branch upstream/base. `scripts/local-diff.sh --unpushed`
   - **all-local** — unpushed commits plus uncommitted edits. `scripts/local-diff.sh --all-local`
2. **Report path.** Default `PRE_PUSH_REVIEW.md` at the repository root. Honor any path the user provides.
3. **Review mode.** Pick the depth, defaulting to **Standard** unless the user requests otherwise or the diff size
   clearly warrants another mode:
   - **Quick** — small/low-risk diffs or a fast gate. Run Phases 1–2, security + correctness only, skip slow builds,
     report only High/Critical and obvious wins. Use for diffs under ~150 changed lines with no auth/data-access
     changes.
   - **Standard** — the default. All phases, all three measurements, safe validation, full report with the scorecard.
   - **Deep** — security-sensitive, large, or pre-release diffs. Standard plus: trace every changed entry point end to
     end, run available test suites and static analysis, expand the reference checklists, and add an explicit
     self-audit (Phase 9).
4. **Fix mode.** Off by default. Do not modify code, dependencies, configuration, or tests unless the user explicitly
   asks for fixes after the review.

## Non-negotiable output

- Create one report only. Default path: `PRE_PUSH_REVIEW.md` at the repository root, unless the user provides another.
- Do not split security, performance, and clean-code results into separate files.
- Every report includes the **Scorecard** (PASS/WARN/FAIL per measurement) and one overall **push recommendation**.
- In chat, return only a concise summary, the scorecard, the push recommendation, and the report path.
- Do not modify code, dependencies, configuration, or tests unless the user explicitly requests fixes after the review.
- Never expose secrets found during review. Redact values and report only the variable, file, and risk.

Use [assets/PRE_PUSH_REVIEW_REPORT_TEMPLATE.md](assets/PRE_PUSH_REVIEW_REPORT_TEMPLATE.md) as the required report
structure.

## Review principles

1. Review the local delta first, then inspect enough surrounding code to validate behavior and impact.
2. Report issues introduced by these changes or materially worsened by them. Do not flood the report with unrelated
   legacy debt.
3. Every finding must be reproducible from code, configuration, test output, or an explicitly stated assumption.
4. Prefer a smaller number of high-confidence findings over speculative warnings.
5. Explain **why** the issue matters in this codebase, not only the general rule.
6. Make recommendations concrete and proportionate. Avoid broad rewrites when a focused fix is safer.
7. Treat framework behavior as version-dependent. Read the manifests and relevant configuration before applying
   framework- or language-specific guidance.
8. Do not recommend memoization, caching, abstractions, or design patterns without evidence they solve a real problem.
9. Distinguish correctness risks from style preferences. Style-only opinions are not findings unless they materially
   reduce maintainability or violate an established repository convention.
10. A clean lint/build result does not prove security, performance, or correctness.

## Phase 1: Establish the review scope

1. Read repository guidance when present: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and `README.md`.
2. Detect the stack. Run `<skill-directory>/scripts/detect-stack.sh` for a quick machine-readable summary, then
   confirm by reading source as needed: languages and frameworks from the manifests (`package.json`, `composer.json`,
   `pyproject.toml`/`requirements.txt`, `go.mod`, `Gemfile`, `Cargo.toml`, etc.), the package manager/lockfile, and
   the installed framework versions whose behavior changes how findings apply.
3. Get the local diff with `<skill-directory>/scripts/local-diff.sh` (add `--staged`, `--unpushed`, or `--all-local`
   to match the Phase 0 scope). Resolve `<skill-directory>` from the loaded skill path. The script prints per-file
   stats, the unified diff, and any new untracked files, and flags an unusually large diff so you can scope the review.
4. Record the branch, diff scope, changed files, excluded generated files, and any review limitations.
5. Review lockfiles for dependency changes, but do not treat generated lockfile churn as ordinary clean-code findings.

## Phase 2: Understand the change

Before raising findings:

1. Summarize the intended behavior of the local changes from the diff, related code, and any tests.
2. Trace changed public entry points and their immediate call paths — request handlers, routes, actions, RPC/CLI
   entry points, jobs/queue consumers, webhooks, auth callbacks, and the data-access functions and external calls
   they reach.
3. Identify trust boundaries, user-controlled inputs, privileged operations, expensive paths, and code shared across
   call sites.
4. Compare implementation behavior with tests and established project patterns.

## Phase 3: Run safe validation

Run only non-destructive checks already available in the repository. Do not install packages or change files without
permission. Use the detected package manager and the project's own scripts (from `detect-stack.sh`,
`package.json`/`composer.json` scripts, `Makefile`, etc.).

Preferred order: existing focused tests for the changed behavior, then type checking, linting, broader unit/integration
tests, and a build only when feasible and useful. Record every command, its outcome, and the reason for any skipped
check. Do not claim a check passed when it was not run.

## Phase 4: Review security

Read [references/SECURITY.md](references/SECURITY.md) when the change touches server code, authentication, data access,
user input, output rendering, external requests, files, cookies/headers, dependencies, environment variables, or
deployment configuration.

At minimum, evaluate relevant changes for: authentication and object/function-level authorization at every privileged
entry point (not only in middleware or the UI); server-side input validation, canonicalization, and output encoding;
injection (SQL/NoSQL, command, template, header, log, path traversal, unsafe deserialization, dynamic evaluation);
XSS, CSRF, CORS, open redirects, SSRF, and clickjacking/CSP gaps; secret exposure through commits, logs, errors, or
client bundles; session/cookie safety, webhook verification, rate limiting, and replay/brute-force controls; data
leakage from caching, over-broad responses, or missing tenant/user scoping; file-upload validation; and dependency or
configuration changes that create a concrete exploitable condition.

A security finding must describe a reachable attack or failure path. Do not report hypothetical vulnerabilities without
a reachable source, unsafe sink, missing control, or credible misuse scenario.

## Phase 5: Review performance

Read [references/PERFORMANCE.md](references/PERFORMANCE.md) when the change touches data access, loops, rendering,
caching, payloads, assets, or hot paths.

At minimum, evaluate relevant changes for: N+1 queries and queries inside loops; over-fetching and unbounded result
sets that should paginate/stream/chunk; missing indexes for new filters/sorts/joins; accidental quadratic work and
repeated expensive computation; blocking work on a request path that should be async or queued; sequential
await/request waterfalls that can run in parallel; oversized payloads; and caching correctness (per-user/tenant keys,
invalidation on writes, never caching authorization-sensitive data under a shared key). For client/rendering changes,
consider bundle growth, unnecessary re-renders, and asset handling.

A performance finding must identify the affected path and expected consequence. Mark unmeasured impact clearly and
avoid invented timings or sizes.

## Phase 6: Review clean code

Read [references/CLEAN_CODE.md](references/CLEAN_CODE.md) for maintainability criteria, the literature behind them, and
the LLM/generated-code failure modes to check when the diff was machine-written.

At minimum, evaluate relevant changes for: clear intent and accurate names; cohesive units and correct separation of
concerns without needless layers; duplication that creates real change risk while avoiding premature abstraction; type
safety and deliberate error handling; dead code, stale comments, magic values, and hidden side effects; tests for new
behavior, fixed bugs, and authorization boundaries; and generated-code smells (invented APIs, plausible-but-wrong
usage, leftover TODOs/placeholders, comments that restate the code).

Do not enforce arbitrary rules such as maximum line counts. Explain the maintenance, correctness, testing, or
change-cost consequence.

## Phase 7: Classify findings

Use IDs by category: `SEC-001`, `PERF-001`, `CLEAN-001`, and so on.

Severity:

- **Critical**: Directly exploitable or catastrophic with likely broad impact (exposed production secrets,
  unauthenticated destructive access, severe cross-tenant disclosure).
- **High**: Likely security breach, major correctness failure, serious data exposure, or substantial performance
  regression.
- **Medium**: Meaningful risk under realistic conditions, or maintainability/performance debt likely to cause defects
  or operational cost.
- **Low**: Limited impact, localized maintainability concern, or worthwhile optimization with low urgency.

Confidence:

- **High**: Confirmed by code path, test, command output, or framework behavior for the installed version.
- **Medium**: Strong evidence exists, but runtime/configuration details could alter the result.
- **Low**: Plausible concern requiring validation. Use sparingly and place under "Open Questions" rather than as a
  blocking finding.

Each finding must contain: ID and concise title; severity and confidence; exact file and line/range; evidence and
affected path; why it matters here; a concrete recommendation; verification guidance; and a reference. Do not duplicate
the same root cause across categories — place it in the category of primary impact and cross-reference secondary
effects.

## Phase 8: Score each measurement and decide the push recommendation

Read [references/SCORING.md](references/SCORING.md) and apply it mechanically.

1. For each measurement (Security, Performance, Clean Code), count confirmed (High/Medium confidence) findings by
   severity and assign a level: **FAIL** if any Critical or High; **WARN** if a Medium or three or more Low; otherwise
   **PASS**.
2. Derive the overall **push recommendation** from the worst level and the severities behind it:
   - **Do not push** — any FAIL caused by a Critical, or a confirmed High security/correctness issue making a push
     unsafe.
   - **Fix before push** — any High-driven FAIL, or two or more WARN measurements with material Medium issues.
   - **Push with follow-ups** — no FAIL; only WARN/PASS with bounded Medium/Low items to track.
   - **Ready to push** — all three measurements PASS.
3. The recommendation follows the evidence, not the number of comments. A single confirmed Critical outranks any
   number of Low notes.

## Phase 9: Write and validate the report

1. Fill [assets/PRE_PUSH_REVIEW_REPORT_TEMPLATE.md](assets/PRE_PUSH_REVIEW_REPORT_TEMPLATE.md), including the Scorecard
   and the push recommendation.
2. Include all three category sections even when no findings exist; for an empty category write: "No substantiated
   findings in the reviewed scope."
3. Include validation commands and limitations, and the most relevant references used.
4. Remove unused placeholders and instructional comments.
5. Run:

   ```bash
   python3 <skill-directory>/scripts/validate-report.py PRE_PUSH_REVIEW.md
   ```

   Resolve `<skill-directory>` from the loaded skill path and use the actual report path if different. Fix structural
   errors before finishing.
6. Self-audit before finalizing (always in Deep mode; briefly in Standard): confirm each finding has a concrete
   location, a reachable path or reproduction, and a proportionate fix; that the scorecard levels follow the rubric;
   that the push recommendation follows the evidence; and that no secret value is reproduced in the report.
7. In chat, return only a concise summary, the scorecard, the push recommendation, the counts by severity, and the
   report path. Do not paste the full report into chat.
