---
name: mes-mysql-schema-check
description: Use when modifying or validating MySQL schema.sql, Java entities, MyBatis mappers, table names, primary keys, field types, or database consistency for AI-MES Copilot.
---

# MES MySQL Schema Check

## Purpose

Use this to prevent schema/entity drift. It is required when touching `schema.sql`, entity classes, mapper SQL, table names, primary keys, or core database fields.

## Checks

1. Read `docs/SETUP.md` and `scripts/lamp_migrations.py` for the ordered schema baseline. Include both `schema.sql` and the applicable migrations when inspecting current table definitions.
2. Count entity classes with `@TableName`.
3. Compare table names between the effective migrated schema and entities; counts from the base `schema.sql` alone are only a starting point.
4. Compare SQL primary keys with `@TableId`.
5. Spot-check important type mapping:
   - `BIGINT` -> `Long`
   - `DECIMAL` -> `BigDecimal`
   - `DATE` -> `LocalDate`
   - `DATETIME` -> `LocalDateTime`
   - `TINYINT` -> `Integer` unless Boolean is explicitly designed
6. Confirm `deleted_flag` handling for business tables.

## Useful Commands

Run from repository root:

```powershell
(Select-String -Path workspace\idea\ems\src\main\resources\db\schema.sql -Pattern '^CREATE TABLE `' | Measure-Object).Count
(rg -n "@TableName\(" workspace\idea\ems\src\main\java\com\neuedu\ems\entity | Measure-Object).Count
(rg -n "@TableId\(" workspace\idea\ems\src\main\java\com\neuedu\ems\entity | Measure-Object).Count
```

## Fix Workflow

1. Determine whether SQL or entity is wrong.
2. Prefer `schema.sql`, the ordered migrations, and verified isolated database design as baseline.
3. Fix entity annotations and fields before mapper/controller code.
4. Re-run the counts and Maven test.
5. Record any intentional schema change in `COLLABORATION.md`.

## Must Not

- Do not silently add fields only in Java or only in SQL.
- Do not change primary keys without checking all affected entities and mappers.
- Do not use ad hoc string mapping for structured SQL inspection when normal tooling is available.
