---
name: skill-signing-verifier
description: >-
  Scaffold for verifying skill package signatures and provenance (planned).
  Use when designing supply-chain checks. NOT for live signing or key management.
user-invocable: false
license: MIT
metadata:
  author: wyattowalsh
  version: "0.1.0"
  internal: true
---

# Skill Signing Verifier

Later-tier scaffold for skill package signature verification.

**Scope:** Design placeholder only. Does not sign packages or manage private keys.

## Planned Workflow

1. Load packaged skill ZIP output from the repo packaging dry-run.
2. Verify signature manifest against maintainer trust store (TBD).
3. Report pass/fail without mutating installed harness skills.

## Validation Contract

```bash
uv run python skills/skill-signing-verifier/scripts/check.py
```

## Critical Rules

1. Never commit or print private signing keys.
2. Route live signing to maintainer-controlled release tooling when implemented.
3. Pair with security-scanner for executable-surface review until signing ships.
