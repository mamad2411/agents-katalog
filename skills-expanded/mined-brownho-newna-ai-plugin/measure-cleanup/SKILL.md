---
name: measure-cleanup
description: Find and remove unused Power BI measures from PBIP projects. Use when the user says "find unused measures", "clean up measures", "dead measures", "remove old measures", "which measures are used", or invokes /measure-cleanup. Spawns the measure-analyzer agent for heavy scanning, then guides interactive deletion.
argument-hint: [project-path]
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, Agent]
---

# /measure-cleanup

Find measures that are not used anywhere in the report, model, or visuals, and help the user safely remove them.

Arguments: $ARGUMENTS

## Step 1: Spawn the measure-analyzer agent

Launch the `measure-analyzer` agent (from this plugin's `agents/` directory) to do the heavy scanning:

```
Analyze the Power BI PBIP project at <project-path> for unused measures.
Scan all .tmdl files, check references in other measures, report visuals,
filters, and bookmarks. Return a structured report of unused measures
with their names, tables, DAX expressions, and classification.
```

The agent will return a structured report of all measures and their usage status.

## Step 2: Present findings

Show the user a clear table of unused measures:

| # | Measure | Table | Folder | DAX (preview) |
|---|---------|-------|--------|---------------|
| 1 | Old Test Calc | Kite Measures | GD-0543 | `CALCULATE(SUM(...))` |
| 2 | Temp Metric | Trend Measures | Debug | `[Revenue] * 0.1` |

Include the summary stats: "Found X unused measures out of Y total (Z%)."

Add a caveat: "These measures have no references in the TMDL model or report files. However, they might be used by external tools, paginated reports, or Power BI Service features not visible in the project files."

## Step 3: Interactive deletion

**Never auto-delete.** For each unused measure, ask the user:
- Show the full DAX expression
- Ask: "Remove this measure? (y/n/skip all)"

If the user says yes:
1. Read the `.tmdl` file containing the measure
2. Remove the entire measure block (from `measure '<Name>'` through to the next `measure`, `column`, or end of `table` block)
3. Verify the file still parses correctly (no orphaned indentation or broken blocks)

If the user says "skip all", stop the deletion loop.

## Step 4: Post-cleanup verification

After removing measures:
1. Re-scan to check if removals created new orphans (a measure that was only used by a now-deleted measure)
2. If new orphans found, report them and offer to remove
3. Update the data dictionary if the `data-dictionary` skill is available
4. Update the changelog if the `pbip-changelog` skill is available

## Step 5: Report

Summarize what was done:
- X measures analyzed
- Y identified as unused
- Z removed (list names)
- Any new orphans found after removal
