---
name: offline-first-development
description: Use when implementing offline-first applications, managing local storage, implementing data synchronization, handling conflicts, and creating offline UI patterns. Includes IndexedDB, localStorage, service workers, and offline state management. Based on offline-first development best practices.
license: MIT
---

# Offline-First Development Skill — Mobile Engineer

## Overview

This skill provides comprehensive guidance for implementing offline-first applications. It covers local storage management, data synchronization, conflict resolution, offline UI patterns, and offline state management following offline-first development best practices.

## When to Use

**Use this skill when:**

- Implementing offline-first applications
- Managing local storage (IndexedDB, localStorage)
- Implementing data synchronization
- Handling synchronization conflicts
- Creating offline UI patterns
- Implementing service workers
- Managing offline state
- Creating offline data models
- Implementing offline-first APIs
- Handling network failures
- Creating offline indicators
- Implementing queue for offline actions
- Managing offline data validation
- Creating offline sync strategies
- Implementing conflict resolution
- Managing offline data consistency
- Creating offline-first UX patterns
- Implementing background sync
- Managing offline data caching
- Creating offline-first error handling
- Implementing offline data encryption
- Managing offline storage limits
- Creating offline-first testing

**Do NOT use this skill when:**

- Writing application business logic (use domain-driven skill)
- Designing database schemas (use database-design skill)
- Writing API endpoint specifications (use api-design skill)
- Performing security audits (use security-auditor skill)
- Writing SQL queries (use sql-best-practices skill)
- Designing multi-page website layouts (use design-system skill)
- Analyzing deployment configurations (use deployment skill)
- Writing documentation (use documentation-best-practices skill)

## Offline-First Principles

### Core Principles

```
┌─────────────────────────────────────────────────────────────┐
│              Offline-First Principles                       │
├─────────────────────────────────────────────────────────────┤
│  1. Always Available:                                       │
│     - Application works offline                             │
│     - Core functionality available                          │
│     - Graceful degradation                                  │
│                                                              │
│  2. Data Persistence:                                       │
│     - Data stored locally                                   │
│     - Data survives app restart                             │
│     - Data survives device restart                          │
│                                                              │
│  3. Automatic Sync:                                         │
│     - Data syncs when online                                │
│     - Sync happens automatically                            │
│     - Sync is transparent to user                           │
│                                                              │
│  4. Conflict Resolution:                                    │
│     - Handle offline changes                                │
│     - Resolve conflicts gracefully                          │
│     - User awareness of conflicts                           │
│                                                              │
│  5. Offline UI:                                             │
│     - Clear offline status                                  │
│     - Offline actions queue                                 │
│     - Offline indicators                                    │
└─────────────────────────────────────────────────────────────┘
```

### Local Storage Options

```
┌─────────────────────────────────────────────────────────────┐
│              Local Storage Options                          │
├─────────────────────────────────────────────────────────────┤
│  localStorage:                                              │
│  - Key-value storage                                        │
│  - Synchronous API                                          │
│  - Limited to ~5MB                                          │
│  - String values only                                       │
│                                                              │
│  sessionStorage:                                            │
│  - Session-scoped storage                                   │
│  - Synchronous API                                          │
│  - Limited to ~5MB                                          │
│  - Cleared on session end                                   │
│                                                              │
│  IndexedDB:                                                 │
│  - Database-style storage                                   │
│  - Asynchronous API                                         │
│  - Large storage capacity                                   │
│  - Supports complex data structures                         │
│                                                              │
│  Cache API:                                                 │
│  - HTTP response caching                                    │
│  - Service worker integration                               │
│  - Query-based retrieval                                    │
│  - Automatic cache management                               │
│                                                              │
│  Web SQL (deprecated):                                      │
│  - SQL database                                             │
│  - Asynchronous API                                         │
│  - Deprecated in favor of IndexedDB                         │
└─────────────────────────────────────────────────────────────┘
```

## Offline Sync Strategies

### Sync Patterns

```
┌─────────────────────────────────────────────────────────────┐
│              Offline Sync Strategies                        │
├─────────────────────────────────────────────────────────────┤
│  Last Write Wins:                                           │
│  - Simple conflict resolution                               │
│  - Timestamp-based                                          │
│  - May lose data                                            │
│  - Good for: Simple data, low conflict                     │
│                                                              │
│  Operational Transform:                                     │
│  - Collaborative editing                                    │
│  - Transform operations                                    │
│  - Complex implementation                                   │
│  - Good for: Real-time collaboration                       │
│                                                              │
│  CRDT (Conflict-free Replicated Data Types):                │
│  - Automatic conflict resolution                            │
│  - No coordination needed                                   │
│  - Complex data structures                                  │
│  - Good for: Distributed systems                           │
│                                                              │
│  Merge Conflicts:                                           │
│  - User-assisted resolution                                 │
│  - Conflict detection                                       │
│  - User interface for resolution                            │
│  - Good for: User-editable data                            │
│                                                              │
│  Queue-based Sync:                                          │
│  - Queue offline actions                                    │
│  - Process sequentially                                     │
│  - Track sync status                                        │
│  - Good for: Action-based sync                             │
└─────────────────────────────────────────────────────────────┘
```

### Sync Implementation

```javascript
// ✅ Good: Offline sync with IndexedDB
class OfflineSync {
  constructor(db, apiClient) {
    this.db = db;
    this.apiClient = apiClient;
  }

  async sync() {
    // Get pending changes
    const pendingChanges = await this.db.getAll('pendingChanges');

    for (const change of pendingChanges) {
      try {
        // Attempt to sync
        const result = await this.apiClient.sync(change);

        // Mark as synced
        await this.db.delete('pendingChanges', change.id);

        // Update local cache
        await this.db.put('cache', result);
      } catch (error) {
        // Handle error
        console.error('Sync failed:', error);

        // Retry later
        if (this.shouldRetry(error)) {
          await this.db.update('pendingChanges', change.id, {
            retryCount: (change.retryCount || 0) + 1,
          });
        }
      }
    }
  }

  async queueChange(record, action) {
    // Queue change for later sync
    await this.db.put('pendingChanges', {
      record,
      action,
      timestamp: Date.now(),
      retryCount: 0,
    });
  }
}
```

## Offline UI Patterns

### Offline Indicators

```html
<!-- ✅ Good: Offline indicator -->
<div class="offline-indicator" id="offlineIndicator">
  <span class="offline-icon">wifi_off</span>
  <span class="offline-text">You're offline</span>
</div>

<script>
  // Monitor network status
  window.addEventListener('online', () => {
    document.getElementById('offlineIndicator').style.display = 'none';
    // Trigger sync
    offlineSync.sync();
  });

  window.addEventListener('offline', () => {
    document.getElementById('offlineIndicator').style.display = 'block';
  });
</script>
```

### Offline Actions Queue

```html
<!-- ✅ Good: Offline action queue -->
<div class="action-queue" id="actionQueue">
  <h3>Pending Actions</h3>
  <ul id="queueList"></ul>
</div>

<script>
  // Display pending actions
  function displayQueue() {
    const queueList = document.getElementById('queueList');
    queueList.innerHTML = '';

    offlineSync.getPendingActions().forEach((action) => {
      const li = document.createElement('li');
      li.textContent = `${action.type}: ${action.description}`;
      queueList.appendChild(li);
    });
  }
</script>
```

## Service Workers

### Service Worker Registration

```javascript
// ✅ Good: Service worker registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/sw.js')
      .then((registration) => {
        console.log('SW registered:', registration);
      })
      .catch((error) => {
        console.log('SW registration failed:', error);
      });
  });
}
```

### Service Worker Cache Strategy

```javascript
// ✅ Good: Service worker cache strategy
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('app-cache').then((cache) => {
      return cache.addAll([
        '/',
        '/styles/main.css',
        '/scripts/app.js',
        '/images/logo.png',
      ]);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(event.request).then((response) => {
        // Cache the response
        const responseClone = response.clone();
        caches.open('app-cache').then((cache) => {
          cache.put(event.request, responseClone);
        });

        return response;
      });
    })
  );
});
```

## Real-World Impact

**Before this skill:**

- Applications fail when offline
- No data persistence
- Poor user experience
- Data loss
- Manual sync required

**After this skill:**

- Applications work offline
- Automatic data persistence
- Excellent user experience
- No data loss
- Automatic sync

## Cross-References

- **`mobile-performance`** - For mobile optimization
- **`testing-strategy`** - For offline testing
- **`api-design`** - For offline-first APIs

## References

- [Offline-First by Adam Silver](https://abookapart.com/products/offline-first)
- [Service Worker API](https://developer.mozilla.org/)
- [IndexedDB API](https://developer.mozilla.org/)
- [Cache API](https://developer.mozilla.org/)
- [Offline-First Development](https://offlinefirst.org/)
