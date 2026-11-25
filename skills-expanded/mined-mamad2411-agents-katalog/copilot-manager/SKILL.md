---
name: copilot-manager
description: >
  Discover, audit, reconcile, modify, and delete GitHub Copilot customizations across
  both Copilot IDE (VS Code) and Copilot CLI environments. Use this skill whenever the
  user wants to "list copilot customizations", "find copilot files", "audit copilot setup",
  "what copilot configs do I have", "reconcile copilot IDE and CLI", "clean up copilot files",
  "delete copilot agent", "show copilot instructions", "compare copilot configs",
  "remove unused copilot customizations", "copilot drift", "copilot inventory",
  "what does copilot see", "manage copilot", "copilot hygiene", or any request involving
  exploring, inspecting, modifying, or removing existing Copilot customization files.
  Also triggers when the user mentions conflicts between Copilot IDE and Copilot CLI,
  cross-readability issues, or wants to understand which files each Copilot variant sees.
  Does NOT trigger for creating new customizations from scratch (use copilot-customization
  skill instead).
---

# Copilot Manager

Manage existing GitHub Copilot customizations across both Copilot IDE (VS Code/JetBrains)
and Copilot CLI (terminal agent). This skill gives you the ability to discover what exists,
find conflicts, reconcile between the two environments, and surgically modify or remove
customizations — all using file tools, no external dependencies.

## How the Two Copilots Differ

Copilot IDE and Copilot CLI share some paths but have distinct discovery models.
Understanding this is key to everything that follows.

**Shared paths** (both targets read these):
- `.github/copilot-instructions.md` — project-level guidance
- `.github/agents/*.md` — custom agents
- `.github/skills/*/SKILL.md` — skills
- `.github/hooks/*.json` — hooks
- `AGENTS.md` — root-level agent definitions
- `~/.copilot/agents/`, `~/.copilot/skills/` — user-level artifacts

**IDE-only features:**
- `.github/prompts/*.prompt.md` — prompt templates (CLI has no equivalent)
- `.vscode/settings.json`, `.vscode/mcp.json` — VS Code settings & MCP
- `.devcontainer.json` — dev container MCP servers
- Settings-driven custom paths (`chat.*Locations` keys)
- Cross-reads `CLAUDE.md` and `GEMINI.md` from repo root
- Language model overrides via settings

**CLI-only features:**
- `~/.copilot/config.json` — CLI-specific configuration
- `~/.copilot/copilot-instructions.md` — user-level guidance
- `.claude/commands/*.md` — command files
- Parent directory chain walking (inherits from parent dirs)
- Environment variables: `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`, `COPILOT_HOME`
- User-level agents override project-level (opposite of IDE)

**Files read by both targets at repo root:**
- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`
- `CLAUDE.local.md` is read by IDE only (not by CLI)

For complete path listings, read `references/copilot-ide-paths.md` and
`references/copilot-cli-paths.md`.

## Operations

### 1. Discover — "What customizations exist?"

Scan the workspace and user home to build a complete inventory.

**Workspace scan** — use Glob to check each path family:

```
# Shared paths
.github/copilot-instructions.md
.github/instructions/*.instructions.md
.github/agents/*.md
.github/skills/*/SKILL.md
.github/hooks/*.json
.github/prompts/*.prompt.md
AGENTS.md
.agents/skills/*/SKILL.md

# IDE-specific paths
.vscode/settings.json
.vscode/mcp.json
.vscode/hooks/*.json
.devcontainer.json
.devcontainer/devcontainer.json
.github/chatmodes/*.chatmode.md

# Shared instruction files (read by both IDE and CLI)
CLAUDE.md
GEMINI.md

# IDE-only instruction files
CLAUDE.local.md
.claude/CLAUDE.md
.claude/rules/*.md
.claude/agents/*.md
.claude/skills/*/SKILL.md
.claude/commands/*.md
.claude/settings.json
.claude/settings.local.json
```

**User-level scan** — expand `~` to the actual home directory, then Glob:

```
# Copilot user tree
~/.copilot/config.json
~/.copilot/copilot-instructions.md
~/.copilot/instructions/*.instructions.md
~/.copilot/agents/*.md
~/.copilot/skills/*/SKILL.md
~/.copilot/mcp-config.json

# Claude user tree (cross-read)
~/.claude/CLAUDE.md
~/.claude/rules/*.md
~/.claude/agents/*.md
~/.claude/skills/*/SKILL.md
~/.claude/commands/*.md

# VS Code profile (Windows: ~/AppData/Roaming/Code/User/, Linux/Mac: ~/.config/Code/User/)
<vscode-profile>/agents/*.md
<vscode-profile>/prompts/*.prompt.md
<vscode-profile>/skills/*/SKILL.md
<vscode-profile>/hooks/*.json
<vscode-profile>/mcp.json
```

**Plugin scan:**
```
~/.copilot/installed-plugins/*/
~/.copilot/state/marketplace-cache/*/
```
Each plugin folder should contain a `plugin.json` (check `.github/plugin/`, `.claude-plugin/`, then root).

**For each discovered file**, read it and extract:
- **Kind**: guidance, agent, skill, prompt, hook, mcp, setting, command, plugin
- **Target**: which Copilot(s) see it (IDE, CLI, or both)
- **Scope**: user, repository, or directory
- **Name**: from frontmatter `name`/`id` field, or filename stem
- **Frontmatter**: parse the YAML between `---` delimiters (see `references/frontmatter-schema.md`)

Present results as a table grouped by kind, showing path, target visibility, scope, and name.

### 2. Audit — "Are there problems?"

After discovery, check for these issue categories:

**Name collisions**: Two artifacts of the same kind with the same logical name.
Group all discovered artifacts by `(kind, lowercase_name)`. Any group with >1 entry
is a potential collision. Classify as:
- **Same target, different scopes** → shadowed (higher scope wins)
- **Same target, same scope, different paths** → ambiguous (error — needs resolution)
- **Different targets, same scope** → duplicate (warning — may be intentional)

**Lossy mappings**: Artifacts that exist for one target but not the other, where no
cross-readability rule covers the gap:
- `.prompt.md` files → only IDE sees them, CLI has no equivalent
- `.claude/commands/*.md` → only CLI sees them, IDE has no equivalent
- VS Code settings-driven instructions → only IDE sees them
- `CLAUDE.local.md` → only IDE reads it, CLI does not
- `.vscode/mcp.json` → only IDE sees it; CLI uses `~/.copilot/mcp-config.json`

**Cross-read awareness**: Both `CLAUDE.md` and `GEMINI.md` are read by both Copilot
IDE and CLI. `CLAUDE.local.md` is read only by IDE. Warn if these files contain
tool-specific instructions that don't make sense for all readers.

**MCP drift**: Compare `.vscode/mcp.json` (IDE) with `~/.copilot/mcp-config.json`
(CLI user). Flag servers that exist in one but not the other. Note: CLI has no
standard repo-level MCP path equivalent to IDE's `.vscode/mcp.json`.

**Orphaned legacy files**: Check for `.chatmode.md` files — these still work but should
be migrated to `.md` agents.

**Settings checks**: If `.vscode/settings.json` exists, look for:
- `chat.useAgentsMdFile` — is `AGENTS.md` reading enabled?
- `chat.useClaudeMdFile` — is `CLAUDE.md` cross-reading enabled?
- `chat.useNestedAgentsMdFiles` — are nested `AGENTS.md` files enabled?
- Custom location overrides that might point to nonexistent paths

For the full reconciliation checklist, read `references/reconciliation.md`.

### 3. Reconcile — "Fix the gaps"

Based on audit findings, propose and execute fixes:

**For duplicate agents across targets:**
Choose a shared location (`.github/agents/`) so both targets see it, then remove
the target-specific copy.

**For lossy mappings (prompts with no CLI equivalent):**
Offer to create a corresponding `.claude/commands/<name>.md` with equivalent content
adapted for CLI context.

**For MCP drift:**
Offer to sync server definitions between `.vscode/mcp.json` (IDE) and
`~/.copilot/mcp-config.json` (CLI). Note: CLI has no standard repo-level MCP config
path — MCP is configured per-user or via `--additional-mcp-config` flag at runtime.

**For shared instruction files (CLAUDE.md, GEMINI.md read by all Copilots):**
Review the content for tool-specific instructions. Offer to:
- Add a note at the top: `<!-- Note: This file is read by Claude Code, Copilot IDE, and Copilot CLI -->`
- Split Claude-specific content into `.claude/rules/` (not read by Copilot) and keep
  only universal guidance in `CLAUDE.md`
- For `CLAUDE.local.md`: note it is read by Copilot IDE but not CLI

**For shadowed artifacts:**
Explain which version wins (scope precedence: user < repo < directory) and offer to
remove the shadowed version or rename it.

### 4. Modify — "Change a customization"

To modify an existing customization:

1. Read the target file
2. Parse frontmatter if present (YAML between `---` lines)
3. Make the requested change to frontmatter or body
4. Write back using the Edit tool (preserve existing formatting)

Common modifications:
- **Update agent tools list**: Edit the `tools:` array in frontmatter
- **Change instruction scope**: Modify or add `applyTo:` glob
- **Update skill description**: Edit the `description:` field
- **Add handoffs**: Add `handoffs:` entries to agent frontmatter
- **Change MCP server config**: Edit the server entry in the JSON file
- **Move an artifact**: Read from source, Write to destination, delete source

When modifying frontmatter, preserve the `---` delimiters and any fields you're not
changing. Be careful with YAML formatting — use the same style (quoted vs unquoted,
flow vs block) as the existing file.

### 5. Delete — "Remove a customization"

Before deleting, always:

1. **Show what will be removed** — display the file path and a summary of its content
2. **Check for references** — search for the artifact's name in other files:
   - Agent names referenced in `handoffs:`, `agents:`, `excludeAgent:`
   - Skill names referenced in agent tool lists
   - MCP server names referenced in `mcp-servers:`
3. **Confirm with the user** — deletion is not easily reversible outside of git
4. **Delete the file** using bash `rm`
5. **Clean up empty directories** if the deleted file was the only occupant
6. **Report what was deleted** and any dangling references found

For skill folders (`*/SKILL.md`), delete the entire skill directory, not just the
SKILL.md file.

## Reporting Format

When presenting discovery or audit results, use this structure:

```markdown
## Copilot Customization Inventory

### Guidance (N files)
| File | Target | Scope | Applied To |
|------|--------|-------|------------|

### Agents (N files)
| File | Name | Target | Scope | Tools |
|------|------|--------|-------|-------|

### Skills (N folders)
| Folder | Name | Target | Scope |
|--------|------|--------|-------|

### MCP Servers
| Config File | Target | Servers |
|-------------|--------|---------|

### Issues Found
- [severity] description
```

## Reference Files

Load these on demand — only when you need detailed path listings or schema info:

| File | When to read |
|------|-------------|
| `references/copilot-ide-paths.md` | Deep-dive into all IDE discovery paths |
| `references/copilot-cli-paths.md` | Deep-dive into all CLI discovery paths |
| `references/reconciliation.md` | Full conflict types, cross-read rules, and checklist |
| `references/frontmatter-schema.md` | Complete frontmatter field reference by artifact type |
