---
name: find-agents
version: 2.0.0
description: |
  Discover, install, and manage AI agents across 43+ coding CLIs and IDEs from ONE source —
  auto-translated to each client's native format, not hand-ported — with the `agentshq` CLI: `find`,
  `add`, `list`, `remove`, `check`/`update`, and `init` scaffolding, scoped by `-g` (global) and
  `--ide` targets. Explicit-user-only and precise: it never installs, removes, or updates agents the
  user didn't ask for. Use to find agents or manage an existing agent catalog.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
disable-model-invocation: true
user-invocable: true
argument-hint: "[search query, source repo, or management action]"
arguments:
  - request
when_to_use: |
  Use only when the user explicitly asks to find, install, list, remove, update, or scaffold agents.
  Examples: "/find-agents react reviewer", "install agents from owner/repo", "list my installed
  agents", "update all agents". Do NOT use proactively, do NOT install globally unless global scope was
  requested, and do NOT guess target IDEs when the user named a specific client; confirm scope and
  target before mutating the agent inventory.
effort: high
---

<EXTREMELY-IMPORTANT>
This skill changes the user's agent inventory and must stay explicit-user-only.

Non-negotiable rules:
1. Verify `agentshq` availability before relying on it.
2. Be explicit about scope: project vs global, specific IDEs vs auto-detect.
3. Do not install or remove agents the user did not ask for.
4. Confirm ambiguous install targets before making changes.
5. Report exactly what was added, removed, or updated.
</EXTREMELY-IMPORTANT>

# Find Agents

## Inputs

- `$request`: Search terms, repo source, or management intent such as `list`, `remove`, or `update`

## Goal

Use `agentshq` to help the user:

- discover relevant agents
- install agents into one or more CLIs or IDEs
- list current inventory
- remove or update installed agents
- scaffold a new agent when asked

## Step 0: Verify runtime prerequisites

Check:

- Node.js availability
- `npx agentshq --version`

If the CLI is unavailable, explain the blocker and stop.

**Success criteria**: `agentshq` can be invoked from the current environment.

## Step 1: Resolve the user's intent

Determine whether the user wants to:

- search
- install
- list
- remove
- update
- scaffold

Also resolve:

- project vs global scope
- target IDEs/CLIs if specified
- source repo, URL, or local path if installing

If those details are ambiguous, ask before mutating anything.

**Success criteria**: The exact `agentshq` action is clear before execution.

## Step 2: Run the narrowest relevant command

### Command Reference

| Action | Command | Key Flags |
|--------|---------|-----------|
| Search | `npx agentshq find [query]` | interactive picker when no query given |
| Install from repo | `npx agentshq add <owner>/<repo>` | `@<agent-name>` for specific agent |
| Install from URL | `npx agentshq add <url>` | also works with local paths |
| Install scope | | `-g` for global, `--ide <name> ...` for specific IDEs |
| Install options | | `--all` for all agents to all IDEs, `--list` to preview |
| List installed | `npx agentshq list` | `-g` for global, `--ide <name>`, `--json` |
| Remove | `npx agentshq remove [name]` | `-g` for global, `--all` for all agents |
| Check updates | `npx agentshq check` | |
| Apply updates | `npx agentshq update` | |
| Scaffold new | `npx agentshq init [name]` | |

When installing, respect:

- explicit `--ide ...` choices when the user gave them
- `-g` only when the user asked for global scope
- `--list` when the user wants to inspect a source before installing

### Supported IDEs

The CLI supports 43+ IDEs. Common ones:

| IDE | Format |
|-----|--------|
| Claude Code | `.md` with YAML frontmatter |
| Cursor | `AGENTS.md` sections |
| GitHub Copilot | `.agent.md` |
| Windsurf | `AGENTS.md` sections |
| Codex | `AGENTS.md` sections |
| Gemini CLI | `.md` with YAML frontmatter |
| Kiro | `.json` |
| Amp | `AGENTS.md` sections |
| Roo Code | `AGENTS.md` sections |

Agents are automatically translated to each IDE's native format on install.

**Success criteria**: The command matches the user's intent and scope exactly.

## Step 3: Report the result clearly

After execution, report:

- what command ran
- which agents matched or changed
- which clients/IDEs were targeted
- any next steps such as authentication, reload, or restart

When searching, present the most relevant results instead of dumping raw output.

**Success criteria**: The user can immediately decide what to do next.

## Guardrails

- Do not run this skill proactively.
- Do not install globally unless the user asked for global scope.
- Do not remove or update agents without explicit user intent.
- Do not guess target IDE names when the user clearly cares about a specific client.
- Remember that `agentshq` can translate one source agent into multiple client formats; report that clearly.

## Output Contract

Report:

1. the resolved action
2. project/global scope
3. target IDEs or CLIs
4. the agents found or changed
5. any follow-up steps the user should know about
