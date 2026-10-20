---
description: Provider adapters, Context Compiler, streaming, receipts, OpenRouter
globs: "packages/ai-gateway/**"
alwaysApply: false
---

# AI Gateway

Adapters implement one interface: `listModels`, `chatStream`, `testConnection`, `capabilities`. Add providers **inside this package**, not as new packages.

- OpenRouter is first-class (not a hidden custom base URL). Native OpenAI/Anthropic/Gemini/Groq still exist.
- `chatStream` must support abort. Persist tokens in batches (`streaming | interrupted | complete | aborted`).
- Context Compiler: `compile(input) → ProviderAgnosticPacket`. Switching models uses the packet, not pasted recap.
- Every completed/errored attempt writes a **receipt**: provider, model, tokens in/out, latency, estimated cost. No secrets in receipts.
- Cost catalog lives in `packages/shared`. Prefer provider-reported usage when present.
- Map SDK failures to the error taxonomy. Never swallow. Never switch model inside the adapter.

Unit tests use stream fixtures — **no live API keys in CI**.
