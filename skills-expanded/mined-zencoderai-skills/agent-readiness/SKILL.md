---
name: agent-readiness
description: Audit a repository's preparedness for autonomous AI coding agents - evaluates 86 checks spanning code quality, testing, documentation, security, and observability across 5 tiers (Bronze to Diamond)
disable-model-invocation: true
---

# Repository Agent-Readiness Audit

Perform a read-only audit of a code repository to determine how well it supports autonomous AI coding agents. Produce an **Agent-Readiness Report** covering 86 checks grouped into 5 tiers: Bronze, Silver, Gold, Platinum, and Diamond.

**Target repository:** $ARGUMENTS (GitHub URL or local path). Falls back to the current working directory when no argument is given.

---

## Phase 1 - Scan the Repository

**Cloning (when a URL is provided):** If $ARGUMENTS is a GitHub URL, clone it into `/tmp` and `cd` into the result. If cloning fails (bad URL, auth issue, private repo without keys), report the failure and stop — never evaluate a partial clone.

**Stay inside the repo boundary.** All exploration must remain within the directory containing `.git`. Parent directories are fine as long as they stay inside the repo root. Skip `.git`, `node_modules`, `dist`, and `build` directories during traversal.

1. **Detect shallow clones**
   Run `git rev-parse --is-shallow-repository`. When the result is `true`, flag it in the report metadata. Criteria that rely on git history (`ai_agent_workflow`, `doc_recency`) cannot produce reliable results — set their numerator to `null` with the note "Skipped: shallow clone limits git history". Optionally try `git fetch --unshallow` but do not fail if it is unavailable.

2. **Identify languages**
   Detect the primary language(s) by looking for telltale files:
   - JS/TS: `package.json`, `tsconfig.json`, `.ts`/`.tsx`/`.js`/`.jsx`
   - Python: `pyproject.toml`, `setup.py`, `requirements.txt`, `.py`
   - Rust: `Cargo.toml`, `.rs`
   - Go: `go.mod`, `.go`
   - Java: `pom.xml`, `build.gradle`, `.java`
   - Ruby: `Gemfile`, `.gemspec`, `.rb`

   **Multi-language repos:** Record a primary language per application directory. Evaluate language-specific criteria against the matching language for each app (e.g. check ESLint for a TS app, ruff for a Python app).

3. **Map the file tree**
   Walk the entire repo from root. Note main source directories (`src/`, `app/`, `lib/`), config files, docs, and test directories.

---

## Phase 2 - Discover Applications

Complete this phase fully before Phase 3.

### Defining "application"

An application is a **directory** representing an independently deployable unit — it has its own build/run lifecycle, could theoretically live in its own repo, and directly serves users or other systems.

**Strong indicators:**
- Own `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` with build & start scripts
- Own `Dockerfile`
- Dedicated CI/CD workflow or deploy config

**Typical patterns:**
- Single-purpose repo = 1 application (the root)
- Monorepo with service directories = one application per independently deployable service
- Library repo = 1 application (root), even though it ships as a package
- Tutorials / showcase repos = 1 application (the collection)

**Clarifications:**
- Applications are directories, not individual files
- Shared libraries and utility packages consumed by other apps are **not** applications
- Demo/example directories sharing infrastructure with the main app are **not** separate applications
- If the scan finds zero applications, treat the repo root (`.`) as one application

### Output

List every application with its relative path from repo root and a short description derived from README, `package.json` description, or inferred from directory name and scripts.

```
APPLICATIONS_FOUND: N

1. [path] - [description]
...
```

Once N is established it is fixed for the rest of the evaluation:
- Every **Application Scope** criterion uses denominator = N
- Every **Repository Scope** criterion uses denominator = 1

---

## Phase 3 - Evaluate Criteria

Criteria within the same scope are independent and may run concurrently. Batch VCS CLI calls (`gh`/`glab`) to stay within rate limits.

### Scope definitions

| Scope | Evaluated how | numerator | denominator |
|-------|--------------|-----------|-------------|
| Repository (45 criteria) | Once for the whole repo | 1 pass / 0 fail / null skip | Always 1 |
| Application (41 criteria) | Once per app | Count of passing apps (0..N) or null | Always N |

Equivalent tools not explicitly listed below also count. The named tools are common examples.

### VCS CLI prerequisite

Evaluate `platform_cli_auth` first. If it fails, automatically skip every criterion that depends on `gh`/`glab`: `pr_review_bots`, `ci_turnaround`, `build_metrics`, `deploy_cadence`, `branch_rules`, `credential_detection`, `security_report_gen`, `issue_hygiene`, `test_stability`, `quality_dashboard`. Set their numerator to `null` with "Skipped: VCS CLI unavailable".

---

### Repository Scope Criteria (45)

| ID | Tier | Summary |
|----|------|---------|
| `readme_present` | Bronze | `README.md` exists at repo root with setup/usage content |
| `gitignore_coverage` | Bronze | `.gitignore` properly excludes `.env` (not `.env.example`), `node_modules`, build artifacts, IDE configs, OS files |
| `env_vars_template` | Bronze | `.env.example` or env-var documentation in README/AGENTS.md exists |
| `build_instructions` | Silver | README or AGENTS.md documents the build command |
| `dependency_lockfile` | Silver | A lockfile is committed (e.g. `yarn.lock`, `poetry.lock`, `Cargo.lock`) |
| `agent_guide` | Silver | `AGENTS.md` exists at repo root with >100 characters of agent-oriented guidance |
| `ownership_manifest` | Silver | `CODEOWNERS` in root or `.github/` with valid team assignments |
| `issue_forms` | Silver | Issue templates directory exists with structured bug/feature templates |
| `issue_taxonomy` | Silver | Consistent label taxonomy for priority, type, and area |
| `pr_forms` | Silver | PR template exists with sections for description, testing, and context |
| `container_dev_env` | Silver | `.devcontainer/devcontainer.json` configured for the repo's primary language |
| `incident_playbooks` | Silver | Runbook references exist (links to Notion/Confluence/wiki or a `runbooks/` dir) |
| `dep_update_bots` | Silver | Dependabot, Renovate, or equivalent is configured and creating update PRs |
| `doc_auto_generation` | Silver | Automated doc tooling in place (Swagger/OpenAPI generators, JSDoc, Sphinx, etc.) |
| `secrets_infra` | Silver | Secrets management pattern evident (cloud secrets manager, CI secrets, SOPS, proper `.env` handling) |
| `platform_cli_auth` | Silver | `gh` or `glab` CLI installed and authenticated |
| `pr_review_bots` | Silver | [Skippable] Automation posts review comments on PRs (not just status checks) |
| `workspace_orchestration` | Silver | [Skippable] Monorepo tooling configured (Turborepo, Nx, Lerna). Skip for single-app repos |
| `local_deps_setup` | Silver | [Skippable] `docker-compose.yml` or docs for running local services. Skip if no external deps |
| `branch_rules` | Silver | [Skippable] Branch protection / rulesets on main/dev. Skip if CLI unavailable |
| `quickstart_command` | Gold | README/AGENTS.md documents a single command (or short chain) from fresh clone to running dev server |
| `deterministic_builds` | Gold | Lockfile committed AND CI uses frozen/locked install commands |
| `deploy_pipeline` | Gold | Automated release/deploy pipeline (CD, semantic-release, GitOps, Docker publish) |
| `changelog_generation` | Gold | Automated changelog or release notes generation exists |
| `agent_skills` | Gold | At least one valid skill in `.skills/` or `.claude/skills/` with proper metadata |
| `doc_recency` | Gold | README, AGENTS.md, or CONTRIBUTING.md modified within the last 180 days |
| `architecture_docs` | Gold | Architecture diagrams or service dependency documentation exists |
| `ai_agent_workflow` | Gold | Evidence AI agents actively participate in development (co-authored commits, agent config dirs, MCP configs, agent CI jobs, skills dirs) |
| `credential_detection` | Gold | [Skippable] Secret scanning configured (GitHub native, gitleaks, trufflehog, pre-commit hooks). Skip if CLI unavailable and no other evidence |
| `debt_marker_scanning` | Gold | Tooling tracks TODO/FIXME markers or tech debt metrics |
| `file_size_guard` | Gold | Mechanism to detect/prevent large files (hooks, CI, LFS, linter rules) |
| `dep_version_sync` | Gold | [Skippable] Dependency version drift detection for monorepos. Skip for single-app repos |
| `preview_env` | Gold | [Skippable] Non-production environment for validating changes before prod. Skip for libraries |
| `container_dev_verified` | Gold | [Skippable] Devcontainer can be built and run successfully. Skip if devcontainer CLI not installed |
| `feature_toggles` | Platinum | Feature flag system configured (LaunchDarkly, Statsig, Unleash, GrowthBook, or custom) |
| `ci_turnaround` | Platinum | [Skippable] Average CI feedback under 10 minutes. Skip if CLI unavailable |
| `build_metrics` | Platinum | [Skippable] Build performance monitoring exists (caching, metrics, optimization evidence). Skip if CLI unavailable and no other evidence |
| `deploy_cadence` | Platinum | [Skippable] Multiple deployments per week with automation. Skip if CLI unavailable |
| `gradual_rollout` | Platinum | [Skippable] Canary/percentage/ring-based rollout configured. Skip if not infra-related |
| `revert_capability` | Platinum | [Skippable] One-click or automated rollback exists. Skip if not infra-related |
| `issue_hygiene` | Platinum | [Skippable] >70% of open issues have descriptive titles and labels; <50% stale. Skip if CLI unavailable |
| `agent_guide_validation` | Platinum | Automation validates AGENTS.md stays consistent with code. Prerequisite: `agent_guide` passes |
| `stale_toggle_cleanup` | Gold | [Skippable] Dead feature flag detection tooling. Prerequisite: `feature_toggles` passes |
| `privacy_infra` | Platinum | [Skippable] Privacy compliance infrastructure (consent management, GDPR/CCPA handling). Skip for apps without user data |
| `security_report_gen` | Silver | [Skippable] SAST or security assessments produce readable reports. Skip if CLI unavailable and no other evidence |

### Application Scope Criteria (41)

| ID | Tier | Summary |
|----|------|---------|
| `linter_setup` | Bronze | A linter or static analysis tool is configured |
| `type_checker` | Bronze | Type checking configured (`tsconfig.json` strict for TS, mypy/pyright for Python, etc.) |
| `code_formatter` | Bronze | Formatter configured (Prettier for TS, Black/ruff for Python, gofmt for Go) |
| `unit_tests_present` | Bronze | Test files exist following standard naming (`*.test.ts`, `test_*.py`, `*_test.go`) |
| `commit_hooks` | Silver | Pre-commit hooks configured (Husky/lint-staged for JS, `.pre-commit-config.yaml` for Python) |
| `dep_vuln_audit` | Silver | Dependency vulnerability scanning in CI or pre-commit (npm audit, pip-audit, cargo-audit, Snyk) |
| `coverage_gates` | Silver | Minimum test coverage thresholds enforced (not just tracked) |
| `tests_executable` | Silver | Test command exists and dry-run succeeds. NEVER run the actual suite — read-only evaluation only |
| `structured_logs` | Silver | Logging library installed AND imported in at least one source file |
| `error_tracking` | Silver | Error tracking service configured (Sentry, Bugsnag, Rollbar) with source maps and context |
| `data_model` | Silver | [Skippable] Database schema definitions exist (Prisma, TypeORM, SQLAlchemy, raw SQL). Skip if no DB |
| `strict_types` | Silver | [Skippable] Strict mode enabled for language type checker. Skip if unclear |
| `integration_tests_present` | Gold | Integration/E2E test infrastructure exists (Cypress, Playwright, Behave, `tests/integration/`) |
| `test_naming_patterns` | Gold | Test framework configured with explicit naming patterns or conventions documented |
| `naming_enforcement` | Gold | Naming conventions enforced via linter rules or documented standards |
| `unused_code_scan` | Gold | Dead code detection tooling configured (knip, vulture, deadcode) |
| `duplication_scan` | Gold | Copy-paste/duplicate code detection (jscpd, SonarQube CPD) |
| `dep_pruning` | Gold | Unused dependency detection (depcheck, deptry, `go mod tidy` in CI) |
| `request_tracing` | Gold | Trace/request ID propagation (OpenTelemetry, X-Request-ID) |
| `telemetry_instrumentation` | Gold | Metrics/APM instrumentation (Datadog, Prometheus, New Relic, CloudWatch) |
| `alert_rules` | Gold | Alerting rules defined (PagerDuty, OpsGenie, custom alerts) |
| `product_analytics` | Gold | Product analytics instrumented (Mixpanel, Amplitude, PostHog, GA4) |
| `log_redaction` | Gold | Log sanitization/scrubbing mechanism configured |
| `api_contract` | Gold | [Skippable] OpenAPI/Swagger or GraphQL schema exists. Skip for non-API apps |
| `test_fixtures` | Gold | [Skippable] Seed scripts, fixture files, or factory libraries for test data. Skip if no DB |
| `pii_safeguards` | Gold | [Skippable] PII detection/handling tooling or documented procedures. Skip if no user data |
| `health_endpoints` | Gold | [Skippable] Health/readiness endpoints or probes configured. Skip for libraries/CLI tools |
| `test_duration_tracking` | Platinum | Evidence that test suite timing is monitored (verbose output, analytics platforms, artifacts) |
| `test_independence` | Platinum | Test parallelization, DB isolation, or randomization configured |
| `deploy_monitoring` | Platinum | Pointers to monitoring dashboards or deploy notification integrations |
| `module_boundaries` | Platinum | [Skippable] Code modularization enforcement (eslint-plugin-boundaries, dependency-cruiser, ArchUnit). Skip for small projects or Rust |
| `query_optimization` | Platinum | [Skippable] N+1 query detection (bullet, nplusone, DataLoader). Skip for apps without ORM |
| `bundle_weight_analysis` | Platinum | [Skippable] Bundle size analysis configured (webpack-bundle-analyzer, size-limit). Skip for non-bundled apps |
| `test_stability` | Platinum | [Skippable] Flaky test detection or retry mechanisms. Skip if CLI unavailable and no other evidence |
| `quality_dashboard` | Platinum | [Skippable] Code quality metrics tracked (coverage bots, SonarQube quality gates). Skip if CLI unavailable and no evidence |
| `error_clarity` | Platinum | [Skippable] Typed/custom error classes or structured error responses (not bare string throws). Skip for simple scripts |
| `resilience_patterns` | Platinum | [Skippable] Circuit breaker or retry-with-backoff for external calls. Skip if no external deps |
| `perf_profiling` | Platinum | [Skippable] Profiling infrastructure (APM, Pyroscope, clinic.js). Skip where profiling is not meaningful |
| `dynamic_security_scan` | Platinum | [Skippable] DAST tool in CI (OWASP ZAP, StackHawk, Nuclei). Skip for non-web-service apps |
| `complexity_analysis` | Diamond | Cyclomatic complexity analyzer or threshold enforced in CI |
| `error_issue_bridge` | Diamond | Error-tracking tool integrated with issue creation (Sentry-GitHub, PagerDuty-to-issue) |

### Recording results

For every criterion provide:
- **numerator** — integer >= 0, or `null` (only for [Skippable] criteria)
- **denominator** — 1 for repo-scope; N for app-scope
- **rationale** — concise explanation, max 500 characters

---

## Phase 4 - Validate Before Reporting

Before writing output, verify:

1. All 41 application-scope criteria have denominator = N
2. All 45 repository-scope criteria have denominator = 1
3. The report contains exactly 86 criterion keys using only the IDs listed above:
   `file_size_guard`, `debt_marker_scanning`, `build_instructions`, `dependency_lockfile`, `deterministic_builds`, `platform_cli_auth`, `pr_review_bots`, `ai_agent_workflow`, `ci_turnaround`, `build_metrics`, `deploy_cadence`, `quickstart_command`, `feature_toggles`, `changelog_generation`, `gradual_rollout`, `revert_capability`, `workspace_orchestration`, `dep_version_sync`, `deploy_pipeline`, `stale_toggle_cleanup`, `agent_guide`, `readme_present`, `doc_auto_generation`, `agent_skills`, `doc_recency`, `architecture_docs`, `agent_guide_validation`, `container_dev_env`, `env_vars_template`, `local_deps_setup`, `preview_env`, `container_dev_verified`, `incident_playbooks`, `branch_rules`, `credential_detection`, `ownership_manifest`, `security_report_gen`, `dep_update_bots`, `gitignore_coverage`, `privacy_infra`, `secrets_infra`, `issue_forms`, `issue_taxonomy`, `issue_hygiene`, `pr_forms`, `linter_setup`, `type_checker`, `code_formatter`, `commit_hooks`, `strict_types`, `naming_enforcement`, `complexity_analysis`, `unused_code_scan`, `duplication_scan`, `module_boundaries`, `query_optimization`, `bundle_weight_analysis`, `dep_pruning`, `dep_vuln_audit`, `unit_tests_present`, `integration_tests_present`, `tests_executable`, `test_duration_tracking`, `test_stability`, `coverage_gates`, `test_naming_patterns`, `test_independence`, `test_fixtures`, `api_contract`, `data_model`, `structured_logs`, `request_tracing`, `telemetry_instrumentation`, `quality_dashboard`, `error_tracking`, `error_clarity`, `alert_rules`, `deploy_monitoring`, `health_endpoints`, `resilience_patterns`, `perf_profiling`, `dynamic_security_scan`, `pii_safeguards`, `log_redaction`, `product_analytics`, `error_issue_bridge`
4. No invented criterion IDs are present

Stop and fix any inconsistencies before continuing.

---

## Phase 5 - Score and Generate Report

### Scoring

- Pass rate per criterion = numerator / denominator
- Null-numerator criteria are excluded from both sums
- Tier score = sum(numerators) / sum(denominators) for all non-null criteria at that tier, combining both repo-scope and app-scope criteria
- Achieved tier follows a gated progression:
  - **Bronze** (Tier 1): Baseline — every repo starts here
  - **Silver** (Tier 2): Unlocked when Bronze score >= 80%
  - **Gold** (Tier 3): Unlocked when Silver achieved AND Silver score >= 80%
  - **Platinum** (Tier 4): Unlocked when Gold achieved AND Gold score >= 80%
  - **Diamond** (Tier 5): Unlocked when Platinum achieved AND Platinum score >= 80%

### Persist to JSON

Resolve `repoUrl` dynamically via `git remote get-url origin`.

**Detect the agent config directory** by finding the parent of the `skills/` folder this skill was loaded from:

| Agent | Skills location | Report path |
|-------|----------------|-------------|
| Claude Code | `.claude/skills/` | `.claude/agent-readiness-report.json` |
| Zen CLI | `.zencoder/skills/` | `.zencoder/agent-readiness-report.json` |
| Codex CLI | `.codex/skills/` | `.codex/agent-readiness-report.json` |
| Gemini CLI | `.gemini/skills/` | `.gemini/agent-readiness-report.json` |

Write `agent-readiness-report.json` inside the detected agent config directory (create it if it doesn't exist). If a previous report exists at that path, read it first for delta comparison.

```json
{
  "repoUrl": "https://github.com/org/repo",
  "evaluatedAt": "2025-01-15T12:00:00Z",
  "tier": "Gold",
  "apps": {
    "apps/backend": { "description": "Primary API service" }
  },
  "criteria": {
    "readme_present": { "numerator": 1, "denominator": 1, "rationale": "README.md found with setup section" },
    "linter_setup": { "numerator": 2, "denominator": 2, "rationale": "ESLint configured for both apps" }
  }
}
```

### Human-readable summary

Present the report in this structure:

```markdown
# Tier
<Achieved tier: Bronze, Silver, Gold, Platinum, or Diamond>
<Per-tier scores: Bronze: X%, Silver: X%, Gold: X%, Platinum: X%, Diamond: X%>

# Applications
<Numbered list of every application with path and description>

# Failing Criteria (N/86)
<Only criteria where numerator < denominator, sorted by tier ascending (Bronze first = easiest wins)>
**Tier Name**
- criterion_name: X/Y - Why it failed and what would make it pass

# Passing Criteria (N/86)
<Only criteria where numerator == denominator, grouped by category>
**Category**
- criterion_name: X/Y - Brief rationale

Categories: Style & Validation, Build System, Testing, Documentation, Dev Environment, Debugging & Observability, Security

# Skipped Criteria (N/86)
- criterion_name: Skipped - Reason

# Changes Since Last Evaluation
<Only if a prior agent-readiness-report.json was found in the agent config directory>
- NEW PASS: criterion_name (previously failing)
- NEW FAIL: criterion_name (previously passing)
- Tier: Bronze/Silver/Gold/Platinum/Diamond -> Bronze/Silver/Gold/Platinum/Diamond
- Improved: X | Regressed: Y | Unchanged: Z

# Action Items
<3-5 high-impact next steps prioritized by:
  1. Lowest-tier failures first (Bronze failures block Silver)
  2. Criteria that unblock others (e.g. platform_cli_auth gates 10+ checks)
  3. Quick wins (criteria nearly passing)>
```

---

## Guidelines

- Produce identical output for identical repos
- Prefer presence checks over deep semantic analysis
- Evaluate the default branch
- When evidence is ambiguous, mark the criterion as failing
- Keep rationales brief, actionable, and under 500 characters
- Application count from Phase 2 is immutable for the entire run
- Use only the 86 defined criterion IDs

### Resource constraints

- **File tree:** If the repo exceeds 50,000 files, limit traversal to top-level directories and common source paths. Note the limitation in the report.
- **VCS API calls:** Cap at 30 + (5 x N_apps). Batch fields where possible.
- **Git log:** Never scan more than 100 commits.
- **Time target:** Aim to finish within 15 minutes. Skip individual checks that time out with "Skipped: timed out".

---

## Appendix - Evaluation Procedures

### proc_file_size_guard
Pass when any of these exist: git hooks checking file/line size, a CI job flagging oversized files, `.gitattributes` with LFS tracking, linter rules enforcing file size limits (e.g. ESLint `max-lines`, pylint `max-module-lines`), or a code-quality platform with size/complexity gates.

### proc_debt_marker_scanning
Pass when TODO/FIXME scanning runs in CI, a linter rule flags unlinked TODOs, or a platform like SonarQube/SonarCloud tracks technical debt through SQALE (enabled by default — verify it is not explicitly disabled in sonar properties).

### proc_deterministic_builds
Prerequisite: `dependency_lockfile` must pass. Then confirm CI actually consumes the lockfile with frozen install flags. Check CI workflow files for: JS (`npm ci`, `yarn --frozen-lockfile`, `pnpm --frozen-lockfile`), Python (`pip install --require-hashes`, `poetry install --no-update`, `pip-sync`), Go (`-mod=readonly`), Rust (`--locked`), Java (Gradle lockfile or `--write-locks`), Ruby (`bundle --frozen`). Fail if no CI workflows exist.

### proc_platform_cli_auth
Run `gh auth status` or `glab auth status`. This gates many Gold-tier and above checks.

### proc_pr_review_bots
With an authenticated CLI, inspect recent PRs (`gh pr list --state all --limit 10 --json reviews,comments`) for bots or automation posting review content. Look for danger.js, custom Actions comments, or AI review bots. The check targets systems that **generate** review content, not those that merely run status checks.

### proc_ai_agent_workflow
Pass when at least one **strong signal** is present:
1. Agent identifiers in git log author/co-author fields (Claude Code, Copilot, Devin, Cursor, dependabot[bot], github-actions[bot]) — check via `git log --format='%an|||%ae|||%s|||%b' -100`
2. Agent config directories with non-trivial content: `.claude/`, `.cursor/`, `.github/copilot/`, `.coderabbit.yaml`, `.devin/`, `.aider*`, `.continue/`
3. MCP server configs (`.claude/mcp.json`, `.cursor/mcp.json`)
4. CI jobs that explicitly invoke agent CLIs (`claude`, `cursor`, `aider`) for code generation or review
5. Skills/prompts directories (`.claude/skills/`, `.github/prompts/`)

Supporting signals (not sufficient alone): agent CLI references in Makefiles/scripts, substantive AGENTS.md/CLAUDE.md, `.cursorrules` / `.clinerules`.

### proc_ci_turnaround
With an authenticated CLI, pull recent merged PRs (`gh pr list --state merged --limit 20 --json statusCheckRollup`). Calculate CI duration from earliest `startedAt` to latest `completedAt`/`updatedAt` across status checks. Measure **CI check time**, not overall PR merge time. Pass if average is under 10 minutes.

### proc_build_metrics
With an authenticated CLI, inspect build step timing via `gh run view --log` or PR status rollups. Also check for build caching (turbo, nx, webpack, buildx cache), metrics exported to monitoring, or evidence of build optimization (parallelism, incremental builds). Must show deliberate performance tracking.

### proc_deploy_cadence
With an authenticated CLI, check both `gh release list --limit 30` and workflow-based deploys (`gh run list --workflow=<deploy-workflow>.yml --limit 30`). Combine both sources. Pass when multiple successful deploys per week are verifiable and deployment automation exists.

### proc_dep_version_sync
Check for syncpack, manypkg, Renovate/Dependabot grouping rules, custom CI scripts comparing versions, or monorepo tooling with version enforcement (Nx/Turborepo constraints, shared dependency configs).

### proc_deploy_pipeline
Check for CD pipelines that deploy on merge to main, semantic-release or changesets, GitOps (ArgoCD, Flux), or automated Docker image publishing.

### proc_stale_toggle_cleanup
Prerequisite: `feature_toggles` passes. Check for flag platform stale-flag detection, scripts that compare flag usage to definitions, CI jobs reporting on flag age, or documented flag lifecycle/cleanup processes.

### proc_agent_guide
File must contain actionable guidance for autonomous agents: build/test/lint commands, development workflow, project conventions. Pass if file exists and exceeds 100 characters.

### proc_agent_skills
Scan `.skills/` and `.claude/skills/` (up to repo root). Each skill should follow `{name}/SKILL.md` with YAML frontmatter (`name`, `description`) or table metadata, plus non-empty prompt content. Pass when at least one valid skill is found.

### proc_doc_recency
Run `git log --since="180 days ago" --name-only -- README.md AGENTS.md CONTRIBUTING.md` and look for `.md` matches. Pass if at least one key doc was touched recently.

### proc_architecture_docs
Check for diagram files (`*.mermaid`, `*.puml`, `*.plantuml`), `docs/architecture*`, `docs/diagrams*`, or images in README/docs whose names suggest architecture, flow, sequence, or dependency diagrams.

### proc_preview_env
Check for CI/CD jobs targeting staging/dev/preview/sandbox, environment-specific configs (`.env.staging`, `docker-compose.staging.yml`), Vercel/Netlify preview deploys, Kubernetes non-prod namespaces, or docs referencing preview URLs. Any evidence of a pre-production validation environment qualifies.

### proc_agent_guide_validation
Prerequisite: `agent_guide` passes. Check for CI jobs verifying AGENTS.md commands, automated AGENTS.md generation, pre-commit validation hooks, doc-testing tooling, or link checkers targeting AGENTS.md.

### proc_branch_rules
With an authenticated CLI, first check modern rulesets (`gh api repos/{owner}/{repo}/rulesets`). If empty, fall back to legacy protection (`gh api repos/{owner}/{repo}/branches/main/protection`). Pass if PR review requirements and direct-push prevention are configured on main/dev.

### proc_credential_detection
Check for GitHub/GitLab native secret scanning (`gh api /repos/{owner}/{repo}/secret-scanning/alerts`), CI jobs running gitleaks/trufflehog/detect-secrets, pre-commit hooks with secret scanners, or SonarQube security hotspots.

### proc_security_report_gen
With an authenticated CLI, check for SAST tools via `gh api /repos/{owner}/{repo}/code-scanning/alerts` (Semgrep, CodeQL, Snyk). Also look for dependency audit reports in PR comments, container scan summaries, or automated security assessments producing readable output.

### proc_privacy_infra
Check for consent management SDKs (OneTrust, Cookiebot), documented data retention policies, GDPR/CCPA request handling (data export/deletion endpoints), or privacy-by-design patterns (anonymization, data minimization configs).

### proc_secrets_infra
Check for cloud secrets manager integrations (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault), CI secrets usage (`secrets.*` references), encrypted secrets (SOPS, age), or proper `.env` handling (gitignored with `.env.example` template). Fail if secrets are hardcoded or no management pattern exists.

### proc_issue_hygiene
With an authenticated CLI, pull open issues (`gh issue list --state open --limit 50 --json title,createdAt,labels`). Pass if >70% have descriptive titles (>10 chars) AND at least one label. Fail if >50% are older than 365 days without recent activity.

### proc_linter_setup
Check for ESLint (`.eslintrc.*`, `eslint.config.*`), ruff/flake8 (`pyproject.toml`, `.flake8`, `ruff.toml`), SonarQube/SonarCloud (`sonar-project.properties` or CI integration), or any equivalent static analysis tool.

### proc_strict_types
Check for TS `tsconfig.json` with `"strict": true`, Python mypy strict mode, SonarQube type-related rules. Rust and Go are typed by default. Skip when unclear.

### proc_naming_enforcement
Check for ESLint `@typescript-eslint/naming-convention`, pylint naming-style rules, SonarQube naming rules, or documented naming conventions in AGENTS.md or CONTRIBUTING.md.

### proc_complexity_analysis
Check for ESLint `complexity` rule, lizard/radon for Python, gocyclo/go-critic for Go, SonarQube cognitive/cyclomatic complexity analysis.

### proc_unused_code_scan
Check for knip, ts-prune, unimported, ESLint `no-unused-vars` for JS/TS; vulture/dead for Python; deadcode/staticcheck for Go; cargo-udeps for Rust; SonarQube unused code detection.

### proc_duplication_scan
Check for jscpd in CI or pre-commit, PMD CPD for Java, SonarQube's built-in CPD.

### proc_module_boundaries
Check for eslint-plugin-boundaries, eslint-plugin-import/no-restricted-paths, dependency-cruiser, Nx module boundaries (JS/TS); ArchUnit (Java); `internal/` packages (Go); import-linter (Python).

### proc_query_optimization
Check for bullet gem (Rails), nplusone (Django), DataLoader (GraphQL), ORM query logging with analysis, or APM slow-query detection.

### proc_bundle_weight_analysis
Check for webpack-bundle-analyzer, @next/bundle-analyzer, size-limit, bundlesize, bundlewatch, rollup-plugin-visualizer, or Lighthouse CI performance budgets.

### proc_dep_pruning
Check for depcheck/npm-check/knip (JS), deptry/pip-extra-reqs (Python), `go mod tidy` in CI (Go), cargo-udeps (Rust), Maven `dependency:analyze` or Gradle dependency-analysis plugin (Java), or any CI check for unused deps.

### proc_dep_vuln_audit
Check for `npm audit`/`yarn audit` in CI, pip-audit/safety (Python), govulncheck/nancy (Go), cargo-audit (Rust), OWASP dependency-check (Java), Dependabot security config (`.github/dependabot.yml`), Renovate `vulnerabilityAlerts`, or native platform dependency scanning. Distinct from `credential_detection` (leaked secrets) and `dep_update_bots` (freshness).

### proc_tests_executable
Verify via dry-run flags only: `--listTests` (Jest), `--collect-only` (pytest), `--list` (Vitest). NEVER execute the actual test suite — it may have side effects that violate the read-only contract.

### proc_test_duration_tracking
Check for CI output with timing (jest `--verbose`, pytest `--durations`), test reports as artifacts, test analytics platform integrations (BuildPulse, Datadog CI), or configured timing flags in scripts/CI.

### proc_test_stability
With an authenticated CLI, inspect recent PRs for duplicate check names (retries indicating flakiness). Also check for retry config (jest-retry, pytest-rerunfailures), flaky test trackers (BuildPulse), CI quarantine mechanisms, or test stability metrics.

### proc_coverage_gates
Check for jest coverageThreshold, pytest `--cov-fail-under`, Codecov/Coveralls PR status checks blocking on coverage, or SonarQube quality gates with coverage thresholds. Must **enforce** minimums, not just track.

### proc_test_naming_patterns
Check for Jest `testMatch`/`testRegex`, Vitest `include`, Mocha test directory config, pytest naming in `pytest.ini`/`pyproject.toml`, Go `*_test.go` convention with existing tests, or documented naming conventions.

### proc_test_independence
Check for Jest parallelization (absence of `--runInBand`), Vitest threads, pytest-xdist, Go `t.Parallel()`, JUnit parallel config, DB isolation (transactions, testcontainers), or test randomization (pytest-randomly).

### proc_test_fixtures
Check for seed scripts (`db:seed`, `prisma db seed`), fixture files (`*.fixture.ts`, `fixtures/`), factory libraries (fishery, factory_boy, Faker), Django fixtures, SQL seed files, or Docker Compose with DB init scripts.

### proc_api_contract
Search for `**/openapi.{json,yaml,yml}`, `**/swagger.{json,yaml,yml}`, `**/schema.graphql`, `**/*.graphql`, `**/*.gql`. Pass if any valid API schema file exists anywhere in the repo.

### proc_structured_logs
Two steps: (1) Confirm a logging library in dependencies (winston/pino/bunyan for JS, structlog/loguru for Python, zap/zerolog for Go, SLF4J/Logback for Java). (2) Confirm it is actually imported in source files (not just listed in deps). Alternatively, a custom logger module (`src/logger.*`, `utils/log.*`) wrapping a library qualifies. Fail if the library exists only in dependencies with no imports.

### proc_quality_dashboard
Check for GitHub code scanning analyses (`gh api /repos/{owner}/{repo}/code-scanning/analyses`), coverage bots in PR comments (Codecov, Coveralls), coverage config in test frameworks (`--coverage` in scripts), or SonarQube quality gates.

### proc_health_endpoints
Check for `/health`, `/healthz`, `/ready`, `/live` endpoints in routes, Kubernetes liveness/readiness probes, health-check libraries (terminus, lightship, django-health-check), Docker HEALTHCHECK, or load balancer health config.

### proc_resilience_patterns
Check for circuit breaker libraries (opossum, cockatiel for Node, resilience4j for Java, tenacity for Python), service mesh circuit breaking (Istio, Linkerd), custom circuit breaker implementations, or retry-with-backoff configs.

### proc_perf_profiling
Check for APM tools (Datadog APM, New Relic, Dynatrace), continuous profiling (Pyroscope, Parca, Cloud Profiler), Node profiling (clinic.js, 0x), memory profiling setup, or flame graph generation.

### proc_dynamic_security_scan
Check for OWASP ZAP in CI, Burp Suite Enterprise, Nuclei scanner, StackHawk, or other DAST tools. Distinct from SAST — DAST tests the running application.

### proc_pii_safeguards
Check for data classification tools (Presidio, AWS Macie, Google DLP), PII detection in CI, data masking libraries, or documented PII handling in AGENTS.md/privacy docs.

### proc_log_redaction
Check for logging library redaction config (pino `redact`, winston format filtering, structlog processors), custom sanitization utilities (search for 'redact', 'sanitize', 'mask' in logging code), or log scrubbing documentation.

### proc_error_clarity
Pass when any of these exist: custom error classes extending base errors with structured fields, error response schemas with codes (`{ code: "INVALID_INPUT", ... }`), error catalog/registry files, or typed error libraries (`http-errors`, `thiserror`, Spring `ProblemDetail`). Fail if error handling consists solely of bare try/catch with string literals.

### proc_error_issue_bridge
Check for Sentry-GitHub/GitLab integration (webhooks, `SENTRY_ORG`/`SENTRY_PROJECT` in env), error-to-issue automation in CI, or PagerDuty/OpsGenie with issue creation configured.
