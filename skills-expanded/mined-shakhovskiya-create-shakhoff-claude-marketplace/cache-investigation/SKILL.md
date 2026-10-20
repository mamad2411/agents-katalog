---
name: cache-investigation
description: Persist one-shot investigations (architecture survey, dependency map, library research) to docs/cache/<topic>/ so they're not re-done each session. Use BEFORE running any deep investigation skill (data-source-research, system-architect surveys). Reuse if cache fresh; otherwise refresh.
---

# cache-investigation

Pattern: investigate ONCE, save permanently, reuse until invalidated.

## When to apply

Before any of:
- `data-source-research` (DB schemas, API discovery)
- `system-architect` (module surveys)
- `security-auditor` (dependency CVE walks)
- Library research (e.g. "how does Stripe Connect work")

## Convention path

```
docs/cache/
├── data-sources/
│   └── <db-or-api-name>.md
├── architecture/
│   └── <module-or-system>.md
├── libraries/
│   └── <lib-name>.md
└── investigations/
    └── <slug>.md
```

Each cached file frontmatter:
```yaml
---
topic: <slug>
created_at: 2026-05-08T09:30:00Z
ttl_days: 30
sources_consulted: ["url", "file:line", ...]
invalidate_when:
  - "src/billing/** changed"
  - "package.json::stripe version bumped"
hash_inputs:
  - "src/billing/connect.ts"
  - "package.json"
---
```

## Lookup workflow

1. Compute slug from request ("postgres production schema" → `data-sources/postgres-prod`).
2. Check `docs/cache/<path>/<slug>.md` exists.
3. If exists:
   - Compare `created_at + ttl_days` vs now → expired? skip cache.
   - Recompute hash_inputs digests; mismatch → expired.
   - Otherwise — read and reuse, log `[cache hit]`.
4. If missing or expired:
   - Run actual investigation.
   - Save to cache with frontmatter.
   - Log `[cache miss → wrote]`.

## Eviction

- Manual: `/audit:fix` or user delete.
- TTL — agent may bump created_at if re-validates.
- File-change triggers — when `invalidate_when` hits during sprint, agent invalidates.

## Output to consumer

Caller skill always receives same shape regardless of hit/miss:
```json
{
  "source": "cache_hit | cache_miss | refreshed",
  "path": "docs/cache/.../slug.md",
  "content": "...",
  "freshness_minutes": <int>
}
```

## Prevents

- Repeat DB schema surveys ("Claude keeps re-asking what tables exist").
- Re-reading entire codebase per session.
- Lost institutional knowledge between sessions.

Pairs with `engram` memory: cache = artifact (file), engram = decisions/observations.
