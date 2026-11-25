---
name: firestore-data-modeling-patterns
version: "1.0"
description: >
  Firestore data modeling best practices including subcollections, document structure, and atomic operations.
  PROACTIVELY activate for: (1) designing Firestore collection structures, (2) choosing between subcollections vs root collections, (3) implementing transactions vs batched writes.
  Triggers: "subcollection", "data model", "firestore"
group: data
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Firestore Data Modeling Patterns

## Overview

Firestore is a NoSQL document database that requires careful modeling to optimize for query patterns, scalability, and cost. This skill provides patterns for structuring data effectively.

## Subcollections vs. Root Collections

### When to Use Subcollections

**Pattern**: `users/{userId}/orders/{orderId}`

**Use When**:
- Data is tightly coupled to a parent (orders belong to a specific user)
- Child data is always accessed via parent
- You don't need to query children globally across all parents
- Document hierarchy makes semantic sense

**Example**:
```typescript
// User's private sessions (accessed only via user)
users/{userId}/sessions/{sessionId}

// User's notification preferences
users/{userId}/settings/notifications
```

**Critical Limitation**: Deleting a parent document **does NOT** delete subcollections. You must implement cleanup logic (e.g., Cloud Function).

### When to Use Root Collections

**Pattern**: Separate `users` and `posts` collections with reference fields

**Use When**:
- Need to query data globally (e.g., "all posts across all users")
- Data has many-to-many relationships
- Want simpler deletion semantics (no orphaned data risk)
- Need flexibility for future access patterns

**Example**:
```typescript
// posts collection
{
  id: "post1",
  authorId: "user123",  // Reference to users collection
  title: "...",
  createdAt: Timestamp
}

// Query all posts by a user
postsRef.where('authorId', '==', 'user123').get()

// Query all posts globally
postsRef.orderBy('createdAt', 'desc').limit(10).get()
```

**Decision Matrix**:

| Criterion | Subcollection | Root Collection |
|-----------|--------------|-----------------|
| Query across parents | Requires Collection Group Query | Simple query |
| Deletion cascade | Manual cleanup needed | Independent lifecycle |
| Document limit (1MB) | Spreads data | Risk if embedding arrays |
| Semantic hierarchy | Clear parent-child | Relies on references |

## Document Structure Best Practices

### Embedding vs. Referencing

**Embed When**:
- Data is small and frequently accessed together
- 1-to-1 or 1-to-few relationships
- Data doesn't change frequently

```typescript
// User profile with embedded address
{
  id: "user1",
  name: "Alice",
  address: {
    street: "123 Main St",
    city: "NYC",
    zip: "10001"
  }
}
```

**Reference When**:
- Data is large or changes frequently
- 1-to-many or many-to-many relationships
- Need to query the related data independently

```typescript
// Post references author
{
  id: "post1",
  title: "My Post",
  authorId: "user1", // Reference
  categoryIds: ["cat1", "cat2"] // Many-to-many
}
```

### Document Size Limits

- **Max Document Size**: 1MB
- **Max Array Size**: 20,000 elements (but practical limit is much lower for performance)
- **Max Nesting Depth**: 20 levels

## Atomic Operations

### Transactions (Read-Modify-Write)

**Use When**: Write depends on current document state

**Example**: Increment a counter
```typescript
import { runTransaction } from 'firebase/firestore';

await runTransaction(db, async (transaction) => {
  const postRef = doc(db, 'posts', 'post1');
  const postDoc = await transaction.get(postRef);

  if (!postDoc.exists()) {
    throw new Error('Post does not exist');
  }

  const newViewCount = postDoc.data().viewCount + 1;
  transaction.update(postRef, { viewCount: newViewCount });
});
```

**Characteristics**:
- Reads must precede writes
- Automatic retries on conflicts
- Fails if offline
- Limited to 500 documents

### Batched Writes (Write-Only)

**Use When**: Multiple independent write operations need atomicity

**Example**: Create user + settings document
```typescript
import { writeBatch } from 'firebase/firestore';

const batch = writeBatch(db);

const userRef = doc(db, 'users', 'user1');
batch.set(userRef, {
  name: 'Alice',
  email: 'alice@example.com',
  createdAt: serverTimestamp(),
});

const settingsRef = doc(db, 'users', 'user1', 'settings', 'notifications');
batch.set(settingsRef, {
  emailNotifications: true,
  pushNotifications: false,
});

await batch.commit(); // All succeed or all fail
```

**Characteristics**:
- Faster than transactions
- Works offline (queued)
- Up to 500 operations
- No reads allowed

**Decision Rule**: Default to batched writes (simpler, faster). Use transactions only when reads are required.

## Best Practices Summary

**Do**:
- Denormalize data for read-heavy applications
- Use root collections for flexibility
- Create composite indexes for complex queries
- Use batched writes for atomic multi-document updates
- Keep documents under 1MB

**Don't**:
- Embed large arrays or frequently-changing data
- Use subcollections without cleanup strategy
- Create excessive indexes (storage cost + write latency)
- Assume parent deletion cascades to subcollections
- Use transactions when batches suffice

---

**Related Skills**: `zod-firestore-type-safety`, `firebase-nextjs-integration-strategies`
