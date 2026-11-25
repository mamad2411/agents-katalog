---
name: laravel-pr-review
description: Reviews pull requests, merge requests, branch changes, and code diffs for Laravel and PHP applications (Laravel 9–12, PHP 8.0–8.4). Use when asked to review a PR or changed code for security, performance, and clean-code quality, then create one detailed Markdown report containing evidence, impact, rationale, recommendations, validation results, references, and a merge verdict. Supports Quick, Standard, and Deep review modes and can optionally post findings as inline PR comments. Do not use for feature implementation unless the user separately asks for fixes.
license: MIT
compatibility: Requires git. GitHub CLI is optional for PR metadata and inline comments. Designed for Codex and Claude Code using the Agent Skills open standard.
metadata:
  author: Ezzat Malak
  version: "1.0.0"
---

# Laravel PR Review

Perform a focused, evidence-based review of a Laravel or PHP pull request and write all results to exactly one Markdown report.

## Phase 0: Resolve inputs and review mode

Determine these before doing anything else, then echo them back in the report's Review Scope.

1. **Target.** What is being reviewed: a GitHub PR number/URL, a branch, a commit range, or the working tree against a base branch. If ambiguous, default to comparing the current branch against the detected base (`origin/main`, `origin/master`, `main`, `master`).
2. **Report path.** Default `PR_REVIEW.md` at the repository root. Honor any path the user provides.
3. **Review mode.** Pick the depth, defaulting to **Standard** unless the user requests otherwise or the diff size clearly warrants another mode:
   - **Quick** — small/low-risk diffs or a fast gate. Run Phases 1–2, security + correctness only, skip the build, report only High/Critical and obvious wins. Use for diffs under ~150 changed lines with no controller/route/auth/database changes.
   - **Standard** — the default. All phases, all three categories, safe validation, full report.
   - **Deep** — security-sensitive, large, or pre-release diffs. Standard plus: trace every changed route/controller/job/command end to end, run the available test suite and static analysis, expand the reference checklists, and add an explicit self-audit (Phase 9) before finalizing.
4. **Inline comments.** Off by default — the report is the deliverable. Only post inline PR comments when the user explicitly asks, and only after the report exists (see Phase 10).
5. **Fix mode.** Off by default. Do not modify application code, dependencies, configuration, migrations, or tests unless the user explicitly asks for fixes after the review.

## Non-negotiable output

- Create one report only. Default path: `PR_REVIEW.md` at the repository root, unless the user provides another path.
- Do not split security, performance, and clean-code results into separate files.
- In chat, return only a concise summary, the merge verdict, and the report path.
- Do not modify application code, dependencies, configuration, migrations, or tests unless the user explicitly requests fixes after the review.
- Never expose secrets found during review. Redact values and report only the variable, file, and risk.

Use [assets/PR_REVIEW_REPORT_TEMPLATE.md](assets/PR_REVIEW_REPORT_TEMPLATE.md) as the required report structure. The report H1 must be `# Laravel PR Code Review`.

## Review principles

1. Review the PR delta first, then inspect enough surrounding code to validate behavior and impact.
2. Report issues introduced by the PR or materially worsened by it. Do not flood the report with unrelated legacy debt.
3. Every finding must be reproducible from code, configuration, test output, or an explicitly stated assumption.
4. Prefer a smaller number of high-confidence findings over speculative warnings.
5. Explain **why** the issue matters in this application, not only the general rule.
6. Make recommendations concrete and proportionate. Avoid broad rewrites when a focused fix is safer.
7. Treat framework behavior as version-dependent. Read `composer.json`, `composer.lock`, and relevant configuration before applying Laravel or PHP guidance.
8. Do not recommend caching, queues, repositories, abstractions, or design patterns without evidence that they solve a real problem.
9. Distinguish correctness risks from style preferences. Style-only opinions are not findings unless they materially reduce maintainability or violate an established repository convention (PSR-12, Pint, project standards).
10. A clean static-analysis/test result does not prove security, performance, or correctness.

## Phase 1: Establish the review scope

1. Read repository guidance when present: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, and package-specific instructions.
2. Detect the stack. Run `<skill-directory>/scripts/detect-stack.sh` for a quick machine-readable summary, then confirm by reading source as needed:
   - `composer.json` and `composer.lock`.
   - PHP version constraint, `laravel/framework` version, and key packages (Sanctum, Passport, Fortify, Livewire, Inertia, Filament, Telescope, Horizon, Octane, Pest/PHPUnit, Larastan/PHPStan, Pint).
   - Whether the app uses Laravel 11/12's slimmed skeleton (`bootstrap/app.php`, no `app/Http/Kernel.php`) or the older structure.
   - Database driver, queue/cache/session drivers, and `.env`/config conventions.
   - PHP 8 features in use that change how findings apply: enums, readonly properties/classes, constructor promotion, `match`, named arguments, nullsafe operator, first-class callable syntax, and typed properties/return types.
3. Identify the exact diff:
   - For a GitHub PR, prefer `gh pr view` and `gh pr diff` when GitHub CLI is installed and authenticated. To review a specific PR, pass its number: `<skill-directory>/scripts/pr-diff.sh --pr 123`.
   - Otherwise determine the target branch and compare the merge base with `HEAD`.
   - Use `<skill-directory>/scripts/pr-diff.sh [base-ref]` when useful. Resolve `<skill-directory>` from the loaded skill path. The script prints per-file change stats and flags an unusually large diff so you can scope the review.
4. Record the base, head, commit range, changed files, excluded generated files (e.g. `composer.lock`, compiled assets), and any review limitations.
5. Review `composer.lock` for dependency changes, but do not treat generated lockfile churn as ordinary clean-code findings.

## Phase 2: Understand the change

Before raising findings:

1. Summarize the PR's intended behavior from its description, commits, tests, and code.
2. Trace changed public entry points and their immediate call paths:
   - Routes (`web.php`, `api.php`, route files), controllers, invokable controllers, and route model bindings.
   - Middleware, Form Requests, Gates/Policies, and authorization checks.
   - Eloquent models, relationships, scopes, accessors/mutators/casts, and migrations.
   - Jobs, listeners, events, commands, schedulers, notifications, mailables, and broadcast channels.
   - API resources/transformers, validation rules, and serialization to the client.
   - External calls (`Http`, SDKs), file storage, and third-party webhooks.
3. Identify trust boundaries, user-controlled inputs, privileged operations, expensive paths, and code shared across routes/jobs.
4. Compare implementation behavior with tests and established project patterns.

## Phase 3: Run safe validation

Run only non-destructive checks that are available in the repository. Do not install packages, run migrations against real data, or change files without permission.

Preferred order:

1. Existing focused tests for changed behavior (`php artisan test`, `vendor/bin/phpunit`, or `vendor/bin/pest`).
2. Static analysis when configured (`vendor/bin/phpstan`, Larastan, Psalm).
3. Code style check in report-only mode (`vendor/bin/pint --test`, PHP_CodeSniffer).
4. Relevant unit/feature tests.
5. Repository-provided security or analysis scripts when already configured (`composer audit`).

Use the detected tooling and existing Composer scripts. Never run destructive Artisan commands (`migrate:fresh`, `db:wipe`, `migrate` on a real database) as part of validation. Record every command, outcome, and reason for skipped checks. Do not claim a check passed when it was not run.

## Phase 4: Review security

Read [references/SECURITY.md](references/SECURITY.md) when the PR changes routes, controllers, authentication, authorization, data access, user input, Blade output, external requests, files, cookies, headers, queues, dependencies, environment variables, or deployment configuration.

At minimum, evaluate relevant changes for:

- Authentication and object/function-level authorization on every privileged entry point (Policies, Gates, `$this->authorize`, `can` middleware, Form Request `authorize()`).
- Mass assignment exposure via `$fillable`/`$guarded`, `forceFill`, `Model::unguard`, or `$request->all()` into `create`/`update`/`fill`.
- SQL injection through raw queries, `DB::raw`, `whereRaw`, `orderByRaw`, `selectRaw`, and dynamic column/order names not allowlisted.
- XSS via unescaped Blade `{!! !!}`, `@php` echo, `Js::from`, or `HtmlString` with user data; missing sanitization of rich text.
- CSRF protection on state-changing routes, correct `VerifyCsrfToken` exclusions, and SameSite/session configuration.
- Validation completeness and trust: Form Requests / `$request->validate` with explicit rules, type and bounds checks, and allowlists for enums, sort keys, and file types.
- Injection and unsafe execution: command injection (`exec`, `shell_exec`, `proc_open`, `Process`), `eval`, `unserialize` of untrusted data, path traversal in storage/file paths, and template/header/log injection.
- SSRF and open redirects: server-side `Http`/`file_get_contents` to user-controlled URLs, and unvalidated `redirect()` targets.
- Secret exposure through commits, logs, exceptions, debug responses (`APP_DEBUG=true`), `dd()`/`dump()` left in code, or serialized job payloads.
- Session, cookie, token, and API auth safety (Sanctum/Passport scopes, token expiry, `HttpOnly`/`Secure`/`SameSite`, signed URLs, password hashing/rehash).
- Rate limiting and abuse controls (`throttle` middleware, RateLimiter) on login, reset, OTP, search, export, upload, and webhook endpoints; webhook signature verification.
- File upload validation (size, MIME/extension allowlist, storage disk, public vs private, signed/serving headers).
- Data leakage from over-broad API resources, cached responses, or queries that ignore tenant/user scoping (missing global scopes or `where` clauses).
- Dependency or configuration changes that create a concrete exploitable condition (use `composer audit` evidence; do not invent CVE status).

Security findings must describe an attack or failure path. Do not report hypothetical vulnerabilities without a reachable source, unsafe sink, missing control, or credible misuse scenario.

## Phase 5: Review performance

Read [references/PERFORMANCE.md](references/PERFORMANCE.md) when the PR changes database access, Eloquent usage, caching, queues, collections, serialization, or hot request paths.

At minimum, evaluate relevant changes for:

- N+1 queries from lazy-loaded relationships in loops/Blade; verify eager loading (`with`, `load`, `withCount`) and consider `preventLazyLoading` in non-production.
- Queries inside loops, missing `select` of only needed columns, and `SELECT *` on wide tables.
- Large result sets loaded fully into memory where `chunk`, `chunkById`, `cursor`, or `lazy` is appropriate; missing pagination on list endpoints.
- Missing or mismatched database indexes for new query/filter/sort/foreign-key columns introduced by the change.
- Redundant or duplicate queries that could be combined, cached (`Cache::remember`), or memoized within the request.
- Expensive synchronous work (email, external API, image processing, exports) that should be dispatched to a queued Job.
- Inefficient collection operations on large datasets, repeated re-querying, and re-computation that could be hoisted.
- Caching correctness: cache keys that include the user/tenant where data is personalized, and invalidation on writes; never cache authorization-sensitive data under a shared key.
- Eager-loading too much (over-fetching relationships/columns not used) as well as too little.
- Config/route/view/event caching assumptions and `APP_ENV`-dependent behavior; Octane state leakage (static/singleton state retained between requests) when Octane is in use.

A performance finding must identify the affected path and expected consequence. Mark unmeasured impact clearly and avoid invented timings or query counts.

## Phase 6: Review clean code

Read [references/CLEAN_CODE.md](references/CLEAN_CODE.md) for maintainability criteria and the literature behind them.

At minimum, evaluate relevant changes for:

- Clear intent, accurate names, cohesive classes, and appropriately scoped methods following PSR-12 and project conventions.
- Correct separation of concerns: thin controllers, validation in Form Requests, business logic in services/actions, data access in models/repositories where it reduces coupling — without inventing unnecessary layers.
- Duplication that creates real change risk, while avoiding premature abstraction.
- Type safety: parameter/return/property types, enums for fixed sets, readonly where appropriate, DTOs/value objects for complex data, and avoidance of untyped arrays passed across boundaries.
- Predictable error handling: typed exceptions, the exception handler, transactions (`DB::transaction`) around multi-step writes, and no swallowed errors.
- Eloquent and framework idioms: proper relationships, scopes, casts, accessors/mutators, route model binding, and avoiding logic in Blade templates.
- Dead code, leftover `dd`/`dump`/`var_dump`, stale comments, magic values, and inconsistent repository conventions.
- Tests for new behavior, regressions, authorization boundaries, validation, and important failure cases.
- Migration safety and reversibility (`down` methods, non-destructive column changes, data-migration concerns).

Do not enforce arbitrary rules such as maximum line counts. Explain the maintenance, correctness, testing, or change-cost consequence.

## Phase 7: Classify findings

Use IDs by category:

- `SEC-001`, `SEC-002`, ...
- `PERF-001`, `PERF-002`, ...
- `CLEAN-001`, `CLEAN-002`, ...

Severity:

- **Critical**: Directly exploitable or catastrophic issue with likely broad impact, such as exposed production secrets, unauthenticated destructive access, SQL injection, or severe cross-tenant data disclosure.
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
