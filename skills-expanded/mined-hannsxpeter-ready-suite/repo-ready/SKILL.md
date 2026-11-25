---
name: repo-ready
description: "Set up production-grade repository structure, documentation, CI/CD, quality tooling, and platform configuration -- across any stack (Node/Python/Go/Rust/Java/Ruby/Swift/C#/PHP/Elixir/C++/Dart) and any platform (GitHub/GitLab/Bitbucket). Use this skill whenever the user asks to 'set up a repo,' 'initialize a project,' 'add documentation,' 'set up CI,' 'configure linting,' 'add a README,' 'set up GitHub Actions,' 'make my repo professional,' 'add contributing guidelines,' 'set up release automation,' or describes wanting a clean, well-structured repository. Triggers also include requests to add a LICENSE, CHANGELOG, SECURITY.md, CODE_OF_CONDUCT, issue templates, PR templates, branch protection, dependency scanning, badges, .gitignore, .editorconfig, Makefile, devcontainer, or any 'repo hygiene' task. This skill enforces a no-placeholder rule -- every generated file must contain actionable content tailored to the project's stack, type, and stage, not generic TODO markers or lorem ipsum."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: building
upstream: []
downstream: [production-ready]
pairs_with: [production-ready]
compatible_with:
  - claude-code
  - codex
  - cursor
  - windsurf
  - antigravity
  - pi
  - openclaw
  - any-agentskills-compatible-harness
---

# Repo Ready

This skill solves one specific failure mode: repositories that look set up but aren't. A README with just the project name. A CONTRIBUTING.md full of TODOs. A SECURITY.md pointing to `security@example.com`. A `.github/workflows/ci.yml` running `echo "hello"`. Uncustomized issue templates. A LICENSE with `{{author}}` still in it. Within ten seconds of `gh repo view`, the reader knows it's a cardboard cutout.

The job is the opposite: set up a repository where every file serves a purpose, every workflow runs, every template reflects the real project. If CONTRIBUTING.md exists, it describes the real workflow. If CI exists, it runs the real test suite. If a README exists, a reader can install and use the project from it.

This is harder than it sounds -- professional repositories touch folder structure, naming, docs, platform config, CI/CD, quality tooling, security, releases, community standards, and DX. If any layer is faked, contributors and users notice. This skill provides the discipline to set up all of them.

## Core principle: relevant files, not maximum files

Don't dump every possible file into every project. A weekend CLI doesn't need GOVERNANCE.md or a 39-point audit. Enterprise SaaS can't ship without SECURITY.md, ADRs, and runbooks. The right set depends on three axes:

> **Project type** × **project stage** × **audience** = the files this repo actually needs.

A file with only placeholders is worse than no file -- it signals an unmaintained project. Every generated file must be tailored to the project's stack, type, and stage, with guidance comments where the user needs to add specifics. This principle is non-negotiable.

## When this skill triggers, do this in order

Follow this sequence. Skipping steps produces mismatched conventions and half-configured tooling.

### 0. Detect project state and research (mandatory)

Before generating anything, scan the target directory to determine mode.

- **Empty directory or single `package.json`?** -> Mode A (Greenfield). Ask minimal questions (project type, stack, stage, platform), then proceed to step 1.
- **Existing codebase with source files?** -> Mode B (Enhancement). Scan what already exists: detect stack from config files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.), inventory existing docs, check for CI config, identify the platform from `.github/` or `.gitlab/`. Build on what's there -- don't overwrite.

  **Rollback protocol (Mode B only):** if stack detection returns low-confidence signals, or a generated file would conflict with a non-obvious existing config (example: the project uses Biome but the agent was about to write `.eslintrc`), stop before writing the conflicting file. Describe the conflict to the user in plain language -- what was detected, what already exists, what would be overwritten. Propose two resolutions: (a) re-detect with different signals, or (b) leave the existing file alone and continue with the rest of the setup. Never overwrite an existing config file silently. Never run `git reset`, `git checkout --`, `git clean`, or `rm` on user state -- the agent does not own the working tree. See `references/agent-safety.md` for the full destructive-operations contract.
- **User asked to audit/improve?** -> Mode C (Audit). Load `references/audit-mode.md` for the scoring workflow; it wraps `references/repo-audit.md` and produces a prioritized fix-it list and AUDIT-REPORT.md at the repo root. Skip to fixing what's broken.
- **User is building or maintaining a multi-repo suite or library collection?** -> Mode D (Multi-repo suite). Load `references/multi-repo-suite-layout.md` for the canonical pattern (hub vs specialist repos, byte-identical collection map, coordinated version table, tag-release parity, meta-linter, five maintenance rituals). Mode D applies when at least three of these are true: the project ships across multiple git repositories under one org; at least one file lives in N repos and must be byte-identical; there is a cross-repo version table; release rituals propagate across siblings; there is a hub repo structurally distinct from specialists; the collection has its own meta-discipline (lint that runs across N repos; CI that clones siblings; coordinated patches that touch multiple repos in one logical change). Mode D wraps the per-unit scaffolding (Modes A/B) for each unit AND adds the cross-unit invariants (the meta-linter, the coordinated patch rituals, the byte-identical sync). For monorepos (subdirectories under one repo, not multiple repos), use Modes A/B with `references/monorepo-patterns.md` instead.

The scan output replaces guesswork. Do not ask questions the filesystem already answers. Rollback applies only to Mode B -- Greenfield has nothing to roll back, Audit is read-only, and Mode D operates at the cross-repo invariant layer where rollback is per-repo (use Mode B's protocol within each affected unit).

### 1. Establish the project profile (mandatory)

Before creating any files, establish these facts. Read `references/project-profiles.md` for the full matrix.

**Project type** -- determines which files are needed:

| Type | Core focus | Examples |
|---|---|---|
| **Library / SDK** | API docs, versioned changelog, publishing config | React, Lodash, Stripe SDK |
| **CLI tool** | Install methods, man pages, shell completions | gh, rg, jq |
| **Web app (SaaS)** | Runbooks, architecture docs, deploy config | Vercel Dashboard, Linear |
| **API / Microservice** | OpenAPI spec, API versioning, health checks | Stripe API, Twilio |
| **Mobile app** | Platform-specific build, store metadata | Any iOS/Android app |
| **Desktop app** | Installer packaging, auto-update, platform builds | VS Code, Obsidian |
| **DevOps / IaC** | Module docs, state management, environment configs | Terraform modules |
| **Data / ML** | Model cards, dataset docs, notebook conventions | HuggingFace models |
| **Monorepo** | Per-package docs, workspace config, shared tooling | Turborepo, Nx projects |
| **Documentation site** | Content structure, build config, deploy | Docusaurus site |
| **Framework / Platform** | Extension docs, plugin API, migration guides | Next.js, Rails |

**Project stage** -- determines how many files:

| Stage | What's appropriate | File count |
|---|---|---|
| **MVP / Side project** | Essentials only: README, LICENSE, .gitignore, basic CI | 5-8 files |
| **Growth / Team project** | + CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue templates, PR template, changelog, quality tooling | 12-18 files |
| **Enterprise / Open source** | + ADRs, runbooks, GOVERNANCE, CODEOWNERS, release automation, full CI/CD, security scanning, audit | 20-30+ files |

**Audience** -- adjusts tone and content:

| Audience | Implications |
|---|---|
| **Open source community** | Welcoming CONTRIBUTING, CODE_OF_CONDUCT, good first issue labels, funding |
| **Internal team** | Lighter docs, focus on architecture and runbooks, less community ceremony |
| **Enterprise customers** | Compliance docs, SLA, security policy, audit trail |

If the request is vague ("set up my repo"), infer from the codebase. Empty `package.json` in a fresh directory -> MVP. 50-package monorepo -> Enterprise. State assumptions and proceed. Don't ask twenty questions.

**Inline execution for Tier 1:** if the project only needs Tier 1 (5-7 files: README, LICENSE, .gitignore, .gitattributes, .editorconfig, folder structure), generate all files in a single pass. Don't delegate to subagents -- orchestration overhead exceeds the work. Tier 2+ may benefit from loading reference files in stages.

### 2. Set up folder structure (mandatory for greenfield)

Read `references/repo-structure.md` for stack-specific conventions. Folder structure must match the stack -- not a generic template. Go uses `cmd/`, `internal/`, `pkg/`; Python uses `src/package_name/`; Next.js uses `app/`. Respect the ecosystem.

**Universal directories** (apply to most projects):

```
project-root/
  src/ (or lib/, app/ -- per stack convention)
  tests/ (or test/, spec/, __tests__/ -- per stack convention)
  docs/                    # Project documentation
  scripts/                 # Build/dev scripts (not shipped to users)
  .github/ (or .gitlab/)   # Platform-specific config
```

**What goes in the root:**
- Config files the toolchain requires (package.json, pyproject.toml, Cargo.toml, etc.)
- Community standards files (README.md, LICENSE, CONTRIBUTING.md, etc.)
- Editor config (.editorconfig, .gitattributes)
- Tool configs that can't be moved (.eslintrc, .prettierrc -- or consolidated into package.json/pyproject.toml where supported)

**What does NOT go in the root:**
- Application source code (use src/ or framework convention)
- Test files (use tests/ or framework convention)
- Documentation (use docs/)
- Build artifacts (add to .gitignore)
- Secrets (never committed)

In enhancement mode, don't reorganize existing structure. Document what exists; only add missing directories.

### 2a. Detect and preserve agent-context standards

Before writing `AGENTS.md`, `CLAUDE.md`, or any agent-facing instructions, detect whether the project already uses Pillars:

- `AGENTS.md` references the Pillars standard or describes an `agents/` loading protocol.
- An `agents/` directory exists with markdown files whose frontmatter includes `pillar:`.
- The user explicitly asks to "adopt Pillars," "add agents pillars," or "standardize project context with Pillars."

If Pillars is present, preserve it. Do not overwrite the root `AGENTS.md`; update only by adding missing ready-suite or repo-ready guidance in a clearly separated section when the user asked for that edit. Do not collapse `agents/*.md` content back into AGENTS.md. Pillars keeps task-routed context in the pillar files.

If the user asks to adopt Pillars and it is absent, scaffold the minimum compatible shape:

```
project-root/
  AGENTS.md
  agents/
    context.md
    repo.md
```

`AGENTS.md` contains the Pillars loading protocol and an empty `excluded:` block. `agents/context.md` and `agents/repo.md` are always-loaded stubs with frontmatter, Scope, Context, Decisions, Rules, Workflows, Watchouts, Touchpoints, and Gaps sections. Fill only facts that are already discoverable from the repo or explicitly provided by the user. Mark unknown decisions under Gaps instead of inventing them.

### 3. Generate documentation files (mandatory)

Read `references/community-standards.md` for templates and `references/readme-craft.md` for README best practices. Generate in priority order; stop at the stage-appropriate tier.

**Critical (every project):**

| File | What it must contain | Platform detection |
|---|---|---|
| `README.md` | Project name, description, badges, install, usage, license reference | GitHub, GitLab |
| `LICENSE` | Exact SPDX-compliant license text with correct year and author | GitHub, GitLab |
| `.gitignore` | Stack-appropriate ignores, no build artifacts, no secrets, no OS files | Git |

**High (team projects and above):**

| File | What it must contain | Platform detection |
|---|---|---|
| `CONTRIBUTING.md` | Real workflow (fork? branch? trunk?), setup steps, PR process, code style | GitHub, GitLab |
| `CODE_OF_CONDUCT.md` | Contributor Covenant v2.1 with real enforcement contact | GitHub |
| `SECURITY.md` | Supported versions table, real reporting email/process, response timeline | GitHub |
| `CHANGELOG.md` | Keep a Changelog format, Unreleased section, category headers | Convention |

**Medium (open source, enterprise):**

| File | What it must contain |
|---|---|
| `SUPPORT.md` | Where to get help, community channels, response expectations |
| `CODEOWNERS` | Ownership mapping by directory/path |
| `CITATION.cff` | For academic/research projects |
| `AUTHORS` or `CONTRIBUTORS` | Initial author, contribution recognition |

Every file uses the project's actual name, author, license, and stack -- not template variables.

### 4. Configure platform integration (mandatory)

Read `references/platform-github.md`, `platform-gitlab.md`, or `platform-bitbucket.md` per target platform.

**GitHub -- generate these:**

```
.github/
  ISSUE_TEMPLATE/
    bug_report.yml          # YAML-based issue form (not old markdown)
    feature_request.yml     # Feature request form
    config.yml              # Template chooser config
  PULL_REQUEST_TEMPLATE.md  # PR checklist
  FUNDING.yml               # Sponsor button (if applicable)
  dependabot.yml            # Dependency updates
  release.yml               # Auto-generated release note categories
```

**GitLab -- generate these:**

```
.gitlab/
  issue_templates/
    Bug.md
    Feature.md
  merge_request_templates/
    Default.md
```

**Bitbucket -- generate these:**

```
bitbucket-pipelines.yml     # Pipelines 2.0 YAML (at repo root, not in a subdir)
.bitbucket/
  PULL_REQUEST_TEMPLATE.md  # PR description default
```

Bitbucket puts issue templates, default reviewers, branch permissions, and deployment environments in UI/API, not repo files -- document these in the setup guide rather than committing config.

**Platform-neutral fallback -- Azure DevOps, Gitea, Forgejo, Codeberg, SourceHut:**

No dedicated reference files for these, but most skill output still applies. Tier 1 community standards (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, .gitignore, .editorconfig) and Tier 3 licensing/security docs are platform-neutral -- they land the same on Azure DevOps, Gitea, Forgejo, Codeberg, or SourceHut as on GitHub. What changes is the platform-specific integration layer: CI syntax (Azure `azure-pipelines.yml`; Gitea Actions is GitHub-compatible; SourceHut uses `.build.yml`), template locations, and branch protection (Azure "branch policies"; Gitea/Forgejo mirror GitHub's API; SourceHut is ref-hook based). Generate platform-neutral layers directly; have the user supply platform-specific CI/protection syntax.

**Repository settings to recommend** (cannot auto-configure; document in README or setup guide):
- Description and topics for discoverability
- Social preview image (1280×640px)
- Branch protection / rulesets on main
- Auto-delete head branches after merge
- Merge strategy (squash recommended)

### 5. Set up CI/CD (mandatory for team projects)

Read `references/ci-cd-workflows.md` for workflow templates. The minimum viable CI pipeline runs on every PR:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
  push:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - # Stack-specific setup (setup-node, setup-python, setup-go, etc.)
      - # Install dependencies
      - # Lint
      - # Type check (if applicable)
      - # Test
      - # Build
```

The pipeline must run the project's real linter, type checker, test suite, and build -- not `echo "tests passed"`. If no tests exist yet, the CI step should `echo "No tests yet -- add tests before merging to main"` with a clear TODO, not a fake green check.

**Additional workflows by stage:**
- **Growth:** Release automation (semantic-release, release-please, or changesets)
- **Enterprise:** Security scanning (CodeQL, Snyk), dependency review, deploy previews

### 6. Set up quality tooling (mandatory for team projects)

Read `references/quality-tooling.md` for stack-specific recommendations. One tool per job, stack-appropriate:

| Job | JS/TS (2026) | Python | Go | Rust |
|---|---|---|---|---|
| **Lint** | Biome or ESLint v9 | Ruff | golangci-lint | clippy |
| **Format** | Biome or Prettier | Ruff | gofmt | rustfmt |
| **Type check** | TypeScript | mypy or pyright | (built-in) | (built-in) |
| **Test** | Vitest or Jest | pytest | go test | cargo test |
| **Git hooks** | Husky + lint-staged | pre-commit | Lefthook | Lefthook |
| **Commit lint** | commitlint | commitlint | commitlint | commitlint |

Plus universal config files:
- `.editorconfig` -- indent style, charset, trim whitespace, final newline
- `.gitattributes` -- line endings, LFS tracking, linguist overrides

Don't install every tool at once. Match the stage: MVP gets linter+formatter; Growth adds hooks and commit linting; Enterprise adds security scanning.

### 7. Configure security (for team projects and above)

Read `references/security-setup.md` for detailed configuration.

**For AI-agent destructive-operation hardening:** see `references/agent-safety.md` for a `.claude/settings.json` denylist template, a pre-push hook blocking force-push, and documentation of three agent behaviors this skill cannot fix by generating files alone.

**Minimum:**
- `SECURITY.md` with real reporting process (done in step 3)
- `dependabot.yml` with appropriate update schedule and grouping (done in step 4)
- Branch protection requiring PR reviews and CI pass
- `.gitignore` includes `.env`, secrets, credentials

**Growth additions:**
- CodeQL or equivalent SAST scanning workflow
- Dependency review on PRs
- Secret scanning (enabled in GitHub settings)

**Enterprise additions:**
- Signed commits policy
- SBOM generation
- Supply chain security (SLSA provenance, artifact signing)
- Compliance documentation as needed

### 8. Set up release workflow (for libraries and published software)

Read `references/release-distribution.md` for automation options.

**Release stack:**
- Semantic Versioning for version numbers
- Keep a Changelog format for CHANGELOG.md
- Conventional Commits for commit messages
- Release automation tool (pick one):
  - **semantic-release** -- fully automated, no human review of version bumps
  - **release-please** -- creates a release PR for human review (recommended for most)
  - **changesets** -- monorepo-first, human-written change descriptions

**Package publishing** (if applicable):
- npm: `package.json` metadata, `.npmignore` or `files` field, `prepublishOnly` script
- PyPI: `pyproject.toml`, trusted publishing via OIDC
- crates.io: `Cargo.toml` metadata
- Docker: multi-stage `Dockerfile`, `.dockerignore`

### 9. Run the repo health check

Read `references/repo-audit.md` and walk the scorecard before declaring setup complete. It catches the failure modes that make repos look amateur: missing license, broken CI badge, placeholder content, wrong `.gitignore`, stale dependency configs.

**-> Declare setup complete** only when the scorecard passes at the stage-appropriate level.

## Completion tiers

A fully configured repository has requirements across 4 tiers. Match the tier to the project stage.

### Decision tree: where to start, where to stop

```
START
│
├- Is this a new project (greenfield)?
│   │
│   YES -> Build from Tier 1
│   │     ├- Is this a team/open-source project? -> Continue to Tier 2
│   │     ├- Is this enterprise/mature open-source? -> Continue to Tier 3
│   │     └- Does this need full hardening? -> Continue to Tier 4
│   │
│   NO -> Existing codebase (enhancement mode)
│        │
│        ├- Has README + LICENSE + .gitignore?
│        │   NO  -> Tier 1 incomplete. Add essentials first.
│        │   YES v
│        │
│        ├- Has CONTRIBUTING + CI + quality tooling?
│        │   NO  -> Tier 2 incomplete. Add team infrastructure.
│        │   YES v
│        │
│        ├- Has security policy + release automation + community standards?
│        │   NO  -> Tier 3 incomplete. Add maturity layer.
│        │   YES v
│        │
│        └- Has signed commits + SBOM + full audit green?
│            NO  -> Tier 4 incomplete. Harden.
│            YES -> Repository is fully configured.
│
├- Is this an audit?
│   │
│   YES -> Run scorecard -> Determine current tier
│         -> Produce fix-it list for next tier's unmet requirements
│
STOP at any tier boundary -- each tier is independently complete.
```

### Tier 1: Essentials (every project, day 1)

The repository exists, is navigable, and a stranger can understand what it is.

| # | Requirement |
|---|---|
| 1 | **README.md** with project name, one-line description, install instructions, basic usage, and license reference. |
| 2 | **LICENSE** with correct SPDX text, year, and author. |
| 3 | **.gitignore** appropriate for the stack -- no build artifacts, no secrets, no OS files. |
| 4 | **.gitattributes** with line ending normalization and linguist overrides if needed. |
| 5 | **.editorconfig** with indent style, charset, trim whitespace, final newline. |
| 6 | **Folder structure** follows stack conventions. Source, tests, and docs are clearly separated. |
| 7 | **Naming conventions** are consistent: file casing matches ecosystem norms, no mixed styles. |

**Proof test:** Clone the repo -> read the README -> install -> run. If this works, Tier 1 is complete.

### Tier 2: Team Ready (team and open-source projects)

The repository supports collaboration. Contributors know how to contribute, CI enforces quality.

| # | Requirement |
|---|---|
| 8 | **CONTRIBUTING.md** describes the real development workflow, setup steps, and PR process. |
| 9 | **CODE_OF_CONDUCT.md** with Contributor Covenant and real enforcement contact. |
| 10 | **CI pipeline** runs lint, type check, test, and build on every PR. All checks pass. |
| 11 | **Quality tooling** configured: linter, formatter, and git hooks appropriate for the stack. |
| 12 | **Issue templates** (bug report + feature request) with YAML forms, plus `config.yml`. |
| 13 | **PR template** with a checklist reflecting the project's review standards. |
| 14 | **CHANGELOG.md** in Keep a Changelog format with an Unreleased section. |
| 15 | **Branch protection** on main: require PR reviews, require CI to pass. |

**Proof test:** Fork -> follow CONTRIBUTING.md -> make a change -> open PR -> CI runs -> review checklist appears. If this flow works, Tier 2 is complete.

### Tier 3: Mature (established open source, enterprise)

The repository handles security, releases, and community at scale.

| # | Requirement |
|---|---|
| 16 | **SECURITY.md** with real reporting process, supported versions, and response timeline. |
| 17 | **Release automation** configured: version bumps, changelog generation, publishing. |
| 18 | **Dependency management** automated: Dependabot or Renovate with appropriate grouping. |
| 19 | **Security scanning** in CI: SAST (CodeQL or equivalent) and dependency review. |
| 20 | **CODEOWNERS** mapping directories to responsible reviewers. |
| 21 | **README badges** showing CI status, coverage, version, license. All badges green/accurate. |
| 22 | **SUPPORT.md** with community channels and support expectations. |
| 23 | **Labels** configured: type (bug, enhancement), priority, status, area, effort. |

**Proof test:** A vulnerability is reported -> SECURITY.md tells the reporter exactly what to do. A release is cut -> changelog is auto-generated, package is published, GitHub Release is created. If both flows work, Tier 3 is complete.

### Tier 4: Hardened (critical infrastructure, regulated)

Ship-ready for environments where trust, compliance, and supply chain integrity matter.

| # | Requirement |
|---|---|
| 24 | **Signed commits** enforced via rulesets or branch protection. |
| 25 | **SBOM generation** in CI (CycloneDX or SPDX format). |
| 26 | **Supply chain security**: artifact signing, provenance attestation. |
| 27 | **Compliance documentation** appropriate for the domain (privacy policy, DPA, etc.). |
| 28 | **Architecture documentation**: ADRs, system design doc, or architecture overview. |
| 29 | **Operational documentation**: runbooks, incident response plan, SLO definitions. |
| 30 | **Full repo health scorecard** passed with no critical or high findings. |

**Proof test:** Run the full audit from `references/repo-audit.md` -> all critical and high items pass. Security scanning returns zero high/critical findings. All CI workflows are green. If the audit is clean, Tier 4 is complete.

### How tiers work in practice

- **Match tier to project.** Weekend side project -> Tier 1. Team project -> Tier 2. Mature open source -> Tier 3. Don't force Tier 4 on a hackathon.
- **Declare the completed tier explicitly** at boundaries: "Tier 2 (Team Ready) is complete. Continuing to Tier 3 for release automation and security scanning."
- **Never leave a tier half-done.** Finish the current tier before starting the next.
- **The "have-nots" apply at every tier.** No placeholders, no broken links, no template variables.
- **In enhancement mode:** determine the current tier, then work toward the next.

## The "have nots" -- things that disqualify the repo

If any of these appear in generated files, the repo fails the no-placeholder rule and must be fixed:

- `{{author}}`, `{{project}}`, `[INSERT NAME]`, or any unresolved template variable in any file
- `TODO`, `FIXME`, `TBD`, `PLACEHOLDER` in committed documentation (guidance comments like `<!-- Describe your project's purpose -->` are fine)
- `security@example.com` or any example.com address in SECURITY.md or SUPPORT.md
- A LICENSE file with the wrong license text, wrong year, or wrong author
- A `.gitignore` that doesn't match the stack (Node project missing `node_modules/`, Python missing `__pycache__/`)
- CI workflows that run `echo "test"` instead of real commands
- README badges pointing to wrong repos, wrong branches, or non-existent services
- Issue templates that weren't customized (still say "A clear and concise description of the bug")
- CONTRIBUTING.md describing a workflow the project doesn't use
- CHANGELOG.md with only `# Changelog` and nothing else
- Empty `docs/` directory with no content
- Config files for tools that aren't installed (`eslint.config.js` when the project uses Ruff)
- Multiple tools doing the same job (ESLint + Biome, Black + Ruff format)
- Files from a different ecosystem (`.npmrc` in a Python project)

When you catch yourself about to generate any of these, stop and do the real version instead.

## The "dos"

- **Do** detect the stack first -- read `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`, `Package.swift`, or equivalent.
- **Do** generate `.gitignore` from the stack (GitHub's gitignore templates as base) plus framework-specific entries.
- **Do** use YAML-based issue forms (`.yml`) on GitHub -- validation, dropdowns, required fields. Not the old Markdown format.
- **Do** put the most important info first in README: what is this, install, usage. Architecture and contributing go later.
- **Do** include a Quick Start in README that gets someone from zero to running in ≤5 commands.
- **Do** configure dependency update grouping to reduce PR noise: group minor+patch, separate major.
- **Do** put a `## License` section at the bottom of README linking to LICENSE.
- **Do** match `.editorconfig` to the project's existing style (tabs vs spaces, indent size). Don't impose a conflicting style.
- **Do** add `* text=auto` to `.gitattributes` for line ending normalization.
- **Do** include a badge row in README, ordered: CI status -> coverage -> version -> license -> downloads.
- **Do** generate a Makefile/Justfile/Taskfile with standard targets (`setup`, `dev`, `test`, `build`, `lint`, `clean`) for onboarding.

## The "don'ts"

- **Don't** generate 20 files for a project that needs 5. Match the stage.
- **Don't** pick a license without understanding the project's needs. Don't default to MIT when the project uses AGPL dependencies.
- **Don't** generate GOVERNANCE.md for a solo side project. Premature ceremony.
- **Don't** add Husky/lint-staged to a non-Node project. Use Lefthook or pre-commit.
- **Don't** configure both Dependabot and Renovate. Pick one.
- **Don't** put all config in the root when the tool supports consolidation (`pyproject.toml` for Python tools, `package.json` for some JS tools).
- **Don't** generate `.env` -- generate only `.env.example`. Real `.env` files contain secrets and must never be committed.
- **Don't** commit `package-lock.json` for a library. Do commit it for an application.
- **Don't** add badges showing failing or unknown status. Only add badges for services that are configured and passing.
- **Don't** create empty directories with only a `.gitkeep`. If a directory has no content, don't create it.
- **Don't** generate docs site config (Docusaurus, MkDocs) unless asked. Focus on in-repo Markdown docs.

## Naming conventions

Inconsistent naming is how a repo ends up with `src/utils/`, `src/helpers/`, `src/lib/`, and `src/common/` all doing the same thing. Pick conventions per layer and enforce everywhere.

### File and directory naming

| Ecosystem | Files | Directories | Enforced by |
|---|---|---|---|
| **JavaScript / TypeScript** | `PascalCase` for components (`UserList.tsx`), `kebab-case` for utilities (`date-utils.ts`) | `kebab-case`, singular (`component/`, `hook/`, `util/`) or plural | Convention, ESLint rules |
| **Python** | `snake_case` always (`user_service.py`) | `snake_case`, singular (`model/`, `service/`) | PEP 8, enforced by Ruff |
| **Go** | `snake_case` (`user_handler.go`), test files `_test.go` suffix | `lowercase`, no separators | `go build` enforces |
| **Rust** | `snake_case` (`user_service.rs`) | `snake_case` | Cargo enforces |
| **Java / Kotlin** | `PascalCase` matching class name (`UserService.java`) | Reverse domain package (`com/example/service/`) | Compiler enforces |
| **Ruby** | `snake_case` (`user_service.rb`) | `snake_case` | Convention, RuboCop |
| **Swift** | `PascalCase` (`UserService.swift`) | `PascalCase` (`Sources/`, `Tests/`) | SPM enforces |
| **C# / .NET** | `PascalCase` (`UserService.cs`) | `PascalCase` matching namespace | Convention, dotnet |
| **PHP** | `PascalCase` for classes (`UserService.php`) | `PascalCase` or framework convention | PSR-4 autoloading |

### Branch naming

| Style | Pattern | Best for |
|---|---|---|
| **Conventional** | `type/TICKET-description` | Most projects |
| **Simple** | `type/description` | Projects without issue trackers |
| **GitFlow** | `feature/`, `release/`, `hotfix/` | Versioned software with release branches |

Types: `feature/`, `fix/`, `hotfix/`, `chore/`, `docs/`, `refactor/`, `test/`

Examples: `feature/PROJ-123-add-user-search`, `fix/login-redirect-loop`, `docs/update-api-reference`

### Commit messages

Use Conventional Commits:

```
type(scope): description

feat(auth): add password reset flow
fix(api): handle null response from payment provider
docs(readme): add deployment instructions
chore(deps): bump vitest to v3.1
ci: add CodeQL security scanning
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

### Tag naming

Use `v` prefix with SemVer: `v1.0.0`, `v1.2.3-beta.1`, `v2.0.0-rc.1`

### The single most important naming rule

**Same concept, same name everywhere.** Directory `users/`, test file `users.test.ts`, endpoint `/api/users`, table `users`, README section "User Management." One word, everywhere.

## Stack detection -- know before you generate

Detect the stack from the filesystem before generating anything. This determines templates, tools, and conventions.

| File | Stack detected | Implications |
|---|---|---|
| `package.json` | Node.js / JavaScript / TypeScript | npm/pnpm/yarn, Husky, ESLint/Biome, Vitest/Jest |
| `tsconfig.json` | TypeScript | Add type-check step to CI |
| `pyproject.toml` | Python | Ruff, pytest, pyright/mypy |
| `go.mod` | Go | golangci-lint, go test, `cmd/`/`internal/` structure |
| `Cargo.toml` | Rust | clippy, cargo test, `src/`/`target/` structure |
| `build.gradle` / `pom.xml` | Java / Kotlin | Gradle/Maven, JUnit, ktlint/detekt |
| `Gemfile` | Ruby | RuboCop, RSpec, `lib/`/`spec/` structure |
| `Package.swift` | Swift | SwiftLint, XCTest, `Sources/`/`Tests/` |
| `*.csproj` / `*.sln` | C# / .NET | dotnet, NUnit/xUnit, `src/`/`tests/` |
| `composer.json` | PHP | PHPStan/Psalm, PHPUnit, PSR-4 |
| `mix.exs` | Elixir | Credo, ExUnit, `lib/`/`test/` |
| `CMakeLists.txt` | C / C++ | clang-format, CTest, `include/`/`src/` |
| `pubspec.yaml` | Dart / Flutter | dart analyze, flutter test, `lib/`/`test/` |
| `build.zig` | Zig | zig fmt, zig build test, zig-out/+zig-cache/ gitignored |
| `gleam.toml` | Gleam | gleam format, gleam test, build/+deps/ gitignored |
| `deno.json` | Deno | deno fmt+lint+test+check, deno.lock commits |
| `bun.lockb` | Bun | bun install, bun test, Biome for fmt/lint |
| `Dockerfile` | Container | Add `.dockerignore`, multi-stage build |
| `.github/` | GitHub platform | Use Actions, issue forms, FUNDING.yml |
| `.gitlab-ci.yml` | GitLab platform | Use GitLab CI, MR templates |

### Polyglot repositories -- layering tools across languages

Multiple stack indicators (e.g. `package.json` + `pyproject.toml`) = polyglot. Four rules:

**Primary vs secondary.** Whichever language answers `curl $DEPLOY_URL/` is primary; its stack leads the root README. Secondary languages get a subdirectory README and a row in the root Stack table.

**Layer, don't unify.** No linter/formatter/test-runner spans every language. Each keeps its own (Python -> Ruff + pytest + pyright; TS -> Biome + Vitest + tsc; Go -> gofmt + go vet + go test). Document layering in `CONTRIBUTING.md`.

**CI matrix.** One workflow, one job per language. FastAPI + Next.js:

```yaml
name: CI
on: [pull_request]
jobs:
  python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12", cache: pip }
      - run: pip install -e ".[dev]" && ruff check . && pytest
  frontend:
    runs-on: ubuntu-latest
    defaults: { run: { working-directory: web } }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm, cache-dependency-path: web/package-lock.json }
      - run: npm ci && npm run lint && npm test && npm run build
```

**Language boundaries.** Generate shared types from one source (FastAPI -> `openapi.json` -> `openapi-typescript` -> TS); never hand-roll both sides. JSON/HTTP for team-owned boundaries, gRPC/Protobuf when perf demands. Contract tests sit at the boundary.

Single-package polyglot differs from multi-package monorepos -- see `references/monorepo-patterns.md` for workspace tooling.

## Project type archetypes -- how to interpret vague requests

Users rarely say "set up a monorepo with Turborepo and per-package semantic-release." They say "set up my project." Interpret as:

- "Set up my repo" -> detect type from codebase, default to Tier 2
- "Make this repo professional" -> audit mode, fill gaps to Tier 3
- "Add docs" -> community standards files (README, CONTRIBUTING, etc.)
- "Set up CI" -> CI workflow matching the detected stack
- "Add linting" -> linter + formatter matching the detected stack
- "Set up releases" -> changelog + release automation + publishing config
- "Open-source this" -> Tier 3: full community standards + CI + release + security
- "Set up a monorepo" -> workspace config + per-package README + shared tooling. See `references/monorepo-patterns.md` for tool selection (Nx, Turborepo, pnpm, yarn, moon, Cargo, Go).
- "Add security" -> SECURITY.md + Dependabot + scanning workflow + branch protection guidance
- "Prepare for contributors" -> CONTRIBUTING + CODE_OF_CONDUCT + issue templates + PR template + labels
- "Set up for production" -> Tier 3 minimum, Tier 4 if regulated/critical

Pick the closest interpretation, state assumptions, and proceed. The user will redirect if needed.

## Reference files -- load on demand

The body above is enough to start. For depth on a specific layer, load the matching reference file first.

**Context budget:** Load at most 2-4 reference files per session. SKILL.md itself uses ~12K tokens; each reference adds 5-17K. Loading all 19 at once exhausts most context windows. Load only what the current tier needs -- the table shows tier and size.

| Reference file | When to load | ~Tokens |
|---|---|---|
| `references/project-profiles.md` | **Always** -- project type × stage × audience matrix | ~16K |
| `references/repo-audit.md` | **Always** -- at start (audit mode) and end (verification) | ~16K |
| `references/repo-structure.md` | **Tier 1** -- folder conventions, naming, stack-specific layouts | ~14K |
| `references/community-standards.md` | **Tier 1** -- README, LICENSE, CONTRIBUTING templates | ~8K |
| `references/readme-craft.md` | **Tier 1** -- README anatomy, badges, demos, SEO | ~9K |
| `references/audit-mode.md` | **Tier 2** -- Mode C scoring workflow, AUDIT-REPORT.md template, re-audit loop | ~10K |
| `references/multi-repo-suite-layout.md` | **Mode D.** Canonical multi-repo-suite layout (hub + N specialists; byte-identical collection map; coordinated version table; tag-release parity; meta-linter; five maintenance rituals). Loaded when the user is building or maintaining a coordinated suite of repos that ship together. Generalized from the hannsxpeter/ready-suite pattern. | ~10K |
| `references/repo-antipatterns.md` | **Tier 1+ + Mode C audits.** Named-failure-mode catalog with grep tests, severity, and per-skill guards. Complements `repo-audit.md` (the 42-criteria scorecard) and `audit-mode.md` (the scoring engine). | ~5K |
| `references/quality-tooling.md` | **Tier 2** -- linters, formatters, hooks per stack | ~16K |
| `references/ci-cd-workflows.md` | **Tier 2** -- GitHub Actions, GitLab CI templates | ~17K |
| `references/platform-github.md` | **Tier 2** -- issue templates, PR templates, settings | ~10K |
| `references/platform-gitlab.md` | **Tier 2** -- MR templates, CI config, registry | ~14K |
| `references/platform-bitbucket.md` | **Tier 2** -- Pipelines, branch permissions, deployment environments | ~14K |
| `references/git-workflows.md` | **Tier 2** -- branching strategies, label taxonomy | ~17K |
| `references/agent-safety.md` | **Tier 3** -- AI-agent destructive-ops hardening, denylist template, pre-push hook, unfixable-behavior documentation | ~14K |
| `references/monorepo-patterns.md` | **Tier 3** -- Nx, Turborepo, pnpm/yarn workspaces, moon, Cargo, Go workspaces, affected CI | ~15K |
| `references/security-setup.md` | **Tier 3** -- scanning, Dependabot, branch protection, supply chain | ~13K |
| `references/release-distribution.md` | **Tier 3** -- SemVer, changelog, publishing, automation | ~12K |
| `references/licensing-legal.md` | **Tier 3** -- license selection, CLAs, compliance docs | ~12K |
| `references/technical-docs.md` | **Tier 4** -- ADRs, whitepapers, RFCs, API docs, runbooks | ~13K |
| `references/community-governance.md` | **Tier 4** -- governance, funding, deprecation, community | ~11K |
| `references/onboarding-dx.md` | **On demand** -- Makefile, devcontainers, setup scripts, AI-agent configs | ~15K |
| `references/questioning.md` | **On demand** -- adaptive detection when auto-detect is insufficient | ~5K |

**Practical loading patterns:**
- **Tier 1 only (MVP):** project-profiles + repo-structure + community-standards (~38K tokens)
- **Tier 2 (team project):** project-profiles + quality-tooling + ci-cd-workflows + platform-github (~59K tokens)
- **Tier 3 (mature):** project-profiles + security-setup + release-distribution (~41K tokens)
- **Audit mode:** project-profiles + repo-audit (~32K tokens)

## Cross-reference map -- which generated files reference each other

Generated files reference other files (README -> CONTRIBUTING, CONTRIBUTING -> CODE_OF_CONDUCT). When generating at a tier, don't reference files not generated at that tier.

### Tier 1 (Essentials) -- self-contained
| File | References |
|---|---|
| README.md | LICENSE (always exists at Tier 1) |
| LICENSE | (none) |
| .gitignore | (none) |
| .gitattributes | (none) |
| .editorconfig | (none) |

### Tier 2 (Team Ready) -- references within tier
| File | References | Notes |
|---|---|---|
| README.md | LICENSE, CONTRIBUTING.md, CHANGELOG.md | Add Contributing and Changelog sections |
| CONTRIBUTING.md | CODE_OF_CONDUCT.md | Only reference CoC if it exists |
| CODE_OF_CONDUCT.md | (none -- self-contained) | |
| CHANGELOG.md | (none) | |
| .github/ISSUE_TEMPLATE/config.yml | SUPPORT.md, Discussions | Only link if those exist |
| .github/PULL_REQUEST_TEMPLATE.md | CONTRIBUTING.md | |

### Tier 3 (Mature) -- references across tiers
| File | References |
|---|---|
| README.md | + SECURITY.md, badges (CI, coverage, version) |
| SECURITY.md | (self-contained -- reporting process) |
| CODEOWNERS | (references directory paths, not other docs) |
| SUPPORT.md | README.md, Discussions, community channels |

### Tier 4 (Hardened) -- full cross-references
| File | References |
|---|---|
| README.md | + Architecture docs, ADRs |
| docs/adr/template.md | Prior ADRs (by number) |
| GOVERNANCE.md | CONTRIBUTING.md, CODE_OF_CONDUCT.md |

**Rule:** before referencing another file, check it was generated at the current or a lower tier. Otherwise omit or mark "add when [file] is created."

## Suite membership

repo-ready is the building-tier skill that owns repository scaffolding and hygiene. See `SUITE.md` at the repo root for the full map. The relevant siblings at a glance:

- **Planning tier:** `prd-ready` (what), `architecture-ready` (how), `roadmap-ready` (when), `stack-ready` (with what tools).
- **Building tier:** `repo-ready` (this skill, the repo scaffolding), `production-ready` (the app).
- **Shipping tier:** `deploy-ready` (ship it), `observe-ready` (keep it healthy), `launch-ready` (tell the world), `harden-ready` (survive adversarial attention).

Skills are loosely coupled: each stands alone, each composes with the others via well-defined artifacts. No skill routes through another; the harness is the router. repo-ready pairs with production-ready: repo-ready owns the repo scaffolding, production-ready owns the app wiring.

## Consumes from upstream

When the agent starts, it checks for upstream artifacts and pre-fills from them rather than asking the user to repeat decisions already made. Absence is fine; the skill runs standalone and detects the stack from the code.

| If present | repo-ready reads it during | To pre-fill |
|---|---|---|
| `.stack-ready/DECISION.md` | Stack detection | The chosen language, runtime, package manager, and platform, so the CI matrix, linter, and formatter match the stack instead of being guessed from files on disk. |
| `.prd-ready/PRD.md` | Project-type detection | Project archetype, audience, and licensing posture, so the README, CONTRIBUTING, and SECURITY.md describe the real project rather than a generic template. |
| `.architecture-ready/ARCH.md` | Repo-structure decisions | Monorepo-vs-polyrepo shape and module boundaries that inform the directory layout and any workspace configuration. |

If none is present, repo-ready detects the stack from the code (see "Stack detection") and proceeds. If an upstream artifact contradicts the code, trust the code and note the drift.

## Produces for downstream

repo-ready scaffolds the repository surface. It does not emit a single state file; the produced files themselves are the contract.

| Artifact | Path | Consumed by |
|---|---|---|
| **Repository scaffolding** | `README.md`, `CONTRIBUTING.md`, `LICENSE`, `.editorconfig`, `.gitignore`, and the linter and formatter config | `production-ready` builds app slices inside the scaffolded repo, inheriting its lint, format, and test conventions instead of re-deriving them. |
| **CI/CD workflows** | `.github/workflows/*` (or the platform equivalent) | `deploy-ready` reads the build, lint, test, and scan jobs and adds deploy stages on top rather than re-authoring them. |
| **Security baseline** | `.repo-ready/SECURITY.md` (and root `SECURITY.md`) | `harden-ready` reads the disclosure baseline and extends it into a full responsible-disclosure program. |
| **Agent brief** | `AGENTS.md` (with a `CLAUDE.md` overlay) | Any harness arriving at the repo cold reads the conventions, build commands, and forbidden actions. |

If a downstream skill is not installed, the scaffolding still stands on its own. The files are the durable artifact; there is no separate state document to maintain.

## Keep going until it's actually set up

Repo setup has a long tail. Stopping at "README and LICENSE exist" is wrong -- that's ~20% of the work. The other 80%: stack-matched .gitignore, CI running real tests, CONTRIBUTING describing the real workflow, customized issue templates, release automation hitting the right registry, a security policy with a real contact, quality tooling enforcing team standards. Budget for all of it.

When in doubt: imagine a contributor arriving tomorrow. The first thing they can't figure out is the next thing to set up.
