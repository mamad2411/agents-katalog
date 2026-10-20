---
description: Run LLM Integration and AI Security Standards Check
globs: ['**/ai/**/*.ts', '**/llm/**/*.ts', '**/openai/**/*.ts', '**/anthropic/**/*.ts']
---

# AI: LLM Integration & Security Standards

<audit_rules>

- You MUST implement prompt injection defenses using input sanitization, prompt templating, and instruction following techniques.
- You MUST configure API key security with proper rotation, environment variable storage, and access logging.
- You MUST implement output validation and content filtering to prevent harmful or inappropriate responses.
- You MUST enforce rate limiting and cost controls to prevent unbounded consumption and budget overruns.
- You MUST implement proper error handling that doesn't expose sensitive prompts or system information.
- You MUST ensure all LLM interactions are logged for audit trails and debugging purposes.
- You MUST implement caching for repeated queries to reduce costs and improve response times.
- You MUST validate and sanitize all user inputs before sending them to LLM APIs.
- You MUST implement fallback mechanisms when LLM services are unavailable or rate-limited.
- You MUST ensure compliance with data privacy regulations when sending data to third-party AI services.
- For RAG (retrieval-augmented generation): You MUST enforce retrieval boundaries and source validation so retrieved context cannot override system instructions; validate and sanitize content before embedding or after retrieval.
- For vector stores and embeddings: You MUST enforce access control on vector DBs and embedding APIs; prevent injection of malicious or misleading content via embeddings; do not trust retrieved chunks without validation when feeding to the LLM.
  </audit_rules>

<reference_standards>

- Align with [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) (e.g. prompt injection, insecure output, overreliance on LLM, model denial of service / unbounded consumption, supply chain, sensitive info disclosure).
  </reference_standards>

<example_good>

```typescript
// Server-side rate limiting and token restriction
import { rateLimit } from '@/lib/rate-limit'

export async function POST(req: Request) {
  const { success } = await rateLimit(req.headers.get('x-forwarded-for'))
  if (!success) return new Response('Rate limit exceeded', { status: 429 })

  const { prompt } = await req.json()
  if (prompt.length > 1000) return new Response('Prompt too long', { status: 400 })

  // Proceed with LLM call
}
```

</example_good>

<example_bad>

```typescript
// BAD: Exposing AI without limits
export async function POST(req: Request) {
  const { prompt } = await req.json()
  // Unrestricted LLM call vulnerable to cost attacks
  const completion = await openai.completions.create({ prompt })
  return NextResponse.json(completion)
}
```

</example_bad>
