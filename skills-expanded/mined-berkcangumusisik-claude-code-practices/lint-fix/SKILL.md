---
name: lint-fix
description: Fixes all auto-fixable lint errors and explains the non-auto-fixable ones
user-invocable: true
allowed-tools: Bash Read Edit
effort: low
---

## Fix Lint Errors

1. Run linter to see all issues:
```bash
npx eslint . --ext .ts,.tsx,.js,.jsx 2>&1 | head -80
# or
npx biome check . 2>&1 | head -80
# or
golangci-lint run 2>&1 | head -80
```

2. Apply auto-fix:
```bash
npx eslint . --ext .ts,.tsx,.js,.jsx --fix 2>&1
```

3. For remaining errors (non-auto-fixable):
   - Read each affected file
   - Understand why the rule exists
   - Apply the correct fix (not just suppressing with comments)

4. If a rule keeps firing and seems wrong for the project: note it but do NOT add `eslint-disable` comments - flag it for review instead.

5. Report: N auto-fixed, N manually fixed, N flagged for team review.
