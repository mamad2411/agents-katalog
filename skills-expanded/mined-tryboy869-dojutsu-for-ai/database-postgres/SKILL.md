---
name: database-postgres
description: "Apply for PostgreSQL schema design, queries, migrations, and performance. Covers: indexes, constraints, JSONB, migrations with Alembic, connection pooling, query optimization. Trigger for: database, PostgreSQL, SQL, schema, migration, query, index."
---

# DATABASE POSTGRES — Production Schema & Query Patterns

## Schema Design Principles

### Always use UUID + timestamps
```sql
CREATE TABLE jobs (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  status      TEXT NOT NULL CHECK (status IN ('pending','running','done','failed')),
  payload     JSONB NOT NULL DEFAULT '{}',
  result      JSONB,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at  TIMESTAMPTZ  -- soft delete
);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION touch_updated_at()
RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$
LANGUAGE plpgsql;
CREATE TRIGGER jobs_updated_at BEFORE UPDATE ON jobs
  FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
```

### Indexes — Index what you query
```sql
-- Partial index (only active jobs — smaller, faster)
CREATE INDEX idx_jobs_pending ON jobs (created_at)
  WHERE status = 'pending';

-- Composite index (order matches query WHERE + ORDER BY)
CREATE INDEX idx_jobs_user_status ON jobs (user_id, status, created_at DESC);

-- JSONB index for deep queries
CREATE INDEX idx_jobs_payload_type ON jobs USING GIN (payload);
```

## Query Patterns

### Paginate correctly (keyset, not OFFSET)
```sql
-- ❌ OFFSET gets slow on large tables
SELECT * FROM jobs ORDER BY created_at DESC LIMIT 20 OFFSET 10000;

-- ✅ Keyset pagination (always fast)
SELECT * FROM jobs
WHERE created_at < :last_seen_cursor
ORDER BY created_at DESC LIMIT 20;
```

### Upsert (INSERT ... ON CONFLICT)
```sql
INSERT INTO job_results (job_id, output, duration)
VALUES (:job_id, :output, :duration)
ON CONFLICT (job_id)
DO UPDATE SET
  output   = EXCLUDED.output,
  duration = EXCLUDED.duration,
  updated_at = NOW();
```

### Avoid N+1 — JOIN or prefetch
```python
# ❌ N+1 queries
jobs = await db.execute("SELECT * FROM jobs")
for job in jobs:
    user = await db.execute("SELECT * FROM users WHERE id = ?", job.user_id)

# ✅ Single join
jobs = await db.execute("""
    SELECT j.*, u.email FROM jobs j
    JOIN users u ON u.id = j.user_id
    WHERE j.status = 'done'
""")
```

## Alembic Migrations
```python
# Always reversible
def upgrade():
    op.add_column('jobs', sa.Column('priority', sa.Integer, server_default='0'))
    op.create_index('idx_jobs_priority', 'jobs', ['priority'])

def downgrade():
    op.drop_index('idx_jobs_priority')
    op.drop_column('jobs', 'priority')
```

## Connection Pooling
```python
# SQLAlchemy async — production settings
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,        # base connections
    max_overflow=20,     # extra under load
    pool_timeout=30,     # wait before error
    pool_recycle=1800,   # recycle after 30min
    echo=False,          # never True in production
)
```

## Forbidden
❌ `SELECT *` in production queries
❌ String concatenation in SQL (use params)
❌ Migrations without `downgrade()`
❌ `OFFSET` for pagination > page 10
❌ No indexes on FK columns
❌ Storing passwords in plaintext (use pgcrypto or app-side bcrypt)
