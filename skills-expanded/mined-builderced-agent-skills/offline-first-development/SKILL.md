---
name: offline-first-development
description: Build offline-capable applications with IndexedDB, service workers, background sync, and conflict resolution patterns.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: offline
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [global, africa]
priority: medium
dependencies:
  mcp: []
  skills: []
  apis: []
  data: []
update_sources:
  - url: "https://web.dev/articles/offline-cookbook"
    check_frequency: "yearly"
    last_checked: "2026-04-21"
license: MIT
---

# Offline-First Development

## When to Use

- Building apps for low-connectivity environments (rural, Africa, transit)
- Building PWAs that must work without internet
- Designing sync strategies for mobile apps
- Implementing local-first architectures
- Building for environments with unreliable connections

## Core Principles

1. **Local-first**: Data lives on the device. Server is backup, not source of truth.
2. **Sync on reconnect**: Queue changes offline, sync when connection returns.
3. **Conflict resolution**: Define merge strategy before building.
4. **Progressive enhancement**: App works offline; online adds features.

## Storage Options

| Storage | Size Limit | Persistence | Best For |
|---------|-----------|-------------|----------|
| IndexedDB | ~50% of disk | Persistent | Structured data, large datasets |
| Cache API | ~50% of disk | Persistent | HTTP responses, assets |
| localStorage | 5-10 MB | Persistent | Small key-value config |
| OPFS | ~50% of disk | Persistent | File-like access (new) |

**Recommendation**: IndexedDB for data, Cache API for assets, OPFS for files.

## Service Worker Pattern

```
Install → Cache essential assets (app shell, fonts, icons)
Activate → Clean old caches
Fetch → Cache-first for assets, network-first for API data
Sync → Background sync for queued mutations
```

### Caching Strategies

| Strategy | When | How |
|----------|------|-----|
| Cache-first | Static assets (CSS, JS, images) | Serve from cache, update in background |
| Network-first | API data | Try network, fall back to cache |
| Stale-while-revalidate | Semi-static (user profile) | Serve cache, update from network |
| Network-only | Real-time data (chat, payments) | No caching |

## Sync Patterns

### Optimistic Updates
1. Apply change locally immediately
2. Queue mutation for sync
3. On reconnect: send queued mutations
4. On conflict: apply resolution strategy

### Conflict Resolution Strategies

| Strategy | When | How |
|----------|------|-----|
| Last-write-wins | Simple data, single user | Timestamp comparison |
| Server-wins | Authoritative server | Discard local on conflict |
| Client-wins | User autonomy priority | Overwrite server |
| Merge | Collaborative editing | Field-level merge |
| Manual | Critical data | Show conflict to user |

### Queue Design
```
Mutation queue entry:
{
  id: "uuid",
  timestamp: "ISO-8601",
  entity: "task",
  entity_id: "uuid",
  action: "create|update|delete",
  payload: { ... },
  retries: 0,
  status: "pending|syncing|failed|synced"
}
```

## Connectivity Detection

```javascript
// Basic
navigator.onLine // boolean (unreliable alone)

// Robust: combine with actual fetch test
async function isOnline() {
  try {
    const response = await fetch('/api/health', {
      method: 'HEAD',
      cache: 'no-store',
      signal: AbortSignal.timeout(3000)
    });
    return response.ok;
  } catch {
    return false;
  }
}
```

## Mobile-Specific Considerations

- **Battery**: Batch sync operations, avoid polling
- **Bandwidth**: Compress payloads, delta sync
- **Storage quotas**: Monitor usage, evict old data
- **App lifecycle**: Handle background/foreground transitions

## What This Skill Does NOT Do

- Does not implement a specific sync protocol (CRDT, OT)
- Does not handle real-time collaboration (use dedicated tools)
- Does not manage authentication tokens offline (security concern)
- Does not provide a database library (guides architecture choices)
