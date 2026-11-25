---
name: fabrico-creating-prompts
description: "Create custom slash commands (.claude/commands/*.md) for Claude Code. Provides templates, guidelines, and a structured process for building command files that trigger specific workflows, optionally delegating to the right subagent. Use when creating, reviewing, or updating .claude/commands/*.md files."
---

# Creating Prompts

Creates well-structured custom slash commands for Claude Code. Enforces a consistent pattern across all commands and ensures clear separation between command files, subagent definitions, and skills.

## Core Design Principles

<principles>

<separation-of-concerns>
A slash command (`.claude/commands/*.md`) defines WHAT workflow to execute. It must NOT define WHO the agent is.

- **Command** = workflow trigger, workflow steps, tool configuration, expected outcome (`.claude/commands/*.md` files)
- **Subagent** = behavior, personality, responsibilities, and problem-solving approach (`.claude/agents/*.md` files)
- **Skills** = reusable domain knowledge, step-by-step processes, templates (`.claude/skills/<name>/SKILL.md` files)

A command routes work to a subagent (via the Task tool) and configures the workflow context. The subagent's role, personality, and behavioral guidelines are defined exclusively in the subagent file. The command must never redefine, override, or contradict the subagent's identity.
</separation-of-concerns>

<workflow-focus>
A slash command is a **workflow trigger**. It must:

- Optionally DELEGATE to a **specific subagent** via the **Task** tool (`subagent_type: <subagent-name>`) when the workflow has a clear owner
- Describe the **workflow steps** Claude should follow for this specific task
- Define the **expected outcome** of the workflow
- Optionally restrict **tools** via the `allowed-tools` frontmatter field
- Optionally pick a **model** via the `model` frontmatter field (otherwise the command inherits the session model)

A command must NOT:

- Define or alter a subagent's personality, tone, or behavioral traits
- Duplicate instructions that belong in skills
- Duplicate coding standards or guidelines that belong in `CLAUDE.md` memory files
- Contain generic instructions that are not specific to the workflow
</workflow-focus>

<xml-syntax>
All structured content inside the command body MUST use XML-like tags for explicit structure. This ensures reliable parsing across all model tiers.

Use Markdown only for inline formatting (bold, code blocks, tables, lists) within XML sections.
</xml-syntax>

<minimal-scope>
A command should only describe what is necessary for the specific workflow it triggers. Delegate domain knowledge to skills, coding standards to `CLAUDE.md` memory, and behavioral guidelines to subagents.
</minimal-scope>

</principles>

## Creation Process

Use the checklist below and track your progress (the **TodoWrite** tool is useful here):

```
Creation progress:
- [ ] Step 1: Define the command's purpose
- [ ] Step 2: Decide whether to delegate to a subagent (and pick a model)
- [ ] Step 3: Determine tool requirements
- [ ] Step 4: Identify required skills
- [ ] Step 5: Design the workflow steps
- [ ] Step 6: Define output expectations
- [ ] Step 7: Assemble the command file using the template
- [ ] Step 8: Validate the command file
```

**Step 1: Define the command's purpose**

Answer these questions before writing anything:
- What specific workflow does this command trigger? (e.g., research a task, implement a feature, run e2e tests)
- What is the expected outcome? (e.g., a research document, implemented code, test suite)
- What inputs does the workflow require? (e.g., Jira ID, plan file, feature description) — these arrive via `$ARGUMENTS` (or `$1`, `$2`, …)
- Does this command extend or depend on another command?
- What makes this workflow distinct from existing commands?

**Step 2: Decide whether to delegate to a subagent (and pick a model)**

Decide if the workflow has a clear specialist owner:
- Review existing subagents in `.claude/agents/` to find one whose role aligns with the workflow
- If a subagent fits, the command should delegate to it via the **Task** tool (`subagent_type: <subagent-name>`) — add the delegation directive as the first line of the body. The command should not redefine the subagent's capabilities.
- If the workflow is generic and needs no specialist, omit delegation and write the steps for the main thread to follow.
- Optionally set the `model:` frontmatter field (`opus`, `sonnet`, or `haiku`) when the workflow's complexity warrants a specific tier; otherwise omit it and inherit the session model.

**Step 3: Determine tool requirements**

Decide if the command should restrict the tools Claude may use:
- By default, a command inherits the full Claude Code toolset (including all configured MCP servers). Omit `allowed-tools` unless you need to restrict.
- If the workflow should be limited to a specific set (e.g., a read-only review command), list them in the `allowed-tools` frontmatter field (e.g., `Read, Grep, Glob, Bash`).
- To allow a specific MCP server's tools, reference them by their `mcp__<server>__*` names (e.g., `mcp__context7__*`, `mcp__figma__*`, `mcp__playwright__*`).

**Step 4: Identify required skills**

Determine which skills the workflow depends on:
- Review existing skills in `.claude/skills/` to find relevant ones
- Each referenced skill provides domain knowledge the workflow relies on; reference it so Claude loads it before starting the workflow
- List skills with a brief explanation of why they are needed for THIS workflow
- Do not reference skills that are not directly used in the workflow steps

**Step 5: Design the workflow steps**

Outline the workflow as a numbered sequence:
- Each step should be a clear, actionable instruction
- Steps should reference skills and tools where appropriate
- Include decision points and branching logic if the workflow is not purely linear
- Include handoffs to other subagents (via the **Task** tool) or follow-up slash commands if the workflow spans multiple specializations
- Keep steps focused on WHAT to do, not HOW to think about it (the subagent's personality handles the how)

**Step 6: Define output expectations**

Specify the expected deliverables of the workflow:
- File name conventions and output locations
- Document structure or template to follow (reference skill templates where applicable)
- Summary format if the workflow produces a report
- Success criteria — how to know the workflow is complete
- This step is optional if the workflow outcome is self-evident (e.g., implemented code)

**Step 7: Assemble the command file using the template**

Use the `./prompt.template.md` template to assemble the final command file. Place the file in `.claude/commands/` with a descriptive kebab-case filename and the `fabrico-` prefix (e.g., `fabrico-research.md`, `fabrico-implement-ui.md`). The command is then invoked with its slash form (e.g., `/fabrico-research`, `/fabrico-implement-ui`). Commands can also be scoped globally by placing them in `~/.claude/commands/`.

**Step 8: Validate the command file**

Verify the command file against this checklist:
- [ ] YAML frontmatter is valid and parseable
- [ ] `description` field is present and concise (shown in the `/` menu)
- [ ] `argument-hint` field (if present) describes what the user passes
- [ ] If the command delegates, the delegation directive names an existing subagent in `.claude/agents/` and uses the **Task** tool (`subagent_type: <subagent-name>`)
- [ ] `allowed-tools` field (if present) lists only the tools the workflow needs
- [ ] `model` field (if present) is one of `opus`, `sonnet`, `haiku`
- [ ] All skills referenced in `Required Skills` section exist in `.claude/skills/`
- [ ] XML-like tags are properly opened and closed
- [ ] No subagent personality or behavioral instructions are embedded (those belong in `.claude/agents/*.md`)
- [ ] No coding standards or guidelines are embedded (those belong in `CLAUDE.md`)
- [ ] No skill content is duplicated (reference skills, don't copy them)
- [ ] Workflow steps are clear, sequential, and actionable
- [ ] The command is distinct from existing commands and does not duplicate their workflows
- [ ] If the command extends another command, the dependency is explicitly stated

## Command File Structure Reference

### Frontmatter Fields

| Field | Required | Description |
|---|---|---|
| `description` | **Yes** | A short description of what the command does. Shown in the `/` menu. |
| `argument-hint` | No | Hint text shown in the `/` menu to guide the user on what to provide (e.g., `[Jira ID or task description]`). |
| `allowed-tools` | No | A comma-separated list of tools the command is permitted to use. If omitted, the command inherits the full Claude Code toolset (including MCP servers). Reference MCP tools as `mcp__<server>__*`. |
| `model` | No | The model used when running the command (`opus`, `sonnet`, or `haiku`). If omitted, the command inherits the current session model. |

> **Delegation, not an `agent:` field.** Claude Code commands do not have an `agent` frontmatter field. To route a workflow to a specialist, put a delegation directive at the top of the command body that launches the subagent with the **Task** tool (`subagent_type: <subagent-name>`). See the template for the exact wording.

### Body Sections

| Section | Required | Purpose |
|---|---|---|
| Delegation directive | No | First line of the body when the workflow has a subagent owner: launch it via the **Task** tool. |
| Goal statement | **Yes** | 1-2 paragraphs describing what the command accomplishes and the expected outcome. |
| `<prerequisites>` | No | Dependencies on other commands or files that must be completed first. |
| `<input-requirements>` | No | Describes what context or inputs the workflow needs to start (often arriving via `$ARGUMENTS`). |
| Required Skills | **Yes** | Skills to load before starting the workflow, with brief rationale for each. |
| Workflow | **Yes** | Numbered steps defining the workflow sequence. |
| `<output-specification>` | No | File naming, document structure, summary format, or success criteria. |
| `<handoff>` | No | Follow-up subagent (via the **Task** tool) or slash command to run at the end of the workflow. |
| `<constraints>` | No | Workflow-specific limitations, anti-patterns, or scope boundaries. |

## XML Syntax Guidelines

All body content in the command file must use XML-like tags for structure. Rules:

1. Every section uses a matching opening and closing tag: `<section-name>` ... `</section-name>`
2. Tags use lowercase-kebab-case naming
3. Nesting is allowed for sub-sections
4. Markdown formatting (bold, lists, tables, code blocks) is used inside XML tags for content
5. Avoid XML attributes for structural content — use nested tags or Markdown content instead. Exception: identifier attributes (e.g., `<tool name="...">`) are acceptable when they improve readability.

## Arguments Reference

Slash commands receive the user's input through argument placeholders that Claude Code substitutes at runtime. Use them to make commands operate on dynamic input:

| Placeholder | Description |
|---|---|
| `$ARGUMENTS` | The full argument string the user passed after the slash command (e.g., everything after `/fabrico-research`). |
| `$1`, `$2`, `$3`, … | Individual positional arguments, split on whitespace. Use these when the command expects multiple discrete inputs. |

Place a brief line like `The request: $ARGUMENTS` near the top of the body when the command clearly operates on user input. Use the `argument-hint` frontmatter field to tell the user what to provide.

> **Note on dynamic editor context.** Unlike VS Code prompt variables, Claude Code commands do not resolve `${file}`/`${selection}`/`${workspaceFolder}`-style editor variables. To reference workspace files, name the path directly in the workflow (Claude reads it with the **Read** tool), or have the user pass it as an argument. You can also embed shell output by prefixing a body line with `!` to run a Bash command and inline its result, or reference a file's contents with `@path/to/file`.

## Connected Skills

- `fabrico-creating-agents` - to understand subagent patterns and ensure commands don't overlap with subagent responsibilities
- `fabrico-creating-skills` - to ensure this skill's own structure follows the canonical skill creation requirements
- `fabrico-technical-context-discovering` - to understand existing command patterns and project conventions before creating a new one
- `fabrico-codebase-analysing` - to analyze existing commands and identify patterns to follow
- `fabrico-creating-instructions` - to understand when coding standards belong in `CLAUDE.md` memory files rather than command definitions
