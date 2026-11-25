---
name: workers-ai
description: >
  Write Cloudflare Workers AI and AI Gateway code for model inference, prompts, streaming, token budgets, model selection, observability, and fallback design. Use when adding LLM, embeddings, summarization, classification, or generation to Workers.
compatibility: "Cloudflare Workers TypeScript projects using Wrangler; verify current Cloudflare APIs, limits, and pricing before production use."
metadata:
  source: "Architecting on Cloudflare plus official Cloudflare Developer Platform docs"
  generated: "2026-04-28"
---
# Workers AI

Use this skill when adding AI inference to a Worker. Separate model selection, prompt design, cost control, and observability.

## Decision rules

- Use Workers AI when operational simplicity, binding-based access, and Cloudflare-native deployment matter.
- Use AI Gateway when requests need centralized observability, caching, rate controls, fallback, or multi-provider routing.
- Use external model providers when required model quality, fine-tuning, modalities, or SLAs exceed Workers AI's fit.
- Do not assume edge inference is automatically low latency for every model or geography; measure.

## Binding

```jsonc
{
  "ai": { "binding": "AI" }
}
```

```ts
export interface Env {
  AI: Ai;
}
```

## Text generation pattern

```ts
export async function answerQuestion(env: Env, question: string) {
  const response = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
    messages: [
      { role: "system", content: "Answer clearly and concisely. Do not invent facts." },
      { role: "user", content: question }
    ],
    max_tokens: 512
  });

  return response;
}
```

Verify model IDs and parameter names against the current model catalog.

## Embeddings pattern

```ts
export async function embed(env: Env, text: string) {
  const result = await env.AI.run("@cf/baai/bge-base-en-v1.5", { text });
  return result.data[0];
}
```

## Prompt safety and output shape

- Put invariant rules in the system message.
- Include the user's task and constraints explicitly.
- For JSON output, ask for a schema and validate the result after parsing.
- Never trust model output for authorization, billing, or safety-critical decisions without deterministic checks.
- Add token caps and refusal/unknown behavior.

## Observability

Log:

- Model name.
- Request ID.
- Tenant/user ID hash or safe identifier.
- Prompt class, not necessarily full prompt text.
- Token counts where available.
- Latency and error type.
- Fallback path.

## Cost controls

- Summarize or retrieve context before generation.
- Set `max_tokens`.
- Cache deterministic or public AI results where safe.
- Use smaller/cheaper models for classification and routing.
- Avoid sending entire documents when chunks will do.

## Anti-patterns

- Blindly forwarding user input and trusting the answer.
- Using generation for deterministic validation that should be code.
- No model fallback or user-visible error strategy.
- No token budget.
- RAG prompt includes retrieved text but answer is not constrained to it.
