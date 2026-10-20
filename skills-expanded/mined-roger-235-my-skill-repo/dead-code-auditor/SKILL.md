---
name: dead-code-auditor
description: "Scans codebase for unused exports, zombie functions, unreachable code paths, and unused imports. Produces a prioritized removal list with file:line references and estimated cleanup impact. Different from tech-debt-tracker (which scores general debt). Triggers: dead code, unused code, zombie functions, unused imports, unreachable code, find unused, 死碼, 未使用的程式碼."
metadata:
  category: dev
---

## Purpose

Surface code that exists but is never executed or referenced. Dead code increases maintenance burden, confuses readers, and masks real complexity. This skill finds it and ranks it by removal impact.

## Trigger

Apply when:
- "dead code", "unused code", "zombie functions", "unreachable code"
- "find unused exports", "unused imports", "死碼", "未使用的程式碼"
- Pre-cleanup sprint, post-migration cleanup, repository health audit

Do NOT trigger for:
- General code quality analysis — use `code-quality` instead
- Technical debt prioritization — use `tech-debt-tracker` instead
- Dependency vulnerabilities — use `dependency-auditor` instead

## Prerequisites

- Codebase accessible in current working directory
- Language detection: reads `package.json`, `pyproject.toml`, `go.mod`, or file extensions to determine language

## Steps

### Step 1 — Detect Language and Tooling

| Language | Native dead-code tools |
|----------|----------------------|
| TypeScript/JS | `ts-unused-exports`, `depcheck`, ESLint `no-unused-vars` |
| Python | `vulture`, `autoflake --check`, pylint unused imports |
| Go | `go vet`, `staticcheck ./...` |
| Java/Kotlin | IDE inspection, `PMD UnusedCode` ruleset |
| Ruby | `debride` |

If tools are available, run them first. If not, proceed with structural analysis (Step 2).

### Step 2 — Unused Imports / Variables

Scan each source file for:

**TypeScript/JavaScript:**
```bash
# ESLint no-unused-vars (if configured)
npx eslint --rule '{"no-unused-vars": "error"}' --ext .ts,.js src/ 2>&1 | grep "no-unused-vars"

# Unused exports across the project
npx ts-unused-exports tsconfig.json 2>/dev/null | head -50
```

**Python:**
```bash
python3 -m vulture . --min-confidence 80 2>/dev/null | head -50
```

**Go:**
```bash
staticcheck ./... 2>/dev/null | grep "unused"
```

### Step 3 — Zombie Functions and Classes

Look for exported symbols with zero internal usages. Criteria:
- Function/class exported but never imported in any other file
- Function defined but called 0 times within the codebase
- Interface/type defined but never referenced

Search pattern (language-agnostic heuristic):
```bash
# For each exported symbol, count references across the codebase
# Flag any with count == 1 (only the definition itself)
```

Prioritize by: public API surface (exported) > private helpers > test utilities.

### Step 4 — Unreachable Code Paths

Identify:
- Code after unconditional `return`/`throw`/`exit`
- Conditions that can never be true (e.g., `if (false)`, `if (x > 10 && x < 5)`)
- `default` branches in exhaustive switches
- Catch blocks that catch exceptions that cannot be thrown

Flag these as **SAFE_DELETE** — removing them has zero behavior impact.

### Step 5 — Unused Dependencies

```bash
# Node.js
npx depcheck 2>/dev/null

# Python
pip-autoremove --list 2>/dev/null || python3 -m pip check
```

Flag packages listed in `package.json`/`requirements.txt` with no import in source files.

### Step 6 — Rank and Output

Rank findings by removal impact:

| Priority | Type | Why High Impact |
|----------|------|-----------------|
| P1 | Unused npm/pip packages | Reduces bundle size + attack surface |
| P1 | SAFE_DELETE unreachable blocks | Zero risk, immediate clarity gain |
| P2 | Unused exported functions (public API) | Reduces maintenance contract |
| P3 | Unused private functions | Low blast radius |
| P4 | Unused imports | Minor cleanup |

## Output Format

```
╔══════════════════════════════════════════════════╗
║  DEAD CODE AUDIT                                 ║
║  Files scanned: <n>   Findings: <n>             ║
║  Est. lines removable: ~<n>                      ║
╚══════════════════════════════════════════════════╝

P1 — Unused Dependencies (remove immediately)
  • lodash — listed in package.json, 0 imports found
  • moment — superseded by date-fns (already installed)

P1 — Unreachable Code (SAFE_DELETE)
  • src/utils/format.ts:45 — code after unconditional return
  • src/api/orders.ts:112 — catch(e) block, exception never thrown here

P2 — Zombie Exported Functions
  • src/helpers/crypto.ts:23 — generateLegacyHash() — exported, 0 callers
  • src/models/user.ts:88 — toXML() — exported, 0 callers

P3 — Unused Private Functions
  • src/services/email.ts:67 — _buildMimeHeader() — defined, never called

P4 — Unused Imports
  • src/components/Button.tsx:1 — import { memo } from 'react' — memo unused
  • src/api/auth.ts:3 — import bcrypt — bcrypt unused in this file

Total removable: ~180 lines across 8 files
```

## Rules

### Must
- Verify each finding before reporting — do not flag symbols used via dynamic access (e.g., `obj[key]`, `require(variable)`)
- Check test files separately — test utilities are not dead even if not called from production code
- Mark `SAFE_DELETE` only for code provably unreachable at compile/parse time
- Report estimated line count reduction for each category

### Never
- Never auto-delete findings — this skill reports only; deletion requires user confirmation
- Never flag symbols used via reflection, serialization, or magic strings as dead
- Never report `@deprecated` functions as dead code if they are still called
- Never conflate "never tested" with "dead" — untested code may still be live

## Examples

### Good Example

```
P1 — Unused Dependency: `xml2js` in package.json
  • 0 imports found across 47 source files
  • Safe to remove: npm uninstall xml2js
  • Est. bundle reduction: ~180KB

P2 — Zombie Export: src/utils/legacy-auth.ts:12
  • generateMD5Token() exported but 0 callers in codebase
  • Introduced in commit abc123 (2024-01-15), never used after JWT migration
```

### Bad Example

```
Found unused code everywhere. You should clean up your codebase.
```

> Why this is bad: No file:line references, no prioritization, no actionable removal instructions. Impossible to act on.
