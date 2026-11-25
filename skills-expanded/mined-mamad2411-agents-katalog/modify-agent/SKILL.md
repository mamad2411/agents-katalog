---
name: modify-agent
description: 'Modify an existing Claude Code custom subagent. Use when user wants to edit, update, refactor, or change an agent at any scope (project, user, plugin).'
argument-hint: [agent-name] [modification-description]
disable-model-invocation: true
---

# Modify Existing Claude Code Subagent

You are modifying an existing Claude Code custom subagent. Follow all phases sequentially.

For agent structure reference, frontmatter fields, description patterns, and prompt template, refer to `../create-agent/references/agent-guide.md`.

---

## Phase 1: Discover Agents

If `$1` is provided, search for an agent matching that name. Otherwise, discover all available agents.

Scan these locations using Glob for `*.md`:

1. **Project-level**: `.claude/agents/` in current working directory
2. **User-level**: `~/.claude/agents/`
3. **Plugin-level**: Check for `.claude-plugin/marketplace.json` or `.claude-plugin/plugin.json` in CWD and parents, then scan `<plugin-root>/agents/`

For each discovered agent, extract from frontmatter:
- `name`, `description`, scope (project/user/plugin), file path

If `$1` matches exactly one agent, auto-select it. If multiple matches or no argument, use AskUserQuestion to present the list and let user choose.

---

## Phase 2: Analyze Selected Agent

Thoroughly analyze the target agent before any modification:

1. **Read the agent file** — parse all frontmatter fields and full system prompt content
2. **Map frontmatter** — list every field and its current value
3. **Analyze system prompt** — identify structure (XML tags, sections), workflow steps, constraints, output format
4. **Identify issues** — validate against `../create-agent/references/agent-guide.md`:
   - Is the description action-oriented with proper trigger phrases?
   - Are prompt sections well-structured with XML tags?
   - Are workflow steps specific about HOW, not just WHAT?
   - Are constraints explicit?
   - Are there edge cases not handled?

Present a summary to user:
- Agent name, scope, file path
- All frontmatter fields and values
- System prompt structure overview
- Issues or improvement opportunities found

**Proactively suggest improvements** — don't just report what exists, recommend what could be better.

---

## Phase 3: Determine Modifications

If `$2` (or remaining arguments after agent name) describes the modification, use that as the starting point. Otherwise, use AskUserQuestion extensively to collect what the user wants to change.

Common modification types:
- **Frontmatter changes** — name, description, model, permissionMode, tools, memory, color, hooks
- **System prompt changes** — rewrite role, update workflow, add/remove constraints, change output format
- **Capability changes** — tool access, MCP servers, skills preloading
- **Runtime changes** — model selection, permission mode, max turns, background, isolation
- **Scope migration** — move agent between project/user/plugin levels
- **Hook changes** — add/edit/remove lifecycle hooks

For each requested change, assess risk and **deeply challenge risky decisions**:

**Challenge the user when:**
- Removing workflow steps or constraints from the system prompt
- Changing scope (may affect availability)
- Enabling `bypassPermissions` or `dontAsk` permission modes
- Removing tool restrictions (expanding from limited to full access)
- Changing model to a less capable one for complex tasks
- Enabling `background` or `isolation` without clear justification
- Adding `PROACTIVELY` or `ALWAYS` to description (auto-invocation implications)
- Removing memory configuration (data loss)

For risky changes, explain the impact and propose alternatives before proceeding.

---

## Phase 4: Plan Changes

Design the specific modifications:

1. List every change to apply
2. For frontmatter changes, show **before → after** values
3. For system prompt changes, describe structural impact
4. For new capabilities (hooks, MCP servers), outline configuration
5. Flag risky combinations (e.g., `bypassPermissions` + broad tool access)

**IMPORTANT**: If modifications require domain knowledge (library APIs, framework patterns), use Context7 MCP to fetch current documentation.

Present the change plan to user using AskUserQuestion. Include:
- Summary of all planned changes
- Before → after for each frontmatter field change
- Risk assessment for risky changes
- Recommendation if applicable

Do NOT proceed until user approves the plan.

---

## Phase 5: Apply Changes

Execute the approved modifications:

1. **Edit the agent file** using the Edit tool (prefer targeted edits over full rewrites)
2. **For scope migration**:
   - Copy agent file to new location
   - Update any path-dependent references
   - Confirm deletion of old file with user
3. **Self-review as prompt engineer** before finalizing:
   - Is the description specific enough for auto-invocation (if intended)?
   - Is the system prompt unambiguous?
   - Are workflow steps specific about HOW?
   - Are constraints clear about what NOT to do?
   - Is the output format well-defined?
   - Fix any issues found during self-review

---

## Phase 6: Validate & Review

After applying changes:

1. **Read the modified agent file** in full
2. **Validate against criteria** from `../create-agent/references/agent-guide.md`:
   - All required frontmatter fields present (`name`, `description`)
   - Description follows action-oriented pattern with trigger context
   - System prompt uses XML tags for structure
   - Workflow has specific HOW instructions
   - No broken or inconsistent references
3. **Present a diff summary** — show what changed (before/after)
4. **Ask user** using AskUserQuestion:
   - `Looks good` — confirm completion
   - `I have feedback` — collect feedback, revise, and present again
   - `Revert changes` — undo modifications (if possible via git)

Remind user to:
- Test with `/agents` command to verify agent still appears correctly
- Try invoking the agent to verify modified behavior
- For plugin-level agents: test with `claude --plugin-dir <plugin-root>`
- Iterate on the prompt based on results
