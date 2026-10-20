# Offline-First Architecture Standards

**Version**: 2.7.0  
**Applies to**: Mobile apps, PWAs, distributed systems  
**Last Updated**: 2026-04-09

---

## 🎯 Core Principle

Offline-first means the app works without network, syncing when available. Not "online-first with offline fallback"—network is optional, not required. This is critical for mobile users who experience poor connectivity, airplane mode, or network switches.

---

## 🏗️ Offline-First Architecture Pattern

### 1. Local-First Data Store

All user data lives locally (device), synced to cloud when connected.

**React Native / Flutter Example**
```typescript
// BAD: Online-first (fails without network)
async function loadUsers() {
  const response = await fetch('/api/users');
  setUsers(response.json());
}

// GOOD: Offline-first (works always)
async function loadUsers() {
  // 1. Load from local database immediately
  const localUsers = await localDB.query('users');
  setUsers(localUsers);
  
  // 2. Sync with server in background (don't wait)
  if (isOnline()) {
    fetchServerUsers()
      .then(serverUsers => {
        // Update local DB with server data
        localDB.upsert('users', serverUsers);
        setUsers(serverUsers);
      })
      .catch(err => {
        // Network failed: keep showing local data
        console.log('Sync failed, showing cached data');
      });
  }
}
```

### 2. Event Log / Transaction Log

Instead of direct updates, record all changes as events. This enables:
- Offline queuing (apply when online)
- Conflict resolution
- Audit trail
- Replay on sync

**Example: User Profile Update**
```typescript
// Offline change
const updateUserProfile = async (userId: string, changes: Partial<User>) => {
  const localUser = await localDB.get('users', userId);
  const updatedUser = { ...localUser, ...changes };
  
  // 1. Update local DB immediately (optimistic)
  await localDB.put('users', updatedUser);
  setUser(updatedUser);
  
  // 2. Queue event for sync
  await eventLog.append({
    id: uuid(),
    type: 'user.updated',
    userId,
    changes,
    timestamp: Date.now(),
    synced: false,
  });
  
  // 3. Attempt sync in background
  if (isOnline()) {
    syncEventLog(); // Send all pending events to server
  }
};
```

---

## 🗄️ Local Database Technologies

| Platform | Library | Pros | Cons |
|----------|---------|------|------|
| React Native | WatermelonDB, Realm | Type-safe, relations, sync-friendly | Setup complexity |
| Flutter | Isar, Hive | Fast, encrypted, simple | Less mature than SQLite |
| iOS | CoreData, Realm | Native, powerful | Complex relationships |
| Android | Room, Realm | Type-safe, DAOs | More boilerplate |
| Web/PWA | IndexedDB, PouchDB | Unlimited storage, sync | Async only, no transactions |

### Recommended Setup

**React Native**: WatermelonDB or Realm
- Relations between tables
- Sync protocols (WatermelonDB has built-in)
- Type-safe with TypeScript

```typescript
// Example: WatermelonDB
import { Database } from '@nozbe/watermelondb';
import SQLiteAdapter from '@nozbe/watermelondb/adapters/sqlite';

const adapter = new SQLiteAdapter({
  schema: appSchema, // Define tables, columns, relations
  dbName: 'myapp',
});

const database = new Database({
  adapter,
  modelClasses: [User, Post, Comment],
});

// Usage
const users = await database.get('users').query().fetch();
```

**Flutter**: Isar or Hive
```dart
// Isar: type-safe, relations
final isar = await Isar.open([UserSchema]);
final user = await isar.users.get(1);

// Hive: simple key-value, encrypted
final box = await Hive.openBox('users');
box.put('user_1', User(name: 'Alice'));
```

---

## 🔄 Sync Strategies

### 1. Optimistic Updates + Event Log

**Flow:**
1. User makes change (e.g., update profile)
2. Update local DB immediately, show to user (optimistic)
3. Queue event for server
4. When online, send event to server
5. Server responds with sync confirmation or conflict
6. If conflict, resolve (latest-write-wins, merge, user prompt)

**Pros:** Instant feedback, works offline  
**Cons:** Conflict handling required

**Example**
```typescript
const updateTitle = async (postId: string, newTitle: string) => {
  // 1. Optimistic: update local immediately
  const post = await db.posts.find(postId);
  post.title = newTitle;
  post.lastModified = Date.now();
  await db.posts.update(post);
  
  // 2. Queue for sync
  await syncQueue.add({
    action: 'update',
    resource: 'posts',
    id: postId,
    changes: { title: newTitle },
  });
  
  // 3. Sync when online
  triggerSync();
};
```

### 2. Incremental Sync (Cursor-Based)

Track last sync point. On reconnect, fetch changes since then.

**Pros:** Minimal data transfer, works for append-only systems  
**Cons:** Doesn't handle deletes well, order matters

**Example**
```typescript
const lastSyncTimestamp = await db.meta.get('last_sync');

const syncChanges = async () => {
  if (!isOnline()) return;
  
  // Fetch only changes after last sync
  const response = await api.get('/changes', {
    params: { since: lastSyncTimestamp }
  });
  
  // Apply changes to local DB
  for (const change of response.data) {
    if (change.deleted) {
      await db.delete(change.resource, change.id);
    } else {
      await db.upsert(change.resource, change.data);
    }
  }
  
  // Update sync timestamp
  await db.meta.set('last_sync', Date.now());
};
```

### 3. Conflict Resolution

When user edited data offline, and server also changed it:

**Strategies:**
- **Latest-write-wins (LWW):** Server timestamp beats local
- **Local-write-wins:** Assume user's offline change is authoritative
- **Merge:** Combine changes (works for lists, not primitives)
- **User prompt:** "Your change conflicts with latest. Keep yours?"

**Example: Merge Strategy**
```typescript
const resolveConflict = (
  localVersion: Post,
  serverVersion: Post
): Post => {
  // Merge: preserve local comments, use server title
  return {
    ...serverVersion,
    comments: localVersion.comments, // Local additions preserved
    updatedAt: Math.max(
      localVersion.updatedAt,
      serverVersion.updatedAt
    ),
  };
};
```

---

## 📡 Network State Detection & Sync Triggers

### Monitor Network Status

```typescript
// React Native
import { useNetInfo } from '@react-native-community/netinfo';

const NetworkAwareComponent = () => {
  const netInfo = useNetInfo();
  
  useEffect(() => {
    if (netInfo.isConnected && !netInfo.isInternetReachable) {
      // Connected to WiFi but no internet
    } else if (netInfo.isConnected && netInfo.isInternetReachable) {
      // Real internet available: trigger sync
      syncOfflineChanges();
    }
  }, [netInfo.isConnected, netInfo.isInternetReachable]);
};

// Flutter
StreamSubscription<List<ConnectivityResult>> subscription =
    Connectivity()
        .onConnectivityChanged
        .listen((List<ConnectivityResult> result) {
      if (result.contains(ConnectivityResult.wifi) ||
          result.contains(ConnectivityResult.mobile)) {
        syncOfflineChanges();
      }
    });
```

### Auto-Sync Triggers

1. **On network change:** WiFi → Cellular
2. **Periodic sync:** Every 5 minutes (if online)
3. **On app foreground:** Resume from background
4. **On queue threshold:** N pending changes accumulated
5. **Manual:** User taps "Sync Now"

---

## 💾 Data Integrity & Soft Deletes

**Never hard-delete immediately:**
```typescript
// BAD: Hard delete (can't recover, sync issues)
await db.posts.delete(postId);

// GOOD: Soft delete (can recover, sync-safe)
const post = await db.posts.get(postId);
post.isDeleted = true;
post.deletedAt = Date.now();
await db.posts.update(post);

// When syncing, send isDeleted=true to server
// Server marks as deleted, but can undelete with sync
```

**Garbage collection:** After server confirms deletion (e.g., 30 days), hard-delete locally.

---

## 🔐 Secure Offline Storage

**Never store sensitive data unencrypted:**

```typescript
// React Native with WatermelonDB
import { Database } from '@nozbe/watermelondb';
import SQLiteAdapter from '@nozbe/watermelondb/adapters/sqlite';
import { encryptSchema } from '@nozbe/watermelondb/encryption';

const adapter = new SQLiteAdapter({
  schema: encryptSchema(appSchema), // Encrypt entire DB
  dbName: 'myapp.db',
  encryptionKey: await getEncryptionKey(), // From Keychain
});

// Flutter with Isar
final encryptionKey = base64Decode('your_key');
final isar = await Isar.open([UserSchema],
  encryption: IsarEncryption(encryptionKey),
);
```

---

## 📊 Offline-First UI Patterns

### 1. Sync Status Indicator

Show user current sync state:
```typescript
const SyncStatus = ({ status }) => {
  switch (status) {
    case 'synced':
      return <Text>✓ All changes synced</Text>;
    case 'syncing':
      return <Text>↻ Syncing...</Text>;
    case 'offline':
      return <Text>⚠ Offline (changes queued)</Text>;
    case 'error':
      return <Text>✗ Sync failed, tap to retry</Text>;
  }
};
```

### 2. Optimistic UI

Show changes immediately (before server confirms):
```typescript
// User creates post
const createPost = async (title: string) => {
  const tempId = uuid();
  
  // 1. Show immediately (optimistic)
  setPosts([...posts, { id: tempId, title, synced: false }]);
  
  // 2. Try to sync
  try {
    const response = await api.post('/posts', { title });
    // Update with real ID from server
    setPosts(posts =>
      posts.map(p => p.id === tempId ? response.data : p)
    );
  } catch (err) {
    // Error: show "Retry" button next to post
    setPosts(posts =>
      posts.map(p => p.id === tempId ? { ...p, error: true } : p)
    );
  }
};
```

### 3. Conflict Notification

```typescript
const ConflictPrompt = ({ localChange, serverChange }) => {
  return (
    <Dialog>
      <Text>Changes conflict. Which version?</Text>
      <Button onPress={() => keepLocal()}>Keep my changes</Button>
      <Button onPress={() => useServer()}>Use server version</Button>
      <Button onPress={() => mergeChanges()}>Merge both</Button>
    </Dialog>
  );
};
```

---

## 🧪 Testing Offline-First Code

### 1. Network Mocking

```typescript
// Mock network failure
jest.mock('@react-native-community/netinfo', () => ({
  useNetInfo: () => ({
    isConnected: false,
    isInternetReachable: false,
  }),
}));

test('app loads from cache when offline', async () => {
  const { getByText } = render(<App />);
  
  // Should show cached data
  await waitFor(() => {
    expect(getByText('Cached post 1')).toBeTruthy();
  });
  
  // Should queue changes
  const queue = await syncQueue.getPending();
  expect(queue.length).toBeGreaterThan(0);
});
```

### 2. Sync Simulation

```typescript
test('syncs changes when network restores', async () => {
  // 1. Make change offline
  fireEvent.press(getByText('Update'));
  
  // 2. Verify queued
  let pending = await syncQueue.getPending();
  expect(pending.length).toBe(1);
  
  // 3. Restore network
  NetworkService.setOnline(true);
  
  // 4. Verify synced
  await waitFor(async () => {
    pending = await syncQueue.getPending();
    expect(pending.length).toBe(0);
  });
});
```

### 3. Conflict Handling

```typescript
test('resolves conflicts with latest-write-wins', async () => {
  const local = { title: 'Local Edit', updatedAt: 1000 };
  const server = { title: 'Server Edit', updatedAt: 2000 };
  
  const resolved = resolveConflict(local, server);
  expect(resolved.title).toBe('Server Edit'); // Server is newer
});
```

---

## ✅ Offline-First Checklist

- [ ] Local DB (WatermelonDB, Realm, Room, Isar): set up and tested
- [ ] All reads default to local DB first
- [ ] Writes are optimistic (show immediately)
- [ ] Event log queues changes for sync
- [ ] Network status monitoring implemented
- [ ] Auto-sync on network restore
- [ ] Conflict resolution strategy chosen & implemented
- [ ] Sync status visible to user
- [ ] Sensitive data encrypted at rest
- [ ] Soft deletes (not hard) for all deletions
- [ ] E2E test: offline create → online sync → server confirmed
- [ ] E2E test: conflict scenario handled gracefully

---

**Version**: 2.7.0  
**Last Updated**: 2026-04-09  
**Author**: SmartWorkz Dev
