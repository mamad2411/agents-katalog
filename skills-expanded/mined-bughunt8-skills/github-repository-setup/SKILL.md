---
name: github-repository-setup
description: "Audit and incrementally set up a GitHub repository with documented governance, quality gates, CI, releases, security, and deployment templates. Use when asked to bootstrap, standardize, or assess repository automation."
disable-model-invocation: true
argument-hint: "[checklist | preset | search query]"
---

# GitHub Repository Setup

> Adapted from [domelic/github-repository-setup](https://github.com/domelic/github-repository-setup).
> See [ATTRIBUTION.md](ATTRIBUTION.md) for the pinned upstream snapshot and license.

Use this skill to assess or improve a repository's GitHub configuration. It
turns the upstream template catalog into a safe, incremental setup process:
inspect first, recommend a small set of compatible changes, apply only after
confirmation, and validate the result.

The upstream project provides templates and workflows as starting points, not
drop-in production guarantees. Review every generated or imported workflow for
the repository's language, permissions, secrets, deployment target, and
compliance requirements before enabling it.

## Commands

| Invocation | Purpose |
| --- | --- |
| `/github-repository-setup` | Assess the project and guide an incremental setup. |
| `/github-repository-setup checklist` | Report missing setup elements by priority without changing files. |
| `/github-repository-setup <preset>` | Plan or apply one named preset after confirmation. |
| `/github-repository-setup search <query>` | Find upstream templates by metadata and keywords. |

Presets are composable. Do not assume that a broad preset bundle is appropriate:
select the smallest set that meets the repository's current needs.

## Operating principles

- Inspect the repository and existing settings before proposing changes.
- Preserve existing configuration. Merge deliberately; never overwrite a
  workflow, ignore file, package manifest, or policy document without explicit
  approval and a clear diff.
- Ask before enabling repository settings, adding GitHub Actions workflows,
  creating labels, configuring branch protection, or introducing any service
  integration.
- Use least-privileged workflow permissions and GitHub-native OIDC where a
  cloud provider supports it. Do not place credentials in repository files.
- Prefer established project commands for build, lint, test, and release
  validation. Do not invent commands only to satisfy a template.
- Pin every downloaded upstream template to an immutable release tag or commit,
  fetch its matching checksum manifest, and verify the digest before use.
- Explain required repository secrets and variables by name, purpose, scope,
  and where to configure them. Never request or expose secret values.

## Guided setup

### 1. Inspect and classify

Identify the primary project type from its files and existing automation:

| Signals | Likely project type |
| --- | --- |
| `package.json` | Node.js or JavaScript/TypeScript |
| `pyproject.toml`, `requirements.txt` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml`, `build.gradle` | Java/JVM |
| `Gemfile` | Ruby |
| `composer.json` | PHP |
| `*.csproj`, `*.sln` | .NET |
| `pubspec.yaml` | Flutter |
| `main.tf` | Terraform |

Also inventory documentation, issue and pull-request templates, existing
workflows, dependency update tooling, release configuration, deployment
targets, branch rules, package registries, and the project's actual validation
commands. Treat the existing repository as the source of truth.

### 2. Establish requirements

Confirm only the decisions that affect the proposed files:

1. Project type and supported runtime or platform versions.
2. Whether the repository is a library, application, service, documentation
   site, internal tool, or infrastructure project.
3. Release strategy: no automation, Release Please, or a separately approved
   release process.
4. Deployment and publishing targets, if any.
5. Security baseline: GitHub-native scanning only, extra scanners, or no new
   scanners.
6. Required integrations such as notifications, observability, code coverage,
   documentation publishing, or a package registry.

Ask follow-up questions only when inspection cannot answer them. Present the
candidate files, permissions, triggers, and required secrets before applying
anything.

### 3. Select a minimal preset set

Use language presets for language-specific CI and package publishing:
`nodejs`, `python`, `go`, `rust`, `java`, `ruby`, `php`, `dotnet`, `android`,
`ios`, `flutter`, `react-native`, or `terraform`.

Add category presets only when required:

| Category | Typical coverage |
| --- | --- |
| `docs` | Contribution, security, release, ownership, and citation documents |
| `editor` | Editor settings, formatting, and development container configuration |
| `protection` | Branch protection guidance and CODEOWNERS |
| `issues` | Issue forms, pull-request templates, labels, and discussions |
| `quality` | Commit, spelling, link, Markdown, and pre-commit checks |
| `releases` | Conventional commits and Release Please |
| `security` | Dependency review, CodeQL, SBOM, and supply-chain checks |
| `deploy` | Deployment workflow for an approved platform |
| `testing` | E2E, accessibility, visual, load, or contract testing |
| `bots` | Stale, welcome, or auto-label workflows |
| `notifications` | Slack, Discord, Teams, or other approved notifications |
| `monorepo` | Workspace-aware CI and release configuration |

Specialized upstream presets cover areas such as Kubernetes, cloud deployment,
OpenAPI, Storybook, ML, games, Web3, browser extensions, desktop software,
embedded software, DAST, and mobile publishing. Search the upstream metadata
before selecting one instead of guessing its template names or requirements.

### 4. Retrieve and review templates

For a selected upstream version:

1. Retrieve `templates/presets.yaml` to confirm destination mappings,
   compatibility constraints, and required secrets.
2. Search `templates/template-index.yaml` and workflow metadata when the user
   requests a capability rather than a known preset.
3. Retrieve only the selected templates and the matching
   `templates/checksums.json`.
4. Verify SHA-256 checksums before copying a template into the repository.
5. Diff each template against the destination and adapt it to the detected
   language, package manager, branch names, and deployment model.
6. Review action versions, workflow `permissions`, trigger scope, untrusted
   pull-request behavior, and all references to secrets or repository
   variables.

Never install a template merely because it appears in a preset. Omit optional
workflows that the project cannot run or maintain.

### 5. Apply in dependency order

After approval, work in small, reviewable groups:

1. Documentation and ownership
2. Editor and repository hygiene configuration
3. Issue and pull-request collaboration files
4. Quality checks and language-specific CI
5. Dependency maintenance and security checks
6. Release automation
7. Deployment, publishing, bots, and integrations

For each group, identify required manual GitHub settings separately from
versioned repository files. Before enabling a workflow, confirm that any
referenced environment, branch protection rule, variable, secret, permission,
or external account already exists or has a documented owner.

### 6. Validate and hand off

Run the repository's existing formatter, linter, build, and test commands that
the changes affect. Validate workflow YAML and configuration syntax where
project tooling supports it. Check that:

- workflow triggers do not create loops or run privileged operations from
  untrusted code;
- the CI matrix matches supported versions;
- publishing and deployment steps are gated to the intended branch, tag, or
  environment;
- security scanners have the permissions and event coverage they require;
- all documented secrets are configured outside version control; and
- manual GitHub settings have an explicit owner and verification step.

Summarize the applied files, pending manual actions, required secrets and
variables, validation performed, and intentionally deferred presets.

## Checklist mode

Report findings under these headings without changing repository settings:

1. **Essential:** a clear README, license, contribution and security guidance,
   working CI, and a dependency-update strategy.
2. **Recommended:** ownership and review rules, issue and pull-request
   templates, formatting and quality checks, release documentation, and
   appropriate security scanning.
3. **Optional:** automated releases, deployment, publishing, notifications,
   observability, advanced testing, documentation publishing, and specialized
   integrations.

For each missing item, state why it matters, whether it is already covered by
an equivalent local solution, the smallest appropriate upstream preset, and
any manual configuration it would require.

## Search mode

Search the upstream template metadata with these filters, combining filters
with a quoted or unquoted text query when useful:

| Filter | Example |
| --- | --- |
| `language:<name>` | `language:python` |
| `type:<name>` | `type:workflow` |
| `category:<name>` | `category:security` |
| `complexity:<level>` | `complexity:starter` |
| `platform:<name>` | `platform:docker` |
| text query | `"bundle size"` |

Group results by workflow, configuration, devcontainer, gitignore,
documentation template, or hook. Include each candidate's source path,
destination, trigger, permissions, external integrations, and required
secrets before recommending it.

## Upstream resources

- [Repository and guide](https://github.com/domelic/github-repository-setup)
- [Template directory](https://github.com/domelic/github-repository-setup/tree/main/templates)
- [Preset definitions](https://github.com/domelic/github-repository-setup/blob/main/templates/presets.yaml)
- [Template index](https://github.com/domelic/github-repository-setup/blob/main/templates/template-index.yaml)
- [Workflow metadata](https://github.com/domelic/github-repository-setup/blob/main/templates/workflows/workflow-metadata.yaml)
- [Compatibility matrix](https://github.com/domelic/github-repository-setup/blob/main/docs/reference/COMPATIBILITY_MATRIX.md)
- [Template customization guide](https://github.com/domelic/github-repository-setup/blob/main/docs/guides/TEMPLATE_CUSTOMIZATION.md)
