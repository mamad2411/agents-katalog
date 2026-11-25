---
name: infra-kit.workflow.review
description: Make infra PRs reviewable: PR readiness checklist, traceability to ticket, and how to respond to review feedback.
---

# Review Loop (PR Readiness + Feedback)

Use this skill when you are preparing to open a pull request, requesting review, or responding to review feedback for infra changes (Terraform/Helm/GitHub Actions/platform config).

## Outcomes

- Ensure the PR tells reviewers: what changed, why, risk, rollout/rollback, and verification evidence
- Reduce back-and-forth by front-loading required context
- Provide a consistent process for responding to feedback without losing traceability to the ticket

## Where This Fits In The Flow

- Use after `infra-kit.workflow.verify` and before merge.
- Pair with `infra-kit.workflow.audit` for the cross-cutting safety gate.

## Output Rules

- Write PR-ready summary content into the work item:
  - `docs/infras-kit/work-items/<id>-<slug>/confluence.md` (can double as PR body)
  - and ensure `implementation-notes.md` contains verification evidence.

## PR Readiness Checklist

Confirm:

- The PR links to the ticket and matches the scope in `ticket.md`.
- Acceptance criteria are testable and mapped to:
  - tasks (`tasks.md`)
  - verification evidence (`implementation-notes.md` or `verification.md`)
- The PR description includes:
  - what changed and why
  - impact and risk
  - rollout steps
  - rollback steps and trigger
  - verification commands run + key results
- Any required manual steps (GitHub UI settings, approvals, secrets) are called out explicitly.

## Responding To Review Feedback

1. Categorize feedback:
   - correctness/safety blockers
   - clarity/docs requests
   - style/nits
2. For blockers, prioritize the smallest safe change and re-run verification.
3. Update artifacts when needed:
   - if scope changes, update `ticket.md` / `spec.md`
   - if the plan changes, update `plan.md` and reflect it in `tasks.md`
4. Record what changed in `implementation-notes.md` and add new evidence.
5. When you disagree, propose an alternative with explicit trade-offs and a way to verify.

## Guardrails

- Do not merge with unresolved `[NEEDS CLARIFICATION: ...]` unless explicitly accepted as a spike with `[ASSUMPTION: ...]`.
- Do not answer reviewers with speculation; either cite evidence or propose a test.
