---
name: new-project
description: >
  Scaffold a new project for use with Claude Code. Guides through project type selection
  (coding-tool, data-analysis, or info-management), creates the directory structure and
  essential files, initializes git, sets up the programming environment, and configures
  Claude Code tooling — all in a single guided workflow. Use when the user says "start
  a new project", "create a new project", "scaffold a project", "initialize a project",
  or "/new-project". Takes an optional project type and name as arguments.
argument-hint: [coding-tool|data-analysis|info-management] [project-name]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Skill: new-project

Scaffold a complete new project for use with Claude Code. Covers structure, environment,
and Claude tooling in one guided workflow.

---

## Phase 0: Project identity

### Step 1 — Parse arguments

Scan `$ARGUMENTS` for a recognized type keyword:

| Keywords | Type |
|---|---|
| "coding-tool", "package", "library", "cli", "tool", "service" | `coding-tool` |
| "data-analysis", "data", "analysis", "research", "science", "notebook" | `data-analysis` |
| "info-management", "info", "notes", "knowledge", "vault", "research-aggregation" | `info-management` |

If a second token exists and matches neither keyword list, treat it as the project name.

### Step 2 — Ask for what is still unknown

**If project type is unknown**, present:

> "What kind of project are you starting?
>
> 1. **Coding tool / package** — a library, CLI, or service; built for programmatic
>    use and potentially external contributors
> 2. **Data analysis** — reproducible research producing models, figures, and reports
>    for distribution
> 3. **Information management** — structured knowledge collection: research aggregation,
>    note-taking, or executive-assistant-style work
>
> Reply with a number or a type name."

Wait for the user's choice.

**If project name is unknown**, ask:

> "What is the project name? (kebab-case, used for the directory and package name)"

Optionally ask for a one-line description (used in README and package manifest stubs).

**For `coding-tool` projects**, also ask:

> "What license? (default: MIT — other common choices: Apache-2.0, GPL-3.0, BSD-2-Clause, or 'proprietary' to skip)"

Default to MIT if the user does not answer. Store the choice for use in Phase 2 when
writing the LICENSE file.

### Step 3 — Load project type reference

| Type | Reference |
|---|---|
| `coding-tool` | `${CLAUDE_PLUGIN_ROOT}/../references/project-types/coding-tool.md` |
| `data-analysis` | `${CLAUDE_PLUGIN_ROOT}/../references/project-types/data-analysis.md` |
| `info-management` | `${CLAUDE_PLUGIN_ROOT}/../references/project-types/info-management.md` |

**Load this reference before proceeding.** All scaffold content, CLAUDE.md templates,
and configuration recommendations come from it.

---

## Phase 1: Directory check

Check whether `<project-name>/` exists in the current working directory.

- **Does not exist** → proceed.
- **Exists and is empty** → proceed (files will be created inside it).
- **Exists and is non-empty** → warn:

  > "`<project-name>/` already exists and is not empty. Continuing will add scaffold
  > files but will not overwrite anything that already exists.
  >
  > Proceed, or cancel?"

  Wait for confirmation. If cancelled, stop.

---

## Phase 2: Scaffold structure

Create the directory tree and stub files defined in the reference's **Directory
scaffold** and **Essential files** sections.

Rules:

- Create directories with `mkdir -p`.
- For each stub file: check whether it already exists before writing. If it exists,
  skip it and note that it was preserved.
- Substitute `<project-name>` and `<description>` throughout stub content.
- Do not create any file not listed in the reference's scaffold spec.

After scaffolding, briefly list the directories and files created.

---

## Phase 3: Git and secrets hygiene

Load `${CLAUDE_PLUGIN_ROOT}/../references/git.md`.

Run `git rev-parse --is-inside-work-tree` from within `<project-name>/`.

**Not already a git repository** (expected for new projects):

- Run `git init` inside the project directory.
- Write `.gitignore` using the language entries from `references/git.md`, the
  **Claude Code local files** entries from `references/git.md`, plus any
  project-type-specific entries from the loaded reference's **.gitignore additions**
  section.
- Inform the user: "Git initialized."

**Already inside a git repository** (nested — less common for new projects):

- Run the `.gitignore` coverage check from `references/git.md` for the env directory.
- Offer to add missing entries.

**Secrets check (both cases):**

Follow the `.env` check from `references/git.md`. For new projects neither `.env` nor
`.env.example` will exist — offer to create the pattern unless the project type
reference explicitly advises against it (info-management projects often don't need it).

---

## Phase 4: Environment setup

*Skip this phase for `info-management` projects — they have no programming environment.
Proceed directly to Phase 5.*

Follow `${CLAUDE_PLUGIN_ROOT}/../skills/env-check/SKILL.md` **Phases 1–3**, with these
adjustments for the new-project context:

- **Skip env-check Phase 0 Steps 2–4** (git status, `.gitignore` coverage, and `.env`
  check) — Phase 3 of new-project already handled all of these.
- **Skip the existing-environment check** in env-check Phase 0 Step 4 — this is a new
  project with no prior environment.
- Use the manifest file written in Phase 2 as the language signal (no need to re-scan):

  | Manifest created | Language |
  |---|---|
  | `pyproject.toml` | Python |
  | `package.json` (no `tsconfig.json`) | JavaScript |
  | `package.json` + `tsconfig.json` | TypeScript |
  | `Cargo.toml` | Rust |
  | `go.mod` | Go |
  | `renv.lock` / `DESCRIPTION` | R |

  If no manifest was created, ask the user which language to use before continuing.

All conda detection, uv preference, environment creation, verification, and
CLAUDE.md documentation logic is defined in env-check — follow it exactly.

---

## Phase 5: Document in CLAUDE.md

The project type reference includes a **CLAUDE.md template** section. Write this
template to `<project-name>/CLAUDE.md`.

Rules:

- If CLAUDE.md was already created by Phase 2 scaffolding (some project types include
  it), append or merge — do not overwrite.
- Substitute `<project-name>`, `<description>`, `<language>`, and environment details
  from Phase 4 throughout the template.
- After writing the template, also write or update the `## Active Environment` section
  (format defined in `${CLAUDE_PLUGIN_ROOT}/../skills/env-check/SKILL.md` Phase 4).
  For info-management projects, use:

  ```markdown
  ## Active Environment

  - Language: none (knowledge management project)
  - Last setup: <YYYY-MM-DD>
  ```

---

## Phase 6: Claude Code configuration

Load `${CLAUDE_PLUGIN_ROOT}/../skills/claude-config/SKILL.md` and execute its full
workflow with these adjustments:

- **Skip Phase 0 Steps 1–3** (project type detection, reference loading, language
  detection) — these are already established. Use the type and language from Phase 0
  and Phase 4 of this skill directly.
- Start at **Phase 1: Configuration menu**, presenting the full 11-option menu with the
  known project type highlighted in the profile line.

The user receives the full interactive configuration menu without re-answering questions
already answered during this workflow.

The user will receive the full menu of configuration options (CLAUDE.md refinement, LSP,
hooks, MCP servers, agents, local skills, `.editorconfig`) without needing to invoke
`/claude-config` separately.

---

## Phase 7: Closing summary

Print a structured summary of everything completed:

```
## Project initialized: <project-name>

**Type:** <type>
**Language:** <language or "none">
**Location:** <absolute path to project directory>

### Created
- [list of directories and files written in Phase 2]
- .gitignore (Phase 3)
- CLAUDE.md (Phase 5)
- [any Claude Code config files written in Phase 6]

### Claude Code configuration
- [list of options selected in Phase 6, or "none selected"]

### Next steps
1. `cd <project-name>`
2. Fill in all `<placeholder>` fields in CLAUDE.md and any stub files
3. `git add . && git commit -m "Initial commit"` to record the starting state
4. Run `/claude-md-audit` once placeholders are filled to verify quality
```

If the user cancelled during Phase 6 (chose "none"), omit the Claude Code configuration
section and note: "Claude Code tooling not configured — run `/claude-config` at any
time to add it."

---

## Constraints

- Never overwrite a file that already exists during scaffolding — skip and note it.
- Never skip the conda check when any conda signal is present (Python only) — this is
  enforced by env-check; do not bypass it.
- Do not create files outside `<project-name>/` unless the user explicitly requests it.
- If a Bash command is blocked, surface the exact command and wait for "done" — do not
  retry or silently skip.
- The CLAUDE.md template from the project type reference is the authoritative content
  for Phase 5 — do not invent project-specific instructions beyond what the template
  specifies.
- Always verify the environment before declaring Phase 4 complete.
