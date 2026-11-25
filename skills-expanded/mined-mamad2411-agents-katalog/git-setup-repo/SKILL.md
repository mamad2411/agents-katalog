---
name: git-setup-repo
description: Set up, standardize, or singularify a repository with monorepo dependency ownership, CI, Oxc, Vitest coverage, Git hooks and commit rules, workspace metadata, local services, release checks, and README onboarding. Use for new repo bootstrapping, existing repo cleanup, monorepo conversion, or dependency deduplication.
---

# Git Setup Repo

Turn a new or existing repository into a predictable, contributor-ready Singular repository. Treat this as an orchestration workflow: inspect first, agree on material choices, delegate independent lanes when useful, integrate the files, and prove that local hooks and CI run the same contracts.

## Pattern Precedence

Apply these sources in order:

1. Explicit user requirements and the target repository's local `AGENTS.md`, docs, runtime, package manager, and working conventions.
2. The current baseline encoded in this skill's references and assets.
3. Conditional variants only when the target repository has the matching package manager, framework, service, or deployment need.
4. Migration compatibility only when a current repository still depends on an older tool or layout.

Do not average conflicting examples. Preserve a working local choice unless replacing it is part of the agreed setup. The bundled files are generic public templates; do not copy organization, product, provider, tracker, reviewer, environment, or credential details from another repository.

## Read The Relevant References

- Read [references/repository-audit.md](references/repository-audit.md) for every run.
- Read [references/javascript-quality.md](references/javascript-quality.md) when the repository contains JavaScript or TypeScript.
- Read [references/monorepo-dependencies.md](references/monorepo-dependencies.md) when the repository is or may become a workspace, or dependency deduplication/ownership is in scope.
- Read [references/git-hooks.md](references/git-hooks.md) when adding or changing commit, staged-file, or push checks.
- Read [references/ci-and-services.md](references/ci-and-services.md) when creating CI or local/CI services.
- Read [references/project-documentation.md](references/project-documentation.md) when changing the README, workspace file, environment docs, or repository metadata.
- Read [references/release-and-deploy.md](references/release-and-deploy.md) only when release or deployment wiring is in scope and its target is discoverable.

Load only the references needed for the target. The entrypoint owns sequencing; references own detailed recipes.

## Workflow

### 1. Establish Scope And Safety

Read repository instructions and inspect the working tree before proposing changes:

```bash
git status --short
git branch --show-current
git log --format='%h %s' -n 20
rg --files -g 'AGENTS.md' -g 'README.md' -g 'package.json' -g '*lock*' \
  -g '.github/**' -g '.husky/**' -g '*vitest*' -g '*oxlint*' -g '*oxfmt*' \
  -g '*commitlint*' -g '*code-workspace' -g 'compose*.yml' -g 'docker-compose*.yml'
```

Identify user-owned edits, generated files, secrets, and existing automation. Never replace a working config merely because an asset exists. For an existing repository, patch in place and keep migration churn separate from behavioral changes.

### 2. Build A Repository Setup Brief

Infer what the repository needs from its files and runtime. Record:

- repository shape: single package, workspace monorepo, or polyglot;
- package manager and lockfile, runtime versions, module system, and build orchestrator;
- deployable apps, runtime boundaries, libraries, generated artifacts, and build outputs;
- dependency topology: internal package graph, production/runtime ownership, shared toolchain owners, peer contracts, repeated version declarations, and resolved duplicate copies;
- local and CI services, migrations, seed data, and health checks;
- current lint, format, type-check, test, coverage, build, and audit commands;
- current hooks, commit grammar, valid scopes, and branch/PR rules;
- README gaps, workspace folders, environment-file contract, and operational docs;
- release/deploy evidence, environments, secrets contract, and rollback path.

Keep this phase read-only. Present the target state, proposed file/package moves, and unresolved material decisions before editing.

### 3. Resolve Material Decisions

Explicit choices in the user's request are already resolved; do not ask again. Otherwise, obtain confirmation before editing when setup would:

- convert the repository to a monorepo or split, merge, move, or introduce packages/config owners;
- relocate shared dependencies, convert runtime dependencies to peers, or change a published consumer contract;
- change a Node/package-manager support range or upgrade a framework, bundler, lint, test, or other tool across a major;
- add E2E/browser infrastructure, CI coverage/thresholds/artifacts, required checks, audits, or service-backed tests with meaningful cost;
- introduce/remove services, choose destructive seed/reset behavior, or add release/deploy wiring;
- replace a formatter/linter, create repository-wide mechanical churn, or mutate remote repository settings.

Ask at most three grouped questions at a time. Give a recommended answer and state the scope, compatibility, CI-time, or maintenance trade-off. For monorepo conversion, a broad tool migration, or two or more coupled decision areas, write `Workflow recommendation: continue in Plan mode before implementation` immediately before the questions. Continue read-only discovery while answers are pending; editing lanes start only after material choices are resolved or explicitly deferred.

Stay autonomous for routine implementation inside the agreed target: current config syntax, exact file paths, template cleanup, non-breaking compatible versions for newly requested tools, focused tests, and documentation alignment.

### 4. Orchestrate Independent Lanes

Use subagents when the repository is large enough that the lanes can run independently:

- `repo-map`: inventory conventions, commands, packages, generated artifacts, and missing pieces; read-only.
- `quality-tooling`: design Oxc, Vitest, coverage, package scripts, and staged-file integration.
- `ci-services`: design CI, caching, service containers, provisioning, and optional release wiring.
- `docs-onboarding`: design README, workspace, environment, and contributor metadata.

Give each editing lane disjoint file ownership. Keep one integrator responsible for shared files such as root `package.json`, the lockfile, and the final validation contract. For a small repository, run the lanes sequentially instead of creating coordination overhead.

### 5. Verify Current Tooling Contracts

Before adding or upgrading Oxc, Vitest, Husky, lint-staged, commitlint, package-manager actions, or deployment tooling, inspect the installed version and fetch its current official documentation. Use `$context7-mcp` when available; resolve the library id first and query with the full setup question. Use official provider releases or Marketplace pages for GitHub Actions and official docs for deploy targets.

Do not invent config keys or assume the bundled examples match a different major version. Documentation snippets can lag releases: never downgrade a bundled action or dependency merely because a setup example shows an older major. Assets are starting shapes, not version authority.

### 6. Implement In Dependency Order

Implement in this order so every later layer calls a real local command:

1. Preserve the repository-supported runtime and package manager unless a change was approved; keep exactly one authoritative lockfile.
2. For an approved monorepo conversion or deduplication, establish package boundaries, dependency owners, and peer contracts before changing scripts.
3. Add or reconcile root/package scripts for format, lint/type-check, test, coverage, and build.
4. Configure Oxc and Vitest; make normal tests deterministic before enforcing coverage.
5. Configure lint-staged, Husky, and commitlint around those scripts.
6. Add approved local services and `script/provision.sh` when the app needs infrastructure.
7. Add `.github/workflows/ci.yml` using the same install, provision, lint, test, and build contracts.
8. Add the project workspace, git instructions, PR template, and README.
9. Add release/deploy automation only when its contract is evidenced and the user approved the material choices.

Prefer root scripts as the stable interface. CI and hooks should call package scripts or the monorepo runner rather than reimplement tool flags in three places.

### 7. Adapt Assets Deliberately

Reusable files live under `assets/templates/`. Resolve this installed skill's directory as `SKILL_DIR`, then copy only files that do not already exist. For existing files, compare and patch instead of overwriting.

| Target | Starting asset | Use when |
| --- | --- | --- |
| `.github/workflows/ci.yml` | `.github/workflows/ci.yml` | Baseline JavaScript/TypeScript CI |
| `.github/workflows/ci.yml` | `.github/workflows/ci-pnpm.yml` | The authoritative lockfile/package manager is pnpm |
| `.github/workflows/ci.yml` | `.github/workflows/ci-with-services.yml` | npm tests require PostgreSQL and/or Redis |
| `.github/workflows/ci.yml` | `.github/workflows/ci-pnpm-with-services.yml` | pnpm tests require PostgreSQL and/or Redis |
| `.nvmrc` | `.nvmrc` | Contributors and CI need one Node version source |
| `.gitignore` | `.gitignore` | A new repository needs baseline Node/test/build ignores |
| `.oxlintrc.json` | `.oxlintrc.json` | A TypeScript/Node-oriented Oxc baseline is appropriate |
| `.oxlintrc.json` | `.oxlintrc-react.json` | A mixed JavaScript/TypeScript React client and Node server share one root config |
| `.oxfmtrc.json` | `.oxfmtrc.json` | Oxfmt supports the repository's file types |
| `vitest.config.ts` | `vitest.config.ts` | A single TypeScript package or shared base Vitest config |
| `vitest.config.js` | `vitest.react-node.config.js` | A mixed JavaScript/TypeScript React client and Node server need distinct test environments |
| `.lintstagedrc.json` | `.lintstagedrc.json` | Oxc formats and fixes staged JS/TS files |
| `.husky/*` | `.husky/*` | The root package owns Git hooks |
| `commitlint.config.js` | `commitlint.config.js` | Commit scopes come from a workspace file |
| `<project>.code-workspace` | `project.code-workspace` | VS Code/Cursor contributors need one repository map |
| `README.md` | `README.md` | Create or materially rebuild root onboarding docs |
| `script/provision.sh` | `script/provision.sh` | Local services or migrations need one idempotent entrypoint |
| `ops/docker-compose.yml` | `ops/docker-compose.yml` | PostgreSQL/Redis are locally provisioned with Compose |
| PR template | `.github/pull_request_template.md` | The repository has no stronger local PR template |
| Git instructions | `.github/instructions/git-conventions.instructions.md` | Editor/agent commit guidance should mirror commitlint |

Example for a new file:

```bash
mkdir -p .github/workflows
cp "$SKILL_DIR/assets/templates/.github/workflows/ci.yml" .github/workflows/ci.yml
```

Assets intentionally contain `__PLACEHOLDER__` values and `TODO(git-setup-repo)` markers. Replace or delete every one. Remove unused services, framework overrides, environment variables, reporters, workspace folders, and README sections. Never leave an example secret or a nonfunctional command in the target repository.

### 8. Validate The Whole Contract

Run checks in increasing cost order and use the target package manager:

1. Parse configs and inspect the final diff for placeholders and secrets.
2. Install and run the checks with the pinned runtime and exact declared package-manager version; host-tool success is not proof of compatibility.
3. For a monorepo, inspect the resolved dependency tree, explain every duplicate version, and prove workspace packages do not rely on accidental undeclared imports.
4. Pack each affected publishable workspace and install/import it from a clean external consumer; a root workspace install is not publication proof.
5. Run format check, lint/type-check, focused tests, and build.
6. Run coverage and compare its summary with the setup brief's first-party runtime boundaries; do not accept a green partial report.
7. Run `docker compose config` and the provision/up/down flow when services changed.
8. Smoke-test lint-staged, commitlint with valid and invalid examples, and the pre-push command.
9. Validate the workflow syntax when a local checker exists, then make CI commands match the proven local commands.
10. Run `git diff --check` and confirm generated outputs are either committed intentionally or absent.

Do not trigger a deployment, publish a release, mutate remote settings, commit, or push unless the user authorized that action. If publication is requested, use `git-commit-pr` for the final commit/PR workflow.

## Definition Of Done

A repository setup is complete when:

- a fresh clone can install and reach a useful local state from the README;
- runtime, package manager, lockfile, hooks, local scripts, and CI agree;
- resolved dependencies support the pinned runtime and declared engine ranges;
- shared dependency families have an intentional lowest common owner and one resolved version/copy where constraints allow, without phantom undeclared imports;
- every affected publishable workspace packs with complete metadata/output and works in a clean external consumer;
- `Lint, Test and Build` covers formatting/linting, type checks, deterministic tests, and real build outputs;
- required services are pinned, healthy, isolated, and provisioned idempotently for development and tests;
- coverage reports meaningful source files and is not silently missing a client, server, worker, or workspace;
- commit rules and documented examples accept the same types/scopes/ticket prefixes;
- the workspace file maps real folders and recommends only relevant extensions;
- CI uses least-privilege permissions, correct caching, cancellation/queueing, timeouts, and exact tested revisions;
- all material setup choices were user-approved, already explicit, or documented as deferred;
- release/deploy wiring is either approved, proven, and documented or explicitly deferred;
- no template placeholders, copied secrets, stale commands, or unrelated rewrites remain.

## Handoff

Report the chosen repository shape, dependency-owner map and remaining duplicates, files added/changed, approved material decisions, important deviations from the baseline, services and versions, exact validation commands/results, coverage scope, hook behavior, and intentionally deferred choices or repository-host settings.
