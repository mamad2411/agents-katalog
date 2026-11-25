---
name: fabrico-creating-agents
description: "Create custom subagents (.claude/agents/*.md) for Claude Code. Provides templates, guidelines, and a structured process for building subagent definitions that describe behavior, personality, responsibilities, and problem-solving approaches. Use when creating, reviewing, or updating Claude Code subagent files."
---

# Creating Agents

Creates well-structured custom subagents for Claude Code. Enforces a consistent pattern across all subagents and ensures clear separation between subagent definitions, skills, and slash commands.

## Core Design Principles

<principles>
<separation-of-concerns>
A subagent file (`.claude/agents/<name>.md`) defines WHO the agent is. It must NOT define HOW specific workflows are executed.

- **Subagent** = behavior, personality, responsibilities, and problem-solving approach
- **Skills** = reusable workflows, domain knowledge, step-by-step processes (`.claude/skills/<name>/SKILL.md` files)
- **Commands** = task triggers, workflow starters, reusable slash-command templates (`.claude/commands/*.md` files)

Every subagent is designed to be extendable with skills and commands. The subagent itself provides the foundation; skills and commands layer on top for specific workflows.
</separation-of-concerns>

<xml-syntax>
All structured content inside the subagent body MAY use XML-like tags for explicit structure. This makes the system prompt easier to parse reliably and keeps sections clearly delimited.

Use Markdown for inline formatting (bold, code blocks, tables, lists) within sections. The subagent body is the system prompt that Claude adopts when the subagent runs, so write it as clear natural-language instructions, not as configuration.
</xml-syntax>

<minimal-scope>
A subagent should only describe what is necessary for its specific role. Avoid duplicating instructions that belong in skills or in project-level memory (`CLAUDE.md` files).
</minimal-scope>
</principles>

## Creation Process

Use the checklist below and track your progress:

```
Creation progress:
- [ ] Step 1: Define the subagent's purpose
- [ ] Step 2: Write the subagent role and responsibilities
- [ ] Step 3: Determine tools and write tool usage guidelines
- [ ] Step 4: Determine skills and write skills usage guidelines
- [ ] Step 5: Configure next steps / handoffs (if applicable)
- [ ] Step 6: Add domain standards (if applicable)
- [ ] Step 7: Add constraints (if applicable)
- [ ] Step 8: Assemble the subagent file using the template
- [ ] Step 9: Validate the subagent file
```

**Step 1: Define the subagent's purpose**

Answer these questions before writing anything:
- What specific role does this subagent fulfill? (e.g., architect, reviewer, engineer)
- What problems does it solve?
- What is the subagent's primary focus area?
- Which other subagents does it collaborate with?
- What makes this subagent distinct from existing subagents?

**Step 2: Write the subagent role and responsibilities**

Write the `<agent-role>` section. This is the core of the subagent. It must describe:
- A clear role statement starting with "Role: You are..."
- The subagent's primary responsibilities and focus areas
- The subagent's behavioral guidelines (how it approaches work)
- Skip-level instructions for skill and tool usage (always check skills first, always use tools to gather context)

Follow the pattern from existing subagents. Keep the role focused. Do not include workflow-specific steps — those belong in skills.

The `description` frontmatter field is critical: Claude Code uses it to auto-route work to the right subagent. Write it action-oriented (e.g., "Use this subagent when reviewing code for security issues..."), so the main thread knows when to delegate via the Task tool.

**Step 3: Determine tools and write tool usage guidelines**

By default, a subagent inherits the FULL Claude Code toolset (Read, Edit, Write, Bash, Grep, Glob, TodoWrite, Task, WebFetch, WebSearch) plus every configured MCP server. Only set the `tools` frontmatter field when you want to RESTRICT access:
- Omit `tools` for most subagents so they inherit everything.
- For read-only subagents (pure reviewers that must not edit), explicitly list a restricted set, e.g. `tools: Read, Grep, Glob, Bash, Task, TodoWrite, WebFetch, WebSearch`. Note: MCP wildcard entries are not supported in `tools` — list the concrete tools you need.
- For each tool the subagent relies on, write a `<tool>` entry in the `<tool-usage>` section describing:
  - **MUST use when**: Specific conditions requiring tool use
  - **IMPORTANT**: Configuration notes, prerequisites, or behavioral constraints
  - **SHOULD NOT use for**: Anti-patterns and out-of-scope usage

Match tool guidance to the subagent's responsibilities. Read-only subagents should not be told to use the Edit/Write tools. Implementation subagents need the Bash tool for execution.

**Step 4: Determine skills and write skills usage guidelines**

Review available skills and select those the subagent should load:
- For each skill, write a short entry explaining WHEN to use it
- Use the format: `skill-name` - brief description of when to use it

Do not duplicate skill content in the subagent file. The subagent only references skills.

**Step 5: Configure next steps / handoffs (if applicable)**

Claude Code subagents do not have a structured `handoffs` frontmatter field. Instead, fold handoff intent into the body as a `## Next Steps / Handoffs` section:
- Describe when the subagent's work is complete.
- Suggest the slash command to run next (e.g., "When done, suggest running `/fabrico-review`").
- Or suggest handing off to another subagent (e.g., "Delegate follow-up to the `fabrico-architect` subagent via the Task tool").
- These are suggestions surfaced to the user or main thread — they typically require user approval before the next step runs.

**Step 6: Add domain standards (if applicable)**

If the subagent's role requires enforcing domain-specific standards (e.g., testing conventions, security rules, UI patterns), add a `<domain-standards>` section. This section is optional and should only appear when the subagent genuinely needs domain-specific rules that are NOT covered by skills.

**Step 7: Add constraints (if applicable)**

If the subagent has specific limitations or anti-patterns to avoid, add a `<constraints>` section. Common constraints include:
- What the subagent must NOT produce (e.g., "don't create implementation plans")
- Scope boundaries (e.g., "don't provide deployment instructions")
- Delegation rules (e.g., "escalate architectural decisions to the architect")

**Step 8: Assemble the subagent file using the template**

Use the `./agent.template.md` template to assemble the final subagent file. Place the file in `.claude/agents/` with the naming convention `<agent-name>.md` (for example, `.claude/agents/fabrico-software-engineer.md`). Use `~/.claude/agents/` instead for a global, user-level subagent.

**Step 9: Validate the subagent file**

Verify the subagent file against this checklist:
- [ ] YAML frontmatter is valid and parseable
- [ ] `name` is present and exactly equals the filename without the `.md` extension
- [ ] `description` is present, concise, and action-oriented so Claude auto-routes to it
- [ ] `model` is set to one of `opus`, `sonnet`, or `haiku` (or omitted to inherit the session model)
- [ ] `tools` is omitted (inherits full toolset) OR explicitly restricted for read-only subagents
- [ ] If `tools` is restricted, every tool relied on in `<tool-usage>` is actually listed
- [ ] All skills referenced in `<skills-usage>` are existing skills in the project
- [ ] XML-like tags (if used) are properly opened and closed
- [ ] No workflow-specific instructions are embedded (those belong in skills)
- [ ] No coding standards are embedded (those belong in `CLAUDE.md`)
- [ ] Subagent role is focused and distinct from existing subagents
- [ ] Any suggested handoffs target valid subagent names or slash commands

## Subagent File Structure Reference

### Frontmatter Fields

| Field | Required | Description |
|---|---|---|
| `name` | **Yes** | The subagent identifier. Must exactly equal the filename without `.md`. Used as `subagent_type` when launching via the Task tool. |
| `description` | **Yes** | Action-oriented description of when to use the subagent. Claude Code reads this to auto-route delegated work. |
| `tools` | No | Comma-separated list of allowed tools. OMIT to inherit the full toolset (including all MCP servers). Set only to RESTRICT (e.g., read-only reviewers). MCP wildcards are not supported. |
| `model` | No | Model tier for the subagent: `opus`, `sonnet`, or `haiku`. Omit to inherit the session model. |

> Note: Claude Code subagents do NOT support `handoffs`, `agents`, `argument-hint`, `user-invokable`, or `disable-model-invocation` fields. Auto-invocation is governed by the `description`; handoffs are expressed in the body.

### Body Sections

| Section | Required | Purpose |
|---|---|---|
| `<agent-role>` | **Yes** | Role definition, responsibilities, behavioral guidelines. |
| `<skills-usage>` | **Yes** | List of skills the subagent uses with guidance for each. |
| `<tool-usage>` | **Yes** | Tool access rules and usage guidelines per tool. |
| `<domain-standards>` | No | Domain-specific standards and rules the subagent enforces. |
| `<collaboration>` | No | Interaction patterns with other subagents or team members. |
| `<constraints>` | No | Explicit limitations and anti-patterns for the subagent. |
| `<next-steps>` | No | Suggested follow-up slash commands or subagent handoffs when work is complete. |
| `<output-format>` | No | Expected structure or format of the subagent's deliverables. |

## XML Syntax Guidelines

Body content in the subagent file may use XML-like tags for structure. When you do, follow these rules:

1. Every section uses a matching opening and closing tag: `<section-name>` ... `</section-name>`
2. Tags use lowercase-kebab-case naming
3. Nesting is allowed for sub-sections: `<tool>` inside `<tool-usage>`
4. Markdown formatting (bold, lists, tables, code blocks) is used inside the tags for content
5. Avoid XML attributes for structural content — use nested tags or Markdown content instead. Exception: identifier attributes (e.g., `<tool name="...">`) are acceptable when they improve readability.

Example structure:
```xml
<agent-role>
Role: You are a...
</agent-role>

<tool-usage>
<tool name="Bash">
- **MUST use when**: ...
- **SHOULD NOT use for**: ...
</tool>
</tool-usage>
```

## Connected Skills

- `fabrico-creating-prompts` - to understand how slash commands reference subagents and ensure subagents don't overlap with command responsibilities
- `fabrico-creating-skills` - to ensure this skill's own structure follows the canonical skill creation requirements
- `fabrico-technical-context-discovering` - to understand existing subagent patterns in the project before creating a new one
- `fabrico-codebase-analysing` - to analyze existing subagents and identify patterns to follow
- `fabrico-creating-instructions` - to understand when coding standards and project conventions belong in `CLAUDE.md` memory files rather than subagent definitions
