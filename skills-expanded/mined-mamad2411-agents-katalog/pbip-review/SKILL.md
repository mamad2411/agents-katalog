---
name: pbip-review
description: Comprehensive 9-point audit of a Power BI PBIP project covering relationships, naming conventions, TMDL syntax, best practices, RLS security, performance, visual consistency, accessibility, and bookmarks. Use when the user says "review my model", "audit PBIP", "check for issues", "PBIP health check", "validate my project", or invokes /pbip-review. Spawns the pbip-reviewer agent for thorough analysis.
argument-hint: [project-path]
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, Agent]
---

# /pbip-review

Run a comprehensive audit of a Power BI PBIP project. Spawns the `pbip-reviewer` agent to run 9 independent checks, then presents findings and offers to fix auto-fixable issues.

Arguments: $ARGUMENTS

## 9 Review Areas

1. **Relationship Validator** — ambiguous paths, bidirectional risks, missing keys
2. **Naming Convention Enforcer** — table/column/measure naming standards
3. **TMDL Linter** — syntax errors, missing lineageTags, duplicates
4. **Code Review Checklist** — best practices (descriptions, no magic numbers, proper date tables)
5. **RLS Tester** — role definitions, filter validity, coverage
6. **Performance Analyzer** — complex measures, expensive patterns
7. **Visual Standardizer** — font/color/size consistency
8. **Accessibility Checker** — WCAG 2.1 AA compliance
9. **Bookmark Auditor** — orphaned bookmarks, navigation gaps

## Step 1: Spawn the pbip-reviewer agent

```
Perform a comprehensive audit of the Power BI PBIP project at <project-path>.
Run all 9 review checks. Read the reference files in the pbip-review/references/
directory for naming conventions, DAX patterns, and the review checklist.
Return a structured report with findings by severity.
```

## Step 2: Present the report

Show the summary first — total findings by severity (critical, warning, info, pass).

Then show findings grouped by severity, highest first. For each finding:
- Which check found it
- What's wrong (specific file/measure)
- How to fix it

## Step 3: Offer to fix auto-fixable issues

Some findings can be fixed automatically:
- **Missing descriptions** — add a description annotation to measures
- **Naming violations** — rename with user confirmation
- **Missing .gitignore entries** — add patterns
- **Duplicate display folders** — consolidate

Ask: "I found X auto-fixable issues. Want me to fix them? (y/n/pick)"

If "pick", list each and let the user choose.

## Step 4: Post-review

After fixes:
- Update data dictionary
- Update changelog: "Ran /pbip-review: fixed X issues (naming, descriptions, ...)"
- Report what was fixed and what still needs manual attention
