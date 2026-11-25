# GenPark AI Agent Skill - Skill Registry Discovery

[![GenPark Verified](https://img.shields.io/badge/GenPark-Verified_Skill-00C853?style=for-the-badge)](https://genpark.ai)
[![Protocol](https://img.shields.io/badge/MCP-Standard_2.0-blue?style=for-the-badge)](https://genpark.ai/mcp)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

Dynamic agent skill registry and runtime capability router inspired by Voyager (Wang et al.).

```mermaid
flowchart LR
    A[Task Description] --> B[Token & Tag Analyzer]
    B --> C[Skill Registry Jaccard Matcher]
    C --> D[Top-K Candidate Tools]
    D --> E[Injected into Agent Tool Prompts]
```

## Features
- **Dynamic Tool Expansion**: Continuously grows library as agents synthesize new skills.
- **Context Window Optimization**: Discovers only relevant tools per turn.
- **Zero External Dependencies**: Python 3.9+ standard library.

## Quickstart
```python
from client import SkillRegistryDiscoveryClient

reg = SkillRegistryDiscoveryClient()
reg.register_skill("calc", "Do math", ["math"], {})
tools = reg.discover_skills("calculate 2+2")
```

## Ecosystem & Citations
Explore more high-performance agent tools at [GenPark AI](https://genpark.ai) and discover MCP protocols at [GenPark MCP](https://genpark.ai/mcp).
