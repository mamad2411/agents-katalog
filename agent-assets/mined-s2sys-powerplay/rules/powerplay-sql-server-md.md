---
name: sql-server
description: SQL Server and T-SQL standards (applies to **/*.sql files)
globs: ["**/*.sql"]
alwaysApply: false
---

# SQL Server / T-SQL Standards

Applied to all `.sql` files. Enforces SQL Server 2022 best practices.

## Every Stored Procedure

**TEMPLATE**:
```sql
CREATE PROCEDURE usp_GetUserById
  @UserId INT
AS
BEGIN
  SET NOCOUNT ON;

  BEGIN TRY
    -- Your logic here
    SELECT UserId, Email, FirstName, LastName, CreatedDate
    FROM Users WITH (NOLOCK)
    WHERE UserId = @UserId;
  END TRY
  BEGIN CATCH
    -- Error handling
    DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
    RAISERROR (@ErrorMessage, 16, 1);
  END CATCH
END;
```

**ALWAYS**:
- `SET NOCOUNT ON` as first statement
- `BEGIN TRY / BEGIN CATCH` error handling
- Parameterised queries (use `@Parameter`)
- `WITH (NOLOCK)` on read-heavy SELECTs
- Meaningful error messages in CATCH block

**NEVER**:
- String concatenation in SQL
- Dynamic SQL without parameters
- Missing error handling
- Procedures without NOCOUNT

## Queries

### SELECT

**ALWAYS**:
- List columns explicitly (no `SELECT *`)
- Include `WITH (NOLOCK)` for reporting queries
- SARGable WHERE clauses (no functions wrapping columns)
- Use JOINs over subqueries when possible

**BAD** ❌:
```sql
SELECT * FROM Users WHERE YEAR(CreatedDate) = 2024;
-- Problem: Function on column prevents index usage
```

**GOOD** ✅:
```sql
SELECT UserId, Email, FirstName, LastName, CreatedDate
FROM Users WITH (NOLOCK)
WHERE CreatedDate >= '2024-01-01' AND CreatedDate < '2025-01-01';
-- Solution: Range condition is SARGable, uses index
```

### Joins

**ALWAYS**:
- Use explicit JOIN syntax (not comma-separated tables)
- Specify ON conditions clearly
- Consider JOIN order (small dimension tables first)

**Example**:
```sql
SELECT
  u.UserId,
  u.Email,
  r.RoleName
FROM Users u
INNER JOIN UserRoles ur ON u.UserId = ur.UserId
INNER JOIN Roles r ON ur.RoleId = r.RoleId
WHERE u.IsActive = 1;
```

### Subqueries vs CTEs vs Temp Tables

| When | What | Example |
|------|------|---------|
| < 1000 rows | CTE | `WITH cte AS (SELECT ...) SELECT * FROM cte` |
| 1000-10k rows | CTE or indexed temp | `CREATE TABLE #temp ... INSERT ... SELECT FROM #temp` |
| > 10k rows | Indexed temp | `CREATE TABLE #large ... CREATE INDEX on #large ... SELECT` |

**Example — Large Dataset**:
```sql
-- Create temp table with index
CREATE TABLE #ActiveUsers (
  UserId INT PRIMARY KEY,
  Email NVARCHAR(100),
  CreatedDate DATETIME
);

INSERT INTO #ActiveUsers
SELECT UserId, Email, CreatedDate
FROM Users
WHERE IsActive = 1;

-- Now query with benefit of index
SELECT u.UserId, u.Email, COUNT(o.OrderId) as OrderCount
FROM #ActiveUsers u
LEFT JOIN Orders o ON u.UserId = o.UserId
GROUP BY u.UserId, u.Email
HAVING COUNT(o.OrderId) > 10;

DROP TABLE #ActiveUsers;
```

## Performance

### Indexes

**ALWAYS**:
- Create indexes for frequently searched columns
- Consider composite indexes for common WHERE + JOIN combinations
- Include covering columns to avoid lookups

**Example**:
```sql
-- Before: full table scan on every WHERE Email = ...
CREATE NONCLUSTERED INDEX ix_Users_Email
  ON Users(Email)
  INCLUDE (FirstName, LastName);  -- Covering columns
```

### Avoid These

**NEVER**:
```sql
-- ❌ Function on column — blocks index usage
WHERE YEAR(CreatedDate) = 2024
WHERE CONVERT(NVARCHAR, Amount) = '100.00'
WHERE UPPER(Email) = 'TEST@EXAMPLE.COM'

-- ✅ Alternative — SARGable
WHERE CreatedDate >= '2024-01-01' AND CreatedDate < '2025-01-01'
WHERE Amount = 100.00
WHERE Email = 'test@example.com'  -- COLLATE not required
```

### N+1 Prevention

**NEVER** ❌:
```sql
-- N+1 query pattern
DECLARE CURSOR cur FOR SELECT UserId FROM Users;
OPEN cur;
FETCH NEXT FROM cur INTO @UserId;
WHILE @@FETCH_STATUS = 0
BEGIN
  SELECT * FROM Orders WHERE UserId = @UserId;
  FETCH NEXT FROM cur INTO @UserId;
END;
```

**ALWAYS** ✅:
```sql
-- Single query with JOIN
SELECT u.UserId, u.Email, COUNT(o.OrderId) as OrderCount
FROM Users u
LEFT JOIN Orders o ON u.UserId = o.UserId
GROUP BY u.UserId, u.Email;
```

## Naming Conventions

| What | Convention | Example |
|------|-----------|---------|
| Stored Procedures | `usp_FeatureName` | `usp_GetUserById` |
| Views | `vw_FeatureName` | `vw_ActiveUsers` |
| Tables | PascalCase | `Users`, `Orders` |
| Columns | PascalCase | `UserId`, `CreatedDate` |
| Indexes | `ix_TableColumn` | `ix_Users_Email` |
| Foreign Keys | `fk_TableColumn` | `fk_Orders_UserId` |

## Transactions

**WHEN TO USE**:
- Multi-step operations that must succeed together
- Updates + inserts that depend on each other

**Example**:
```sql
BEGIN TRANSACTION;

BEGIN TRY
  INSERT INTO Orders (UserId, OrderDate, Total) VALUES (@UserId, GETDATE(), @Total);
  DECLARE @OrderId INT = SCOPE_IDENTITY();

  INSERT INTO OrderItems (OrderId, ProductId, Quantity)
  SELECT @OrderId, ProductId, Quantity FROM @ItemsTVP;

  COMMIT TRANSACTION;
END TRY
BEGIN CATCH
  ROLLBACK TRANSACTION;
  THROW;
END CATCH
```

**ALWAYS**:
- Keep transactions short
- Commit only when all steps succeed
- Use explicit BEGIN/COMMIT/ROLLBACK

## Data Types

**GUIDANCE**:
- Use appropriate sizes (not NVARCHAR(MAX) for emails)
- Use correct temporal types (DATE, DATETIME, DATETIME2)
- Use BIGINT for IDs that might exceed 2 billion

| Use | Type | Example |
|-----|------|---------|
| IDs | BIGINT or INT | `UserId BIGINT PRIMARY KEY` |
| Emails | NVARCHAR(100) | `Email NVARCHAR(100) NOT NULL` |
| Names | NVARCHAR(50) | `FirstName NVARCHAR(50)` |
| Dates | DATETIME2 | `CreatedDate DATETIME2 DEFAULT GETDATE()` |
| Booleans | BIT | `IsActive BIT DEFAULT 1` |
| Money | DECIMAL(10,2) | `Amount DECIMAL(10,2)` |

## Documentation

**ALWAYS**:
- Comment complex logic
- Include example queries for views
- Document indexes (why they exist)

**Example**:
```sql
-- Purpose: Report active users by region
-- Updated: 2024-04-09
-- Performance: < 100ms on 1M rows (uses ix_Users_RegionId)
CREATE VIEW vw_ActiveUsersByRegion AS
SELECT
  r.RegionName,
  COUNT(u.UserId) as ActiveUserCount
FROM Regions r
LEFT JOIN Users u ON r.RegionId = u.RegionId
  AND u.IsActive = 1
GROUP BY r.RegionId, r.RegionName;
```

## Security

**ALWAYS**:
- Use parameterised queries (Dapper, Entity Framework)
- Avoid `EXECUTE` with dynamic SQL
- Restrict procedure permissions (GRANT EXECUTE)
- Encrypt sensitive columns (TRANSPARENT DATA ENCRYPTION)

**NEVER**:
```sql
-- ❌ SQL Injection risk
DECLARE @SQL NVARCHAR(MAX) = 'SELECT * FROM Users WHERE Email = ''' + @Email + '''';
EXECUTE sp_executesql @SQL;

-- ✅ Parameterised
DECLARE @SQL NVARCHAR(MAX) = 'SELECT * FROM Users WHERE Email = @Email';
EXECUTE sp_executesql @SQL, N'@Email NVARCHAR(100)', @Email;
```

---

**Last Updated**: 2026-04-09

