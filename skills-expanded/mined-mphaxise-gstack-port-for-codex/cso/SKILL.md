---
name: cso
description: Security audit workflow for Codex. Use when a repo, feature, or system should be reviewed for concrete security risks before or after shipping.
---

# CSO

Use this skill when the user wants a serious security pass instead of generic best-practices advice.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Identify the audit scope:
   - application surface
   - infrastructure or CI
   - secrets and auth
   - dependencies and supply chain
2. Review the relevant risks using concrete lenses:
   - trust boundaries
   - data exposure
   - auth and authorization
   - secret handling
   - unsafe defaults
   - exploitable deployment gaps
3. Report only the issues that matter, with a realistic exploit scenario when possible.

## Guardrails

- Do not flood the user with low-confidence noise.
- Distinguish verified issues, likely issues, and open questions.
- Prefer concrete exploit paths over checklist theater.
