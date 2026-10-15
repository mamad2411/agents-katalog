---
name: analyst-stakeholder-feedback
description: >-
  Analyst checklist for ad-hoc stakeholder or user feedback: triage symptoms, map to code areas,
  assign Backend/Frontend/SDET/DevOps, and record in evaluation-report without requiring a
  matching phase-plan row.
---

# Analyst: stakeholder feedback triage

Use when **user or stakeholder feedback** arrives outside a formal **phase-plan** task (bugs, “nothing works”, auth, empty data).

## Main agent

The **Analyst Orchestrator** ([`.cursor/agents/analyst-orchestrator.md`](../../agents/analyst-orchestrator.md)) coordinates. It **assigns** specialists.

## Quick symptom → owner

| Symptom | Likely area | Subagent |
|--------|-------------|----------|
| Auth / login / session | Frontend auth layer | `react-implementer.md` |
| API errors / CORS / 401 | API client + server | Frontend first; **Backend** if server-side |
| Empty data / wrong routing | UI or API contract | **Frontend** + **Backend** as needed |
| Deployed-only failures | Cloud resources | `sdet-validator.md` + `diagnose-deployed-apps` |
| E2E regression | `tests/e2e` | `sdet-validator.md` |
| CI/CD (GitHub Actions) | **git@github.com:kmabery/pipeline-eval.git** — **ci-cd-deploy.yml** | `devops-github-actions-operator.md` |

## Mandatory redeploy after triage fixes

If triage produces **deployable** changes:

1. **Commit and push** to **`main`** on **`git@github.com:kmabery/pipeline-eval.git`** (SSH) — see [`.cursor/rules/github-remote-ssh.mdc`](../../rules/github-remote-ssh.mdc).
2. **DevOps** ensures/triggers **ci-cd-deploy.yml** (see `devops-github-actions-ci-aws`).
3. Record **run ID** (GitHub Actions) in `docs/evaluation-report.md` (index), `docs/phase-evidence/phase-MM-dd-yyyy-HHmmss-<n>.json` when applicable, or the session handoff.

Pure **documentation** updates with no artifact change may skip redeploy; state that explicitly.

## Evidence

- Summarize in **`docs/evaluation-report.md`** when feedback is addressed or deferred.
- Full phase **closure** still uses [`.cursor/skills/analyst-evaluation-report-evidence/SKILL.md`](../analyst-evaluation-report-evidence/SKILL.md) and **phase-closure-gate**.
