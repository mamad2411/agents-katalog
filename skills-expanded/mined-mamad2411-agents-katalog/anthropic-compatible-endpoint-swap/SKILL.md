---
name: anthropic-compatible-endpoint-swap
description: Point the Claude Agent SDK at any Anthropic-compatible endpoint (OpenRouter, Vercel AI Gateway, Ollama, custom) by setting ANTHROPIC_BASE_URL + ANTHROPIC_AUTH_TOKEN before instantiating — no SDK changes, no adapter layer.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [claude-agent-sdk, openrouter, ollama, base-url, byoc]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/agent/backend/internal/drivers/anthropic.ts
imported_at: 2026-04-18T00:00:00Z
---

# Anthropic-compatible endpoint swap

## When to use
- Want to reuse the Claude Agent SDK's tool loop / session handling, but route LLM calls to a non-Anthropic provider (OpenRouter, Vercel AI Gateway, self-hosted Ollama, internal proxy).
- Building an app that offers "bring your own API key" for multiple providers.
- Need to bypass Anthropic for on-prem / cost / compliance reasons while keeping the same SDK.

## How it works
The SDK reads two env vars before every request:
- `ANTHROPIC_BASE_URL` - the API endpoint to call (default `https://api.anthropic.com`).
- `ANTHROPIC_AUTH_TOKEN` or `ANTHROPIC_API_KEY` - the auth header value.

Set these in the SDK subprocess env and it transparently talks to whatever endpoint you point at, as long as the endpoint accepts Anthropic's request/response format (which most gateways do).

1. Resolve the user's selected connection: `{ providerType: 'openrouter', apiKey: '...', baseUrl: 'https://openrouter.ai/api' }`.
2. Before `query()` / `new Anthropic()`, set:
   ```ts
   process.env.ANTHROPIC_BASE_URL = baseUrl;
   process.env.ANTHROPIC_AUTH_TOKEN = apiKey;
   ```
3. If you're spawning a subprocess, pass them via spawn env instead.
4. Model IDs may differ per provider (OpenRouter uses `anthropic/claude-opus-4.7`); expose the full model string in UI so users aren't guessing.
5. `clearClaudeBedrockRoutingEnvVars()` helper removes any leftover `CLAUDE_CODE_USE_BEDROCK=1` / `AWS_REGION` env that could mis-route.

## Example
```ts
function resolveAuthEnv(conn: LlmConnection): Record<string, string> {
  switch (conn.providerType) {
    case 'anthropic':   return { ANTHROPIC_API_KEY: conn.apiKey };
    case 'openrouter':  return {
      ANTHROPIC_BASE_URL: 'https://openrouter.ai/api/v1',
      ANTHROPIC_AUTH_TOKEN: conn.apiKey,
    };
    case 'ollama':      return {
      ANTHROPIC_BASE_URL: 'http://localhost:11434/v1',
      ANTHROPIC_AUTH_TOKEN: '',
    };
    case 'custom':      return {
      ANTHROPIC_BASE_URL: conn.baseUrl,
      ANTHROPIC_AUTH_TOKEN: conn.apiKey ?? '',
    };
  }
}
```

## Gotchas
- `ANTHROPIC_AUTH_TOKEN` vs `ANTHROPIC_API_KEY` - SDK accepts both, but AUTH_TOKEN is treated as a raw bearer (good for OpenRouter) while API_KEY gets prefixed. Some gateways are strict about the Authorization header format.
- Ollama expects no auth; pass empty string, not `undefined`, or the SDK may skip setting the header at all and fail on strict endpoints that require it.
- Rate limits, feature support (vision, tools, streaming) vary per endpoint - some gateways are "kinda compatible". Test with YOUR tool set.
- Clear Bedrock env vars if users might switch - `CLAUDE_CODE_USE_BEDROCK=1` will override your base URL even if you set it.
- OpenRouter routes by model slug; the model ID tells OpenRouter which provider to forward to.
