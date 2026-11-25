---
name: mongodb-mean
description: "MongoDB database architecture for MEAN stack apps. Use when designing collections, schemas, indexes, relationships, and data modeling with Mongoose ODM."
---

# Mongodb Mean

## Purpose

Design MongoDB database architectures for MEAN stack applications. Produce Mongoose schema definitions, index strategies, relationship patterns, and data modeling decisions that backend developers implement directly.

## Key Patterns

### Schema Design Principles
- **Embed vs Reference:** Embed data accessed together (comments in a post). Reference data accessed independently (user profiles from posts). If embedded array can grow unbounded, reference instead.
- **Schema-first with Mongoose:** Always define explicit schemas. Use Mongoose schema types, validators, and virtuals.
- **Denormalize for reads:** Duplicate frequently-read fields (e.g., author.name in posts) to avoid joins.

### Standard Mongoose Patterns
- Always include `{ timestamps: true }` — adds createdAt, updatedAt
- Soft delete pattern: `{ isDeleted: Boolean, deletedAt: Date }`
- Pagination-ready: always index on createdAt
- Enum validation: `{ role: { type: String, enum: ['user', 'admin'], default: 'user' } }`
- Reference pattern: `{ author: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true } }`

### Index Strategy
- Every query field gets an index
- Compound indexes for multi-field queries: `{ userId: 1, createdAt: -1 }`
- Unique indexes for natural keys: `{ email: 1 }` with `unique: true`
- Text indexes for search: `{ title: 'text', body: 'text' }`

### Relationship Patterns
- **One-to-Few (<=20):** Embed directly (addresses in user)
- **One-to-Many (20-1000):** Array of references (posts by user)
- **One-to-Millions:** Parent reference in child (log entries referencing server)
- **Many-to-Many:** Array of references on both sides, or junction collection

## Conventions

- Collection names: lowercase plural (users, posts, comments)
- Field names: camelCase (firstName, createdAt, isActive)
- Always include timestamps: true in every schema
- Always define toJSON transform to remove __v and convert _id to id
- Define indexes in schema file, not in application code
- Use Mongoose middleware (pre/post hooks) for cross-cutting concerns
- Validate at schema level (required, min/max, enum, match)

## Knowledge Strategy

- **Patterns to capture:** Schema designs that worked well, index strategies for common queries, relationship patterns
- **Examples to collect:** Complete schema files for common entities (User, Post, Comment, Product, Order)
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
