---
name: workers-ai
description: Run AI inference at the edge with OpenAI SDK and Workers AI. Load when generating text with LLMs, extracting structured JSON from text, building chat interfaces, streaming AI responses, generating embeddings, or integrating GPT-4/Claude via AI Gateway.
---

# Workers AI

Run AI inference at the edge using Workers AI and industry-standard SDKs like OpenAI. Deploy LLM-powered applications with structured outputs, streaming responses, and AI Gateway integration.

## FIRST: Installation

```bash
npm install openai
```

**Optional dependencies for advanced use cases:**
```bash
npm install ai @ai-sdk/openai  # For streaming with Vercel AI SDK
```

## When to Use

| Use Case | Description |
|----------|-------------|
| Text Generation | Generate content, summaries, translations |
| Structured Extraction | Extract structured data from unstructured text |
| Chat Interfaces | Build conversational AI applications |
| Content Moderation | Analyze and filter user-generated content |
| Embeddings | Generate vector embeddings for semantic search |
| RAG Pipelines | Combine with Vectorize for retrieval-augmented generation |

## Quick Reference

| Task | API |
|------|-----|
| Structured JSON output | `response_format: { type: 'json_schema', schema }` |
| JSON mode (parse yourself) | `response_format: { type: 'json_object' }` |
| Stream responses | Use Vercel AI SDK's `streamText()` |
| Enable AI Gateway | Set `baseUrl` in OpenAI client config |
| Generate embeddings | `client.embeddings.create({ model, input })` |

## Structured JSON Outputs

Workers AI supports structured JSON outputs using the OpenAI SDK's `response_format` API. This ensures the model returns data matching your schema.

```typescript
import { OpenAI } from "openai";

interface Env {
  OPENAI_API_KEY: string;
}

// Define your JSON schema
const CalendarEventSchema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    date: { type: 'string' },
    participants: { type: 'array', items: { type: 'string' } },
  },
  required: ['name', 'date', 'participants']
};

export default {
  async fetch(request: Request, env: Env) {
    const client = new OpenAI({
      apiKey: env.OPENAI_API_KEY,
    });

    const response = await client.chat.completions.create({
      model: 'gpt-4o-2024-08-06',
      messages: [
        { role: 'system', content: 'Extract the event information.' },
        { role: 'user', content: 'Alice and Bob are going to a science fair on Friday.' },
      ],
      // Request structured JSON output with schema validation
      response_format: {
        type: 'json_schema',
        schema: CalendarEventSchema,
      },
    });

    // Parsed according to your schema
    const event = response.choices[0].message.parsed;

    return Response.json({
      calendar_event: event,
    });
  }
}
```

**wrangler.jsonc:**
```jsonc
{
  "name": "my-ai-app",
  "main": "src/index.ts",
  "compatibility_date": "2025-01-17",
  "observability": {
    "enabled": true
  }
}
```

## Streaming Responses

For real-time chat experiences, use streaming to send tokens as they're generated.

```typescript
import { OpenAI } from "openai";

interface Env {
  OPENAI_API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env) {
    const client = new OpenAI({
      apiKey: env.OPENAI_API_KEY,
    });

    const stream = await client.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'user', content: 'Tell me a story about the edge.' }
      ],
      stream: true,
    });

    // Create a ReadableStream for SSE
    const encoder = new TextEncoder();
    const readable = new ReadableStream({
      async start(controller) {
        try {
          for await (const chunk of stream) {
            const content = chunk.choices[0]?.delta?.content;
            if (content) {
              controller.enqueue(encoder.encode(`data: ${JSON.stringify({ content })}\n\n`));
            }
          }
          controller.enqueue(encoder.encode('data: [DONE]\n\n'));
          controller.close();
        } catch (error) {
          controller.error(error);
        }
      },
    });

    return new Response(readable, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  }
}
```

## AI Gateway Integration

AI Gateway provides caching, rate limiting, analytics, and request logging for your AI requests. Configure it by setting the `baseUrl` in your OpenAI client.

```typescript
import { OpenAI } from "openai";

interface Env {
  OPENAI_API_KEY: string;
  AI_GATEWAY_ACCOUNT_ID: string;
  AI_GATEWAY_ID: string;
}

export default {
  async fetch(request: Request, env: Env) {
    const client = new OpenAI({
      apiKey: env.OPENAI_API_KEY,
      // Route requests through AI Gateway
      baseUrl: `https://gateway.ai.cloudflare.com/v1/${env.AI_GATEWAY_ACCOUNT_ID}/${env.AI_GATEWAY_ID}/openai`
    });

    const response = await client.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'user', content: 'Hello, world!' }
      ],
    });

    return Response.json(response.choices[0].message);
  }
}
```

**Benefits of AI Gateway:**
- **Caching**: Reduce costs by caching identical requests
- **Rate Limiting**: Protect against abuse and control costs
- **Analytics**: Monitor token usage, latency, and error rates
- **Logging**: Inspect requests and responses for debugging
- **Multi-provider**: Works with OpenAI, Anthropic, Azure, and more

## Model Selection

Choose models based on your use case:

| Model Family | Best For | Structured Output Support |
|--------------|----------|---------------------------|
| GPT-4o | Complex reasoning, structured extraction | Yes |
| GPT-4o-mini | Fast, cost-effective tasks | Yes |
| GPT-3.5-turbo | Simple completions, high throughput | Limited |
| Claude 3.5 Sonnet | Long-form content, analysis | Via Anthropic SDK |
| Claude 3 Haiku | Fast responses, simple tasks | Via Anthropic SDK |

**Choosing the right model:**
- **Structured extraction**: Use GPT-4o with `json_schema`
- **Chat interfaces**: Use GPT-4o or Claude 3.5 Sonnet with streaming
- **High volume/low latency**: Use GPT-4o-mini or Claude 3 Haiku
- **Complex reasoning**: Use GPT-4o or Claude 3.5 Sonnet

## Response Formats

Workers AI supports multiple response format options:

```typescript
// Option 1: JSON Schema (recommended for structured extraction)
response_format: {
  type: 'json_schema',
  schema: {
    type: 'object',
    properties: {
      name: { type: 'string' },
      age: { type: 'number' },
    },
    required: ['name']
  }
}

// Option 2: JSON Object (parse manually)
response_format: {
  type: 'json_object'
}
// Remember to prompt the model to return JSON

// Option 3: Text (default)
// No response_format specified - returns plain text
```

## Generating Embeddings

Use embeddings for semantic search, RAG, and similarity matching. Combine with Vectorize for storage.

```typescript
import { OpenAI } from "openai";

interface Env {
  OPENAI_API_KEY: string;
  VECTORIZE: VectorizeIndex;
}

export default {
  async fetch(request: Request, env: Env) {
    const client = new OpenAI({
      apiKey: env.OPENAI_API_KEY,
    });

    const text = "Cloudflare Workers run at the edge";

    // Generate embedding
    const response = await client.embeddings.create({
      model: 'text-embedding-3-small',
      input: text,
    });

    const vector = response.data[0].embedding;

    // Store in Vectorize
    await env.VECTORIZE.upsert([
      {
        id: '1',
        values: vector,
        metadata: { text }
      }
    ]);

    return Response.json({ 
      dimensions: vector.length,
      stored: true 
    });
  }
}
```

**wrangler.jsonc with Vectorize binding:**
```jsonc
{
  "vectorize": [
    {
      "binding": "VECTORIZE",
      "index_name": "my-embeddings-index"
    }
  ]
}
```

## Error Handling

Always handle AI API errors gracefully:

```typescript
export default {
  async fetch(request: Request, env: Env) {
    const client = new OpenAI({
      apiKey: env.OPENAI_API_KEY,
    });

    try {
      const response = await client.chat.completions.create({
        model: 'gpt-4o',
        messages: [{ role: 'user', content: 'Hello!' }],
      });

      return Response.json(response.choices[0].message);
    } catch (error) {
      // Handle rate limits
      if (error.status === 429) {
        return Response.json(
          { error: 'Rate limit exceeded. Please try again later.' },
          { status: 429 }
        );
      }

      // Handle invalid requests
      if (error.status === 400) {
        return Response.json(
          { error: 'Invalid request. Check your parameters.' },
          { status: 400 }
        );
      }

      // Generic error
      console.error('AI request failed:', error);
      return Response.json(
        { error: 'Internal server error' },
        { status: 500 }
      );
    }
  }
}
```

## Detailed References

- **[references/models.md](references/models.md)** - Model capabilities, pricing, and selection guide
- **[references/streaming.md](references/streaming.md)** - Streaming patterns, SSE, and client integration
- **[references/dynamic-model-discovery.md](references/dynamic-model-discovery.md)** - Programmatically discover models and capabilities at runtime
- **[references/testing.md](references/testing.md)** - Mocking AI responses, remote bindings, testing different models

## Best Practices

1. **Use structured outputs**: Set `response_format` with `json_schema` for reliable data extraction
2. **Enable observability**: Set `observability.enabled: true` in wrangler.jsonc
3. **Stream for chat**: Use streaming responses for better user experience
4. **Cache with AI Gateway**: Route requests through AI Gateway to cache and monitor
5. **Handle errors**: Always catch and handle API errors gracefully
6. **Choose right model**: Balance cost, speed, and capability based on your use case
7. **Validate inputs**: Sanitize user inputs before sending to AI models
8. **Set timeouts**: Use appropriate timeouts for long-running requests
9. **Use embeddings wisely**: Batch embedding generation when possible
10. **Monitor token usage**: Track costs through AI Gateway analytics

## Integration Patterns

### Pattern 1: Chat with Message History

```typescript
interface Env {
  OPENAI_API_KEY: string;
  KV: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env) {
    const { userId, message } = await request.json();
    const client = new OpenAI({ apiKey: env.OPENAI_API_KEY });

    // Get message history from KV
    const historyJson = await env.KV.get(`chat:${userId}`);
    const history = historyJson ? JSON.parse(historyJson) : [];

    // Add user message
    history.push({ role: 'user', content: message });

    // Get AI response
    const response = await client.chat.completions.create({
      model: 'gpt-4o',
      messages: history,
    });

    const assistantMessage = response.choices[0].message;
    history.push(assistantMessage);

    // Store updated history
    await env.KV.put(`chat:${userId}`, JSON.stringify(history), {
      expirationTtl: 3600 // 1 hour
    });

    return Response.json({ message: assistantMessage.content });
  }
}
```

### Pattern 2: RAG with Vectorize

```typescript
interface Env {
  OPENAI_API_KEY: string;
  VECTORIZE: VectorizeIndex;
}

export default {
  async fetch(request: Request, env: Env) {
    const { query } = await request.json();
    const client = new OpenAI({ apiKey: env.OPENAI_API_KEY });

    // Generate query embedding
    const embeddingResponse = await client.embeddings.create({
      model: 'text-embedding-3-small',
      input: query,
    });

    // Search similar documents
    const results = await env.VECTORIZE.query(embeddingResponse.data[0].embedding, {
      topK: 3,
    });

    // Build context from results
    const context = results.matches
      .map(match => match.metadata.text)
      .join('\n\n');

    // Generate answer with context
    const response = await client.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { 
          role: 'system', 
          content: `Answer questions using this context:\n\n${context}` 
        },
        { role: 'user', content: query }
      ],
    });

    return Response.json({
      answer: response.choices[0].message.content,
      sources: results.matches.map(m => m.metadata),
    });
  }
}
```

## Common Pitfalls

1. **Not handling rate limits**: Always catch 429 errors and implement backoff
2. **Ignoring token limits**: Monitor and truncate input to stay within model limits
3. **Not caching**: Use AI Gateway or KV to cache responses for identical requests
4. **Blocking on responses**: Use streaming for better perceived performance
5. **Missing error boundaries**: Wrap AI calls in try-catch blocks
6. **Hardcoding API keys**: Always use environment bindings
7. **Not validating schemas**: Test your JSON schemas thoroughly
8. **Overfitting prompts**: Keep system prompts concise and clear
