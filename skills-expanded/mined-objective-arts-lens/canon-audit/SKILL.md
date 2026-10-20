---
name: canon-audit
description: Audit a project against a canon's rules and checklist. Read-only — produces prioritized report without fixing. Works with any canon (nextjs, sql, typescript, etc.).
---

# /canon-audit

**Read-only** project audit against a named canon's rules. Extracts every checkable rule from the canon's SKILL.md and topic files, scans the codebase against each, produces a prioritized report with file:line references. Makes zero edits.

> **No arguments?** Describe this skill and stop. Do not execute.

## Arguments

```
/canon-audit <canon-name> [path]
```

- `canon-name` — required. Name of the canon to audit against (e.g., `nextjs`, `sql`, `typescript`)
- `path` — optional. Directory or file to audit. Defaults to `src/` or project root

## Process

### Step 1: Resolve Canon

Find the canon at:
1. `.claude/canon/<canon-name>/` (deployed by `lens init`)

If not found, output `CANON_NOT_FOUND: <canon-name>` and stop. The user needs to re-run `lens init` with a profile that includes the canon.

Read **every file** in the canon directory:
- `SKILL.md` — main skill definition
- `*.md` — all topic files

Count total files and rules extracted. Report what was loaded.

### Step 2: Extract Rules

Parse every loaded file for auditable rules. Extract from these patterns:

**A. Explicit checklists**
```
- [ ] No `'use client'` on components that only display data
```

**B. Detection rules** — lines starting with "Detect:" or "**Detect:**"
```
**Detect:** File has `'use client'` AND component is `async function`
```

**C. Anti-patterns** — content under `## Anti-Patterns`, `### Don't...`, or `// Bad:` / `// Good:` pairs

**D. Quick reference tables** — rows with `| Pattern | Valid? | Fix |` or `| Need | Directive |`

**E. Numbered rules** — `1. **No cursors**`, `### 1. Server Components by Default`

**F. Standards from SKILL.md** — any `## Core Principles`, `## Decision Framework`, `## Code Review Checklist`

Organize extracted rules by source topic file. Each rule gets:
- A short name (e.g., `no-async-client-component`)
- The source file it came from (e.g., `rsc-boundaries.md`)
- Whether it's **grepable** (can be detected by searching for a code pattern) or **semantic** (requires reading code and judging)

### Step 3: Scan — Grepable Rules

For each grepable rule, run targeted searches across the target path.

Examples of grepable patterns:
- `<img ` without nearby `next/image` import → image.md violation
- `'use client'` + `async function` in same file → rsc-boundaries.md violation
- `SELECT *` in .sql or query strings → sql violation
- Missing `loading.tsx` in route directories → file-conventions.md violation
- Missing `error.tsx` in route directories → error-handling.md violation
- `useEffect` + `fetch` for data that could be server-fetched → data-patterns.md violation

Search source files only — skip `node_modules/`, `.next/`, `dist/`, `build/`, test files, and config files.

### Step 4: Scan — Semantic Rules

For rules that require judgment, read the relevant files and evaluate.

Examples of semantic rules:
- Is the `'use client'` boundary pushed to the smallest leaf? (rsc-boundaries.md)
- Does `generateMetadata` use actual data or hardcoded strings? (metadata.md)
- Are Server Actions used for mutations vs unnecessary API routes? (data-patterns.md)
- Is middleware thin — auth checks and redirects only? (file-conventions.md)

Group files by which semantic rules apply to them. Read each file once, evaluate all applicable rules.

### Step 5: Classify Severity

For each finding:

| Severity | Criteria | Points |
|----------|----------|--------|
| **Critical** | Broken at runtime, security risk, data loss | 3 |
| **High** | Wrong pattern that degrades perf/UX or blocks best practice | 2 |
| **Medium** | Suboptimal but functional — missing optimization, weak pattern | 1 |
| **Low** | Style/convention deviation, minor improvement opportunity | 0.5 |

**Severity heuristics by rule type:**
- Async client component → Critical (runtime error)
- Non-serializable props to client → Critical (runtime error)
- Raw `<img>` instead of `next/image` → High (perf/LCP impact)
- Missing `error.tsx` on data-fetching routes → High (unhandled errors)
- Missing `loading.tsx` → Medium (no loading state)
- Hardcoded metadata → Medium (SEO gap)
- Missing `sizes` on fill images → Low (suboptimal responsive)
- SELECT * → High (unnecessary data transfer)
- Cursors/row-by-row → Critical (performance antipattern)

### Step 6: Write Report

Write the report to **two locations**:
1. Output to conversation (immediate visibility)
2. Write to `.claude/canon-audit-report.md` in the target project (persists across sessions)

## Output Format

```markdown
## Canon Audit: [canon-name] → [target-path]

### Canon Loaded

| Metric | Value |
|--------|-------|
| Canon | [canon-name] |
| Source | [resolved path] |
| Topic files | N |
| Rules extracted | N (N grepable, N semantic) |
| Files scanned | N |
| Total source lines | N |

### Topic Scorecard

| # | Topic | Rules | Pass | Fail | Worst Severity |
|---|-------|-------|------|------|----------------|
| 1 | rsc-boundaries | N | N | N | Critical |
| 2 | image | N | N | N | High |
| 3 | metadata | N | N | N | Medium |
| ... | ... | ... | ... | ... | ... |

### Critical Findings

1. **[file:line]** [topic] — [rule name]
   - Rule: [what the canon says]
   - Found: [what the code does]
   - Fix: [specific fix]

### High Findings

1. **[file:line]** [topic] — [rule name]
   - Rule: [what the canon says]
   - Found: [what the code does]
   - Fix: [specific fix]

### Medium Findings

1. **[file:line]** [topic] — [description]

### Low Findings

1. **[file:line]** [topic] — [description]

### Passing Rules

Rules the codebase already satisfies (brief list):

- [topic] — [rule name] ✓
- [topic] — [rule name] ✓

### Summary

| Metric | Value |
|--------|-------|
| Total rules checked | N |
| Passing | N (N%) |
| Critical | N |
| High | N |
| Medium | N |
| Low | N |
| Compliance score | N% |
| Worst topic | [name] (N/N failing) |
| Best topic | [name] (N/N passing) |

### Remediation Priority

Ordered list of fixes by impact — what to fix first:

1. [topic] — [N critical + N high findings] — [1-line summary of what to do]
2. [topic] — [N findings] — [1-line summary]
3. ...

---
CANON_AUDIT_RESULT: [canon-name] — [N] rules, [N]% compliance, [N] critical, [N] high
CANON_AUDIT_DONE
```

## Rules

- **READ ONLY** — Do not edit any files in the target project
- **COMPLETE** — Read every canon file. Scan every source file in scope
- **SPECIFIC** — Cite file:line for every finding
- **BOTH LOCATIONS** — Output report to conversation AND write to `.claude/canon-audit-report.md`
- **PASSING RULES TOO** — Report what's working, not just what's broken
- **NO EXTERNAL TOOLS** — Claude analysis only. No Gemini or MCP tool calls
- **ACTIONABLE** — Every critical/high finding has a specific fix suggestion

## When to Use

- Audit a project after applying a new profile
- Baseline assessment before an improvement sprint
- Verify compliance after a round of fixes
- Compare compliance across projects

## When NOT to Use

- To fix code — use `/cleanup` or `/improve` with the report
- For general code quality — use `/code-scan`
- For AI smell detection — use `/ai-smell-scan`
- For external model review — use `/gemini-scan`
