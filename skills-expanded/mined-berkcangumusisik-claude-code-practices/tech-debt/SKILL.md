---
name: tech-debt
description: Audits the codebase for technical debt and produces a prioritized backlog
user-invocable: true
allowed-tools: Bash Grep Read Glob
effort: medium
---

## Technical Debt Audit

1. Find explicit debt markers:
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX\|TEMP\|DEPRECATED" src/ --include="*.ts" --include="*.js" | grep -v node_modules
```

2. Find implicit debt:
   - Files with cyclomatic complexity > 15
   - Files > 500 lines
   - Functions > 60 lines
   - Test coverage < 40%
   - Dependencies significantly outdated (major version behind)
   - Inconsistent patterns (multiple ways of doing the same thing)

3. Check for known anti-patterns:
```bash
# God objects / huge files
find src/ -name "*.ts" | xargs wc -l | sort -rn | head -10

# Any files
grep -rn ": any" src/ --include="*.ts" | wc -l
```

4. Score each debt item:
   - **Impact** (1-5): How much does this slow down development?
   - **Effort** (1-5): How hard to fix?
   - **Risk** (1-5): How likely to cause bugs?

5. Output a prioritized backlog (high impact × high risk, low effort first):
```markdown
| # | Issue | File | Impact | Risk | Effort | Priority |
|---|-------|------|--------|------|--------|----------|
| 1 | ...   | ...  | 5      | 4    | 2      | URGENT   |
```
