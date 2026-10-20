# Zen-Ai-Pentest Framework Skill

Complete guide to the Zen-Ai-Pentest autonomous pentesting framework architecture.

## Project Structure

```
zen-ai-pentest/
├── agents/              # ReAct AI agents (11 specialized personas)
├── api/                 # FastAPI backend + WebSocket
├── core/                # Orchestrator, models, caching
├── tools/               # 72+ integrated security tools
├── risk_engine/         # CVSS, EPSS, false positive detection
├── modules/             # Scanner, exploit modules
├── web_ui/              # React frontend + dashboard
├── database/            # PostgreSQL models (SQLAlchemy)
├── reports/             # PDF/HTML/DOCX generator
├── docker/              # Dockerfiles + compose
├── tests/               # 43,000+ tests (unit, integration, security)
└── mcp/                 # MCP servers (8 total)
```

## Key Components

### Agent System
```python
from agents.react_agent import ReActAgent, ReActAgentConfig

config = ReActAgentConfig(max_iterations=10, use_vm=False)
agent = ReActAgent(config)
result = agent.run(target="example.com", objective="Full security assessment")
```

### 11 Personas
| Persona | CLI | Purpose |
|---------|-----|---------|
| Reconnaissance | deep-recon | OSINT, subdomain, port scan |
| Exploitation | deep-exploit | CVE matching, sandboxed exec |
| Analysis | deep-analyze | FP detection, CVSS scoring |
| Reporting | deep-report | PDF/HTML generation |
| Red Team | deep-redteam | Full adversarial simulation |
| Social Engineering | deep-social | Phishing, OSINT |
| Network | deep-network | Infrastructure testing |
| Cloud | deep-cloud | AWS/Azure/GCP |
| ICS | deep-ics | SCADA/industrial |
| Mobile | deep-mobile | iOS/Android |
| Crypto | deep-crypto | TLS, cert, cipher analysis |

### Risk Engine
```python
from risk_engine.false_positive_engine import FalsePositiveEngine

engine = FalsePositiveEngine()
score = engine.assess_finding({"vuln_type": "xss", "confidence": 0.85})
# Combines Bayesian + multi-model voting
```

### Guardrails
- Private IP blocking (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- Risk levels 0-3 (SAFE → AGGRESSIVE)
- Read-only default, --force for exploitation
- Timeout management (10min max)

## MCP Servers
```bash
# 8 MCP servers registered in opencode.jsonc
mcp/obscura/      # Encrypted secret vault
mcp/ip-tracker/   # Visitor IP tracking
mcp/omni-ai/      # AI chat via OmniRoute
mcp/qterminal/    # Shell/Docker orchestration
mcp/metasploit/   # Metasploit RPC connector
mcp/vpn-killswitch/# Connection-loss failover
mcp/zen-agents/   # 11-agent orchestration
```
