---
name: ffuf-web-fuzzing
description: Expert penetration testing guidance for advanced ffuf scenarios, including authenticated fuzzing and complex parameter discovery.
allowed-tools:
- Bash
- Read
- Write
- Edit
- Grep
- Glob
metadata:
  version: 0.2.0
  category: tooling
---
# Ffuf Web Fuzzing

## Quick Start
```bash
ffuf -u http://target/FUZZ -w wordlist.txt
```

## Workflow
1. Define target URL and fuzzing points.
2. Select appropriate wordlist.
3. Execute ffuf and filter results by status code or size.

## Rules & Constraints
- Respect rate limits to avoid DOS.
- Only fuzz authorized targets.

## When to Use
- Directory and file discovery.
- Parameter fuzzing and subdomain enumeration.

## When NOT to Use
- Deep application logic testing.
- Testing that requires session persistence beyond simple headers.

## References
- [Skill Manual](references/ffuf-web-fuzzing-manual.md)
