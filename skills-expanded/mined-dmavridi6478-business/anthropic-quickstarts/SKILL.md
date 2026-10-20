# Anthropic Quickstarts — Reference Implementation Library

Production-ready starter projects for building Claude-powered applications. Each quickstart is a complete, runnable app demonstrating a specific integration pattern.

**Source:** `anthropics/anthropic-quickstarts` (public)
**Local clone:** `/home/user/anthropics/anthropic-quickstarts`
**API key required:** yes — sign up at [console.anthropic.com](https://console.anthropic.com)

---

## Quickstart Projects

### Standalone agents

| Project | Directory | What it demonstrates |
|---------|-----------|---------------------|
| **Customer Support Agent** | `customer-support-agent/` | NLU-powered support with knowledge base access |
| **Financial Data Analyst** | `financial-data-analyst/` | Interactive data visualization via chat |
| **Autonomous Coding Agent** | `autonomous-coding/` | Two-agent pattern (initializer + coder); multi-session git-persisted feature list |
| **Agents SDK example** | `agents/` | Core agent loop: `agent.py`, tools, utils, demo notebook |

### Computer & browser use

| Project | Directory | What it demonstrates |
|---------|-----------|---------------------|
| **Computer Use Demo** | `computer-use-demo/` | Full desktop control; latest `computer_toolset_20260801` shape; each action is a named member tool |
| **Computer Use Best Practices** | `computer-use-best-practices/` | Native macOS reference; explicit tool definitions, image sizing/pruning, prompt caching, server-side compaction, batched tool calls, sandboxed shell, trajectory recording |
| **Browser Use Demo** | `browser-use-demo/` | Playwright-backed browser tool: navigate, inspect DOM, extract content, fill forms |

### Managed Agents

All Managed Agents quickstarts live in `managed-agents/`. They use [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) — server-side sessions with sandboxed tools and an event stream your app consumes.

| Project | Directory | Pattern |
|---------|-----------|---------|
| **Assistant UI** | `managed-agents/assistant-ui/` | Spreadsheet analyst in browser chat; `bash` is `always_ask` with inline Allow/Deny gate; Files API attachments; pure reducer over event log |
| **Chat SDK** | `managed-agents/chat-sdk/` | Research analyst + Vercel Chat SDK; persistent session per conversation; token-by-token streaming via `event_deltas`; same handler runs Slack/Teams/Discord/Telegram/WhatsApp via adapter swap |
| **CopilotKit + AG-UI** | `managed-agents/copilot-kit-ag-ui/` | Personal finance assistant; bridges Managed Agent → AG-UI protocol; interactive chart tools rendered as generative UI (payoff timelines, growth projections, budget sliders) |
| **Knowledge Wiki** | `managed-agents/knowledge-wiki/` | M&A data room (Squarespace/Permira, SEC EDGAR); parallel extraction → resolve pass → consolidation dream (`client.beta.dreams`); versioned memory store; `[source \| as-of]` provenance on every fact |
| **Linear** | `managed-agents/linear/` | Stateless webhook bridge on Linear's Agent Platform; `@mention`/assignment → session with Linear IDs in `metadata`; `session.status_idled` webhook posts reply; Linear OAuth with `actor=app` |
| **MCP Server (TypeScript)** | `managed-agents/mcp-server-typescript/` | Wraps Sessions API as 9 MCP tools; `wait_for_idle` collapses event stream into one request/response; agent allowlist; stdio + Streamable HTTP |
| **Road Trip Planner** | `managed-agents/roadtrip-planner/` | Next.js, no chat framework, no DB; `event_deltas` streaming, vault credentials with `injection_location`, per-session model override with `agent_with_overrides`, `multiagent` coordinator + reviewer in a session thread |
| **Sentry** | `managed-agents/sentry/` | Scheduled triage agent; cron-triggered session with no host process; vault env-var credential for `sentry-cli` — egress proxy substitutes token only on requests to Sentry hosts |
| **Slack** | `managed-agents/slack/` | Stateless webhook bridge; `@mention` → session with channel/thread in `metadata`; `session.status_idled` posts reply in-thread; no DB, no persistent connection |
| **Self-hosted Sandboxes** | `managed-agents/self-hosted-sandboxes/` | Docker and docker-memory variants for running sandboxed agent tools in your own infrastructure |

---

## Key Patterns Demonstrated

### Managed Agents session lifecycle
```
POST /sessions              → create session (store ID)
POST /sessions/{id}/messages → send user message
GET  /sessions/{id}/events  → stream events (event_deltas for token-by-token)
     session.status_idled   → reply is ready; read final message
```

### Stateless webhook bridge (Slack / Linear pattern)
1. Inbound event → create session, store platform context in `metadata`
2. `session.status_idled` webhook fires → read `metadata`, post reply to platform
3. No database, no long-lived process

### Vault credentials (Road Trip / Sentry pattern)
Store secrets in the vault; use `injection_location` to mount them into the sandbox at a specific request location. The egress proxy substitutes the real token only on approved host patterns — the token never appears in session content.

### Knowledge distillation (Knowledge Wiki pattern)
1. Parallel extraction sessions read source documents
2. Resolve pass merges findings
3. Consolidation "dream" (`client.beta.dreams`) builds a versioned memory-store wiki
4. Answer repeated questions from the wiki (not re-reading documents) — fraction of the per-question token cost

### Computer Use best practices
- Explicit tool definitions over implicit toolsets
- Correct image sizing and pruning before sending screenshots
- Prompt caching on stable system prompt sections
- Server-side compaction to manage long trajectories
- Batched tool calls to reduce round-trips
- Sandboxed shell for command execution
- Trajectory recording for debugging

---

## Setup (general)

```bash
cd /home/user/anthropics/anthropic-quickstarts/<project>
# Each project has its own README with specific setup
pip install -r requirements.txt   # Python projects
npm install                        # Node/Next.js projects
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Prompts

### Run a quickstart

```
Using /home/user/anthropics/anthropic-quickstarts/[project]:
Read its README.md and walk me through setup and what the project demonstrates.
```

### Adapt a pattern for a new use case

```
Using /home/user/anthropics/anthropic-quickstarts/managed-agents/[project] as a reference:
Adapt the [stateless webhook bridge / knowledge wiki / streaming chat] pattern for [use case].
Show the key files that need to change and what they should contain.
```

### Build a Managed Agents integration

```
Using /home/user/anthropics/anthropic-quickstarts/managed-agents:
Build a [Slack/Linear/custom webhook] integration for [use case] following the stateless bridge pattern.
Key requirements: [list them].
```

### Study computer use best practices

```
Using /home/user/anthropics/anthropic-quickstarts/computer-use-best-practices:
Read the README and source. Explain each best practice (image sizing, prompt caching,
batched tool calls, trajectory recording) with a concrete code example from the project.
```
