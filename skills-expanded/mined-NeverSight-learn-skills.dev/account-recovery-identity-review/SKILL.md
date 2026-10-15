---
name: account-recovery-identity-review
description: Design and audit account recovery, password reset, MFA reset, passkey recovery, SSO fallback, device change, email/phone change, account ownership proof, support escalation, anti-takeover controls, lockouts, notifications, and recovery analytics. Use when users can lose access or attackers can exploit recovery to take over an account.
---

# Account Recovery Identity Review

Use this skill to convert a account recovery, identity proof, MFA reset, support escalation, anti-takeover risk, and user access restoration question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify account type, authentication factors, recovery factor, asset sensitivity, abuse history, support role, and lockout cost.
2. Read `references/account-recovery-identity-patterns.md`.
3. Classify the recovery path: password reset, MFA reset, passkey loss, SSO fallback, email/phone change, device loss, admin recovery, or support-assisted proof.
4. Define proof requirements, friction ladder, rate limits, notifications, session invalidation, audit logs, and escalation boundaries.
5. Produce recovery state machine, risk decision table, event schema, support policy, and abuse-monitoring checklist.

## Guardrails

- Do not let support override authentication without evidence, audit, and privilege boundaries.
- Do not expose whether an email, phone, tenant, or account exists through recovery copy or timing.
- Do not remove all factors at once for high-value accounts without cooldown, notification, or admin review.
- Do not punish legitimate lockout users with permanent loss when safer step-up or appeal paths are possible.

## Output format

```text
Recovery context:
Account type / factor lost / asset sensitivity:

Recovery plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Proof and controls:
- <item> -> <policy, metric, edge case, support note>

Escalation and abuse response:
- <trigger> -> <action, communication, owner>
```
