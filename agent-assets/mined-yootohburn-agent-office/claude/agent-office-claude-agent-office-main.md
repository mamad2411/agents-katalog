@AGENTS.md

# CLAUDE.md — Agent Office

## Development Tool

Claude Code is the primary development tool for this project.
Codex support will be added later once repository access is confirmed working.

## Phase 1 Status

- Real Shopee API: NOT connected. Mock data only.
- Real Lazada API: NOT connected. Mock data only.
- Real TikTok API: NOT connected. Mock data only.
- Real Anthropic/OpenAI API calls inside the app: NOT used. Mock data only.
- Web scraping: NOT implemented.
- Auto-posting: NOT implemented.

All agent actions, workflows, and outputs in Phase 1 are simulated with static mock data.

## Stack

- React + TypeScript + Vite (frontend only, no backend)
- Pure CSS for 8-bit pixel dashboard styling
- No external UI libraries

## Folder Guide

- `.claude/agents/` — Claude Code subagent instruction files
- `src/agents/` — TypeScript agent registry, routing, session state
- `src/components/AgentOffice/` — Dashboard UI components
- `prototypes/` — Reference files only, not wired into production
- `docs/` — Documentation

## Adding a New Agent

1. Add an instruction file to `.claude/agents/<agent-name>.md`
2. Add the agent definition to `src/agents/agentRegistry.ts`
3. Register its platform in `src/agents/platformRegistry.ts`
4. Add routing logic in `src/agents/agentTaskRouter.ts`
5. The dashboard will pick it up automatically

## Orchestration

Do NOT build production orchestration inside Claude Code.
Real production orchestration for Phase 2 should use n8n / Make / Pipedream or a custom backend.
Phase 1 is mock data only — all workflows are simulated in TypeScript.

## Phase 2 Direction

When moving beyond Phase 1:
- Replace mock data in `src/agents/agentRegistry.ts` with real API calls
- Build workflow orchestration using n8n, Make, or Pipedream
- Connect real Shopee Affiliate API, Lazada Affiliate API, TikTok Shop API
- Human Approval Gate remains mandatory — never automate the publish decision
- Keep mock data available as a fallback for development and testing

## Future: Codex Support

When Codex repository access is restored, add agent instruction files under `.codex/agents/`.
Do not create `.codex/` files until that access is confirmed working.
