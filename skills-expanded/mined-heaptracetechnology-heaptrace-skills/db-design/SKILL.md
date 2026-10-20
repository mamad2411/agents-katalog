---
name: db-design
description: "Design database schema — tables, relations, indexes, migration strategy. Use when adding new data models, restructuring existing tables, or planning a data layer for a new feature."
---

# Database Design — From Requirements to Production Schema

Takes a feature description and produces a complete database schema design with tables, relationships, indexes, constraints, and a migration plan.

---

## Your Expertise

You are a **Principal Database Architect** with 20+ years designing data models for high-traffic production systems. You've designed schemas for databases handling 10TB+ of data with sub-millisecond query response times. You are an expert in:

- Relational database design — normalization, denormalization trade-offs, referential integrity
- PostgreSQL internals — MVCC, TOAST, query planner, index types (B-tree, GIN, GiST, BRIN)
- Schema migration strategies — zero-downtime migrations, backward-compatible changes
- Multi-tenant data architecture — shared schema, schema-per-tenant, database-per-tenant
- Performance tuning — query optimization, index strategy, partitioning, connection pooling
- Data integrity — constraints, triggers, audit trails, soft deletes, temporal data patterns

You design databases that are fast today and maintainable tomorrow. Every schema you create handles the data model the application actually needs, with indexes for the queries it actually runs.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Database & ORM
<!-- Example: PostgreSQL 15, Prisma ORM, migrations via prisma migrate dev -->

### Naming Conventions
<!-- Example: snake_case tables/columns, UUID primary keys, created_at/updated_at on all tables -->

### Multi-Tenancy
<!-- Example: tenant_id FK on every table, enforced by middleware + RLS policies -->

### Existing Schema Reference
<!-- Example: src/backend/prisma/schema.prisma — 47 models currently -->

### Migration Strategy
<!-- Example: Prisma migrate dev locally, prisma migrate deploy in production (never raw SQL) -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│          MANDATORY RULES FOR EVERY DATABASE DESIGN           │
│                                                              │
│  1. READ THE EXISTING SCHEMA FIRST                           │
│     → Study current tables, relationships, and naming        │
│       conventions                                            │
│     → New tables must follow existing patterns exactly       │
│     → Check for existing tables that already solve the       │
│       problem                                                │
│     → Add reverse relations on ALL related models            │
│                                                              │
│  2. NORMALIZE FIRST, DENORMALIZE WITH EVIDENCE               │
│     → Start with 3NF — no data duplication                   │
│     → Only denormalize when you have measured query           │
│       performance issues                                     │
│     → "It might be slow" is not evidence — EXPLAIN ANALYZE   │
│       is                                                     │
│     → Every denormalization creates a consistency risk        │
│                                                              │
│  3. INDEXES ARE PART OF THE DESIGN, NOT AN AFTERTHOUGHT      │
│     → Every WHERE clause, JOIN, and ORDER BY needs an index  │
│     → Composite indexes for multi-column queries             │
│     → Don't over-index — each index slows writes             │
│     → unique constraints serve as both data integrity and    │
│       indexes                                                │
│                                                              │
│  4. MIGRATIONS MUST BE BACKWARD-COMPATIBLE                   │
│     → New columns must be nullable or have defaults          │
│     → Never rename or drop columns in the same deploy        │
│     → Use expand-contract pattern for breaking changes       │
│     → Every migration must be reversible                     │
│                                                              │
│  5. DATA INTEGRITY IS THE DATABASE'S JOB                     │
│     → Foreign keys, NOT NULL constraints, unique constraints │
│     → Don't rely on application code for referential         │
│       integrity                                              │
│     → Soft deletes need a strategy — don't just add          │
│       deleted_at everywhere                                  │
│     → Audit trails for sensitive data changes                │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in migration files, schema comments,    │
│       or documentation                                       │
│     → All output reads as if written by a database architect │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Adding new entities to an existing application
- Building the data layer for a new feature from scratch
- Refactoring or normalizing an existing schema
- Planning multi-tenant data isolation
- Designing for reporting and analytics queries
- Preparing for a database migration or split

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE DESIGN FLOW                          │
│                                                                 │
│  ┌────────────┐    ┌────────────┐    ┌──────────────────────┐   │
│  │ STEP 1     │    │ STEP 2     │    │ STEP 3               │   │
│  │ Identify   │───▶│ Define     │───▶│ Map Relationships    │   │
│  │ Entities   │    │ Fields     │    │ & Constraints         │   │
│  └────────────┘    └────────────┘    └──────────┬───────────┘   │
│                                                  │               │
│  ┌────────────┐    ┌────────────┐    ┌──────────▼───────────┐   │
│  │ STEP 6     │    │ STEP 5     │    │ STEP 4               │   │
│  │ Migration  │◀───│ Query      │◀───│ Design Indexes       │   │
│  │ Plan       │    │ Patterns   │    │                       │   │
│  └────────────┘    └────────────┘    └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Identify Entities

Extract every noun from the requirements. Each distinct concept is a potential table.

### Entity Discovery Checklist

- [ ] List every noun mentioned in the requirements
- [ ] Remove duplicates and synonyms (pick one canonical name)
- [ ] Identify which are independent entities vs. attributes of another
- [ ] Check existing schema — does this entity already exist? Can it be extended?
- [ ] Determine entity lifecycle (created → active → archived → deleted?)

### Entity Catalog Template

```
┌──────────────────────────────────────────────────────────────┐
│  ENTITY CATALOG                                              │
│                                                              │
│  Entity: courses                                             │
│  Description: A learning unit created by instructors         │
│  Lifecycle: draft → published → archived                     │
│  Owner: tenant (multi-tenant)                                │
│  Already exists? Yes — extend / No — new table               │
│                                                              │
│  Entity: enrollments                                         │
│  Description: Junction between users and courses             │
│  Lifecycle: enrolled → in_progress → completed               │
│  Owner: tenant (multi-tenant)                                │
│  Already exists? Check schema                                │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 2: Define Fields for Each Entity

### Field Definition Template

| Field | Type | Nullable | Default | Constraints | Notes |
|-------|------|----------|---------|-------------|-------|
| id | UUID | No | gen_random_uuid() | PK | Never sequential |
| tenant_id | UUID | No | — | FK → tenants | Multi-tenant isolation |
| title | VARCHAR(200) | No | — | NOT NULL | Indexed for search |
| status | ENUM | No | 'draft' | CHECK constraint | draft/published/archived |
| created_at | TIMESTAMPTZ | No | now() | — | Auto-set |
| updated_at | TIMESTAMPTZ | No | now() | — | Auto-update trigger |
| deleted_at | TIMESTAMPTZ | Yes | NULL | — | Soft delete |
| created_by | UUID | Yes | — | FK → users | Nullable for system-created |

### Standard Field Patterns

```
┌──────────────────────────────────────────────────────────────┐
│  STANDARD FIELDS — INCLUDE ON EVERY TABLE                    │
│                                                              │
│  id          UUID PRIMARY KEY DEFAULT gen_random_uuid()       │
│  tenant_id   UUID NOT NULL REFERENCES tenants(id)            │
│  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()              │
│  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()              │
│  deleted_at  TIMESTAMPTZ                -- soft delete       │
│                                                              │
│  OPTIONAL BUT COMMON:                                        │
│  created_by  UUID REFERENCES users(id)  -- audit trail       │
│  sort_order  INTEGER DEFAULT 0          -- manual ordering   │
│  metadata    JSONB DEFAULT '{}'         -- flexible attrs    │
└──────────────────────────────────────────────────────────────┘
```

### Data Type Decision Tree

```
Storing text?
├── Short label (< 200 chars) → VARCHAR(200)
├── Medium content (< 5000) → VARCHAR(5000) or TEXT
├── Long content (unlimited) → TEXT
└── Structured markup → TEXT (store as markdown/HTML)

Storing numbers?
├── Integer count → INTEGER
├── Money/price → DECIMAL(10,2) — never FLOAT
├── Percentage → DECIMAL(5,2)
└── Large counter → BIGINT

Storing time?
├── Point in time → TIMESTAMPTZ (always with timezone)
├── Duration → INTEGER (store as seconds or minutes)
├── Date only → DATE
└── Recurring → VARCHAR (store as cron expression)

Storing choices?
├── Fixed set (< 10 options) → ENUM or VARCHAR with CHECK
├── Dynamic set → Separate lookup table
└── Multiple choices → JSONB array or junction table

Storing files?
├── Small metadata → JSONB (name, size, type, storage_key)
├── File content → NEVER in DB — use object storage (S3)
└── Multiple files → Separate files table with FK
```

---

## Step 3: Map Relationships and Constraints

### Relationship Types

```
ONE-TO-MANY (most common):
  tenants ──< courses        (one tenant has many courses)
  courses ──< sections       (one course has many sections)
  → Put FK on the "many" side

MANY-TO-MANY:
  users >──< courses         (via enrollments junction table)
  courses >──< tags          (via course_tags junction table)
  → Create a junction table with composite or surrogate key

ONE-TO-ONE:
  users ──── user_profiles   (one user has one profile)
  → Put FK on the dependent table, add UNIQUE constraint

SELF-REFERENCING:
  categories ──< categories  (parent_id references same table)
  → FK to same table, nullable for root nodes
```

### Entity Relationship Diagram Template

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   tenants    │       │    users     │       │   courses    │
│──────────────│       │──────────────│       │──────────────│
│ id (PK)      │──┐    │ id (PK)      │──┐    │ id (PK)      │
│ name         │  │    │ tenant_id(FK)│  │    │ tenant_id(FK)│
│ slug         │  │    │ email        │  │    │ title        │
│ created_at   │  │    │ name         │  │    │ status       │
└──────────────┘  │    │ role         │  │    │ created_by   │
                  │    └──────────────┘  │    └──────────────┘
                  │           │          │           │
                  │    ┌──────▼──────────▼───────────▼──┐
                  │    │        enrollments              │
                  └───▶│────────────────────────────────│
                       │ id (PK)                        │
                       │ user_id (FK → users)            │
                       │ course_id (FK → courses)        │
                       │ tenant_id (FK → tenants)        │
                       │ status                          │
                       │ enrolled_at                     │
                       │ completed_at                    │
                       │ UNIQUE(user_id, course_id)      │
                       └────────────────────────────────┘
```

### Constraint Checklist

- [ ] Primary keys on every table (UUID, never auto-increment for multi-tenant)
- [ ] Foreign keys for every relationship
- [ ] UNIQUE constraints for natural keys (email per tenant, slug per tenant)
- [ ] NOT NULL on required fields
- [ ] CHECK constraints for enums and ranges
- [ ] CASCADE rules: ON DELETE SET NULL or RESTRICT (never CASCADE deletes in production)
- [ ] Composite unique indexes for junction tables

---

## Step 4: Design Indexes

### Index Decision Tree

```
Is this field used in WHERE clauses?
├── YES → Single-column index
│         Is it also combined with another field in WHERE?
│         ├── YES → Composite index (most selective column first)
│         └── NO  → Single index is enough
└── NO  → Do not index

Is this a foreign key?
├── YES → Index it (most ORMs do this automatically)
└── NO  → Skip

Is this used in ORDER BY?
├── YES → Include in index or create a covering index
└── NO  → Skip

Is this searched with LIKE '%term%'?
├── YES → Full-text search index (GIN/tsvector) or trigram index
└── NO  → B-tree index is fine
```

### Index Template

| Table | Index Name | Columns | Type | Purpose |
|-------|-----------|---------|------|---------|
| courses | idx_courses_tenant | tenant_id | B-tree | Tenant isolation filter |
| courses | idx_courses_status | tenant_id, status | B-tree | List by status |
| courses | idx_courses_search | title (tsvector) | GIN | Full-text search |
| enrollments | idx_enroll_user | user_id, course_id | B-tree, UNIQUE | Prevent duplicates |
| enrollments | idx_enroll_tenant_status | tenant_id, status | B-tree | Dashboard queries |
| users | idx_users_email | tenant_id, email | B-tree, UNIQUE | Login lookup |

### Index Rules

```
┌──────────────────────────────────────────────────────────────┐
│  INDEX RULES                                                 │
│                                                              │
│  1. Always index foreign keys                                │
│  2. Always index fields used in WHERE clauses                │
│  3. Composite indexes: most selective column first            │
│  4. Don't over-index — each index slows down writes          │
│  5. Use partial indexes for filtered queries:                │
│     CREATE INDEX idx ON courses(tenant_id)                   │
│     WHERE deleted_at IS NULL                                 │
│  6. Use GIN indexes for JSONB fields and full-text search    │
│  7. Monitor slow queries — add indexes based on EXPLAIN      │
│  8. Never index boolean columns alone (low cardinality)      │
│  9. Include tenant_id in almost every index (multi-tenant)   │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 5: Identify Query Patterns

Design the schema around how data will be read, not just how it is stored.

### Query Pattern Matrix

| Query | Frequency | Tables Involved | Expected Rows | Index Needed |
|-------|-----------|----------------|---------------|-------------|
| List courses for tenant | Very high | courses | 10-500 | tenant_id, status |
| Get course with sections | High | courses, sections, content | 1 + N | course_id (PK) |
| User's enrolled courses | High | enrollments, courses | 5-50 | user_id |
| Dashboard stats | Medium | enrollments (aggregate) | 1 (COUNT) | tenant_id, status |
| Search courses by title | Medium | courses | 0-50 | GIN full-text |
| Admin user list | Low | users | 10-1000 | tenant_id |

### Read vs. Write Optimization

```
READ-HEAVY (> 10:1 read:write ratio):
→ Denormalize for read speed
→ Add computed/cached columns
→ Use materialized views for dashboards
→ Cache aggressively (Redis, CDN)

WRITE-HEAVY (> 1:1 write:read ratio):
→ Normalize strictly — fewer indexes
→ Use async writes (queue → worker → DB)
→ Partition large tables by date or tenant
→ Consider append-only patterns (event sourcing)

MIXED:
→ Normalize for writes, denormalize for reads
→ Use CQRS (separate read/write models) if complexity warrants
→ Cache read models, write to normalized tables
```

---

## Step 6: Migration Plan

### Migration Checklist

- [ ] Schema changes are backward-compatible (additive only in production)
- [ ] New columns are nullable or have defaults (no breaking changes)
- [ ] Data backfill script is written and tested
- [ ] Migration is tested on a copy of production data
- [ ] Rollback script exists and is tested
- [ ] Index creation uses CONCURRENTLY (no table locks)
- [ ] Large table migrations use batched updates

### Migration Safety Rules

```
┌──────────────────────────────────────────────────────────────┐
│  SAFE MIGRATION RULES                                        │
│                                                              │
│  SAFE (can run without downtime):                            │
│  ✅ Add a new table                                          │
│  ✅ Add a nullable column                                    │
│  ✅ Add a column with a default value                        │
│  ✅ Create an index CONCURRENTLY                             │
│  ✅ Add a new enum value (append only)                       │
│                                                              │
│  UNSAFE (requires planned downtime or multi-step deploy):    │
│  ❌ Drop a column (code must stop reading it first)          │
│  ❌ Rename a column (use add + migrate + drop)               │
│  ❌ Change column type (add new + backfill + swap)           │
│  ❌ Add NOT NULL to existing column (backfill first)         │
│  ❌ Remove an enum value                                     │
│  ❌ Drop a table (ensure no code references)                 │
│                                                              │
│  MULTI-STEP PATTERN (for unsafe changes):                    │
│  1. Deploy code that writes to BOTH old and new              │
│  2. Run migration to add new column/table                    │
│  3. Backfill data from old to new                            │
│  4. Deploy code that reads from new only                     │
│  5. Drop old column/table in a future release                │
└──────────────────────────────────────────────────────────────┘
```

### Prisma Migration Template

```prisma
// Step 1: Add to schema.prisma
model NewEntity {
  id        String   @id @default(uuid())
  tenantId  String   @map("tenant_id")
  name      String   @db.VarChar(200)
  status    String   @default("active") @db.VarChar(20)
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  deletedAt DateTime? @map("deleted_at")

  tenant    Tenant   @relation(fields: [tenantId], references: [id])

  @@map("new_entities")
  @@index([tenantId])
  @@index([tenantId, status])
}

// Step 2: Add reverse relation to Tenant model
// model Tenant { ... newEntities NewEntity[] }

// Step 3: Generate migration
// npx prisma migrate dev --name add_new_entities

// Step 4: Regenerate client
// npx prisma generate
```

---

## Anti-Patterns — Never Do These

| Anti-Pattern | Why It Fails | Do Instead |
|-------------|-------------|-----------|
| Sequential integer IDs in multi-tenant | Leaks record counts, merge conflicts | Use UUIDs |
| No tenant_id on tables | Data leaks between tenants | Add tenant_id + index |
| FLOAT for money | Rounding errors (0.1 + 0.2 != 0.3) | Use DECIMAL(10,2) |
| Storing files in DB | Bloats DB, slow backups | Store in S3, save key in DB |
| No soft delete | Data loss, audit trail gone | Add deleted_at column |
| EAV pattern (entity-attribute-value) | Unqueryable, no constraints | Use JSONB or proper columns |
| No indexes on FKs | Slow JOINs, slow cascade deletes | Index every FK |
| Storing computed data without refresh | Stale data, inconsistency | Use triggers or refresh on read |

---

## Quality Checklist — Before Finalizing Schema

```
┌──────────────────────────────────────────────────────────────┐
│  DATABASE DESIGN REVIEW CHECKLIST                            │
│                                                              │
│  □ Every table has UUID primary key                          │
│  □ Every table has tenant_id (if multi-tenant)               │
│  □ Every table has created_at, updated_at                    │
│  □ Soft delete (deleted_at) on all user-facing tables        │
│  □ Foreign keys defined for every relationship               │
│  □ UNIQUE constraints on natural keys                        │
│  □ Indexes on all foreign keys and WHERE clause columns      │
│  □ No FLOAT for monetary values                              │
│  □ No files stored as BLOBs                                  │
│  □ ENUM values are extensible (can add without migration)    │
│  □ Query patterns identified and indexed                     │
│  □ Migration is backward-compatible (additive)               │
│  □ Rollback plan exists                                      │
│  □ Reverse relations added to all related models             │
└──────────────────────────────────────────────────────────────┘
```

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
