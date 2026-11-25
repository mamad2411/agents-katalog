---
name: compose-agent
description: Wire together existing skills, workflows, and backend configuration into a runnable agent. Use when the user has individual pieces (skills, workflows, identity) and wants to assemble them into a complete agent, or wants to add skills/workflows to an existing agent.
user-invocable: true
---

# Compose Agent — Assembly and Wiring

Take existing components (skills, workflows, SOUL.md, backend config) and wire them into a complete, runnable agent.

## When to Use

- User has standalone skills and wants to bundle them into an agent
- User wants to add a skill or workflow to an existing agent
- User wants to change an agent's backend, model, or tool permissions
- User wants to fork an existing agent for a different domain

## Process

### Step 1: Inventory

Discover what exists:

1. **Check for existing agents:**
   ```
   Find directories matching: agents/*/AGENT.yaml
   ```

2. **Check for standalone skills:**
   ```
   Find files matching: skills/*/SKILL.md
   ```

3. **Check for standalone workflows:**
   ```
   Find files matching: workflows/*.yaml
   ```

4. **Check dispatch backends:**
   ```
   Read ~/.config/ai-dispatch/config.json for available backends
   ```

Present the inventory to the user.

### Step 2: Select Components

Ask the user:

1. **Base**: "Start from scratch or fork an existing agent?"
   - If forking: copy the agent directory and modify

2. **Skills**: "Which skills should this agent include?"
   - List available skills with descriptions
   - Allow selecting existing or noting new ones to create

3. **Workflows**: "Does this agent need workflow enforcement?"
   - List available workflows
   - Allow selecting existing or noting new ones to create

4. **Backend**: "Which backend should it use?"
   - List available dispatch backends
   - Default, specific provider, or multi-backend routing

5. **Identity**: "Keep/modify the SOUL.md or create new?"

### Step 3: Assemble

Create or update the agent directory:

**If creating new:**
```
agents/<name>/
├── SOUL.md
├── AGENT.yaml
├── skills/
│   ├── <skill-1>/SKILL.md    ← copy or symlink
│   └── <skill-2>/SKILL.md
├── workflows/
│   └── <workflow>.yaml        ← copy or symlink
└── memory/
```

**If modifying existing:**
1. Read current AGENT.yaml
2. Add/remove skills from the skills list
3. Add/remove workflows from the workflows list
4. Update configuration as needed
5. Validate any new workflow files

### Step 4: Generate Launch Command

Based on the composed agent, generate the dispatch command:

**Simple dispatch:**
```bash
dispatch <backend> claude \
  --system-prompt "$(cat agents/<name>/SOUL.md)" \
  --max-turns 15 \
  --output-format json \
  -p "your task here"
```

**With MCP tools:**
```bash
dispatch <backend> claude \
  --system-prompt "$(cat agents/<name>/SOUL.md)" \
  --mcp-config agents/<name>/mcp-config.json \
  --max-turns 15 \
  -p "your task here"
```

**As a shell alias (suggest adding to .zshrc):**
```bash
alias my-agent='dispatch claude --system-prompt "$(cat ~/agents/my-agent/SOUL.md)" --max-turns 15 -p'
# Usage: my-agent "analyze AAPL"
```

### Step 5: Verify

1. Validate all workflow files: `bash scripts/validate-workflow.sh agents/<name>/workflows/*.yaml`
2. Verify all skill files have valid frontmatter (name + description)
3. Verify AGENT.yaml references existing skills and workflows
4. Show the complete agent structure to the user
5. Optionally do a dry-run: dispatch the agent with a simple test prompt

## Composition Patterns

### Specialist Agent
One domain, deep skills, opinionated identity.
```yaml
skills: [dcf-valuation, fundamental-analysis, sec-filing-reader]
model: opus    # needs deep reasoning
```

### Generalist Agent
Broad capabilities, neutral identity.
```yaml
skills: [web-research, summarize, compare]
model: sonnet  # fast and capable
allowed_tools: null  # all tools
```

### Pipeline Agent
Workflow-driven, strict stage enforcement.
```yaml
skills: [gather-data, analyze, report]
workflows: [research-pipeline.yaml]
model: sonnet
```

### Swarm Coordinator
Dispatches sub-tasks to other agents.
```yaml
skills: [task-decomposition, result-synthesis]
allowed_tools: [shell, web_search, read_file]
# Uses shell to dispatch sub-agents
```

$ARGUMENTS
