---
name: config-export
description: >
  Exports the project's Claude configuration (CLAUDE.md + ai-context/) to
  tool-specific instruction files for GitHub Copilot, Google Gemini, and Cursor.
  Trigger: /config-export, export config, copilot instructions, gemini config, cursor rules.
format: procedural
---

# config-export

> Exports CLAUDE.md and ai-context/ to tool-native instruction files for GitHub Copilot, Google Gemini, and Cursor.

**Triggers**: `/config-export`, export config, copilot instructions, gemini config, cursor rules

---

## Purpose

`config-export` reads the project's Claude configuration (`CLAUDE.md` and any present `ai-context/` files) into an in-context bundle, lets the user select one or more target AI assistants, generates tool-specific instruction files via LLM transformation, shows a dry-run preview, and writes the confirmed files to their canonical locations. It never modifies source files and never writes without explicit user confirmation.

---

## Process

### Step 1 — Source collection

**Guard — no CLAUDE.md:**
If no `CLAUDE.md` exists in the current working directory, present the user with two paths:

```
No CLAUDE.md found in the current directory.

Choose an option:
  1. project-setup first  — run /project-setup to scaffold CLAUDE.md + ai-context/ in this project,
                            then re-run /config-export (recommended for new projects with SDD workflow)
  2. SDD bootstrap         — generate a minimal .github/copilot-instructions.md from the global SDD
                            template only (no project-specific stack or conventions)

Enter 1 or 2 (or press Enter to cancel):
```

- If the user selects **1**: emit `Run /project-setup, then re-run /config-export` and stop. No files are written.
- If the user selects **2**: proceed using the global SDD methodology as the sole source bundle (skip ai-context/ collection; note "No project CLAUDE.md — bootstrap mode" in transformation context).
- If the user cancels: emit `Export cancelled — no files written` and stop.

**Guard — no ai-context/:**
If no `ai-context/` directory is present, emit:

```
WARNING: ai-context/ not found — export quality will be lower; only CLAUDE.md will be used as source
```

Continue; `CLAUDE.md` alone is sufficient.

**Read and bundle source files in priority order:**

| #   | File                         | Required? | Behavior when absent                                                 |
| --- | ---------------------------- | --------- | -------------------------------------------------------------------- |
| 1   | `CLAUDE.md`                  | Yes       | Halt (see guard above)                                               |
| 2   | `ai-context/stack.md`        | No        | Skip; note "stack.md not available" in transformation context        |
| 3   | `ai-context/architecture.md` | No        | Skip; note "architecture.md not available" in transformation context |
| 4   | `ai-context/conventions.md`  | No        | Skip; note "conventions.md not available" in transformation context  |
| 5   | `ai-context/known-issues.md` | No        | Skip silently if absent                                              |

All present files are read into the in-context bundle before any transformation begins.

---

### Step 2 — Target selection

**If the user provided a target as a CLI argument** (e.g., `/config-export copilot`), skip the interactive menu and proceed directly to Step 3 with that target.

**Otherwise, present the target menu:**

```
Available export targets:

  1. copilot  →  .github/copilot-instructions.md
  2. gemini   →  GEMINI.md
  3. cursor   →  .cursor/rules/conventions.mdc
               →  .cursor/rules/stack.mdc
               →  .cursor/rules/architecture.mdc

Enter targets (comma-separated numbers or names, or "all"):
```

**Claude target rejection:**
If the user requests target `claude` or `CLAUDE.md`, respond with:

```
The Claude target is not supported in V1 — use /project-update to refresh CLAUDE.md
```

Do not write any files; re-present the menu or halt based on user choice.

---

### Step 3 — Dry-run generation and confirmation

For each selected target, apply the corresponding transformation prompt (see sub-sections below). Then:

1. Display the full generated content for each file and its destination path.
2. If a target output file already exists at its canonical path, emit a warning **before** the confirmation prompt:
   ```
   WARNING: Overwriting existing file: <path>
   ```
3. Prompt the user:
   ```
   Write these files? [y/N]
   ```
   Default is **N**.
4. If the user responds with anything other than `y`, exit cleanly:
   ```
   Export cancelled — no files written
   ```
   No files are written.
5. If the user responds `y`, proceed to Step 4.

These transformation prompts are self-instructions executed by the agent using its own in-context LLM reasoning. No external API call, subprocess, or tool invocation is required to apply them — the agent reads the prompt and generates the output directly.

#### Shared STRIP Preamble

The following items MUST be stripped from ALL target outputs. Each transformation prompt below references this block — apply it in addition to any target-specific delta listed in that prompt.

- All slash commands used as executable triggers (any `/<word>` pattern that is a Claude Code meta-tool or SDD phase command)
- Task tool references and sub-agent delegation patterns (`"Task tool:"`, `"subagent_type:"`, `"Launch sub-agent"`, `"Sub-agent launch pattern"`)
- install.sh and sync.sh references
- Claude Code-specific identity statements ("I am an expert development assistant…")
- The `## Skills Registry` section of `CLAUDE.md` (lines beginning with `~/.claude/skills/` or `.claude/skills/`)
- Any section whose content is enclosed between `<!-- [auto-updated]` and `<!-- [/auto-updated] -->` comment markers in `ai-context/` files

---

#### Copilot transformation prompt

Apply the following prompt to the source bundle to generate `.github/copilot-instructions.md`:

---

You are transforming a Claude Code project configuration into a GitHub Copilot instruction file.

**Source bundle:** CLAUDE.md + any available ai-context/ files provided above.

**STRIP:**

Apply the Shared STRIP Preamble above, then additionally strip:

- Plan Mode rules section (Claude Code-specific)

**ADAPT — do NOT strip; rewrite for Copilot:**

1. **SDD phase DAG and workflow** → Convert to a `## SDD Development Workflow` section written in declarative prose:
   - Describe each phase (explore, propose, spec, design, tasks, apply, verify, archive) and its artifacts
   - Include the artifact storage paths (`openspec/changes/<change-name>/proposal.md`, `design.md`, `tasks.md`, `verify-report.md`, archive convention)
   - Do NOT include any slash command syntax — describe the phases as steps the developer initiates

2. **SDD available commands table** → Replace with a `## Active SDD Coaching Instructions` section containing Copilot behavioral instructions:

   ```
   When a developer mentions implementing a new feature, change, or fix:
   - Proactively ask: "Would you like to follow the SDD workflow for this change?"
   - If yes, guide them step by step: propose → (spec + design in parallel) → tasks → apply → verify → archive
   - Before starting apply, confirm that proposal.md, design.md, and tasks.md exist under openspec/changes/<change-name>/
   - Remind the developer to run verify after implementation and archive once confirmed
   ```

   Adapt the phrasing to be Copilot-idiomatic (imperative instructions telling Copilot how to behave).

3. **Project memory layer (ai-context/)** → Retain the table and description verbatim; it applies directly to projects using Copilot too.

**RETAIN and adapt:**

- Tech stack (language, framework, key tools, versions)
- Coding conventions (naming, style, patterns) — rephrase as direct instructions to the AI assistant in imperative voice
- Architecture decisions and rationale
- Known issues and gotchas relevant to a developer working in the project
- Key working principles (clean code, no over-engineering, tests as first-class citizens, etc.)
- openspec/ artifact paths and SDD change directory structure

**FORMAT:**

- Single flat Markdown file
- UTF-8, no BOM
- H2 sections (no YAML frontmatter)
- Start with a top-level heading: `# Project Instructions`
- Required H2 sections in this order:
  1. `## Tech Stack` (if stack data available)
  2. `## Architecture` (if architecture data available)
  3. `## Conventions`
  4. `## SDD Development Workflow` ← always present, even in bootstrap mode
  5. `## Active SDD Coaching Instructions` ← always present
  6. `## Working Principles`
  7. `## Known Issues` (if known-issues.md available)
  8. `## Source Notes` (only if any source file was absent)
- Begin with the generated-file banner (verbatim, before the H1):
  ```
  <!-- GENERATED BY config-export — DO NOT EDIT MANUALLY -->
  <!-- Source: CLAUDE.md + ai-context/ | Generated: YYYY-MM-DD -->
  <!-- Re-generate: run /config-export in your Claude Code session -->
  ```
  Replace `YYYY-MM-DD` with today's date.
- In bootstrap mode (no project CLAUDE.md), the `## SDD Development Workflow` and `## Active SDD Coaching Instructions` sections MUST still be fully generated from the global SDD methodology; all project-specific sections are omitted and noted under `## Source Notes`.
- Output path: `.github/copilot-instructions.md`

---

#### Gemini transformation prompt

Apply the following prompt to the source bundle to generate `GEMINI.md`:

---

You are transforming a Claude Code project configuration into a Google Gemini instruction file (GEMINI.md).

**Source bundle:** CLAUDE.md + any available ai-context/ files provided above.

**STRIP:**

Apply the Shared STRIP Preamble above, then additionally strip:

- SDD phase DAG diagram
- openspec/ artifact paths and SDD change directory references

**ADAPT (do not strip wholesale):**

- SDD command tables: remove the command table verbatim; you MAY include an adapted prose paragraph describing a structured development workflow if it adds value for Gemini users — but no slash commands
- Claude-specific section headers (e.g., "How I Execute Commands", "SDD Orchestrator — Delegation Pattern"): rename to Gemini equivalents or remove if the content has no value outside Claude Code

**RETAIN:**

- Tech stack, coding conventions, architecture decisions, known issues
- Working principles and development philosophy
- Project memory layer description (ai-context/ structure)

**FORMAT:**

- Single Markdown file at project root
- UTF-8, no BOM
- Structure similar to CLAUDE.md (not flat — preserve H2/H3 hierarchy where content warrants it)
- Start with a top-level heading (e.g., `# Gemini — Project Configuration`)
- Begin with the generated-file banner (verbatim, before the H1):
  ```
  <!-- GENERATED BY config-export — DO NOT EDIT MANUALLY -->
  <!-- Source: CLAUDE.md + ai-context/ | Generated: YYYY-MM-DD -->
  <!-- Re-generate: run /config-export in your Claude Code session -->
  ```
  Replace `YYYY-MM-DD` with today's date.
- Output path: `GEMINI.md`

---

#### Cursor transformation prompt

Apply the following prompt to the source bundle to generate `.cursor/rules/*.mdc` files:

---

You are transforming a Claude Code project configuration into Cursor MDC rule files.

**Source bundle:** CLAUDE.md + any available ai-context/ files provided above.

**STRIP the following from all output files:**

Apply the Shared STRIP Preamble above, then additionally strip:

- SDD phase DAG diagram
- openspec/ artifact paths and SDD change directory references

**OUTPUT STRUCTURE — split into exactly three domain files:**

1. **`conventions.mdc`** — coding rules, naming conventions, style guidelines, error handling patterns
2. **`stack.mdc`** — tech stack, language versions, key frameworks and tools, package manager
3. **`architecture.mdc`** — architecture decisions, system design patterns, data flow, inter-component contracts

If source material is insufficient to produce meaningful content for a domain (e.g., no architecture.md and no architecture content in CLAUDE.md), produce a minimal file with the frontmatter and a one-line note rather than omitting the file.

**MDC FRONTMATTER CONTRACT — every file MUST have:**

```yaml
---
description: "[one-line description of this rules domain]"
globs: "[glob pattern or empty string]"
alwaysApply: [true|false]
---
```

Domain defaults:

| File               | `globs` | `alwaysApply` |
| ------------------ | ------- | ------------- |
| `conventions.mdc`  | `""`    | `true`        |
| `stack.mdc`        | `""`    | `false`       |
| `architecture.mdc` | `""`    | `false`       |

**CRITICAL — globs field:** Use `""` when no meaningful file-pattern can be inferred. NEVER guess at glob patterns. The `globs` field MUST be a string (not YAML null).

**FORMAT per file:**

- UTF-8, no BOM
- YAML frontmatter block first (between `---` delimiters)
- Generated-file banner immediately after the closing `---` of the frontmatter:
  ```
  <!-- GENERATED BY config-export — DO NOT EDIT MANUALLY -->
  <!-- Source: CLAUDE.md + ai-context/ | Generated: YYYY-MM-DD -->
  <!-- Re-generate: run /config-export in your Claude Code session -->
  ```
  Replace `YYYY-MM-DD` with today's date.
- File name: lowercase slug with `.mdc` extension (e.g., `conventions.mdc`)
- If source material was only CLAUDE.md (no ai-context/), set `description` to note it: e.g., `"Generated from CLAUDE.md — ai-context/ not found"`
- Output paths: `.cursor/rules/conventions.mdc`, `.cursor/rules/stack.mdc`, `.cursor/rules/architecture.mdc`

---

### Step 4 — File writing

For each confirmed target:

1. Create required directories silently if they do not exist:
   - Copilot: `.github/`
   - Cursor: `.cursor/rules/`
   - Gemini: no directory required (file at project root)
   - Do NOT emit any output for directory creation unless it fails.

2. Write the generated file to its canonical path, prepending the generated-file banner:

   ```
   <!-- GENERATED BY config-export — DO NOT EDIT MANUALLY -->
   <!-- Source: CLAUDE.md + ai-context/ | Generated: YYYY-MM-DD -->
   <!-- Re-generate: run /config-export in your Claude Code session -->
   ```

   Replace `YYYY-MM-DD` with today's date.

3. Overwrite any existing file at the canonical path — this is idempotent behavior. No error is raised when overwriting.

---

### Step 5 — Summary

After all confirmed files have been written, print a summary table:

```
Export complete — files written:

  File                                  Status
  ──────────────────────────────────    ───────
  .github/copilot-instructions.md       written
  GEMINI.md                             written
  .cursor/rules/conventions.mdc         written
  .cursor/rules/stack.mdc               written
  .cursor/rules/architecture.mdc        written
```

(Only include rows for targets that were written in this run.)

Then append the snapshot reminder:

```
Exported files are snapshots. Re-run /config-export after significant changes to CLAUDE.md or ai-context/
```

---

## Rules

- If no `CLAUDE.md` is found in CWD, the skill MUST present the two-path menu (project-setup or bootstrap) before any file write; the hard ERROR path is NOT the default
- Bootstrap mode (option 2) MUST produce a valid Copilot instructions file containing the full SDD workflow and coaching instructions even when no project CLAUDE.md exists
- The Copilot transformation MUST NOT strip the SDD phase workflow or artifact paths — it MUST adapt them to prose and Copilot coaching instructions
- The `## SDD Development Workflow` and `## Active SDD Coaching Instructions` sections MUST always be present in the Copilot output (whether from project mode or bootstrap mode)
- Dry-run preview MUST precede any file write — there is no flag to skip dry-run
- Overwrite warnings MUST appear in the dry-run step (before user confirmation), not after
- The skill MUST NOT modify `CLAUDE.md`, any `ai-context/` file, or any `openspec/` artifact — read-only with respect to all source files
- Directory creation (`.github/`, `.cursor/rules/`) MUST be silent — no output for directory creation unless it fails
- The Claude target (`CLAUDE.md`) is NOT supported in V1 — respond with the defined rejection message; do not write any files for that target
- All generated files MUST be UTF-8, no BOM
- Each Cursor `.mdc` file MUST have valid YAML frontmatter with `description`, `globs`, and `alwaysApply` fields
- Cursor `.mdc` file names MUST be valid slugs: lowercase letters, digits, and hyphens only, with the `.mdc` extension
- Copilot output MUST be a single file at `.github/copilot-instructions.md` — no splitting
- Gemini output MUST be a single file at `GEMINI.md` at the project root — no subdirectories
- The `globs` field in Cursor MDC files MUST use `""` when no meaningful pattern can be inferred — never guess
- All content in generated files MUST be free of Claude Code-specific execution syntax: no Task tool invocations, no sub-agent patterns, no `~/.claude/skills/` file paths
- Copilot MUST adapt SDD content (workflow, phases, artifacts) — stripping rules apply only to execution-layer Claude Code syntax; SDD methodology and openspec/ paths are RETAINED and adapted for all targets
- No target receives a verbatim copy of `CLAUDE.md`
