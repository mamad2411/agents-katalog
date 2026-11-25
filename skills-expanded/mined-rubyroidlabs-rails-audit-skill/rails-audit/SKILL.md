---
name: rails-audit-skill
description: Perform comprehensive technical reviews of Ruby on Rails applications. Runs automated analysis tools (RubyCritic, Brakeman, bundler-audit, Gitleaks, Debride, linters, SimpleCov, Rails stats, Rails ERD), analyzes code for architecture, security, authorization (Pundit/CanCanCan), dead code, and design issues, and produces a structured markdown report with prioritized findings and a 0-10 score. Use when the user requests a tech review, code audit, project assessment, or quality analysis of a Rails application.
---

# Rails Tech Review Skill

Perform comprehensive technical reviews of Ruby on Rails applications. This skill runs automated analysis tools, inspects source code manually, and produces a structured audit report with prioritized findings.

## Audit Scope

The audit can be run in two modes:
1. **Full Application Audit**: Analyze entire Rails application (default)
2. **Targeted Audit**: Analyze specific files or directories

## Execution Flow

### Phase 1: Project Discovery

1. **Verify this is a Rails project.** Check for `config/application.rb`, `Gemfile`, and `app/` directory. If none of these exist, immediately abort and tell the user: "This does not appear to be a Ruby on Rails project. This skill only supports Rails applications."
2. Extract key metadata:
   - Ruby version (from `.ruby-version`, `Gemfile.lock`, or `.tool-versions`)
   - Rails version (from `Gemfile.lock` — look for `rails (` entry)
   - Database adapter (from `config/database.yml` or `Gemfile.lock`)
   - Background job framework (check Gemfile for Sidekiq, GoodJob, DelayedJob, Resque)
   - Frontend setup (check `package.json`, `app/javascript/`, `app/assets/`)
   - CI/CD (check `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)
   - Test framework (check for `spec/` directory → RSpec, `test/` directory → Minitest)
   - Infrastructure signals (check for `Procfile`, `Dockerfile`, `docker-compose.yml`, `app.json`)
3. Attempt `bundle install` to verify dependencies resolve. Note any failures.
4. Attempt to run the app (`bin/rails server` — just verify it starts). Note errors or missing secrets.
5. **If tests exist**, run a single quick test to verify the suite is functional:
   - RSpec: `bundle exec rspec spec/models/..._spec.rb:<line>` (pick any spec file, run one example)
   - Minitest: `bundle exec rails test test/models/..._test.rb:<line>`
   - This verifies the test framework works — the full suite can be run later with coverage instrumentation via the optional SimpleCov agent
   - If even a single test fails to run, note the errors — this is itself a finding

### Phase 2: Tool Selection

Determine which tools to use based on project characteristics:

**Linter selection logic (Ruby):**
1. Check for `.rubocop.yml` in project root OR `rubocop` in `Gemfile` → use **RuboCop**
2. Else check for `.standard.yml` in project root OR `standard` in `Gemfile` → use **standardrb**
3. Else → default to **standard + standard-rails** (install if needed)

**ESLint (JavaScript):**
- Only applicable if JS files are detected: check for `app/javascript/`, `package.json`, `.js`/`.jsx`/`.ts`/`.tsx` files
- Check if the project already has ESLint configured: look for `eslint.config.js`, `eslint.config.mjs`, `.eslintrc.js`, `.eslintrc.json`, `.eslintrc.yaml`
- If NO config file exists → skip ESLint entirely. Note in the report. Never create a config file from scratch.
- If a config file exists AND `package.json` exists → the project intends to use ESLint. Proceed (even if eslint is not yet in `package.json` or `node_modules` is missing — Phase 3 handles setup inline using the same stash/restore pattern as Ruby gems).
- If no `package.json` but JS files exist (e.g., importmaps, Sprockets) → skip ESLint

**Importmap audit (Rails 7+):**
- Check if `bin/importmap` exists and is executable AND `config/importmap.rb` exists
- If both present → the project uses importmaps; `bin/importmap audit` can check for outdated/vulnerable JS packages
- If not present → skip (not an importmap project, or Rails < 7)

**SimpleCov:** Only applicable if `spec/` or `test/` directory exists. Skip otherwise.

**Rails stats:**
- Rails 5+: run `bin/rails stats`
- Rails 4.x: run `bin/rake stats`

**Always run:** Brakeman, bundler-audit, Gitleaks, Debride (these don't need user confirmation).

**Optional (user is asked):** RubyCritic, SimpleCov (see Phase 3).

### Phase 3: Data Collection

Ask the user about optional metrics collection upfront. Tailor the question based on whether tests exist:

**If tests exist:**
- "Before starting the audit, would you like to collect automated metrics?\n\n1. **RubyCritic** — analyzes code complexity, duplication, and smells (does not run tests)\n2. **SimpleCov** — runs your full test suite with coverage instrumentation to measure line/branch coverage, test count, and pass/fail status. Runs in the background so it won't block the audit.\n\nBoth are recommended for the most thorough audit."
- Options: "Yes to both (Recommended)" / "RubyCritic only" / "SimpleCov only" / "Skip both"

**If no tests exist:**
- "Before starting the audit, would you like to run RubyCritic? It analyzes code complexity, duplication, and smells."
- Options: "Yes (Recommended)" / "Skip"
- (SimpleCov option is omitted since there are no tests to run)

**Agent launch logic:**

If the user selected SimpleCov → launch SimpleCov agent. It runs the full test suite with coverage instrumentation, capturing **both coverage data and test metrics** (test count, pass/fail status, run time).

If the user selected RubyCritic → launch RubyCritic agent.

Always launch: Brakeman, bundle-audit, Gitleaks, Debride (these don't need user confirmation).

**Launch all accepted agents in parallel** using the Task tool. The SimpleCov agent runs in the **background** — do not wait for it.

**Execution order while agents run:**
1. Execute the inline checks below ("While agents run").
2. **Wait for the foreground agents** (RubyCritic, Brakeman, bundle-audit, Gitleaks, Debride) to complete before starting Phase 5 manual review — Phase 5 consumes their data (RUBYCRITIC_DATA, BRAKEMAN_DATA, etc.).
3. Phase 4 (load references) can be done while waiting.
4. The background SimpleCov agent may still be running — collect `COVERAGE_DATA` when it completes, before writing the Testing section of the report. If it has not completed by Phase 6, note the pending status in the report rather than blocking indefinitely.

| Agent | Source | Condition | Runs in | Purpose |
|-------|--------|-----------|---------|---------|
| RubyCritic | `agents/rubycritic_agent.md` | If accepted | Foreground | Code quality score, complexity, duplication, smells |
| SimpleCov | `agents/simplecov_agent.md` | If accepted AND tests exist | **Background** | Coverage % + test metrics (count, pass/fail, run time) |
| Brakeman | `agents/brakeman_agent.md` | Always | Foreground | Security warnings |
| bundle-audit | `agents/bundle_audit_agent.md` | Always | Foreground | Gem vulnerabilities |
| Gitleaks | `agents/gitleaks_agent.md` | Always | Foreground | Secrets in git history |
| Debride | `agents/debride_agent.md` | Always | Foreground | Potentially dead methods |

**Each file-based agent invocation:**
```
Read the file agents/<agent_name>.md from the skill directory and follow all steps
described in it. The project root is: <PROJECT_ROOT>.
Return the data in the output format specified in that file.
```

**While agents run**, execute these additional checks. Some temporarily modify files (package.json, Gemfile) — use the stash/restore pattern for those and verify the working tree is clean afterward:

1. **Ruby linter**: Run the selected linter with offense reporting:
   - RuboCop: `bundle exec rubocop --format offenses --format worst` (or `rubocop` standalone)
   - standardrb: `bundle exec standardrb --format offenses` (or `standardrb` standalone)
   - Capture: total offenses, top offense types by count, worst-offending files

2. **ESLint** — if a config file exists AND `package.json` exists (from Phase 2 detection):
   - **Backup**: `git stash push -m "rails-audit-eslint-setup" -- package.json yarn.lock package-lock.json` (or `cp` fallback)
   - **Setup**: If eslint is not in `package.json`, add it: `npm install --save-dev eslint` (or `yarn add -D eslint`)
   - **Run**: `npx eslint app/javascript --format json` (or target the relevant JS directory)
   - **Capture**: total errors/warnings, top rules violated, worst-offending files
   - **Restore**: `git stash pop` (or restore from backup copies, then delete backups)
   - **Verify**: `git status` — confirm no leftover changes
   - If eslint is already present in `package.json` AND `node_modules/` exists → skip backup/restore, just run it
   - If the config file exists but eslint produces only config errors → note the config issue in the report

3. **Importmap audit** (if `bin/importmap` exists AND `config/importmap.rb` exists):
   - Run: `bin/importmap audit`
   - This checks pinned JS packages for known vulnerabilities and outdated versions
   - Capture: any vulnerabilities found, outdated packages, and the summary line
   - If the command fails or isn't available, skip — note that importmap tooling is present but `audit` may not be supported in this Rails version

4. **Rails ERD** (entity-relationship diagram + invalid association detection):
   - If `rails-erd` is in the Gemfile: run `bundle exec erd` directly
   - If not in Gemfile: use stash/restore to add `gem "rails-erd", group: :development`, `bundle install`, run, then restore (same pattern as other tools)
   - **Capture stderr** — rails-erd logs association warnings there, e.g. "WARNING: Cannot resolve association..." or "failed to load model"
   - Parse: models with invalid associations (referencing non-existent tables, columns, or classes) → High finding
   - The Mermaid diagram (`erd.mmd`) itself is documentation; the warnings are the audit value
   - Cleanup: `rm -f erd.mmd` and restore Gemfile if it was modified

5. **Rails stats**: Run `bin/rails stats` (or `bin/rake stats`)
   - Capture: code-to-test ratio, lines of code by directory

**After all agents complete**, clean up any generated files:
- `rm -rf coverage/` (if SimpleCov ran)
- `rm -rf tmp/rubycritic/` (if RubyCritic ran)
- `rm -f brakeman_output.json gitleaks-report.json bundle-audit-output.json erd.mmd`

CRITICAL: After cleanup, run `git status` and verify no files were left modified. The working tree must be clean — every temporary modification (Gemfile, package.json, yarn.lock, package-lock.json, test helpers) must have been restored to its original state. If any files are unexpectedly dirty, restore them with `git checkout -- <file>`.

**Interpreting agent responses:**
- `RUBYCRITIC_FAILED` / `COVERAGE_FAILED` / `BRAKEMAN_FAILED` / `BUNDLE_AUDIT_FAILED` / `GITLEAKS_FAILED` / `DEBRIDE_FAILED`: Note the failure reason in the report, omit or estimate that section
- `RUBYCRITIC_DATA`: parse and keep for Source Code Health and Code Design sections (score, ratings, smells, complexity)
- `BRAKEMAN_DATA`: parse and keep for Security Analysis section (warnings grouped by confidence and type)
- `BUNDLE_AUDIT_DATA`: parse and keep for Dependencies Vulnerabilities section (advisories grouped by severity)
- `GITLEAKS_DATA`: parse and keep for Git section (leaks, affected commits, secret types)
- `DEBRIDE_DATA`: parse and keep for the Dead Code subsection — potentially dead methods (candidates, not certainties)
- `COVERAGE_DATA`: parse and keep for the Testing section — includes both coverage percentages and test metrics (count, pass/fail, run time) from the SimpleCov run
- If the user skipped SimpleCov and no test suite was run, only the Phase 1 single-test verification result is available for the Testing section

### Phase 4: Load Reference Materials

Read the reference files to inform manual code review patterns:
- `references/code_smells.md` — Code smell patterns to identify
- `references/security_checklist.md` — Security vulnerability patterns + full authorization framework audit procedure
- `references/rails_antipatterns.md` — Rails-specific antipatterns
- `references/detection_patterns.md` — Grep/Glob patterns to use during manual analysis

### Phase 5: Manual Code Review

Analyze the codebase by category, cross-referencing tool output. As you review, collect findings with Problem/Priority/Solution details.

**Severity ordering:** Within each subsection, list findings from most severe to least severe — Critical first, then High, Medium, Low. This applies to both the report output and how you organize findings during review.

**Positive observations:** For each section, start with a 1-3 sentence summary of the overall assessment — including what's working well, not just problems. E.g., "In general, database structure looks good. All needed indexes are applied. There are only a few issues described below." This gives a balanced report.

#### 5.1 Back-end

**Source Code Health:**
- If RubyCritic data: report the overall score, worst-rated files (D/F ratings), most common smells, most complex files
- If no RubyCritic data: manually assess based on code review observations
- Identify files that RubyCritic flags as problematic for deeper manual review

**Dependencies:**
- Count gems in production group vs development/test
- Identify potentially unused gems (listed in Gemfile but never required/used)
- Flag gems that are unmaintained (no releases in >1 year)
- Flag gems with native extensions that could complicate deployment
- Check if `Gemfile.lock` is committed (should be) and up to date

**Dependencies Vulnerabilities:**
- If bundle-audit data: group vulnerabilities by severity (Critical/High/Medium/Low)
- For each high-severity finding, document the vulnerability and its fix

**Code Quality & Style:**
- If linter data: report total offenses, top offense types, worst-offending files
- Assess whether the team follows a consistent style
- Check if there's a linter configuration committed to the repo

**Security Analysis:**
- If brakeman data: group warnings by confidence (High/Medium/Weak) and severity
- Cross-reference with `references/security_checklist.md` patterns
- Key areas to check manually:
  - SQL injection risks (string interpolation in queries)
  - Mass assignment (`params.permit!`, missing strong parameters)
  - XSS vulnerabilities (`raw`, `html_safe`, `<%==`)
  - **Stored XSS**: check user-generated content rendered with `html_safe` or `raw` — especially document uploads, rich text fields, comments, and file contents displayed in views
  - Command injection (`system()`, backticks with user input)
  - IDOR (direct object references without authorization checks)
  - Missing authentication (`before_action :authenticate` absence)
  - CSRF protection (check for `skip_before_action :verify_authenticity_token`)
  - CSP headers (check `config/initializers/content_security_policy.rb`)
  - Redirect security (open redirects via `redirect_to params[:xxx]`)
  - **Session cookie hardening**: check `config/initializers/session_store.rb` for `secure:`, `httponly:`, `same_site:` flags. Missing flags → Medium finding. (Rails has secure defaults, but explicit configuration is preferred for auditability.)

**Authorization:**
- Detect which authorization framework is used (check `Gemfile`):
  - `pundit` → audit Pundit policies and scopes
  - `cancancan` → audit CanCanCan abilities
  - Neither → determine if authorization exists at all
- **Follow the full audit procedure in `references/security_checklist.md` → "Authorization Framework Audit"** — it is the single source of truth for what to check (policy coverage, scopes, controller integration, bypasses, safe patterns)
- Severity mapping (quick reference):
  - No framework AND no manual authorization at all → **Critical** (every user can access every record)
  - CanCanCan `can :manage, :all` without admin restriction → **Critical**
  - Pundit: missing scopes, manual filtering instead of `policy_scope`, unexplained `skip_authorization` → **High**
  - CanCanCan: missing abilities, controllers without `authorize!`/`load_and_authorize_resource` → **High**
  - Admin namespace without authorization rules → **High**
  - Missing policy for a model → **Medium**
- Cross-reference with `references/rails_antipatterns.md` "Missing Authorization Scopes" section

**Code Design & Architecture:**
- Review directory structure: are concerns properly separated?
- Check for code duplications (RubyCritic Flay data or manual observation)
- Assess architecture layers: are there too many layers with few files each? Too few layers with everything crammed together?
- Check for service objects in `app/services/` — are they named `*Service`, `*Manager`, `*Handler`?
- Assess SOLID principle adherence (Single Responsibility especially)
- Look for HTML/string concatenation in Ruby files
- Identify key models and their relationships (the ERD diagram from Phase 3)
- Check for **god helpers**: flag helpers exceeding 100 lines or with mixed responsibilities — they should be split into focused modules or presenters

**Dead Code:**
- If `DEBRIDE_DATA` collected: report the potentially dead methods (Medium priority — these are candidates from static analysis, not certainties)
- Review the filtered list from the agent — focus on the TOP_FILES and group by class
- Complement with manual checks:
  - Unreachable controllers: glob `app/controllers/` → cross-ref `config/routes.rb` — controllers with no routes
  - Unused rake tasks: check `lib/tasks/` against `rake -T` output
  - Gems in Gemfile with no corresponding `require` anywhere in the codebase
  - Dead partials/views: glob `app/views/**/_*.html.erb` → check each partial is rendered via `render` or referenced
- Findings: "potentially dead code" → Medium. Confirm with user/manual review before reporting as certain.

**Database Structure:**
- From `db/schema.rb`: assess table count, check for obvious missing indexes
- Look for foreign keys without indexes, polymorphic associations without composite indexes
- Check migration hygiene: are there model references in migrations? Missing `down` methods?
- **Invalid associations**: use the rails-erd stderr output from Phase 3 — it logs warnings like "Cannot resolve association" and "failed to load model" for models referencing non-existent tables, columns, or classes. Also check manually: associations in `app/models/` that reference non-existent tables or classes → High finding

#### 5.2 Front-end (if JS/CSS detected)

- List all JS frameworks/libraries in use (check `package.json`, importmaps, CDN references)
- Check for framework mixing (e.g., jQuery + Stimulus, multiple versions)
- If ESLint was run in Phase 3: report total errors/warnings, top rules violated, worst-offending files
- If ESLint was skipped but JS files exist: note that no linter is configured for JavaScript
- If importmap audit was run in Phase 3: report any vulnerable or outdated pinned packages
- Assess internationalization: are strings inlined in views or using I18n?
- Check Stimulus controllers for DOM query anti-patterns (`querySelector`, `getElementById`)
- Look for inline scripts/styles in views
- **PHPitis check** (logic in views): Grep views for `.where(`, `.find_by(`, `.joins(`, `.all.` — database queries embedded in the view layer instead of controllers/scopes. → Medium finding

#### 5.3 Testing

**If no test directory exists at all**, note this as a Critical finding and skip the rest of this section. The absence of automated tests is the single biggest risk to long-term maintainability.

**Test suite metrics (from Phase 3 SimpleCov agent, or Phase 1 quick check):**
- **If SimpleCov was run:** test metrics come from `COVERAGE_DATA` (the SimpleCov agent runs the full suite and captures test count, pass/fail status, and run time alongside coverage percentages)
- **If SimpleCov was skipped:** only the Phase 1 single-test verification is available — note that the suite appears functional but detailed metrics (count, time) were not collected
- Total test count and assertions (e.g., "5005 tests, 5048 assertions")
- Pass/fail status (e.g., "0 failures, 0 errors")
- Test run time (e.g., "Finished in 15 minutes 23 seconds")
- If SimpleCov reported `test_suite_passed: false`, report the failure — this is itself a finding

**Coverage data (from Phase 3 SimpleCov agent — only if user opted into SimpleCov):**
- Report coverage percentages, per-directory breakdown
- Lowest-coverage files (bottom 10)
- Files with zero coverage
- Cross-reference: files RubyCritic flagged as complex + low coverage = highest priority to test

**If no SimpleCov data was collected:**
- Estimate coverage by checking how many `app/` files have corresponding test files
- Categorize as Low / Medium / High coverage based on ratio

**Test quality assessment (manual review):**
- Assess test structure: Factory Bot usage, Four Phase Test pattern
- Look for testing anti-patterns: `sleep` in tests, hardcoded IDs, `allow(subject).to receive`, mystery guests, brittle tests
- Check if tests exercise behavior vs. implementation

#### 5.4 Git

- If gitleaks data: report total leaks, types of secrets found, affected commits
- **REDACT SECRETS**: Never include actual secret values (tokens, API keys, passwords) in the report. Describe the type and location, show only first/last 4 characters for identification, or use `***[REDACTED]***`

**Checking for sensitive files in git (use exact commands — avoid false positives):**

CRITICAL: `git ls-files <path>` always exits 0 regardless of whether the file matches. Do NOT chain it with `&&`/`||` to decide if a file is tracked — this produces false positives.

Use these correct checks instead:

1. **Is a file gitignored?** `git check-ignore -v <path>` — exits 0 (with output) if ignored, exits 1 if NOT ignored. Use this first: if a file is gitignored and has never been committed, it's safe.

2. **Is a file tracked (in the index)?** `git ls-files --error-unmatch <path>` — exits 0 if tracked, exits 1 if NOT tracked. The `--error-unmatch` flag makes the exit code meaningful.

3. **Was it ever committed?** `git log --all -- <path>` — empty output means no commits touched this file. Non-empty means it exists in history even if deleted/ignored now.

**Checklist for sensitive files:**
- `config/master.key` — must be gitignored AND never committed. If committed: Critical.
- `.env`, `.env.production`, `.env.staging` — must be gitignored. If committed: High (even if only containing public keys).
- Check for other credential files: `*.pem`, `*.p12`, `credentials.json`, `service-account.json`

**General git checklist:**
- Check for Rails credentials usage (`config/credentials/`) — is `master.key` gitignored?
- Assess git flow: branch naming conventions, PR templates, commit message quality
- Check `.gitignore` completeness: are log files, tmp files, coverage reports, `node_modules/` ignored?

#### 5.5 Infrastructure (if signals detected)

- Heroku: check `Procfile`, `app.json` — is setup straightforward? Note Heroku's end-of-development status
- AWS: check for SDK usage, S3 configuration, infrastructure-as-code
- Docker: evaluate `Dockerfile` and `docker-compose.yml` completeness
- CI/CD: assess pipeline configuration, check if linters/security scanners run in CI
- Check for deployment documentation

#### 5.6 Development Setup

- README quality: does it explain what the app does and how to set it up?
- Local setup experience: what difficulties were encountered?
- Docker Compose for dependencies?
- Seed data quality: are seeds present and functional?
- Missing config files: `.node-version`, `.ruby-version`, `.tool-versions`
- **Docs vs reality mismatch**: cross-reference documentation against actual infrastructure:
  - README/docs mention services not in Gemfile or not used (e.g., AWS SDK documented but app deployed on Heroku)
  - Outdated deployment docs (e.g., Heroku instructions when app uses Kamal/Docker)
  - Stale architecture docs describing removed features
  - Findings → Low/Medium

#### 5.7 AI Development Setup

Assess the project's AI-assisted development tooling:

- Check for: `.claude/` directory, `CLAUDE.md`, `.cursor/`, `.cursorrules`, `.github/copilot-instructions.md`, `AGENTS.md`
- Check for MCP configuration: `.mcp.json`, `.claude/settings.json` with mcp servers
- Check for project skills: `.claude/skills/` or plugin configs
- If present: assess quality — are rules consistent with the codebase? Do they cover project-specific conventions?
- If absent: recommend setting up:
  - `CLAUDE.md` (or `AGENTS.md`) — project rules: commands, architecture, conventions
  - Skills — repeatable workflows (testing, deployment)
  - MCP servers — tool integrations (databases, issue trackers)
- Findings → Low severity (nice-to-have, not critical)

### Phase 6: Generate Report

Write `RAILS_AUDIT_REPORT.md` in the project root using the structure defined in `references/report_template.md`.

**Guidelines:**
- Group related findings under category sections
- Within each section, group findings by severity using `### Critical`, `### High`, `### Medium`, `### Low` sub-headers. Omit severity levels with no findings.
- Each finding uses the Problem → Priority → Solution format. When the finding references specific code, include before/after code blocks:

  `### Critical` (or High/Medium/Low — omit empty levels)

  `#### [Issue Title]`

  `**File:** \`path/to/file.rb:line\``

  `#### Problem` — what was found, in which file(s), why it matters, concrete impact

  `#### Priority` — Critical/High/Medium/Low

  `#### Solution` — prose explanation of the fix

  `**Current Code:**` — the actual problematic code in a fenced code block

  `**Recommendation:**` — the fixed code in a fenced code block

- For structural/architectural findings without specific code to show, omit the code blocks
- **Positive notes for clean sections**: if a section has no findings, write a brief positive note (e.g., "Authentication is properly configured. No issues were found."). Don't leave sections empty.
- **REDACT SENSITIVE DATA**: Never include actual secrets, tokens, passwords, or API keys in the report. Replace secret values with `***[REDACTED]***`, or show only the first/last 4 characters for identification. This applies to: gitleaks findings, hardcoded credentials, environment variable values, and any tokens found in source code.
- The Conclusion must include a score out of 10 (rarely below 4 or above 9)
- Prioritized recommendations in three tiers: Quick Wins (immediate), Short-term (this sprint), Long-term (technical debt)
- No screenshot references — text descriptions and code blocks only
- No company branding or contact information

**Post-report artifact offer** (only if supported by the environment):

After the report is saved, detect whether the environment supports visual artifacts:
- **Claude Code (official Anthropic)**: the session model is Claude (contains "claude", "sonnet", "opus", or "haiku" — NOT "deepseek" or other non-Anthropic models). If Claude:
  Ask: "The audit report has been saved to RAILS_AUDIT_REPORT.md. Would you like me to also publish an interactive version on claude.ai? It renders the findings with severity badges, collapsible sections, and visual summaries — easier to navigate than raw markdown."
  If yes: generate a self-contained HTML artifact (`.html`) with collapsible sections per category, color-coded severity badges (Critical=red, High=orange, Medium=yellow, Low=blue), summary stats at top, and the full report content. Inline CSS/JS only (no external dependencies — CSP constraint). Publish to claude.ai via the Artifact tool.
- **Cursor**: if running inside Cursor IDE. Detect via environment: `CURSOR_TRACE_ID` env var, `TERM_PROGRAM` containing "cursor", or the presence of `.cursor/` in the project. Detection is best-effort — if you cannot confirm the environment, skip the offer. If Cursor:
  Ask: "The audit report has been saved to RAILS_AUDIT_REPORT.md. Would you like me to render it as a Cursor Canvas for an interactive view with charts and collapsible sections?"
- **Neither** (DeepSeek, other models, API-key sessions) → skip the offer entirely. Don't mention the feature.

## Severity Definitions

- **Critical**: Security vulnerabilities (brakeman high-confidence, bundle-audit high-severity CVEs, git leaks of secret keys/production credentials), data loss risks, production-breaking issues
- **High**: Missing security headers (CSP), missing authorization scopes, performance issues affecting users, missing tests for critical paths
- **Medium**: Code smells, missing tests, code duplications, convention violations, outdated but not vulnerable dependencies, maintainability concerns
- **Low**: Style inconsistencies, minor improvements, dev setup suggestions, nice-to-have features

## Report Output

Always save the audit report to `RAILS_AUDIT_REPORT.md` in the project root and present a summary to the user.
