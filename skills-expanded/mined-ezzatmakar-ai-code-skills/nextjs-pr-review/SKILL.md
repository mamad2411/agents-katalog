---
name: nextjs-pr-review
description: Reviews pull requests, merge requests, branch changes, and code diffs for Next.js and React applications (App Router and Pages Router, Next.js 13–16). Use when asked to review a PR or changed code for security, performance, and clean-code quality, then create one detailed Markdown report containing evidence, impact, rationale, recommendations, validation results, references, and a merge verdict. Supports Quick, Standard, and Deep review modes and can optionally post findings as inline PR comments. Do not use for feature implementation unless the user separately asks for fixes.
license: MIT
compatibility: Requires git. GitHub CLI is optional for PR metadata and inline comments. Designed for Codex and Claude Code using the Agent Skills open standard.
metadata:
  author: Ezzat Malak
  version: "2.0.0"
---

# Next.js PR Review

Perform a focused, evidence-based review of a Next.js or React pull request and write all results to exactly one Markdown report.

## Phase 0: Resolve inputs and review mode

Determine these before doing anything else, then echo them back in the report's Review Scope.

1. **Target.** What is being reviewed: a GitHub PR number/URL, a branch, a commit range, or the working tree against a base branch. If ambiguous, default to comparing the current branch against the detected base (`origin/main`, `origin/master`, `main`, `master`).
2. **Report path.** Default `PR_REVIEW.md` at the repository root. Honor any path the user provides.
3. **Review mode.** Pick the depth, defaulting to **Standard** unless the user requests otherwise or the diff size clearly warrants another mode:
   - **Quick** — small/low-risk diffs or a fast gate. Run Phases 1–2, security + correctness only, skip the build, report only High/Critical and obvious wins. Use for diffs under ~150 changed lines with no server/auth/data-access changes.
   - **Standard** — the default. All phases, all three categories, safe validation, full report.
   - **Deep** — security-sensitive, large, or pre-release diffs. Standard plus: trace every changed server entry point end to end, attempt the production build and available test suites, expand the reference checklists, and add an explicit self-audit (Phase 9) before finalizing.
4. **Inline comments.** Off by default — the report is the deliverable. Only post inline PR comments when the user explicitly asks, and only after the report exists (see Phase 10).
5. **Fix mode.** Off by default. Do not modify application code, dependencies, configuration, or tests unless the user explicitly asks for fixes after the review.

## Non-negotiable output

- Create one report only. Default path: `PR_REVIEW.md` at the repository root, unless the user provides another path.
- Do not split security, performance, and clean-code results into separate files.
- In chat, return only a concise summary, the merge verdict, and the report path.
- Do not modify application code, dependencies, configuration, or tests unless the user explicitly requests fixes after the review.
- Never expose secrets found during review. Redact values and report only the variable, file, and risk.

Use [assets/PR_REVIEW_REPORT_TEMPLATE.md](assets/PR_REVIEW_REPORT_TEMPLATE.md) as the required report structure.

## Review principles

1. Review the PR delta first, then inspect enough surrounding code to validate behavior and impact.
2. Report issues introduced by the PR or materially worsened by it. Do not flood the report with unrelated legacy debt.
3. Every finding must be reproducible from code, configuration, test output, or an explicitly stated assumption.
4. Prefer a smaller number of high-confidence findings over speculative warnings.
5. Explain **why** the issue matters in this application, not only the general rule.
6. Make recommendations concrete and proportionate. Avoid broad rewrites when a focused fix is safer.
7. Treat framework behavior as version-dependent. Read `package.json`, the lockfile, and relevant configuration before applying Next.js or React guidance.
8. Do not recommend memoization, caching, dynamic imports, abstractions, or design patterns without evidence that they solve a real problem.
9. Distinguish correctness risks from style preferences. Style-only opinions are not findings unless they materially reduce maintainability or violate an established repository convention.
10. A clean lint/build result does not prove security, performance, or correctness.

## Phase 1: Establish the review scope

1. Read repository guidance when present: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, and package-specific instructions.
2. Detect the stack. Run `<skill-directory>/scripts/detect-stack.sh` for a quick machine-readable summary, then confirm by reading source as needed:
   - `package.json` and the active lockfile.
   - `next.config.*`, `tsconfig.json`, ESLint configuration, middleware/proxy files, and deployment configuration when changed or relevant.
   - Whether the app uses App Router, Pages Router, or both.
   - Installed Next.js, React, Node.js, TypeScript, authentication, database, validation, and state-management versions.
   - Major-version behavior that changes how findings apply, including: Next.js 15+ `fetch` and Route Handlers no longer caching by default; `cookies()`, `headers()`, `draftMode()`, `params`, and `searchParams` being async; React 19 and the React Compiler; and any opted-in `'use cache'`, `cacheLife`/`cacheTag`, Partial Prerendering (`ppr`), `dynamicIO`, or `after()` usage.
3. Identify the exact diff:
   - For a GitHub PR, prefer `gh pr view` and `gh pr diff` when GitHub CLI is installed and authenticated. To review a specific PR, pass its number: `<skill-directory>/scripts/pr-diff.sh --pr 123`.
   - Otherwise determine the target branch and compare the merge base with `HEAD`.
   - Use `<skill-directory>/scripts/pr-diff.sh [base-ref]` when useful. Resolve `<skill-directory>` from the loaded skill path. The script also prints per-file change stats and flags an unusually large diff so you can scope the review.
4. Record the base, head, commit range, changed files, excluded generated files, and any review limitations.
5. Review lockfiles for dependency changes, but do not treat generated lockfile churn as ordinary clean-code findings.

## Phase 2: Understand the change

Before raising findings:

1. Summarize the PR's intended behavior from its description, commits, tests, and code.
2. Trace changed public entry points and their immediate call paths:
   - Route Handlers, API routes, Server Actions/Functions, middleware/proxy, webhooks, authentication callbacks, and form submissions.
   - Pages, layouts, Server Components, Client Components, hooks, stores, and shared utilities.
   - Data-access functions, ORM queries, cache boundaries, external requests, and serialization to the client.
3. Identify trust boundaries, user-controlled inputs, privileged operations, expensive paths, and code shared across routes.
4. Compare implementation behavior with tests and established project patterns.

## Phase 3: Run safe validation

Run only non-destructive checks that are available in the repository. Do not install packages or change files without permission.

Preferred order:

1. Existing focused tests for changed behavior.
2. Type checking.
3. Linting.
4. Relevant unit/integration tests.
5. Production build when feasible and useful.
6. Repository-provided security or bundle-analysis scripts when already configured.

Use the detected package manager and existing scripts. Record every command, outcome, and reason for skipped checks. Do not claim a check passed when it was not run.

## Phase 4: Review security

Read [references/SECURITY.md](references/SECURITY.md) when the PR changes server code, authentication, data access, user input, HTML rendering, external requests, files, cookies, headers, dependencies, environment variables, or deployment configuration.

At minimum, evaluate relevant changes for:

- Authentication and object/function-level authorization on every privileged server entry point.
- Server Actions/Functions and Route Handlers being callable directly, regardless of UI visibility.
- Trusted-server input validation, canonicalization, safe parsing, output encoding, and HTML sanitization.
- Injection risks: SQL/NoSQL, command, template, header, log, path traversal, and unsafe dynamic evaluation.
- XSS, CSRF, CORS, open redirects, SSRF, unsafe URL handling, and clickjacking/CSP gaps.
- Secret exposure through commits, logs, errors, browser bundles, `NEXT_PUBLIC_*`, or Server-to-Client serialization.
- Session and cookie safety, webhook verification, rate limiting, replay protection, and brute-force controls.
- Data leakage caused by caching, revalidation, tenant/user scoping, or over-broad API responses.
- File upload validation and safe storage/serving behavior.
- Dependency or configuration changes that create a concrete exploitable condition.
- Middleware used as the only authorization gate: confirm privileged work is also guarded at the handler/action, since middleware can be bypassed and matchers are easy to misconfigure.
- `'use cache'`, `cacheTag`, and revalidation that could place user- or tenant-scoped data into a shared cache without a per-principal key.

Security findings must describe an attack or failure path. Do not report hypothetical vulnerabilities without a reachable source, unsafe sink, missing control, or credible misuse scenario.

## Phase 5: Review performance

Read [references/PERFORMANCE.md](references/PERFORMANCE.md) when the PR changes rendering, data fetching, caching, assets, client boundaries, state, lists, third-party scripts, APIs, or build configuration.

At minimum, evaluate relevant changes for:

- Unnecessary Client Components or broad `'use client'` boundaries that increase shipped JavaScript.
- Sequential data-fetching waterfalls where independent work can safely run in parallel.
- Duplicate requests, N+1 queries, oversized payloads, unbounded result sets, and expensive work on hot paths.
- Next.js caching and revalidation behavior according to the installed framework version and data sensitivity.
- Bundle growth, barrel-import side effects, heavy libraries, missing lazy loading, and third-party script impact.
- Image, font, and media handling that can harm LCP or CLS.
- React render loops, unnecessary Effects, duplicated derived state, unstable list keys, and expensive repeated calculations.
- Memoization only when supported by measured or obvious expensive work; account for React Compiler configuration.
- Long main-thread work, large lists without an appropriate strategy, hydration mismatches, and interaction latency.
- Server runtime, database, and external API latency; caching must not compromise authorization or data freshness.
- Caching behavior matched to the installed version: in Next.js 15+ `fetch` and Route Handlers are uncached by default, so flag hot-path data that should opt into `'use cache'`, `cacheLife`/`cacheTag`, or `revalidate` — and conversely flag personalized data wrongly placed behind a shared cache.
- Correct use of newer primitives when present: `after()` for non-blocking post-response work, streaming/`Suspense` and Partial Prerendering (`ppr`) for slow segments, and unnecessary forced-dynamic rendering that defeats prerendering.

A performance finding must identify the affected path and expected consequence. Mark unmeasured impact clearly and avoid invented timings or bundle sizes.

## Phase 6: Review clean code

Read [references/CLEAN_CODE.md](references/CLEAN_CODE.md) for maintainability criteria and the literature behind them.

At minimum, evaluate relevant changes for:

- Clear intent, accurate names, cohesive modules, and appropriately scoped functions/components.
- Correct separation of UI, domain, data-access, and infrastructure concerns without unnecessary layers.
- Duplication that creates real change risk, while avoiding premature abstraction.
- Type safety, unsafe assertions, `any`, nullable states, schema drift, and unhandled variants.
- Predictable error handling, useful error context, cleanup, and failure-state behavior.
- React purity, Hook correctness, Effect dependencies, stable keys, state ownership, and component API clarity.
- Dead code, stale comments, magic values, hidden side effects, and inconsistent repository conventions.
- Tests for new behavior, regressions, authorization boundaries, and important failure cases.
- Accessibility regressions in changed interactive UI when they indicate broken semantics or usability.

Do not enforce arbitrary rules such as maximum line counts. Explain the maintenance, correctness, testing, or change-cost consequence.

## Phase 7: Classify findings

Use IDs by category:

- `SEC-001`, `SEC-002`, ...
- `PERF-001`, `PERF-002`, ...
- `CLEAN-001`, `CLEAN-002`, ...

Severity:

- **Critical**: Directly exploitable or catastrophic issue with likely broad impact, such as exposed production secrets, unauthenticated destructive access, or severe cross-tenant data disclosure.
- **High**: Likely security breach, major correctness failure, serious data exposure, or substantial production performance regression.
- **Medium**: Meaningful risk requiring realistic conditions, or maintainability/performance debt likely to cause defects or operational cost.
- **Low**: Limited impact, localized maintainability concern, or worthwhile optimization with low urgency.

Confidence:

- **High**: Confirmed by code path, test, command output, or framework behavior for the installed version.
- **Medium**: Strong evidence exists, but runtime/configuration details could alter the result.
- **Low**: Plausible concern requiring validation. Use sparingly and place under “Open questions” rather than as a blocking finding when evidence is insufficient.

Each finding must contain:

1. ID and concise title.
2. Severity and confidence.
3. Exact file and line/range, using the changed line when possible.
4. Evidence and affected execution path.
5. Why it matters in this PR.
6. Concrete recommendation.
7. Verification guidance or suggested test.
8. Reference to the applicable project rule, official documentation, standard, or book principle.

Do not duplicate the same root cause across categories. Place it in the category of primary impact and cross-reference secondary effects.

## Phase 8: Decide the merge verdict

Use one verdict:

- **Block**: At least one confirmed Critical issue, or a confirmed High security/correctness issue that makes merging unsafe.
- **Needs changes**: High issues or material Medium issues should be fixed before merge.
- **Approve with follow-ups**: No blocking issue; only bounded Medium/Low improvements that can be tracked separately.
- **Approve**: No substantiated issues in the reviewed scope.

The verdict must follow the evidence, not the number of comments.

## Phase 9: Write and validate the report

1. Fill [assets/PR_REVIEW_REPORT_TEMPLATE.md](assets/PR_REVIEW_REPORT_TEMPLATE.md).
2. Include all three category sections even when no findings exist.
3. For an empty category, state: “No substantiated findings in the reviewed scope.”
4. Include validation commands and limitations.
5. Include the most relevant references used during this review.
6. Remove unused placeholders and instructional comments.
7. Run:

```bash
python3 <skill-directory>/scripts/validate-report.py PR_REVIEW.md
```

Resolve `<skill-directory>` from the loaded skill path and use the actual report path if different. Fix structural errors before finishing.

8. Self-audit before finalizing (always in Deep mode; briefly in Standard). Confirm each finding has a concrete location, a reachable path or reproduction, and a proportionate fix; remove any finding that is only a style preference or cannot be substantiated; verify the verdict follows the evidence rather than the finding count; and confirm no secret value is reproduced in the report.

9. In chat, return only a concise summary, the merge verdict, the counts by severity, and the report path. Do not paste the full report into chat.

## Phase 10: Optional — post inline PR comments

Only when the user explicitly asks and the target is a GitHub PR with `gh` installed and authenticated.

1. Confirm the exact scope (which findings, which PR) before posting. Posting comments is outward-facing and hard to undo.
2. Keep each comment short: the finding ID, severity/confidence, one-line impact, and the concrete recommendation. Link back to the report for full detail.
3. Anchor each comment to the precise file and line from the finding. Never include a secret value in a comment.
4. Prefer one batched review over many separate comments. Summarize what was posted in chat afterward.
5. Do not approve, request changes, or merge the PR on the user's behalf unless they explicitly direct it.
