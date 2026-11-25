---
name: triage-integration
description: "Diagnose and fix codebase integration failures, whether they occur locally (husky pre-commit/pre-push hooks, lint-staged) or remotely (GitHub Actions CI workflows). Use when a commit is rejected, a push fails, or a CI check goes red. Retrieves logs automatically and provides specific fixes for lint-codebase (typecheck, eslint, oxfmt, knip, spell-check), test-coverage, sync checks, and conventions."
argument-hint: "Optional: paste failure logs, or specify a workflow name / run URL to fetch"
---

# Triage Integration Failures

Diagnose failing integration checks in this codebase—whether they occur locally during `git commit` / `git push` or remotely in GitHub Actions CI workflows. Map errors to their root causes, read the relevant configuration, apply targeted fixes, and verify locally.

## When to Use

- A `git commit` or `git push` is rejected by a local hook (Husky, lint-staged, commitlint, validate-branch-name).
- A CI check is red on a pull request or push.
- The user pastes error logs and asks for a fix.
- Asked to "fix CI", "debug the failing check", or "triage submission errors".

## Step 1: Obtain the Logs

Determine if this is a local failure or a CI failure.

### Option A: Local Submission Failure

```sh
NX_PERF_LOGGING=false lint-staged --config configuration/lint-staged.config.ts --continue-on-error
```

Invoked directly rather than through `nx run codebase:lint-staged`. That target's own command
still carries `NODE_OPTIONS='--import=tsx'`, which the hook deliberately drops: the flag is
inherited by every command lint-staged runs, and its `--import=tsx` loader preempts the
transpiler Nx uses for workspace plugins. esbuild emits no `design:paramtypes`, so the
conformetry plugin's NestJS constructor injection would silently resolve to `undefined` and the
project graph would fail to build. Node reads the TypeScript config natively instead. The hook
also measures code (`nx run codebase:codometer:write`) and clears staged notepad files before
running lint-staged.

lint-staged config: [configuration/lint-staged.config.ts](../../../configuration/lint-staged.config.ts)

Almost every check reaches the staged files through one `nx affected` run over the
`lint-code` target:

```bash
nx affected --target=lint-code --configuration=check --parallel=8 --outputStyle=static --files=<path> --files=<path> …
```

One `--files=` flag per staged path, never one comma-separated value: Node is
killed by the operating system on a single argument past 1011 bytes, and
lint-staged reports that as `Task failed to spawn: undefined` with no output.

### commit-msg hook

File: [configuration/.husky/commit-msg](../../../configuration/.husky/commit-msg)

```sh
nx run codebase:commitlint --edit=$1
# resolves to:
NODE_OPTIONS='--import=tsx' commitlint --config configuration/commitlint.config.ts --edit <msg-file>
```

### pre-push hook

File: [configuration/.husky/pre-push](../../../configuration/.husky/pre-push)

```sh
nx run codebase:validate-branch-name
# resolves to:
validate-branch-name
# reads config from: validate-branch-name.config.cjs
```

Config: [validate-branch-name.config.cjs](../../../validate-branch-name.config.cjs)

### lint-staged pattern → command matrix

`configuration/lint-staged.config.ts` declares three patterns, in this order. A
staged `package.json` matches all three, so all four commands run.

| Staged file pattern                     | Commands lint-staged runs                                                                                                                                                                                                                                                                                            |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `{**/package.json,pnpm-workspace.yaml}` | `validation lockfile`, run as the CLI directly rather than through its Nx target                                                                                                                                                                                                                                     |
| `**/package.json`                       | `nx run-many --projects=codebase --targets=check-catalog-manifests,sherif,syncpack`                                                                                                                                                                                                                                  |
| `*` (every staged path)                 | `nx affected --target=lint-code --target=gate --target=conformetry-generators --target=conventional-config --target=devcontainer-configuration --target=pull-request-template --target=skill-exclusions --configuration=check --parallel=8 --files=…`, then `nx run-many --targets=conformetry-validate`             |

There is deliberately no per-file-type row any more. `lint-code` is an
`nx:noop` aggregator whose `dependsOn` list holds every static check, and each
leaf target declares the config files it reads in its own `inputs` — so staging
`configuration/knip.config.ts` re-runs `knip` and cache-hits the rest, with no
hand-written mapping to drift. Anything the old table routed by hand
(`sync-vscode-extensions`, `markdown-lint`, `yaml-lint`, `spell-check`) is now
reached through that `dependsOn` list.

Each derivation synchronization target is named in the same invocation rather
than reached through `dependsOn`, because each also publishes on the default
branch, and Nx forwards an explicit configuration down `dependsOn` — so an
edge there would let `lint-code --configuration=write` publish from a
branch.

`gate` is named the same way, but for a different reason: the callidescope Nx
plugin infers it with no configuration at all, so it has nothing for
`dependsOn` to forward in the first place. It stays a named sibling because
`nx affected` scopes it to the projects a commit actually touched, the same
way it scopes `lint-code` itself — a commit that deepens one project's
call stacks fails that project's own task, which the workspace-wide
`callidescope --check depth` run this replaced never could name.

There is no aggregate `synchronize` target: each synchronization command is its
own Nx target on the `synchronization` project, named here directly. Naming
them alongside keeps a commit gating call-stack depth and derivation drift
without a second `nx affected` call and the extra project graph build it would
cost.

Conformetry is the one exception to `affected`: a generated instance can drift
without matching any changed-file glob, so it validates the whole workspace on
every commit.

`nx sync:check` no longer runs on commit at all — the pre-commit hook says so in
place of the call it used to make. The generator plugin it checked is emitted
into `.conformetry` on install rather than committed, so no commit can stage it
out of date, and every conformetry command re-checks the emitted plugin against
the configuration itself.

## Triage Procedure

### Step 1: Identify the Failing Hook

Read the error output carefully. Determine which hook failed:

- **`pre-commit`** → lint-staged ran Nx targets on staged files
- **`commit-msg`** → commitlint rejected the commit message format
- **`pre-push`** → `validate-branch-name` rejected the current branch name

### Step 2: Read the Error Output

If the user did not paste error output, read the last recorded output from the pre-commit hook:

```bash
cat last-lint-staged-output.log
```

_(This file is written automatically after every commit attempt at the workspace root)._

### Option B: CI Workflow Failure

If the user gave a specific run URL or log output in `$ARGUMENTS`, fetch only that run:

```bash
gh run view <run-id> --log-failed
```

If no logs are provided, fetch ALL failing runs for the current PR:

```bash
gh pr checks --json name,state,link \
  --jq '.[] | select(.state == "FAILURE") | "\(.name) \(.link)"'
```

Parse the `<run-id>` from the link and fetch the logs for each failure.

## Step 2: Identify the Failing Target

Read the error output carefully to determine:

- Which **Nx target** failed (e.g., `oxfmt`, `eslint`, `typecheck`, `spell-check`)
- Which **project(s)** failed (e.g., `lexico`, `caelundas`, `codebase`)
- The **specific error messages** from the underlying tool

### Step 3: Locate Relevant Configuration

Use the table below to find the exact config file and command for the failing tool. Read the config file before proposing a fix.

#### `prettier` and `oxfmt` (formatting — no composite `format` target exists)

Both are independent leaf targets that `lint-code` depends on directly.

| Target     | Check command                                                                                                                               | Write command       | Config file                                                                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `prettier` | `prettier --check --config configuration/prettier.config.ts --ignore-path configuration/.prettierignore {projectRoot}` (cwd: workspaceRoot) | same with `--write` | [configuration/prettier.config.ts](../../../configuration/prettier.config.ts), [configuration/.prettierignore](../../../configuration/.prettierignore) |
| `oxfmt`    | `oxfmt -c configuration/oxfmt.config.ts --ignore-path configuration/.oxfmtignore --check {projectRoot}` (cwd: workspaceRoot)                | same with `--write` | [configuration/oxfmt.config.ts](../../../configuration/oxfmt.config.ts)                                                                                |

Python projects run `ruff-format` instead — `uv run ruff format --check .` (cwd: projectRoot),
config: [pyproject.toml](../../../pyproject.toml)

#### `eslint` and `oxlint` (linting — no composite `lint` target exists)

Both are independent leaf targets that `lint-code` depends on directly.

| Target   | Check command                                                                                                                     | Write command     | Config file                                                                                                        |
| -------- | --------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------ |
| `eslint` | `eslint . {args}` (cwd: projectRoot)                                                                                              | same with `--fix` | project `eslint.config.ts` which extends [configuration/eslint.config.ts](../../../configuration/eslint.config.ts) |
| `oxlint` | `oxlint --config configuration/oxlint.config.ts --ignore-path configuration/.oxlintignore {projectRoot}/src` (cwd: workspaceRoot) | same with `--fix` | [configuration/oxlint.config.ts](../../../configuration/oxlint.config.ts)                                          |

Python projects run `ruff-lint` instead — `uv run ruff check .` (cwd: projectRoot), config:
[pyproject.toml](../../../pyproject.toml)

#### `typecheck`

| Project type       | Command                                   | Config                                                                                              |
| ------------------ | ----------------------------------------- | --------------------------------------------------------------------------------------------------- |
| TypeScript         | `tsc --noEmit` (cwd: projectRoot)         | project `tsconfig.json` extends [configuration/tsconfig.json](../../../configuration/tsconfig.json) |
| Python (`pyright`) | `uv run pyright src/` (cwd: projectRoot)  | [pyproject.toml](../../../pyproject.toml)                                                           |
| Python (`ty`)      | `uv run ty check src/` (cwd: projectRoot) | [pyproject.toml](../../../pyproject.toml)                                                           |

#### `spell-check`

Command: `cspell --config configuration/cspell.config.yaml '{projectRoot}/**/*.{ts,tsx,js,...,py,ipynb}' --no-progress --gitignore` (cwd: workspaceRoot)
Config: [configuration/cspell.config.yaml](../../../configuration/cspell.config.yaml)

#### `markdown-lint`

|       | Command                                                                                                          | Config                                                                                    |
| ----- | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| check | `markdownlint-cli2 --config configuration/.markdownlint-cli2.jsonc '{projectRoot}/**/*.md'` (cwd: workspaceRoot) | [configuration/.markdownlint-cli2.jsonc](../../../configuration/.markdownlint-cli2.jsonc) |
| write | same with `--fix`                                                                                                |                                                                                           |

#### `yaml-lint`

Command: `uv run --project configuration yamllint -c configuration/yamllint.yaml '{projectRoot}'` (cwd: workspaceRoot)
Config: [configuration/yamllint.yaml](../../../configuration/yamllint.yaml)

#### `stylelint`

|       | Command                                                                                         | Config                                                                            |
| ----- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| check | `stylelint --config ../../configuration/stylelint.config.cjs 'src/**/*.css'` (cwd: projectRoot) | [configuration/stylelint.config.cjs](../../../configuration/stylelint.config.cjs) |
| write | same with `--fix`                                                                               |                                                                                   |

#### `knip` and `vulture` (dead-code detection — no composite `clean` target exists)

`knip` runs on TypeScript projects and `vulture` on Python projects; there is no `clean` target
on any project.

| Target             | Check command                                                                                | Config                                                                                                                    |
| ------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `knip` (TS)        | `knip --config configuration/knip.config.ts --workspace {projectRoot}` (cwd: workspaceRoot)  | [configuration/knip.config.ts](../../../configuration/knip.config.ts)                                                     |
| `vulture` (Python) | `uv run python -m vulture src/ .vulture_whitelist.py --min-confidence 80` (cwd: projectRoot) | project `.vulture_whitelist.py`, global [configuration/vulture_whitelist.py](../../../configuration/vulture_whitelist.py) |

#### `nbstripout` (affirmations only — Jupyter notebooks)

Strips cell outputs from `.ipynb` files before staging. Runs automatically on `*.ipynb` staged files.
Config: [applications/affirmations/project.json](../../../applications/affirmations/project.json)

#### Sync checks

Every synchronization command is its own Nx target on the `synchronization` project — `conformetry-generators`, `conventional-config`, `devcontainer-configuration`, `pull-request-template`, and `skill-exclusions` — run directly rather than through a shared aggregate, the same way `codebase:codometer` and `codebase:callidescope` are run. There is no `sync-*` target, no `scripts/sync-*.ts` script, and no `synchronization:synchronize` aggregate target — those were retired when the work moved into [tools/synchronization](../../../tools/synchronization). `lint-code`'s dependents name each derivation target directly.

The `nestjs-module-graphs` and `nx-project-graphs` targets were retired too, per issue #296: [codependix](../../../packages/ic-suite/codependix/codependix-cli) now derives the same NestJS module graphs and Nx neighborhood graphs through its own anchor blocks, checked by `nx run codebase:codependix` instead.

| Check command                                             | Write command           | What it validates                                                                                                                                           |
| --------------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `nx run synchronization:conformetry-generators:check`     | `:write`                | AGENTS.md generators table matches [configuration/conformetry.config.ts](../../../configuration/conformetry.config.ts)                                      |
| `nx run synchronization:conventional-config:check`        | `:write`                | Types/scopes consistent across [configuration/conventional.config.cjs](../../../configuration/conventional.config.cjs), `.vscode/settings.json`, skill docs |
| `nx run synchronization:devcontainer-configuration:check` | `:write`                | Cloud and local devcontainer configs share common fields                                                                                                    |
| `nx run synchronization:pull-request-template:check`      | `:write`                | [.github/PULL_REQUEST_TEMPLATE.md](../../../.github/PULL_REQUEST_TEMPLATE.md) in sync with skills and prompts                                               |
| `nx run synchronization:skill-exclusions:check`           | `:write`                | Installed-skill exclusion lists match `skills-lock.json`                                                                                                    |
| `nx run codebase:sync-vscode-extensions:check`            | `:write`                | `.vscode/extensions.json` matches devcontainer extension lists                                                                                              |
| `nx run codebase:codependix --configuration=check`        | `--configuration=write` | Each project's README codependix blocks match its real Nx, NestJS, and import graphs                                                                        |

> **Lesson**: If sync checks fail, it means a source of truth was edited without updating its counterpart. Example: editing `configuration/conformetry.config.ts` requires regenerating the `AGENTS.md` generators table. Editing `configuration/conventional.config.cjs` requires regenerating `.vscode/settings.json`, the PR template, and the types/scopes tables in AGENTS.md and the branch and commit skills.

There is no command that regenerates a skills table of contents. The synchronization module that once maintained the `AGENTS.md` skills list was retired along with the list itself: agents are handed the installed skills directly, so reading [.agents/skills](../../../.agents/skills) is what tells you which ones exist. A new skill needs no synchronization run — a skill added to `skills-lock.json` does, because `skill-exclusions` derives the exclusion blocks from it.

#### `check-lockfile` (package.json / pnpm-workspace.yaml changes)

Command: `validation lockfile`, the [lockfile](../../../tools/validation/src/modules/lockfile/lockfile.command.ts) check

lint-staged runs it as the CLI directly rather than through its `codebase:check-lockfile` Nx target, so one command does not cost another project graph build. Run it by hand through the target:

```bash
pnpm exec nx run codebase:check-lockfile
```

#### `commitlint` (commit-msg hook)

Command: `NODE_OPTIONS='--import=tsx' commitlint --config configuration/commitlint.config.ts --edit <msg-file>`
Config: [configuration/commitlint.config.ts](../../../configuration/commitlint.config.ts)

---

### Step 3: Apply Targeted Fixes

#### ⚠️ CRITICAL RULE: Validate Fixes But Never Run lint-staged

**After applying fixes with `--configuration=write`, you MUST:**

- ❌ **DO NOT** run `lint-staged` (this would stage the unstaged fixes, defeating the purpose)
- ❌ **DO NOT** run `git commit`
- ❌ **DO NOT** run `git push`
- ❌ **DO NOT** invoke submit, checkout-branch, or create-pull-request skills
- ✅ **DO** validate that fixes work by running the exact failing Nx target with `--configuration=check`
- ✅ **DO** leave all modified files **unstaged** so the user can review and stage them

#### Auto-Fixable Targets (run `--configuration=write`)

For these targets, run the Nx target with `--configuration=write` to auto-fix. Do NOT stage the modified files — leave them unstaged so the user can review the changes before staging.

```bash
# Format errors (oxfmt, prettier — no composite `format` target exists)
pnpm exec nx affected --target=oxfmt,prettier --configuration=write --files=<staged-files>

# Lint errors with auto-fix (ESLint --fix, oxlint --fix — no composite `lint` target exists)
pnpm exec nx affected --target=eslint,oxlint --configuration=write --files=<staged-files>

# Markdown lint with auto-fix
pnpm exec nx affected --target=markdown-lint --configuration=write --files=<staged-files>

# Unused code (knip --fix, vulture whitelist — no composite `clean` target exists)
pnpm exec nx affected --target=knip,vulture --configuration=write --files=<staged-files>

# Sync checks: run the write configuration to regenerate the out-of-sync file
pnpm exec nx run synchronization:conformetry-generators:write
pnpm exec nx run synchronization:conventional-config:write
pnpm exec nx run synchronization:devcontainer-configuration:write
pnpm exec nx run synchronization:pull-request-template:write
pnpm exec nx run synchronization:skill-exclusions:write
pnpm exec nx run codebase:sync-vscode-extensions:write
pnpm exec nx run codebase:codependix --configuration=write

# Or every derivation at once
pnpm exec nx run-many --targets=conformetry-generators,conventional-config,devcontainer-configuration,pull-request-template,skill-exclusions --configuration=write
```

#### Validate Fixes Passed

After applying fixes with `--configuration=write`, run the exact failing target with `--configuration=check` to confirm the fixes work. Use the same `--files` argument as the original failing lint-staged run:

```bash
# Validate format fixes worked
pnpm exec nx affected --target=oxfmt,prettier --configuration=check --files=<staged-files>

# Validate lint fixes worked
pnpm exec nx affected --target=eslint,oxlint --configuration=check --files=<staged-files>

# Validate markdown-lint fixes worked
pnpm exec nx affected --target=markdown-lint --configuration=check --files=<staged-files>

# Validate knip/vulture fixes worked
pnpm exec nx affected --target=knip,vulture --configuration=check --files=<staged-files>

# Validate sync checks fixed themselves (re-run the check configuration)
pnpm exec nx run-many --targets=conformetry-generators,conventional-config,devcontainer-configuration,pull-request-template,skill-exclusions --configuration=check
pnpm exec nx run codebase:sync-vscode-extensions:check
```

**If all `--configuration=check` commands pass**, the fixes are confirmed working. Proceed to Step 5.

**If a `--configuration=check` command still fails**, review the error output and apply additional manual fixes as needed, then re-validate that target.

> ✅ **Best practice:** Re-run the exact original composite `nx affected --target=... --configuration=check --files=...` command after each fix batch. A first pass may reveal additional lint/type errors hidden behind the first failure, so continue iterating until the full original command is green.

#### Manual Fix Required

| Failing target                                 | What to do                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `typecheck`                                    | Read the TypeScript/Python errors. **TS**: Use optional chaining `array[0]?.property` for index access, avoid `any`, require explicit function return types, and use `import { type Foo }` for type-only imports. **Python**: Note that `[tool.ty]` config must remain in the project-level `pyproject.toml` (not workspace root).                                                                                                                                                               |
| `spell-check`                                  | Either fix the typo, or if it's a valid word (false negative), add it to the most relevant dictionary in `configuration/.cspell/` (e.g. `lexico.txt`, `tooling.txt`). If a suitable category doesn't exist, create a new dictionary file in `configuration/.cspell/`, register it in `configuration/cspell.config.yaml`, and refactor existing dictionaries to move any relevant words into the new dictionary. As a fallback, add it directly to `words` in `configuration/cspell.config.yaml`. |
| `markdown-lint` (`MD024/no-duplicate-heading`) | Check whether duplicate headings also contain duplicate content. If content is verbatim duplicated, remove only the extra block. If content differs, keep both content blocks and rename one heading to a distinct, specific title.                                                                                                                                                                                                                                                              |
| `yaml-lint`                                    | Fix YAML syntax errors per `configuration/yamllint.yaml` rules.                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `stylelint`                                    | Fix CSS issues per `configuration/stylelint.config.cjs`.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `check-lockfile`                               | Run `pnpm install` to regenerate `pnpm-lock.yaml`. Do NOT stage the lockfile — leave it unstaged for the user to review. **Lesson**: Any manual change to a `package.json` or workspace config often requires this.                                                                                                                                                                                                                                                                              |
| `commitlint`                                   | Fix the commit message. See format below.                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `validate-branch-name`                         | Rename the branch with `git branch -m <new-valid-name>`. See format above.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `vulture` (Python)                             | Fix the flagged unused code, or add a `# noqa` comment. The project-local `.vulture_whitelist.py` and global `configuration/vulture_whitelist.py` are both read. Min-confidence is 80.                                                                                                                                                                                                                                                                                                           |

#### Invalid Branch Name (pre-push hook)

Required format: `<type>/<scope>-<description>`

- **type** and **scope**: see [Valid Types and Scopes](#valid-types-and-scopes) below
- **description**: lowercase kebab-case (e.g., `user-auth`, `fix-build-script`)

Exempt branches (no validation): `main`, `copilot/*`, `dependabot/*`, `renovate/*`

To fix, rename the current branch:

```bash
git branch -m <new-valid-name>
# example:
git branch -m feat/lexico-user-auth
```

Read [validate-branch-name.config.cjs](../../../validate-branch-name.config.cjs) to see the full regex and error message.

#### Commitlint Errors (commit-msg hook)

Required format: `<type>(<scope>): <gitmoji> <subject>`

- **type** and **scope**: see [Valid Types and Scopes](#valid-types-and-scopes) below
- **gitmoji**: Required emoji at the start of the subject (e.g., ✨ `feat`, 🐛 `fix`, 📝 `docs`, ✅ `test`, ♻️ `refactor`, ⚡️ `perf`, 🔧 `chore`, 👷 `ci`, ⬆️ deps)
- **subject**: lowercase, imperative mood, no period, max 128 chars total
- No body or footer — all context in the subject

Read `configuration/commitlint.config.ts` for the full rule set before amending.

#### Valid Types and Scopes

<!-- types-start -->

| Type | Description |
| ---- | ----------- |
| `feat` | A new feature or capability that adds value for users |
| `fix` | A bug fix that addresses a specific issue or problem |
| `docs` | Documentation, AGENTS.md, SKILL.md, README, and planning files |
| `test` | Adding or correcting unit, integration, or end-to-end tests |
| `refactor` | Code restructuring that neither fixes a bug nor adds a feature |
| `style` | Formatting, whitespace, or code structure changes with no semantic effect |
| `perf` | A code change that improves performance (caching, query optimization, etc.) |
| `chore` | Housekeeping that doesn't modify src or test files (gitignore, editor config, etc.) |
| `ci` | GitHub Actions workflows, composite actions, and CI/CD scripts |
| `build` | Build system, Vite/Docker/Helm config, or external dependency integration |
| `revert` | Reverts a previous commit |

<!-- types-end -->

<!-- scopes-start -->

| Scope | Description |
| ----- | ----------- |
| `ic-suite` | In-house code measurement and validation toolchains (Callidescope, Codependix, Codometer, Conformetry) and their shared conventions |
| `affirmations` | Python Jupyter notebook application for LangGraph affirmation generation |
| `caelundas` | Node.js CLI for astronomical calendar generation (NASA JPL ephemeris) |
| `configuration` | Workspace root config files (tsconfig, eslint, vitest, nx.json, etc.) |
| `conformetry` | Code generator templates and validation tests for generated instances |
| `dependencies` | Dependency version changes (upgrades, additions, removals via pnpm) |
| `deployments` | GitHub Actions workflows and CI/CD pipeline configuration |
| `documentation` | Markdown docs, skills, planning files, and AGENTS.md files |
| `infrastructure` | Helm charts, Terraform configs, and Kubernetes resources |
| `JimmyPaolini` | Static GitHub profile README project (markdown and assets) |
| `lexico` | TanStack Start SSR Latin dictionary web app with Supabase backend |
| `lexico-components` | Shared React/shadcn component library |
| `lexico-entities` | Shared TypeORM entities and GraphQL types |
| `lexico-ingestion` | Data ingestion scripts for Lexico |
| `meanderaw` | Greek meander (key/fret) SVG generator CLI and the composable motif/modifier library it reads |
| `sempientor` | Lexical gap discovery CLI that surveys English for morphological, phonotactic, and semantic gaps and coins words to fill them |
| `callidescope` | Call stack tracing and linting CLI, the configuration package it reads, and the packages that build and render its call graph |
| `codependix` | Dependency graph export CLI, the configuration package it reads, and the package that judges the graphs against declared rules |
| `codometer` | Code statistics measurement CLI, the configuration package it reads, and the packages that diff and render its pull request change report |
| `no-release` | Escape hatch: suppress semantic-release for any commit type |
| `release` | Version bumps and release commits generated by semantic-release |
| `reporting` | Pull request change report generation and the packages that diff and render it |
| `scripts` | Shell and TypeScript scripts in scripts/ (sync, setup, utilities) |
| `testing` | Vitest configuration, shared test utilities, and coverage setup |
| `synchronization` | Synchronization application and commands for automating workflows |
| `validation` | Validation CLI and the checks it runs, such as pull request metadata |

<!-- scopes-end -->

### Step 5: Report Errors Found and Fixes Implemented

**The skill ends here. Do NOT do anything else.**

At the end of the run, report a summary to the user covering:

1. **Errors found** — for each failing hook/target, state:
   - Which hook failed (`pre-commit`, `commit-msg`, or `pre-push`)
   - Which Nx target or tool produced the error (e.g., `eslint`, `oxfmt`, `typecheck`)
   - The specific error messages or rule violations

2. **Fixes implemented** — for each fix, state:
   - Whether it was an auto-fix command (e.g., `format --configuration=write`) or a manual code/configuration edit
   - Which files were modified (all left unstaged — the user must review and `git add` them before retrying the commit)

3. **Validation** — for each fix, state:
   - The command(s) run to validate the fix
   - The pass/fail result for each command

4. **Remaining actions** — if any issues require user action (e.g., manual typecheck fixes, commit message amend, branch rename), list them explicitly so the user knows what still needs to be done before committing. If all validations passed, state "All fixes validated. Ready to review, stage, and commit."

Use this report template:

```text
Errors Found
- <hook>: <target/tool> — <error message>

Fixes Implemented
- <auto-fix command and/or manual change>
- Files changed: <file list>

Validation
- <check command> — ✅ PASSED

Remaining Actions
- <none | explicit follow-up actions>
```

## Common Patterns

| Symptom                                   | Cause                                   | Fix                                                                                                                                                                                                                                                                                                                                                                                            |
| ----------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Unexpected token`, `Expected whitespace` | oxfmt/prettier format check failed      | `nx affected --target=oxfmt,prettier --configuration=write`                                                                                                                                                                                                                                                                                                                                    |
| `error  ...  @typescript-eslint/...`      | ESLint rule violation                   | `nx affected --target=eslint,oxlint --configuration=write` or manual fix                                                                                                                                                                                                                                                                                                                       |
| `MD024/no-duplicate-heading`              | Duplicate markdown heading in same file | If duplicated content is identical, remove one block; if content differs, keep both and rename one heading                                                                                                                                                                                                                                                                                     |
| `Type 'X' is not assignable to 'Y'`       | TypeScript type error                   | Manual fix — check `tsconfig.json` strict settings                                                                                                                                                                                                                                                                                                                                             |
| `Unknown word` in cspell                  | Unrecognized word                       | Add it to the most relevant dictionary in `configuration/.cspell/` (e.g. `lexico.txt`, `tooling.txt`). If a suitable category doesn't exist, create a new dictionary file, register it in `configuration/cspell.config.yaml`, and refactor existing dictionaries to move any relevant words into the new dictionary. As a fallback, add it to `configuration/cspell.config.yaml` `words` list. |
| `lockfile needs update`                   | `pnpm-lock.yaml` out of sync            | `pnpm install` (leave lockfile unstaged for user to review)                                                                                                                                                                                                                                                                                                                                    |
| `sync check failed`                       | Generated file is out of date           | Run the corresponding `:write` target                                                                                                                                                                                                                                                                                                                                                          |
| `subject may not be empty`                | commitlint missing subject              | Amend commit message to correct format                                                                                                                                                                                                                                                                                                                                                         |
| Knip: `Unused export`                     | Export not used anywhere                | Remove export or add to knip `ignoreBinaries`/`ignoreExports`                                                                                                                                                                                                                                                                                                                                  |

## References

### Hooks

- [configuration/.husky/pre-commit](../../../configuration/.husky/pre-commit) — runs `lint-staged` directly, bypassing `nx run codebase:lint-staged`
- [configuration/.husky/commit-msg](../../../configuration/.husky/commit-msg) — runs `nx run codebase:commitlint`
- [configuration/.husky/pre-push](../../../configuration/.husky/pre-push) — runs `nx run codebase:validate-branch-name`
- [configuration/lint-staged.config.ts](../../../configuration/lint-staged.config.ts) — file-pattern → Nx target mapping
- [validate-branch-name.config.cjs](../../../validate-branch-name.config.cjs) — branch name regex, error message, exempt patterns
- [project.json](../../../project.json) — `lint-staged`, `commitlint`, and `validate-branch-name` target definitions
- [nx.json](../../../nx.json) — default target definitions for `oxfmt`, `eslint`, `typecheck`, `spell-check`, `knip`, `vulture`, etc.

### Tool Configurations

| Tool                                | Config File                                                                                                                                            |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ESLint (base)                       | [configuration/eslint.config.ts](../../../configuration/eslint.config.ts)                                                                              |
| oxlint                              | [configuration/oxlint.config.ts](../../../configuration/oxlint.config.ts)                                                                              |
| oxfmt                               | [configuration/oxfmt.config.ts](../../../configuration/oxfmt.config.ts)                                                                                |
| Prettier                            | [configuration/prettier.config.ts](../../../configuration/prettier.config.ts), [configuration/.prettierignore](../../../configuration/.prettierignore) |
| TypeScript (base)                   | [configuration/tsconfig.json](../../../configuration/tsconfig.json)                                                                                    |
| cspell                              | [configuration/cspell.config.yaml](../../../configuration/cspell.config.yaml)                                                                          |
| markdownlint                        | [configuration/.markdownlint-cli2.jsonc](../../../configuration/.markdownlint-cli2.jsonc)                                                              |
| yamllint                            | [configuration/yamllint.yaml](../../../configuration/yamllint.yaml)                                                                                    |
| stylelint                           | [configuration/stylelint.config.cjs](../../../configuration/stylelint.config.cjs)                                                                      |
| knip                                | [configuration/knip.config.ts](../../../configuration/knip.config.ts)                                                                                  |
| Ruff + pyright                      | [pyproject.toml](../../../pyproject.toml)                                                                                                              |
| commitlint                          | [configuration/commitlint.config.ts](../../../configuration/commitlint.config.ts)                                                                      |
| validate-branch-name                | [validate-branch-name.config.cjs](../../../validate-branch-name.config.cjs)                                                                            |
| Conventional commits (types/scopes) | [configuration/conventional.config.cjs](../../../configuration/conventional.config.cjs)                                                                |
| check-lockfile                      | [tools/validation/src/modules/lockfile/lockfile.constants.ts](../../../tools/validation/src/modules/lockfile/lockfile.constants.ts)                    |

### Git Conventions

- [commit-code](../commit-code/SKILL.md)
- [checkout-branch](../checkout-branch/SKILL.md)
- [create-pull-request](../create-pull-request/SKILL.md)
- [update-pull-request](../update-pull-request/SKILL.md)
- [submit-changes](../submit-changes/SKILL.md)

## Root Cause & Prevention

> **You are in triage mode because a proactive validation step was skipped.**
>
> After resolving these failures, remind the user: **use the [validate-code skill](../validate-code/SKILL.md) before committing to catch all of these issues before pre-commit hooks run.**

Specifically, after every implementation task:

```bash
# Auto-fix format, lint, and unused-code issues
pnpm exec nx affected --target=lint-code --configuration=write --base=main

# Verify all checks pass — do not commit until this is clean
pnpm exec nx affected --target=lint-code --configuration=check --base=main
```

Running this loop _before_ staging catches 100% of the pre-commit hook failures this skill handles — formatting, linting, typecheck, spell-check, unused code, and sync checks — without any pre-commit interruption.
