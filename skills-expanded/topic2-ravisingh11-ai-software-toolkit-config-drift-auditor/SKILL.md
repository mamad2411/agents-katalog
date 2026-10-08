---
name: "config-drift-auditor"
description: "Compare application configuration across code, env samples, CI, and deployment assumptions to find dangerous drift. Use when a user asks for environment drift review, configuration audit, deployment config sanity check, or as part of $full-test-suite deep-audit work."
---

# Config Drift Auditor

Identify dangerous divergence between documented, coded, and deployed configuration assumptions.

## Focus Areas

- mismatched env variable names or defaults
- CI, local, and production config divergence
- secrets accidentally treated as optional or vice versa
- sample env files that mislead operators

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Severity rubric: `../_shared-project-ops/references/severity-rubric.md`
