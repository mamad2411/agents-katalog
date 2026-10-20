---
name: typescript-api-patterns
description: "When to activate: REST API client, type-safe fetch, Zod validation, OpenAPI codegen, Axios, error handling for HTTP"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: typescript
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# TypeScript API Client Patterns

## Type-Safe Fetch Client
```ts
import { z } from 'zod'

class ApiClient {
  constructor(
    private baseUrl: string,
    private defaultHeaders: Record<string, string> = {}
  ) {}

  private async request<T>(
    method: string,
    path: string,
    options: { body?: unknown; params?: Record<string, string>; schema?: z.ZodType<T> } = {}
  ): Promise<T> {
    const url = new URL(path, this.baseUrl)
    if (options.params) {
      Object.entries(options.params).forEach(([k, v]) => url.searchParams.set(k, v))
    }

    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...this.defaultHeaders,
      },
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: AbortSignal.timeout(10_000),
    })

    if (!res.ok) {
      const text = await res.text()
      throw new ApiError(res.status, res.statusText, text)
    }

    const data = await res.json()
    return options.schema ? options.schema.parse(data) : data as T
  }

  get<T>(path: string, params?: Record<string, string>, schema?: z.ZodType<T>) {
    return this.request<T>('GET', path, { params, schema })
  }

  post<T>(path: string, body: unknown, schema?: z.ZodType<T>) {
    return this.request<T>('POST', path, { body, schema })
  }

  patch<T>(path: string, body: unknown, schema?: z.ZodType<T>) {
    return this.request<T>('PATCH', path, { body, schema })
  }

  delete<T>(path: string) {
    return this.request<T>('DELETE', path)
  }
}

export class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public body: string
  ) {
    super(`HTTP ${status}: ${statusText}`)
  }
}
```

## Domain API Layer
```ts
// api/users.ts
const UserSchema = z.object({
  id:        z.string(),
  email:     z.string().email(),
  name:      z.string(),
  role:      z.enum(['user', 'admin']),
  createdAt: z.string().transform(v => new Date(v)),
})

const UsersPageSchema = z.object({
  users:   z.array(UserSchema),
  total:   z.number(),
  page:    z.number(),
  limit:   z.number(),
})

export function createUsersApi(client: ApiClient) {
  return {
    list: (page = 1, limit = 20) =>
      client.get('/users', { page: String(page), limit: String(limit) }, UsersPageSchema),

    getById: (id: string) =>
      client.get(`/users/${id}`, undefined, UserSchema),

    create: (data: { name: string; email: string }) =>
      client.post('/users', data, UserSchema),

    update: (id: string, data: Partial<{ name: string }>) =>
      client.patch(`/users/${id}`, data, UserSchema),

    delete: (id: string) =>
      client.delete(`/users/${id}`),
  }
}

// Usage
const apiClient = new ApiClient('https://api.example.com', {
  Authorization: `Bearer ${token}`,
})
const usersApi = createUsersApi(apiClient)
const page = await usersApi.list(1, 20)
```

## Interceptors / Middleware
```ts
type RequestMiddleware = (req: RequestInit & { url: string }) => RequestInit & { url: string }
type ResponseMiddleware = (res: Response) => Response | Promise<Response>

class EnhancedClient {
  private requestMiddleware: RequestMiddleware[] = []
  private responseMiddleware: ResponseMiddleware[] = []

  use(mw: RequestMiddleware)  { this.requestMiddleware.push(mw); return this }
  useResponse(mw: ResponseMiddleware) { this.responseMiddleware.push(mw); return this }

  async fetch(url: string, init: RequestInit = {}) {
    let config = { url, ...init }
    for (const mw of this.requestMiddleware) config = mw(config) as typeof config

    let response = await fetch(config.url, config)
    for (const mw of this.responseMiddleware) response = await mw(response)
    return response
  }
}

const client = new EnhancedClient()
  .use(req => ({ ...req, headers: { ...req.headers as any, 'X-Request-Id': crypto.randomUUID() } }))
  .useResponse(async res => {
    if (res.status === 401) { await refreshToken(); }
    return res
  })
```

## OpenAPI Codegen
```bash
# Generate type-safe client from OpenAPI spec
npx openapi-typescript openapi.yaml -o src/api/schema.ts

# Or with orval for full client + React Query hooks
npx orval --config orval.config.ts
```

```ts
// orval.config.ts
import { defineConfig } from 'orval'
export default defineConfig({
  api: {
    input: './openapi.yaml',
    output: {
      mode: 'tags-split',
      target: './src/api',
      schemas: './src/api/model',
      client: 'react-query',
      override: {
        mutator: { path: './src/api/instance.ts', name: 'customInstance' },
      },
    },
  },
})
```

## Error Handling Strategies
```ts
// Error classification
function classifyError(err: unknown): 'network' | 'auth' | 'not_found' | 'server' | 'unknown' {
  if (err instanceof ApiError) {
    if (err.status === 401 || err.status === 403) return 'auth'
    if (err.status === 404) return 'not_found'
    if (err.status >= 500) return 'server'
    return 'unknown'
  }
  if (err instanceof TypeError && err.message === 'Failed to fetch') return 'network'
  return 'unknown'
}

// React hook with error boundary escape hatch
function useApiError(err: unknown) {
  const type = classifyError(err)
  if (type === 'auth') return { message: 'Please log in', action: 'login' as const }
  if (type === 'network') return { message: 'Check your connection', action: 'retry' as const }
  if (type === 'not_found') return { message: 'Not found', action: 'back' as const }
  return { message: 'Something went wrong', action: 'retry' as const }
}
```
