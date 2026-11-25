# SIMOSphere AI integration — Cursor rules

When working in a project that uses the SIMOSphere AI API
(`api.simosphereai.com`), apply the following rules.

## Base URL + auth

- Always set `base_url` / `baseURL` to `https://api.simosphereai.com/v1`.
- Read the API key from `process.env.SIMO_API_KEY` (Node) or
  `os.environ["SIMO_API_KEY"]` (Python). Never hardcode `sk-simo-…`.
- The API accepts `Authorization: Bearer sk-simo-…` and
  `X-API-Key: sk-simo-…` interchangeably.

## SDK choice

- Use the official `openai` SDK with the base-URL override. Do not
  reinvent the HTTP client.

## Model defaults

- Default to `qwen/qwen3-8b` unless the user names a different model.
- For premium reasoning, use `qwen/qwen3-30b` and warn about the price
  jump (€0.40/€1.60 vs €0.15/€0.60 per 1M tokens).

## Rate limits

- Read `X-RateLimit-Remaining` from every response when generating code
  that makes >10 req/min. Self-throttle rather than retrying on 429
  blindly. Honour `Retry-After`.

## Errors

- Parse `response.json().error` (OpenAI envelope shape). Do not display
  raw HTML to users — every endpoint returns JSON.

## Streaming

- For chat-style UX, prefer `stream=True`. Chunks are OpenAI delta
  shape. Terminate on `data: [DONE]`.

## Things NOT to do

- Do not call SIMOSphere AI from browser code without a backend proxy
  (the API key would leak into the bundle).
- Do not generate BYOK code that hard-codes upstream OpenAI/Anthropic
  keys — those are tenant-configured in the dashboard.
- Do not assume features that the base 8B model lacks (large context,
  vision). Check `/v1/models` first or read
  https://onboarding.simosphereai.com/llms-full.txt.
