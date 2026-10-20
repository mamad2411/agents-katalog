---
name: mongodb-conventions
description:
  This skill should be used when working on MongoDB databases, designing document schemas, creating
  collections, or reviewing MongoDB code. It provides document modeling rules, BSON type guidance,
  collection design conventions, JSON Schema validator patterns, and existing repository
  compatibility checks for consistent MongoDB development.
version: 0.1.0
---

# MongoDB Conventions Skill

This skill defines the conventions, rules, and best practices for MongoDB development. Apply these
rules when creating collections, designing document schemas, writing queries, or reviewing MongoDB
code.

---

## Table of Contents

1. [Document Modeling Rules](#document-modeling-rules)
2. [BSON Type Rules](#bson-type-rules)
3. [Collection Design Rules](#collection-design-rules)
4. [JSON Schema Validator Rules](#json-schema-validator-rules)
5. [Query and Update Rules](#query-and-update-rules)
6. [Existing Repo Compatibility](#existing-repo-compatibility)
7. [Safety Conventions](#safety-conventions)

---

## Document Modeling Rules

### Rule DM-1: Embed vs Reference Decision Tree

Always evaluate the following criteria before embedding or referencing related data. Never default
to either approach without analysis.

**Embed when ALL of these are true:**

- The related data is always accessed with the parent
- The related data is owned by the parent (no sharing)
- The related data set is bounded and small (< 500 elements)
- The combined document stays well under 2 MB

**Reference when ANY of these are true:**

- The related data is shared across multiple parents
- The related data grows without bound
- The related data is updated independently of the parent
- The related data set is large (> 500 elements)
- The relationship is many-to-many

```javascript
// CORRECT — embed address in user (1:1, always accessed together, owned)
{
  _id: ObjectId("64a1b2c3d4e5f6a7b8c9d0e1"),
  name: "Jane Doe",
  email: "jane@example.com",
  address: {
    street: "123 Main St",
    city: "Portland",
    state: "OR",
    zip: "97201"
  }
}

// CORRECT — reference for shared data (product in multiple orders)
// orders collection
{
  _id: ObjectId("65c0d1e2f3a4b5c6d7e8f9a0"),
  customerId: ObjectId("64a1b2c3d4e5f6a7b8c9d0e1"),
  items: [
    { productId: ObjectId("64b2c3d4e5f6a7b8c9d0e1f2"), quantity: 2, price: NumberDecimal("79.99") }
  ]
}
```

```javascript
// WRONG — embedding shared data (product duplicated in every order)
{
  _id: ObjectId("65c0d1e2f3a4b5c6d7e8f9a0"),
  items: [
    {
      product: { /* entire 30-field product document duplicated */ },
      quantity: 2
    }
  ]
}

// WRONG — referencing 1:1 data that is always accessed together
// Two separate collections just for user + address
// users collection
{ _id: ..., name: "Jane", email: "jane@example.com" }
// addresses collection
{ _id: ..., userId: ..., street: "123 Main", city: "Portland" }
// Requires $lookup for every user query
```

### Rule DM-2: Use the Subset Pattern for Partial Embedding

When a related entity is large but a summary is frequently needed, embed only a subset and reference
the full document.

```javascript
// CORRECT — subset pattern: recent reviews embedded, full reviews referenced
// products collection
{
  _id: ObjectId("64b2c3d4e5f6a7b8c9d0e1f2"),
  name: "Wireless Headphones",
  price: NumberDecimal("79.99"),
  recentReviews: [
    { _id: ObjectId("..."), author: "alice", rating: 5, snippet: "Great..." },
    { _id: ObjectId("..."), author: "bob", rating: 4, snippet: "Good..." }
  ],
  reviewCount: 247,
  averageRating: 4.3
}

// reviews collection (full data)
{
  _id: ObjectId("..."),
  productId: ObjectId("64b2c3d4e5f6a7b8c9d0e1f2"),
  author: "alice",
  rating: 5,
  title: "Great sound quality and battery life",
  body: "I have been using these headphones for two weeks now...",
  date: ISODate("2024-01-15T10:30:00Z"),
  helpful: 42,
  verified: true
}
```

```javascript
// WRONG — embed all 247 reviews in the product document
{
  name: "Wireless Headphones",
  reviews: [ /* all 247 full reviews — approaches 16 MB limit */ ]
}
```

### Rule DM-3: Use Extended Reference for Denormalization

When a reference is frequently joined, copy the most-needed fields into the referencing document.
Document which fields are denormalized and maintain consistency.

```javascript
// CORRECT — extended reference in order
{
  _id: ObjectId("65c0d1e2f3a4b5c6d7e8f9a0"),
  customer: {
    _id: ObjectId("64a1b2c3d4e5f6a7b8c9d0e1"),
    name: "Jane Doe",          // Denormalized — updated on customer change
    email: "jane@example.com"  // Denormalized — updated on customer change
  },
  items: [
    {
      productId: ObjectId("64b2c3d4e5f6a7b8c9d0e1f2"),
      name: "Wireless Headphones",  // Snapshot at order time (NOT updated)
      price: NumberDecimal("79.99") // Snapshot at order time (NOT updated)
    }
  ]
}
```

### Rule DM-4: Limit Array Size to 500 Elements

Arrays embedded in documents should not exceed 500 elements. For larger sets, use a separate
collection with parent references.

```javascript
// CORRECT — bounded array for course enrollments (max 30 students)
{
  _id: ObjectId("64f7a8b9c0d1e2f3a4b5c6d7"),
  title: "MongoDB Fundamentals",
  enrolledStudentIds: [ /* max 30 ObjectIds */ ],
  maxEnrollment: 30
}

// CORRECT — separate collection for unbounded relationships
// followers collection
{
  _id: ObjectId("..."),
  userId: ObjectId("64a1b2c3d4e5f6a7b8c9d0e1"),    // Who is being followed
  followerId: ObjectId("65d1e2f3a4b5c6d7e8f9a0b1"), // Who is following
  followedAt: ISODate("2024-03-01T10:00:00Z")
}
```

```javascript
// WRONG — unbounded array of followers
{
  _id: ObjectId("64a1b2c3d4e5f6a7b8c9d0e1"),
  username: "popular_user",
  followerIds: [ /* potentially millions */ ]
}
```

### Rule DM-5: Keep Documents Under 2 MB

While MongoDB allows 16 MB documents, target under 2 MB for optimal performance. Larger documents
increase memory pressure, slow network transfer, and complicate partial updates.

### Rule DM-6: Use the Bucket Pattern for High-Volume Data

Group time-series or high-volume data into buckets to reduce document count.

```javascript
// CORRECT — bucket pattern for sensor data (60 readings per bucket)
{
  sensorId: "temp-001",
  bucketStart: ISODate("2024-03-15T10:00:00Z"),
  bucketEnd: ISODate("2024-03-15T10:59:59Z"),
  count: 60,
  readings: [
    { ts: ISODate("2024-03-15T10:00:00Z"), value: 22.1 },
    { ts: ISODate("2024-03-15T10:01:00Z"), value: 22.3 }
    // ... up to 60 readings
  ],
  stats: { min: 21.8, max: 23.1, avg: 22.4 }
}
```

```javascript
// WRONG — one document per sensor reading (millions of tiny documents)
{
  sensorId: "temp-001",
  timestamp: ISODate("2024-03-15T10:00:00Z"),
  value: 22.1
}
// Consider time series collections (MongoDB 5.0+) as an alternative
```

### Rule DM-7: Use the Polymorphic Pattern with Discriminators

When storing different entity types in one collection, always include a `type` or `kind`
discriminator field. Create partial indexes for type-specific fields.

```javascript
// CORRECT — discriminator with partial indexes
// media collection
{ type: "book",    title: "MongoDB in Action", isbn: "978-..." }
{ type: "movie",   title: "The Matrix",        director: "Wachowskis" }
{ type: "podcast", title: "MongoDB Podcast",   host: "..." }

// Partial indexes
db.media.createIndex({ isbn: 1 }, { partialFilterExpression: { type: "book" } });
db.media.createIndex({ director: 1 }, { partialFilterExpression: { type: "movie" } });
```

```javascript
// WRONG — no discriminator field
// How do you query for only books? Only movies?
{ title: "MongoDB in Action", isbn: "978-..." }
{ title: "The Matrix", director: "Wachowskis" }
// Must check for field existence: { isbn: { $exists: true } }
```

---

## BSON Type Rules

### Rule BT-1: Use ISODate for All Timestamps

Never store dates as strings. Always use ISODate (BSON Date type) for timestamps, dates, and any
temporal data.

```javascript
// CORRECT — ISODate for timestamps
{
  createdAt: ISODate("2024-01-15T10:30:00Z"),
  scheduledFor: ISODate("2024-02-01T09:00:00Z"),
  expiresAt: ISODate("2024-12-31T23:59:59.999Z")
}

// WRONG — date strings
{
  createdAt: "2024-01-15T10:30:00Z",   // String, not queryable as date
  scheduledFor: "01/15/2024",           // Ambiguous format
  expiresAt: "December 31, 2024"        // Not sortable or comparable
}
```

### Rule BT-2: Use Decimal128 for Monetary and Precision Values

Never use regular numbers (IEEE 754 doubles) for money or any value requiring exact decimal
precision.

```javascript
// CORRECT — Decimal128 for money
{
  price: NumberDecimal("19.99"),
  tax: NumberDecimal("1.60"),
  total: NumberDecimal("21.59")
}

// WRONG — double for money
{
  price: 19.99,    // IEEE 754: 19.989999999999998...
  tax: 1.60,       // Rounding errors accumulate in aggregation
  total: 21.59
}
```

When to use Decimal128:

- Monetary values (prices, balances, taxes, fees)
- Exchange rates and financial ratios
- Scientific measurements requiring exact precision
- Any value where `0.1 + 0.2 === 0.3` must be true

### Rule BT-3: Use ObjectId for References

Use ObjectId for inter-document references unless there is a specific reason to use another type
(e.g., natural keys from external systems).

```javascript
// CORRECT — ObjectId references
{
  customerId: ObjectId("65d1e2f3a4b5c6d7e8f9a0b1"),
  productId: ObjectId("64b2c3d4e5f6a7b8c9d0e1f2")
}

// WRONG — string references when ObjectId would work
{
  customerId: "65d1e2f3a4b5c6d7e8f9a0b1",  // String, not ObjectId
  productId: "64b2c3d4e5f6a7b8c9d0e1f2"
}
```

When to use non-ObjectId identifiers:

- External system IDs (UUIDs from microservices)
- Natural keys (ISBN, email as unique ID, SKU)
- Cross-database references where ObjectId might collide

### Rule BT-4: Use NumberLong for Large Integers

JavaScript numbers lose precision beyond `Number.MAX_SAFE_INTEGER` (9,007,199,254,740,991). Use
NumberLong for counters, file sizes, or any integer that might exceed this.

```javascript
// CORRECT — NumberLong for large integers
{
  viewCount: NumberLong("9007199254740993"),
  fileSize: NumberLong("5368709120")    // 5 GB in bytes
}

// WRONG — regular number for large integers
{
  viewCount: 9007199254740993   // Loses precision!
}
```

### Rule BT-5: Use Binary for Hash Values and Tokens

Store cryptographic hashes, encrypted tokens, and UUIDs as Binary data, not as hex strings.

```javascript
// CORRECT — Binary for UUIDs (subtype 4)
{
  externalId: BinData(4, 'kO0ECdrNEe6VGwAiDMClQQ==');
}

// CORRECT — Binary for password hashes (subtype 0)
{
  passwordHash: BinData(0, 'JDJiJDEyJGFiY2RlZmdoaWprbG1ub3BxcnN0dQ==');
}

// WRONG — hex string for UUID (wastes 2x storage)
{
  externalId: '90ed040d-dacd-11ee-951b-00220cc0a541';
}
```

### Rule BT-6: Never Use the Timestamp BSON Type for Application Data

The BSON Timestamp type is reserved for MongoDB internal use (replication oplog). Use ISODate for
application timestamps.

```javascript
// WRONG — Timestamp for application dates
{
  createdAt: Timestamp(1705312200, 1);
}

// CORRECT — ISODate for application dates
{
  createdAt: ISODate('2024-01-15T10:30:00Z');
}
```

---

## Collection Design Rules

### Rule CD-1: Use Plural Nouns for Collection Names

Collection names must be plural nouns describing the entity type stored.

```javascript
// CORRECT — plural nouns
db.users;
db.orders;
db.products;
db.orderLineItems;
db.paymentTransactions;

// WRONG — singular nouns
db.user;
db.order;
db.product;
```

### Rule CD-2: Consistent Naming Convention

Choose one naming convention for collections and apply it across the entire database. Match the
dominant language/framework convention.

| Language/Framework | Convention | Example            |
| ------------------ | ---------- | ------------------ |
| JavaScript/Node    | camelCase  | `orderLineItems`   |
| Python             | snake_case | `order_line_items` |
| Go                 | camelCase  | `orderLineItems`   |
| Java               | camelCase  | `orderLineItems`   |
| C#                 | PascalCase | `OrderLineItems`   |

```javascript
// CORRECT — consistent camelCase (JavaScript project)
db.userProfiles;
db.orderItems;
db.paymentTransactions;

// WRONG — mixed conventions
db.userProfiles; // camelCase
db.order_items; // snake_case
db.PaymentHistory; // PascalCase
```

### Rule CD-3: Limit Nesting to 3 Levels

Document nesting should not exceed 3 levels of depth. Deeper nesting makes queries complex, updates
fragile, and indexing impractical.

```javascript
// CORRECT — 2 levels of nesting
{
  name: "Jane Doe",
  address: {                    // Level 1
    street: "123 Main St",
    city: "Portland",
    geo: {                      // Level 2
      lat: 45.5152,
      lng: -122.6784
    }
  }
}

// WRONG — 4+ levels of nesting
{
  order: {                      // Level 1
    details: {                  // Level 2
      shipping: {               // Level 3
        address: {              // Level 4 — too deep
          coordinates: {        // Level 5 — way too deep
            lat: 45.5152
          }
        }
      }
    }
  }
}
```

### Rule CD-4: Use Descriptive Collection Names

Collection names must be self-documenting. Avoid abbreviations unless they are universally
understood in the domain.

```javascript
// CORRECT — descriptive names
db.users;
db.orderLineItems;
db.paymentTransactions;
db.auditLogs;
db.inventoryAdjustments;

// WRONG — abbreviated names
db.usr;
db.oli;
db.pmtTxn;
db.audlog;
db.invAdj;
```

### Rule CD-5: Discriminator Pattern for Polymorphic Collections

When multiple entity types share a collection, always include a discriminator field (`type`, `kind`,
or `_type`) and document the allowed values.

```javascript
// CORRECT — clear discriminator with documented values
// notifications collection: type = "email" | "sms" | "push"
{
  type: "email",
  recipientId: ObjectId("..."),
  status: "sent",
  subject: "Order shipped",
  body: "<html>..."
}
{
  type: "sms",
  recipientId: ObjectId("..."),
  status: "delivered",
  phoneNumber: "+1-555-0101",
  message: "Order shipped!"
}
```

### Rule CD-6: Use Time Series Collections for IoT/Metrics

For time-series data (IoT sensors, application metrics, event logs), use MongoDB 5.0+ time series
collections instead of regular collections.

```javascript
// CORRECT — time series collection
db.createCollection('sensorReadings', {
  timeseries: {
    timeField: 'timestamp',
    metaField: 'sensorId',
    granularity: 'minutes',
  },
  expireAfterSeconds: 2592000, // 30-day retention
});

// WRONG — regular collection for time series data
db.createCollection('sensorReadings');
// Missing: time series optimizations, automatic bucketing, TTL
```

### Rule CD-7: System Collection Prefix Reservation

Never create collections starting with `system.` — this prefix is reserved for MongoDB internal use.

```javascript
// WRONG — system prefix
db.createCollection('system.myCustomLogs');

// CORRECT — descriptive prefix
db.createCollection('appSystemLogs');
```

---

## JSON Schema Validator Rules

### Rule JV-1: Every Write-Target Collection Needs a Validator

Any collection that receives inserts or updates from application code must have a JSON Schema
validator defined.

```javascript
// CORRECT — validator on collection creation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['email', 'name', 'role', 'createdAt'],
      properties: {
        email: { bsonType: 'string', pattern: '^.+@.+\\..+$' },
        name: {
          bsonType: 'object',
          required: ['first', 'last'],
          properties: {
            first: { bsonType: 'string', minLength: 1 },
            last: { bsonType: 'string', minLength: 1 },
          },
        },
        role: { bsonType: 'string', enum: ['admin', 'editor', 'viewer'] },
        createdAt: { bsonType: 'date' },
      },
    },
  },
  validationLevel: 'strict',
  validationAction: 'error',
});
```

### Rule JV-2: Use bsonType Instead of type

In MongoDB JSON Schema validators, use `bsonType` for MongoDB-specific types.

```javascript
// CORRECT — bsonType
{
  bsonType: 'objectId';
}
{
  bsonType: 'date';
}
{
  bsonType: 'decimal';
}
{
  bsonType: 'long';
}
{
  bsonType: 'int';
}
{
  bsonType: 'binData';
}

// WRONG — JSON Schema type (does not map to BSON)
{
  type: 'number';
} // Ambiguous: int, long, double, or decimal?
```

### Rule JV-3: Use strict Validation for New Collections

New collections must use `validationLevel: "strict"`. Use `"moderate"` only during schema migrations
on existing collections.

```javascript
// CORRECT — strict for new collections
validationLevel: 'strict';

// CORRECT — moderate during migration
// Temporarily set to moderate while backfilling new required fields
validationLevel: 'moderate';
// Then switch back to strict after migration completes
```

### Rule JV-4: Use error Validation Action in Production

Production collections should use `validationAction: "error"` to reject invalid writes. Use `"warn"`
only in development or during migration testing.

### Rule JV-5: Include Description Fields

Add `description` fields to validator properties for documentation.

```javascript
// CORRECT — descriptions for documentation
{
  email: {
    bsonType: "string",
    pattern: "^.+@.+\\..+$",
    description: "User email address, must be unique"
  },
  role: {
    bsonType: "string",
    enum: ["admin", "editor", "viewer"],
    description: "User role determining access permissions"
  }
}
```

### Rule JV-6: Validators Must Be Version-Controlled

JSON Schema validators must be defined in version-controlled scripts, not applied manually via
mongosh. This ensures reproducibility and auditability.

```javascript
// CORRECT — validator in a versioned migration script
// migrations/001_create_users_collection.js
db.createCollection('users', {
  validator: {
    /* ... */
  },
  validationLevel: 'strict',
  validationAction: 'error',
});

// WRONG — applied manually in production mongosh session
// (Not reproducible, not auditable, no code review)
```

---

## Query and Update Rules

### Rule QU-1: Always Use $set for Partial Updates

Never replace entire documents when only specific fields need updating.

```javascript
// CORRECT — $set for partial update
db.users.updateOne(
  { _id: userId },
  {
    $set: { email: 'new@example.com', updatedAt: new Date() },
  }
);

// WRONG — replace entire document
db.users.replaceOne(
  { _id: userId },
  { name: 'Jane', email: 'new@example.com' /* must include ALL fields */ }
);
```

### Rule QU-2: Use $push with $slice for Bounded Arrays

When pushing to arrays, always include `$slice` to prevent unbounded growth.

```javascript
// CORRECT — bounded push
db.users.updateOne(
  { _id: userId },
  {
    $push: {
      recentActivity: {
        $each: [{ action: 'login', ts: new Date() }],
        $slice: -50, // Keep only the 50 most recent
      },
    },
  }
);

// WRONG — unbounded push
db.users.updateOne({ _id: userId }, { $push: { activity: { action: 'login', ts: new Date() } } });
```

### Rule QU-3: Use Bulk Operations for Multiple Writes

When performing multiple write operations, use bulkWrite for efficiency.

```javascript
// CORRECT — bulk operations
db.products.bulkWrite(
  [
    {
      updateOne: {
        filter: { _id: id1 },
        update: { $set: { price: NumberDecimal('29.99') } },
      },
    },
    {
      updateOne: {
        filter: { _id: id2 },
        update: { $set: { price: NumberDecimal('39.99') } },
      },
    },
    {
      updateOne: {
        filter: { _id: id3 },
        update: { $inc: { stock: -1 } },
      },
    },
  ],
  { ordered: false }
); // Unordered for maximum parallelism

// WRONG — individual updates in a loop
for (const update of updates) {
  await db.products.updateOne({ _id: update.id }, { $set: { price: update.price } });
}
```

### Rule QU-4: Use Projection to Limit Returned Fields

Always project only the fields needed by the consumer.

```javascript
// CORRECT — explicit projection
db.users.find(
  { status: 'active' },
  { name: 1, email: 1, role: 1, _id: 1 } // Only needed fields
);

// WRONG — return all fields
db.users.find({ status: 'active' });
// Returns all 30 fields when only 4 are needed
```

### Rule QU-5: Use explain() Before Deploying Queries

Before deploying any new query to production, verify its execution plan.

```javascript
// CORRECT — verify with explain
db.orders
  .find({ customerId: id, status: 'completed' })
  .sort({ orderDate: -1 })
  .explain('executionStats');

// Check:
// - stage is "IXSCAN" not "COLLSCAN"
// - totalKeysExamined ~ totalDocsExamined ~ nReturned
// - executionTimeMillis is acceptable
```

---

## Existing Repo Compatibility

### Rule RC-1: Match Existing Naming Convention

When adding new collections or fields to an existing project, detect and match the existing naming
convention. Never introduce a new convention.

### Rule RC-2: Match Existing ODM Patterns

If the project uses Mongoose, generate Mongoose schemas. If it uses Prisma, generate Prisma models.
Never introduce a competing tool.

### Rule RC-3: Match Existing Directory Structure

Place new files in the same directory structure used by existing models/schemas.

```text
// If existing structure is:
src/
  models/
    User.js
    Order.js

// New collection goes in:
src/
  models/
    Product.js    // Same directory, same naming pattern
```

### Rule RC-4: Match Existing Validation Patterns

If existing collections use Mongoose validation, use Mongoose validation for new collections. If
they use MongoDB JSON Schema validators, use those.

### Rule RC-5: Check for TypeScript

If the project uses TypeScript, generate TypeScript files with proper type annotations. Never
generate plain JavaScript in a TypeScript project.

```typescript
// CORRECT — TypeScript in a TS project
import { Schema, model, Document } from 'mongoose';

interface IUser extends Document {
  email: string;
  name: { first: string; last: string };
  role: 'admin' | 'editor' | 'viewer';
  createdAt: Date;
}

const userSchema = new Schema<IUser>({
  /* ... */
});
export const User = model<IUser>('User', userSchema);
```

---

## Safety Conventions

### Rule SC-1: Never Connect to Production Without Confirmation

Before running any command against a production database, display the connection string (masking
credentials) and require explicit user confirmation.

### Rule SC-2: Never Include Real Credentials

All code, configurations, and examples must use environment variables or placeholders for
credentials.

```javascript
// CORRECT
const uri = process.env.MONGODB_URI;

// WRONG
const uri = 'mongodb+srv://admin:secret@prod.mongodb.net/mydb';
```

### Rule SC-3: Backup Before Schema Migrations

Always recommend creating a backup or snapshot before running any schema migration on collections
with existing data.

### Rule SC-4: Use Write Concern Majority for Critical Writes

Default to `{ w: "majority" }` for any write affecting data integrity.

### Rule SC-5: Test Validators Before Production Deployment

Always test JSON Schema validators against sample data before applying to production collections.
Use `validationAction: "warn"` in staging to identify documents that would fail validation.

### Rule SC-6: Never Use $where in Application Code

`$where` executes arbitrary JavaScript and bypasses indexes. It is a security risk (injection) and
performance antipattern.

```javascript
// WRONG — $where
db.users.find({ $where: 'this.age > 21' });

// CORRECT — standard operators
db.users.find({ age: { $gt: 21 } });
```

### Rule SC-7: Validate ObjectId Format Before Queries

When accepting user input as ObjectId, validate the format before using it in queries to prevent
injection and errors.

```javascript
// CORRECT — validate before query
const { ObjectId } = require('mongodb');

function isValidObjectId(id) {
  return ObjectId.isValid(id) && new ObjectId(id).toString() === id;
}

if (isValidObjectId(req.params.id)) {
  const user = await db.users.findOne({ _id: new ObjectId(req.params.id) });
}
```

---

## Index Conventions

### Rule IX-1: Follow the ESR Rule for Compound Indexes

Order compound index fields as: Equality, Sort, Range.

```javascript
// Query: find active users in a city, sorted by createdAt
db.users
  .find({
    status: 'active', // Equality
    createdAt: { $gte: ISODate('2024-01-01') }, // Range
  })
  .sort({ lastName: 1 }); // Sort

// CORRECT — ESR order
db.users.createIndex({ status: 1, lastName: 1, createdAt: 1 });

// WRONG — Range before Sort
db.users.createIndex({ status: 1, createdAt: 1, lastName: 1 });
```

### Rule IX-2: Use Partial Indexes for Discriminated Collections

When a collection uses the polymorphic/discriminator pattern, create partial indexes for
type-specific fields.

```javascript
// CORRECT — partial indexes for discriminated collection
db.notifications.createIndex({ subject: 1 }, { partialFilterExpression: { type: 'email' } });

db.notifications.createIndex({ phoneNumber: 1 }, { partialFilterExpression: { type: 'sms' } });
```

### Rule IX-3: Use TTL Indexes for Expiring Data

For session data, temporary tokens, and cache entries, use TTL indexes instead of manual cleanup
jobs.

```javascript
// CORRECT — TTL index for sessions
db.sessions.createIndex(
  { lastActivity: 1 },
  { expireAfterSeconds: 86400 } // Expire after 24 hours
);

// CORRECT — TTL with explicit expiry date
db.verificationTokens.createIndex(
  { expiresAt: 1 },
  { expireAfterSeconds: 0 } // Expire at the date in expiresAt field
);
```

### Rule IX-4: Always Verify Index Usage with explain()

Before deploying new queries or indexes to production, verify the query execution plan.

```javascript
// CORRECT — check execution plan
db.orders
  .find({ customerId: id, status: 'active' })
  .sort({ orderDate: -1 })
  .explain('executionStats');

// Verify these indicators:
// - winningPlan.stage === "IXSCAN" (not "COLLSCAN")
// - totalKeysExamined ~= nReturned (no excessive scanning)
// - executionTimeMillis is within acceptable range
```

### Rule IX-5: Keep Index Count Under 10 Per Collection

Each index adds overhead to write operations and consumes RAM. Monitor index counts and drop unused
indexes.

```javascript
// CORRECT — audit index usage periodically
db.orders.aggregate([{ $indexStats: {} }]);

// Drop indexes with zero ops.since.restart
// (after verifying no seasonal queries depend on them)
```

---

## Error Handling Conventions

### Rule EH-1: Always Handle MongoDB Driver Errors

Wrap all MongoDB operations in proper error handling with specific error code checks.

```javascript
// CORRECT — handle specific MongoDB errors
try {
  await db.collection('users').insertOne(userData);
} catch (error) {
  if (error.code === 11000) {
    // Duplicate key violation
    throw new ConflictError('User with this email already exists');
  }
  if (error.code === 121) {
    // Document validation failure
    throw new ValidationError('User data does not match schema');
  }
  throw error; // Re-throw unexpected errors
}
```

```javascript
// WRONG — swallow all errors
try {
  await db.collection('users').insertOne(userData);
} catch (error) {
  console.log('Insert failed'); // No error details, no re-throw
}
```

### Rule EH-2: Handle Transaction Errors with Retry Logic

Transactions must include retry logic for transient errors.

```javascript
// CORRECT — transaction with retry
async function runWithRetry(session, txnFn) {
  while (true) {
    try {
      await txnFn(session);
      break;
    } catch (error) {
      if (error.hasErrorLabel('TransientTransactionError')) {
        continue; // Retry the entire transaction
      }
      throw error;
    }
  }
}

async function commitWithRetry(session) {
  while (true) {
    try {
      await session.commitTransaction();
      break;
    } catch (error) {
      if (error.hasErrorLabel('UnknownTransactionCommitResult')) {
        continue; // Retry commit
      }
      throw error;
    }
  }
}
```
