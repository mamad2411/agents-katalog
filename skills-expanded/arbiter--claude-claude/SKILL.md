# The Arbiter - Project Context

## What This Is

A hierarchical AI orchestration system that extends Claude's effective context window by managing a chain of Claude sessions through the Agent SDK.

## Key Files

- `arbiter-architecture.md` - Full system architecture
- `docs/tui-redesign.md` - RPG-style TUI redesign spec (wizard circle, campfire, etc.)
- `src/test-headless.ts` - Headless end-to-end test

## Testing Without TUI

Run the headless test to verify the system works without needing an interactive terminal:

```bash
npm run test:headless
```

This exercises the full flow:
1. Starts Arbiter session with MCP tools
2. Sends test messages
3. Spawns an Orchestrator
4. Watches Orchestrator do work via subagents
5. Logs all messages, context %, and tool usage

Use this when debugging SDK integration, message routing, or session issues.

## Running the TUI

```bash
npm run dev     # Development
npm run build   # Compile TypeScript
npm start       # Production
```

Exit with `Ctrl+C` or `Ctrl+Z`.

## Architecture Quick Reference

```
Human → Arbiter (manager, MCP tools) → Orchestrators (workers) → Subagents (do actual work)
```

- Arbiter only has: spawn_orchestrator, disconnect_orchestrators, read-only tools, Explore
- Orchestrators have all tools and spawn blocking subagents
- Each layer has ~200K context window

## Permissions

Everything runs with `permissionMode: 'bypassPermissions'`. This is intentional - designed for controlled environments.

## Current State

- Core system works end-to-end
- TUI is basic, being redesigned as RPG-style wizard council (see docs/tui-redesign.md)
- Context tracking uses Math.max to prevent decreasing values
