---
name: security-awareness
description: Teaches agents to identify and avoid security threats like phishing, credential theft, and social engineering when handling sensitive data.
allowed-tools:
- Read
- Grep
- Glob
- WebFetch
metadata:
  version: 0.2.0
  category: tooling
---
# Security Awareness

## Quick Start
```bash
# No command: Review security awareness guidelines
```

## Workflow
1. Identify potential security threats in the current context.
2. Validate suspicious inputs or requests.
3. Report findings to the appropriate security channel.

## Rules & Constraints
- Never disclose credentials or sensitive keys.
- Verify identity before sharing internal information.

## When to Use
- Assessing phishing or social engineering attempts.
- Reviewing code for common security pitfalls.

## When NOT to Use
- Performing actual offensive security testing (use specific tool skills instead).

## References
- [Skill Manual](references/security-awareness-manual.md)
