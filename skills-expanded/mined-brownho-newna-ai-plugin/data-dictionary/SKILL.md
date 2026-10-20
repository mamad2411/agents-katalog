---
name: data-dictionary
description: Generate and maintain a data dictionary from Power BI TMDL model files. Auto-triggers after changes to .tmdl files, semantic model modifications, or when the user finishes editing measures, columns, or relationships. Also available as /data-dictionary for manual refresh. Use whenever you detect TMDL file changes, model edits, or the user asks "what's in the model", "update dictionary", "show me the tables", "list measures", or "refresh dictionary".
argument-hint: [project-path]
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob]
---

# Data Dictionary Generator

Generates and maintains a `data-dictionary.md` file from TMDL model definitions in a PBIP project.

Arguments: $ARGUMENTS

## When to run

- After any `.tmdl` file is created or modified
- After measures, columns, or relationships are added/changed/removed
- When the user asks about the model contents
- When `/data-dictionary` is invoked

## Step 1: Find the semantic model

Look for `.SemanticModel/definition/` directories:
```bash
find <project-dir> -maxdepth 3 -type d -name "definition" -path "*.SemanticModel/*" 2>/dev/null
```

If multiple models exist, process all of them.

## Step 2: Parse TMDL files

For each semantic model, read these files:

**Tables and columns** — from `definition/tables/*.tmdl`:
- Extract `table '<Name>'` declarations
- Extract `column '<Name>'` with `dataType`, `sourceColumn`, `isHidden`
- Extract `measure '<Name>'` with DAX expression, `displayFolder`, `formatString`
- **Skip files matching `LocalDateTable_*` and `DateTableTemplate_*`** — these are auto-generated and clutter the dictionary

**Relationships** — from `definition/relationships.tmdl`:
- Extract relationship definitions: from-table.from-column to to-table.to-column
- Note crossFilteringBehavior and isActive status

**Model metadata** ��� from `definition/model.tmdl`:
- Extract model name, culture, default power bi data source version

## Step 3: Generate data-dictionary.md

Write to `<project-root>/data-dictionary.md` using this format:

```markdown
# Data Dictionary

*Auto-generated from TMDL definitions. Last updated: YYYY-MM-DD*
*Run `/data-dictionary` to refresh.*

## Model Overview

| Metric | Count |
|--------|-------|
| Tables | X |
| Columns | X |
| Measures | X |
| Relationships | X |

## Tables

### <TableName>

| Column | Type | Source | Hidden |
|--------|------|--------|--------|
| ColumnA | string | SourceA | No |

**Measures:**

| Measure | Folder | Expression |
|---------|--------|------------|
| Total Revenue | Financial | `SUM(Sales[Revenue])` |

*(repeat for each table)*

## Relationships

| From | To | Active | Cross-Filter |
|------|----|--------|-------------|
| Sales[CustomerID] | Customer[ID] | Yes | Single |

```

## Step 4: Diff-aware updates

If `data-dictionary.md` already exists:
1. Read the existing file
2. Only rewrite sections that changed (compare table lists, measure counts)
3. Update the "Last updated" timestamp
4. This minimizes git diffs — a small model change shouldn't rewrite the entire dictionary

## Step 5: Commit note

If the git-autopilot skill is active, this update will be included in the next natural commit. Don't make a separate commit just for the dictionary — let it ride with the model changes that triggered it.

## MCP integration

If the `powerbi-knowledge` MCP server is connected, you can use its tools for faster/richer data:
- `list_objects` — get all tables, measures, columns in one call
- `get_object` — get detailed info about a specific table or measure
- `trace_lineage` — understand measure dependencies

Use MCP tools when available, fall back to direct TMDL file parsing when not.
