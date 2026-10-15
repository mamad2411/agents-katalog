---
name: trend-to-redbook-automation
description: End-to-end automation orchestrator. Fetches data from Twitter (X) or global News MCPs, passes it through the detoxifier for compliance, formats it via the content-creator, and renders/publishes to Redbook using the local render engine.
---
# 🌟 Trend to Redbook Automation Workflow
## Core Definition
This acts as a **"Workflow Orchestrator"**. It does not perform physical work itself, but schedules and coordinates operations across four distinct modules, creating a complete, no-code AI automation pipeline.
## Prerequisites
To run this pipeline perfectly, you need to install the following underlying skill modules in OpenClaw/your system:
1. **Data Acquisition Layer** (Install at least one):
   - `opentwitter-mcp` (from infra403, for stable Twitter fetching)
   - `opennews-mcp` (from infra403, for stable news sourcing)
2. **Processing & Publishing Layer** (Required standard suite):
   - `redbook-anti-risk-detoxifier-skills` (Compliance formatting & deduplication)
   - `redbook-content-creator-skills` (Redbook viral copywriting structure)
   - `redbook-render-skills` (Local image rendering & publishing engine)
---
## Automation Pipeline SOP (Execution Standard for Agents)
When the user issues a command (e.g., "Help me migrate @cryptoxiao's latest tweet to Redbook"), the Agent must strictly and sequentially execute the following four stages in the background. Do not arbitrarily interrupt or ask questions unless an error occurs:
### 🎯 Stage 1: Information Acquisition
- Call the appropriate MCP interface based on the user's source command.
- If the target is a Twitter influencer (e.g., `@cryptoxiao`), silently call `opentwitter-mcp` to get their latest tweet (Text/Media).
- If the target is global news, call `opennews-mcp` to fetch the news content.
- **Output:** Obtain high-density `Raw_Text`.
### 🎯 Stage 2: Compliance Detoxification
- Pass the `Raw_Text` to `redbook-anti-risk-detoxifier-skills`.
- Strictly follow its ban-word list and detoxification strategy (e.g., rewriting high-risk terms like "VPN", "Twitter scraping", "Crypto" into localized neutral phrases like "cloud assistants" and "information arbitrage").
- **Output:** Obtain a sanitized and compliant `Safe_Text`.
### 🎯 Stage 3: Viral Content Creation
- Feed the `Safe_Text` into `redbook-content-creator-skills`.
- Format the content following the CES algorithm rules for strong emotional pacing.
- **Output:** A structured final draft, including a highly suspenseful `Title`, a platform-native `Body`, and high-traffic `Tags`.
### 🎯 Stage 4: Rendering & Publishing
- Locate the root directory of `redbook-render-skills` (formerly `Auto-Redbook-Skills`).
- Inject the title and body generated in the previous step, and call its core `render_xhs.py` or `render_xhs.js` to batch-render stacked graphic cards.
- Finally, execute the publishing script or prompt the user to review the beautifully rendered card set in the local output directory.
---
## Why Design It This Way?
Novice users or operators only need to **trigger this skill with a single sentence**. The AI will act as the master contractor of the pipeline, automatically dispatching the Twitter data fetcher, the compliance filter, the copywriter, and the graphic renderer, delivering a finished product ready for Redbook publishing within a minute.
