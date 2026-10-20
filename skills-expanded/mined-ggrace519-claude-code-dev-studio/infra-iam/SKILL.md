---
name: infra-iam
description: Cloud IAM — roles, policies, SCPs / Organization Policies, workload identity, secrets, key management, zero-standing-privilege. Auto-invoked when designing IAM posture, auditing overly-broad permissions, or implementing break-glass procedures.
---

# Infra IAM

IAM is the blast radius. Every wildcard policy, every long-lived key, every
orphaned role is a pre-positioned incident — the work is structure, enforcement,
and continuous verification of who (and what) can do what.

## When to reach for this

- Designing the identity model: humans via SSO/SCIM, workloads via role
  federation (IRSA / Workload Identity / Managed Identity), third parties via
  external-ID role assumption
- Authoring or reviewing IAM policies, SCPs / Organization Policies
- Setting up secrets/KMS topology, rotation, or break-glass procedures
- Auditing for over-broad permissions, dormant identities, or static credentials

## Principles

1. **Deny by default; grant by exception.** Guardrails (SCPs / Org Policies)
   set the outer boundary; allow statements are scoped to exact actions and
   resource ARNs. Any wildcard ships with a written justification and an expiry
   date.
2. **Workload identity over keys.** IAM roles + IRSA / GCP Workload Identity /
   Azure Managed Identity everywhere. No access keys in env vars — and not in
   the secrets manager either; a stored static key is still a static key. Found
   one? Rotate it and replace the binding, in that order.
3. **Generate least-privilege from observed behavior.** Run IAM Access Analyzer
   / GCP IAM Recommender against 90 days of activity, then constrain to what was
   actually used. Hand-authored policies miss both ends: too broad on actions,
   too narrow on the conditions that matter.
4. **Break-glass is a ritual, not a door.** MFA-protected, approval-gated,
   time-boxed, session-recorded, auto-revoked, and every use reviewed. If it's
   used casually, it is no longer break-glass — it's a standing admin account.
5. **Access reviews run automatically on a quarterly cadence.** Every human,
   role, and service account has a named owner who re-attests. Dormant 90+ days
   → disabled; unclaimed → tombstoned. Evidence retained for audit.
6. **Detect drift continuously.** Preventive controls (SCPs) stop the known-bad
   in real time; detective scans (Prowler / Steampipe / cloud-custodian) run
   daily. Every finding gets a ticket with a severity SLA; unresolved findings
   escalate, not expire.

## IAM posture review checklist

- [ ] No IAM users with long-lived access keys (workloads federated, humans via SSO)
- [ ] Root / org-admin accounts: hardware MFA, no API keys, usage alarmed
- [ ] SCP / Org Policy baseline: deny region sprawl, deny disabling audit logs
      (CloudTrail / audit sink), deny public buckets, deny leaving the org
- [ ] No `Action: "*"` or `Resource: "*"` outside justified, expiring exceptions
- [ ] Cross-account third-party roles use external ID and least-privilege scope
- [ ] KMS: per-domain keys, key policies separate admins from users, rotation on
- [ ] Secrets: central manager, rotation wired, no secrets in repos / images /
      task definitions (verified by scanner in CI)
- [ ] Break-glass: documented, tested in the last 6 months, alerts on use
- [ ] Quarterly access review evidence exists for the last cycle

## Pitfalls

- Treating the secrets manager as the fix while it stores never-rotated static
  keys — the binding, not the storage, is the problem
- Permission boundaries confused with SCPs (boundary caps a principal; SCP caps
  an account) — guardrails built on the wrong one don't hold
- `iam:PassRole` left broad — it quietly converts a narrow role into privilege
  escalation via any service that runs as another role
- Dormant-identity cleanup that only covers humans; orphaned service accounts
  and CI deploy roles outlive their projects
- Break-glass accounts excluded from logging "to keep them independent" —
  independence means separate auth path, never blind spots

---
*Related: `infra-networking` (segmentation is the other half of blast radius),
`infra-k8s` (pod-level RBAC and service-account binding), `infra-dr-backup`
(separate-credential backup isolation) · domain agent: `infra-architect` ·
output/ADR format: `playbook-conventions`*
