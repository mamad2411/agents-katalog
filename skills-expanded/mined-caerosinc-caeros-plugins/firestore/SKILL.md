---
name: firestore
description: Model, query, and secure Cloud Firestore, collections and documents, security rules, composite indexes, pagination, and aggregations. Use when the user works with Firestore data or rules.
---

# Cloud Firestore

## Data modeling

Documents (max 1 MiB) in collections, nesting via subcollections:
`users/{uid}/orders/{orderId}`. Model for your reads:

- Embed what a screen reads together; documents are the unit of read
  billing and of atomic updates.
- Subcollections for unbounded child data (messages under a chat), arrays in
  the parent doc only for small bounded lists.
- **Collection group queries** read all subcollections of one name across
  parents: `collectionGroup(db, "orders")`; they need their own index scope.
- Duplicate display fields into child docs (denormalize) instead of doing
  client-side joins; there is no server-side join.
- Avoid write hotspots: do not stuff high-frequency counters into one doc
  (use distributed counter shards) and avoid monotonically increasing doc
  IDs; auto-IDs are fine.

## Queries

```js
import { collection, query, where, orderBy, limit, startAfter, getDocs,
         getCountFromServer } from "firebase/firestore"

const q = query(collection(db, "posts"),
  where("published", "==", true),
  where("tags", "array-contains", "firebase"),
  orderBy("createdAt", "desc"),
  limit(20))
const snap = await getDocs(q)

// pagination: cursor on the last doc, never offset
const next = query(q, startAfter(snap.docs.at(-1)))

// aggregation without reading documents
const n = await getCountFromServer(query(collection(db, "posts"),
  where("published", "==", true)))
```

Constraints to design around:
- Every query's result set must be servable by an index; single-field
  indexes are automatic, combinations of `where` + `orderBy` on different
  fields need a composite index. The runtime error helpfully contains a
  creation link; persist the result in `firestore.indexes.json` and deploy
  with `firebase deploy --only firestore:indexes`.
- Range/inequality filters and the first `orderBy` must be on the same
  field (recent releases relaxed multi-field inequalities; check current
  docs before relying on it).
- `array-contains-any` and `in` accept up to 30 values.
- No full-text search; pair with an external search service or the vector
  search extension for semantic cases.
- Realtime: `onSnapshot(q, cb)` streams changes; every listener costs reads
  on updates, so scope listeners tightly.

## Security rules

Rules are the ONLY thing between the public internet and your data; client
SDK access hits them directly.

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{uid} {
      allow read, update: if request.auth != null && request.auth.uid == uid;
      allow create: if request.auth != null && request.auth.uid == uid
                    && request.resource.data.keys().hasOnly(['name', 'bio']);
      allow delete: if false;
    }
    match /posts/{id} {
      allow read: if resource.data.published == true
                  || request.auth.token.admin == true;
      allow write: if request.auth.token.admin == true;
    }
  }
}
```

- `request.auth` is the caller (uid + token claims); `resource.data` is the
  existing doc; `request.resource.data` is the incoming write.
- Rules are not filters: a query must be provably within the rule (querying
  `posts` without `where("published","==",true)` fails even if all results
  happen to be published).
- Admin SDK and Cloud Functions BYPASS rules entirely; enforce server-side
  invariants in code.
- Test rules in the emulator (`@firebase/rules-unit-testing`) and validate
  via the MCP server's rules validation before deploying:
  `firebase deploy --only firestore:rules`.

## Writes

```js
await setDoc(doc(db, "users", uid), data, { merge: true })
await updateDoc(ref, { views: increment(1), updatedAt: serverTimestamp() })
const batch = writeBatch(db); batch.set(a, x); batch.delete(b); await batch.commit()  // max 500 ops
await runTransaction(db, async (tx) => { const s = await tx.get(ref); tx.update(ref, ...) })
```

Prefer `increment`/`arrayUnion`/`serverTimestamp` field transforms over
read-modify-write; they are atomic without a transaction.
