---
name: data-migrations
description: Safe database migrations — schema changes, data backups, verification, rollbacks
triggers: [migration, database schema, alter table, data cleanup, backups, production database]
---

# SKILL: Data Migrations

## The Law
```
NEVER run a migration on production without:
1. Backup tested (can restore from it)
2. Dry run on staging with production data size
3. Rollback plan documented
4. Verification query written
```

## Migration Safety Checklist

Before running ANY migration on production:

```
□ BACKUP CREATED
  - Full backup exists
  - Backup can be restored (tested it)
  - Backup is on separate storage (not same database server)
  - Backup is > 24 hours old minimum

□ TESTED ON STAGING
  - Staging has same data size as production
  - Migration runs to completion
  - Application still works after migration
  - Performance is acceptable (no 10x slowdown)

□ VERIFIED REVERSIBILITY
  - Can rollback if things go wrong?
  - Down migration exists and tested
  - Time to rollback: < 5 minutes

□ MONITORING READY
  - Alerts configured for migration impact
  - Error rate dashboard open
  - Slow query monitoring enabled

□ WINDOW SELECTED
  - Off-peak time (lowest traffic)
  - Support team on standby
  - On-call engineer available to monitor
```

## Migration Patterns

### Pattern 1: Add Optional Column (safe)
```sql
-- SAFE — doesn't affect existing code
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);
-- Application keeps working, just ignores new column
```

### Pattern 2: Add Required Column (requires 2 deploys)
```
Deploy 1 (Friday):
  - Code: app handles phone_number being null OR present
  - Migration: ALTER TABLE users ADD COLUMN phone_number VARCHAR(20) DEFAULT '';
  - Result: Code is compatible, column populated with defaults

Deploy 2 (next Monday, after no errors for 72 hours):
  - Code: app now requires phone_number (not null)
  - Migration: UPDATE users SET phone_number='unknown' WHERE phone_number='';
              ALTER TABLE users MODIFY phone_number NOT NULL;
  - Result: All users have phone_number, code enforces it
```

### Pattern 3: Rename Column (requires 2 deploys)
```
Deploy 1:
  - Code: read from BOTH old and new column names
  - Migration: ALTER TABLE users ADD COLUMN first_name VARCHAR(100);
              UPDATE users SET first_name = name;
  - Result: Both name and first_name have same data

Deploy 2 (after 72 hours, no errors):
  - Code: only read from first_name, ignore name
  - Migration: ALTER TABLE users DROP COLUMN name;
  - Result: Column renamed safely
```

## Backup & Restore

```bash
# CREATE BACKUP (hourly, automated)
# PostgreSQL
pg_dump -U postgres -d production > production_$(date +%Y%m%d_%H%M%S).sql

# Verify backup works (critical!)
createdb test_restore
psql -d test_restore < production_20240115_143000.sql
# Should complete without errors

# RESTORE from backup (if migration fails)
psql -d production < production_20240115_143000.sql
# Application should work immediately
```

## Migration Script Template

```python
# alembic/versions/[timestamp]_add_phone_number.py
"""Add phone_number column to users

Revision ID: abc123
Previous Revision: def456
"""

from alembic import op
import sqlalchemy as sa

revision = "abc123"
down_revision = "def456"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add column
    op.add_column('users', sa.Column('phone_number', sa.String(20), nullable=True))
    
    # Create index if frequently queried
    op.create_index('idx_users_phone', 'users', ['phone_number'])

def downgrade() -> None:
    # Reverse the migration
    op.drop_index('idx_users_phone')
    op.drop_column('users', 'phone_number')
```

## Verification

After migration, verify:
```python
# Check: all rows have data
SELECT COUNT(*) as total,
       COUNT(phone_number) as with_phone
FROM users;
-- Should show: all rows now have phone_number

# Check: no errors in logs
SELECT COUNT(*) as error_count
FROM logs
WHERE level = 'ERROR'
  AND timestamp > (NOW() - INTERVAL '5 minutes');
-- Should show: 0 errors

# Check: performance
SELECT AVG(duration_ms) as avg_query_time
FROM query_logs
WHERE query_type = 'select'
  AND timestamp > (NOW() - INTERVAL '5 minutes');
-- Should show: normal query times (< 100ms)
```

## Quality checks
- [ ] Backup created and verified before migration
- [ ] Migration tested on staging with production data volume
- [ ] Rollback procedure documented and tested
- [ ] Verification queries written
- [ ] Migration runs in off-peak window
- [ ] Team on standby during migration
- [ ] Verification queries run after migration completes
- [ ] No errors in production logs post-migration
