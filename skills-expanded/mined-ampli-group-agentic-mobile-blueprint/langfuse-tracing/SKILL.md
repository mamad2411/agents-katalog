---
name: langfuse-tracing
description: Add Langfuse observability and tracing to AI operations in Supabase Edge Functions. Use when creating functions with LLM calls that need monitoring, cost tracking, or debugging.
---

# Langfuse Tracing for AI Operations

## Available Modules

```
_shared/langfuse/
├── shared.ts      # Base: Tracer, withTrace()
├── gemini.ts      # Gemini: text, tools, images
├── anthropic.ts   # Anthropic: Claude text, tools
└── openai.ts      # OpenAI: text, tools, images
```

## Basic Usage

### Wrap Function with Tracing

```typescript
import { withTrace, traceLLMGemini } from '../_shared/langfuse/gemini.ts';

Deno.serve(async (req: Request) => {
  return await withTrace(
    {
      name: 'my-function',
      userId: user.id,
      sessionId: item_id,
      input: { prompt: 'analyze this' },
      metadata: { function: 'my-function' },
      tags: ['ai', 'analysis'],
    },
    async (tracer) => {
      // Your AI calls here
      const { text } = await traceLLMGemini(tracer, {
        model: 'gemini-2.5-flash',
        messages: [{ role: 'user', content: 'Hello' }],
      });
      
      return new Response(JSON.stringify({ result: text }));
    }
  );
});
```

### Gemini: Text Completion

```typescript
const { text, usage } = await traceLLMGemini(tracer, {
  model: 'gemini-2.5-flash',
  messages: [{ role: 'user', content: 'Summarize this' }],
  temperature: 0.7,
  maxTokens: 500,
});
```

### Gemini: Structured Output

```typescript
const { data } = await traceLLMGemini<{ title: string; price: number }>(tracer, {
  model: 'gemini-2.5-flash',
  messages: [{ role: 'user', content: 'Extract product info' }],
  schema: {
    type: 'object',
    properties: {
      title: { type: 'string' },
      price: { type: 'number' },
    },
    required: ['title', 'price'],
  },
});
// data.title, data.price are typed!
```

### Gemini: Function Calling

```typescript
const result = await traceLLMWithToolsGemini(tracer, 'agent-name', {
  model: 'gemini-2.5-flash',
  messages: [{ role: 'user', content: 'Get weather in SF' }],
  tools: [{
    name: 'get_weather',
    description: 'Get current weather',
    parameters: {
      type: 'object',
      properties: { location: { type: 'string' } },
      required: ['location'],
    },
  }],
});

if (result.message.tool_calls) {
  // Execute tools
}
```

## What Gets Tracked

✅ **Traces:** Function execution with nested operations  
✅ **Generations:** LLM calls with prompts and responses  
✅ **Usage:** Token counts and costs  
✅ **Latency:** Timing for each operation  
✅ **Metadata:** Custom tags and context  
✅ **Errors:** Automatic error tracking

## Setup

Set environment variables in `.env.local`:

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxx
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Available Functions

**Gemini:** `traceLLMGemini`, `streamLLMGemini`, `traceLLMWithToolsGemini`, `traceImageEditGemini`  
**Anthropic:** `traceLLMAnthropic`, `streamLLMAnthropic`, `traceLLMWithToolsAnthropic`  
**OpenAI:** `traceLLMOpenAI`, `streamLLMOpenAI`, `traceLLMWithToolsOpenAI`, `traceImageEditOpenAI`
