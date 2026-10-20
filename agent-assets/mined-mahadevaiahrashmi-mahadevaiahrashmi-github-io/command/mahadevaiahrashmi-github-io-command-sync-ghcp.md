<!-- agent-notes: { ctx: "sync Claude Code agents to GitHub Copilot format", deps: [CLAUDE.md, .claude/agents/, .claude/commands/, docs/methodology/personas.md], state: active, last: "diego@2026-02-12" } -->
Sync the Claude Code agent/persona system to GitHub Copilot format.

This command uses Claude Code as the source of truth and generates/updates the GHCP equivalents in `.github/`. It does NOT use a static generation script — instead it researches the current GHCP format at runtime and adapts accordingly.

## Why a Command Instead of a Script

Both Claude Code and GHCP are actively evolving their agent/customization formats. A static script encodes today's format assumptions and rots silently. This command brings the model's current knowledge of both platforms to every run and can web-search for the latest specs, making it resilient to format changes on either side.

## Process

### 1. Read the Claude Code Source of Truth

Read all files that define the agent/persona system:

- `CLAUDE.md` — project instructions and persona triggers
- `.claude/agents/*.md` — all subagent definitions (frontmatter + body)
- `.claude/commands/*.md` — all custom commands
- `docs/methodology/personas.md` — shared persona catalog

Take note of each agent's name, description, tool permissions (both allowed and disallowed), model preference, max turns, and the full body content that defines their behavior.

### 2. Research Current GHCP Format

Use `WebSearch` to find the **current** GitHub Copilot customization specs:

- Search for "GitHub Copilot custom agents .agent.md format site:code.visualstudio.com OR site:docs.github.com" — look for frontmatter fields, tool names, and supported options.
- Search for "GitHub Copilot prompt files .prompt.md format site:code.visualstudio.com OR site:docs.github.com" — look for frontmatter fields and how they're invoked.
- Search for "GitHub Copilot copilot-instructions.md format site:code.visualstudio.com OR site:docs.github.com" — look for structure and conventions.
- Search for "GitHub Copilot AGENTS.md format" — check if this coordination file is still supported and how it works.

Also check `docs/plans/ghcp-migration.md` for any earlier mapping work, but **prefer fresh web research** over the plan file since GHCP may have changed since the plan was written.

### 3. Build the Tool Name Mapping

Based on the current GHCP docs, build a mapping from Claude Code tool names to GHCP equivalents. As of the last known state, the mapping was roughly:

| Claude Code | GHCP |
|---|---|
| `Read` | `read` |
| `Write`, `Edit` | `edit/editFiles` |
| `Grep`, `Glob` | `search/codebase` |
| `Bash` | `runInTerminal` |
| `WebSearch`, `WebFetch` | `fetch` or MCP equivalent |
| `NotebookEdit` | (check if equivalent exists) |

**Do not assume this mapping is current.** Verify against the GHCP docs you just found.

### 4. Convert Agent Files

For each `.claude/agents/*.md` file, create or update the corresponding `.github/agents/*.agent.md` file:

- Translate the YAML frontmatter to GHCP format (field names, tool names, model identifier).
- Convert `disallowedTools` (blocklist) to an allowlist.
- Drop `maxTurns` if GHCP has no equivalent, or map it if they've added one.
- Keep the body content largely intact, but update Claude Code-specific references to GHCP equivalents.

### 5. Convert Command Files

For each `.claude/commands/*.md` file, create or update the corresponding `.github/prompts/*.prompt.md` file:

- Add GHCP prompt file frontmatter (`mode`, `description`, `tools`, `model`).
- Translate `$ARGUMENTS` to whatever GHCP uses for prompt arguments.
- Update internal references to other commands and agents to use GHCP paths/syntax.

### 6. Generate copilot-instructions.md

Create or update `.github/copilot-instructions.md` based on `CLAUDE.md`:

- Adapt the project overview, development philosophy, and workflow sections.
- Translate the persona trigger table to reference GHCP agents and invocation patterns.
- Update subagent and command paths.
- Keep `docs/` references unchanged — those are shared.

### 7. Verify Consistency

After generating all files, do a quick consistency check:

- Every `.claude/agents/*.md` file has a corresponding `.github/agents/*.agent.md` file.
- Every `.claude/commands/*.md` file has a corresponding `.github/prompts/*.prompt.md` file (except this `sync-ghcp.md` command itself — it's Claude Code-only).
- No GHCP files reference Claude Code-specific concepts.
- The tool names in GHCP agent files are valid GHCP tool identifiers.

### 8. Summary

Report:
- How many agent files were created/updated.
- How many prompt files were created/updated.
- Whether `copilot-instructions.md` was created/updated.
- Any conversion decisions that were ambiguous or need human review.
- Any GHCP format changes detected compared to previous runs.
- Any Claude Code features that have no GHCP equivalent.
