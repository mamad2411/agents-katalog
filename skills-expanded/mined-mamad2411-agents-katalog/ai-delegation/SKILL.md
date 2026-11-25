# AI↔AI Delegation & Multi-Agent Orchestrierung Skill

Workflows für Agent-to-Agent Delegation, Workflow-Chaining, Sub-Agent-Spawning, Result-Merging.

## Architektur

```
User Request
    │
    ▼
Orchestrator Agent (Coordinator)
    │
    ├── ▶ Specialist Agent A ──▶ Result
    ├── ▶ Specialist Agent B ──▶ Result
    └── ▶ Specialist Agent C ──▶ Result
    │
    ▼
Merge & Final Response
```

## Delegation Patterns

### 1. Sequential Chain
Jeder Agent baut auf dem vorherigen auf:
```
deep-recon --target example.com → recon.json
deep-exploit --target-file recon.json → exploit.log
deep-report --scan-id <id> --format pdf → report.pdf
```

### 2. Parallel Fan-Out
Mehrere Agenten gleichzeitig, Ergebnisse mergen:
```python
import asyncio


async def fan_out(target: str):
    tasks = [
        agent_run("recon", target),
        agent_run("network", target),
        agent_run("cloud", target),
        agent_run("social", target),
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return merge_results(results)
```

### 3. Hierarchisch (Manager + Worker)
```python
manager_prompt = """
Analyze the task and break it into sub-tasks.
Assign each to the right specialist agent.
Track dependencies and merge results.
"""
```

### 4. ReAct mit Sub-Agent-Calls
```python
class DelegatingReActAgent(ReActAgent):
    async def _act(self, plan: str) -> ToolResult:
        if plan.get("delegate_to"):
            # Spawn sub-agent
            sub = create_agent(plan["delegate_to"])
            return await sub.run(plan["task"])
        return await super()._act(plan)
```

## Workflow Chaining

### Dependency Graph
```python
workflow = coordinator.create_workflow(
    target="example.com",
    phases=["recon", "scan", "exploit", "report"],
)
# Automatisch: recon-output → scan-input, scan-output → exploit-input
```

### Conditional Branching
```python
if result["critical_findings"] > 0:
    # Escalate to red team
    workflow.add_phase("redteam")
else:
    # Skip to report
    workflow.add_phase("report")
```

## Context Passing

Zwischen Agenten wird Kontext über JSON weitergegeben:
```json
{
  "task_id": "wf-abc123",
  "target": "example.com",
  "phase": "recon",
  "results": {
    "subdomains": ["admin.example.com", "api.example.com"],
    "ports": {"22": "open", "80": "open", "443": "open"},
    "technologies": ["nginx", "react", "postgresql"]
  },
  "artifacts": ["recon.json", "screenshots/"]
}
```

## Hermes Integration (via MCP)

```python
# Agent delegiert an anderen Agent
zen_agents_agent_run(agent_type="recon", target="example.com")
# → Result enthält findings für nächsten Agent

# Workflow orchestrieren
zen_agents_workflow_create(target="example.com", phases="recon,scan,exploit,report")
```

## Fehlerbehandlung

```python
class AgentOrchestrator:
    def handle_failure(self, agent: str, error: str):
        if "timeout" in error.lower():
            return self.retry(agent, timeout=timeout * 2)
        elif "rate_limit" in error.lower():
            ks_rotate_now()  # VPN-Killswitch
            return self.retry(agent)
        else:
            return self.escalate(agent, error)
```
