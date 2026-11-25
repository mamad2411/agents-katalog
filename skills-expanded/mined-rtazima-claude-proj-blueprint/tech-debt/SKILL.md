---
name: tech-debt
description: "Technical debt identification and tracking. Activated when the user says \"tech debt\", \"technical debt\", \"cleanup backlog\", \"what needs fixing\", \"code health\", \"debt audit\", \"code quality scan\", or wants to systematically find and prioritize tech debt."
allowed tools: Read, Write, Edit, Grep, Glob, Bash
---

# Tech Debt Tracker

Systematically identify, catalog, and prioritize technical debt.
Not opinions — evidence-based assessment from the codebase itself.

## Rules

1. **Evidence over opinion** — every debt item must reference specific files, lines, or metrics
2. **Quantify impact** — estimate effort to fix and cost of NOT fixing
3. **Prioritize by risk** — debt near active features > debt in dormant code
4. **Check history** — use git log to find high-churn files (debt compounds where changes are frequent)
5. **Output to docs** — write report to `docs/architecture/tech-debt-report-{date}.md`
6. **Don't fix during audit** — catalog first, fix later (separate concerns)

## Debt Categories

### 1. Code quality debt
- [ ] `TODO` / `FIXME` / `HACK` / `XXX` comments without tracking
- [ ] `@ts-ignore` / `# type: ignore` / `nolint` suppressions
- [ ] `any` types (TypeScript) or untyped functions
- [ ] Functions > 50 lines or files > 500 lines
- [ ] Cyclomatic complexity hotspots (deeply nested logic)
- [ ] Copy-paste duplication (similar blocks in 3+ places)

### 2. Dependency debt
- [ ] Outdated dependencies (major versions behind)
- [ ] Dependencies with known vulnerabilities
- [ ] Deprecated packages still in use
- [ ] Unnecessary dependencies (installed but unused)
- [ ] Pinned to exact versions without update strategy

### 3. Test debt
- [ ] Source files without corresponding test files
- [ ] Tests that are skipped (`.skip`, `@pytest.mark.skip`, `xit`)
- [ ] Tests with no assertions (passing but testing nothing)
- [ ] Missing edge case coverage (only happy path tested)
- [ ] Flaky tests (pass/fail inconsistently)

### 4. Architecture debt
- [ ] Circular dependencies between modules
- [ ] God objects/files (one file does everything)
- [ ] Missing abstraction layers (business logic in controllers/handlers)
- [ ] Hardcoded values that should be configurable
- [ ] Deferred ADR decisions ("we'll decide later" still pending)

### 5. Documentation debt
- [ ] CLAUDE.md `[SPEC]` markers still unfilled
- [ ] Missing or outdated .env.example entries
- [ ] README project structure doesn't match actual files
- [ ] ADRs with status "proposed" that were never accepted/rejected
- [ ] Runbooks that reference outdated procedures

### 6. Infrastructure debt
- [ ] Manual deployment steps not automated
- [ ] Missing health checks or monitoring
- [ ] No alerting for critical failures
- [ ] Secrets not rotated (age > policy)
- [ ] No backup/restore verification

## Workflow

### Phase 1: Automated scan
Run these commands and capture results:

```bash
# TODOs and markers
grep -rn "TODO\|FIXME\|HACK\|XXX" src/ --include="*.[SPEC]" | wc -l

# Type suppressions
grep -rn "@ts-ignore\|@ts-expect-error\|# type: ignore\|nolint" src/ | wc -l

# High-churn files (top 10 most changed in last 3 months)
git log --since="3 months ago" --name-only --pretty=format: -- src/ | sort | uniq -c | sort -rn | head -10

# Large files
find src/ -name "*.[SPEC]" -exec wc -l {} + | sort -rn | head -10

# Test coverage gaps
# [SPEC] adapt to your test framework

# Outdated dependencies
# [SPEC] npm outdated / pip list --outdated / go list -m -u all

# Skipped tests
grep -rn "\.skip\|@skip\|xit\b\|xdescribe\b\|@pytest.mark.skip" src/ tests/ | wc -l
```

### Phase 2: Manual assessment
For each finding from Phase 1:
1. Is this actually debt? (Sometimes a TODO is tracked elsewhere, or a suppression is justified)
2. What's the impact? (Blocks feature work? Causes bugs? Just ugly?)
3. Where does it live? (Near active code or dormant?)

### Phase 3: Prioritize
Score each debt item:

| Factor | High (3) | Medium (2) | Low (1) |
|---|---|---|---|
| **Frequency** | Near code changed weekly | Changed monthly | Rarely touched |
| **Severity** | Causes bugs or blocks features | Slows development | Cosmetic |
| **Effort** | < 1 hour to fix | 1 day to fix | > 1 week to fix |

Priority = (Frequency + Severity) × (1/Effort)
High frequency + high severity + low effort = fix first.

### Phase 4: Report
Write `docs/architecture/tech-debt-report-{date}.md`:

```markdown
# Tech Debt Report — {date}

## Summary
- Total items: {N}
- Critical (fix now): {N}
- Important (fix soon): {N}
- Minor (fix when nearby): {N}

## Critical items
### 1. [Title]
- **Location**: file:line
- **Category**: [code quality | dependency | test | architecture | docs | infra]
- **Impact**: [what happens if we don't fix it]
- **Effort**: [estimate]
- **Evidence**: [specific finding]

## Important items
...

## Minor items
...

## Metrics
- TODOs/FIXMEs: {N}
- Type suppressions: {N}
- Skipped tests: {N}
- Files > 500 lines: {N}
- Dependencies outdated: {N}
```

## References
- `docs/architecture/` — past tech debt reports and ADRs
- `docs/specs/testing-strategy/` — coverage requirements
- `docs/specs/observability/` — monitoring gaps
- CLAUDE.md Gotchas — known issues
