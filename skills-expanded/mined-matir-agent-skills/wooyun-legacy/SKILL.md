---
name: wooyun-legacy
description: Web vulnerability testing methodology distilled from 88,636 real-world cases.
allowed-tools:
- Read
- Grep
- Glob
- Bash
metadata:
  version: 0.2.0
  category: trail-of-bits
---
# WooYun Vulnerability Analysis

## Quick Start
```bash
# 1. Identify Input Sources (GET/POST/Cookie/Header)
# 2. Map Data Path to Sinks (SQL/HTML/Shell/Filesystem)
# 3. Apply Bypass Patterns for Filters (Encoding/Keywords)
```

## Workflow
1. **Mapping**: Trace data from input sources (GET, POST, Cookies, Headers) to output sinks.
2. **Detection**: Identify potential vulnerabilities using terminators (SQL) or event handlers (XSS).
3. **Bypass**: Apply encoding, keyword mutation, or parser discrepancy techniques to evade filters/WAFs.
4. **Verification**: Prove impact by extracting data, executing commands, or bypassing logic.
5. **Chaining**: Combine individual findings (e.g., Info Disclosure + IDOR) into critical attack paths.

## Rules & Constraints
- **RULE-1**: MUST obtain written authorization before testing any system.
- **RULE-2**: NEVER assume a WAF or framework provides absolute protection; test the application logic.
- **RULE-3**: Validate all business-critical logic server-side.
- **RULE-4**: Client-side validation is for UX, not security; bypass it during testing.

## When to Use
- Penetration testing web applications and APIs.
- Security code review (server-side and client-side).
- Assessing web application attack surface and trust boundaries.

## When NOT to Use
- Network infrastructure testing (firewalls, routers).
- Mobile application binary analysis.
- Cloud infrastructure misconfigurations (IAM, S3).

## References
- [Skill Manual](references/wooyun-legacy-manual.md)
- [SQL Injection Checklist](references/checklists/sql-injection-checklist.md)
- [XSS Checklist](references/checklists/xss-checklist.md)
- [Business Logic Checklist](references/checklists/logic-flaws-checklist.md)
