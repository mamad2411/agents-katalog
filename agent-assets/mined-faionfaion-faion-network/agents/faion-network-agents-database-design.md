# Database Design

## Summary

**One-sentence:** Design a relational schema (PostgreSQL-first) for integrity, query performance, and zero-downtime migrations.

**One-paragraph:** Models the domain into 3NF tables (denormalize only with documented justification), declares every FK + check constraint at DB layer (not app), creates indexes only after observing query plans, and treats every schema change as an additive expand-then-contract migration so deploys are reversible. Output is a schema spec + ERD + migration plan that reviewers can validate against acceptance criteria.

**Ефективно для:**

- New service designs with non-trivial relational data.
- Schema reviews before code lands to prevent integrity bugs at the DB edge.
- Migration planning for live systems where downtime windows are scarce.
- Bringing junior developers to schema-quality parity.

## Applies If (ALL must hold)

- Service has multi-table relational data (>=3 entities with FKs).
- Persistence is PostgreSQL or another transactional RDBMS.
- Schema changes need to ship without downtime (live customers).
- Reads and writes both matter (not write-only event store).

## Skip If (ANY kills it)

- Storage is purely key-value or document (DynamoDB, MongoDB without joins) — different patterns.
- Data is throw-away (test fixtures, ETL staging) where integrity is not enforced.
- Table is single-row config (use file or env var).
- OLAP / data-warehouse modelling (star schema needs warehouse-specific methodology).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain entity list + relationships | bullet list or ERD draft | product/domain |
| Expected query patterns (top 5 reads, top 5 writes) | list | tech-lead |
| Read/write QPS estimate + data volume per table | numbers | platform |
| Existing schema if migration (DDL dump) | SQL file | DB owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[sql-optimization]] | Indexing rules consume this schema. |
| [[api-versioning]] | Schema changes drive API version policy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (FK + check at DB, 3NF default, index-after-plan, additive migration, naming convention, no-business-logic-in-DB) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for schema spec artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: model → DDL → constraints → indexes → migration plan → review | 800 |
| `content/05-examples.xml` | essential | Worked example: orders + line-items schema | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `entity_modeling` | opus | Domain-to-relational mapping needs deep synthesis. |
| `constraint_authoring` | sonnet | Mechanical DDL emission once entities decided. |
| `index_plan` | sonnet | Match indexes to query patterns from prereqs. |
| `migration_plan` | opus | Expand-then-contract sequencing needs care. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.sql` | Reference PostgreSQL schema (UUIDs, constraints, indexes, soft-delete, audit trigger) |
| `templates/migration.py` | Alembic migration example: expand-contract pattern |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-database-design.py` | Validate the schema spec artefact metadata against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[sql-optimization]]
- [[api-versioning]]
- [[logging-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps storage type, change cadence, and downtime tolerance to a rule from `01-core-rules.xml`, telling the agent whether to run the full schema spec methodology or skip when preconditions fail. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/schema.sql`

```sql
-- Reference e-commerce schema: UUIDs, constraints, indexes, soft-delete, audit trigger
-- PostgreSQL 14+

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    UNIQUE(order_id, product_id)
);

-- Indexes keyed to query patterns
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
CREATE INDEX idx_orders_status_pending ON orders(created_at) WHERE status = 'pending';
CREATE INDEX idx_users_email_active ON users(email) WHERE deleted_at IS NULL;

-- Soft-delete view
CREATE VIEW active_users AS SELECT * FROM users WHERE deleted_at IS NULL;

-- Audit log
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION audit_trigger_func() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log(table_name, record_id, action, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log(table_name, record_id, action, old_data, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log(table_name, record_id, action, old_data)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD));
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

### `templates/migration.py`

```python
"""Alembic migration example: expand-contract pattern for adding NOT NULL column.

Step 1 (this migration): add as nullable
Step 2 (separate migration): backfill in batches
Step 3 (separate migration): add NOT NULL constraint

Revision ID: a1b2c3d4e5f6
Revises: 9z8y7x6w5v4u
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    # Step 1 of expand-contract: add NULLABLE — no table rewrite, no lock
    op.create_table(
        'user_preferences',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('theme', sa.String(20), default='light'),
        sa.Column('notifications_enabled', sa.Boolean(), default=True),
        sa.Column('language', sa.String(5), default='en'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_user_prefs_user', 'user_preferences', ['user_id'])

    # To add NOT NULL to existing big table — use expand-contract:
    # op.add_column('orders', sa.Column('currency', sa.String(3), nullable=True))
    # Then in a separate migration after backfill:
    # op.alter_column('orders', 'currency', nullable=False)


def downgrade():
    op.drop_index('idx_user_prefs_user', table_name='user_preferences')
    op.drop_table('user_preferences')
```
