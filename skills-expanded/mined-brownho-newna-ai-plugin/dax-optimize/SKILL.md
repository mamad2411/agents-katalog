---
name: dax-optimize
description: Analyze and optimize DAX measures in Power BI PBIP projects. Use when the user says "optimize DAX", "is this DAX slow", "review my measures", "DAX performance", "improve DAX", "check DAX patterns", or invokes /dax-optimize. Spawns the dax-analyzer agent for comprehensive scanning, then presents findings and offers to apply rewrites.
argument-hint: [measure-name|all]
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, Agent]
---

# /dax-optimize

Scan DAX measures for anti-patterns, performance issues, and complexity. Suggest optimizations with before/after rewrites.

Arguments: $ARGUMENTS

- No arguments or `all`: scan every measure in the model
- Specific measure name: analyze just that measure

## Step 1: Spawn the dax-analyzer agent

Launch the `dax-analyzer` agent to scan the model:

```
Analyze DAX measures in the Power BI PBIP project at <project-path>.
Check all measures for performance anti-patterns (missing DIVIDE,
FILTER on large tables, nested CALCULATE, missing variables, etc.).
Rate complexity 1-5 and suggest optimizations with rewrites.
```

If a specific measure was requested, tell the agent to focus on that one but still scan its dependencies.

## Step 2: Present findings

Show results organized by severity:

**Critical issues** (will cause errors or major performance problems):
- List each with the problematic DAX and suggested fix

**Warnings** (performance improvements available):
- List each with before/after comparison

**Info** (style and readability improvements):
- List each briefly

Include the complexity distribution: "X simple, Y standard, Z moderate, W complex measures"

## Step 3: Offer to apply fixes

For each issue, ask: "Apply this optimization? (y/n)"

If yes:
1. Read the `.tmdl` file
2. Replace the measure's DAX expression with the optimized version
3. Preserve all metadata (displayFolder, lineageTag, annotations, formatString)
4. Verify the edit looks correct

Never change the measure name, lineageTag, or displayFolder — only the DAX expression.

## Step 4: Post-optimization

After applying changes:
- Update the data dictionary if available
- Update the changelog: "Optimized DAX in X measures (fixed: missing DIVIDE, unnecessary FILTER, ...)"
