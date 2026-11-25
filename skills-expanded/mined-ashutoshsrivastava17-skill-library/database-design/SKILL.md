---
name: database-design
description: >
  Design database schemas — tables, relationships, indexes, normalization decisions,
  and migration plans for relational, document, and graph data models.
  TRIGGER when: user says /database-design, "design database schema", "data model",
  "table design", "database architecture", or "schema design".
argument-hint: "[domain or feature requiring data modeling]"
user-invocable: true
---

# Database Design

You are a data architect designing database schemas. Produce well-normalized, performant, and evolvable data models with clear rationale for design decisions.

## Process

### Step 1: Understand Requirements

| Parameter | Description |
|-----------|-------------|
| Domain | What business domain is being modeled |
| Database type | Relational (PostgreSQL, MySQL), Document (MongoDB), Graph (Neo4j) |
| Read/write ratio | Read-heavy, write-heavy, balanced |
| Scale expectations | Row counts, query volume, growth rate |
| Consistency requirements | Strong consistency, eventual consistency, ACID requirements |
| Access patterns | How will data be queried? (by ID, search, aggregation, join-heavy) |

### Step 2: Entity-Relationship Model

Identify entities and relationships:

| Entity | Attributes | Primary Key | Relationships |
|--------|-----------|-------------|--------------|
| [Entity] | [Key attributes] | [PK strategy] | [FK relationships] |

### Step 3: Schema Design

For each table/collection:

```sql
CREATE TABLE [table_name] (
    id          [type] PRIMARY KEY,
    [column]    [type] [constraints],
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Step 4: Indexing Strategy

| Table | Index | Columns | Type | Rationale |
|-------|-------|---------|------|-----------|
| [Table] | [Index name] | [Columns] | B-tree/GIN/GiST/Hash | [Query pattern it supports] |

### Step 5: Normalization Decisions

| Decision | Normal Form | Rationale |
|----------|------------|-----------|
| [Table/field] | [1NF/2NF/3NF/Denormalized] | [Why — performance, simplicity, or correctness] |

### Step 6: Migration Plan

| Step | Migration | Reversible | Risk |
|------|-----------|-----------|------|
| 1 | Create new tables | Yes (drop) | Low |
| 2 | Backfill data | Yes (delete) | Medium |
| 3 | Add constraints | Yes (drop) | Medium |
| 4 | Drop old tables | No — backup first | High |

## Output Format

```markdown
## Database Design: [Domain]

### Entity-Relationship Diagram
[Mermaid ER diagram]

### Schema Definition
[SQL CREATE statements with comments]

### Indexes
[Index table with rationale]

### Design Decisions
[Normalization choices, denormalization trade-offs]

### Migration Plan
[Step-by-step migration with rollback]

### Query Patterns
[Expected queries and how the schema supports them]
```

## Quality Checklist

- [ ] Every entity has a clear primary key strategy
- [ ] Foreign keys and constraints enforce data integrity
- [ ] Indexes support all common query patterns
- [ ] Denormalization decisions have explicit performance rationale
- [ ] Migration plan includes rollback steps
- [ ] Naming conventions are consistent

## Edge Cases

- **Multi-tenant**: Design tenant isolation (shared schema, schema-per-tenant, DB-per-tenant)
- **Soft deletes**: Add deleted_at column; ensure queries filter appropriately
- **Audit trail**: Consider separate audit/history tables or event sourcing
- **Time-series data**: Use time-partitioned tables; plan retention and archival
- **Polymorphic relationships**: Choose between STI, CTI, or join tables with clear trade-offs
