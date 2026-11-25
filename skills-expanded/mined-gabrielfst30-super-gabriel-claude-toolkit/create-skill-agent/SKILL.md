---
name: create-skill-agent
description: >
  Creates a new skill+agent combination from a workflow description. Use when
  the user wants to automate a new workflow, create a new slash command, build
  a new subagent, or design a skill+agent architecture for a recurring task.
  Trigger on phrases like "cria uma skill", "cria um agent", "cria skill+agent",
  "quero automatizar", "novo workflow", "nova skill", "novo agent", "create skill",
  "create agent", "build agent", "build skill", "new workflow".
user-invocable: true
argument-hint: [workflow description or name]
allowed-tools: Read, Write, Glob, Agent
---

# /create-skill-agent

Creates a well-structured skill+agent pair from a workflow description, following
the architecture formula.

## Reference

Always read `references/architecture-formula.md` before starting. It contains
the full decision tree, frontmatter specs, anti-patterns, and checklist.

---

## Flow

### Step 1 — Understand the workflow

If the user provided a name (e.g., `/create-skill-agent deploy-review`):
- Check if `developer/requests/$ARGUMENTS.md` exists and read it.
- Otherwise use `$ARGUMENTS` as the inline description.

Ask clarifying questions if the workflow is ambiguous:
- What triggers this? (user command, keyword, another skill?)
- What is the atomic unit of work? (one task or many?)
- Does it need to run CLI commands, write files, or only read?
- Are there steps that can run in parallel?

### Step 2 — Design the architecture

Read `references/architecture-formula.md` fully.

Map the workflow to layers:

```
1. How does it start? → Skill (user-invocable) or Agent (programmatic)
2. What decisions does it make? → Skill body (conditional logic)
3. What does it actually execute? → Agent(s)
4. What validates the result? → Validator agent (if needed)
```

Apply the decision tree from the formula doc to classify each part.

### Step 3 — Consult the architecture guardian

Use the `architecture-guardian` agent to check:
- Whether similar skills or agents already exist
- Which existing patterns apply
- Whether new agents overlap with existing ones

```
Agent(
  subagent_type: "architecture-guardian",
  prompt: "Check if any existing skill or agent in .claude/agents/ and .claude/skills/
           already covers this workflow: [workflow description].
           List overlapping agents/skills and recommend whether to create new ones
           or extend existing ones."
)
```

### Step 4 — Create the files

#### 4a. Create the skill

Create `.claude/skills/$ARGUMENTS/SKILL.md` using this template:

```yaml
---
name: [kebab-case name]
description: >
  [What it does + keywords that trigger it automatically.
  Be specific — vague descriptions cause missed matches.]
user-invocable: true          # remove if keyword-triggered only
argument-hint: [hint text]    # remove if no arguments needed
allowed-tools: [minimum set]  # always include Agent if spawning subagents
---

# /[name]

[One-line description of what this skill does.]

## Flow

### Step 1 — [First step]
[What to do, what to read, what to decide]

### Step 2 — [Second step]
[Conditions, branches, parallel vs sequential]

### Step N — Execute
Delegate to agents:
\`\`\`
Agent(subagent_type: "[agent-name]", prompt: "...")
\`\`\`

## Success Criteria
- [ ] [Testable outcome]
```

#### 4b. Create each agent

For each worker identified in the design, create `.claude/agents/[name].md`:

```yaml
---
name: [kebab-case name]
description: [What it does + when to invoke it. Used for automatic matching.]
model: haiku | sonnet | opus  # proportional to task complexity
allowed-tools: [absolute minimum]
---

You are the **[Role Name]**.

## Responsibilities
[What this agent does — one clear paragraph]

## Protocol
### 1. [First step]
### 2. [Second step]
### N. [Last step]

## Response Format
\`\`\`
[AGENT NAME] COMPLETE | FAILED | BLOCKED

[Structured output format]
\`\`\`
```

#### 4c. Create references (if needed)

If the skill requires codified patterns, create
`.claude/skills/$ARGUMENTS/references/` with supporting `.md` files.

Reference files contain **facts and patterns**, not workflow steps.

### Step 5 — Validate

Apply the checklist from `references/architecture-formula.md`:

**Skill check:**
- [ ] `name` is unique across `.claude/agents/` and `.claude/skills/`
- [ ] `description` includes specific keywords for auto-matching
- [ ] `allowed-tools` declared and includes `Agent` if it spawns subagents
- [ ] Workflow steps are numbered and unambiguous
- [ ] No CLI commands run directly in the skill (delegated to agents)

**Agent check (per agent):**
- [ ] Does exactly one thing
- [ ] `allowed-tools` is the minimum necessary
- [ ] `model` is proportional to complexity
- [ ] `description` is specific enough for automatic matching
- [ ] Response format is documented in the body

**Architecture check:**
- [ ] No upward layer invocation (agents don't call skills)
- [ ] Parallel execution identified where applicable
- [ ] Validator agent exists if the workflow modifies files or runs commands

### Step 6 — Output

```
SKILL+AGENT CREATED

Skill: .claude/skills/[name]/SKILL.md
  Trigger: /[name] [args] | keyword-triggered
  Spawns: [list of agents]

Agents created:
  .claude/agents/[agent-name].md — [one-line role]

References:
  .claude/skills/[name]/references/[file].md — [topic]

Architecture:
  User → /[name] → [agent-executor] → [agent-validator]

Next step: test by running /[name] [example-argument]
```

---

## Decision shortcuts

Simple workflow (one executor, no validation):
→ One skill + one agent. Skip validator.

Multiple parallel steps:
→ One skill (orchestrator) + one agent type (run multiple instances in parallel).

Modifies critical files or runs destructive commands:
→ Always add a validator agent and a confirmation step in the skill.

Similar agent already exists:
→ Extend its `description` with new keywords rather than creating a duplicate.
