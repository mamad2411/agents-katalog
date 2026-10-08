---
name: task-to-skill
description: Convert a completed user-requested task into a reusable Cursor skill by retrospecting what was done, identifying variable inputs, and generating a generic but precise SKILL.md. Use when the user asks to create a skill from work already completed in the current chat.
---

# Task to Skill

Turn completed execution into a reusable skill.

## When to Use

Use this after the agent has already completed a concrete task in the current chat and the user asks to "make a skill from this."

## Outputs

Create:
- a global skill copy at `~/.cursor/skills/<skill-name>/SKILL.md`
- a repo copy at `pm-agentic-engineering/skills/cursor_<skill-name>/SKILL.md`

Then push the repo copy using GitHub MCP.

## Workflow

### 1) Retrospect completed work

Summarize exactly what was done:
- objective
- key steps performed
- tools used
- outputs produced
- edge cases/errors handled

Share this summary with the user before writing the new skill.

### 2) Extract variables vs constants

Classify workflow inputs:
- **Variables**: inputs likely to change between runs (branches, URLs, labels, IDs, org/repo, envs).
- **Constants**: stable policy/process steps.

For each variable, decide default behavior:
- ask every time
- optional default with confirmation
- fixed value only if user explicitly requests it

### 3) Confirm design choices

Before finalizing SKILL.md, confirm:
- skill name
- trigger scenarios
- variable handling strategy
- required confirmations before destructive actions

If user gives no preference, default to safe prompts for variable values.

### 4) Author the skill

Write concise SKILL.md with:
- YAML frontmatter (`name`, `description`)
- clear purpose
- required tools
- step-by-step workflow
- explicit confirmation checkpoints
- error handling rules
- output format template
- one concrete example based on the completed task pattern

Keep it generic enough for reuse, but specific enough to execute reliably.

### 5) Save to both locations

1. Global: `~/.cursor/skills/<skill-name>/SKILL.md`
2. Repo: `pm-agentic-engineering/skills/cursor_<skill-name>/SKILL.md`

Repo naming rule:
- if Cursor-specific format/instructions are used, prefix repo copy folder with `cursor_`.

### 6) Push repo copy

Use GitHub MCP (not CLI push) to commit/push the repo skill file.

Return:
- file paths created
- commit SHA / repo URL
- short note on variable prompts included in the generated skill

## Required Safety Pattern in Generated Skills

Generated skills should always instruct agents to:
- show a plan first for multi-target operations
- request approval before irreversible or external-write operations
- continue batch operations even when one target fails
- report created / skipped / failed outcomes separately

## Template for Generated Skills

Use this structure when generating new skills:

```markdown
---
name: <kebab-case-name>
description: <what + when, in third person>
---

# <Title>

## Purpose
<what this automates>

## Inputs to Collect
- <variable 1>
- <variable 2>

## Workflow
1. <retrospected step converted to reusable instruction>
2. <...>

## Confirmation Checkpoints
- <what to confirm before writes>

## Error Handling
- <expected error class> -> <action>

## Output Format
<created/skipped/failed template>

## Example
<short example run>
```

## Example Scenario

Completed task:
- "Create release PRs from a Confluence checklist."

Generated skill should:
- ask for checklist URL
- extract repos
- ask/confirm source and target branches
- ask/confirm title pattern
- run PR creation in parallel
- return PR links and failures
