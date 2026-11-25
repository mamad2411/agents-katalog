# a6-agent-orchestrator-pro

> Full-featured agent orchestrator with registry, task queue, workflow engine, security scoping, cost controls, ClickUp integration, and project isolation.

## Features

- **Agent Registry** — Register agents with model, system prompt, and permission scoping
- **Permission Scoping** — Per-agent allowed tools, paths, external comms, and runtime limits
- **Task Queue** — Priority-based queue with auto-routing to matched agents
- **Project Isolation** — Tag tasks by project, filter and scope agent context per project
- **Budget Controls** — Daily/monthly spend limits with alerts and pre-spawn checks
- **ClickUp Integration** — Bi-directional sync (pull tasks, push completions)
- **Workflow Engine** — Multi-step workflows with dependencies and failure handling
- **Dashboard** — Auto-generated HEARTBEAT.md with full system overview
- **Heartbeat** — Quick one-line health check
- **Reports** — Summary reports with project and cost breakdowns

## Requirements

- Python 3.10+
- SQLite (built-in)
- OpenClaw workspace with `.data/sqlite/` directory
- ClickUp API token (optional, for ClickUp sync)

## Quick Start

```bash
PY=~/.openclaw/workspace/.venv/bin/python3

# Initialize schema and seed default agents
$PY scripts/agent_orchestrator.py --init

# Register an agent with permissions
$PY scripts/agent_orchestrator.py register security-scanner claude-sonnet-4 \
  "Security scanning specialist" \
  --allowed-tools "web_search,read" \
  --allowed-paths "/workspace/tools,/workspace/skills" \
  --max-runtime 120

# Queue a task with project tag
$PY scripts/agent_orchestrator.py queue "Research competitor pricing" --type research --priority 2 --project mlm

# Set budget limits
$PY scripts/agent_orchestrator.py budget set --daily 5.00 --monthly 100.00

# Check status
$PY scripts/agent_orchestrator.py status

# Run next task (checks budget before spawning)
$PY scripts/agent_orchestrator.py run-next
```

## Commands

### Agent Management
| Command | Description |
|---------|-------------|
| `register <name> <model> <prompt> [--allowed-tools] [--allowed-paths] [--can-send-external] [--max-runtime]` | Register agent with permissions |
| `list` | List all agents with permission summary |
| `list --project <name>` | List tasks filtered by project |
| `assign <task_type> <agent_name>` | Map task type to agent |

### Task Queue
| Command | Description |
|---------|-------------|
| `queue <description> [--type] [--priority] [--project]` | Queue a task |
| `run-next` | Run highest-priority queued task (budget-checked) |
| `auto-route [--execute] [--force]` | Auto-assign agents to unrouted tasks |
| `status` | Overview with agent count, queue, budget |

### Budget Controls
| Command | Description |
|---------|-------------|
| `budget set --daily <$> --monthly <$>` | Set spend limits |
| `budget status` | Current spend vs limits |
| `budget alert` | Warning if approaching limits (80%+) |
| `budget log <amount> [--agent] [--desc]` | Record a spend entry |

### ClickUp Integration
| Command | Description |
|---------|-------------|
| `sync-clickup` | Pull tasks from ClickUp folders |
| `update-clickup` | Push completed results back to ClickUp |

### Monitoring
| Command | Description |
|---------|-------------|
| `dashboard` | Full dashboard → HEARTBEAT.md |
| `heartbeat` | Quick one-line health check |
| `report` | Summary report with project/cost breakdown |
| `history [--limit N]` | Execution history |

## Permission Scoping

Each agent can be configured with:
- **allowed_tools** — JSON array of tool names the agent can use
- **allowed_paths** — JSON array of file paths the agent can access
- **can_send_external** — Whether the agent can send emails/messages
- **max_runtime_seconds** — Kill timeout for the agent

Permissions are injected into the agent's system prompt when spawned via `run-next`, creating a security scope enforced by the model.

## Project Isolation

Tasks can be tagged with a project name:
```bash
$PY scripts/agent_orchestrator.py queue "Build landing page" --type build_skill --project mlm
$PY scripts/agent_orchestrator.py list --project mlm
```

When an agent is spawned for a project-tagged task, its system prompt includes project context instructions limiting scope.

## Cost Controls

Budget limits prevent runaway spending:
```bash
$PY scripts/agent_orchestrator.py budget set --daily 5.00 --monthly 100.00
$PY scripts/agent_orchestrator.py budget log 0.15 --agent researcher --desc "Deep research on X"
$PY scripts/agent_orchestrator.py budget alert
```

The `run-next` command checks budget before spawning any agent and refuses if limits are exceeded.

## Database

SQLite at `.data/sqlite/agxntsix.db` with tables:
- `agents` — Registry with permissions
- `task_queue` — Priority queue with project tags
- `execution_log` — Run history
- `budget_config` — Spend limits
- `daily_spend` — Spend tracking
- `workflow_definitions` / `workflow_steps` / `workflow_runs` — Workflow engine
- `agent_task_mappings` — Type-to-agent routing
- `agent_configs` — Key-value config per agent

## Architecture

```
User/Cron → Queue Task → Auto-Route → Budget Check → Spawn Agent (with permissions)
                                                          ↓
                                              Permission-scoped system prompt
                                              Project-isolated context
                                              Runtime-limited execution
                                                          ↓
                                              Log result → Update ClickUp → Dashboard
```

---

**Built by Agent Six (a6)**

🌐 [agxntsix.ai](https://agxntsix.ai)
💼 [LinkedIn](https://linkedin.com/in/agxntsix)
🎥 [YouTube](https://youtube.com/@agxntsix)
🐙 [GitHub](https://github.com/agxntsix)
📅 [Book a Call](https://cal.com/agxntsix)
