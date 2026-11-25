---
name: tpl-ai-ml-openai-api-integration
description: Template do pack (ai-ml/02-openai-api-integration.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/02-openai-api-integration.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: OpenAI API Integration (Node.js + TypeScript + Zod + Redis caching)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/02-openai-api-integration.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Runtime:** Node.js 20 + TypeScript 5.x (strict)
- **SDK:** openai v4 (official)
- **Schema Validation:** Zod 3.x (structured outputs)
- **Caching:** Redis 7 (ioredis) — cache completions by prompt hash
- **Rate Limiting:** Express-rate-limit + sliding window
- **Retry:** Custom exponential backoff on 429/500
- **Moderation:** OpenAI Moderation API (pre-user-input check)

---

## PROJECT STRUCTURE
```
src/
├── lib/
│   ├── openai.ts           # OpenAI client singleton + config
│   ├── cache.ts            # Redis completion caching
│   ├── moderation.ts       # Input moderation
│   └── cost.ts             # Token cost estimation
├── services/
│   ├── chat.ts             # Chat completions service
│   ├── extraction.ts       # Structured output extraction
│   └── streaming.ts        # Streaming completions
├── schemas/
│   └── outputs.ts          # Zod schemas for structured outputs
└── utils/
    ├── retry.ts
    └── tokenCount.ts
```

---

## ARCHITECTURE RULES
1. **Single OpenAI client instance** — instantiate once, import everywhere. Never `new OpenAI()` per request.
2. **Estimate tokens BEFORE the call** — reject requests that would exceed budget. Never surprise with a $50 call.
3. **Moderate user input before sending** — always run Moderation API on user-provided content.
4. **Cache deterministic calls** — `temperature=0` + same prompt = cacheable. TTL 1 hour minimum.
5. **Stream long responses** — never block for 30s waiting for a full response; stream to client.
6. **Structured output via `response_format`** — use Zod + `zodResponseFormat` for data extraction; never regex-parse JSON strings.
7. **Error handling is mandatory** — distinguish `RateLimitError`, `APIError`, `AuthenticationError`. Don't swallow all as 500.
8. **Track cost per feature** — tag every call with `metadata.feature`; aggregate in Redis/Postgres.

---

## OPENAI CLIENT SINGLETON

```typescript
// src/lib/openai.ts
import OpenAI from 'openai'
import { logger } from './logger'

if (!process.env.OPENAI_API_KEY) {
  throw new Error('OPENAI_API_KEY environment variable is required')
}

export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  maxRetries: 3,        // Built-in retry for 429 + 500
  timeout: 30_000,      // 30s timeout per request
})

// Model pricing table (USD per 1K tokens) — update quarterly
export const MODEL_PRICING: Record<string, { input: number; output: number }> = {
  'gpt-5.4':         { input: 0.005,   output: 0.015 },
  'gpt-5.4-mini':    { input: 0.00015, output: 0.0006 },
  'gpt-5.4-nano':    { input: 0.005,   output: 0.02 },
  'o3-pro':          { input: 0.015,   output: 0.06 },
}

export function estimateCost(
  model: string,
  inputTokens: number,
  outputTokens: number,
): number {
  const pricing = MODEL_PRICING[model] ?? MODEL_PRICING['gpt-5.4']
  return (inputTokens / 1000) * pricing.input + (outputTokens / 1000) * pricing.output
}
```

---

## TOKEN ESTIMATION (BEFORE THE CALL)

```typescript
// src/utils/tokenCount.ts
import { encoding_for_model, TiktokenModel } from 'tiktoken'

const BUDGET_LIMITS: Record<string, number> = {
  'gpt-5.4':      0.50,    // Max $0.50 per single call
  'gpt-5.4-mini': 0.05,
}

export function estimateInputTokens(text: string, model: string = 'gpt-5.4'): number {
  const enc = encoding_for_model(model as TiktokenModel)
  const tokens = enc.encode(text).length
  enc.free()
  return tokens
}

export function assertWithinBudget(
  model: string,
  inputTokens: number,
  expectedMaxOutputTokens: number,
): void {
  const { input, output } = MODEL_PRICING[model] ?? MODEL_PRICING['gpt-5.4']
  const estimatedCost =
    (inputTokens / 1000) * input + (expectedMaxOutputTokens / 1000) * output
  const limit = BUDGET_LIMITS[model] ?? 0.50

  if (estimatedCost > limit) {
    throw new Error(
      `Estimated cost $${estimatedCost.toFixed(4)} exceeds limit $${limit} for model ${model}`,
    )
  }
}
```

---

## MODERATION

```typescript
// src/lib/moderation.ts
import { openai } from './openai'

export class ContentPolicyError extends Error {
  constructor(public categories: Record<string, boolean>) {
    super('Content violates usage policy')
    this.name = 'ContentPolicyError'
  }
}

export async function moderateInput(text: string): Promise<void> {
  const response = await openai.moderations.create({ input: text })
  const result = response.results[0]

  if (result.flagged) {
    const flaggedCategories = Object.entries(result.categories)
      .filter(([, flagged]) => flagged)
      .reduce((acc, [key, val]) => ({ ...acc, [key]: val }), {})

    throw new ContentPolicyError(flaggedCategories)
  }
}
```

---

## STRUCTURED OUTPUTS WITH ZOD

```typescript
// src/schemas/outputs.ts
import { z } from 'zod'

export const ProductExtractionSchema = z.object({
  name: z.string().describe('Product name as stated in the text'),
  price: z.number().nullable().describe('Price in USD, null if not mentioned'),
  features: z.array(z.string()).describe('List of product features'),
  sentiment: z.enum(['positive', 'neutral', 'negative']).describe('Overall product sentiment'),
})

export type ProductExtraction = z.infer<typeof ProductExtractionSchema>
```

```typescript
// src/services/extraction.ts
import { openai } from '../lib/openai'
import { zodResponseFormat } from 'openai/helpers/zod'
import { ProductExtractionSchema, type ProductExtraction } from '../schemas/outputs'
import { moderateInput } from '../lib/moderation'
import { assertWithinBudget, estimateInputTokens } from '../utils/tokenCount'

export async function extractProductInfo(text: string): Promise<ProductExtraction> {
  // 1. Moderate user input before sending to LLM
  await moderateInput(text)

  // 2. Estimate and check budget
  const inputTokens = estimateInputTokens(text)
  assertWithinBudget('gpt-5.4-mini', inputTokens, 500)

  // 3. Call with structured output
  const completion = await openai.beta.chat.completions.parse({
    model: 'gpt-5.4-mini',
    temperature: 0,
    messages: [
      {
        role: 'system',
        content: 'Extract product information from the provided text. Return null for missing fields.',
      },
      { role: 'user', content: text },
    ],
    response_format: zodResponseFormat(ProductExtractionSchema, 'product_extraction'),
  })

  const parsed = completion.choices[0].message.parsed
  if (!parsed) throw new Error('Failed to parse structured output')

  return parsed
}
```

---

## REDIS CACHING

```typescript
// src/lib/cache.ts
import { Redis } from 'ioredis'
import { createHash } from 'crypto'

const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379')

const CACHE_TTL = 3600   // 1 hour

export function buildCacheKey(model: string, messages: object, temperature: number): string {
  if (temperature !== 0) return ''   // Only cache deterministic calls
  const hash = createHash('sha256')
    .update(JSON.stringify({ model, messages }))
    .digest('hex')
  return `llm:cache:${hash}`
}

export async function getCached<T>(key: string): Promise<T | null> {
  if (!key) return null
  const cached = await redis.get(key)
  return cached ? JSON.parse(cached) as T : null
}

export async function setCached<T>(key: string, value: T): Promise<void> {
  if (!key) return
  await redis.setex(key, CACHE_TTL, JSON.stringify(value))
}
```

---

## STREAMING COMPLETIONS

```typescript
// src/services/streaming.ts — SSE endpoint
import { openai } from '../lib/openai'
import type { Response } from 'express'

export async function streamChatResponse(
  userMessage: string,
  res: Response,
): Promise<void> {
  res.setHeader('Content-Type', 'text/event-stream')
  res.setHeader('Cache-Control', 'no-cache')
  res.setHeader('Connection', 'keep-alive')

  const stream = openai.beta.chat.completions.stream({
    model: 'gpt-5.4',
    messages: [{ role: 'user', content: userMessage }],
    max_tokens: 1024,
  })

  for await (const chunk of stream) {
    const delta = chunk.choices[0]?.delta?.content
    if (delta) {
      res.write(`data: ${JSON.stringify({ text: delta })}\n\n`)
    }
  }

  const finalCompletion = await stream.finalChatCompletion()
  const usage = finalCompletion.usage

  // Log token usage after stream completes
  logger.info({
    event: 'stream_complete',
    input_tokens: usage?.prompt_tokens,
    output_tokens: usage?.completion_tokens,
  })

  res.write('data: [DONE]\n\n')
  res.end()
}
```

---

## FUNCTION CALLING PATTERN

```typescript
// src/services/chat.ts — function calling
const tools: OpenAI.Chat.ChatCompletionTool[] = [
  {
    type: 'function',
    function: {
      name: 'get_weather',
      description: 'Get current weather for a city',
      parameters: {
        type: 'object',
        properties: {
          city: { type: 'string', description: 'City name' },
          unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
        },
        required: ['city'],
        additionalProperties: false,
      },
      strict: true,   // Strict mode: guaranteed JSON schema adherence
    },
  },
]

async function chatWithTools(userMessage: string): Promise<string> {
  const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
    { role: 'user', content: userMessage },
  ]

  const response = await openai.chat.completions.create({
    model: 'gpt-5.4',
    messages,
    tools,
    tool_choice: 'auto',
  })

  const toolCalls = response.choices[0].message.tool_calls
  if (!toolCalls?.length) return response.choices[0].message.content ?? ''

  // Execute tool calls
  messages.push(response.choices[0].message)   // Append assistant message

  for (const toolCall of toolCalls) {
    const args = JSON.parse(toolCall.function.arguments)
    const result = await executeToolCall(toolCall.function.name, args)
    messages.push({
      role: 'tool',
      tool_call_id: toolCall.id,
      content: JSON.stringify(result),
    })
  }

  // Second LLM call with tool results
  const finalResponse = await openai.chat.completions.create({ model: 'gpt-5.4', messages })
  return finalResponse.choices[0].message.content ?? ''
}
```

---

## ERROR HANDLING

```typescript
import OpenAI from 'openai'

export function handleOpenAIError(error: unknown): never {
  if (error instanceof OpenAI.RateLimitError) {
    throw new Error(`Rate limit exceeded. Retry after: ${error.headers?.['retry-after']}s`)
  }
  if (error instanceof OpenAI.AuthenticationError) {
    throw new Error('Invalid OpenAI API key. Check OPENAI_API_KEY env var.')
  }
  if (error instanceof OpenAI.BadRequestError) {
    throw new Error(`Bad request: ${error.message}`)
  }
  if (error instanceof OpenAI.APIConnectionError) {
    throw new Error('Network error connecting to OpenAI. Check connectivity.')
  }
  throw error   // Re-throw unknown errors
}
```
