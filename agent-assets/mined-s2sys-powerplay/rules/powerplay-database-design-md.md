---
name: database-design
description: Database schema design standards — normalization, indexes, naming, migrations, constraints
globs: ["**/*.sql", "**/Migrations/**", "**/*Migration*.cs", "**/DbContext*.cs"]
alwaysApply: false
---

# Database Design Standards

Every database is either well-designed (fast, maintainable, consistent) or becomes a bottleneck. Establish standards early.

## Normalization & Schema Design

**ALWAYS**:
- **First Normal Form (1NF)**: No repeating groups (arrays/lists in single column)
- **Second Normal Form (2NF)**: Every non-key column depends on entire primary key
- **Third Normal Form (3NF)**: No transitive dependencies (column depends on non-key column)
- **Name tables & columns PascalCase**: `Users`, `Orders`, `FirstName`, `CreatedAt`
- **Primary keys**: Always `Id` (not `UserId`, not `user_id`)
- **Foreign keys**: `[TableName]Id` (e.g., `UserId`, `OrderId`)
- **Timestamps**: `CreatedAt` (UTC, NOT NULL, default GETUTCDATE()) and `UpdatedAt`
- **Soft delete**: Use `IsDeleted` (BIT/BOOL) + `DeletedAt` (nullable DATETIME), never hard delete

**NEVER**:
- Store arrays/JSON in single column without solid reason (violates 1NF)
- Transitive dependencies (Name stored when UserId already identifies user)
- Denormalization without a documented performance reason
- Nullable primary or foreign keys
- Hard delete production data (impossible to audit, breaks foreign keys)
- Mix data types (don't store phone numbers as strings if they're only looked up as numbers)
- Create "catch-all" tables (like `Attributes` storing arbitrary key-value pairs)

### ✅ GOOD Schema (3NF)

```sql
-- Users table (normalized)
CREATE TABLE Users (
  Id INT PRIMARY KEY IDENTITY(1,1),
  Email NVARCHAR(255) NOT NULL UNIQUE,
  FirstName NVARCHAR(100) NOT NULL,
  LastName NVARCHAR(100) NOT NULL,
  CreatedAt DATETIME NOT NULL DEFAULT GETUTCDATE(),
  UpdatedAt DATETIME NOT NULL DEFAULT GETUTCDATE(),
  IsDeleted BIT NOT NULL DEFAULT 0,
  DeletedAt DATETIME NULL
);

-- Orders table (foreign key to Users)
CREATE TABLE Orders (
  Id INT PRIMARY KEY IDENTITY(1,1),
  UserId INT NOT NULL FOREIGN KEY REFERENCES Users(Id),
  OrderDate DATETIME NOT NULL DEFAULT GETUTCDATE(),
  Total DECIMAL(10,2) NOT NULL,
  CreatedAt DATETIME NOT NULL DEFAULT GETUTCDATE(),
  UpdatedAt DATETIME NOT NULL DEFAULT GETUTCDATE(),
  IsDeleted BIT NOT NULL DEFAULT 0,
  DeletedAt DATETIME NULL
);

-- Order items (join table for many-to-many)
CREATE TABLE OrderItems (
  Id INT PRIMARY KEY IDENTITY(1,1),
  OrderId INT NOT NULL FOREIGN KEY REFERENCES Orders(Id),
  ProductId INT NOT NULL FOREIGN KEY REFERENCES Products(Id),
  Quantity INT NOT NULL,
  UnitPrice DECIMAL(10,2) NOT NULL,
  CreatedAt DATETIME NOT NULL DEFAULT GETUTCDATE()
);
```

### ❌ BAD Schema (Denormalized, Hard to maintain)

```sql
-- Bad: User data stored in Orders (redundant, update anomaly)
CREATE TABLE Orders (
  OrderId INT,
  UserId INT,
  UserName NVARCHAR(100),  -- Duplicated! Should come from Users
  UserEmail NVARCHAR(255), -- Duplicated!
  OrderDate DATETIME,
  -- When user name changes, must update all orders!
);

-- Bad: Hard delete (can't audit, breaks integrity)
DELETE FROM Orders WHERE OrderId = 123;  -- Data gone forever

-- Bad: Items as array in single column (violates 1NF)
CREATE TABLE Orders (
  OrderId INT,
  Items VARCHAR(MAX),  -- '[{id:1,qty:2},{id:3,qty:1}]' — bad!
);
```

---

## Indexes

**ALWAYS**:
- Index foreign keys (needed for JOINs, prevents full table scans)
- Index columns in WHERE clauses (filters)
- Index columns in ORDER BY (sorting)
- Index columns in JOIN conditions
- Composite indexes: most selective column first
- Consider covering indexes for read-heavy queries (include non-key columns)
- Regular maintenance: REBUILD or REORG based on fragmentation %

**NEVER**:
- Index every column (slows writes, wastes space)
- Index low-cardinality columns (sex, status with 2-3 values)
- Forget to index foreign keys (huge performance cost)
- Create duplicate indexes

### ✅ GOOD Indexes

```sql
-- Primary key (auto-indexed)
CREATE TABLE Users (
  Id INT PRIMARY KEY,
  ...
);

-- Foreign keys (always index for JOINs)
CREATE INDEX IX_Orders_UserId ON Orders(UserId);

-- WHERE clause filtering
CREATE INDEX IX_Users_Email ON Users(Email);

-- Composite index: user by email
CREATE INDEX IX_Users_Email_Active ON Users(Email, IsActive);

-- Covering index (includes columns needed for query without table scan)
CREATE INDEX IX_Orders_UserId_Include 
  ON Orders(UserId) INCLUDE (Total, CreatedAt);
```

---

## Constraints & Data Integrity

**ALWAYS**:
- Primary key on every table (no orphaned rows)
- Foreign keys for relationships (referential integrity)
- NOT NULL on required columns (data quality)
- UNIQUE constraints on unique data (email, username)
- CHECK constraints for valid values (age > 0, status IN ('active', 'inactive'))
- Default values for timestamps (CreatedAt = GETUTCDATE())

**NEVER**:
- Nullable foreign keys (indicates data design issue)
- Missing NOT NULL (creates NULL surprises in queries)
- No constraints (trust the application layer — big mistake)

### ✅ GOOD Constraints

```sql
CREATE TABLE Users (
  Id INT PRIMARY KEY,                          -- PK: No nulls, unique
  Email NVARCHAR(255) NOT NULL UNIQUE,         -- NOT NULL + UNIQUE
  FirstName NVARCHAR(100) NOT NULL,            -- NOT NULL
  Age INT NOT NULL CHECK (Age >= 0),           -- CHECK: valid value
  Status NVARCHAR(20) NOT NULL DEFAULT 'active'
    CHECK (Status IN ('active', 'inactive')),   -- CHECK: enum-like
  CreatedAt DATETIME NOT NULL DEFAULT GETUTCDATE()  -- DEFAULT
);
```

---

## Migrations & Backward Compatibility

**ALWAYS**:
- Write migrations (never manual schema changes)
- Migrations are reversible (DOWN script for every UP)
- Never destructive in production (no DROP COLUMN without backup)
- Add columns as nullable first, then backfill, then NOT NULL
- Rename columns via temporary column (old → temp, new ← temp, drop old)
- Test migrations on production-sized data
- Run migrations in transaction

**NEVER**:
- Drop table/column without backup
- Rename column directly (breaks dependent code)
- Add NOT NULL column without default
- Lock tables during migration (use minimal locking patterns)

### ✅ GOOD Migration (C# with EF Core)

```csharp
// Adding a new required column safely
public partial class AddPhoneToUsers : Migration {
  protected override void Up(MigrationBuilder migrationBuilder) {
    // Step 1: Add nullable column
    migrationBuilder.AddColumn<string>(
      name: "PhoneNumber",
      table: "Users",
      nullable: true);

    // Step 2: Backfill existing rows
    migrationBuilder.Sql(
      "UPDATE Users SET PhoneNumber = '0000000000' WHERE PhoneNumber IS NULL");

    // Step 3: Add NOT NULL constraint
    migrationBuilder.AlterColumn<string>(
      name: "PhoneNumber",
      table: "Users",
      nullable: false);
  }

  protected override void Down(MigrationBuilder migrationBuilder) {
    migrationBuilder.DropColumn(name: "PhoneNumber", table: "Users");
  }
}
```

### ❌ BAD Migration

```csharp
// Dangerous: Adds NOT NULL without default
migrationBuilder.AddColumn<string>(
  name: "PhoneNumber",
  table: "Users",
  nullable: false);  // FAILS if Users table not empty!

// Dangerous: Drops column immediately
migrationBuilder.DropColumn(name: "LegacyField", table: "Users");  // No backup!
```

---

## Soft Delete Pattern

**ALWAYS use soft delete** for production data:

```sql
-- Mark as deleted, don't remove
UPDATE Users SET IsDeleted = 1, DeletedAt = GETUTCDATE() WHERE Id = 123;

-- Query only non-deleted rows
SELECT * FROM Users WHERE IsDeleted = 0;

-- Find deleted rows (for recovery/audit)
SELECT * FROM Users WHERE IsDeleted = 1 ORDER BY DeletedAt DESC;
```

**Implementation in C#:**

```csharp
// Entity
public class User {
  public int Id { get; set; }
  public string Email { get; set; }
  public bool IsDeleted { get; set; }
  public DateTime? DeletedAt { get; set; }
}

// DbContext
protected override void OnModelCreating(ModelBuilder modelBuilder) {
  // Global filter: always exclude deleted rows
  modelBuilder.Entity<User>()
    .HasQueryFilter(u => !u.IsDeleted);
}

// Delete operation
user.IsDeleted = true;
user.DeletedAt = DateTime.UtcNow;
await db.SaveChangesAsync();
```

---

## Data Types & Precision

| Use Case | Type | NOT String |
|----------|------|-----------|
| IDs | INT / BIGINT | Never VARCHAR |
| Timestamps | DATETIME / DATETIME2 | Never INT unix time |
| Money | DECIMAL(10,2) | Never FLOAT |
| Booleans | BIT | Never 0/1 in VARCHAR |
| Email | NVARCHAR(255) | Can be VARCHAR but UTF-8 safer |
| Phone | NVARCHAR(20) | VARCHAR acceptable, consider normalization |
| JSON | NVARCHAR(MAX) | OK but defeats normalization |

---

## Query Performance Checklist

- [ ] All WHERE columns indexed
- [ ] All JOIN columns indexed  
- [ ] No N+1 query problem (1 query becomes N in loop)
- [ ] SELECT * minimized (list only needed columns)
- [ ] UNION preferred over multiple queries
- [ ] JOIN preferred over subqueries
- [ ] No functions on indexed columns in WHERE (defeats index)
- [ ] Statistics updated regularly (SQL query optimizer needs them)

---

## Database Design Checklist

- [ ] All tables have primary key (Id)
- [ ] Foreign keys defined for relationships
- [ ] Foreign keys indexed
- [ ] Required columns marked NOT NULL
- [ ] Unique data has UNIQUE constraint
- [ ] Timestamps on every table (CreatedAt, UpdatedAt)
- [ ] Soft delete columns (IsDeleted, DeletedAt)
- [ ] No hard deletes in production
- [ ] Migrations written and reversible
- [ ] No denormalization without performance justification
- [ ] Column naming consistent (PascalCase)
- [ ] Table naming consistent (PascalCase)

---

## Summary

Good database design:
1. **Normalized** (3NF) — avoids redundancy and anomalies
2. **Indexed** — WHERE/JOIN/ORDER BY columns indexed
3. **Constrained** — PK, FK, NOT NULL, UNIQUE, CHECK
4. **Soft-deleted** — IsDeleted + DeletedAt, never hard delete
5. **Migrated** — reversible, tested, documented migrations
6. **Auditable** — timestamps, soft delete history, change log

This prevents performance problems, data corruption, and audit nightmares down the line.
