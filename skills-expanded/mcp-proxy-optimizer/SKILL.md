# MCP-Proxy Optimizer
> **ID**: mcp-proxy-optimizer
> **Layer**: MCP CONTEXT MANAGEMENT (PON38)
> **Priority**: HIGH — Prevent MCP tool schemas from eating context window
> **Token Cost**: 0

## Problem
Every MCP server injects its full tool schema into context. 3-4 MCP servers = 20K-50K tokens before you type anything. This makes the AI "slower and dumber" — context window is full of tool schemas that 99% won't be used.

## Solution: MCP Proxy Pattern

### P1: SINGLE PROXY ENTRY
```
→ Instead of connecting 50 MCP servers directly to AI:
→ Connect 1 MCP proxy
→ Proxy exposes 3 fixed tools:
  - tool_find(query) → search all MCP servers, return matching tool names
  - tool_call(name, args) → execute specific tool on-demand
  - tool_list(category) → list tools in a category
→ Context cost: 3 tool schemas (~500 tokens) instead of 50 × 400 = 20K tokens
```

### P2: LAZY TOOL LOADING
```
→ MCP servers NOT initialized at session start
→ MCP lazy_init = true (config already set)
→ When AI calls tool_find("web scraping"):
  → Proxy searches registered MCP servers
  → Returns only matching tool schema (~400 tokens)
  → AI calls tool_call with that schema
→ Tools never loaded until needed
```

### P3: OUTPUT CAPPING
```
→ Every MCP tool output capped at 600 chars (config: mcp_output_cap_chars)
→ If output > 600 chars: truncate + add "[truncated, full output at /tmp/mcp_output_N]"
→ Prevents one tool response from eating entire context budget
```

### P4: MCP SERVER CATEGORIES
```
Group MCP servers by domain:
- web: fetch, scrape, browser
- code: git, github, filesystem
- data: postgres, mongo, redis
- ai: openai, anthropic, embedding
- devops: docker, k8s, terraform
→ Only load servers for matching domain when user asks
→ If user asks "query database" → load data-category MCP only
```

### P5: SHARED STATE ACROSS PLATFORMS
```
→ MCP server configs shared via ~/.agents/.mcp_state.json
→ If Codex already fetched a URL → CodeBuddy uses cached result
→ 1× work = 21× savings (cross-platform sync)
→ Cache TTL: 1 hour for tool results
```

## Config
```yaml
mcp_proxy_optimizer:
  enabled: true
  proxy_mode: true
  fixed_tools: [tool_find, tool_call, tool_list]
  lazy_init: true
  output_cap_chars: 600
  cache_ttl_minutes: 60
  cross_platform_sync: true
  shared_state: ~/.agents/.mcp_state.json
  categories:
    web: [fetch, scrape, browser]
    code: [git, github, filesystem]
    data: [postgres, mongo, redis]
    ai: [openai, anthropic, embedding]
    devops: [docker, k8s, terraform]
```
