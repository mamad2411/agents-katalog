---
name: create-agent
description: Brainstorm and scaffold a new domain-specific AI agent. Creates SOUL.md (identity), AGENT.yaml (config), skills, and workflows. Use when the user wants to build an agent for a specific domain like financial research, code review, customer support, etc.
user-invocable: true
---

# Create Agent — Domain-Specific AI Agent Factory

Build a complete agent from scratch through guided brainstorming, then scaffold all files.

## Process

### Phase 1: Discovery

Ask these questions **one at a time**. Adapt based on answers.

1. **Domain**: "What domain will this agent specialize in?" (e.g., financial research, code review, DevOps, customer support, legal analysis)

2. **Purpose**: "What's the core job? What question does someone bring to this agent?" (e.g., "Is this stock undervalued?", "Is this PR safe to merge?")

3. **Personality**: "How should this agent think and communicate?"
   - a) Analytical and precise (like a researcher)
   - b) Friendly and explanatory (like a tutor)
   - c) Terse and action-oriented (like an operator)
   - d) Opinionated with strong convictions
   - e) Custom — describe it

4. **Data Sources**: "What information does this agent need access to?"
   - APIs (financial data, GitHub, Jira, etc.)
   - Web search
   - Local files / codebases
   - Databases
   - Browser automation
   - Custom tools

5. **Workflows**: "What multi-step processes should this agent follow?"
   - e.g., "Gather data → Analyze → Validate → Present results"
   - e.g., "Read code → Find issues → Suggest fixes → Verify"

6. **Backend**: "What LLM backend should it prefer?"
   - a) Default (whatever's configured)
   - b) Specific provider (glm, openrouter)
   - c) Local (ollama)
   - d) Multiple — route by task complexity

### Phase 2: Design

Based on discovery, design these components:

**Identity (SOUL.md)**:
- Who is this agent? Give it a name and personality
- What philosophy guides its decisions?
- What does it value? What does it refuse to do?
- Give the agent conviction and a clear point of view

**Configuration (AGENT.yaml)**:
- Model selection (sonnet for speed, opus for depth, haiku for lightweight)
- Tool allowlist (restrict to what's needed)
- Backend preference
- Memory settings

**Skills (SKILL.md files)**:
- Each skill = one repeatable workflow the agent can execute
- Design 2-4 core skills based on the domain
- Each skill has: name, description, step-by-step checklist, output format
- Each skill should have a clear trigger, step-by-step checklist, and structured output

**Workflows (YAML state machines)** (if needed):
- Multi-step processes with state transitions
- Per-state tool restrictions and permission modes
- Entry/exit hooks with instructions

Present the design for approval before scaffolding.

### Phase 3: Scaffold

After user approves, create the agent directory at `~/.talon/agents/<agent-name>/`:

```
~/.talon/agents/<agent-name>/
├── SOUL.md              — Identity and philosophy
├── AGENT.yaml           — Configuration
├── skills/
│   ├── <skill-1>/SKILL.md
│   ├── <skill-2>/SKILL.md
│   └── ...
├── workflows/
│   └── <workflow>.yaml  (if needed)
└── memory/              — Persistent memory directory
```

**Default location**: `~/.talon/agents/` — shared across all workspaces, auto-discovered by Talon IDE.
**Override**: If the user specifies a different path, use that instead.

**File creation order:**
1. Read templates from the agent-factory plugin's `templates/` directory
2. Fill in templates with the designed content
3. Create SOUL.md first (identity drives everything)
4. Create AGENT.yaml with configuration
5. Create each SKILL.md with full workflow instructions
6. Create workflow YAML files if designed
7. Validate workflows with `scripts/validate-workflow.sh`

### Phase 4: Verify

After scaffolding:
1. Read back each created file to verify correctness
2. Run `bash scripts/validate-workflow.sh` on any workflow files
3. Show the user the complete agent structure
4. Explain how to run it:
   - Via dispatch: `dispatch <backend> claude --system-prompt "$(cat ~/.talon/agents/<name>/SOUL.md)" -p "task"`
   - Via Talon IDE: Agent auto-discovered from `~/.talon/agents/`

## Examples of Domain Agents

| Agent | Domain | Core Skills |
|-------|--------|-------------|
| Analyst | Financial Research | DCF valuation, fundamental analysis, stock screening, SEC filing analysis |
| Sentinel | Security Audit | Dependency scanning, OWASP check, secret detection, compliance review |
| Scribe | Documentation | API doc generation, changelog writing, README scaffolding, diagram creation |
| Conductor | DevOps | Deployment pipeline, incident response, infrastructure review, cost optimization |
| Advocate | Legal | Contract review, clause analysis, risk assessment, compliance check |

## Key Principles

- **Opinionated > Generic**: An agent with a clear point of view and philosophy is more useful than a generic assistant
- **Focused skills > Many tools**: 3-4 excellent skills beat 20 mediocre ones
- **Validation built in**: Every skill should have a validation/sanity-check step
- **File-based > Code-based**: Everything is markdown/YAML, no code needed to create an agent

$ARGUMENTS
