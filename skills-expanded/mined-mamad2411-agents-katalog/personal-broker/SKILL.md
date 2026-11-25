---
name: personal-broker
description: Smart Resale Agent hub. Orchestrates the complete 7-step C2C resale workflow. Use when user wants to sell second-hand items, list goods on resale platforms (Xianyu/闲鱼, Zhuanzhuan/转转, eBay, Depop), needs price research, or says "sell this", "list this", "help me resell", "I want to sell", "我要卖", "闲置出售". This hub chains 7 sub-skills into a complete conversational resale pipeline.
---

# Smart Resale Agent — Hub

Orchestrates the complete C2C resale workflow: photo recognition → price research → platform auth → listing card & publish → schedule + fuse → auto-delist on sale.

## Two Modes

### Mode A: MCP Server (v2, recommended for non-Claude-Code clients)
Use `broker_core/mcp_server.py` — a standard MCP server exposing 7 tools. Any MCP-compatible client (Claude Desktop, Cursor, VS Code) can connect.

### Mode B: Claude Code Skills (v1, still supported)
Use the 7 `/broker-*` slash commands within Claude Code CLI.

## For MCP Mode

Load `guardrails/Omni-Agent-Guardrails.yaml` as the system prompt. This enforces:
- **Tool Routing**: Step 1→2→3→4→5 forced order
- **Shield Protocol**: blocked=true → all actions cancelled
- **Transparency Schema**: Every output carries `audit://` reference

MCP tool mapping:
```
cognitive_intake       → broker-recognize
generate_xai_pricing   → broker-price
fuse_gatekeeper         → broker-fuse (MANDATORY GATE)
execute_platform_action → broker-card + broker-delist
audit_trail_query       → audit_logger
schedule_repricing      → broker-schedule
platform_auth_trigger   → broker-auth
```

## Prerequisites

**ANTHROPIC_API_KEY** must be set. `broker-recognize` (Step 1) requires Claude Vision API to analyze product photos. Without this key, photo recognition will fail.

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 7-Skill Pipeline

```
📷 broker-recognize  →  Photo → structured product info
🔐 broker-auth       →  Bind platform accounts (login once, session persisted)
🔍 broker-price      →  Authenticated price search across platforms
🛡️ broker-fuse       →  ⚠️ GLOBAL INTERCEPTOR — set fuse BEFORE publish/schedule
📋 broker-card       →  Listing card preview → user confirmation → auto-publish
⏰ broker-schedule   →  Set repricing interval → register cron/launchd
✅ broker-delist     →  Auto-detect sale → delist all platforms
```

**broker-fuse is NOT step 6. It is a mandatory interceptor/gate.** Before `broker-card` can publish and before `broker-schedule` can auto-reprice, `broker-fuse` MUST be called and set. Every publish and repricing action validates against the fuse.

## Orchestration Rules

### When user wants to sell (full flow)
Guide the user through skills in this order: recognize → auth → price → fuse → card → schedule. Fuse is set as a gate BEFORE card publishing. Schedule is configured during the card conversation before publishing.

### Flow control
1. Call `broker-recognize` — user uploads photo, AI extracts product info. User confirms.
2. Call `broker-auth` — open browser for each platform user wants to list on. Sessions persist automatically.
3. Call `broker-price` — search all bound platforms using stored sessions. Present transparency report. User confirms recommended price.
4. **MANDATORY GATE: Call `broker-fuse`** — set unbreachable floor price. This is NOT optional. No publishing or repricing may proceed without a fuse set.
5. Call `broker-card` — generate listing cards. **Script validates fuse before publish.** Ask user to set repricing interval (default 7 days). User reviews card → says "发布" → script checks fuse → auto-publishes.
6. `broker-schedule` registers the cron/launchd task. **Daily repricing also validates against fuse.** Done automatically after publish.
7. `broker-delist` triggers when: (a) user says "卖了", or (b) daily scheduler detects item sold on a platform.

### Standalone usage
Each sub-skill can be invoked independently:
- `/broker-recognize` — just analyze a product photo
- `/broker-price` — just research prices for a described item
- `/broker-fuse` — adjust an existing fuse
- `/broker-delist` — manually trigger delisting
- `/broker-schedule` — change repricing interval

### Cross-skill data passing
Skills communicate via `~/.broker/listings.json` (state_manager) and conversation context. The `item_id` links everything.
