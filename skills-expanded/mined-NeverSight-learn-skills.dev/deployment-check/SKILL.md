---
name: deployment-check
description: Use before deployment or release validation; checks configuration, build, runtime assumptions, incidents, rollback readiness, and human approval boundaries.
---

# Purpose

Reusable workflow for deployment readiness checks.

# Required Knowledge

- `ai-workspace/70-knowledge/company/`
- `ai-workspace/70-knowledge/teams/{team}/`
- `ai-workspace/70-knowledge/systems/{system}/`
- `ai-workspace/70-knowledge/incidents/`

# Inputs

- target system
- environment
- deployment command or checklist
- rollback method
- verification commands

# Workflow

1. Load required system and team knowledge.
2. Review related incidents.
3. Confirm environment and target.
4. Check build/test status.
5. Check configuration and secret handling without exposing secret values.
6. Check migration or destructive operation requirements.
7. Confirm rollback path.
8. Verify deployment readiness.
9. Request human approval for risky operations.

# Safety Rules

- Do not deploy to production without explicit human approval.
- Do not run migrations without explicit human approval.
- Do not print secrets.
- Do not overwrite production configuration.
- Do not proceed if rollback is unknown for high-risk changes.

# Incident References

- Check incidents for failed deploys, configuration drift, rollback failures, timeout loops, and data migration issues.

# Output

- readiness summary
- blockers
- verification result
- required approvals

# Verification

- Build/test commands reviewed or run.
- Risky operations identified.
- Rollback path documented.
