---
name: dispatch
description: "Analyze task, select appropriate agent from registry, launch sub-agent with agent rules. Triggers: dispatch, select agent, route, assign task."
argument-hint: "[task description]"
---

# /dispatch — Agent Router & Dispatcher

Analyzes incoming task, selects appropriate agent from `agent-registry.json`, and launches sub-agent with that agent's rules.

## Flow

### 1. Task Analysis (max 3 tool calls)

Analyze user task:
- Which capabilities are needed? (api, flutter, security, jira, research, etc.)
- Which category does it fall into? (backend, code-review, market-research, etc.)
- How many category overlaps?

### 2. Agent Selection

Read `agent-registry.json` → only select from agents in `active_agents` list.

**Matching rules:**
- Match agent `capabilities` against task requirements
- If multiple agents qualify → select cheapest by `primary_model` cost
- If no agents match → escalate to A1 (Lead Orchestrator)
- 3+ category overlap → escalate to Opus (`A2.escalate_when` rule)

**Confidence scoring:**
- >= 0.85 → single agent dispatch
- 0.6 - 0.85 → primary + secondary parallel
- < 0.6 → ask user

### 3. Model & Effort Assignment

Use registry settings for selected agent:
- `primary_model` → assign as model
- `effort` → effort level
- `max_tool_calls` → sub-agent limit
- `fallbacks` → try in order if model degrades
- `mcps` → which MCPs are active

### 4. Launch Sub-agent

Dispatch via Agent tool. Sub-agent prompt:

```
AGENT: {id} ({name})
MODEL: {primary_model} | EFFORT: {effort} | MAX: {max_tool_calls} tool calls
MCP: {mcps}
CAPABILITIES: {capabilities}

TASK: {user task}

RULES:
- {scope and escalation rules from agent .md file}
- WATCHDOG: Self-check every {watchdog.self_check_interval} calls, max {max_tool_calls} calls
- Escalation needed → {related agents}
```

### 5. Result

When sub-agent completes:
- Success → show result to user
- Failure → apply retry_strategy (1. same agent different model, 2. different agent same capability, 3. escalate to A1)

## Special Cases

### Parallel Dispatch
If task can be split into independent parts:
```
"Write REST endpoint + write tests" → B2 (Backend Coder) + B6 (Test Writer) parallel
"Research market + write landing page" → H1 (Market Researcher) + M2 (Landing Page) parallel
```

### Escalation Chains
| Situation | Action |
|-----------|--------|
| Architecture decision | → B1 (Opus) |
| Security concern | → B13 (Opus) |
| 3+ categories | → A1 (Lead Orchestrator) |
| Model poor performance | → fallback chain |
| All fallbacks exhausted | → ask user |

## Rules
- NEVER sees pool agents — only active_agents
- Each dispatch: 1 line log: `[DISPATCH] {task} → {agent_id} ({model})`
- Max 5 tool calls for dispatch (task analysis + read registry + select agent + dispatch)
- Don't dispatch unnecessarily — don't assign agents for simple Q&A
