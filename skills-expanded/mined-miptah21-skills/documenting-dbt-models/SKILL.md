---
name: documenting-dbt-models
description: |
  Documents dbt models and columns in schema.yml. Use when working with dbt documentation for:
  (1) Adding model descriptions or column definitions to schema.yml
  (2) Task mentions "document", "describe", "description", "dbt docs", or "schema.yml"
  (3) Explaining business context, grain, meaning of data, or business rules
  (4) Preparing dbt docs generate or improving model discoverability
  Matches existing project documentation style and conventions before writing.
---

**Document the WHY, not just the WHAT. Include grain, business rules, and caveats.**

### 1. Study Existing Documentation Patterns
**CRITICAL: Match the project's documentation style before adding new docs.**

```bash
find . -name "schema.yml" | head -5
cat models/marts/schema.yml | head -150
cat models/staging/schema.yml | head -150
```

**Extract from existing documentation:**
- Description length (brief vs detailed)
- Formatting style (plain text vs markdown with headers)
- Information included (grain? business rules? caveats?)
- Column description depth (all columns vs key columns)
- Use of meta tags or custom properties

### 2. Read Model SQL
```bash
cat models/<path>/<model_name>.sql
```

### 3. Check Existing Documentation for This Model
```bash
find . -name "schema.yml" -exec grep -l "<model_name>" {} \;
cat models/<path>/schema.yml | grep -A 100 "<model_name>"
```

### 4. Identify Documentation Needs
For each model, document:
- **Model description**: Purpose, grain, key business rules
- **Column descriptions**: Business meaning, not just data type

### 5. Write Documentation
**Match the style discovered in step 1.**

### Model Description Template
```yaml
description: |
  [One sentence: what this model contains]

  **Grain:** [What does one row represent?]

  **Business Rules:**
  - [Key rule 1]
  - [Key rule 2]

  **Caveats:**
  - [Important limitation or edge case]
```

### Column Description Patterns
| Column Type | Documentation Focus |
|-------------|---------------------|
| Primary key | Source system, uniqueness guarantee |
| Foreign key | What it joins to, NULL handling |
| Metric | Calculation formula, units, exclusions |
| Date | Timezone, what event it represents |
| Status/Category | All possible values, business meaning |
| Boolean/Flag | What true/false means in business terms |

### 6. Generate Docs
```bash
dbt docs generate
dbt docs serve
```

## Anti-Patterns
- Adding documentation without checking existing project patterns
- Describing WHAT instead of WHY/context
- Missing grain documentation
- Not documenting NULL handling
- Copy-pasting column names as descriptions
