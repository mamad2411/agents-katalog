---
name: cursor-context-scout
description: Use before editing unfamiliar or large codebases, especially when Claude Code or Codex needs to save context by asking Cursor SDK to identify the smallest set of relevant files first. Triggers for requests mentioning Cursor SDK, context scouting, codebase indexing, semantic search, relevant files, Figma comments to implementation, or "before editing, find files".
allowed-tools: Bash(node *) Bash(npm *)
---

# Cursor Context Scout

Use this skill before making code changes when the task would benefit from Cursor's codebase indexing and semantic search. The goal is to spend a small Cursor SDK run to produce a compact file map, then have the current agent read only the relevant files.

## Workflow

1. Do not edit files yet.
2. Locate the bundled script. Use the first existing path:

- `${CLAUDE_SKILL_DIR}/scripts/cursor-scout.mjs` when `CLAUDE_SKILL_DIR` is available.
- `.agents/skills/cursor-context-scout/scripts/cursor-scout.mjs` for Codex or other agents using the shared skills path.
- `.claude/skills/cursor-context-scout/scripts/cursor-scout.mjs` for Claude Code project installs.
- `~/.agents/skills/cursor-context-scout/scripts/cursor-scout.mjs` for global Agent Skills installs.
- `~/.config/agents/skills/cursor-context-scout/scripts/cursor-scout.mjs` for global universal Agent Skills installs.
- `~/.cursor/skills/cursor-context-scout/scripts/cursor-scout.mjs` for global Cursor installs.
- `~/.codex/skills/cursor-context-scout/scripts/cursor-scout.mjs` for global Codex installs.
- `~/.claude/skills/cursor-context-scout/scripts/cursor-scout.mjs` for global Claude Code installs.

3. Run the scout script from the target repository root:

```bash
node <path-to-cursor-scout.mjs> scout --repo . --task "$ARGUMENTS"
```

4. Read the generated `.cursor-scout/last-scout.json`.
5. Read only the top `recommended_files` first. Expand to `supporting_files` only if implementation needs more context.
6. Then implement the user's requested change using the current agent's normal editing tools.
7. Do not commit `.cursor-scout/` unless the user explicitly wants scout artifacts checked in.

## First Run

The first scout run may be slower because Cursor may need to prepare or warm its codebase index. The script will bootstrap `@cursor/sdk` into a user cache directory if the package is not already available.

Requirements:

- A Cursor User API Key must be configured with `configure` or set as `CURSOR_API_KEY`.
- Node.js 22+ is recommended by Cursor's SDK examples.
- Network access is needed the first time `@cursor/sdk` is installed into the cache.

To get a Cursor User API Key, open <https://cursor.com/dashboard>, then go to `Integrations` > `User API Keys` and create a key. Do not use a model-provider key from Cursor model settings, and do not use a Cursor Admin API key.

Configure the Cursor API key if `doctor` reports that no key is available. Use global setup for all repositories:

```bash
node <path-to-cursor-scout.mjs> configure --scope global
```

Global setup writes an `export CURSOR_API_KEY=...` block to the user's shell profile such as `~/.zshrc`. Use project setup to write `.env.local` in the target repo:

```bash
node <path-to-cursor-scout.mjs> configure --scope project --repo .
```

`CURSOR_API_KEY` in the current process has highest priority. Project `.env.local` is read next, then the global shell profile.

Run a setup check:

```bash
node <path-to-cursor-scout.mjs> doctor --install-sdk
```

Run a warmup without a concrete task:

```bash
node <path-to-cursor-scout.mjs> warmup --repo .
```

## Guardrails

- Treat Cursor as a read-only scout. The prompt explicitly forbids edits, dependency installs, commits, and destructive commands.
- Cursor has not documented a direct public API for reading its embedding index. This skill asks Cursor Agent to use its codebase tools and return a compact file map.
- If the scout JSON cannot be parsed, inspect `.cursor-scout/last-scout.raw.txt` and decide manually.
- If the user explicitly asks you to skip scouting or the repo is small enough that direct inspection is cheaper, proceed without this skill.
- Do not paste secrets into prompts. Use environment variables.

## Output

The script writes:

- `.cursor-scout/last-scout.json`: parsed scout result.
- `.cursor-scout/last-scout.raw.txt`: raw Cursor response for debugging.

For the full schema, see `references/output-schema.md`.
