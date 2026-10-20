---
name: zod-firestore-type-safety
version: "1.0"
description: >
  End-to-end type safety for Firestore using Zod schemas with withConverter API.
  PROACTIVELY activate for: (1) implementing Firestore converters with Zod validation, (2) ensuring runtime validation at application boundaries, (3) evolving schemas safely.
  Triggers: "zod converter", "firestore type safety", "withConverter"
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

# Zod Firestore Type Safety

## Overview

Firestore is schemaless, creating a mismatch with TypeScript's compile-time types. Zod bridges this gap by providing runtime validation at the application boundary, ensuring data integrity.

## Core Pattern: Zod + withConverter

### The Atomic Unit

Every Firestore collection requires three components:

1. **Zod Schema**: Runtime validation definition
2. **TypeScript Type**: Inferred from Zod schema
3. **Converters**: Client and server withConverter objects

**Template**:
```typescript
import { z } from 'zod';
import { Timestamp } from 'firebase/firestore';

// 1. Zod Schema
export const UserSchema = z.object({
  id: z.string(),
  name: z.string().min(1, 'Name required').max(100),
  email: z.string().email('Invalid email'),
  role: z.enum(['admin', 'user', 'moderator']),
  age: z.number().int().positive().optional(),
  createdAt: z.instanceof(Timestamp),
  updatedAt: z.instanceof(Timestamp),
});

// 2. Inferred TypeScript Type
export type User = z.infer<typeof UserSchema>;

// 3. Converters (import from shared utility)
import { zodConverter, zodAdminConverter } from '@/lib/firebase/zodConverter';

export const userConverter = zodConverter(UserSchema);
export const userAdminConverter = zodAdminConverter(UserSchema);
```

### Generic Zod Converter Implementation

```typescript
// lib/firebase/zodConverter.ts
import type {
  DocumentData,
  FirestoreDataConverter,
  QueryDocumentSnapshot,
  SnapshotOptions,
  WithFieldValue,
} from 'firebase/firestore';
import type { ZodSchema } from 'zod';

/**
 * Client-side converter with validation on read and write
 * Automatically injects document ID and ref
 */
export function zodConverter<T extends DocumentData>(
  schema: ZodSchema<T>
): FirestoreDataConverter<T> {
  return {
    toFirestore(data: WithFieldValue<T>): DocumentData {
      // Validate before writing to Firestore
      const validated = schema.parse(data);
      return validated;
    },
    fromFirestore(
      snapshot: QueryDocumentSnapshot<DocumentData>,
      options?: SnapshotOptions
    ): T {
      const data = snapshot.data(options);

      // Inject document metadata for convenience
      const dataWithMeta = {
        ...data,
        id: snapshot.id,
        ref: snapshot.ref,
      };

      // Validate after reading from Firestore
      return schema.parse(dataWithMeta) as T;
    },
  };
}
```

## Usage Examples

### Client-Side (React Component)

```typescript
'use client';

import { collection, doc, getDoc, getDocs, query, where } from 'firebase/firestore';
import { db } from '@/lib/firebase/client';
import { userConverter, type User } from '@/lib/firebase/schemas/user.schema';

export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    async function fetchUser() {
      // Use withConverter for type-safe, validated read
      const userRef = doc(db, 'users', userId).withConverter(userConverter);
      const userDoc = await getDoc(userRef);

      if (userDoc.exists()) {
        const userData = userDoc.data(); // Type: User (validated!)
        setUser(userData);
      }
    }
    fetchUser();
  }, [userId]);

  return <div>{user?.name}</div>;
}
```

### Server-Side (Next.js Server Component)

```typescript
// app/users/page.tsx
import { adminDb } from '@/lib/firebase/admin';
import { userAdminConverter, type User } from '@/lib/firebase/schemas/user.schema';

export default async function UsersPage() {
  // Use Admin SDK with converter in Server Component
  const usersSnapshot = await adminDb
    .collection('users')
    .withConverter(userAdminConverter)
    .where('role', '==', 'admin')
    .get();

  const users: User[] = usersSnapshot.docs.map(doc => doc.data()); // Type: User[]

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

## Schema Evolution Best Practices

### Adding Optional Fields

When evolving schemas, mark new fields as optional or provide defaults:

```typescript
// Evolution: Add optional viewCount field
export const PostSchema = z.object({
  title: z.string(),
  content: z.string(),
  createdAt: z.instanceof(Timestamp),
  viewCount: z.number().int().nonnegative().default(0), // Default prevents validation errors on old docs
});
```

**Why**: Old documents without `viewCount` will validate successfully with the default value.

## Anti-Patterns

**Skipping Converter**:
```typescript
// BAD: No runtime validation
const userDoc = await getDoc(doc(db, 'users', userId));
const user = userDoc.data(); // Type: any
```

**Using Converter**:
```typescript
// GOOD: Type-safe + validated
const userDoc = await getDoc(doc(db, 'users', userId).withConverter(userConverter));
const user = userDoc.data(); // Type: User (validated)
```

## Best Practices Summary

**Do**:
- Always use `z.infer<typeof Schema>` for types
- Mark new fields as optional when evolving schemas
- Use `.default()` for fields that should have fallback values
- Validate on both read and write for client SDK
- Use `.safeParse()` for user input validation

**Don't**:
- Skip runtime validation with converters
- Use `any` type (use `unknown` with validation)
- Make breaking schema changes without migration
- Hardcode validation logic outside Zod schema

---

**Related Skills**: `firestore-data-modeling-patterns`, `firebase-nextjs-integration-strategies`
