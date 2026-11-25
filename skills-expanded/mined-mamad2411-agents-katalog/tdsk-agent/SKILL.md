---
name: "tdsk-agent"
description: "Knowledge base for the headless AI agent orchestration library"
tags: ["ai-agent", "llm", "streaming", "multi-turn", "tool-execution", "sandbox", "typescript"]
---
# Agent Repo Skill

## Overview

The **Agent** repo (`repos/agent`, `@tdsk/agent`) is a headless AI agent orchestration library.

- **Instance-based `AgentRunner`** with `init()` / `runTurn()` / `updateConfig()` / `destroy()` lifecycle, plus static `AgentRunner.run()` for one-shot SSE use
- **Wraps pi-mono** (`@mariozechner/pi-agent-core` Agent class) for multi-turn ReAct loops with streaming, automatic context management (prune/compact), and transient error retries
- **11 runtime tools** (defined in `tools/tools.ts`): 9 sandbox tools (fs, shell, code, artifact) + 2 web tools (search, fetch via Jina), plus 2 memory tools (`memorySearch`, `memoryWrite`) when an `IMemoryProvider` is injected, plus variable custom function tools from `FunctionModel[]`. Note: `tools/definitions/` is legacy/unused
- **Supports all pi-mono LLM providers** (Anthropic, OpenAI, Google, etc.) via `getModel()`, extended thinking via `thinkingLevel`, and custom message roles (artifact, notification, systemEvent) filtered before LLM calls
- **Pluggable persistence** via `IAgentRunnerDB` interface -- backend uses direct DB, TSA delegates to backend API

## Directory Structure

```
repos/agent/
├── configs/           # agent.config.ts, aliases.ts (@TAG/*), tsup.config.ts, vitest.config.ts
└── src/
    ├── index.ts       # Barrel re-exports
    ├── adapters/      # eventBridge (AgentEvent→TStreamEvent), messageConverter (ThreadedStack↔pi-mono)
    ├── runner/        # AgentRunner — instance-based with init/runTurn/updateConfig/destroy + static run()
    ├── tools/         # createSandboxTools(), createWebTools(), buildCustomFunctionTools()
    │   └── definitions/  # Static TLLMToolDef[] by category: fs (6), shell (1), code (1), web (2)
    ├── types/         # runner.types.ts, web.types.ts, customMessages.ts (declaration merging)
    └── utils/         # skillResolver, contextManager, errorClassifier, logger, paths
```

## Architecture

The `AgentRunner` is an instance that maintains state across turns. It wraps pi-mono's `Agent` class, providing DB persistence, event bridging, per-turn skill resolution, transient error retries, context management, and sandbox integration.

**Key components:**
- **Event Bridge** (`mapAgentEvent`) -- converts pi-mono `AgentEvent` to `TStreamEvent` (text, thinking, tool_call_start/args, tool_result, tool_execution_update, done, error, turnEnd with usage/cost via `calculateCost()`)
- **Message Converter** -- bidirectional conversion between `TMessageContent[]` and pi-mono `Message[]`, handling text, images, files, thinking, tool_use, tool_result
- **Skill Resolver** (`resolveActiveSkills`) -- per-turn keyword-triggered skill activation, injects instructions into system prompt and merges tool names
- **Error Classifier** (`isTransientError`) -- regex-based detection of rate limits, 429, 502/503, timeouts, network errors; retry loop with exponential backoff via `agent.continue()`
- **Context Manager** (`createContextManager`) -- keeps messages within a percentage of the model's context window using prune (drop oldest) or compact (LLM-summarize old) strategy. Its `onSummary` callback (fire-and-forget) hands the compaction summary to the runner, which persists it as a durable `compaction`-kind memory via the injected `memoryProvider` instead of discarding it
- **Custom Messages** -- declaration merging adds `artifact`, `notification`, `systemEvent` roles to pi-agent-core; stored in history but filtered out before LLM calls via `filterCustomMessages`

### AgentRunner Lifecycle

In instance mode, create a runner, call `init()` to set up the sandbox/tools/history/Agent, then call `runTurn()` for each user message (returns `TAgentHandle` with steer/followUp/abort/waitForIdle). Use `updateConfig()` to hot-swap model/systemPrompt/tools between turns. Call `destroy()` to clean up. The static `AgentRunner.run()` wraps init+runTurn+auto-destroy for one-shot SSE endpoints.

### init Flow

Loads conversation history from DB, creates sandbox + tools if configured, creates web provider, builds all tools (sandbox + web + custom function), creates pi-mono model via `getModel()`, converts history to pi-mono Messages, builds streamFn/contextManager, creates Agent, and subscribes to events for streaming + persistence.

### runTurn Flow

Resolves active skills for this turn, wires abort signal, builds user content (text + images + files) and persists to DB, starts the agent loop (prompt → waitForIdle → transient retry loop → context overflow detection → drain persistence queue), and returns `TAgentHandle`.

## Key Types

All types are in `src/types/`. Key interfaces and their fields:

- **TAgentInitOpts** -- agentId, threadId, userId, orgId, db (IAgentRunnerDB), llmConfig (TLLMAdapterConfig), sandboxConfig?, tools?, environment? (TAgentEnvironment), onEvent, customFunctions?, onExecuteFunction?, skills?, memoryProvider? (IMemoryProvider, enables the memory tools)
- **TAgentTurnOpts** -- prompt, images?, files?, signal?
- **TAgentConfig** -- model?, provider?, systemPrompt?, thinkingLevel?, tools? (runtime-updatable between turns)
- **TAgentHandle** -- steer(message), followUp(message), abort(), waitForIdle()
- **TAgentRunOpts** -- TAgentInitOpts & TAgentTurnOpts & { maxSteps? } (one-shot mode)
- **IAgentRunnerDB** -- listMessages({ where: { threadId }, limit, offset }), createMessage({ threadId, type, content, orgId })
- **IWebProvider** -- type, search(query, maxResults?), fetch(url, opts?)
- **TAgentEnvironment** -- thinkingLevel, thinkingBudgets, contextBudgetPercent, contextCompaction, webProvider, maxRetries, cacheRetention

## Tools

### Sandbox Tools (createSandboxTools)

9 tools backed by an `ISandbox` instance: `shellExec`, `readFile`, `writeFile`, `listDir`, `deleteFile`, `mkdir`, `fileExists`, `evalCode` (V8 sandbox), `createArtifact` (renderable HTML/SVG/Markdown/code/etc.). Uses TypeBox for parameter schemas. Each calls `onUpdate()` for progress streaming.

### Web Tools (createWebTools)

2 tools backed by `IWebProvider`: `webSearch` (search → titles/URLs/snippets), `webFetch` (URL → cleaned markdown). Returns "not configured" gracefully when no provider.

### Memory Tools (createMemoryTools)

2 tools (`memorySearch`, `memoryWrite`) backed by an injected `IMemoryProvider` (`src/types/memory.types.ts`), added only when `opts.memoryProvider` is present. This is the api-brain memory path: the backend supplies the provider (scored search + write over the `memories` store); tool errors are logged and returned gracefully rather than thrown.

### JinaWebProvider

Implements `IWebProvider` using Jina AI APIs (search: `s.jina.ai`, fetch: `r.jina.ai`). Includes URL validation blocking private IPs, localhost, metadata endpoints, and non-http protocols.

### Custom Function Tools (buildCustomFunctionTools)

Converts `FunctionModel[]` into `AgentTool[]` delegating execution to a caller-provided `onExecuteFunction` callback. Supports 3 schema modes: inputSchema (rich typed), defaultArgs (legacy string params), generic fallback.

### Static Tool Definitions

`allToolDefs` / `getToolDefs(allowedTools?)` / `buildFunctionToolDefs(functions)` in `src/tools/definitions/`. 10 static `TLLMToolDef[]` across fs (6), shell (1), code (1), web (2). Used for API metadata, not runtime execution.

## Key Patterns

1. **Instance-based multi-turn sessions** -- Agent created once in `init()`, reused across `runTurn()` calls; `#pendingPersistence` queue batches DB writes drained after each turn
2. **Per-turn skill resolution** -- `resolveActiveSkills()` checks keyword matches + `alwaysActive` skills each turn, injecting instructions and merging tools
3. **Transient error retry loop** -- after `agent.waitForIdle()`, checks `isTransientError()`, retries up to `maxRetries` (default 2) with exponential backoff via `agent.continue()`
4. **Context overflow detection** -- `isContextOverflow()` from pi-mono checked after each turn, emits error event if exceeded
5. **Message persistence queue** -- `turn_end` events push to `#pendingPersistence`, drained after agent completes; failures logged but don't crash
6. **Pluggable persistence (IAgentRunnerDB)** -- narrow interface; backend passes direct DB calls, TSA delegates to backend API
7. **Custom message filtering** -- `filterCustomMessages` passed as `convertToLlm` to pi-mono Agent, strips artifact/notification/systemEvent roles before LLM calls

## Workspace Dependencies

| Package | Purpose |
|---------|---------|
| `@mariozechner/pi-agent-core` | Agent class, AgentEvent types, AgentTool interface, StreamFn, CustomAgentMessages |
| `@mariozechner/pi-ai` | getModel(), streamSimple(), isContextOverflow(), calculateCost(), Message types, TypeBox, ImageContent |
| `@tdsk/sandbox` | Sandbox execution (E2B, K8s, local providers) |
| `@tdsk/domain` | Shared types: TStreamEvent, TLLMToolDef, TMessageContent, TLLMAdapterConfig, TAgentEnvironment, ISandbox, FunctionModel, Skill, and all enums |
| `@tdsk/logger` | Winston logger via `buildApiLogger()` |

## Integration Points

- **Backend**: SSE endpoint calls `AgentRunner.run()` (static) with direct DB as `IAgentRunnerDB`; WebSocket session manager uses instance mode; provides `onExecuteFunction` callback and resolves web provider secrets
- **Sandbox**: `init()` creates sandbox via `createSandboxProvider(type).create(config)`; `createSandboxTools()` wraps `ISandbox` methods; sandbox created per-session, closed in `destroy()`
- **Domain**: TStreamEvent, TTokenUsage, TLLMToolDef, TMessageContent, TLLMAdapterConfig, TAgentEnvironment, TAgentConfigFields, ISandbox, FunctionModel, Skill, TImageAttachment, TFileAttachment, TWebProviderConfig, buildFallbackModel
- **TSA**: `LocalAgentExecutor` calls `AgentRunner.run()` (static) with HTTP-based `IAgentRunnerDB`

## Build & Test

```bash
cd repos/agent
pnpm build    # CJS bundle via tsup → dist/index.cjs
pnpm test     # Vitest (12 test files)
```
