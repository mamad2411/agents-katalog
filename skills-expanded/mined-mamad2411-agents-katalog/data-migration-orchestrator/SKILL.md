---
name: "Data Migration Orchestrator"
version: "1.0.0"
description: "Orchestrates complex data migrations between systems with validation, rollback, and progress tracking."
author: "workspace"
activated: false
---

# Data Migration Orchestrator

Orchestrates complex data migrations between systems with validation, rollback, and progress tracking.

## Decision Framework

### When to Apply
Use when: Moving data between databases, ETL processes, system upgrades, data transformations

### When NOT to Apply
Don't use when: Simple schema changes (use migrations), real-time sync (use offline-sync-engine)

## Anti-Patterns

### 1. No Backup Before Migration
Always snapshot before destructive operations.

### 2. No Rollback Plan
```javascript
// BAD: Destructive with no rollback
await db.raw('DROP TABLE old_users');

// GOOD: Rename first, drop later
await db.raw('ALTER TABLE old_users RENAME TO old_users_deprecated');
// Verify migration successful, then drop in separate step
```


## Trigger Phrases

- "Migrate data"
- "ETL pipeline"
- "Data transformation"
- "System migration"
- "Data import/export"

## Patterns

### Migration Pipeline
```javascript
class MigrationPipeline {
  async execute(source, target, mapping) {
    const stats = { total: 0, migrated: 0, failed: 0, skipped: 0 };
    const batchSize = 1000;
    
    for await (const batch of source.readBatches(batchSize)) {
      const transformed = batch.map(row => mapping.transform(row));
      const validated = transformed.filter(row => {
        const errors = mapping.validate(row);
        if (errors.length) { stats.skipped++; return false; }
        return true;
      });
      
      try {
        await target.writeBatch(validated);
        stats.migrated += validated.length;
      } catch (error) {
        stats.failed += validated.length;
        await this.deadLetterQueue.add({ batch: validated, error: error.message });
      }
      stats.total += batch.length;
    }
    return stats;
  }
}
```


## Escalation Chain

1. **Retry** - Retry failed batch (3 attempts)
2. **Skip** - Skip bad records, log to dead letter queue
3. **Rollback** - Revert to pre-migration state
4. **Alert** - Notify operators of migration failure
5. **Manual** - Manual intervention required

## Error Classification

| Error Type | Strategy | Recovery |
|-----------|----------|----------|
| Constraint violation | Skip + log | Manual review |
| Connection timeout | Retry batch | Auto |
| Data type mismatch | Transform + retry | Auto |
| Disk full | Pause + alert | Manual |

## Integration
- Works with: database-schema-designer, error-recovery-orchestrator

