---
name: prompt-engineering
description: Create reusable skills and agent configurations through structured interview and template generation. Covers SKILL.md authoring, agent persona design, and structured output contracts. Use when creating a new skill, designing an agent, capturing a repeatable process, or when asked to "skillify" a workflow.
user-invocable: true
disable-model-invocation: true
---

# Prompt Engineering

CRITICAL: Check existing project conventions before inventing new ones. Read CLAUDE.md, `.claude/rules/`, and existing skills to align with what's already established.

## Skill Creation Workflow

### Step 1: Analyze the Session/Request

Before asking questions, analyze what you already know:
- What repeatable process was performed or requested
- What the inputs/parameters are
- The distinct steps in order
- Success criteria for each step
- Where the user steered or corrected during the session
- What tools and permissions are needed

### Step 2: Interview (4 Rounds)

Use structured questions. Don't over-ask for simple processes.

**Round 1 — High-Level Confirmation**
- Suggest a name and description. Ask to confirm or rename.
- Suggest goal(s) and specific success criteria.

**Round 2 — Details**
- Present the steps as a numbered list.
- Suggest arguments based on observed inputs.
- Ask: inline (current conversation) or forked (sub-agent with own context)?
  - Fork for self-contained tasks without mid-process user input
  - Inline when the user wants to steer mid-process
- Ask where to save:
  - **This repo** (`.claude/skills/<name>/SKILL.md`) — project-specific workflows
  - **Personal** (`~/.claude/skills/<name>/SKILL.md`) — follows you across repos

**Round 3 — Per-Step Breakdown**
For each major step, if not obvious:
- What does this step produce that later steps need?
- What proves this step succeeded?
- Should the user confirm before proceeding? (especially irreversible actions)
- Are any steps independent and could run in parallel?
- What are the hard constraints?

**Round 4 — Final**
- Confirm when the skill should be invoked. Suggest trigger phrases.
- Ask for gotchas or edge cases.

### Step 3: Write the SKILL.md

Use this template:

```markdown
---
name: {{skill-name}}
description: {{one-line description}}
allowed-tools:
  {{list of tool permission patterns}}
when_to_use: {{detailed invocation triggers with example phrases}}
argument-hint: "{{hint showing argument placeholders}}"
arguments:
  {{list of argument names}}
context: {{inline or fork — omit for inline}}
---

# {{Skill Title}}
Description of skill

## Inputs
- `$arg_name`: Description of this input

## Goal
Clearly stated goal with defined artifacts or completion criteria.

## Steps

### 1. Step Name
What to do. Be specific and actionable. Include commands when appropriate.

**Success criteria**: What proves this step is done.
```

### Per-Step Annotations

- **Success criteria** (REQUIRED on every step): What proves the step is done
- **Execution**: `Direct` (default), `Task agent` (subagent), or `[human]` (user does it)
- **Artifacts**: Data this step produces that later steps need
- **Human checkpoint**: When to pause and ask before proceeding (irreversible actions, error judgment)
- **Security constraints**: For steps handling user input, external APIs, or data storage, include explicit requirements (input sanitization, output encoding, auth checks). Reference `security-review` patterns for checklists.
- **Rules**: Hard constraints. User corrections from the reference session are especially useful here.

### Step Structure Tips
- Steps that can run concurrently use sub-numbers: 3a, 3b
- Steps requiring the user to act get `[human]` in the title
- Keep simple skills simple — a 2-step skill doesn't need annotations on every step

### Frontmatter Rules
- `allowed-tools`: Minimum permissions needed — least privilege. Use patterns like `Bash(gh:*)`, not blanket `Bash`. Grant only what the skill actually requires.
- `context`: Only set `context: fork` for self-contained skills
- `when_to_use`: CRITICAL — this tells the model when to auto-invoke. Start with "Use when..." and include trigger phrases
- `user-invocable: true` for skills the user triggers explicitly
- `disable-model-invocation: true` for sensitive skills that shouldn't auto-trigger

### Step 4: Review and Save

Show the complete SKILL.md to the user for review before writing. After saving, tell them:
- Where the skill was saved
- How to invoke it: `/{{skill-name}} [arguments]`
- That they can edit the SKILL.md directly to refine it

## Agent Creation Workflow

When designing a standalone agent (not a skill):

### 1. Extract Core Intent
Identify the fundamental purpose, responsibilities, and success criteria. Check CLAUDE.md for project-specific context the agent should align with.

### 2. Design Expert Persona
Create an identity with domain knowledge relevant to the task. Written in second person ("You are...", "You will...").

### 3. Architect Instructions
The system prompt should:
- Establish clear behavioral boundaries
- Provide specific methodologies for task execution
- Anticipate edge cases
- Include concrete examples
- Define output format expectations
- Build in self-verification steps

### 4. Create Identifier
- Lowercase letters, numbers, and hyphens only
- 2-4 words joined by hyphens
- Clearly indicates the agent's function
- Memorable and easy to type
- Avoid generic terms like "helper" or "assistant"

### Agent Output Format
```json
{
  "identifier": "descriptive-agent-name",
  "whenToUse": "Use this agent when... (include example triggers)",
  "systemPrompt": "Complete operational manual for the agent"
}
```

## Structured Output Contracts

When a skill or agent needs structured output, define the contract explicitly:

- **JSON**: Include the exact schema with field descriptions and required fields
- **Markdown**: Define section headers and what goes in each
- **XML tags**: Use `<analysis>`, `<summary>`, `<result>` for machine-parseable sections

Forced structured output (guaranteed schema with tool_choice or JSON mode) eliminates format drift at zero ongoing prompt cost.

CRITICAL REMINDER: Check existing conventions first. Interview before authoring. Every skill needs `when_to_use` and per-step success criteria. Show the result for review before saving.

## Related Skills

- Skills created here often invoke `codebase-exploration` and `code-verification` as sub-workflows.
- `task-orchestration` patterns inform how multi-step skills coordinate work.
- `safe-autonomous-mode` risk classification informs `allowed-tools` scoping.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Team conventions for skill naming and placement
- Required frontmatter fields for the project
- Default allowed-tools patterns
- Standard step annotations required by the team
