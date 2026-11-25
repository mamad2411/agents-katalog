---
name: init-python-project
description: Initialize or enhance a Python/ML project. Use for new repos or forks needing production structure, uv environment setup, and research evidence docs.
argument-hint: (interactive — no arguments needed, the skill asks questions)
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Initialize Python Project

Help the user create a production-ready Python project or upgrade an existing one without inlining large file bodies inside this skill. Use the bundled references and templates as the source of truth. Treat the Python toolchain as an explicit gate: default to non-mutating checks, run format/fix commands only when requested or required, and record the actual commands in repo guidance. Use `pre-commit` as the optional local gate runner for code, shell, secrets, notebooks, configs, GitHub Actions, and docs links.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── architecture.md
│   ├── new-project.md
│   ├── fork-enhancement.md
│   └── best-practices.md
├── scripts/
│   └── scaffold_new_project.py
├── template_manifest.json
└── templates/
    ├── common/
    │   ├── .gitignore
    │   ├── .env.example
    │   ├── README.md
    │   ├── AGENTS.md
    │   ├── CLAUDE.md
    │   ├── pyproject.toml.tmpl
    │   ├── tests/
    │   └── docs/
    └── ml/
        ├── .agent/
        ├── docs/
        ├── experiments/
        ├── infra/
        ├── eval/
        └── scripts/
```

## Progressive Loading

Read only the references needed for the current path:

- Always read `references/architecture.md`
- For new projects, read `references/new-project.md`
- For fork/enhancement work, read `references/fork-enhancement.md`
- If you need policy, tradeoff, or failure-handling guidance, read `references/best-practices.md`

Use `templates/` as the source of truth for file contents instead of reproducing long inline snippets.
Use `template_manifest.json` as the source of truth for which template groups and placeholders the scaffold supports.

## Step 1 — Gather Project Information

Ask the user in a single message:

1. Project type:
   - `new` — create a new project
   - `fork` — clone and enhance an existing repository
2. If `new`:
   - Project name
   - Package name (default: snake_case of project name)
   - Short description
   - Python version (default: `3.11`)
   - Project type: `ml`, `web`, `lib`, or `general`
3. If `fork`:
   - GitHub repository URL
   - Whether they want a fork workflow or just a local enhancement
4. For both:
   - GitHub repository URL for the target repo, if available
   - Author name and email
   - Existing toolchain policy, if any: `ruff`, `black`, `isort`, `mypy`, `pyright`, `pytest`, `pre-commit`, `gitleaks`, `shellcheck`, `shfmt`, `actionlint`, `nbstripout`, CI, or custom commands

Wait for the answer before continuing.

## Step 2 — Choose the Execution Path

### Path A: New Project

Read `references/new-project.md` and `references/architecture.md`.

#### 2A.1 Create the project root

```bash
mkdir <project-name>
cd <project-name>
uv init --name <package_name> --python <version>
```

If the directory already exists, stop and ask whether to choose a new name or reuse it.

#### 2A.2 Preferred path for `new + ml`

For a new ML project, prefer the bundled scaffold script:

```bash
python3 <installed-skill-dir>/scripts/scaffold_new_project.py \
  <target-dir> \
  --project-name <project-name> \
  --package-name <package-name> \
  --description "<short-description>" \
  --python-version <version> \
  --author-name "<author-name>" \
  --author-email "<author-email>" \
  --repo-url "<repo-url-or-TBD>"
```

The script handles:

- `uv init`
- source/test/docs directory creation
- copying templates from `templates/common/` and `templates/ml/`
- placeholder replacement
- creating `.env`
- bootstrapping remote-project memory files for local-to-remote workflows
- writing `.gitkeep` files

After it completes, continue with install, verification, and git setup in Steps 2A.6 and 2A.7.

If the user wants a non-ML layout or the script is not suitable, fall back to the manual path below.

#### 2A.3 Manual fallback: create the directory layout

For `ml` projects, create the full four-layer structure from `references/architecture.md`.

At minimum, create:

```bash
mkdir -p src/<package_name>/{models,data,utils}
mkdir -p tests/{data,outputs}
mkdir -p docs/outlines docs/dev/features docs/src docs/results docs/reports docs/runs
mkdir -p .vscode .cursor .claude/commands
touch src/<package_name>/__init__.py
touch src/<package_name>/models/__init__.py
touch src/<package_name>/data/__init__.py
touch src/<package_name>/utils/__init__.py
touch tests/__init__.py
```

For non-ML projects, keep the common project files but only create ML-specific directories if the user explicitly wants them.

#### 2A.4 Materialize templates

Use the templates under `templates/` and replace placeholders:

- `{{PROJECT_NAME}}`
- `{{PACKAGE_NAME}}`
- `{{DESCRIPTION}}`
- `{{PYTHON_VERSION}}`
- `{{AUTHOR_NAME}}`
- `{{AUTHOR_EMAIL}}`
- `{{REPO_URL}}`

Write these common files from `templates/common/`:

- `.gitignore`
- `.env.example`
- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.pre-commit-config.yaml`
- `pyproject.toml`
- `tests/conftest.py`
- `docs/outlines/project_plan.md`
- `docs/outlines/progress.md`
- `docs/results/.gitkeep`
- `docs/reports/.gitkeep`
- `docs/runs/.gitkeep`
- `docs/dev/feature_template.md`
- `docs/src/dependencies.md`
- `.vscode/settings.json`

For `ml` projects, also write:

- `experiments/config.py`
- `experiments/configs/base.yaml`
- `infra/envs/local.yaml`
- `infra/envs/cluster.yaml.example`
- `infra/remote-projects.yaml`
- `infra/README.md`
- `docs/ops/current-status.md`
- `docs/ops/decision-log.md`
- `.agent/local-overrides.yaml`
- `eval/baselines/README.md`
- `scripts/train.py`
- `scripts/download_data.py`

Create `.env` as an empty file with a short comment header if it does not exist.

#### 2A.5 Add placeholder files for empty directories

Use `.gitkeep` where needed so empty directories are tracked:

```bash
touch experiments/configs/.gitkeep
touch eval/benchmarks/.gitkeep
touch eval/baselines/reproduced/.gitkeep
touch infra/submit/slurm/.gitkeep
touch docs/results/.gitkeep
touch docs/reports/.gitkeep
touch docs/runs/.gitkeep
touch tests/data/.gitkeep
touch tests/outputs/.gitkeep
```

Only create placeholders for directories that actually exist in the chosen project type.

#### 2A.6 Install and verify toolchain gates

If this code repo is part of a project-control-root layout (`<ProjectName>/code/` with sibling `<ProjectName>/code-worktrees/`), use a shared project-code uv environment before running any `uv sync` or `uv run` command:

```bash
export UV_PROJECT_ENVIRONMENT=<absolute-project-root>/.uv-envs/code
```

Do not use a relative `UV_PROJECT_ENVIRONMENT` for this policy; uv resolves relative values against each active workspace root, so different worktrees can still fork into different environments. Run Python entry points through `uv run` from the active worktree rather than directly invoking the shared env's `bin/python`. Use a separate stage env only when dependencies, Python/CUDA stack, destructive package tests, or real concurrent sync risk requires it, and record that exception in worktree or project guidance.

For ML projects:

```bash
uv sync
uv pip install -e ".[dev,ml]"
```

For non-ML projects:

```bash
uv sync
uv pip install -e ".[dev]"
```

Run the default non-mutating gates. Omit paths that do not exist in the chosen project type:

```bash
uv run ruff format --check src tests experiments scripts
uv run ruff check src tests experiments scripts
uv run mypy src
uv run pytest tests -v
uv run pre-commit run --all-files
```

If there are no tests yet, create a placeholder test and rerun:

```bash
cat > tests/test_placeholder.py <<'EOF'
def test_placeholder():
    assert True
EOF
uv run pytest tests/
```

Do not run `uv run ruff format ...`, `uv run ruff check --fix ...`, `shfmt -w`, `nbstripout` without `--dry-run`, or other mutating fix commands silently. Use mutating commands only when the user requests formatting/fixes or a documented project policy requires them, then review the diff.

#### 2A.7 Initialize git and optional remote

```bash
git rev-parse --git-dir >/dev/null 2>&1 || git init
git add .
git commit -m "Initial Python project structure"
```

If the user provided a GitHub URL, add `origin`, show `git remote -v`, and ask before pushing:

```bash
git remote add origin <github-ssh-url>
CURRENT_BRANCH="$(git branch --show-current)"
project-push --set-upstream . origin "$CURRENT_BRANCH"
```

### Path B: Fork / Existing Project

Read `references/fork-enhancement.md`, `references/architecture.md`, and `references/best-practices.md`.

#### 2B.1 Clone and inspect

```bash
git clone <github-ssh-url> <project-name>
cd <project-name>
ls -la
```

Check for:

- `pyproject.toml`, `setup.py`, `requirements.txt`
- `src/`, `tests/`, `docs/`, `scripts/`
- `.env.example`, `AGENTS.md`, `CLAUDE.md`, `.vscode/settings.json`

#### 2B.2 Report gaps before bulk edits

Produce a concise report showing:

- Existing structure
- Missing high-value components
- Whether the repo is already installable
- Which toolchain gates already exist
- Whether docs/test isolation are missing

Then ask whether to:

1. Add all missing components
2. Add only selected components
3. Generate a checklist without editing

#### 2B.3 Add only missing components

When the user approves edits, use the templates under `templates/common/` to fill gaps:

- `.env.example`
- `AGENTS.md`
- `CLAUDE.md`
- `.pre-commit-config.yaml`
- `tests/conftest.py`
- docs templates
- `.vscode/settings.json`
- `pyproject.toml` if migrating from `requirements.txt`

Do not force the full ML layout onto an existing repo unless the user explicitly wants that migration.
Preserve an existing healthy toolchain. Do not replace `black`, `isort`, `pyright`, `pre-commit`, `gitleaks`, `shellcheck`, `shfmt`, `actionlint`, `nbstripout`, or CI commands just because the new scaffold defaults to `ruff`, `mypy`, `pytest`, and local `pre-commit` hooks.

## Template Application Rules

- Keep existing substantial files when they are already good enough.
- Prefer surgical edits over overwriting.
- For templated files, replace placeholders consistently.
- If a template is only partially relevant, copy the relevant sections instead of dumping the whole file verbatim.

## Final Summary

Report:

```text
✓ Python project initialized or enhanced: <project-name>
✓ Project type: <new|fork> / <ml|web|lib|general>
✓ Common scaffolding applied
✓ UV environment configured
✓ Toolchain gates configured: format / lint / type-check / test / secrets / shell / notebooks / configs / docs links
✓ Git status: initialized / existing repo reused
✓ Remote: <configured or skipped>

Project location: <full-path>

Next steps:
1. cd <project-name>
2. cp .env.example .env
3. Fill in project-specific settings
4. Start implementing in src/<package_name>/
5. Put stable experiment summaries in docs/results/, reports in docs/reports/, and run pointers in docs/runs/
6. Run the toolchain gates before the next commit:
   `uv run ruff format --check src tests experiments scripts`
   `uv run ruff check src tests experiments scripts`
   `uv run mypy src`
   `uv run pytest tests -v`
   `uv run pre-commit run --all-files`
```

## Important Notes

- Use `references/best-practices.md` when you hit edge cases.
- Keep this `SKILL.md` focused on orchestration; the detailed file content should live in `templates/` and `references/`.
- `experiments/` is runnable experiment logic, not a result archive. Raw outputs, checkpoints, logs, and wandb/tensorboard caches should stay in ignored paths or external storage, with small pointers in `docs/runs/`.
- When this code repo belongs to a project control root, prefer sibling code worktrees under `<ProjectName>/code-worktrees/` instead of nested worktrees inside `code/`.
- For routine final branch pushes after preflight, use `project-push <repo> <remote> <branch>` rather than raw `git push`, `git -C <repo> push`, `cd <repo> && git push`, or shell-wrapped push variants.
- When this code repo belongs to a project control root, record toolchain gate commands in root `memory/project.yaml` and component guidance. Gate status is stale unless verified in the current branch/worktree.
