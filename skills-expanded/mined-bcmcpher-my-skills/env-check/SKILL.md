---
name: env-check
description: >
  Set up, update, or recreate a local programming language environment for the current
  project: Python virtualenv or uv env, Node/JS/TS with nvm and a package manager,
  Rust with cargo/rustup, Go modules, or R with renv. Use when the user says "set up
  my environment", "check my environment", "create a venv", "install dependencies",
  "recreate the virtualenv", "update packages", or "/env-check". Detects language from
  project files automatically. Does not scaffold project structure or configure Claude
  Code tooling — use /new-project or /claude-config for those.
argument-hint: [language] [--recreate]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Skill: env-check

Validate, set up, update, or recreate the programming language environment for the
current project. Language is detected automatically from project files, or can be
specified explicitly via `$ARGUMENTS`.

---

## Phase 0: Pre-flight checks

### Step 1 — Detect language

If `$ARGUMENTS` names a language explicitly (e.g., "python", "rust", "go"), use it and
skip scanning. Otherwise, search for signal files in the project root:

| Signal files | Language | Reference |
|---|---|---|
| `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile` | Python | `${CLAUDE_PLUGIN_ROOT}/../references/python.md` |
| `package.json` (no `tsconfig.json`) | JavaScript | `${CLAUDE_PLUGIN_ROOT}/../references/javascript.md` |
| `package.json` + `tsconfig.json` | TypeScript | `${CLAUDE_PLUGIN_ROOT}/../references/typescript.md` |
| `Cargo.toml` | Rust | `${CLAUDE_PLUGIN_ROOT}/../references/rust.md` |
| `go.mod` | Go | `${CLAUDE_PLUGIN_ROOT}/../references/go.md` |
| `DESCRIPTION`, `renv.lock`, `.Rprofile` | R | `${CLAUDE_PLUGIN_ROOT}/../references/r.md` |

If multiple signal files match different languages, list what was found and ask the user
which language to proceed with.

If no signal files are found and no language is given in `$ARGUMENTS`, ask the user
which language to use before continuing.

**Load the reference file before taking any language-specific action.**

### Step 2 — Git status check

Load `${CLAUDE_PLUGIN_ROOT}/../references/git.md` before this step.

Run: `git rev-parse --is-inside-work-tree`

**Case A: Not a git repository**

Present:

> "This directory is not tracked by git. Initializing a repository now means your
> lockfiles and project files are preserved from the start — and you won't accidentally
> commit the environment directory.
>
> I can:
> - Run `git init`
> - Create or update `.gitignore` to exclude `<env-dir>/`
>
> Set up git tracking now, or skip and go straight to environment setup?"

- User chooses set up: run `git init`, then create or append to `.gitignore` using the
  entry from `references/git.md` for the detected language. Then continue.
- User skips: note the recommendation but continue without making changes.

**Case B: Is a git repository — `.gitignore` coverage check**

Check whether the env directory is already excluded:

```
git check-ignore -q <env-dir> && echo covered || echo missing
```

- **Already ignored**: proceed silently. No interruption.
- **Not ignored**: offer to add the entry:

  > "`<env-dir>/` is not in `.gitignore`. Without this, the environment directory
  > could be accidentally committed (often hundreds of MB).
  >
  > Add `<env-dir>/` to `.gitignore`? (yes / no)"

  If yes: append to `.gitignore` (or create it). If no: note the gap and continue.

### Step 3 — Secrets / `.env` check

Only run this step if the directory is a git repository (Step 2, Case B) or git init was
just performed (Case A, user chose yes).

Check whether `.env` exists:

**`.env` exists:**

```bash
git check-ignore -q .env && echo covered || echo missing
```

- **Covered** → proceed silently. No interruption.
- **Not covered** → warn and offer:

  > "`.env` exists but is not in `.gitignore`. This file may contain secrets that
  > could be accidentally committed.
  >
  > Add `.env` to `.gitignore`? (yes / no)"

  If yes: append `.env` to `.gitignore` (or create it). If no: note the gap and
  continue.

**`.env` does not exist:**

Check for `.env.example`:

- **Neither exists:**

  > "No `.env` or `.env.example` found. Most projects need environment variables for
  > local config (API keys, database URLs, etc.).
  >
  > I can create an empty `.env.example` as a template and add `.env` to `.gitignore`.
  > Set up the secrets pattern now, or skip?"

  - Yes: create `.env.example` with a comment header (`# Environment variables — copy
    to .env and fill in values`), append `.env` to `.gitignore`.
  - Skip: continue without changes.

- **`.env.example` exists but `.env` is not ignored:**

  > "`.env.example` exists. Adding `.env` to `.gitignore` to complete the pattern."

  Append `.env` to `.gitignore` and continue (no prompt needed — this is a clear fix).

- **`.env.example` exists and `.env` is already ignored:** proceed silently.

---

### Step 3b — Check for already-active Python venv

Before creating a new Python environment, check the `$VIRTUAL_ENV` environment variable:

```bash
echo "$VIRTUAL_ENV"
```

If `$VIRTUAL_ENV` is set and non-empty, the user is already inside an active venv. Ask:

> "You are currently inside an active Python venv at `$VIRTUAL_ENV`. Create a new
> environment anyway, or use the existing one?"

Wait for the user's answer before proceeding.

### Step 4 — Check for existing environment

Each language reference defines the environment indicator directory (`.venv/`,
`node_modules/`, `target/`, `go.sum`, `renv/`). Check for it now.

- **Not found** → proceed to Phase 1.
- **Found, no `--recreate` in `$ARGUMENTS`** → ask the user:

  > "An existing environment was found at `<path>`. What would you like to do?
  >
  > 1. Update — run the install/sync command to add or upgrade packages
  > 2. Leave as-is — stop here, no changes
  > 3. Recreate — delete and rebuild from scratch"

  Wait for the user's choice before continuing. If they choose "leave as-is", skip to
  Phase 4 (document the current environment state in CLAUDE.md) and then stop.

- **Found + `--recreate` in `$ARGUMENTS`** → skip the prompt and go directly to the
  warning below, then delete and recreate.

---

## Existing environment warning (update or recreate only)

Before doing anything destructive, present this warning and require explicit
confirmation:

> "**Warning:** Modifying or recreating an existing environment may break installed
> packages, change interpreter versions, or invalidate lockfiles. Proceed only if you
> are intentionally rebuilding or standardizing the environment.
>
> Type **yes** or **proceed** to continue, or anything else to cancel."

If the user does not confirm, stop. For a clean create (no existing env detected), skip
this warning entirely.

---

## Phase 1: Conda check (Python only)

Before creating any Python environment, check all three signals:

1. `which conda` exits 0
2. `environment.yml` exists in the project root
3. `$ARGUMENTS` contains "conda" or "anaconda"

If **any** signal is true, present this choice and wait for the user's response:

> "A conda installation (or `environment.yml`) was detected. Conda environments must be
> activated before Claude Code launches — `conda activate` modifies shell state that
> subprocesses cannot inherit from a running session.
>
> Options:
> 1. **Use conda manually** — I'll document the setup in CLAUDE.md so future sessions
>    have context. You activate the environment before launching Claude Code.
> 2. **Use venv instead** — I'll set up a standard `.venv` (or `uv` env) right now."

- User picks conda: write the conda environment details to CLAUDE.md `## Active
  Environment` section (environment name, `conda activate <name>` command, Python
  version if determinable from `environment.yml`). Note the manual activation
  requirement. Skip Phases 2 and 3 and go directly to Phase 4.
- User picks venv / uv: continue to Phase 2. If `uv` is on PATH (`which uv` exits 0),
  prefer `uv venv` + `uv pip install` over plain venv.

If no conda signals are present, skip this phase entirely.

---

## Phase 2: Create / update environment

Follow the steps in the loaded reference file exactly: tool selection, commands, lockfile
handling, and any language-specific flags.

**Permission-blocked commands:** If a Bash command is blocked by Claude Code's permission
system, do not retry or suggest workarounds. Instead, surface the exact command:

> "The following command needs to be run manually:
>
> ```
> <exact command>
> ```
>
> Please run it in your terminal, then reply **done** to continue."

Wait for the user to confirm before proceeding to the next step.

---

## Phase 3: Verify

Run the verification command from the reference file (e.g., `which python`,
`node --version`, `cargo --version`, `go version`, `Rscript --version`).

Confirm that the interpreter or toolchain resolves **inside the new environment**, not
to a system installation. If the path points to a system binary instead of the project
environment, report the discrepancy and ask the user how to proceed — do not declare
success.

---

## Phase 4: Document in CLAUDE.md

Check for `CLAUDE.md` in the project root. Write or update a fixed
`## Active Environment` section with this exact format:

```markdown
## Active Environment

- Language: <language>
- Environment: <path>
- Interpreter: <full path from which/where>
- Version: <version string>
- Package manager: <pip/uv/npm/yarn/pnpm/cargo/go/renv>
- Activate: <activate command>
- Last setup: <YYYY-MM-DD>
```

For conda environments where venv was not created, use:

```markdown
## Active Environment

- Language: Python (conda)
- Environment: <conda env name>
- Activate: conda activate <env-name>
- Note: activate manually before launching Claude Code
- Last setup: <YYYY-MM-DD>
```

Rules:

- **No file** → create a minimal `CLAUDE.md` containing only this section. Do not invent
  project instructions or add any other content.
- **File exists, no `## Active Environment` section** → append the section at the end of
  the file.
- **File exists, section already present** → replace the content from the
  `## Active Environment` heading through the next `##` heading (or EOF) with the updated
  section.

---

## Closing

After writing CLAUDE.md, confirm what was set up (env path, interpreter version). Then:

> "Environment documented. To configure Claude Code tooling for this project (LSP, hooks,
> MCP servers, agents), run `/claude-config`."

---

## Constraints

- Never delete an existing environment without explicit user confirmation.
- Never skip the conda check when any conda signal is present (Python only).
- If a Bash command is blocked by Claude Code's permission system, surface the exact
  command and wait for "done" — do not retry or silently skip.
- For R projects using `renv`, the standard workflow is:
  - New project: run `renv::init()` to create `renv.lock` and `.Rprofile`
  - After installing packages: run `renv::snapshot()` to update the lockfile
  - On a fresh clone or to restore: run `renv::restore()` to install from lockfile
  Always load the R language reference before advising on `renv` — do not invent `renv` commands from memory.
- Do not modify project source files, `pyproject.toml`, `package.json`, or any other
  project config. Only `CLAUDE.md` may be written or updated.
- Always verify with the interpreter path check before declaring success.
- Always load the language reference file before taking any language-specific action.
- The existing-environment warning is mandatory for any update or recreate action —
  never skip it.
