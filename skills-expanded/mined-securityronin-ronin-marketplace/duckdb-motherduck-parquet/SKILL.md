---
name: duckdb-motherduck-parquet
description: DuckDB, MotherDuck cloud analytics, and Parquet file handling for Node.js/TypeScript applications
triggers:
  - duckdb
  - motherduck
  - parquet
  - analytics
  - olap
  - data warehouse
  - serverless analytics
---

# DuckDB, MotherDuck & Parquet

Comprehensive guide for building analytics applications with DuckDB (embedded OLAP), MotherDuck (cloud-hosted DuckDB), and Parquet columnar storage.

## Package Ecosystem

### Node.js Packages

```bash
# Server-side (Node.js) - for API routes, serverless functions
npm install @duckdb/node-api

# Client-side (Browser) - WASM-based
npm install @duckdb/duckdb-wasm

# MotherDuck WASM client (browser only)
npm install @motherduck/wasm-client
```

**Version Compatibility (as of Jan 2026):**
- `@duckdb/node-api`: ^1.4.3-r.3
- `@duckdb/duckdb-wasm`: ^1.33.1-dev16.0
- `@motherduck/wasm-client`: ^0.8.1

## MotherDuck Authentication

### CRITICAL: Connection String Format

The token MUST be embedded in the connection string, NOT passed as a config option.

```typescript
// CORRECT - Token in connection string
import { DuckDBInstance } from '@duckdb/node-api'

const token = process.env.MOTHERDUCK_TOKEN
const connectionString = `md:?motherduck_token=${token}`
const instance = await DuckDBInstance.create(connectionString)
const connection = await instance.connect()
```

```typescript
// WRONG - This causes "The string did not match the expected pattern" error
const instance = await DuckDBInstance.create('md:', {
  motherduck_token: token,  // NOT SUPPORTED as config option
})
```

### Connection String Variations

```typescript
// Connect to default database
`md:?motherduck_token=${token}`

// Connect to specific database
`md:my_database?motherduck_token=${token}`

// With additional options (if supported)
`md:my_database?motherduck_token=${token}&threads=4`
```

### Environment Variables

```bash
# .env.local for Vercel/Next.js projects
MOTHERDUCK_TOKEN=eyJhbGciOiJIUzI1NiIs...

# For Vite projects (browser-accessible)
VITE_MOTHERDUCK_TOKEN=eyJhbGciOiJIUzI1NiIs...
```

**Security Note:** Never expose `MOTHERDUCK_TOKEN` to the browser. Use server-side API routes.

## DuckDB Node.js API Patterns

### Basic Instance Management

```typescript
import { DuckDBInstance, DuckDBConnection } from '@duckdb/node-api'

// Singleton pattern for connection reuse
let instance: DuckDBInstance | null = null
let connection: DuckDBConnection | null = null

async function getConnection(): Promise<DuckDBConnection> {
  if (connection) return connection

  const token = process.env.MOTHERDUCK_TOKEN
  if (!token) {
    throw new Error('MotherDuck token not configured')
  }

  instance = await DuckDBInstance.create(`md:?motherduck_token=${token}`)
  connection = await instance.connect()

  return connection
}

// Reset for testing
function resetConnection(): void {
  connection = null
  instance = null
}
```

### Query Execution

```typescript
async function executeQuery<T>(sql: string): Promise<T[]> {
  const conn = await getConnection()
  const result = await conn.runAndReadAll(sql)
  return result.getRowObjects() as T[]
}

// Handle BigInt values (DuckDB returns BigInt for large numbers)
function convertBigInts<T>(obj: T): T {
  if (obj === null || obj === undefined) return obj
  if (typeof obj === 'bigint') return Number(obj) as T
  if (Array.isArray(obj)) return obj.map(convertBigInts) as T
  if (typeof obj === 'object') {
    const result: Record<string, unknown> = {}
    for (const [key, value] of Object.entries(obj)) {
      result[key] = convertBigInts(value)
    }
    return result as T
  }
  return obj
}

// Usage
const data = await executeQuery<{ count: bigint }>('SELECT COUNT(*) as count FROM flows')
const safeData = convertBigInts(data)  // { count: number }
```

### Running Statements (No Results)

```typescript
// For DDL or DML without result sets
const conn = await getConnection()
await conn.run(`
  CREATE OR REPLACE TABLE flows AS
  SELECT * FROM read_parquet('https://example.com/data.parquet')
`)
```

## Parquet File Handling

### Loading Remote Parquet Files

```typescript
// Create table from remote parquet URL
await conn.run(`
  CREATE OR REPLACE TABLE ${tableName} AS
  SELECT * FROM read_parquet('${url}')
`)

// Query directly without creating table
const result = await conn.runAndReadAll(`
  SELECT * FROM read_parquet('https://example.com/data.parquet')
  LIMIT 100
`)
```

### Parquet with HTTPS Requirement

```typescript
// Validate URL before loading
function validateParquetUrl(url: string): void {
  const parsed = new URL(url)
  if (parsed.protocol !== 'https:') {
    throw new Error('URL must use HTTPS')
  }
  if (!url.endsWith('.parquet')) {
    console.warn('URL does not end with .parquet extension')
  }
}
```

### Common Parquet Sources

- **Cloudflare R2**: `https://pub-xxx.r2.dev/data.parquet`
- **AWS S3**: `https://bucket.s3.region.amazonaws.com/data.parquet`
- **GCS**: `https://storage.googleapis.com/bucket/data.parquet`

## Vercel/AWS Lambda GLIBC Compatibility

### The Problem

Vercel serverless functions run on AWS Lambda with **Amazon Linux 2 (GLIBC 2.26)**. Standard DuckDB npm packages require **GLIBC 2.29+**, causing runtime crashes.

**Error Message:**
```
/lib64/libm.so.6: version 'GLIBC_2.29' not found (required by duckdb.node)
```

**Affected Packages:**
- `duckdb` (legacy package)
- `@duckdb/node-api` (modern package)

### Solution: duckdb-lambda-x86

Use `duckdb-lambda-x86`, a package specifically compiled for Amazon Linux 2:

```bash
npm install duckdb-lambda-x86
```

```typescript
// api/lib/motherduck-server.ts
// @ts-expect-error - duckdb-lambda-x86 has same API as duckdb but no types
import duckdb from 'duckdb-lambda-x86'

const db = new duckdb.Database(`md:?motherduck_token=${token}`, (err) => {
  if (err) console.error('Connection failed:', err)
})

// Promisified query wrapper
const query = (sql: string) => new Promise((resolve, reject) => {
  db.all(sql, (err, rows) => err ? reject(err) : resolve(rows))
})
```

### Key Points

1. **Same API** - `duckdb-lambda-x86` has identical API to `duckdb`
2. **x86 only** - Only works on x86_64 architecture
3. **No TypeScript types** - Use `@ts-expect-error` for imports
4. **Dependencies** - Must be in `dependencies`, NOT `devDependencies`

### Alternative: MotherDuck WASM (Client-Side)

If server-side DuckDB isn't required, use MotherDuck's WASM SDK in the browser:

```typescript
import { initMotherDuck } from '@motherduck/wasm-client'

const md = await initMotherDuck({ token: process.env.MOTHERDUCK_TOKEN })
const result = await md.sql`SELECT * FROM flows LIMIT 10`
```

**Pros:** No native module issues, runs in browser
**Cons:** Requires exposing token to client (use read-only tokens)

### References

- [GitHub Issue #7088](https://github.com/duckdb/duckdb/issues/7088) - GLIBC compatibility
- [duckdb-lambda-x86 npm](https://www.npmjs.com/package/duckdb-lambda-x86)
- [MotherDuck Vercel Integration](https://motherduck.com/docs/integrations/web-development/vercel/)

## Vercel Serverless Integration

### API Route Pattern

```typescript
// api/motherduck/load.ts
import type { VercelRequest, VercelResponse } from '@vercel/node'
import { handleLoadFromUrl } from '../../src/api/routes/motherduck'

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' })
  }

  try {
    const { url, tableName } = req.body || {}
    const result = await handleLoadFromUrl({ url, tableName })

    if (!result.success) {
      return res.status(400).json(result)
    }
    return res.status(200).json(result)
  } catch (error) {
    console.error('MotherDuck load error:', error)
    return res.status(500).json({ success: false, error: 'Internal server error' })
  }
}
```

### Frontend API Client

```typescript
async function apiPost<T>(endpoint: string, body: Record<string, unknown>): Promise<T> {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  const data = await response.json()

  if (!response.ok || !data.success) {
    throw new Error(data.error || 'API request failed')
  }

  return data
}

// Usage
const result = await apiPost<LoadResponse>('/api/motherduck/load', {
  url: 'https://example.com/data.parquet'
})
```

## CORS Headers for DuckDB-WASM

When using DuckDB-WASM in the browser, SharedArrayBuffer requires specific headers:

```json
// vercel.json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Cross-Origin-Opener-Policy", "value": "same-origin" },
        { "key": "Cross-Origin-Embedder-Policy", "value": "credentialless" }
      ]
    }
  ]
}
```

**Note:** Use `credentialless` instead of `require-corp` for better compatibility with external resources.

## Common Errors & Solutions

### "The string did not match the expected pattern"

**Cause:** Passing `motherduck_token` as a config option instead of in connection string.

**Fix:**
```typescript
// Wrong
DuckDBInstance.create('md:', { motherduck_token: token })

// Correct
DuckDBInstance.create(`md:?motherduck_token=${token}`)
```

### BigInt Serialization Error

**Cause:** JSON.stringify fails on BigInt values from DuckDB.

**Fix:** Use `convertBigInts()` helper before JSON serialization.

### CORS/SharedArrayBuffer Errors (Browser)

**Cause:** Missing COOP/COEP headers.

**Fix:** Add headers to `vercel.json` or server config.

### Token Expiration

MotherDuck tokens are JWTs with expiration. Check the `exp` claim:

```typescript
function isTokenExpired(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 < Date.now()
  } catch {
    return true
  }
}
```

## NetFlow/Security Analytics Patterns

### Common NetFlow Columns (NF-UNSW-NB15 Dataset)

```sql
-- Key columns for IR analysis
SELECT
  IPV4_SRC_ADDR,           -- Source IP
  IPV4_DST_ADDR,           -- Destination IP
  L4_SRC_PORT,             -- Source port
  L4_DST_PORT,             -- Destination port
  PROTOCOL,                -- IP protocol number
  FLOW_START_MILLISECONDS, -- Flow start timestamp
  FLOW_DURATION_MILLISECONDS,
  IN_BYTES,
  OUT_BYTES,
  IN_PKTS,
  OUT_PKTS,
  Attack,                  -- Attack label (Benign, DoS, Exploits, etc.)
  Label                    -- Binary: 0=benign, 1=attack
FROM flows
```

### Time Bucketing for Timeline Charts

```sql
SELECT
  (FLOW_START_MILLISECONDS / 3600000) * 3600000 as time_bucket,  -- 1-hour buckets
  Attack as attack,
  COUNT(*) as count
FROM flows
GROUP BY time_bucket, attack
ORDER BY time_bucket, attack
```

### Top Talkers Query

```sql
-- Top source IPs by flow count
SELECT IPV4_SRC_ADDR as ip, COUNT(*) as value
FROM flows
GROUP BY IPV4_SRC_ADDR
ORDER BY value DESC
LIMIT 10
```

## Testing Patterns

```typescript
// Mock DuckDB for unit tests
vi.mock('@duckdb/node-api', () => ({
  DuckDBInstance: {
    create: vi.fn().mockResolvedValue({
      connect: vi.fn().mockResolvedValue({
        runAndReadAll: vi.fn().mockResolvedValue({
          getRowObjects: vi.fn().mockReturnValue([])
        }),
        run: vi.fn().mockResolvedValue(undefined)
      })
    })
  }
}))
```

## Resources

- [DuckDB Node Neo GitHub](https://github.com/duckdb/duckdb-node-neo)
- [MotherDuck Documentation](https://motherduck.com/docs/)
- [DuckDB SQL Reference](https://duckdb.org/docs/sql/introduction)
- [Parquet Format](https://parquet.apache.org/)
