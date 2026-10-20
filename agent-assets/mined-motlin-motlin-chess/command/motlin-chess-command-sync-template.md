---
description: Sync tool versions from this template to sibling TypeScript projects
argument-hint: [project-name|all]
---

# TypeScript Template Sync

This project (the current working directory) is the source of truth for TypeScript/Node project configurations. When creating tasks in sibling projects, always reference this template so the task has context about where the target version comes from.

Template path: !`pwd`

## Managed Configurations

### Mise Tools (.mise/config.toml)

- just
- node
- `"npm:vite-plus"` (should be `"latest"`)
- pre-commit (should be `"latest"`)

### Package.json

- `packageManager` field (pnpm version)
- devDependencies (typescript, eslint, vitest, etc.)

### Vite+ / Linting / Formatting

If the sibling does NOT use Vite+ yet (no `vite-plus` in .mise/config.toml or package.json):

1. First task: Add `"npm:vite-plus" = "latest"` to .mise/config.toml
2. Second task: Run `vp migrate` to convert from biome/eslint/prettier to oxlint/oxfmt
3. Subsequent tasks depend on this migration

If already on Vite+, compare linting config patterns.

### Pre-commit Hooks (.pre-commit-config.yaml)

- pre-commit-hooks repo version
- Local `vp staged` hook (must exist after Vite+ migration)

### GitHub Actions (.github/workflows/\*.yml)

- CI setup pattern: template uses `jdx/mise-action@v4` + pnpm cache only (no explicit setup-node, setup-python, pnpm/action-setup)
- Job structure: merge-group.yml should have pre-commit, check, build, test jobs
- **`All checks` aggregator** (critical): merge-group.yml must define an `all-checks` job with `name: All checks` using `re-actors/alls-green@release/v1` that `needs:` every other job. The paired `scripts/configure-github.sh` sets the required status check to the literal string `"All checks"` — the name must match exactly.
- pull-request.yml should have check-fix job (runs `vp check --fix`)
- Action versions should match

### Lint Configs (.markdownlint.jsonc, .markdownlint-cli2.jsonc, .yamllint.yaml)

Markdown and YAML linting is part of the template, not optional — `oxfmt` formats these file types and `pre-commit` runs the linters.

- `.markdownlint.jsonc` — rule config. Siblings may tune individual rules (e.g. disable `MD010` when the repo uses tabs in code blocks, disable `MD033` when the repo uses XML-ish tags in LLM prompts), but the file itself must exist.
- `.markdownlint-cli2.jsonc` — globs and ignores. Each sibling sets its own `ignores` list (e.g. `.llm/`, `.remember/`, generated docs directories).
- `.yamllint.yaml` — rule config plus `ignore:` block for any tool-local directories (`.serena/`, `.llm/`, `.remember/`).

Both linters are surfaced via:

- `mise.toml` entries for `"npm:markdownlint-cli2"` and `"pipx:yamllint"`
- local pre-commit hooks with `exclude:` regexes that match the `ignores` list (pre-commit passes filenames regardless of tool-level ignores, so the hook-level exclude is required as belt-and-braces).

### Scripts (scripts/configure-github.sh)

The template owns `scripts/configure-github.sh`. It reads current GitHub repo settings and offers to update branch protection, merge options, and security settings. Its branch-protection logic requires the GHA `All checks` context documented above — keep the two in sync.

### Justfile

- Recipe patterns: `vp install` vs `pnpm install`, `vp check`, CI env detection
- Compare recipe structure with template justfile

## Sibling Projects

If $ARGUMENTS is a specific project name, only sync that project. If $ARGUMENTS is "all" or empty, sync all projects.

Read the project list from `.llm/sync-projects.md` (gitignored, machine-specific).

## Workflow

### Step 1: Update This Template

Check if this template's versions are the latest:

```bash
mise ls-remote just | tail -1
mise ls-remote node | grep "^24" | tail -1
npm outdated
```

Compare with `.mise/config.toml` and `package.json` in this project. If outdated, update them first.

Also read the full configuration set for comparison in Step 3:

- `.mise/config.toml`
- `package.json` (packageManager + devDependencies)
- `.pre-commit-config.yaml`
- `.github/workflows/*.yml`
- `.markdownlint.jsonc` and `.markdownlint-cli2.jsonc`
- `.yamllint.yaml`
- `scripts/configure-github.sh`
- `justfile`

### Step 2: Pull Improvements from Siblings

Scan sibling projects for any versions NEWER than this template.

If a sibling has a newer version:

1. Ask the user whether to pull it in
2. Update this template to match
3. Then push to all other siblings

### Step 3: Push Template Versions to Siblings

For each sibling project, compare versions and create tasks for any mismatches.

Replace each sibling's `.llm/todo.md` with fresh tasks (do not append to stale lists).

### Task Templates

Every task MUST include a `Source:` line referencing this template project so the task executor knows where the target version comes from. Tasks with prerequisites should state them explicitly.

**Mise tool update:**

```
Update <tool> <current> → <target>
  Edit .mise/config.toml
  Change: <tool> = "<current>"
  To: <tool> = "<target>"
  Source: ~/projects/typescript-template
```

**Package.json dependency update:**

```
Update <dep> <current> → <target>
  Edit package.json devDependencies
  Change: "<dep>": "<current>"
  To: "<dep>": "<target>"
  Run: npm install
  Source: ~/projects/typescript-template
```

**pnpm version update:**

```
Update pnpm <current> → <target>
  Edit package.json
  Change: "packageManager": "pnpm@<current>"
  To: "packageManager": "pnpm@<target>"
  Also update all .github/workflows/*.yml where pnpm version is pinned
  Run: pnpm install to regenerate lockfile
  Source: ~/projects/typescript-template
```

**Vite+ migration (for projects not yet on Vite+):**

First task (prerequisite):

```
Add vite-plus to mise config (prerequisite for vp migrate)
  Edit .mise/config.toml
  Add: "npm:vite-plus" = "latest"
  This installs the vp CLI globally via mise, required before running vp migrate
  Source: ~/projects/typescript-template/.mise/config.toml
```

Second task:

```
Migrate project to Vite+ using vp migrate
  Prerequisite: vite-plus must be in .mise/config.toml
  Run: vp migrate
  This replaces biome/eslint/prettier with oxlint/oxfmt
  After migration: delete biome.json if present (replaced by vp lint / vp fmt)
  After migration: run vp check --fix to verify linting/formatting works
  Source: ~/projects/typescript-template
```

**Pre-commit hook update:**

```
Add vp staged hook to .pre-commit-config.yaml
  Append local repo block after pre-commit-hooks repo:
    - repo: local
      hooks:
          - id: vp-staged
            name: vp staged
            entry: vp staged
            language: system
            types: [file]
  Prerequisite: vite-plus must be installed (vp migrate must be done first)
  Source: ~/projects/typescript-template/.pre-commit-config.yaml
```

**GitHub Actions simplification:**

```
Simplify GitHub Actions CI to use mise-only setup
  Remove explicit setup-node, setup-python, pnpm/action-setup steps
  Replace with jdx/mise-action@v4 (cache: true) + pnpm store cache
  Use just install / just build / just check / just test
  Files: .github/workflows/merge-group.yml, pull-request.yml, push.yml
  Source: ~/projects/typescript-template/.github/workflows/
```

**Justfile update:**

```
Update justfile to use vp commands
  Change pnpm install → vp install
  Add check/lint/format recipes using vp check/lint/fmt
  Add CI env detection: ci := env("CI", "")
  Prerequisite: vite-plus migration must be done first
  Source: ~/projects/typescript-template/justfile
```

**Lint configs sync:**

```
Copy lint configs from template
  Copy .markdownlint.jsonc from template (rule config)
  Copy .markdownlint-cli2.jsonc from template (globs/ignores — tune ignores for this repo's directory layout)
  Copy .yamllint.yaml from template (and tune the ignore: list for tool-local dirs like .serena/)
  Ensure mise.toml includes "npm:markdownlint-cli2" and "pipx:yamllint"
  Ensure .pre-commit-config.yaml has local hooks for markdownlint and yamllint with exclude: regexes matching the config ignores
  Source: ~/projects/typescript-template
```

**All checks aggregator:**

```
Add the All checks aggregator job in merge-group.yml
  In .github/workflows/merge-group.yml, add (or verify) a job named `all-checks` with:
    - name: All checks
    - if: ${{ !cancelled() }}
    - needs: [list of every other job in merge-group.yml]
    - steps: uses re-actors/alls-green@release/v1 with jobs: ${{ toJSON(needs) }}
  Reason: scripts/configure-github.sh sets branch protection to require the literal "All checks" context; the job name must match exactly.
  Source: ~/projects/typescript-template/.github/workflows/merge-group.yml
```

**GitHub configure script:**

```
Copy scripts/configure-github.sh from template
  Copy scripts/configure-github.sh as-is (it auto-detects repo and default branch via gh)
  chmod +x scripts/configure-github.sh
  Pairs with the All checks aggregator above — run after merging workflow changes
  Source: ~/projects/typescript-template/scripts/configure-github.sh
```

## Report Format

After syncing, report:

### This Template Status

- Current versions in this template
- Any updates made

### Improvements Pulled In

- List any newer versions found in siblings

### Tasks Distributed

- Number of siblings that received tasks
- Total tasks created
