---
name: project-new
description: "Scaffolds an empty directory into a runnable local project with a Makefile, pre-commit, CLAUDE.md and first commit. Use when starting a Python, TypeScript or Terraform project from nothing. Not for existing code (use /init, then agent-craft:config-audit); not for an experiment (use poc-start)."
when_to_use: "start a new project, scaffold an empty directory, new repo from scratch, project skeleton, bootstrap a new service"
argument-hint: "[project-name]"
allowed-tools: Read, Glob, Edit(./**), Bash(pwd), Bash(git init *), Bash(git init), Bash(git add *), Bash(git commit *), Bash(git status *), Bash(git branch --show-current), Bash(uv init *), Bash(uv add *), Bash(npm init *), Bash(npm install *), Bash(make *), Bash(pre-commit *), AskUserQuestion
license: MIT
---

# Scaffold a New Project Locally

Turns an empty directory into a project where `make verify` passes and one commit holds it
all. Everything stays local: no remote, no push, no branch protection, no pull request. Forge
work belongs to `github-workflow` or `gitlab-workflow`.

Project name from the invocation: `$ARGUMENTS` (empty → default to the directory name).

**Toolchain stance.** Python uses `uv`; TypeScript uses `npm`. These are the only managers this
skill scaffolds, so the commands below are exact. If the user wants another (Poetry, pnpm, …),
say that this skill writes uv/npm and let them choose to proceed or scaffold by hand.

**Without a checkout (web/Cowork):** this skill needs a shell and a filesystem. There, draft the
files in chat for the user to create, and say that nothing was run or committed.

## Step 1 — Check the directory is empty

Run `pwd`, then Glob `**/*` (every file at any depth, dotfiles included) and Glob `.git/HEAD`.
Glob returns files, not directories, so judge by the files it lists.

- **No files outside `.git/`, or only stray dotfiles such as `.DS_Store`** → continue. Note
  whether `.git/HEAD` was found: that means a repository already exists.
- **Has real files** → stop. This skill writes a Makefile, README and `.gitignore` and would
  overwrite someone's work. Point the user to `/init` (generates CLAUDE.md from existing code)
  and `agent-craft:config-audit` (audits existing Claude config), and end.

## Step 2 — Ask what is being built

One `AskUserQuestion` call with three questions, the defaults shown in the text:

1. **Type:** Python service or library / TypeScript application / Terraform only / application
   plus Terraform (then ask Python or TypeScript).
2. **Name:** the argument or directory name. Repository and npm name in kebab-case; Python
   import name in snake_case.
3. **Local runtime:** none / a container compose file under `infrastructure/local/`.

Write nothing until all three are answered.

## Step 3 — Create the manifest and a smoke test

The manifest is what makes `make install` and `make test` real. The smoke test exists only so
the test runner has something to collect (pytest and vitest both fail on zero tests); it is not
application code, so write nothing beyond it.

**Python:**

```bash
uv init --lib --vcs none --no-readme --name <name>
uv add --dev pytest ruff mypy
```

`uv init --lib` writes `pyproject.toml` and `src/<package>/__init__.py`; `--vcs none` stops it
creating a repository (Step 8 owns git). Then write `tests/test_smoke.py`:

```python
import <package>


def test_package_imports() -> None:
    assert <package>.__name__ == "<package>"
```

**TypeScript:**

```bash
npm init -y
npm install --save-dev typescript vitest prettier @types/node
```

Set `"name"`, `"type": "module"` and these scripts in `package.json`:
`"build": "tsc -p tsconfig.build.json"`, `"typecheck": "tsc --noEmit"`, `"test": "vitest run"`,
`"lint": "prettier --check src tests"`, `"format": "prettier --write src tests"`. Prettier is
scoped to source because pre-commit's `pretty-format-json` owns JSON layout and the two disagree
on short arrays; checking `.` also fails on the pre-commit config itself.

Write two plain-JSON configs (no comments, so pre-commit's `check-json` accepts them):

- `tsconfig.json`, for typechecking source and tests: `strict: true`, `module` and
  `moduleResolution` `"NodeNext"`, `noEmit: true`, `include: ["src", "tests"]`.
- `tsconfig.build.json`, for the build: `"extends": "./tsconfig.json"`, `noEmit: false`,
  `rootDir: "src"`, `outDir: "dist"`, `include: ["src"]`.

Then an empty `src/index.ts` export (`export {};`) and `tests/smoke.test.ts`:

```ts
import { expect, test } from "vitest";

test("toolchain runs", () => {
  expect(true).toBe(true);
});
```

**Terraform:** `infrastructure/terraform/versions.tf` containing an empty `terraform {}` block
(so `validate` has a root module), and an empty `infrastructure/terraform/environments/dev.tfvars`.
Environment `.tfvars` files are tracked and hold no secrets.

## Step 4 — Write the Makefile

Recipe lines are indented with a tab. Target names are the same across stacks; `verify` is the
one command that must pass before a change is done, and what CI should run later.

Python:

```makefile
.PHONY: install test lint format typecheck verify
install:
	uv sync
test:
	uv run pytest
lint:
	uv run ruff check .
format:
	uv run ruff format .
typecheck:
	uv run mypy src tests
verify: lint typecheck test
```

TypeScript:

```makefile
.PHONY: install build test lint format typecheck verify
install:
	npm ci
build:
	npm run build
test:
	npm test
lint:
	npm run lint
format:
	npm run format
typecheck:
	npm run typecheck
verify: lint typecheck test build
```

Terraform, with one explicit target per environment so a wrong default cannot point at
production:

```makefile
TF := terraform -chdir=infrastructure/terraform
.PHONY: install fmt validate verify plan-dev apply-dev
install:
	$(TF) init -backend=false -input=false
fmt:
	$(TF) fmt -check -recursive
validate:
	$(TF) init -backend=false -input=false
	$(TF) validate
verify: fmt validate
plan-dev:
	$(TF) plan -var-file=environments/dev.tfvars
apply-dev:
	$(TF) apply -var-file=environments/dev.tfvars
```

Combined projects keep the application Makefile and add to it: the `TF :=` line, the `fmt`,
`validate`, `plan-dev` and `apply-dev` targets (and their `.PHONY` names), and `fmt validate` at
the end of `verify`'s prerequisites. The application's `install` stays; `validate` runs its own
`init`.

## Step 5 — Write CLAUDE.md and rules

Read `${CLAUDE_PLUGIN_ROOT}/templates/claude-md/root.md`, fill every `${…}` from the answers and
the Makefile, and write `./CLAUDE.md`. In the Commands block, list only targets the Makefile
defines: Terraform-only has no `test` or `lint`, so list `install`, `fmt`, `validate`,
`plan-dev` and `verify` instead. `${ADR_SECTION}`: delete it and the comment under it (a new
project has no `docs/adr/`; `adr-init` adds that section later). Anything you cannot fill stays
as `TODO: confirm <what>`.

If Terraform was chosen, fill `${CLAUDE_PLUGIN_ROOT}/templates/claude-md/infra.md` and write it
to `.claude/rules/infrastructure.md`. Its `paths:` frontmatter loads it only when Claude works on
infrastructure files. Writes under `.claude/` always prompt for approval; that is expected.

## Step 6 — Write the README and .gitignore

README, for a human arriving cold:

```markdown
# <name>

TODO: confirm a one-sentence description.

## Quick start

    make install
    make verify

Conventions for contributors and Claude live in [CLAUDE.md](./CLAUDE.md).
```

`.gitignore`, grouped with a comment per group, environment group first:

- **Environment and personal:** `.env`, `.env.*`, `CLAUDE.local.md`, `.claude/settings.local.json`.
- **Python:** `__pycache__/`, `*.py[cod]`, `.venv/`, `.mypy_cache/`, `.pytest_cache/`,
  `.ruff_cache/`, `dist/`, `*.egg-info/`.
- **Node:** `node_modules/`, `dist/`, `coverage/`.
- **Terraform:** `.terraform/`, `*.tfstate`, `*.tfstate.*`, `crash.log`. Keep
  `.terraform.lock.hcl` tracked: it pins provider hashes.
- **Editor and OS:** `.idea/`, `.vscode/`, `.DS_Store`.

Lock files (`uv.lock`, `package-lock.json`) stay tracked; they make `make install` reproducible.

Every version the scaffold writes (dependencies, dev tools, the runtime pin, a base image, an
Action) follows `dev-standards:dependency-versions`: looked up from the registry at write time,
anchored to its major, exact only in the lockfile. Load that skill with the Skill tool before
writing the manifests; without it, run the lookups it names yourself rather than typing a version
from memory.

## Step 7 — Add pre-commit

Load `dev-standards:precommit-standards` with the Skill tool and follow its "The baseline
template" section: it owns the baseline `.pre-commit-config.yaml` (shipped in the dev-standards
plugin), the pinning rules and the stack sections. Enable the sections for the chosen stack only.
If that skill is not installed, write no config and list "add pre-commit" as a next step.

Adjust the baseline to this skeleton, leaving a one-line reason in a comment each time:

- **Python:** enable the `[PYTHON]` section as shipped.
- **TypeScript:** leave `[NODEJS]` commented out; its hooks call eslint and jest, which this
  skeleton does not install. Add one pre-push hook that runs the project's own contract:

  ```yaml
  - repo: local
    hooks:
      - id: make-verify
        name: make verify (pre-push)
        entry: make verify
        language: system
        pass_filenames: false
        stages: [pre-push]
  ```

- **Terraform:** enable `[TERRAFORM]`, but comment out `terraform_docs` unless the
  `terraform-docs` binary is on PATH; without it the hook fails every run.

## Step 8 — Initialise git, run the hooks, commit

Run `git init` only if Step 1 found no `.git/HEAD`; an existing repository is kept as is. Then:

```bash
pre-commit install
git add -A
pre-commit run --all-files
```

The first run usually reformats files. Stage the fixes (`git add -A`) and re-run until it
passes, then commit:

```bash
git commit -m "chore: scaffold project skeleton"
git branch --show-current
```

If `pre-commit` is not on PATH, commit without it and report the install command. Do not rename
the default branch; report its name.

## Step 9 — Verify

```bash
make install
make verify
git status --short
```

`make verify` must pass and `git status` must be clean (Step 3 already created the lock file, so
`make install` should change nothing). If a check fails, fix the file, re-run, and commit the fix
as a follow-up `fix:` commit; report success only on a green `verify`.

## Step 10 — Report

- Every file written, one line each.
- Every `TODO: confirm` left.
- Pre-commit: installed and passing, or skipped and why.
- Default branch name and commit subjects.
- Next steps: fill the TODOs; run `/project-scaffold:adr-init` once real decisions exist; create
  the remote yourself (then `github-workflow` or `gitlab-workflow`); add CI that runs `make verify`.
