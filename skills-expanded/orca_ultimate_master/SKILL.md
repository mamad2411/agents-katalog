---
name: orca-ultimate-master
description: ULTIMATE master skill — unlocks ALL Orca capabilities including 3994+ MCP servers, 8 built-in skills, 8 plugins, 40+ custom skills, and multi-agent orchestration.
---

# Orca Ultimate Master Skill

This is the supreme orchestration skill that unlocks the FULL power of Orca + all MCP servers.

## Total Arsenal: 4000+ Capabilities

| Layer | Count | Location |
|-------|-------|----------|
| Orca Built-in MCP Skills | 8 | `Orca.app/Contents/Resources/skills/` |
| Orca Plugins (marketplace) | 8 | `~/Library/Application Support/orca/plugins/` |
| Custom Development Skills | 17 | `~/.orca/skills/*.md` |
| MCP Category Skills | 16 | `~/.orca/skills/mcp_*.md` |
| Community MCP Servers | 3994 | `~/orca-skills-collection/all_mcp_urls.txt` |
| Reference MCP Servers | 7 | `~/orca-skills-collection/mcp-reference-servers/` |
| **TOTAL UNIQUE CAPABILITIES** | **4000+** | |

## Skill Routing Matrix

### Development Tasks
| Task | Primary Skills | MCP Servers |
|------|---------------|-------------|
| Build web app | `fullstack_development`, `api_design` | Figma MCP, Postman MCP |
| Debug issue | `debugging_master`, `troubleshooting` | Sentry MCP, Raygun MCP |
| Code review | `code_review`, `repository_review` | Semgrep MCP, GitHub MCP |
| Database work | `mcp-databases` | PostgreSQL, SQLite, DuckDB, MongoDB, Redis |
| Deploy/DevOps | `devops_automation`, `cloud_native` | Cloudflare, Kubernetes, Docker MCP |
| Security audit | `security_audit`, `mcp-security-servers` | Semgrep, OSV, Netwrix |
| Git operations | `git_workflow`, `mcp-version-control` | GitHub, GitLab, Git MCP |
| Performance | `performance_optimization` | VictoriaMetrics, Signoz MCP |
| Testing | `testing_strategy` | Playwright, Currents MCP |
| Architecture | `code_architecture`, `api_design` | OpenAPI Schema Explorer |

### Data & AI Tasks
| Task | Primary Skills | MCP Servers |
|------|---------------|-------------|
| ML/Data science | `data_science` | ZenML, VegaLite MCP |
| Search/extract | `mcp-search-extraction` | Brave, Exa, Tavily, Apify |
| Knowledge/memory | `mcp-knowledge-memory` | Qdrant, Redis, Memory MCP |
| AI model integration | `mcp-ai-services-integrations` | OpenAI, Gemini, Ollama, HuggingFace |
| RAG pipeline | `mcp-knowledge-memory` | LlamaCloud, Agentset AI |
| Image generation | `mcp-ai-services-integrations` | Flux, NanoBanana, Imagen3, PiAPI |

### Business Tasks
| Task | Primary Skills | MCP Servers |
|------|---------------|-------------|
| Payments | `mcp-finance-fintech` | Stripe, PayPal, Chargebee |
| Communication | `mcp-communication` | Slack, LINE, Linear, Atlassian |
| Productivity | `mcp-workplace-productivity` | Notion, Todoist, Obsidian, Google Keep |
| Marketing | (built-in) | Google Ads, Facebook Ads, Fathom |
| Monitoring | `mcp-monitoring-observability` | Sentry, VictoriaMetrics, Signoz |
| File ops | `mcp-file-systems-code-execution` | FileSystem, FileStash, Backup |

### Creative Tasks
| Task | Primary Skills | MCP Servers |
|------|---------------|-------------|
| 3D/Video | `mcp-social-media-multimedia` | Blender, Maya, Davinci Resolve |
| Music | `mcp-social-media-multimedia` | FL Studio, Ableton, REAPER |
| Social media | `mcp-social-media-multimedia` | YouTube, TikTok, Spotify, BlueSky |
| Gaming | `mcp-social-media-multimedia` | Unity MCP (3 implementations) |
| Data viz | `mcp-social-media-multimedia` | VegaLite, ECharts, Mermaid |

## Multi-Agent Orchestration Pattern

```
1. ANALYZE → Break task into sub-tasks
2. CATALOG LOOKUP → Search `mcp_mega_catalog` for relevant MCP servers
3. ROUTE → Map sub-tasks to skills + MCP servers
4. EXECUTE → Run in dependency order, using Orca's `orchestration` skill
5. VALIDATE → Use `code_review` + `testing_strategy` to verify
6. MONITOR → Use `mcp-monitoring-observability` for runtime health
7. HANDOFF → Use `change-handoff` if incomplete
```

## Quick Install Commands

### NPM MCP servers
```bash
npx -y @modelcontextprotocol/server-<name>
```

### Python MCP servers
```bash
pip install mcp-server-<name>
```

### Browse full catalog
```bash
cat ~/.orca/skills/mcp_mega_catalog.md
cat ~/orca-skills-collection/all_mcp_urls.txt  # 3994 URLs
```

## Source Repositories

| Repo | Stars | Servers |
|------|-------|---------|
| punkpeye/awesome-mcp-servers | 94.9k | ~3900 |
| appcypher/awesome-mcp-servers | 5.8k | ~176 |
| modelcontextprotocol/servers | 90.3k | 7 |
| stablyai/orca-plugins | - | 8 plugins |
