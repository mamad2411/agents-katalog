---
name: local-llm-web-agent
description: "Build and integrate local LLM-powered agents with function-calling tools in web applications (Next.js + Ollama pattern)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ollama, local-llm, function-calling, agent, nextjs, tools]
    triggers:
      - local LLM
      - web agent
      - browser automation
      - AI agent
      - local inference
      - open-source model
      - Ollama
      - function calling
      - Next.js agent
    related_skills: [subagent-driven-development, systematic-debugging, building-mcp-servers]
---

# Local LLM Web Agent

## Overview

Integrate a **local LLM** (Ollama) as an intelligent AI assistant with **function-calling tools** inside a web application (Next.js API routes). The LLM receives tool definitions, decides which tool to call based on the user's natural language request, and the server executes the tool against the real data layer.

**Why local LLMs over cloud APIs:**
- No API key required (Ollama runs locally)
- Privacy (data never leaves your machine)
- After first load, subsequent requests are fast (model stays in VRAM)
- No rate limits or costs

**Trade-offs:**
- First call is slow (~55s for Gemma 4 to load from disk to VRAM)
- Requires GPU with sufficient VRAM (Gemma 4 ~24B needs ~16-20GB)
- Tool-calling quality varies by model (Gemma 4, Qwen, and Llama 3 work well)

## Architecture

```
Client POST {message, role}
  → Next.js API route
  → Build system prompt + tool definitions
  → POST to Ollama /api/chat (model: huihui_ai/gemma-4-abliterated:latest)
  → Parse tool_calls from response
  → Execute data-service function (getProjects, createTask, etc.)
  → Format {response, action, data, success, suggestions}
  → Return JSON
```

## Prerequisites

- Ollama installed and running (`curl http://localhost:11434/api/tags`)
- A model with function-calling support pulled (e.g., `huihui_ai/gemma-4-abliterated`, `llama3.2`, `qwen2.5`)
- Next.js project (App Router) with API routes

## Tool Definition Pattern

Define tools in OpenAI-compatible function-calling format. Each tool needs:
- `name` — short snake_case name matching the executor function
- `description` — what the tool does (the LLM reads this to decide)
- `parameters` — JSON Schema object describing required and optional fields

```typescript
interface ToolDef {
  type: 'function'
  function: {
    name: string
    description: string
    parameters: {
      type: 'object'
      properties: Record<string, {
        type: string
        description: string
        enum?: string[]
      }>
      required: string[]
    }
  }
}

const TOOLS: ToolDef[] = [
  {
    type: 'function',
    function: {
      name: 'get_projects',
      description: 'Get all projects, optionally filtered by status',
      parameters: {
        type: 'object',
        properties: {
          status: {
            type: 'string',
            description: 'Filter by status: planning, in-progress, on-hold, completed',
          },
        },
        required: [],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'create_project',
      description: 'Create a new construction project',
      parameters: {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'Project name' },
          client_email: { type: 'string', description: 'Client email (resolved to user ID server-side)' },
          status: { type: 'string', enum: ['planning', 'in-progress', 'on-hold', 'completed'] },
          // ... more fields
        },
        required: ['name'],
      },
    },
  },
]
```

## Calling Ollama

Ollama's `/api/chat` endpoint supports the `tools` parameter in the request body. The format is OpenAI-compatible for the request, but the response format differs.

### Request

```typescript
const OLLAMA_URL = 'http://localhost:11434/api/chat'

const body = {
  model: 'huihui_ai/gemma-4-abliterated:latest',
  messages: [
    { role: 'system', content: SYSTEM_PROMPT },
    { role: 'user', content: message },
  ],
  tools: TOOLS,
  stream: false,
  options: { num_predict: 2048 },
}

const res = await fetch(OLLAMA_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
})
```

### Response Parsing (Ollama ≠ OpenAI)

Ollama returns a **different shape** than OpenAI:

```typescript
// Ollama response shape:
{
  model: '...',
  message: {
    role: 'assistant',
    content: 'text response or empty string',
    tool_calls: [
      {
        function: {
          name: 'get_projects',
          arguments: { status: 'planning' }  // object, NOT JSON string!
        }
      }
    ]
  },
  done: true
}

// OpenAI response shape (for comparison):
{
  choices: [{
    message: {
      role: 'assistant',
      content: null,
      tool_calls: [{
        id: 'call_abc123',
        type: 'function',
        function: {
          name: 'get_projects',
          arguments: '{"status":"planning"}'  // JSON STRING!
        }
      }]
    },
    finish_reason: 'tool_calls'
  }]
}
```

**Key differences:**
1. Ollama returns `data.message` directly — no `data.choices[0].message` wrapper
2. Ollama's `tool_calls` items lack `id` and `type` fields
3. Ollama's `function.arguments` is a **parsed object**, not a JSON string
4. Ollama has no `finish_reason` field

**Normalize Ollama's response to OpenAI-like format:**

```typescript
const data = await res.json()
const message = data.message

return {
  message: {
    role: message.role,
    content: message.content || '',
    tool_calls: message.tool_calls?.map((tc, i) => ({
      id: tc.id || `call_${i}`,
      type: 'function' as const,
      function: {
        name: tc.function?.name || '',
        arguments: typeof tc.function?.arguments === 'string'
          ? tc.function.arguments
          : JSON.stringify(tc.function?.arguments || {}),
      },
    })),
  },
}
```

## Tool Executor Pattern

Dispatch tool calls to actual data-layer functions:

```typescript
const EXECUTORS: Record<string, (args: any) => Promise<any>> = {
  get_projects: async (args) => await getProjects(args.status || undefined),
  create_project: async (args) => {
    // Resolve email to user ID server-side (LLM doesn't know UUIDs)
    let clientId = args.client_id
    if (args.client_email && !clientId) {
      const users = await getUsers()
      const user = users.find(u => u.email?.toLowerCase() === args.client_email.toLowerCase())
      if (user) clientId = user.id
    }
    return await createProject({
      name: args.name,
      client_id: clientId,
      status: args.status || 'planning',
      // Provide defaults for NOT NULL date columns
      start_date: args.start_date || new Date().toISOString().split('T')[0],
      estimated_completion: args.estimated_completion ||
        new Date(Date.now() + 30 * 86400000).toISOString().split('T')[0],
    })
  },
  // ... more tools
}

async function executeToolCall(toolName: string, args: any) {
  const executor = EXECUTORS[toolName]
  if (!executor) throw new Error(`Unknown tool: ${toolName}`)
  return await executor(args)
}
```

**Key design insight:** When a tool needs a database UUID (like `client_id`), DON'T expect the LLM to know UUIDs. Accept a human-readable identifier (email, name) and resolve it server-side. Update the tool's `description` field to tell the LLM it can pass the email, and the executor handles the lookup.

## System Prompt Template

The system prompt should describe:
1. The assistant's role / persona
2. The tools available (a text summary of each)
3. What NOT to do (e.g., "don't make up IDs")
4. The response style expected

```
You are an intelligent assistant for [Company Name], helping manage [domain].
You have access to these tools:

1. get_projects — List projects, optionally by status
2. get_project — Get full details of a specific project
3. create_project — Add a new project. You can pass client_email to link a client.
4. update_project — Change project fields (status, priority, budget, etc.)
5. delete_project — Remove a project and its tasks
6. get_tasks — List tasks for a project
7. create_task — Add a task to a project
8. update_task — Change task status/details
9. delete_task — Remove a task
10. get_schedule — View scheduled items
11. get_notifications — View notifications
12. send_notification — Create a notification
13. get_weather — View weather data
14. get_users — List users by role
15. get_report — Get project summary stats

When you need to call a tool, respond with a single tool call.
Do NOT invent IDs or data — use the tools to query real information.
Be concise and helpful in your text responses.
```

## Response Formatting

After executing a tool, format the result for the frontend:

```typescript
function formatToolResponse(action: string, data: any) {
  const success = !!data

  switch (action) {
    case 'create_project':
      return {
        response: success
          ? `Project "${data.name}" has been created successfully.`
          : 'Failed to create the project. Check the details and try again.',
        action,
        data: data || null,
        success,
        suggestions: success
          ? ['Add tasks to the project', 'Schedule a start date', 'Assign a contractor']
          : ['Check the project name and try again'],
      }

    case 'get_projects': {
      const list = Array.isArray(data) ? data : []
      if (list.length === 0) {
        return { response: 'No projects found.', action, data: list, success: true, suggestions: ['Create a new project'] }
      }
      const summary = list.map(p => `  • ${p.name} — ${p.status} (${p.priority} priority)`).join('\n')
      return { response: `Found ${list.length} project(s):\n${summary}`, action, data: list, success, suggestions: [...] }
    }
    // ... more cases
  }
}
```

## POST Handler (Next.js API Route)

```typescript
export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { message, role = 'admin' } = body

    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      { role: 'user', content: message },
    ]

    const choice = await callOllama(messages)
    const assistantMessage = choice.message

    // If the model returned tool_calls, execute the first one
    if (assistantMessage.tool_calls?.length) {
      const toolCall = assistantMessage.tool_calls[0]
      const toolName = toolCall.function.name
      let toolArgs = {}
      try { toolArgs = JSON.parse(toolCall.function.arguments) } catch { toolArgs = {} }

      const result = await executeToolCall(toolName, toolArgs)
      return NextResponse.json(formatToolResponse(toolName, result))
    }

    // No tool call — return conversational response
    const text = assistantMessage.content || 'How can I help?'
    return NextResponse.json({ response: text, action: 'conversation', data: null, success: true })
  } catch (err) {
    return NextResponse.json({
      response: `Error: ${err instanceof Error ? err.message : 'Unknown error'}`,
      action: '', data: null, success: false,
    }, { status: 500 })
  }
}
```

## Next.js Middleware: API Routes Must Be Public

If your Next.js app has a middleware that checks for a session cookie, ALL API routes must be whitelisted — otherwise they redirect to `/login` as HTML pages instead of returning JSON:

```typescript
// middleware.ts
export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const publicRoutes = ['/', '/login', '/careers', '/api/auth', '/api']
  // NOTE: '/api' catches all /api/* routes via pathname.startsWith()
  if (publicRoutes.some(route => pathname.startsWith(route)) || pathname.startsWith('/_next')) {
    return NextResponse.next()
  }
  // ... session check / redirect
}
```

## PostgREST Pitfall: POST Returns No Body

When your data layer talks to PostgREST directly, POST requests return `null` even on success because PostgREST's default behavior is HTTP 201 with no body. Add the `Prefer: return=representation` header:

```typescript
const headers = { 'Content-Type': 'application/json' }
if (method === 'POST') headers['Prefer'] = 'return=representation'
```

## PostgREST Pitfall: DATE NOT NULL Columns

Columns declared as `DATE NOT NULL` reject empty strings. Always provide sensible defaults:

```typescript
start_date: args.start_date || new Date().toISOString().split('T')[0],
estimated_completion: args.estimated_completion ||
  new Date(Date.now() + 30 * 86400000).toISOString().split('T')[0],
```

## First-Call Performance

Ollama loads models lazily. The **first** request will take 50-60 seconds while the model loads from disk into VRAM. Subsequent requests are 12-25 seconds (model cached in VRAM). Design your timeout accordingly.

## Verification Checklist

- [ ] Ollama is running: `curl http://localhost:11434/api/tags`
- [ ] Model is pulled and supports tool calls
- [ ] First request succeeds (even if slow)
- [ ] Tool calls execute and return real data
- [ ] Empty tool args don't crash (try/catch JSON.parse)
- [ ] Fallback conversational response works when no tool is called
- [ ] Error responses are human-readable
- [ ] API route is NOT protected by session middleware
- [ ] System prompt accurately describes all available tools
- [ ] Tool descriptions include hints about human-readable identifiers (email, name) vs UUIDs

## Reference File

See `references/nextjs-ollama-agent-setup.md` for the full worked example from a production session: exact timing, error transcripts, port mapping, smoke test commands, and the complete layer-by-layer verification sequence.

## Pitfalls

- **Don't assume local LLM is preferred** — Some users explicitly prefer cloud inference (OpenRouter). When the user says "we want openrouter" or similar, do NOT set up an Ollama fallback path. Fallbacks that catch cloud 429 and redirect to local inference introduce latency variance (55s VRAM load) and dependency on local GPU resources. If the user objects, strip the fallback and use a reliable paid model via OpenRouter instead.
- **First-call timeout** — If retained, the first Ollama call after server restart takes 50-60s while the model loads from disk to VRAM. Set curl timeouts accordingly (min 90s for first call).
- **Tool-calling quality varies** — Gemma 4 (24B) and Qwen 2.5 work well for function calling. Smaller models (3B, 7B, 1B) produce malformed tool_calls or skip them entirely.

## Related Skills

- **subagent-driven-development** — Use delegate_task to build the data-service layer, tool definitions, and executors in parallel
- **systematic-debugging** — Use 4-phase debugging when tool calls fail silently
- **building-mcp-servers** — Alternative pattern: expose tools as MCP tools instead of custom API routes
