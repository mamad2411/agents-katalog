# OpenAI Model Client

OpenAI-compatible `ModelClient` implementation that speaks the OpenAI
chat-completions wire shape to any provider that accepts it.

- Owns the `KotaMessage` / `KotaTool` ↔ OpenAI chat-completion wire-shape
  translation at the provider seam (see `src/core/agent-harness/AGENTS.md`).
  `translations.ts` is the single place that translation lives; wire-projection
  coverage lives in `translations.test.ts`.
- `stream.ts` normalizes the provider's streaming frames into
  `KotaModelResponse` via `buildKotaModelResponse()`; nothing in this
  subtree imports `@anthropic-ai/sdk`.
