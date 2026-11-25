---
name: audit
description: Run a structured, read-only codebase audit using parallel agents. Surfaces dead code, security gaps, wiring issues, type safety problems, and UI shells. Produces a prioritized fix plan. Use for ship-readiness checks, pre-launch reviews, or periodic hygiene sweeps.
slug: audit
category: operations
complexity: complex
version: "1.0.0"
author: "id8Labs"
triggers:
  - "audit"
  - "audit"
tags:
  - development
  - tool-factory-retrofitted---

# /audit - Codebase Audit


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

Run a comprehensive, **read-only** audit of the target codebase. Do NOT make any changes — only read, search, and report.

## Arguments

`/audit [scope]` where scope is optional:
- No argument: audit the current project's full codebase
- A directory path: audit only that directory tree
- A comma-separated list of dimensions: `security,dead-code,wiring`

## Audit Dimensions

Run ALL dimensions by default. Use parallel Task agents (subagent_type: Explore) — one per dimension — for speed.

### 1. Security
- Auth middleware on every API route (check for missing `getUser()` / session checks)
- IDOR vulnerabilities: routes accepting entity IDs without ownership verification
- Exposed secrets or env vars in client-side code
- Missing RLS policies referenced in API routes
- CORS and CSP configuration

### 2. Dead Code
- API routes with zero frontend callers (grep for fetch/axios calls matching each route)
- Exported functions/components with zero imports
- Unused dependencies in package.json
- Orphaned test files (test files whose subject no longer exists)

### 3. Wiring Gaps
- UI components that render but fetch from nonexistent API endpoints
- Store actions defined but never dispatched
- API routes that exist but return stub/mock data
- Event handlers wired to console.log or no-ops

### 4. Type Safety
- `any` types, type assertions (`as`), and `@ts-ignore` / `@ts-expect-error`
- Missing return types on exported functions
- Zod schemas that don't match their TypeScript counterparts

### 5. UI Shells
- Components rendering placeholder text ("Coming soon", "TODO", "Lorem ipsum")
- Empty state components that are the *only* state (no real data path)
- Hardcoded demo/mock data displayed to users

## Output Format

For each finding, report:

```
| # | File:Line | Severity | Dimension | Finding | Suggested Fix |
```

Severity levels: **critical** (security/data loss risk), **high** (broken feature), **medium** (dead code/tech debt), **low** (style/cleanup)

## Deliverable

After all dimensions complete, produce a single consolidated report:

1. **Executive Summary** — 2-3 sentences: overall health, biggest risks
2. **Findings Table** — grouped by severity (critical first), then by dimension
3. **Fix Plan** — prioritized list of fixes, grouped into PRs, with effort estimates (S/M/L):
   - P0: Critical (security, data loss) — fix immediately
   - P1: High (broken features) — fix before next deploy
   - P2: Medium (dead code, wiring) — fix this sprint
   - P3: Low (cleanup) — backlog

## Rules

- **READ ONLY.** Do not edit, write, or create any files.
- Use Grep, Glob, Read, and Task (Explore agents) only.
- Be exhaustive within each dimension — don't sample, scan every relevant file.
- If a dimension has zero findings, say so explicitly (that's good news).
- Total report should be under 500 lines. Summarize if needed.
