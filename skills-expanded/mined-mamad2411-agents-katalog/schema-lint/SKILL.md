---
name: schema-lint
description: Validate ORM schema for variable visibility bugs, missing hidden variables, and schema/vars.tf drift. This skill should be used when adding new Terraform variables, modifying schema files, before creating ORM zips, or when unexpected fields appear in the ORM UI. Also triggered by "check schema", "lint schema", "validate schema", "schema bug", "ORM showing wrong fields".
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob
---

# ORM Schema Linter

Validate OCI Resource Manager schemas for correctness, catching variable visibility bugs and schema drift before they reach the ORM UI.

## The Core Rule

**Every variable in `vars.tf` that is not universally visible MUST be explicitly listed in `common_schema.yaml` with `visible: false`, then selectively overridden with `visible: true` in category-specific schemas that need it.**

ORM behavior: any variable defined in Terraform that is NOT mentioned in the schema is displayed as a raw field in the ORM UI. This means a variable added to `vars.tf` without a corresponding `visible: false` entry in `common_schema.yaml` will leak into every category's ORM form.

## When to Run

- After adding or renaming any variable in `vars.tf`
- After modifying any schema YAML file
- Before creating an ORM zip (`/integration-test`, `/deploy-and-test`, or manual zip)
- When debugging unexpected fields in the ORM UI
- As part of PR review for changes touching `vars.tf` or `schemas/`

## Validation Steps

### Step 1: Check for Unhidden Variables

Find all variables in `vars.tf` that are NOT mentioned in `common_schema.yaml`:

```bash
cd ai-accelerator-tf

# Extract variable names from vars.tf
grep -oP 'variable\s+"(\K[^"]+)' vars.tf | sort > /tmp/tf_vars.txt

# Extract variable names from common_schema.yaml (under 'variables:' section)
grep -oP '^\s{2}(\K\w+):' schemas/common_schema.yaml | sort > /tmp/schema_vars.txt

# Find variables in TF but not in schema
comm -23 /tmp/tf_vars.txt /tmp/schema_vars.txt
```

**Any output from the last command is a potential bug.** Each listed variable will appear as a raw field in ORM categories that don't explicitly hide it.

### Step 2: Verify Category-Specific Overrides

For variables that should only appear in certain categories, verify the visibility pattern:

```bash
# For each category-specific variable (e.g., skin_cuopt_core):
for category in cuopt vss paas_rag enterprise_rag enterprise_rag_aiq; do
  echo "=== $category ==="
  grep -A2 "skin_cuopt_core" schemas/generated/${category}_schema.yaml 2>/dev/null || echo "NOT FOUND"
done
```

The correct pattern:
- `common_schema.yaml`: `visible: false` (hidden by default)
- `cuopt_schema.yaml`: `visible: true` (shown only for cuOpt)

### Step 3: Regenerate and Diff

Regenerate all schemas and check for unexpected changes:

```bash
source venv/bin/activate 2>/dev/null
cd ai-accelerator-tf/schemas
python3 ../create_final_schema.py --all 2>/dev/null || python3 create_final_schema.py --all
```

### Step 4: Run Schema Tests

```bash
pytest ai-accelerator-tf/schemas/tests/ -v
```

### Step 5: Cross-Check Variable Groups

Verify every variable listed in a `variableGroups` section actually exists in the `variables` section:

```bash
# Extract variables referenced in variableGroups
grep -A1 "variables:" schemas/common_schema.yaml | grep "^\s*-" | sed 's/.*- //' | sort > /tmp/group_vars.txt

# Compare with defined variables
comm -23 /tmp/group_vars.txt /tmp/schema_vars.txt
```

Any output means a variable group references an undefined variable.

## Common Bugs

Refer to `references/common-bugs.md` for detailed examples of schema bugs and their fixes.

## Fixing Visibility Bugs

To hide a variable that's leaking into the ORM UI:

1. Add to `common_schema.yaml` under the `variables:` section:
   ```yaml
     variable_name:
       type: string  # match the type in vars.tf
       visible: false
   ```

2. If the variable should be visible in specific categories, add to that category's schema:
   ```yaml
     variable_name:
       visible: true
       title: "Human Readable Title"
       description: "Description for ORM UI"
       required: true  # if needed
   ```

3. Regenerate all schemas and run tests.
