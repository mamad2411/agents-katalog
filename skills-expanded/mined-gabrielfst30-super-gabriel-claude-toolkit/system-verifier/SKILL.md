---
name: system-verifier
description: Full architectural audit of the codebase. Runs automated checks (type-check, lint) and launches parallel architecture-guardian agents per domain to verify code quality and pattern compliance across the entire project.
user-invocable: true
allowed-tools: Read, Grep, Glob, Agent, Bash(pnpm type-check:*), Bash(pnpm lint:*), Bash(npm run type-check:*), Bash(npm run lint:*)
---

# /system-verifier

Full architectural readiness audit across all project domains.

## Trigger

User runs `/system-verifier`.

## Flow

### Step 1: Read project structure
Read `CLAUDE.md` to understand:
- The project's module/domain breakdown
- Which directories contain feature code
- The type-check and lint commands

### Step 2: Run automated checks

Run the project's type-check command:
```bash
pnpm type-check   # or npm run type-check
```

Run the project's lint command:
```bash
pnpm lint   # or npm run lint
```

Capture all output. Continue even if these fail — include results in final report.

### Step 3: Identify domains

Based on the project structure from `CLAUDE.md`, identify the main domains
(feature modules, layers, or directories) to audit independently.

Example domain breakdown for a feature-module project:
- `src/feature/auth/`
- `src/feature/[module-a]/`
- `src/feature/[module-b]/`
- `src/lib/` (infrastructure layer)
- `src/components/` (component library)

### Step 4: Launch parallel domain agents

For each domain, spawn an `architecture-guardian` agent simultaneously:

```
Agent(
  subagent_type: "architecture-guardian",
  prompt: "Audit the [domain-name] domain in [path].
           Read CLAUDE.md first for project conventions.
           Report all violations, warnings, and passing patterns."
)
```

All domain agents run in parallel.

### Step 5: Aggregate results

Combine automated check output + all agent reports into a unified report.

## Output

```
SYSTEM VERIFICATION REPORT
===========================

Automated Checks:
  TypeScript  → PASSED (0 errors)
  ESLint      → PASSED (0 warnings)

Domain Audits:
  [domain-a]  ✅ COMPLIANT
  [domain-b]  ⚠️  2 warnings
  [domain-c]  ✅ COMPLIANT

Issues:
  1. src/[path]/file.ts:42 — [description of violation]
  2. src/[path]/other.ts:18 — [description of violation]

OVERALL: ⚠️ WARNINGS — N issues require attention
```

If fully compliant:
```
SYSTEM VERIFICATION: ✅ ALL DOMAINS COMPLIANT
TypeScript: 0 errors | Lint: 0 warnings
```

## Success Criteria
- [ ] All domains audited by architecture-guardian
- [ ] Automated checks executed
- [ ] All violations reported with file:line references
