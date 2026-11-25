---
name: backend-patterns
description: Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes.
model: gemini-2.0-pro-exp
---

# Backend Development Patterns

Backend architecture patterns and best practices for scalable server-side applications in Antigravity projects.

## API Design Patterns

### RESTful API Structure

```typescript
GET    /api/resources          # List
GET    /api/resources/:id      # Get single
POST   /api/resources          # Create
PUT    /api/resources/:id      # Replace
PATCH  /api/resources/:id      # Update
DELETE /api/resources/:id      # Delete

// Query parameters for filtering, sorting, pagination
GET /api/resources?status=active&sort=volume&limit=20&offset=0
```

### Repository Pattern

```typescript
interface Repository<T> {
  findAll(filters?: Filters): Promise<T[]>
  findById(id: string): Promise<T | null>
  create(data: CreateDto): Promise<T>
  update(id: string, data: UpdateDto): Promise<T>
  delete(id: string): Promise<void>
}

class SupabaseRepository<T> implements Repository<T> {
  async findAll(filters?: Filters): Promise<T[]> {
    let query = supabase.from(this.table).select('*')
    if (filters?.status) query = query.eq('status', filters.status)
    const { data, error } = await query
    if (error) throw new Error(error.message)
    return data
  }
}
```

### Service Layer Pattern

```typescript
class MarketService {
  constructor(private repo: MarketRepository) {}

  async search(query: string, limit = 10): Promise<Market[]> {
    const embedding = await generateEmbedding(query)
    return this.repo.findByVector(embedding, limit)
  }
}
```

### Middleware Pattern

```typescript
export function withAuth(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    const token = req.headers.authorization?.replace('Bearer ', '')
    if (!token) return res.status(401).json({ error: 'Unauthorized' })
    try {
      req.user = await verifyToken(token)
      return handler(req, res)
    } catch {
      return res.status(401).json({ error: 'Invalid token' })
    }
  }
}
```

## Database Patterns

### Query Optimization

```typescript
// ✅ Select only needed columns
const { data } = await supabase
  .from('markets')
  .select('id, name, status, volume')
  .eq('status', 'active')
  .order('volume', { ascending: false })
  .limit(10)
```

### N+1 Query Prevention

```typescript
// ❌ Bad - N+1
const markets = await getMarkets()
for (const m of markets) m.creator = await getUser(m.creator_id)

// ✅ Good - Batch fetch
const creatorIds = markets.map(m => m.creator_id)
const creators = await getUsers(creatorIds)
const creatorMap = new Map(creators.map(c => [c.id, c]))
markets.forEach(m => { m.creator = creatorMap.get(m.creator_id) })
```

### Pagination

```typescript
const { data } = await supabase
  .from('posts')
  .select('*')
  .range(0, 19)
  .order('created_at', { ascending: false })
```

## Caching Strategies

### Cache-Aside Pattern

```typescript
async function getWithCache<T>(key: string, fetcher: () => Promise<T>, ttl = 300): Promise<T> {
  const cached = await redis.get(key)
  if (cached) return JSON.parse(cached)

  const data = await fetcher()
  await redis.setex(key, ttl, JSON.stringify(data))
  return data
}
```

## Error Handling

### Centralized Error Handler

```typescript
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true
  ) {
    super(message)
    Object.setPrototypeOf(this, ApiError.prototype)
  }
}

export function errorHandler(error: unknown): Response {
  if (error instanceof ApiError) {
    return NextResponse.json({ success: false, error: error.message }, { status: error.statusCode })
  }
  if (error instanceof z.ZodError) {
    return NextResponse.json({ success: false, error: 'Validation failed', details: error.errors }, { status: 400 })
  }
  console.error('Unexpected error:', error)
  return NextResponse.json({ success: false, error: 'Internal server error' }, { status: 500 })
}
```

### Retry with Exponential Backoff

```typescript
async function fetchWithRetry<T>(fn: () => Promise<T>, maxRetries = 3): Promise<T> {
  let lastError: Error
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      if (i < maxRetries - 1) await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000))
    }
  }
  throw lastError!
}
```

## Authentication & Authorization

### Role-Based Access Control

```typescript
type Permission = 'read' | 'write' | 'delete' | 'admin'

const rolePermissions: Record<string, Permission[]> = {
  admin: ['read', 'write', 'delete', 'admin'],
  moderator: ['read', 'write', 'delete'],
  user: ['read', 'write']
}

export function hasPermission(user: User, permission: Permission): boolean {
  return rolePermissions[user.role]?.includes(permission) ?? false
}
```

## Rate Limiting

```typescript
class RateLimiter {
  private requests = new Map<string, number[]>()

  check(id: string, max: number, windowMs: number): boolean {
    const now = Date.now()
    const recent = (this.requests.get(id) || []).filter(t => now - t < windowMs)
    if (recent.length >= max) return false
    this.requests.set(id, [...recent, now])
    return true
  }
}
```

## Structured Logging

```typescript
const logger = {
  info: (msg: string, ctx?: object) => console.log(JSON.stringify({ level: 'info', msg, ...ctx, ts: new Date().toISOString() })),
  error: (msg: string, err: Error, ctx?: object) => console.log(JSON.stringify({ level: 'error', msg, error: err.message, ...ctx, ts: new Date().toISOString() }))
}
```

**Remember**: Backend patterns enable scalable, maintainable server-side applications. Choose patterns that fit your complexity level.
