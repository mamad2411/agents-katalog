---
name: bun-patterns
description: "When to activate: Bun runtime, Bun.serve, Bun.file, bun test, bun build, bun shell, SQLite, performance-first Node.js alternative"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: typescript
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Bun Patterns

## HTTP Server (Bun.serve)
```ts
const server = Bun.serve({
  port: 3000,
  async fetch(req) {
    const url = new URL(req.url)

    if (url.pathname === '/api/health') {
      return Response.json({ status: 'ok' })
    }

    if (url.pathname === '/api/users' && req.method === 'GET') {
      const users = await db.user.findMany()
      return Response.json(users)
    }

    if (url.pathname === '/api/users' && req.method === 'POST') {
      const body = await req.json()
      const user = await db.user.create({ data: body })
      return Response.json(user, { status: 201 })
    }

    return new Response('Not Found', { status: 404 })
  },
})

console.log(`Listening on ${server.url}`)
```

## File I/O
```ts
// Read
const text    = await Bun.file('data.txt').text()
const json    = await Bun.file('config.json').json()
const buffer  = await Bun.file('image.png').arrayBuffer()

// Write
await Bun.write('output.txt', 'Hello World')
await Bun.write('data.json', JSON.stringify(obj, null, 2))

// Stream large file
const file   = Bun.file('large.csv')
const stream = file.stream()
```

## SQLite (built-in)
```ts
import { Database } from 'bun:sqlite'

const db = new Database('myapp.db')

// Create table
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
  )
`)

// Prepared statements (type-safe)
const insert = db.prepare('INSERT INTO users (name, email) VALUES ($name, $email)')
const getAll = db.prepare('SELECT * FROM users')
const getById = db.prepare<User, [number]>('SELECT * FROM users WHERE id = ?')

insert.run({ $name: 'Alice', $email: 'alice@example.com' })
const users = getAll.all()
const user  = getById.get(1)
```

## Bun Shell
```ts
import { $ } from 'bun'

// Run shell commands safely (no injection — args are escaped)
const result = await $`git log --oneline -10`.text()
const files  = await $`ls -la ${dir}`.lines()

// Pipeline
await $`cat input.log | grep ERROR | wc -l`

// Error handling
const { stdout, stderr, exitCode } = await $`npm test`.nothrow()
if (exitCode !== 0) console.error(stderr.toString())
```

## Testing (bun test)
```ts
// tests/math.test.ts
import { describe, test, expect, beforeEach, mock } from 'bun:test'

describe('add', () => {
  test('sums two numbers', () => {
    expect(add(1, 2)).toBe(3)
  })

  test('handles negatives', () => {
    expect(add(-1, 1)).toBe(0)
  })
})

// Mocks
const fetchMock = mock(() => Promise.resolve({ ok: true, json: () => ({ id: 1 }) }))
// globalThis.fetch = fetchMock
```

## Build (bun build)
```ts
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'bun',        // 'node' | 'browser' | 'bun'
  format: 'esm',
  minify: true,
  sourcemap: 'external',
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },
})
```

## Environment & Config
```ts
// Bun auto-loads .env, .env.local, .env.production
const port = Bun.env.PORT ?? '3000'
const dbUrl = Bun.env.DATABASE_URL    // string | undefined

// Type-safe env with zod
import { z } from 'zod'
const env = z.object({
  DATABASE_URL: z.string(),
  JWT_SECRET:   z.string().min(32),
  PORT:         z.coerce.number().default(3000),
}).parse(Bun.env)
```

## WebSockets
```ts
const server = Bun.serve({
  port: 3001,
  fetch(req, server) {
    if (server.upgrade(req)) return  // upgrade to WS
    return new Response('Not a WS request', { status: 400 })
  },
  websocket: {
    open(ws)          { ws.subscribe('room:global') },
    message(ws, msg)  { server.publish('room:global', msg) },
    close(ws, code)   { console.log('closed', code) },
  },
})
```

## Graceful Shutdown
```ts
process.on('SIGINT', async () => {
  server.stop()
  await db.close()
  process.exit(0)
})
```

## package.json Scripts
```json
{
  "scripts": {
    "dev":   "bun --hot run src/index.ts",
    "start": "bun run src/index.ts",
    "test":  "bun test",
    "build": "bun build ./src/index.ts --outdir ./dist --target bun"
  }
}
```
