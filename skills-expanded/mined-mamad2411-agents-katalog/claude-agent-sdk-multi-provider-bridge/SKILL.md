---
name: claude-agent-sdk-multi-provider-bridge
description: Drive non-Anthropic providers (OpenRouter, Ollama, Vercel AI Gateway, any Anthropic-compatible endpoint) through the Claude Agent SDK by swapping base URL + auth env, and route Google/OpenAI/Copilot through a parallel Pi SDK backend with a shared AgentBackend interface.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [claude-agent-sdk, multi-provider, pi-sdk, backend-abstraction]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/agent/backend/factory.ts
imported_at: 2026-04-18T00:00:00Z
---

# Multi-provider agent behind one AgentBackend

## When to use
- App wants "use Claude, but also OpenAI, Gemini, Llama-via-Ollama, Codex, Copilot" without maintaining N bespoke client stacks.
- Claude Agent SDK already handles Claude and any Anthropic-compatible endpoint; a second SDK (Pi) covers OpenAI/Google/Copilot idioms.
- Need a single `AgentBackend` interface so session storage, tool dispatch, event adapters don't branch per provider.

## How it works
1. Define a common `AgentBackend` interface: `start(options)`, `query(messages)`, `abort()`, event stream, permission callbacks. Both `ClaudeAgent` and `PiAgent` implement it.
2. **Driver registry** keyed by `provider`:
   ```ts
   const DRIVER_REGISTRY: Record<AgentProvider, ProviderDriver> = {
     anthropic: anthropicDriver,
     pi: piDriver,
   };
   ```
3. Each LLM connection record carries `providerType` (`anthropic`, `openai`, `google`, `openrouter`, `groq`, `mistral`, `xai`, ...) and `authType` (`apiKey`, `oauth`, `claudeMax`, ...).
4. For Anthropic-family providers, `anthropicDriver` resolves the API key / OAuth token and sets `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` (or `ANTHROPIC_API_KEY`) before instantiating the Claude SDK. That's ALL it takes to point at OpenRouter or Ollama.
5. For Pi-family providers, `piDriver` configures `@mariozechner/pi-ai` with provider-specific auth (`GOOGLE_API_KEY`, Codex OAuth, Copilot device-code flow).
6. A shared **event adapter** translates each SDK's stream into the app's normalized `AgentEvent` type; Claude and Pi have separate adapters but produce the same output shape.

## Example
```ts
// Configure Claude SDK to talk to OpenRouter:
const env = {
  ...process.env,
  ANTHROPIC_BASE_URL: 'https://openrouter.ai/api/v1',
  ANTHROPIC_AUTH_TOKEN: userOpenRouterKey,
};
const q = query({ prompt, options: { ...base, model: 'anthropic/claude-opus-4.7' } });
```

```ts
// Shared dispatch
function createAgent(conn: LlmConnection): AgentBackend {
  const driver = DRIVER_REGISTRY[getProvider(conn.providerType)];
  return driver.create(conn);
}
```

## Gotchas
- OpenRouter uses `provider/model-name` slugs, not bare model names - surface that in the UI.
- Ollama has no auth; pass an empty string for `ANTHROPIC_AUTH_TOKEN` but the env var must exist or the SDK will complain.
- The Pi SDK is ESM-only; your build pipeline needs `bun build --target=bun --format=esm` or it breaks at runtime.
- Don't leak provider-specific fields through the event adapter - keep `AgentEvent` canonical so UI code doesn't sprout `if (provider === …)`.
