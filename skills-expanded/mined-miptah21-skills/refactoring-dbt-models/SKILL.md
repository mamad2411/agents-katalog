---
name: refactoring-dbt-models
description: |
  Safely refactors dbt models with downstream impact analysis. Use when restructuring dbt models for:
  (1) Task mentions "refactor", "restructure", "extract", "split", "break into", or "reorganize"
  (2) Extracting CTEs to intermediate models or creating macros
  (3) Modifying model logic that has downstream consumers
  (4) Renaming columns, changing types, or reorganizing model dependencies
  Analyzes all downstream dependencies BEFORE making changes.
---

**Find ALL downstream dependencies before changing. Refactor in small steps. Verify output after each change.**

### 1. Analyze Current Model
```bash
cat models/<path>/<model_name>.sql
```
Identify refactoring opportunities:
- CTEs longer than 50 lines → extract to intermediate model
- Logic repeated across models → extract to macro
- Multiple joins in sequence → split into steps
- Complex WHERE clauses → extract to staging filter

### 2. Find All Downstream Dependencies
**CRITICAL: Never refactor without knowing impact.**
```bash
dbt ls --select model_name+ --output list
grep -r "ref('model_name')" models/ --include="*.sql"
```
**Report to user:** "Found X downstream models: [list]. These will be affected by changes."

### 3. Check What Columns Downstream Models Use
```bash
cat models/<path>/<downstream_model>.sql | grep -E "model_name\.\w+|alias\.\w+"
```

### 4. Plan Refactoring Strategy
| Opportunity | Strategy |
|-------------|----------|
| Long CTE | Extract to intermediate model |
| Repeated logic | Create macro in `macros/` |
| Complex join | Split into intermediate models |
| Multiple concerns | Separate into focused models |

### 5. Execute Refactoring (one change at a time)

#### Pattern: Extract CTE to Model
```sql
-- customer_metrics.sql (new file)
select customer_id, ...
from {{ ref('customers') }}

-- orders.sql (simplified)
select ...
from {{ ref('raw_orders') }} orders
join {{ ref('customer_metrics') }} cm on ...
```

#### Pattern: Extract to Macro
```sql
-- macros/categorize_amount.sql
{% macro categorize_amount(column_name) %}
case
    when {{ column_name }} < 0 then 'refund'
    when {{ column_name }} = 0 then 'zero'
    else 'positive'
end
{% endmacro %}
```

### 6. Validate Changes
```bash
dbt compile --select +model_name+
dbt build --select +model_name+
```

### 7. Verify Output Matches Original
```bash
dbt show --inline "select count(*) from {{ ref('model_name') }}"
dbt show --select <model_name> --limit 10
```

## Refactoring Checklist
- [ ] All downstream dependencies identified
- [ ] User informed of impact scope
- [ ] One change at a time
- [ ] Build passes after each change
- [ ] Output validated (row counts match)
- [ ] Documentation updated
- [ ] Tests still pass

## Common Refactoring Triggers
| Symptom | Refactoring |
|---------|-------------|
| Model > 200 lines | Extract CTEs to models |
| Same logic in 3+ models | Extract to macro |
| 5+ joins in one model | Create intermediate models |
| Hard to understand | Add CTEs with clear names |
| Slow performance | Split to allow parallelization |

## Anti-Patterns
- Refactoring without checking downstream impact
- Making multiple changes at once
- Not validating output matches after refactoring
- Extracting prematurely (wait for 3+ uses)
- Breaking existing tests without updating them
