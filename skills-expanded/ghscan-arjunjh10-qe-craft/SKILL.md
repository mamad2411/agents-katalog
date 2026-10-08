---
name: qe-uat-gate
description: Release UAT and GO/NO-GO with guided copilot coaching. Call qe_intel_uat first (no API key). Use for release readiness, staging validation, or pre-deploy quality gate.
---

# QE UAT Gate

**Fixed mode:** `UAT`

## Start

1. Collect ticket + **RELEASE** block (rollback, monitoring).
2. Call **`qe_intel_uat`** with `feature`, `release`, optional context. Default: `output_tier: coach`.
3. Execute Phases A–D; deliver **GO / NO-GO / CONDITIONAL** in chat.
4. **`qe_intel_review`** before formal save.
5. Stakeholder HTML/JSON only on request → `output_tier: full` + [artifact-run.md](../shared/artifact-run.md).

Runbook: [intel-run.md](../shared/intel-run.md)

## Input template

```
FEATURE / TICKET:
<paste>

RELEASE:
- Type / Timeline / Rollback / Monitoring

OPTIONAL: API, SYSTEM, USER, RISKS, EXISTING COVERAGE, RELATED_REPOS
```
