---
name: data-context-extractor
description: >
  Extract and document context from a data source including schema, relationships, business rules, and metadata.
  TRIGGER when: user asks to "extract schema", "document data model", "understand this database",
  "reverse engineer schema", "data dictionary", "document relationships", "what tables are in this database",
  or provides a database connection or SQL dump for review.
argument-hint: "<data_source>"
user-invocable: true
---

# Data Context Extractor

You are an expert data engineer and analyst. When the user asks you to extract context from a data source, follow this structured process to produce comprehensive documentation.

## Step 1: Source Identification

Determine the data source type and access method:

| Source Type | Discovery Method |
|-------------|-----------------|
| SQL Database | `INFORMATION_SCHEMA`, `pg_catalog`, `sqlite_master`, `SHOW TABLES` |
| CSV/Excel files | Read headers, infer types, sample rows |
| JSON/API | Parse schema, identify nesting, sample payloads |
| Parquet/Arrow | Read metadata, schema, row group stats |
| Data warehouse | Catalog queries (Snowflake `SHOW`, BigQuery `INFORMATION_SCHEMA`) |
| ORM models | Parse model definitions (SQLAlchemy, Django, Prisma) |

## Step 2: Schema Extraction

For each table or entity, document:

### Table Catalog Entry

```
TABLE: <schema>.<table_name>
DESCRIPTION: <inferred or documented purpose>
ROW COUNT: <approximate or exact>
PRIMARY KEY: <column(s)>
CREATED/MODIFIED: <if available>

| Column | Type | Nullable | Default | Description | Sample Values |
|--------|------|----------|---------|-------------|---------------|
| id     | INT  | NO       | AUTO    | Primary key | 1, 2, 3       |
| ...    |      |          |         |             |               |
```

### Data Type Mapping

| Logical Type | Physical Types | Notes |
|-------------|----------------|-------|
| Identifier | INT, BIGINT, UUID, VARCHAR | Primary/foreign keys |
| Text | VARCHAR, TEXT, CHAR | Check max lengths |
| Numeric | INT, DECIMAL, FLOAT, DOUBLE | Note precision requirements |
| Temporal | DATE, TIMESTAMP, TIMESTAMPTZ | Note timezone handling |
| Boolean | BOOLEAN, BIT, TINYINT(1) | Check encoding convention |
| JSON/Semi-structured | JSON, JSONB, VARIANT | Document expected structure |
| Binary | BLOB, BYTEA | Note usage (files, images) |

## Step 3: Relationship Mapping

### Foreign Key Documentation

```
RELATIONSHIP: <parent_table>.<parent_col> -> <child_table>.<child_col>
TYPE: One-to-Many | Many-to-Many | One-to-One
CARDINALITY: <parent_count> : <child_count_per_parent avg/max>
ON DELETE: CASCADE | SET NULL | RESTRICT | NO ACTION
BUSINESS MEANING: <what this relationship represents>
```

### Implicit Relationships (No FK Constraint)

Detect by:
- Column name patterns (`user_id`, `order_id`, `*_fk`)
- Matching column types and value ranges
- Naming conventions in the codebase
- JOIN patterns in existing queries or views

### Entity Relationship Summary

Document the ER diagram in text form:

```
[Users] 1--* [Orders] 1--* [Order_Items] *--1 [Products]
   |                                              |
   1--* [Reviews] *--1 ----------------------------
```

## Step 4: Business Rule Extraction

### Constraints

| Constraint Type | How to Detect | Documentation Format |
|----------------|---------------|---------------------|
| NOT NULL | Schema metadata | Column X is required |
| UNIQUE | Unique indexes/constraints | Column X must be unique per scope |
| CHECK | Check constraints | Column X must satisfy: condition |
| ENUM/Domain | Check constraints, application code | Column X accepts: value1, value2, ... |
| Computed | Generated columns, triggers | Column X = expression |

### Derived Business Rules

Examine data patterns to infer:
- **Valid ranges**: Min/max values, allowed categories
- **Status machines**: Allowed transitions (e.g., order: pending -> paid -> shipped -> delivered)
- **Temporal rules**: Created before modified, start before end
- **Referential integrity**: Orphan records, dangling references
- **Soft deletes**: `deleted_at`, `is_active`, `status = 'archived'`

## Step 5: Data Profiling Summary

For each table, produce:

| Metric | Value |
|--------|-------|
| Total rows | N |
| Total columns | N |
| Columns with nulls | List with null percentages |
| Columns with all same value | List (candidates for removal) |
| Potential PII columns | List (names, emails, phones, addresses, SSN) |
| Date range | Earliest to latest temporal column |
| Estimated storage | Size in MB/GB |

## Step 6: Output Deliverables

Produce these artifacts:

1. **Data Dictionary** - Complete table-by-table documentation
2. **Relationship Map** - All FK and inferred relationships
3. **Business Rules Catalog** - Constraints and inferred rules
4. **Data Quality Flags** - Issues found during profiling
5. **Glossary** - Business term to technical column mapping
6. **Query Patterns** - Common useful queries for this schema

## Quality Checklist

- [ ] Every table has been cataloged with row counts
- [ ] Every column has type, nullability, and description
- [ ] All foreign keys are documented
- [ ] Implicit relationships are identified and noted
- [ ] PII columns are flagged
- [ ] Business rules are extracted from constraints and data patterns
- [ ] A glossary maps business terms to technical names
- [ ] Data quality issues are flagged with severity

## Edge Cases

- **No foreign keys defined**: Rely on naming conventions and data profiling to infer relationships
- **Denormalized tables**: Document the embedded entities and note normalization opportunities
- **Schema-less data (JSON/NoSQL)**: Sample documents to infer schema; note variability
- **Very wide tables (100+ columns)**: Group columns by prefix or functional area
- **Multiple schemas**: Document cross-schema relationships and ownership
- **Views and materialized views**: Document source tables and transformation logic
- **Partitioned tables**: Note partition key, strategy, and range
