# crawl4ai

Crawl4AI Integration for Zen-AI-Pentest

**Category:** reconnaissance — OSINT & Information Gathering

## Overview

Crawl4AI Integration for Zen-AI-Pentest
Advanced web crawling, JavaScript rendering, and data extraction

## Usage in Zen-Ai-Pentest

```python
from tools.crawl4ai_integration import Crawl4AIIntegration


async def main():
    tool = Crawl4AIIntegration()
    result = await tool.__init__("target.com")
    print(result)
```

## CLI Equivalent

```bash
crawl4ai --help
```

## Agent Integration

- CLI: `deep-recon --tool crawl4ai_integration --target example.com`
- Agent persona: auto-selected from category `reconnaissance`
- MCP: `zen-agents_agent_run agent_type=reconnaissance tool=crawl4ai_integration`
- API: `POST /tools/execute` with `{"tool_name": "crawl4ai_integration", "target": "example.com"}`
