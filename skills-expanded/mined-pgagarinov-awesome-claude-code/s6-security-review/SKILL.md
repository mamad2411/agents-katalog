---
name: s6-security-review
description: Run a security-focused code review identifying vulnerabilities
context: fork
agent: a1-security-reviewer
argument-hint: "[file-or-directory]"
---

# S6 — Security Review

Perform a security-focused review of: **$ARGUMENTS**

If no target is specified, review the entire codebase.

## Review Checklist

### Critical — Check for These First

1. **Hardcoded Secrets**: API keys, tokens, passwords in source code
2. **Injection Vulnerabilities**: SQL injection, command injection, code injection
3. **Insecure Authentication**: Weak comparison, missing rate limiting, plain-text passwords
4. **Input Validation Gaps**: Unvalidated user input passed to sensitive operations

### High Priority

5. **Unsafe Deserialization**: `pickle.loads`, `yaml.load` without SafeLoader
6. **Path Traversal**: User input in file paths without sanitization
7. **Information Disclosure**: Stack traces, debug info, verbose error messages
8. **Missing Access Control**: Operations without authorization checks

### Medium Priority

9. **Timing Attacks**: String comparison of secrets using `==` instead of `hmac.compare_digest`
10. **Dependency Issues**: Known vulnerable packages, unpinned versions

## Report Format

For each finding, report:

```
[SEVERITY: CRITICAL/HIGH/MEDIUM/LOW] Title
  File: file_path:line_number
  Issue: What the vulnerability is
  Impact: What an attacker could do
  Fix: How to remediate
```

End with a severity summary and prioritized fix list.
