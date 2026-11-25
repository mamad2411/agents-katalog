---
name: "Offline Sync Engine"
version: "1.0.0"
description: "Handles offline data synchronization with conflict resolution and progressive sync."
author: "workspace"
activated: false
---

# Offline Sync Engine

## Overview

Manages offline data storage and synchronization when connectivity returns.

## Decision Framework

### When to use
- App needs to work without internet
- Data must sync across devices
- Users edit data while offline

### When NOT to use
- Real-time collaborative systems
- Read-only data displays

## Trigger Phrases

- "Work offline"
- "Sync data when back online"
- "Offline support"
- "Cache data locally"

## Sync Patterns

| Pattern | Conflict Strategy | Best For |
|---------|-------------------|----------|
| Last-write-wins | Timestamp comparison | Simple data |
| Operational transform | Transform operations | Collaborative text |
| CRDT | Merge all changes | Distributed systems |
| Manual merge | User resolves | Critical data |

## Storage Layers

```
┌─────────────────────────────────────┐
│ Application Layer                    │
├─────────────────────────────────────┤
│ Sync Queue (pending changes)         │
├─────────────────────────────────────┤
│ Local Cache (IndexedDB/SQLite)       │
├─────────────────────────────────────┤
│ Conflict Resolution                  │
├─────────────────────────────────────┤
│ Remote API                           │
└─────────────────────────────────────┘
```

## Implementation

### Sync Queue
```javascript
class SyncQueue {
  constructor() {
    this.pending = [];
    this.failed = [];
  }

  add(change) {
    this.pending.push({
      id: generateId(),
      operation: change.operation,
      data: change.data,
      timestamp: Date.now(),
      retries: 0
    });
  }

  async flush() {
    while (this.pending.length > 0) {
      const change = this.pending[0];
      try {
        await this.sendToServer(change);
        this.pending.shift();
      } catch (error) {
        change.retries++;
        if (change.retries >= 3) {
          this.failed.push(this.pending.shift());
        }
        break;
      }
    }
  }
}
```

### Conflict Resolution
```javascript
class ConflictResolver {
  resolve(local, remote, strategy = 'last-write-wins') {
    switch(strategy) {
      case 'last-write-wins':
        return local.updatedAt > remote.updatedAt ? local : remote;
      case 'merge':
        return this.deepMerge(local, remote);
      case 'manual':
        throw new ConflictError(local, remote);
    }
  }
}
```

## Escalation Chain

1. **Retry** - Immediate retry (3 attempts)
2. **Backoff** - Exponential backoff (1s, 2s, 4s, 8s)
3. **Queue** - Add to offline queue for later sync
4. **Notify** - Alert user of sync failure
5. **Manual** - User intervention required

## Error Classification

| Error Type | Strategy | Recovery |
|-----------|----------|----------|
| Network timeout | Retry with backoff | Auto |
| Conflict | Merge strategy | Auto/Manual |
| Auth expired | Refresh token | Auto |
| Data corruption | Rollback + alert | Manual |
