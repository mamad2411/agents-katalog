# Universal Agent Context

Every Ocean.studio agent — **main panel, all providers, multi-agent workers, playground, vibe code, web/mobile** — receives the same platform context via `buildAgentContext()` + `assembleAgentSystemPrompt()`.

## Agent paths (all unified)

| Path | Entry | Context |
|------|-------|---------|
| Main Agent Panel | `AgentPanel` → `buildAgentContext` | Full |
| All providers (OpenAI, Anthropic, Antigravity, Codex, etc.) | `runAgentInference` → `assembleAgentSystemPrompt` | Full |
| Multi-agent workers | `buildMemberContext` spreads `baseContext` | Full + member task |
| Playground agents | `playgroundRunner` → `skillScope: 'playground'` | Full |
| Vibe / Self-Control | `runVibeCodeAgent` → `refreshVibeContext` | Full + OCEAN_TOOL |
| Web / mobile | `webAgent` → `runAgentInference` | Full |
| Electron Python backend | `agent.py` receives full context JSON | Full (events + logs) |

## Injected layers (system prompt order)

1. `providerContext.serialized` — agent.md, tools-skill, extensions-skill, open-source-tools-skill, vibe-code-skill, mcp-skill, etc.
2. `routing.serialized` — provider routing, gateway combos
3. Multi-agent member role, system prompt, skills, task
4. `modelConfig.customInstructions` — user overrides
5. `modelConfig.extensionsGuide` — installed VS Code / IDE extensions
6. `modelConfig.openSourceToolsGuide` — Claw Code, Aider, Firecrawl CLI, etc.
7. `extensionHealth.serialized` — extension store health
8. `vibeCode.serialized` — OCEAN_TOOL protocol (when enabled)
9. Session runtime — workspace, terminal, MCP count, plugins, active providers

## NOT the same as Gateway / Services API

External clients hitting `POST /v1/chat/completions` on Ocean Gateway are **provider routers** — they pass through client messages to connected LLM APIs. They do not auto-inject Ocean workspace context (by design — OpenAI-compatible contract).

Internal Ocean agents always use `assembleAgentSystemPrompt()`.

## Bypass

`modelConfig.bypassDefaultInstructions: true` skips provider docs + routing but keeps extensions, OSS tools, and session runtime.

## Verify

```bash
npm run check:all
```

Checks `assembleAgentSystemPrompt.ts` exists and `providerInference` imports it.
