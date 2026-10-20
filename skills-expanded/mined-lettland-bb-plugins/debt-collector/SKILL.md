---
name: debt-collector
description: Use when finding and prioritizing technical debt — TODOs, hacks, dead code, deprecated patterns, ranked with impact and effort.
metadata:
  added: 2026-06-27
  last_reviewed: 2026-06-27
  type: meta
  status: draft
  related: [refactoring, code-review]
  owns: technical-debt
---

# Debt Collector

This skill finds, catalogs, and prioritizes technical debt. Use it when you want a living
inventory of debt — not just a list of problems, but a ranked one: impact scored, effort
estimated, with a clear "fix NOW vs let it ride" verdict per item.

Not all debt is bad. Some debt is strategic. The job is to make the invisible visible so
decisions are informed. Catalog and prioritize; never auto-fix — humans (or write-enabled
language experts) decide what to pay and when.

## What counts as technical debt

### High signal (definitely debt)

- `TODO`, `FIXME`, `HACK`, `WORKAROUND`, `XXX` comments
- Duplicated code blocks (same logic in multiple places)
- Dead code (functions/components never called)
- Hardcoded values that should be config
- Missing error handling on external calls
- Deprecated API usage (library warnings)
- Security: exposed secrets, SQL injection vectors, XSS risks

### Medium signal (probably debt)

- Functions over 100 lines
- Files over 500 lines
- Deeply nested conditionals (3+ levels)
- Inconsistent naming conventions
- Missing types on public interfaces
- Test files that are commented out

### Low signal (maybe debt, depends on context)

- Missing documentation on internal functions
- Console.log statements left in
- Unused imports
- Inconsistent formatting (if no formatter configured)

## Scan process

### Step 1: Quick scan (always first)

```
Grep for: TODO|FIXME|HACK|WORKAROUND|XXX|DEPRECATED
```

This gives you the "admitted debt" — things developers already know about.

### Step 2: Pattern scan

- Grep for hardcoded URLs, IPs, ports, credentials
- Grep for `any` type annotations (TypeScript)
- Glob for test files, check for empty/commented-out tests
- Check for `.env.example` — are all required vars documented?

### Step 3: Structural scan

- Find the largest files (likely complexity hotspots)
- Find files with the most imports (coupling hotspots)
- Check for circular dependencies
- Look for god objects/components (doing too many things)

### Step 4: Age scan

Read git log to find TODOs > 30 days old (stale), files that change frequently
(churn = fragility), and large files that grow but never shrink.

## Output: debt inventory

```markdown
# Technical Debt Inventory

Last scan: [date]

## Critical (fix this sprint)

| #   | Location  | Type     | Description | Impact | Effort |
| --- | --------- | -------- | ----------- | ------ | ------ |
| 1   | file:line | security | [desc]      | HIGH   | 30m    |

## High (fix this month)

## Medium (fix when nearby)

## Low (track, don't fix)

(same columns)

## Metrics

- Total debt items: [N]
- Critical: [N] | High: [N] | Medium: [N] | Low: [N]
- Estimated total effort: [hours]
- Oldest unfixed TODO: [date] in [file]
- Highest churn file: [file] ([N] changes in last 30 days)
```

## Prioritization framework

Score each item on two axes.

**Impact** (1-5):

- 5: Security risk or data loss potential
- 4: Blocks feature development
- 3: Slows development significantly
- 2: Minor friction
- 1: Cosmetic / style issue

**Effort**: Quick (< 15 min), Small (15-60 min), Medium (1-4 hrs), Large (4+ hrs).

**Priority rule:** Fix HIGH impact + QUICK effort items immediately (best ROI). Track HIGH
impact + LARGE effort items for sprint planning. Ignore LOW impact items unless you're
already in the file.

## Rules

- Scan first, judge second. Collect all debt before prioritizing.
- Never auto-fix. You catalog — humans decide what to fix and when.
- Security debt is always Critical. No exceptions.
- Dead code older than 90 days should be deleted, not documented.
- If a TODO has a ticket/issue reference, include it. Otherwise flag as "untracked."
- Don't count test-specific TODOs the same as production TODOs.
