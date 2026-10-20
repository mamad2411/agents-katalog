---
allowed-tools: Task, Read, Bash(wc:*, find:*, grep:*)
description: Show lean development metrics
model: claude-sonnet-4-20250514
---

## Lean Metrics Dashboard

Display metrics focused on code efficiency and simplicity.

### Code Metrics

Use bloat-detector and complexity-auditor agents to gather:

```bash
# Lines of code
find . -name "*.py" -o -name "*.js" -o -name "*.go" | xargs wc -l

# File count
find . -type f -name "*.py" -o -name "*.js" | wc -l

# Average file size
# Calculate average lines per file
```

### Complexity Metrics

Use complexity-auditor to report:
- Files exceeding complexity thresholds
- Functions > 20 lines
- Classes > 100 lines
- Nesting depth > 3

### Dependency Metrics

Use dependency-tracker to show:
```bash
# Python
poetry show --tree | head -20

# Node.js
npm list --depth=0

# Count direct dependencies
```

### Quality Trends

If git history available:
```bash
# Code growth over time
git log --pretty=format:"%h %ad" --date=short | head -10

# Recent reduction commits
git log --grep="refactor\|reduce\|remove\|simplify" --oneline | head -10
```

### Report Format

```
LEAN METRICS DASHBOARD
=====================

CODE SIZE
---------
Total LOC: X,XXX
Files: XXX
Avg lines/file: XX

COMPLEXITY
----------
High complexity files: X
Long functions: X
Deep nesting: X

DEPENDENCIES
------------
Direct: XX
Transitive: XXX
Total size: XX MB

TRENDS
------
Last week: -XXX lines (reduction!)
Refactor commits: XX
Complexity reduced: X files

RECOMMENDATIONS
---------------
1. Top file to simplify: ...
2. Dependencies to remove: ...
3. Dead code locations: ...
```

Focus on metrics that encourage code reduction and simplicity.
