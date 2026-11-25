---
name: parity-guard
description: Scan the workspace for parity-risk or over-scope wording before shipping an explanation.
user-invocable: true
---

# Parity Guard

Use this skill before making broad claims about what this workspace proves.

## Run

```bash
./.github/skills/parity-guard/check-parity-claims.sh .
```

## Intent

- detect wording that implies full parity with OMC or OMX
- detect wording that silently expands beyond the bounded VS Code workspace
- force a concrete fix before publishing or summarizing
