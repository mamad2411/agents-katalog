---
name: QA
description: Diff-aware QA routing — analyze what changed and route to the right test strategy. USE WHEN qa, what should I test, check my changes, run qa, review changes, diff analysis, what broke, smoke test, test routing.
---

# QA

Diff-aware quality assurance. Analyzes git diffs, classifies file changes by category (style, component, API, data, config, test, docs, infra), and routes to the appropriate test/validation strategy. Smart QA — test what matters, skip what doesn't.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/QA/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the QA skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **QA** skill to ACTION...
   ```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Analyze** | "/qa", "what should I test", "check my changes", "diff analysis" | `Workflows/Analyze.md` |
| **QuickCheck** | "quick check", "smoke test", "quick qa", "sanity check" | `Workflows/QuickCheck.md` |

## Architecture

**Two-stage process:**
1. **Script** (`Tools/DiffAnalyzer.ts`) — deterministic diff parsing, file classification, route generation
2. **AI orchestration** — interpret routes, execute checks, report results

## Tool Reference

**Path:** `~/.claude/skills/QA/Tools/DiffAnalyzer.ts`

**Usage:**
```bash
# Diff against main (default)
bun ~/.claude/skills/QA/Tools/DiffAnalyzer.ts

# Diff against specific branch
bun ~/.claude/skills/QA/Tools/DiffAnalyzer.ts --branch develop

# Staged changes only
bun ~/.claude/skills/QA/Tools/DiffAnalyzer.ts --staged

# Explicit file list
bun ~/.claude/skills/QA/Tools/DiffAnalyzer.ts --files "src/api.ts,src/styles.css"
```

**Output:** JSON with file classifications, diff stats, and QA routing recommendations.

## File Categories

| Category | Matches | QA Strategy |
|----------|---------|-------------|
| **style** | CSS, SCSS, Tailwind config | Visual regression — screenshot before/after |
| **component** | TSX, JSX, Vue, Svelte | Component render check — verify UI |
| **api** | Route handlers, controllers, middleware | Endpoint validation — test request/response |
| **data** | Migrations, schemas, seeds, Prisma | Migration safety — check destructive ops |
| **config** | JSON, YAML, TOML, env files | Config validation — syntax and required fields |
| **test** | *.test.*, *.spec.*, __tests__ | Test-only — run modified tests |
| **docs** | Markdown, README, CHANGELOG | Documentation review — link and accuracy check |
| **infra** | Dockerfile, CI/CD, deploy configs | Infrastructure review — verify deploy config |

## Diff Size Routing

| Size | Lines Changed | Strategy |
|------|--------------|----------|
| **Small** | <50 | Quick smoke test — focused verification |
| **Medium** | 50-199 | Standard testing — run related tests |
| **Large** | 200+ | Full suite — comprehensive check recommended |

## Examples

**Example 1: Before shipping a feature**
```
User: "/qa"
→ Runs DiffAnalyzer.ts against main
→ "12 files changed: 3 component, 2 api, 1 style, 6 test"
→ Routes: visual check for style, endpoint validation for API, run component tests
→ Executes each route, reports results
```

**Example 2: Quick sanity check**
```
User: "quick check"
→ Runs DiffAnalyzer.ts --staged
→ "2 files changed: 1 config, 1 api (small diff)"
→ Quick smoke test: validate config syntax, curl API endpoint
```

**Example 3: Explicit files**
```
User: "qa these files: src/auth.ts, src/auth.test.ts"
→ Runs DiffAnalyzer.ts --files "src/auth.ts,src/auth.test.ts"
→ Routes: API validation for auth.ts, run auth.test.ts
```

## Integration

- **Ship skill**: Run `/qa` before `/ship` to verify changes
- **Evals**: QA routes map to Evals grader types (code_based for config, llm_rubric for docs)
- **Browser**: Visual regression checks use Browser skill for screenshots
