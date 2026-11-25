---
name: secret-scan
description: Scans the codebase for accidentally committed secrets, tokens, and credentials
user-invocable: true
allowed-tools: Bash Grep Read
effort: low
---

## Secret Scanner

```bash
# Common secret patterns
grep -rn \
  -e "password\s*=\s*['\"][^'\"]\+" \
  -e "secret\s*=\s*['\"][^'\"]\+" \
  -e "api_key\s*=\s*['\"][^'\"]\+" \
  -e "token\s*=\s*['\"][^'\"]\+" \
  -e "sk-[a-zA-Z0-9]\{20,\}" \
  -e "ghp_[a-zA-Z0-9]\{36\}" \
  -e "AKIA[0-9A-Z]\{16\}" \
  -e "-----BEGIN.*PRIVATE KEY-----" \
  --include="*.ts" --include="*.js" --include="*.env*" --include="*.json" \
  --exclude-dir=node_modules --exclude-dir=dist \
  . 2>/dev/null | grep -v "\.test\." | grep -v "example\|placeholder\|your_key_here"
```

Also check:
```bash
git log --all --full-history -- "*.env" | head -10
git log --diff-filter=D --summary | grep ".env" | head -10
```

For each finding:
- Show file, line, and the leaked value (partially redacted)
- Confirm if it's a real secret or a false positive
- If real: advise rotating the credential immediately, then removing from git history

**Note:** Rotate first, remove from history second - a removed commit is not the same as a revoked token.
