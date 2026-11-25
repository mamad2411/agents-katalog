---
name: agent-builder
description: Use when editing sub-agents, optimizing agent configuration, auditing agent quality, troubleshooting agent issues, or when someone says "improve this agent", "what's wrong with this agent", "help me tune this agent", "audit my agents", or wants to understand how their agents work. Also use when someone asks about agent settings, configuration, or best practices. Use proactively when the user is working on agent files.
---

## What This Skill Does

Helps edit, optimize, and audit Claude Code sub-agents through a conversational workflow. The user describes what they want in plain language. This skill translates their answers into the correct technical configuration.

For creating new agents from scratch, use the `/agents` command in Claude Code. This skill picks up after creation -- making agents better, fixing issues, and tuning configuration.

For the complete technical reference on all frontmatter fields and advanced patterns, see [reference.md](reference.md).

---

## Core Principle

**The user describes what they want. You figure out the config.**

Never expose raw frontmatter field names to the user. Instead of saying "I'll set permissionMode to acceptEdits", say "I'll configure it so this agent can edit files without asking you first." The user doesn't need to know the technical implementation -- they need to know what changes and why.

---

## Workflow

### Step 1: Identify the Target

Figure out which agent(s) the user wants to work on:

- If they name a specific agent, read its file from `.claude/agents/`
- If they have an agent file open in their editor, use that
- If they say "audit all my agents", read all `.md` files in `.claude/agents/`
- If unclear, ask: "Which agent do you want to work on?"

Read the agent file(s) completely before proceeding.

### Step 2: Understand the Agent's Job

Before suggesting any changes, you need to be 95% confident you understand what this agent is supposed to do. Ask plain-language questions to fill gaps in your understanding. Skip questions you can already answer from reading the agent file.

Group related questions together. Don't run a 20-question interrogation -- ask 2-4 questions max per round, and only ask what you genuinely can't infer.

**Question Bank** (ask only what's needed):

Purpose & Scope:
- "What's the main job of this agent in one sentence?"
- "Who calls this agent -- you directly, or does another skill trigger it?"
- "Does it do one focused thing, or handle multiple types of tasks?"

Capabilities:
- "What does this agent need to access? Files? The internet? Run scripts?"
- "Should it be able to create or edit files, or is it read-only?"
- "Does it need to talk to any external services or APIs?"

Autonomy & Safety:
- "Should it be able to make changes without asking, or should it check with you first?"
- "Is there anything this agent should never be allowed to do?"
- "How much do you trust it to run on its own -- a lot, or should it stay on a short leash?"

Performance:
- "Is this a quick task (under a minute) or a deep research job (several minutes)?"
- "Should it run in the background while you keep working, or do you need the results before moving on?"
- "Would it help if this agent remembered things from previous sessions -- like patterns it discovers or mistakes it learns from?"

Quality:
- "Is this agent performing well right now? What's not working?"
- "Are there specific situations where it fails or gives bad results?"
- "Is it being used when it shouldn't be, or not being used when it should?"

### Step 3: Run the Audit (Internal)

Run this checklist silently. Do NOT dump the raw checklist on the user. Findings get translated into plain-language recommendations in Step 4.

**Frontmatter Check:**
- Does `name` match the filename (minus .md)?
- Is `description` detailed enough for Claude to know when to delegate? Does it include trigger contexts, not just what the agent does?
- Is `model` explicitly set? (Project convention: always set, usually `sonnet`)
- Are `tools` explicitly listed? (Project convention: never rely on inheritance)
- Is `maxTurns` set? Is it appropriate for the task complexity?
- Are there unnecessary fields set that add no value?
- Would any optional fields help? (color, memory, background, isolation)

**Content Check:**
- Does it start with a clear identity/role statement?
- Are there structured sections (process, output format, guidelines)?
- Are process steps numbered and specific?
- Is the output format defined with a template or example?
- Do guidelines cover edge cases and what NOT to do?
- Are file paths absolute? (Agents can run from unknown working directories)
- Are script commands using the correct interpreter path?

**Tool Check:**
- Does the agent have tools it doesn't actually use? (Has Write but never writes anything)
- Is it missing tools it needs? (Runs scripts but no Bash listed)
- Could any tools be swapped for a denylist approach instead?

**Integration Check:**
- Is this agent registered in CLAUDE.md under Active Agents?
- Do skills that call this agent reference it by the correct name?
- If it uses memory, does the memory directory exist?
- If it runs scripts, are the script paths valid?
- If it uses API keys, does it read them from `.env`?

**Performance Check:**
- Could `maxTurns` be reduced without breaking the workflow?
- Could the model be cheaper? (opus -> sonnet, sonnet -> haiku for read-only work)
- Would running in the background improve the user's experience?
- Would persistent memory help this agent get better over time?
- Would an isolated worktree prevent unintended file changes?
- Is the description "pushy" enough for reliable triggering?

### Step 4: Present Recommendations

Translate audit findings into plain language. Organize by priority.

Format:

```
## What I'd Change

### High Priority
- [Plain language: what's wrong, why it matters, what the fix does]

### Nice to Have
- [Optional improvements with clear benefit explained]

### Looks Good
- [Things already well-configured -- briefly note what's working]
```

Then ask: "Want me to make these changes?"

If doing a multi-agent audit, give a brief summary per agent with a table showing the key findings, then offer to dive deeper into any specific agent.

### Step 5: Apply Changes

Edit the agent file with the user's approval. After making changes, briefly explain what was changed in plain language. Example: "I tightened up which tools this agent can use -- it was set to access the internet but never actually needs it, so I removed that to keep it focused."

After edits, update CLAUDE.md if any agent metadata changed (description, model, tools).

---

## Translation Rules

Use these mappings to convert plain-language answers into the correct technical configuration. The user never sees these field names -- you apply them silently.

### Tools Mapping
- "Just reads files / looks through code" -> tools: Read, Grep, Glob
- "Runs scripts or commands" -> add Bash
- "Needs to search the web" -> add WebSearch, WebFetch
- "Creates or edits files" -> add Write, Edit
- "Talks to [specific MCP service]" -> add to mcpServers
- "Should never [specific action]" -> add to disallowedTools

### Complexity -> maxTurns
- Quick lookup, single-step task -> 5-10
- Run a script, format output, moderate analysis -> 10-15
- Multi-source research, API scraping with fallbacks -> 15-20
- Deep multi-step work, intelligence gathering -> 20-25

### Autonomy -> permissionMode
- "Check with me before doing anything risky" -> default (or omit)
- "Let it edit files freely" -> acceptEdits
- "It should never do anything I haven't explicitly allowed" -> dontAsk
- "It should only look at things, never change anything" -> plan

### Memory -> memory scope
- "Remember things across all my projects" -> memory: user
- "Remember things specific to this project (share with team)" -> memory: project
- "Remember things specific to this project (just for me)" -> memory: local
- "Doesn't need to remember anything" -> omit memory field

### Execution -> background / isolation
- "Run while I keep working" -> background: true
- "I need the results before I can continue" -> background: false (default)
- "Should work on its own copy of the code" -> isolation: worktree

### Model Selection
- Read-only analysis, simple lookups, code search -> haiku
- Most tasks, good balance of quality and speed -> sonnet
- Complex reasoning, nuanced analysis, creative work -> opus
- "Use whatever I'm using" -> inherit (default)

---

## Smart Defaults by Agent Type

When the user describes what their agent does, use this table to suggest an initial configuration. These are starting points -- adjust based on the conversation.

| What the Agent Does | Model | Turns | Key Tools | Memory |
|---------------------|-------|-------|-----------|--------|
| Fetches data by running a script | sonnet | 10-15 | Bash, Read, Grep, Glob | No |
| Researches topics on the web | sonnet | 15-20 | Read, Grep, Glob, WebSearch, WebFetch | No |
| Scrapes APIs or external services | sonnet | 15-20 | Bash, Read, WebSearch, WebFetch | Optional |
| Plans content (pure reasoning) | sonnet | 5-10 | None or Read only | No |
| Reads and analyzes code | haiku | 10-15 | Read, Grep, Glob | No |
| Generates or edits files | sonnet | 15-25 | Read, Write, Edit, Bash, Grep, Glob | No |
| Gathers intelligence over time | sonnet | 20-25 | Bash, Read, Grep, Glob, WebSearch, WebFetch, Write, Edit | project |

---

## Project Conventions

Agents in this project follow these patterns. Enforce them during audits:

- Agent files live in `.claude/agents/[agent-name].md` (single file, not a directory)
- All agents explicitly set `model` (usually `sonnet`)
- Tools are always explicitly listed (never rely on inheritance)
- Agent descriptions use full sentences explaining what the agent does and when to use it
- Agent body follows this structure: identity statement -> process/workflow -> output format -> guidelines/rules
- File paths in agent instructions use forward slashes and are absolute
- Python path: `/c/Python313/python`
- Project root: `/c/Users/nateh/OneDrive/Desktop/Herk-2`
- API keys are read from `.env` at project root (never hardcoded, never ask the user)
- Scripts live in `scripts/[related-skill-name]/`
- All agents are registered in CLAUDE.md under Active Agents
- Agent creation/modification decisions are logged in `decisions/log.md`

---

## Multi-Agent Audit Mode

When the user asks to audit all agents:

1. Read every `.md` file in `.claude/agents/`
2. Run the audit checklist on each
3. Present a summary table:

```
| Agent | Status | Key Issues |
|-------|--------|------------|
| researcher | Good | Could reduce turns from 15 to 12 |
| x-scraper | Needs attention | Missing tool restrictions, description too vague |
| carousel-planner | Good | No changes needed |
```

4. Offer to dive into any specific agent for detailed recommendations
5. After all changes, update CLAUDE.md Active Agents section if needed

---

## Important Notes

- Always read the agent file before suggesting changes. Never propose edits blind.
- When in doubt about what the user wants, ask. It's better to ask one more question than to misconfigure an agent.
- Keep descriptions slightly "pushy" -- Claude tends to undertrigger rather than overtrigger.
- Subagents cannot spawn other subagents. If the user describes nested delegation, explain this limitation and suggest alternatives (chaining from main conversation, or using skills).
- Memory is powerful but rare. Only 1 of 6 current agents uses it. Don't default to adding memory unless the agent genuinely learns over time.
- The `/agents` command in Claude Code handles creation with guided setup. This skill handles everything after: optimization, auditing, troubleshooting, and tuning.
