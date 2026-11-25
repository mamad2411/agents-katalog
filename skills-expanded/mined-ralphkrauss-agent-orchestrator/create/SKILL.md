---
name: create-skill
description: Create a new skill in the correct cross-tool location with proper frontmatter, generic language, and sync. Use when user says "create skill", "new skill", "add skill", or wants to create a reusable workflow.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Create Skill

Create or update a reusable multi-step workflow skill that works across all AI coding tools (Claude Code, Codex, Cursor, OpenCode, Copilot).

## Instructions

### Step 1: Parse the Request

Extract from the user's input:
- **What** -- the workflow name and what it automates
- **When** -- trigger phrases users would say to invoke it
- **Steps** -- the multi-step process it guides

### Step 2: Determine If This Should Be a Skill

A skill is the right choice when ALL of these apply:
1. **Multi-step process** -- involves creating or modifying 3+ files in a coordinated way
2. **Repeatable** -- the workflow will be done more than once
3. **Specific file structure** -- files must go in specific locations with specific naming
4. **Easy to get wrong** -- skipping a step causes build failures or runtime errors

If the request is single-step knowledge, conceptual guidance, or reference material, tell the user it should be documentation (`docs/`) or a rule (`.agents/rules/`), not a skill. Point them to `/create-rule` for rules.

### Step 3: Check for Existing Skills

Search `.agents/skills/` for skills that already cover this workflow:

```
ls .agents/skills/
```

Read the `SKILL.md` of any skill that might overlap. Then:

- **Exact duplicate** -- already covered. Tell the user and stop.
- **Partial overlap** -- existing skill covers part of the workflow. Update the existing skill rather than creating a new one.
- **No overlap** -- genuinely new workflow. Proceed to Step 4.

### Step 4: Ask Diagnostic Questions (only when needed)

If the user's request is fully specified (name, workflow steps, file structure), skip to Step 5.

If scope is ambiguous, ask only the questions you cannot answer from context. One round maximum.

Useful diagnostic questions (pick the ones that matter):

- "What files does this workflow create or modify?"
- "Is this specific to one tool (Claude Code only) or should all AI tools support it?"
- "What are the trigger phrases users would say to invoke this?"
- "Does this depend on tool-specific features (MCP tools, subagents, dynamic context injection)?"

### Step 5: Write the Skill

Create the skill at `.agents/skills/{name}/SKILL.md`.

#### Naming

- Directory name: **kebab-case** (e.g., `scaffold-integration`, `add-migration`)
- `name` in frontmatter must match the directory name exactly
- No names containing "claude" or "anthropic"

#### Frontmatter

Required fields: `name` and `description` (optional: `compatibility`):

```yaml
---
name: skill-name-in-kebab-case
description: What it does. Use when user says "trigger phrase 1", "trigger phrase 2", or wants to [specific task].
---
```

Rules:
- `name`: 1-64 chars, lowercase letters + numbers + hyphens, no leading/trailing/consecutive hyphens
- `description`: 1-1024 chars, must include what the skill does AND when to use it (trigger phrases)
- No XML angle brackets (`<` `>`) in frontmatter values
- Add `compatibility: claude-code` only if the skill genuinely requires Claude Code-specific features (subagents, MCP tools, hooks). Most skills should be universal.

#### Body Structure

Follow this template:

```markdown
# Skill Title

Brief one-line description of what this skill does.

Read `path/to/relevant-doc.md` first -- context pointer.

## Instructions

### Step 1: ...
### Step 2: ...
### Step N: ...

## Critical Rules

- Rule 1
- Rule 2

## Checklist

- [ ] Step verified
- [ ] Step verified

## Reference

- `path/to/file.md` -- description
- `path/to/example/` -- reference implementation
```

#### Language Rules

Skills must use generic, tool-agnostic language because they are shared across all AI coding tools:

- **No tool-specific tool names**: Write "search the codebase for X" not `mcp__github__search_code` or `Grep`. Describe the action, not the tool.
- **No tool-specific delegation syntax**: Write "delegate this to a separate agent" not `Agent tool` or `subagent_type: developer`. Describe the intent.
- **No tool-specific file paths**: Write "the skill at `.agents/skills/create-rule/SKILL.md`" not "the skill at `.claude/skills/create-rule/SKILL.md`" -- the canonical location is `.agents/skills/`.
- **Exception**: If the skill genuinely requires Claude Code-specific features, add `compatibility: claude-code` to frontmatter and use Claude-specific syntax only inside `<!-- tool:claude -->` blocks.

#### Tool Blocks (when needed)

For content that applies to only one tool:

The syntax uses HTML comments with the tool name. For Claude-specific content, wrap it between an opening comment `tool:claude` and a closing comment `/tool:claude`. For Codex-specific content, use `tool:codex` and `/tool:codex`. The sync script keeps Claude blocks (stripping markers) and strips Codex blocks entirely. See existing skills like `build-context` or `review-pr` for working examples.

Most skills should be fully generic with no tool blocks.

#### Size Limit

Keep the SKILL.md under 250 lines. If the skill needs detailed reference material (code templates, API specs, long examples), move it to a `references/` subdirectory:

```
.agents/skills/my-skill/
  SKILL.md              # Under 250 lines
  references/
    template.md         # Detailed templates
    api-reference.md    # Specs, examples
```

Reference the files from SKILL.md: "See `references/template.md` for the full code template."

### Step 6: Run Sync

After creating or modifying any skill in `.agents/skills/`, run:

```
just ai-sync
```

This copies the skill to `.claude/skills/` (with tool-block processing for Claude Code). Other tools (Codex, Cursor, OpenCode, Copilot) read `.agents/skills/` directly -- no sync needed for them.

This step is mandatory. Do not skip it or leave it for the user.

### Step 7: Summarize

```
Action: {Created new skill | Updated existing skill}
Skill: .agents/skills/{name}/SKILL.md
Trigger phrases: "phrase 1", "phrase 2", ...
Cross-tool: {All tools | Claude Code only}
Sync: ran just ai-sync
```

## Critical Rules

- **Canonical location is `.agents/skills/`** -- never create skills directly in `.claude/skills/`, `.codex/skills/`, `.cursor/skills/`, or any other tool-specific directory. Those are generated copies.
- **Update before create** -- if an existing skill partially covers the workflow, update it rather than creating a new one.
- **Generic language by default** -- no tool-specific tool names or delegation syntax unless the skill has `compatibility: claude-code` and uses tool blocks.
- **Always run `just ai-sync`** -- the agent must run this, not defer it to the user.
- **Frontmatter is the discovery mechanism** -- the description must include trigger phrases because that is how tools decide when to activate the skill. A skill with a vague description will never be auto-loaded.

## Cross-Tool Reference

How each tool discovers skills:

| Tool | Primary path | Also scans | Sync needed? |
|------|-------------|------------|--------------|
| Claude Code | `.claude/skills/` | -- | Yes (`just ai-sync`) |
| Codex | `.agents/skills/` | parent dirs, `$HOME/.agents/skills/` | No |
| Cursor | `.agents/skills/` | `.cursor/skills/` | No |
| OpenCode | `.agents/skills/` | `.opencode/skills/`, `.claude/skills/` | No |
| Copilot/VS Code | `.agents/skills/` | `.github/skills/`, `.claude/skills/` | No |

## Checklist

- [ ] Confirmed this should be a skill (multi-step, repeatable, specific file structure)
- [ ] Searched existing skills for overlap
- [ ] Frontmatter has `name` (kebab-case, matches dir) + `description` (what + when, under 1024 chars)
- [ ] Body uses generic, tool-agnostic language
- [ ] SKILL.md is under 250 lines (reference material in `references/` if needed)
- [ ] Ran `just ai-sync`
