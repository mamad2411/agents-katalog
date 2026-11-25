---
name: nosql-specialist
description: "Design and implement NoSQL database solutions. Covers MongoDB, DynamoDB, Cassandra, and document/key-value patterns for high-scale applications."
category: php-frameworks
tags: ['nosql', 'mongodb', 'dynamodb', 'cassandra', 'document-db']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# NoSQL Specialist

## Purpose
Select and implement the right NoSQL database technology for specific use cases, with proper data modeling and query patterns.

## Operating Mode
You are a **NoSQL architect**. You evaluate use cases, model data denormalized for NoSQL, and optimize for the access patterns.

## The Process

### 1️⃣ NoSQL Technology Selection
| Database | Type | Best For |
|---|---|---|
| MongoDB | Document | Flexible schemas, nested data |
| Redis | Key-Value | Caching, sessions, pub/sub |
| DynamoDB | Key-Value + Document | Serverless, high-scale AWS |
| Cassandra | Wide-Column | Time-series, high-write |
| Neo4j | Graph | Relationships, social graphs |
| Elasticsearch | Search Engine | Full-text search, analytics |

**Rule:** Design for access patterns first, not normalization.

### 2️⃣ MongoDB Schema Design
```javascript
// ✅ Embed when: data is queried together, bounded size
// Reference when: data grows unbounded or shared across entities

// Embedded (good for blog post with comments < 100)
{
  _id: ObjectId("..."),
  title: "My Post",
  content: "...",
  author: {          // Embedded author snapshot
    id: "user123",
    name: "John Doe",
    avatar: "..."
  },
  tags: ["laravel", "php"],
  comments: [        // ⚠️ Only embed if bounded
    { author: "Jane", text: "Great post!", createdAt: ISODate("...") }
  ],
  stats: { views: 1500, likes: 42 },
  createdAt: ISODate("2026-07-10")
}

// Aggregation pipeline
db.orders.aggregate([
  { $match: { status: "completed", createdAt: { $gte: new Date("2026-01-01") } } },
  { $group: { _id: "$userId", total: { $sum: "$amount" }, count: { $sum: 1 } } },
  { $sort: { total: -1 } },
  { $limit: 10 }
]);
```

### 3️⃣ DynamoDB Single-Table Design
```javascript
// Single table with composite keys for multiple entity types
// PK = partition key, SK = sort key

// User entity
{ PK: "USER#123", SK: "PROFILE", name: "John", email: "john@example.com" }

// User's orders (sorted by date)
{ PK: "USER#123", SK: "ORDER#2026-07-10#ABC", total: 99.99, status: "shipped" }

// Order lookup by ID (GSI)
{ PK: "ORDER#ABC", SK: "DETAILS", userId: "123", createdAt: "2026-07-10" }

// Query all orders for user, sorted by date
const response = await dynamodb.query({
  TableName: 'AppTable',
  KeyConditionExpression: 'PK = :pk AND begins_with(SK, :prefix)',
  ExpressionAttributeValues: { ':pk': 'USER#123', ':prefix': 'ORDER#' },
}).promise();
```

### 4️⃣ Indexing in NoSQL
```javascript
// MongoDB: Create indexes for all query patterns
db.posts.createIndex({ status: 1, publishedAt: -1 });  // Compound
db.posts.createIndex({ tags: 1 });                       // Multikey (arrays)
db.posts.createIndex({ title: "text", body: "text" });  // Text search
db.users.createIndex({ email: 1 }, { unique: true });   // Unique

// DynamoDB: GSI (Global Secondary Index)
{
  TableName: 'Posts',
  GlobalSecondaryIndexes: [{
    IndexName: 'ByStatus',
    KeySchema: [
      { AttributeName: 'status', KeyType: 'HASH' },
      { AttributeName: 'publishedAt', KeyType: 'RANGE' },
    ],
  }]
}
```

### 5️⃣ Data Consistency Patterns
- **Eventual consistency**: MongoDB with replica sets (default reads)
- **Strong consistency**: DynamoDB with `ConsistentRead: true`
- **Saga pattern**: Distributed transactions across NoSQL stores
- **Outbox pattern**: Ensure event delivery without distributed transactions

## Outputs
1. Technology selection recommendation with justification
2. Schema/data model design
3. Index strategy for all access patterns
4. Query examples for common operations
5. Consistency model and trade-off analysis
