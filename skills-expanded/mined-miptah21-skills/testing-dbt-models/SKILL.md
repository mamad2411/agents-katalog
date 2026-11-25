---
name: testing-dbt-models
description: |
  Adds schema tests and data quality validation to dbt models. Use when working with dbt tests for:
  (1) Adding or modifying tests in schema.yml files
  (2) Task mentions "test", "validate", "data quality", "unique", "not_null", or "accepted_values"
  (3) Ensuring data integrity - primary keys, foreign keys, relationships
  (4) Debugging test failures or understanding why dbt test failed
  Matches existing project test patterns and YAML style before adding new tests.
---

**Every model deserves at least one test. Primary keys need unique + not_null.**

### 1. Study Existing Test Patterns
**CRITICAL: Match the project's existing testing style before adding new tests.**
```bash
find . -name "schema.yml" -exec grep -l "tests:" {} \;
cat models/staging/schema.yml | head -100
cat models/marts/schema.yml | head -100
ls tests/
cat packages.yml 2>/dev/null
```

**Extract from existing tests:**
- YAML formatting style (indentation, spacing)
- Test coverage depth (all columns vs key columns only)
- Use of custom tests (dbt_utils, dbt_expectations, custom macros)
- Severity levels used (warn vs error)

### 2. Read Model SQL
```bash
cat models/<path>/<model_name>.sql
```
Identify: primary keys, foreign keys, categorical columns, date columns, business-critical fields.

### 3. Identify Testable Columns
| Column Type | Recommended Tests |
|-------------|-------------------|
| Primary key | `unique`, `not_null` |
| Foreign key | `not_null`, `relationships` |
| Categorical | `accepted_values` |
| Required field | `not_null` |
| Date/timestamp | `not_null` |
| Boolean | `accepted_values: [true, false]` |

### 4. Write Tests in schema.yml
```yaml
version: 2
models:
  - name: model_name
    columns:
      - name: primary_key_column
        tests:
          - unique
          - not_null
      - name: foreign_key_column
        tests:
          - not_null
          - relationships:
              to: ref('related_model')
              field: related_key_column
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'active', 'completed', 'cancelled']
```

### 5. Run Tests
```bash
dbt test --select <model_name>
dbt test --select +<model_name>
```

### 6. Fix Failing Tests
| Failure | Likely Cause | Fix |
|---------|--------------|-----|
| `unique` fails | Duplicate records | Add deduplication in model |
| `not_null` fails | NULL values in source | Add COALESCE or filter |
| `relationships` fails | Orphan records | Add WHERE clause or fix upstream |
| `accepted_values` fails | New/unexpected values | Update accepted values list |

### Custom Generic Tests
```yaml
tests:
  - dbt_utils.expression_is_true:
      expression: "amount >= 0"
  - dbt_utils.recency:
      datepart: day
      field: created_at
      interval: 1
```

### Singular Tests
Create `tests/<test_name>.sql`:
```sql
select *
from {{ ref('orders') }}
where revenue < 0
```

## Anti-Patterns
- Adding tests without checking existing project patterns first
- Using different YAML formatting style than existing tests
- Models without any tests
- Primary keys without both unique AND not_null
- Hardcoding accepted_values without confirming with stakeholders
- Adding dbt_utils tests when project doesn't use that package
