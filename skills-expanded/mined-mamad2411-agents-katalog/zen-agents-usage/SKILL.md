# Zen Agents Usage Skill

How to use the 11 specialized AI agents and the ReAct loop.

## Basic Agent Execution

```python
from agents.react_agent import ReActAgent, ReActAgentConfig

# Create agent with persona
config = ReActAgentConfig(
    max_iterations=10,
    use_vm=True,
    risk_level=1,  # NORMAL
)
agent = ReActAgent(config, persona="reconnaissance")

# Run against target
result = agent.run(target="example.com", objective="Enumerate all subdomains and open ports")

# Generate report
print(agent.generate_report(result))
```

## ReAct Loop States

```
IDLE → PLANNING → EXECUTING → OBSERVING → REFLECTING → COMPLETED
         │           │           │            │
         └───────────┴───────────┴────────────┘
                    (Retry Loop)
```

## CLI Usage

```bash
# Reconnaissance
deep-recon --target example.com --output recon.json

# Exploitation
deep-exploit --target example.com --vulnerability CVE-2021-44228

# Full audit
deep-audit --target example.com --phases recon,scan,exploit,report

# Reporting
deep-report --scan-id wf-abc123 --format pdf
```

## API Usage

```bash
# Create scan
curl -X POST http://localhost:8000/scans \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Audit","target":"example.com","scan_type":"full"}'

# Execute tool
curl -X POST http://localhost:8000/tools/execute \
  -d '{"tool_name":"nmap_scan","target":"example.com","parameters":{"ports":"22,80,443"}}'
```

## WebSocket Monitoring

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/scans/1");
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Progress:", data.progress, "Findings:", data.findings);
};
```

## MCP Agent Tools

```bash
# List all agents
zen-agents_agent_list

# Run single agent
zen-agents_agent_run agent_type=recon target=example.com

# Full workflow
zen-agents_full_audit target=example.com phases=recon,scan,exploit,report
```
