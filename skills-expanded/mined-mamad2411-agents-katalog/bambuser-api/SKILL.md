---
name: bambuser-api
description: >
  Bambuser Live Shopping REST API — shows, products, highlights, webhooks, stats,
  users, tags, channels. Server-side only. Auth is Authorization: Token (not Bearer).
  Use when calling liveshopping-api, BamHub API keys/scopes, show webhooks, or
  syncing Bambuser shows into a CMS. Distinct from bambuser-live (embed/player
  cart bridge) and product catalog feeds used for BamHub ingest.
---

# Bambuser Live REST API

HTTPS/JSON API for automating shows, products, users, and related resources. **Server-side only** — do not call from the browser.

**References:** [endpoints](reference/endpoints.md) · [models](reference/models.md)

## Base URLs

Match BamHub region:

| Region | BamHub host | API base |
|--------|-------------|----------|
| Global | `https://lcx.bambuser.com/` | `https://liveshopping-api.bambuser.com/v1` |
| Europe | `https://lcx-eu.bambuser.com/` | `https://liveshopping-api-eu.bambuser.com/v1` |

OpenAPI default server is **EU**. Prefer EU unless project env documents otherwise.

## Authentication

Create a key in BamHub → Settings → Integrations → API Keys. Assign scopes listed per endpoint.

```http
Authorization: Token YOURAPIKEYHERE
```

**Not** `Bearer`. Product catalog feed auth (often `Bearer` with a feed secret) is a different credential for a different surface.

## Rate limiting

Default: **5 requests / 10 seconds** (moving window). Exceed → HTTP **429**. Some endpoints may document tighter limits; otherwise assume the default. Back off and retry.

## Resources (map)

| Area | Typical ops |
|------|-------------|
| **Shows** | List/create/get/patch/delete; products (incl. batch add); highlights (beta); chat / pinned comments; assets; tags; channels; broadcasts; transcripts |
| **Products** | List/get/patch/delete; highlighted products and appearance lookups |
| **Webhooks** | Create subscription; fetch event by `eventId` to verify delivery |
| **Statistics** | Per-show / multi-show / activity / traffic / orders |
| **Users / tags / channels** | Invite/list/update; tag CRUD; channel create/get |

Full table: [reference/endpoints.md](reference/endpoints.md).

## Show model (CMS sync)

Important `Show` fields (see [models](reference/models.md)). Typical CMS field names when syncing:

| Bambuser | Notes |
|----------|--------|
| `id` | Stable show id → e.g. `bambuserShowId` |
| `title` / `description` | BamHub copy → e.g. `bambuserTitle` / `bambuserDescription` |
| `state` | `upcoming` \| `scheduled` \| `live` \| `ended` |
| `published` / `isTestShow` | Storefront lists: `published && !isTestShow` |
| `scheduledStartAt` / `startedAt` / `endedAt` / `createdAt` | ISO datetimes |
| `preview` | Preview image URL → e.g. `previewUrl` |
| `allowArchivedPlayback` / `isArchived` / `showLengthSeconds` | Playback / archive flags |

## Products

`ProductModel`: `publicUrl` required; optional `productReference`, `title`, `thumbnail`, `brand`.

`productReference` is an external catalog identity (SKU / item id) aligned with whatever the BamHub catalog feed uses. Prefer catalog feed + BamHub for catalog sync; use REST for show/product attachment and admin automation.

## Webhooks

`POST /webhooks` (`WRITE_WEBHOOKS`) body: `name`, `url`, `topics`, `headers` (all required).

**Topics:** `show` · `product` · `user` · `product-highlight` · `broadcast`

**Event payload:**

```ts
{
  collection: 'show' | 'product' | 'user'
  action: 'add' | 'update' | 'remove'
  payload: object
  eventId: string
  timestamp: string // ISO
}
```

Verify origin/contents with `GET /webhooks/{eventId}` (`READ_WEBHOOKS`).

## Integration boundaries

| Surface | Role |
|---------|------|
| Live **REST** API | This skill — server-side shows, webhooks, admin automation |
| Embed / player SDK | Storefront player, cart bridge, product hydration — use **bambuser-live** |
| Product **catalog feed** | BamHub catalog ingest; often **Bearer** feed secret, not Token API key |
| CMS sync | Optional — map show fields into CMS documents when the project does that |

Do not put REST calls in storefront client components. Do not confuse Token API keys with the feed bearer secret.

## Fetch template

```ts
const BAMBUUSER_API_BASE =
  process.env.BAMBUUSER_API_BASE ?? 'https://liveshopping-api-eu.bambuser.com/v1'

async function bambuserFetch<T>(
  path: string,
  init: RequestInit & { apiKey: string },
): Promise<T> {
  const { apiKey, ...rest } = init
  const response = await fetch(`${BAMBUUSER_API_BASE}${path}`, {
    ...rest,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: `Token ${apiKey}`,
      ...rest.headers,
    },
  })

  if (response.status === 429) {
    throw new Error('Bambuser rate limit (429). Back off and retry.')
  }

  if (!response.ok) {
    const body = await response.text()
    throw new Error(`Bambuser ${response.status}: ${body}`)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

// Example: get show
// await bambuserFetch<Show>(`/shows/${showId}`, { method: 'GET', apiKey })
```

Prefer Zod (or equivalent) at the system boundary when persisting into CMS or domain types.
