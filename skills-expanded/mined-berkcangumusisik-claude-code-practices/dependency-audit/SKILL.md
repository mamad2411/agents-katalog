---
name: dependency-audit
description: Audits dependencies for known vulnerabilities and outdated packages
user-invocable: true
allowed-tools: Bash Read
effort: low
---

## Dependency Audit

1. Run security audit:
```bash
npm audit --json 2>/dev/null | head -100 \
  || bun audit 2>/dev/null \
  || pip audit 2>/dev/null \
  || cargo audit 2>/dev/null
```

2. Check for outdated packages:
```bash
npm outdated 2>/dev/null || bun outdated 2>/dev/null
```

3. Categorize findings:
   - **Critical/High CVEs** - list with CVE ID, affected version, fixed version
   - **Outdated major versions** - breaking changes to watch for
   - **Outdated minor/patch** - safe to update

4. For Critical/High vulnerabilities:
   - Can it be fixed with `npm audit fix`?
   - Is there a workaround if no fix exists?
   - Is the vulnerable code path even reachable in this project?

5. Generate an update plan:
```
Safe to auto-update now:  X packages
Requires manual review:   Y packages  
No fix available:         Z packages (mitigations: ...)
```

Ask before running any updates.
