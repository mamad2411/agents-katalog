---
name: azure-pim-eligible-roles
description: >
  Microsoft Entra Privileged Identity Management (PIM) for owned tenants: eligible
  vs permanent Azure RBAC and directory roles, activation MFA/approval, access
  reviews, and just-in-time admin. Use when removing standing Owner/User Access
  Administrator privileges or configuring PIM policies — not for privilege escalation
  outside authorization.
---

# Azure PIM Eligible Roles

## Scope And Authorization

- **In scope:** Entra ID P2/Governance features and Azure RBAC on subscriptions you are authorized to govern.
- **Out of scope:** Activating roles to access data beyond job need; weakening approval requirements covertly.
- PIM misconfiguration can lock out admins or allow standing privilege — test carefully.
- Pair AWS analog concepts with `aws-sso-permission-sets`; use `code-quality-standards` for automation.

## When To Use

- Converting permanent Owner/Contributor to **eligible** assignments.
- Configuring activation requirements (MFA, justification, approval, max duration).
- Access reviews for privileged roles.
- Investigating who can elevate to subscription Owner.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Managed identity for apps | `azure-managed-identity-basics` |
| NSG network controls | `azure-nsg-review` |
| AWS Identity Center permission sets | `aws-sso-permission-sets` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Eligible | User may activate JIT; not standing |
| Active/permanent | Standing privilege — minimize |
| Azure roles | Subscription/MG/RG RBAC via PIM |
| Directory roles | Global Admin, etc. via Entra PIM |
| Controls | MFA, ticket, approval, duration, notifications |
| Tooling | Entra portal PIM, Microsoft Graph, Azure RBAC APIs |

## Workflow

### 1. Confirm scope and success criteria

1. Tenant licensing (P2/Governance), scopes (MG/sub), privileged roles in scope, authorization.
2. Success: no standing human Owner on prod; activation works within SLA; approvals logged.
3. Break-glass accounts: separate, monitored, permanent only if policy requires, offline creds vaulted.

### 2. Inventory privileged assignments

```bash
az account show
az role assignment list --include-classic-administrators -o table
az role assignment list --role "Owner" --all -o table
az role assignment list --role "User Access Administrator" --all -o table
# Entra directory roles: use Microsoft Graph / portal PIM blades
```

1. List permanent vs already-eligible PIM assignments in portal/Graph.
2. Map each privileged human to manager and business need.
3. Identify service principals with Owner — often should not be PIM-eligible humans pattern.

### 3. Baseline policy

| Role | Max activation | Approval | MFA |
| --- | --- | --- | --- |
| Subscription Owner | 1–4 hours | Yes (security/platform) | Required |
| Contributor prod | 4–8 hours | Optional / high risk yes | Required |
| Reader | Standing ok | n/a | n/a |
| Global Admin | 1 hour | Yes dual control | Required |

### 4. Convert to eligible and configure PIM

1. In Entra PIM: Azure resources → subscription/MG → roles → add **eligible** assignment for group.
2. Remove permanent assignment after eligible tested.
3. Role settings: require MFA, justification, ticket number, approval workflow, notification to security.
4. Prefer **group-based** eligible membership driven by IGA.
5. Graph API / automation for bulk conversions where available — validate with Microsoft docs for current endpoints.

```bash
# After PIM activation, validate elevated access
az login
az account show
az role assignment list --assignee "$(az ad signed-in-user show --query id -o tsv)" -o table
```

### 5. Verify with evidence

1. User without activation cannot write prod RBAC-protected actions.
2. Activation request → approval → temporary access → auto expiry.
3. Audit logs show activation events in Entra and Azure Activity Log.
4. Break-glass login test on schedule (controlled).

### 6. Observe and harden

1. Alerts on permanent Owner assignments created outside PIM.
2. Weekly report of activations; anomaly (off-hours mass activations).
3. Access reviews quarterly for eligible members of admin groups.

### 7. Hand off

1. PIM role setting catalog per role.
2. Approver roster and backup approvers.
3. Runbook for emergency elevation if PIM unavailable.

## Standing vs Eligible

| Pattern | When acceptable |
| --- | --- |
| Standing Reader | Broad visibility roles with low risk |
| Eligible Owner | Human admin of last resort |
| Standing app MI Contributor | Avoid — prefer scoped deploy roles |
| Break-glass permanent | Tiny set, monitored, never daily use |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Humans | Eligible + MFA + approval | Permanent Owner for all eng |
| Groups | Role-assignable groups + IGA | Per-user eligible sprawl |
| Duration | Short for Owner | 24h Owner default |
| Break-glass | Monitored rare accounts | Shared “globaladmin” mailbox password |
| Reviews | Scheduled access reviews | Eligible forever without review |

## Output Checklist

- [ ] Permanent privileged humans inventoried
- [ ] PIM eligibility designed per role
- [ ] Activation requirements configured
- [ ] Permanent standing removed after test
- [ ] Activation/approval path evidenced
- [ ] Break-glass accounts documented
- [ ] Alerts on standing privilege creation
- [ ] Access reviews scheduled
- [ ] `code-quality-standards` applied if automation shipped

## Rules

- Authorized identity governance only.
- No standing production Owner for daily work.
- Dual control for highest roles.
- Log and review every activation.
- Do not disable MFA requirements to “make PIM easier.”
