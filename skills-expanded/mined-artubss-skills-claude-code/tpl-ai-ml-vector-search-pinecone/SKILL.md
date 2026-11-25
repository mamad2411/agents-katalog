---
name: tpl-ai-ml-vector-search-pinecone
description: Template do pack (ai-ml/07-vector-search-pinecone.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/07-vector-search-pinecone.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Vector Search with Pinecone (Node.js/Python + OpenAI Embeddings)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/07-vector-search-pinecone.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Vector DB:** Pinecone SDK v3 (pinecone-client)
- **Language:** Node.js + TypeScript (primary) / Python (ingestion scripts)
- **Embeddings:** OpenAI `text-embedding-3-small` (1536 dims)
- **Hybrid Search:** Pinecone sparse+dense (combined score)
- **Metadata Filtering:** Pinecone metadata filters (JSON)
- **Cost Optimization:** Batch upserts + namespace strategies

---

## PROJECT STRUCTURE
```
pinecone-app/
├── src/
│   ├── pinecone/
│   │   ├── client.ts         # Pinecone singleton
│   │   ├── upsert.ts         # Batch upsert logic
│   │   ├── query.ts          # Query + filter patterns
│   │   └── namespaces.ts     # Namespace strategy
│   ├── embeddings/
│   │   └── openai.ts         # Embedding generation + caching
│   └── types/
│       └── vector.ts          # TypeScript interfaces
├── scripts/
│   ├── ingest.py             # Python bulk ingest
│   ├── backup.py             # Index backup to S3
│   └── cleanup.py            # Delete old vectors
└── tests/
    └── pinecone.test.ts
```

---

## ARCHITECTURE RULES
1. **Namespace per data category** — not per user (too many namespaces); use metadata for user filtering.
2. **Batch upserts: 100 vectors/request** — Pinecone free tier: 100/req; paid: up to 1000. Always batch.
3. **Metadata is small, < 40KB/vector** — don't store full documents in metadata; store IDs + retrieval keys.
4. **Dimensions match embedding model** — `text-embedding-3-small` = 1536; `text-embedding-3-large` = 3072. Can't mix.
5. **Cosine similarity for text** — always `metric: cosine` for text embeddings; `euclidean` for image embeddings.
6. **Filter before score threshold** — apply metadata filters in query, not post-query; cheaper + more accurate.
7. **Cache embeddings for repeated queries** — same query text = same embedding; cache in Redis with SHA256 key.
8. **Hybrid search for keyword+semantic mix** — use Pinecone sparse+dense for product search, FAQ matching.

---

## INDEX CONFIGURATION

```typescript
// src/pinecone/client.ts
import { Pinecone } from '@pinecone-database/pinecone'

if (!process.env.PINECONE_API_KEY) throw new Error('PINECONE_API_KEY required')

export const pinecone = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY,
})

// Index configuration (create once, use always)
export const INDEX_CONFIG = {
  name:       'my-app-vectors',
  dimension:  1536,               // text-embedding-3-small dimensions
  metric:     'cosine' as const,  // Always cosine for text
  spec: {
    serverless: {
      cloud:  'aws',
      region: 'us-east-1',
    },
  },
}

export async function ensureIndex(): Promise<void> {
  const { indexes } = await pinecone.listIndexes()
  const exists = indexes?.some(i => i.name === INDEX_CONFIG.name)

  if (!exists) {
    console.log(`Creating index: ${INDEX_CONFIG.name}`)
    await pinecone.createIndex({
      ...INDEX_CONFIG,
      waitUntilReady: true,
    })
  }
}

export const index = pinecone.index(INDEX_CONFIG.name)
```

---

## NAMESPACE STRATEGY

```typescript
// src/pinecone/namespaces.ts
/**
 * Namespace per logical data type — NOT per user
 *
 * ✅ Good namespace design:
 *   "docs-v1"        → Product documentation (version tagged)
 *   "kb-articles"    → Knowledge base articles
 *   "products"       → Product catalog embeddings
 *   "support-tickets"→ Historical support tickets
 *
 * ❌ Bad namespace design:
 *   "user-123"       → Per-user (creates thousands of namespaces)
 *   "2024-01"        → Per month (stale data hard to query)
 *
 * Use metadata for per-user/per-org filtering:
 *   metadata: { org_id: "org-456", visibility: "private" }
 */

export const NAMESPACES = {
  DOCS:          'docs-v1',
  KB:            'kb-articles',
  PRODUCTS:      'products',
  SUPPORT:       'support-tickets',
} as const

export type Namespace = typeof NAMESPACES[keyof typeof NAMESPACES]
```

---

## EMBEDDING GENERATION + CACHING

```typescript
// src/embeddings/openai.ts
import OpenAI from 'openai'
import { createHash } from 'crypto'
import { Redis } from 'ioredis'

const openaiClient = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379')

const EMBED_CACHE_TTL = 86400   // 24 hours — embeddings don't change

export async function embed(text: string): Promise<number[]> {
  const key = `embed:${createHash('sha256').update(text).digest('hex').slice(0, 16)}`

  const cached = await redis.get(key)
  if (cached) return JSON.parse(cached)

  const response = await openaiClient.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
    encoding_format: 'float',
  })

  const embedding = response.data[0].embedding
  await redis.setex(key, EMBED_CACHE_TTL, JSON.stringify(embedding))

  return embedding
}

export async function embedBatch(texts: string[]): Promise<number[][]> {
  // OpenAI supports up to 2048 inputs per batch
  const BATCH = 100
  const results: number[][] = []

  for (let i = 0; i < texts.length; i += BATCH) {
    const batch = texts.slice(i, i + BATCH)
    const response = await openaiClient.embeddings.create({
      model: 'text-embedding-3-small',
      input: batch,
      encoding_format: 'float',
    })
    results.push(...response.data.map(d => d.embedding))
  }

  return results
}
```

---

## BATCH UPSERT

```typescript
// src/pinecone/upsert.ts
import { index, NAMESPACES, type Namespace } from './client'
import { embedBatch } from '../embeddings/openai'
import type { PineconeRecord, RecordMetadata } from '@pinecone-database/pinecone'

interface UpsertDocument {
  id: string
  text: string
  metadata: RecordMetadata
}

export async function upsertDocuments(
  documents: UpsertDocument[],
  namespace: Namespace = NAMESPACES.DOCS,
  batchSize: number = 100,
): Promise<number> {
  const ns = index.namespace(namespace)
  let total = 0

  for (let i = 0; i < documents.length; i += batchSize) {
    const batch = documents.slice(i, i + batchSize)

    // Embed the batch
    const embeddings = await embedBatch(batch.map(d => d.text))

    // Build Pinecone records
    const records: PineconeRecord[] = batch.map((doc, idx) => ({
      id: doc.id,
      values: embeddings[idx],
      metadata: {
        ...doc.metadata,
        text: doc.text.slice(0, 500),    // Store truncated text for retrieval
        indexed_at: new Date().toISOString(),
      },
    }))

    await ns.upsert(records)
    total += batch.length
    console.log(`Upserted ${total}/${documents.length} vectors`)
  }

  return total
}
```

---

## QUERY + METADATA FILTERING

```typescript
// src/pinecone/query.ts
import { index, type Namespace } from './client'
import { embed } from '../embeddings/openai'

interface QueryOptions {
  topK?: number
  namespace?: Namespace
  filter?: Record<string, unknown>
  includeMetadata?: boolean
  scoreThreshold?: number
}

export async function semanticSearch(
  query: string,
  options: QueryOptions = {},
) {
  const {
    topK = 10,
    namespace = 'docs-v1',
    filter,
    includeMetadata = true,
    scoreThreshold = 0.72,     // Reject irrelevant results
  } = options

  const queryEmbedding = await embed(query)
  const ns = index.namespace(namespace)

  const response = await ns.query({
    vector: queryEmbedding,
    topK,
    filter,                    // Applied server-side: faster + cheaper
    includeMetadata,
    includeValues: false,      // Don't return raw vectors: reduces payload
  })

  // Apply score threshold
  return response.matches
    .filter(m => (m.score ?? 0) >= scoreThreshold)
    .map(m => ({
      id: m.id,
      score: m.score,
      metadata: m.metadata,
    }))
}

// Filtered search example:
// const results = await semanticSearch("deployment guide", {
//   filter: {
//     org_id:   { $eq: "org-456" },
//     doc_type: { $in: ["guide", "tutorial"] },
//     version:  { $gte: 2 },
//   }
// })
```

---

## HYBRID SEARCH (SPARSE + DENSE)

```typescript
// Pinecone sparse-dense hybrid (requires dotproduct metric index)
export async function hybridSearch(
  query: string,
  sparseValues: { indices: number[]; values: number[] },   // From BM25 encoder
  options: QueryOptions = {},
) {
  const denseVector = await embed(query)
  const ns = index.namespace(options.namespace || 'products')

  // alpha: 0 = pure sparse, 1 = pure dense, 0.5 = balanced
  const alpha = 0.5
  const scaledDense  = denseVector.map(v => v * alpha)
  const scaledSparse = {
    indices: sparseValues.indices,
    values: sparseValues.values.map(v => v * (1 - alpha)),
  }

  return ns.query({
    vector: scaledDense,
    sparseVector: scaledSparse,
    topK: options.topK || 10,
    includeMetadata: true,
  })
}
```

---

## INDEX BACKUP TO S3

```python
# scripts/backup.py
import boto3
import json
from pinecone import Pinecone
from datetime import datetime
import os

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
s3 = boto3.client("s3")

BUCKET = "my-app-pinecone-backups"
INDEX_NAME = "my-app-vectors"

def backup_index():
    index = pc.Index(INDEX_NAME)
    stats = index.describe_index_stats()
    namespaces = list(stats.namespaces.keys())

    backup_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "index_name": INDEX_NAME,
        "stats": stats.to_dict(),
        "namespaces": namespaces,
    }

    key = f"backups/{INDEX_NAME}/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}/metadata.json"
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(backup_data),
    )
    print(f"Backup metadata saved to s3://{BUCKET}/{key}")
    # Note: Pinecone doesn't support full vector export in free tier
    # For paid: export to parquet using Pinecone serverless export feature

if __name__ == "__main__":
    backup_index()
```

---

## COST OPTIMIZATION RULES
```
Index Type   │ Cost       │ Use When
─────────────┼────────────┼──────────────────────────────────
Serverless   │ Per usage  │ Variable traffic, dev/staging
Pods (p1)    │ Fixed/hour │ Consistent high traffic, SLA needed
Pods (s1)    │ $         │ Storage-heavy, few queries

Optimization strategies:
1. Reduce dimensions: text-embedding-3-small (1536) vs large (3072) — 2x cheaper queries
2. Delete stale vectors: run cleanup_old_vectors() weekly
3. Use namespaces to isolate high-query from low-query data
4. Cache query embeddings in Redis (same query = no re-embed)
5. Sparse+dense on paid plan only — avoid if on free tier
6. topK=10 max for interactive; topK=50 for batch — each match has cost

Cost formula: Reads × $0.000000125 per unit (1000 dims × 1 vector = 1 unit)
```
