---
name: launch-audit
description: >-
  Pre-launch and pre-commit audit for fast-moving projects. Use when the user asks whether a project is ready to ship, deploy, merge, or commit, especially AI-generated or "vibe coded" apps. Covers repository hygiene, committed secrets, environment variable documentation, database migration readiness, unsafe database access, dead code, weak auth, missing tests, broken builds, and deployment configuration footguns. If the user wants to verify their project before a launch, deploy, pull request, or commit, use this skill. Adapt the scope to a staged patch, a feature branch, a production incident follow-up, or a whole-repository readiness review; prioritize the risks that apply to the project's actual stack instead of applying a generic checklist.
---

# launch-audit

A hard-nosed readiness review for projects about to be shipped. The goal is a concrete list of blockers with evidence, not a generic best-practices essay. Work inside the actual repository using the agent's own tools (git, ripgrep, file inspection, existing scripts). This skill provides guidance only; no helper CLI is needed — the agent's shell is the tool.

## Operating Principles

- **Scope first.** Audit the current branch, staged changes, a PR diff, or the whole worktree. If the user did not specify, audit the current worktree plus files that affect deploy and runtime.
- **Evidence over opinion.** Every finding must point to a file, a line, a command result, or a missing expected artifact.
- **Redact secrets.** Never print secret values. Name the file and the variable/key shape, and replace the value with `***`.
- **Stay in review mode** unless the user asks for fixes. If they do ask, make the fixes after presenting the audit and verify them.
- **Preserve user work.** Do not modify unrelated files or discard uncommitted changes.
- **Separate review from remediation.** Report findings first. If the user asks for fixes, make the smallest scoped changes, preserve existing work, and re-check the affected behavior.
- **Do not create false assurance.** A clean search, passing test suite, or successful build only covers the paths and conditions it exercises. State the review boundary and material unknowns.

## Choose the Review Depth

Use the narrowest review that can answer the user's decision. If scope is not specified, review the current worktree and the files that determine build, runtime, data handling, and deployment. For commit or pull-request reviews, distinguish introduced issues from pre-existing findings. Do not assume a launch date, hosting platform, traffic profile, compliance regime, or risk tolerance; record unknowns that affect the conclusion.

Use [the review checklists](references/review-checklists.md) selectively for the project's architecture and release stage. Do not mechanically report every checklist item. Use [the report template](references/report-template.md) when a written audit needs a reusable deliverable.

## Workflow

1. **Map the project.** Identify framework, language, package manager, runtime version, deployment target, database, ORM, auth approach, and the build/test/lint commands. Note whether the worktree is clean or dirty.
2. **Repository hygiene.** Check for tracked junk: `.env*` files other than safe examples, local databases, logs, caches, build output, coverage, screenshots, uploads. Use `git ls-files` to separate tracked junk from ignored local files, and verify `.gitignore` covers the framework's artifacts (`.next`, `dist`, `build`, `coverage`, `node_modules`, lockfile exceptions, local SQLite files, logs, cache and upload directories).
3. **Secrets and environment.** Scan for tokens, private keys, API keys, JWT secrets, database URLs with embedded credentials, webhook secrets, and cloud credentials (AWS, Stripe, GitHub, Slack, OpenAI, Anthropic, Google, SendGrid, Twilio, and generic `*_SECRET` / `*_KEY` / `*_TOKEN` / `*_PASSWORD` assignments with real values). Confirm required env vars are documented in `.env.example`, docs, or typed config. Watch for accidental logging of auth headers, cookies, sessions, or provider responses.
4. **Database readiness.** Identify the migration system (Prisma, Drizzle, TypeORM, Sequelize, Knex, Alembic, Rails/Django migrations, or raw SQL). Confirm schema changes have committed migrations, deploys run migrations, and destructive changes have a backfill or rollback plan. Flag raw SQL that is not parameterized, and call out database-backed apps with no migration mechanism at all.
5. **Correctness and security basics.** Run the project's own `lint`, `typecheck`, `test`, and `build` scripts when practical and report results. Review auth boundaries, admin-only actions, server/client separation, CORS, CSRF, rate limiting, upload validation, SSRF surfaces, open redirects, and unsafe eval/shell execution. Production errors should not leak stack traces, secrets, or internal identifiers.
6. **Dead code.** Look for unused routes, duplicate pages or components, abandoned handlers, stale feature flags, large commented blocks, leftover TODO/FIXME/HACK notes, debugging output (`console.log`, `debugger`), and dependencies nothing imports. Prefer real signals: TypeScript compiler output, ESLint, framework route manifests, depcheck-style import scans. Dead code is low severity unless it touches security, deploy size, routing, migrations, or visible behavior.
7. **Deployment shape.** Inspect Dockerfiles, CI workflows, serverless configs (vercel/wrangler/netlify/fly/render/railway), release scripts, and runtime version pins. Flag missing production build steps, wrong package manager commands, missing migration steps, secrets required at build time versus runtime, and local-only assumptions.

## Match depth to the request

- **Before commit:** focus on the staged or requested paths, their callers, and directly related tests/configuration. Keep pre-existing repository issues separate from new findings.
- **Before pull request or release:** include integration points, migration and deployment configuration, required environment variables, and the relevant checks the project already defines.
- **Whole-project readiness:** map the main user flows and production dependencies first. Follow the paths that handle authentication, user data, payments, file uploads, external requests, and schema changes.
- **Incident follow-up:** trace the affected behavior from entry point through persistence and external services, then check whether the proposed remedy closes the specific failure mode.

Do not assume a framework, database, auth model, or deployment provider. If a category does not apply, omit it; if evidence is unavailable, mark it as not verified instead of converting absence of evidence into a pass or a finding. Use existing project commands only when appropriate to the scope, and record the exact commands and outcomes.

## Detailed audit procedure

### 1. Define the decision and boundary

An audit should answer a decision such as “is this patch safe to merge?”, “what must be fixed before deployment?”, or “what evidence should we collect after this incident?” Record the branch/diff or directory reviewed, the target environment if known, and the worktree state. If the user asks for a whole-app readiness review, include runtime and deployment files even when they are not part of the current feature diff. If they ask about a patch, keep pre-existing debt separate from findings caused by that patch.

Do not expand into unrelated refactoring. An audit is useful when each item can be tied to the chosen decision and a concrete piece of evidence.

### 2. Build a small system map

Before searching for problems, identify the application entry points, the main user flows, the storage layer, external services, deployment target, and existing verification commands. Follow the relevant path from request or user action through authorization, validation, business logic, persistence, and response. For a background worker, trace its trigger, retries, idempotency, and failure handling. For a static site or library, adapt the map instead of forcing server-specific checks.

### 3. Check the highest-impact failure modes first

Prioritize exposed credentials, authorization boundaries, destructive data changes, migration ordering, unsafe input handling, production startup, and deployment configuration. Then inspect reliability, observability, dependency hygiene, and polish. Distinguish a reachable exploit or broken deploy from a pattern that merely deserves review. A suspicious grep match is not proof of a vulnerability until the surrounding code and execution path are understood.

### 4. Use tools as evidence, not verdicts

Run repository-defined checks only when they are relevant, authorized, and practical. Read their scripts before executing them; do not invent commands or trigger broad, destructive, networked, or production-facing actions. Do not install dependencies, alter lockfiles, access production, or run migrations as part of a review unless the user authorized that action. A passing lint or test suite covers only what those tools and tests exercise. A missing test is not by itself proof of a defect; tie it to a meaningful risk or confidence gap. If a check is unavailable, costly, flaky, destructive, or requires credentials, explain that and continue with static review where possible.

When searching for credentials, keep secret-bearing values out of terminal transcripts and the final report. Prefer a scanner that redacts evidence. Do not run a command that prints matching lines when those lines may contain credentials; use filename-only matches or a redacting scanner, then inspect safely. Do not paste a full line if it may contain a credential. If a likely live credential appears, report its location and type without reproducing the value and recommend revocation or rotation through the relevant provider.

### 5. Make findings actionable and calibrated

For every finding, capture:

- **Evidence:** exact file and line, a command result, or a clearly described missing artifact.
- **Condition:** when the issue can occur, including required configuration or user access.
- **Impact:** the concrete failure, exposure, or operational cost.
- **Severity:** based on exploitability and impact, not how surprising the code looks.
- **Remedy:** the smallest practical change or the next verification needed.
- **Confidence:** how directly the available evidence establishes the condition; use high, medium, or low and explain material uncertainty briefly.

If a claim depends on unavailable credentials, production behavior, external service state, or a runtime path you could not exercise, label it unverified. Avoid absolute “safe” or “ready” conclusions when important parts were not observable.

Before including a finding, verify that the cited path is reachable in the relevant configuration and that the stated impact follows from the evidence. A pattern match alone is a lead. If a concern is useful but does not meet the finding threshold, place it under a short “follow-up checks” section rather than inflating its severity.

## Scenario-specific coverage

### Before a commit

Review the staged patch, staged configuration, and relevant callers/tests. Check for accidental local files, credentials, generated bundles, and changes outside the requested scope. Report whether the finding is in the staged content or only elsewhere in the worktree.

### Before deployment

Check the production build/start path, runtime pin, environment variable requirements, migration execution order, persistent storage assumptions, health checks, rollback or recovery path, and secret injection boundary. If the deployment platform or environment is unknown, state that gap rather than assuming a provider's defaults.

### For database changes

Trace both old and new application versions during rollout. Check whether the migration is backward-compatible with the order of deploy steps, whether a backfill is needed, how long locks may be held, and how destructive changes can be recovered. A committed migration file alone does not prove production will run it safely.

### For security-focused review

Follow attacker-controlled data to sensitive operations. Confirm the relevant authorization check occurs server-side and covers object-level access; inspect input validation, output encoding, file type/size handling, outbound request targets, rate limits, and sensitive logging where applicable. Mention only attack surfaces present in this project.

## Closeout format

Lead with blockers and high risks, then medium/low items. If there are no findings in the reviewed scope, say exactly what was inspected and what was not verified. Include commands actually run, their exit/results, and skipped checks with reasons. Do not bury a severe issue under a broad checklist of speculative recommendations.

## Useful Commands

Adapt to the repository. Never run broad destructive commands.

```bash
git status --short
git ls-files
rg -l --hidden --glob '!node_modules' --glob '!.git' \
  'AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{36}|sk_live_|sk-[A-Za-z0-9]{20,}|xox[baprs]-|AIza[0-9A-Za-z_-]{35}|SG\.[A-Za-z0-9_-]{16,}' .
rg -l --hidden --glob '!node_modules' --glob '!.git' \
  '(DATABASE_URL|JWT_SECRET|SECRET_KEY|API_KEY|ACCESS_TOKEN|REFRESH_TOKEN|WEBHOOK_SECRET|PASSWORD)=[^[:space:]]+' .
rg -n --hidden --glob '!node_modules' --glob '!.git' 'TODO|FIXME|HACK|console\.log|debugger|@ts-ignore' .
```

The credential searches above print matching filenames only. They are candidate discovery, not proof that a value is live; validate matches with a redacting method. Exclude generated, vendored, and fixture data where appropriate, but do not silently exclude tracked source or configuration.

For JavaScript/TypeScript projects, inspect `package.json` scripts first and run only the relevant existing ones: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`.

## Severity Levels

- **P0 Blocker** — likely secret exposure, data loss, auth bypass, deploy failure, broken migration, or user-data corruption.
- **P1 High** — strong launch risk: undocumented required envs, unsafe database access, unprotected sensitive routes, failing build or tests, tracked build/cache artifacts.
- **P2 Medium** — maintainability or reliability issues that will slow future work: stale duplicates, missing focused tests, weak error handling, unused dependencies.
- **P3 Low** — cleanup and polish that is not launch-blocking.

## Output Format

Lead with findings ordered by severity. For each finding include severity and short title, evidence (file:line, command output, or missing expected file), impact (what breaks or leaks), and the smallest practical fix. Close with:

- **Verified** — commands actually run and their results.
- **Not verified** — checks skipped and why (no git repo, scripts too heavy, credentials unavailable).
- **Residual risk** — what the repository shape prevented you from proving (e.g., runtime-only behavior, secrets held outside the repo).
