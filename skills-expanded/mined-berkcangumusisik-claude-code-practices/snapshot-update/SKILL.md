---
name: snapshot-update
description: Reviews and selectively updates outdated Jest/Vitest snapshots
user-invocable: true
allowed-tools: Bash Read Edit
effort: low
---

## Update Snapshots

1. Find outdated snapshots:
```bash
npx jest --updateSnapshot --dry-run 2>/dev/null || bun test --update-snapshots --dry-run 2>/dev/null || echo "Run manually"
```

2. For each snapshot that would change:
   - Show the diff (old vs new)
   - Explain what component/output changed
   - Classify: intentional UI change vs potential regression

3. Ask the user:
   - Update all? (if all changes are clearly intentional)
   - Review each one? (if any look suspicious)

4. On confirmation, update snapshots:
```bash
npx jest --updateSnapshot
```

5. List what was updated and flag any that looked suspicious for manual review.
