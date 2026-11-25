---
name: database-integration-testing-qualityforge
description: Routes database integration testing tasks to the testing specialist for QualityForge AI.
company: qualityforge-ai
---

# Database Integration Testing Specialist

## Overview
This skill routes database integration testing tasks to the dedicated testing specialist for QualityForge AI. It covers end-to-end testing of database operations, migrations, and cross-database scenarios.

## Routing Criteria

Route to this skill when:
- Database integration testing for CRUD operations
- Cross-database migration testing
- Schema migration verification testing
- Transaction and rollback testing
- Data integrity and constraint testing
- Performance testing with real database loads
- Connection pooling and concurrency testing
- Backup and restore testing

## Capabilities

### Integration Testing
- End-to-end CRUD operation testing
- Transaction commit/rollback testing
- Concurrency and race condition testing
- Multi-table relationship testing
- Foreign key and constraint validation

### Migration Testing
- Schema migration verification
- Data migration validation
- Downgrade/rollback migration testing
- Migration idempotency verification

### Cross-Database Testing
- Multi-database query testing
- Distributed transaction testing
- Data synchronization testing
- Cross-database integrity validation

### Performance Testing
- Load testing with realistic data volumes
- Query performance benchmarking
- Connection pool stress testing
- Concurrent operation testing

### Data Integrity Testing
- Referential integrity validation
- Data type and constraint testing
- Null handling and edge cases
- Unicode and character encoding tests

## Related Skills

- `accessibility-Accessibility-testing` - UI accessibility testing
- `simulator-qualityforge-workflow-simulation` - Workflow simulation
- `database-infraforge-database-infrastructure` - Database infrastructure

## Testing Tools & Frameworks

```typescript
// Example: Database integration test setup
describe('User Repository Integration Tests', () => {
  beforeEach(async () => {
    await testDb.reset();
    await seedTestData();
  });

  it('should create user with valid data', async () => {
    const user = await userRepo.create({
      email: 'test@example.com',
      name: 'Test User'
    });
    expect(user.id).toBeDefined();
  });

  it('should enforce unique email constraint', async () => {
    await userRepo.create({ email: 'test@example.com' });
    await expect(
      userRepo.create({ email: 'test@example.com' })
    ).rejects.toThrow('unique constraint');
  });
});
```

---

*This skill routes to the database integration testing specialist agent.*