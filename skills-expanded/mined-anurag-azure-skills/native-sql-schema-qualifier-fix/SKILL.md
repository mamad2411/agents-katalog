---
name: "native-sql-schema-qualifier-fix"
description: "Add explicit schema qualifiers to native SQL queries in Spring Data JPA repositories to prevent production failures in multi-schema PostgreSQL environments"
version: 3
created: "2026-06-10"
updated: "2026-06-26"
---
## When to Use
Use when code review or static analysis detects native SQL queries (@Query with nativeQuery=true) that lack explicit schema qualifiers. Critical for multi-tenant applications, schema-per-domain architectures, or any PostgreSQL database using multiple schemas. Run this before production deployment to prevent "relation does not exist" errors.

## Procedure
## Procedure

### Step 1: Identify Native SQL Queries

```bash
# Find all native queries in repository layer
grep -r "@Query.*nativeQuery.*=.*true" --include="*Repository*.java" src/

# Or use more specific pattern
find . -name "*Repository*.java" -exec grep -l "nativeQuery" {} \;
```

**Expected Output:**
- List of repository files with native SQL
- Count: Typically 1-5 files in domain microservices
- Review each file individually

---

### Step 2: Analyze Table References

**Pattern Recognition:**
```sql
-- Tables appear in these SQL clauses:
FROM table_name
JOIN table_name
LEFT JOIN table_name
INNER JOIN table_name
UPDATE table_name
DELETE FROM table_name
INSERT INTO table_name

-- Also check CTEs (Common Table Expressions):
WITH cte_name AS (
    SELECT ... FROM table_name  -- ⚠️ Needs schema qualifier
)
```

**Example from Real Code (IssueGridNativeRepository.java):**
```java
@Query(nativeQuery = true, value = """
    WITH params AS (...),
    appointments AS (
        SELECT ...
        FROM appointment a              -- ❌ Missing schema
        INNER JOIN disposition d ON ... -- ❌ Missing schema
        LEFT JOIN customer c ON ...     -- ❌ Missing schema
    )
    SELECT ...
""")
```

---

### Step 3: Verify Schema Qualifiers

**Check Pattern:**
```bash
# Good: Schema qualifier present
✅ FROM public.appointment a
✅ JOIN access_control.usp_userparms up
✅ UPDATE sales.update_batch SET ...

# Bad: Missing schema qualifier
❌ FROM appointment a
❌ JOIN disposition d
❌ UPDATE update_batch SET ...
```

**Mixed Pattern (Inconsistent - Fix Required):**
```sql
-- ❌ INCONSISTENT: Some have schema, some don't
FROM appointment a                           -- Missing schema
LEFT JOIN access_control.usp_userparms up   -- Has schema
INNER JOIN disposition d                     -- Missing schema
```

---

### Step 4: Cross-Reference with Entity Annotations

**Look up the correct schema from entity classes:**

```java
// Example: Find schema for 'appointment' table
// File: src/main/java/com/renuity/sales/model/Appointment.java

@Entity
@Table(name = "appointment")  // ❌ No schema specified
public class Appointment {
    // Default schema: 'public' (PostgreSQL default)
}

// OR with explicit schema:
@Entity
@Table(name = "tblaccess", schema = "access_control")  // ✅ Schema specified
public class Access {
    // Schema: 'access_control'
}
```

**Schema Mapping Table:**

| Table Name | Entity Class | Schema | Qualified Reference |
|------------|--------------|--------|---------------------|
| appointment | Appointment.java | public | `public.appointment` |
| disposition | Disposition.java | public | `public.disposition` |
| customer | Customer.java | public | `public.customer` |
| tblaccess | Access.java | access_control | `access_control.tblaccess` |
| usp_userparms | (View/Table) | access_control | `access_control.usp_userparms` |
| update_batch | (Temp table) | public or sales | `public.update_batch` |

---

### Step 5: Apply Fixes

**Before (Problematic):**
```java
// File: IssueGridNativeRepository.java
@Query(nativeQuery = true, value = """
    WITH appointments AS (
        SELECT 
            a.id,
            a.appt_date,
            c.name AS customer_name,
            d.description AS disposition
        FROM appointment a                -- ❌ Missing schema
        INNER JOIN disposition d ON ...   -- ❌ Missing schema
        LEFT JOIN customer c ON ...       -- ❌ Missing schema
    )
    SELECT * FROM appointments
""")
List<IssueGridRowDto> findIssueGrid(...);
```

**After (Fixed):**
```java
// File: IssueGridNativeRepository.java
@Query(nativeQuery = true, value = """
    WITH appointments AS (
        SELECT 
            a.id,
            a.appt_date,
            c.name AS customer_name,
            d.description AS disposition
        FROM public.appointment a              -- ✅ Schema qualified
        INNER JOIN public.disposition d ON ... -- ✅ Schema qualified
        LEFT JOIN public.customer c ON ...     -- ✅ Schema qualified
    )
    SELECT * FROM appointments
""")
List<IssueGridRowDto> findIssueGrid(...);
```

**Before (update_batch issue):**
```java
// File: AppAppointmentRepository.java
@Query(value = """
    SELECT COUNT(*) FROM update_batch  -- ❌ Missing schema
    WHERE tenant_id = :tenantId
""", nativeQuery = true)
int updateIssueChecked(...);
```

**After (Fixed):**
```java
// File: AppAppointmentRepository.java
@Query(value = """
    SELECT COUNT(*) FROM public.update_batch  -- ✅ Schema qualified
    WHERE tenant_id = :tenantId
""", nativeQuery = true)
int updateIssueChecked(...);
```

---

### Step 6: Standardize Schema References

**Schema Naming Convention:**

```sql
-- ✅ PREFERRED: Explicit schema in all environments
public.table_name         -- PostgreSQL default schema
access_control.table_name -- Custom schema for access management
sales.table_name          -- Domain-specific schema
audit.table_name          -- Audit/logging schema

-- ❌ AVOID: Relying on search_path (varies by environment)
table_name  -- Depends on PostgreSQL search_path setting
```

**Multi-Tenant Considerations:**

```java
// If using schema-per-tenant pattern:
@Query(nativeQuery = true, value = """
    -- ⚠️ Schema name must be parameterized or resolved at runtime
    SELECT * FROM ${tenantSchema}.appointment a
    WHERE a.tenant_id = :tenantId
""")
// NOTE: This requires custom query processing or Hibernate Multitenancy
```

**Standard Pattern (Most Common):**
```java
// Single schema per table type:
// - Business data: public schema (or domain schema like 'sales')
// - Access control: access_control schema
// - Audit logs: audit schema

@Query(nativeQuery = true, value = """
    SELECT ...
    FROM public.appointment a
    JOIN public.disposition d ON d.id = a.dsp_id
    JOIN access_control.tblaccess acc ON acc.user_id = a.created_by
    WHERE a.tenant_id = :tenantId
""")
```

---

### Step 7: Test with Integration Tests

**Run Testcontainers Integration Tests:**

```bash
# Run repository integration tests
mvn test -Dtest=*Repository*Test

# Or run specific repository test
mvn test -Dtest=IssueGridNativeRepositoryTest

# Or run all integration tests (if separated)
mvn verify -Pintegration-tests
```

**Expected Test Setup (Testcontainers):**

```java
@Testcontainers
@DataJpaTest
class IssueGridNativeRepositoryTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test")
            .withInitScript("schema.sql");  // ⚠️ Must create schemas here
    
    @DynamicPropertySource
    static void setProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Test
    void testNativeQuery_withSchemaQualifiers() {
        // Test will fail if schema qualifiers missing
        List<IssueGridRowDto> results = repository.findIssueGrid(...);
        assertThat(results).isNotNull();
    }
}
```

**Test Database Schema Setup (schema.sql):**

```sql
-- Create schemas before running tests
CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS access_control;
CREATE SCHEMA IF NOT EXISTS sales;

-- Create tables in correct schemas
CREATE TABLE public.appointment (...);
CREATE TABLE public.disposition (...);
CREATE TABLE access_control.tblaccess (...);
CREATE TABLE public.update_batch (...);
```

---

### Step 8: Document Schema Decisions

**Add comments for non-obvious schema choices:**

```java
/**
 * Fetches issue grid data using native SQL.
 * 
 * Schema Qualifiers:
 * - public.appointment: Main appointment table (default schema)
 * - public.disposition: Disposition lookup (default schema)
 * - public.customer: Customer master data (default schema)
 * - access_control.usp_userparms: User parameters view (access control schema)
 * 
 * Multi-Schema Strategy:
 * - Business data: 'public' schema (PostgreSQL default)
 * - Access/permissions: 'access_control' schema
 * - Audit logs: 'audit' schema (if applicable)
 * 
 * @param tenantId Tenant identifier for multi-tenant filtering
 * @param userId User identifier for permission checks
 * @param market Market filter (or 'ALL' for all markets)
 * @param date Appointment date
 * @return List of issue grid rows
 */
@Query(nativeQuery = true, value = """
    WITH appointments AS (
        SELECT ...
        FROM public.appointment a
        INNER JOIN public.disposition d ON d.id = a.dsp_id
        LEFT JOIN access_control.usp_userparms up ON up.emp_id = a.created_by
    )
    SELECT * FROM appointments
""")
List<IssueGridRowDto> findIssueGrid(
    @Param("tenantId") Short tenantId,
    @Param("userId") Long userId,
    @Param("market") String market,
    @Param("date") LocalDate date
);
```

**Schema Configuration Documentation (README.md or application.yml):**

```yaml
# application.yml
spring:
  datasource:
    # PostgreSQL search_path (order matters)
    # Note: Native queries MUST use explicit schema qualifiers
    #       This search_path is for JPA/Hibernate entity resolution only
    hikari:
      data-source-properties:
        currentSchema: public,access_control,sales
  
  jpa:
    properties:
      hibernate:
        default_schema: public  # Default schema for entities without @Table(schema=...)
```

**Project Documentation:**

```markdown
## Database Schema Organization

### Schema Layout:
- **public**: Core business entities (appointment, customer, disposition, product, etc.)
- **access_control**: User access, permissions, branch access
- **sales**: Sales-specific tables (sale_difference, tracking_log, etc.)
- **audit**: Audit logs (if separated)

### Native SQL Requirements:
ALL native SQL queries (@Query with nativeQuery=true) MUST use explicit schema qualifiers:

✅ Correct:
```sql
FROM public.appointment a
JOIN access_control.tblaccess acc
```

❌ Incorrect:
```sql
FROM appointment a  -- Missing schema
JOIN tblaccess acc  -- Missing schema
```

### Why Explicit Schemas?
1. Production uses schema-per-domain isolation
2. PostgreSQL search_path varies by environment
3. Prevents "relation does not exist" errors
4. Enables multi-tenant schema separation (future)
```
## Pitfalls
## Pitfalls

### 1. Assuming Default Schema Works Everywhere

**Problem:**
```sql
-- ❌ Works in dev (search_path=public), fails in prod (search_path=tenant_schema)
FROM appointment a
```

**Why It Fails:**
- Development: `SET search_path TO public;` (default)
- Testing: `SET search_path TO public,access_control;`
- Production: `SET search_path TO tenant_001,public,access_control;`
- Result: Query behavior differs across environments

**Solution:**
```sql
-- ✅ Always explicit - works in all environments
FROM public.appointment a
```

---

### 2. Mixing Qualified and Unqualified References

**Problem:**
```sql
-- ❌ INCONSISTENT: Some tables qualified, some not
FROM public.appointment a
INNER JOIN disposition d ON d.id = a.dsp_id  -- ❌ Missing schema
LEFT JOIN access_control.tblaccess acc ON acc.user_id = a.user_id
```

**Why It's Bad:**
- Confusing for maintainers
- Suggests incomplete migration
- Different tables may resolve to wrong schema
- Code review misses the pattern

**Solution:**
```sql
-- ✅ CONSISTENT: All tables qualified
FROM public.appointment a
INNER JOIN public.disposition d ON d.id = a.dsp_id
LEFT JOIN access_control.tblaccess acc ON acc.user_id = a.user_id
```

---

### 3. Using Schema Qualifiers in JPQL Queries

**Problem:**
```java
// ❌ WRONG: Schema qualifiers in JPQL/HQL (entity-based queries)
@Query("SELECT a FROM public.Appointment a WHERE a.tenantId = :tenantId")
// This will fail - JPQL uses entity names, not table names
```

**Why It Fails:**
- JPQL queries use entity class names (Appointment), not table names (appointment)
- Schema is resolved from @Table annotation, not query
- Hibernate/JPA manages schema mapping

**Solution:**
```java
// ✅ CORRECT: Use entity name, schema from @Table annotation
@Query("SELECT a FROM Appointment a WHERE a.tenantId = :tenantId")
// Entity Appointment.java has @Table(name = "appointment", schema = "public")
// or @Table(name = "appointment") which defaults to default_schema config
```

**Rule:**
- **Native SQL queries**: Use schema.table_name (e.g., `public.appointment`)
- **JPQL/HQL queries**: Use entity name only (e.g., `Appointment`)

---

### 4. Forgetting CTEs (WITH Clauses)

**Problem:**
```sql
-- ❌ Schema qualifier missing in CTE
WITH employee_data AS (
    SELECT emp_id, emp_name
    FROM employees  -- ❌ Missing schema
)
SELECT * FROM employee_data
```

**Real Example from Codebase:**
```sql
-- ❌ From IssueGridNativeRepository.java
WITH appointments AS (
    SELECT ...
    FROM appointment a              -- ❌ Missing schema
    INNER JOIN disposition d ON ... -- ❌ Missing schema
)
SELECT * FROM appointments
```

**Solution:**
```sql
-- ✅ Schema qualifiers in CTE
WITH employee_data AS (
    SELECT emp_id, emp_name
    FROM public.employees  -- ✅ Schema qualified
)
SELECT * FROM employee_data
```

---

### 5. Missing Schema in Subqueries

**Problem:**
```sql
-- ❌ Outer query qualified, subquery not
SELECT a.id, a.name
FROM public.appointment a
WHERE a.market_id IN (
    SELECT m.id FROM markets m  -- ❌ Missing schema in subquery
)
```

**Solution:**
```sql
-- ✅ Schema qualifiers in subqueries too
SELECT a.id, a.name
FROM public.appointment a
WHERE a.market_id IN (
    SELECT m.id FROM public.markets m  -- ✅ Qualified
)
```

---

### 6. Hardcoding Schema Names in Multi-Tenant Apps

**Problem:**
```sql
-- ❌ Hardcoded schema won't work for schema-per-tenant
FROM tenant_001.appointment a  -- Only works for tenant_001
```

**When This Applies:**
- Multi-tenant architecture using **schema-per-tenant** strategy
- Each tenant has separate schema (tenant_001, tenant_002, etc.)
- Schema name varies at runtime

**Wrong Solution:**
```java
// ❌ Hardcoded schema in native query
@Query(value = "SELECT * FROM tenant_001.appointment", nativeQuery = true)
```

**Partial Solution (String Substitution - NOT RECOMMENDED):**
```java
// ⚠️ DANGEROUS: SQL injection risk if not validated
@Query(value = "SELECT * FROM ${tenantSchema}.appointment", nativeQuery = true)
// Requires custom query processing, high risk
```

**Correct Solution (Use Tenant Filter Instead):**
```java
// ✅ RECOMMENDED: Use tenant_id column instead of schema-per-tenant
@Query(value = "SELECT * FROM public.appointment WHERE tenant_id = :tenantId", nativeQuery = true)
List<Appointment> findByTenant(@Param("tenantId") Long tenantId);
```

**Alternative (Hibernate Multitenancy - Advanced):**
```java
// ✅ RECOMMENDED for true schema-per-tenant:
// Use Hibernate's MultitenancyStrategy.SCHEMA
// Schema is resolved at runtime via CurrentTenantIdentifierResolver
// No schema qualifiers needed - Hibernate injects tenant schema automatically
```

**For This Codebase:**
- Current pattern: **tenant_id column** (not schema-per-tenant)
- Use explicit schema qualifiers: `public.appointment`, `access_control.tblaccess`
- Filter by tenant_id in WHERE clause

---

### 7. Trusting IDE Warnings Alone

**Problem:**
- IntelliJ/Eclipse may not validate schema references in native SQL
- IDE autocomplete might not show schema.table suggestions
- Syntax highlighting may not catch missing schema

**Example:**
```java
@Query(nativeQuery = true, value = """
    FROM appointment a  -- ⚠️ IDE shows no error, but query will fail in prod
""")
```

**Why IDEs Miss This:**
- IDE doesn't know production schema configuration
- Native SQL is just a string - not parsed by IDE
- Database connection in IDE may use different search_path

**Solution:**
```bash
# Don't rely on IDE alone - validate with:
1. Static analysis: grep for native queries, check table refs
2. Integration tests: Run with PostgreSQL (Testcontainers)
3. Code review: Peer validates schema qualifiers
4. Staging deployment: Test in prod-like environment
```

---

### 8. Incorrect Schema Names (Typos)

**Problem:**
```sql
-- ❌ Typo: access_controls vs access_control
FROM access_controls.tblaccess acc  -- Will fail: schema does not exist
```

**Common Typos:**
- `access_controls` instead of `access_control`
- `public_schema` instead of `public`
- `sale` instead of `sales`

**Solution:**
```java
// ✅ Cross-reference with entity @Table annotation
@Entity
@Table(name = "tblaccess", schema = "access_control")  // Source of truth
public class Access { ... }

// Use exact schema name from entity:
@Query(value = "FROM access_control.tblaccess", nativeQuery = true)
//                   ^^^^^^^^^^^^^^^^ Match entity schema exactly
```

---

### 9. Forgetting About Views and Temporary Tables

**Problem:**
```sql
-- ❌ Views also need schema qualifiers
FROM usp_userparms up  -- ❌ Missing schema (it's a view, not a table)

-- ❌ Temporary tables might be in different schema
CREATE TEMP TABLE update_batch AS ...;
SELECT * FROM update_batch;  -- ❌ temp tables in pg_temp schema
```

**Solution:**
```sql
-- ✅ Views need schema qualification
FROM access_control.usp_userparms up

-- ✅ Temporary tables: Usually in pg_temp, but check actual location
-- Better: Avoid native SQL for temp tables, use JPA entities
```

---

### 10. Not Testing in Production-Like Environment

**Problem:**
- Tests pass locally with simple schema setup
- Production fails with complex multi-schema configuration

**Local Dev:**
```sql
SET search_path TO public;
-- All tables in public schema
```

**Production:**
```sql
SET search_path TO tenant_schema, public, access_control, sales;
-- Tables spread across multiple schemas
```

**Solution:**
```bash
# Test with production-like schema setup:
1. Use Testcontainers with multi-schema initialization
2. Run integration tests in staging environment
3. Validate schema.sql matches production DDL
4. Check PostgreSQL logs for "relation does not exist" warnings
```

---

### Summary of Key Pitfalls

| Pitfall | Risk Level | Detection Method |
|---------|------------|------------------|
| Missing default schema assumption | 🔴 HIGH | Integration tests, prod staging |
| Mixing qualified/unqualified | 🟡 MEDIUM | Code review, static analysis |
| Schema in JPQL queries | 🔴 HIGH | Unit tests (fail immediately) |
| Forgotten CTEs | 🔴 HIGH | Integration tests |
| Forgotten subqueries | 🔴 HIGH | Integration tests |
| Hardcoded tenant schema | 🟡 MEDIUM | Multi-tenant testing |
| IDE not catching errors | 🟡 MEDIUM | Integration tests, peer review |
| Schema name typos | 🔴 HIGH | Integration tests (immediate fail) |
| Views/temp tables | 🟡 MEDIUM | Integration tests |
| Not testing prod config | 🔴 HIGH | Staging deployment |

**Prevention Strategy:**
1. ✅ Use explicit schema qualifiers in ALL native SQL
2. ✅ Cross-reference entity @Table annotations
3. ✅ Run integration tests with Testcontainers
4. ✅ Code review checklist for schema qualifiers
5. ✅ Staging deployment before production
## Verification
1. Run grep '@Query.*nativeQuery.*true' and verify all results have schema qualifiers
2. Execute mvn clean compile - ensure no syntax errors introduced
3. Run integration tests: mvn test -Dtest=*Repository*Test (with Testcontainers)
4. Check PostgreSQL logs for 'relation does not exist' errors during test execution
5. Validate CTEs and subqueries separately - ensure all table refs have schema
6. Code review: Peer validates schema names match entity @Table annotations
7. Run in staging environment with production-like schema configuration