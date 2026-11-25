---
name: security-review
description: Identify and fix common security issues in application code.
metadata:
    triggers:
        - security review
        - find vulnerabilities
        - harden this code
    tags:
        - coding
        - security
    priority: 100
---

Run a lightweight secure coding review.

Checklist:
- Validate input handling and output encoding.
- Check authz/authn assumptions.
- Look for sensitive data leaks.
- Suggest concrete remediations with minimal code churn.
