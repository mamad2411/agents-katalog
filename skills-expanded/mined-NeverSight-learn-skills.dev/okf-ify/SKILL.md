---
name: okf-ify
description: Scaffolds an OKF (Open Knowledge Format) knowledge base in a new or existing project and configures coding agents (Claude Code, OpenCode, oh-my-pi) to use it. Asks for the knowledge base location, concept directories, and which agents to configure, then creates the bundle structure and wires agent hooks/config.
---

# okf-ify

Create an OKF knowledge base in the current project and wire it into one or more coding agents.

## When to Use This Skill

Use this skill when the user:

- Says `/okf-ify` or "okf-ify"
- Asks to "add a knowledge base" or "set up an OKF knowledge base"
- Wants to create an OKF-style knowledge base for their project
- Wants to scaffold a knowledge base that agents can consult and update

## What is OKF?

The [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) is an open, human- and agent-friendly format for representing knowledge as a directory of markdown files with YAML frontmatter. It is designed to be authored by people and agents, read by both, and diffed in version control.

A knowledge bundle is a directory tree of markdown files:

- `index.md` — directory listing and agent policy (reserved filename).
- `log.md` — chronological update history (reserved filename).
- `<concept>.md` — a concept document with YAML frontmatter (`type` is the only required field).
- Subdirectories organize concepts into groups, each with its own `index.md`.

## Workflow

### Step 1: Gather Parameters

Ask the user the following questions. Present defaults and allow the user to accept or override.

**Question 1: Knowledge base location.**

> Where should the knowledge base be created? (default: `docs/knowledgebase`)

If the project already has a knowledge base at the specified location, confirm whether to re-scaffold (overwrite) or pick a different location.

**Question 2: Concept directories.**

> Which concept directories should be created? Provide a comma-separated list.
> (default: `concepts, decisions, patterns, references, plans`)

These become subdirectories in the bundle, each with an `index.md` listing.

**Question 3: Agent configuration.**

> Which agents should be configured to use this knowledge base?
> Select one or more: claude-code, opencode, oh-my-pi, none
> (default: detect from existing config directories, or ask if none detected)

Detection rules:
- `.claude/` directory exists → suggest claude-code.
- `.opencode/` directory exists → suggest opencode.
- `.omp/` directory exists → suggest oh-my-pi.
- If none detected, ask the user directly.

### Step 2: Determine the Project Name

Derive the project name from:
1. `package.json` `name` field (if it exists).
2. `Cargo.toml` `[package] name` field (if it exists).
3. `go.mod` module name (if it exists).
4. The basename of the project root directory.

Use this name in the KB index title and in agent hook preamble text.

### Step 3: Create the Knowledge Base

Create the following files at the specified location (relative to the project root). All template files are in the `templates/` directory alongside this SKILL.md — read them and substitute the placeholders.

**Placeholders:** All templates use `{{PROJECT_NAME}}`, `{{KB_LOCATION}}`, `{{KB_PATH}}` (the relative path from project root to the KB directory, e.g. `docs/knowledgebase`), and `{{CONCEPT_DIRS}}` (the comma-separated list of concept directory names).

#### Root files

1. **`{{KB_LOCATION}}/index.md`** — from `templates/index.md.tmpl`. The KB manifest with:
   - OKF frontmatter (`okf_version`).
   - Title: `{{PROJECT_NAME}} knowledge base`.
   - Agent policy section (consult before acting, update after acting).
   - Empty concept directory listings (the user will fill these in).
   - Reference to OKF spec.

2. **`{{KB_LOCATION}}/log.md`** — from `templates/log.md.tmpl`. The update history with an initial entry recording the scaffold.

3. **`{{KB_LOCATION}}/references/okf-spec.md`** — from `templates/okf-spec-reference.md.tmpl`. A pointer to the OKF specification.

#### Concept directory index files

For each directory in the concept dirs list, create `{{KB_LOCATION}}/<dir>/index.md` from `templates/category-index.md.tmpl` with the directory name substituted. Capitalize the first letter for the heading title.

### Step 4: Configure Agents

For each selected agent, install the agent-specific configuration. Read the template files from `templates/` and substitute placeholders.

#### Claude Code

1. Create `.claude/hooks/kb-inject.py` from `templates/claude-kb-inject.py.tmpl`.
   - This is a SessionStart hook that injects `{{KB_LOCATION}}/index.md` as context.
   - Make the file executable (`chmod +x`).

2. Create `.claude/hooks/kb-reminder.py` from `templates/claude-kb-reminder.py.tmpl`.
   - PostToolUse + Stop hooks that nudge the agent to keep the KB current.
   - The `TRIGGERS` list is left empty — the user fills in project-specific path patterns.
   - Make the file executable.

3. Update `.claude/settings.json`:
   - If the file exists, read it and merge the hook entries from `templates/claude-settings-fragment.json.tmpl` into the `hooks` object (merge by event name, appending to existing arrays).
   - If the file does not exist, create it from the fragment template.
   - The `KB_PATH` placeholder uses forward slashes.

#### OpenCode

1. Create or update `.opencode/opencode.jsonc`:
   - If the file exists, read it and add `"{{KB_LOCATION}}/index.md"` to the `instructions` array (if not already present). Preserve comments and existing structure.
   - If the file does not exist, create it from `templates/opencode-config-fragment.jsonc.tmpl`.

#### oh-my-pi (omp)

1. Create `.omp/extensions/kb-hooks.ts` from `templates/omp-extension.ts.tmpl`.
   - TypeScript extension with `session_start`, `before_agent_start`, `tool_result`, and `session_stop` hooks.
   - The `TRIGGERS` array is left empty — the user fills in project-specific path patterns.

### Step 5: Update the KB Index with Agent Info

After configuring agents, update `{{KB_LOCATION}}/index.md` to list the configured agents in the "For agents (policy)" section. The policy text should mention which agents are wired and how (e.g., "Claude Code via a SessionStart hook, opencode via the instructions config, oh-my-pi via the .omp/extensions/kb-hooks.ts extension").

### Step 6: Report

Print a summary of what was created:

- The knowledge base directory tree.
- The agent configurations installed.
- A note that the `TRIGGERS` lists in the reminder hooks are empty and should be filled with project-specific path patterns.
- A note that the KB is ready to use — agents will consult it automatically on the next session.

## Non-Goals

- This skill does **not** populate the knowledge base with project-specific content. It scaffolds the structure and configures agents; the agent (or user) fills in concepts, decisions, and patterns as the project evolves.
- This skill does **not** install the OKF spec itself. It creates a reference pointer to the spec.
- This skill does **not** configure agents beyond the three supported (claude-code, opencode, oh-my-pi). For adding a new agent to an existing KB, use the `okf-ify-agent-setup` skill.

## Templates

All template files are in the `templates/` directory next to this SKILL.md. Read them at execution time and substitute the placeholders:

- `{{PROJECT_NAME}}` — the project name.
- `{{KB_LOCATION}}` — the knowledge base directory path relative to project root (e.g. `docs/knowledgebase`).
- `{{KB_PATH}}` — same as `{{KB_LOCATION}}` but with forward slashes (for use in JSON and code).
- `{{CONCEPT_DIRS}}` — comma-separated list of concept directory names (e.g. `concepts, decisions, patterns, references, plans`).
- `{{CONCEPT_DIR}}` — a single concept directory name (used in per-directory templates).
- `{{CONCEPT_TITLE}}` — the concept directory name capitalized (e.g. `Concepts`, `Decisions`).
- `{{PROJECT_SLUG}}` — the project name in lowercase-hyphenated form (e.g. `my-project`), used in temp-dir names and identifiers.