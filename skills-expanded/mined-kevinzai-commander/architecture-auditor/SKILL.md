---
name: architecture-auditor
description: "Review cross-module boundaries, dependency direction, and architectural patterns. Use when 'audit architecture', 'check module boundaries', 'review dependencies', 'architecture review'."
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Architecture Auditor

Analyzes cross-module boundaries, dependency direction, and coupling patterns.

## What It Checks

### 1. Import Direction
- Are dependencies flowing in one direction? (no circular imports)
- Are lower-level modules importing from higher-level ones? (inversion)
- Run: `grep -rn "require\|import" --include="*.js" --include="*.ts" src/`

### 2. Module Cohesion
- Does each directory have a clear single responsibility?
- Are there files that import from 5+ other modules? (God modules)
- Are there modules with 0 imports from within the project? (dead code)

### 3. Boundary Violations
- Are database queries leaking outside the data layer?
- Are HTTP/request objects passed deep into business logic?
- Are environment variables accessed from more than 2-3 files?

### 4. Naming Consistency
- Do module names match their exports?
- Are similar patterns named consistently? (service vs handler vs controller)
- Is there a clear naming convention?

## Process

### Step 1: Map the Module Graph
```bash
# List all source files
find src/ lib/ commander/ -name "*.js" -o -name "*.ts" | head -50

# For each, extract imports
grep -rn "require\|from '" --include="*.js" src/ | head -100
```

### Step 2: Analyze Dependency Direction
Build a simple dependency matrix and identify:
- Circular dependencies
- Modules with highest fan-in (most depended on)
- Modules with highest fan-out (depends on most)

### Step 3: Report
```
Architecture Audit:
━━━━━━━━━━━━━━━━━

Modules: 18 files analyzed
Imports: 47 cross-module imports

Dependency Flow: OK — No circular imports
Highest Fan-In:  state.js (imported by 12 modules)
Highest Fan-Out: engine.js (imports 8 modules)

Boundary Issues: 2
  ! actions/linear.js directly calls HTTP (should go through integration layer)
  ! engine.js imports both UI (tui) and data (state) — consider mediator

Naming: OK — Consistent (all modules use .js, CJS require)

Score: 82/100 — Good with minor coupling issues
```
