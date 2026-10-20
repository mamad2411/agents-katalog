---
agent: orchestrator
description: "Resume an interrupted Enterprise Landing Zone APEX workflow from the last completed step"
---

# Resume Workflow

Resume a previously interrupted APEX workflow session for an Enterprise Landing Zone deployment.

## Process

1. **Primary**: Run `alz-recall show {customer} --json` to restore full session state —
   current step, decisions (region, iac_tool, complexity), artifact inventory
2. **Fallback**: If `alz-recall` returns no customer, check `agent-output/{customer}/00-handoff.md`
   for completed-steps checklist and key decisions
3. **Tertiary**: If both are absent, scan existing artifacts:
   - `00-assessment-*` → Step 0 done (brownfield)
   - `01-requirements.md` → Step 1 done
   - `02-architecture-assessment.md` → Step 2 done
   - `03-design-*` → Step 3 done
   - `04-governance-constraints.*` → Step 3.5 done
   - `04-implementation-plan.md` → Step 4 done
   - IaC files in `infra/` → Step 5 done
   - `06-deployment-summary.md` → Step 6 done
   - `07-*.md` → Step 7 done
   - `08-compliance-report.md` → Step 8 active (monitoring)
   - `09-remediation-log.md` → Step 9 active (remediation)
4. Check platform LZ deployment state from `alz-recall show {customer} --json` →
   `platform_landing_zones` section
5. Check GitHub Actions run status for recent `2-platform-deploy.yml` or `3-app-deploy.yml` runs

## Skills to reference

Read `.github/skills/session-resume/SKILL.md` for full recovery procedure.

## Ask the user

"I found state showing Step {N} complete. Ready to continue with Step {N+1}?"
