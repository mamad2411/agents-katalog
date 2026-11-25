---
name: complexity-report
description: Reports cyclomatic complexity hotspots and refactoring suggestions
argument-hint: [directory]
user-invocable: true
allowed-tools: Bash Grep Read
effort: medium
---

## Complexity Report

Directory: **$1** (or `src/` if not specified)

1. Find complex functions manually (no external tool needed):
```bash
# Functions longer than 50 lines
grep -n "^function \|^  [a-z].*(.*) {" ${1:-src}/**/*.ts 2>/dev/null | head -30
```

Read the top 10 largest files and functions.

2. For each file over 300 lines or function over 40 lines:
   - Count the number of if/else/switch/for/while/try blocks (= cyclomatic complexity)
   - Note the nesting depth
   - Identify the "complexity source"

3. Rank by complexity and report:

```
Top 5 Complexity Hotspots:
  src/auth/middleware.ts:handleRequest()   CC: 18  Lines: 87
  src/api/router.ts:routeRequest()         CC: 14  Lines: 120
  ...

Refactoring recommendations:
  1. handleRequest() - extract 3 auth validation blocks into separate functions
  2. ...
```

4. Offer to refactor the top offender.
