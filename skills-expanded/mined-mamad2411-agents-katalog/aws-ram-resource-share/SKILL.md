---
name: aws-ram-resource-share
description: >
  AWS Resource Access Manager (RAM) for owned organizations: resource shares,
  principals (accounts/OUs), resource types (subnets, TGW, Route53, Aurora, etc.),
  external share settings, and least-privilege sharing. Use when sharing resources
  across accounts safely — not for accepting or creating shares outside authorization.
---

# AWS RAM Resource Share

## Scope And Authorization

- **In scope:** RAM resource shares in AWS Organizations/accounts you administer.
- **Out of scope:** Accepting unexpected shares from unknown accounts; sharing into customer accounts without agreement.
- Shares expand blast radius — prefer OU-scoped principals over entire org when possible.
- Disable sharing with external accounts unless explicitly required.
- Pair with Access Analyzer external access reviews and `code-quality-standards` for IaC.

## When To Use

- Sharing VPC subnets, Transit Gateway, Route 53 Resolver rules, IPAM pools, Aurora, License Manager configs, etc.
- Migrating from duplicate resources per account to shared services account patterns.
- Reviewing who can access a shared resource.
- Restricting `ram.amazonaws.com` external sharing.
- Troubleshooting pending invitations and share ARNs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| VPC design deep dive | networking skills |
| Organizations tag policies | `aws-organizations-tag-policies` |
| S3 cross-account (often bucket policy) | `aws-s3-bucket-hardening` / Access Grants |
| IAM least privilege | `aws-iam-least-privilege` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Object | Meaning |
| --- | --- |
| Resource share | Bundle of resources + principals |
| Principal | Account ID, OU, organization, or IAM role (type-dependent) |
| Managed permissions | RAM permission versions per resource type |
| External accounts | Outside org; invitations |
| Feature set | Some types support sharing only within org |

## Share Safely Checklist

| Control | Guidance |
| --- | --- |
| Principals | Specific OUs/accounts, not every account if avoidable |
| Permissions | Use least RAM managed permission version |
| External | Off by default at org |
| Review | Quarterly list-resources / list-principals |
| Network | Shared subnets still need NACLs/SG discipline in participant accounts |

## Workflow

### 1. Confirm scope and success criteria

1. Record owner account, resource ARNs, consumer accounts/OUs, data sensitivity.
2. Success: consumers can use resource as designed; non-consumers cannot; external sharing disabled; documented owners.
3. Identify alternative (duplicate resource) if share too risky.

### 2. Inventory shares

```bash
aws ram get-resource-shares --resource-owner SELF
aws ram get-resource-shares --resource-owner OTHER-ACCOUNTS
aws ram list-resources --resource-owner SELF --resource-share-arn "$SHARE_ARN"
aws ram list-principals --resource-owner SELF --resource-share-arn "$SHARE_ARN"
aws ram list-pending-invitation-resources 2>/dev/null || true
```

1. Org setting: sharing enabled? external allowed?
2. Access Analyzer findings for shared resources.
3. Unexpected accepted shares from outside.

### 3. Baseline

1. Export share configurations JSON.
2. Diagram owner vs participant accounts.
3. Note RAM managed permission ARNs/versions in use.

### 4. Create/update shares least privilege

```bash
aws ram create-resource-share \
  --name shared-subnets-prod \
  --resource-arns arn:aws:ec2:REGION:OWNER:subnet/subnet-abc \
  --principals ou-xxxx-yyyyyyyy \
  --permission-arns arn:aws:ram::aws:permission/AWSRAMDefaultPermissionSubnet
```

**Hardening**

1. Prefer OU principals over listing 100 accounts when org-aligned.
2. Do not share production databases broadly — prefer data-plane patterns with IAM auth and explicit consumers.
3. For subnet sharing: educate participants about launch permissions and SG ownership models.
4. Reject pending invites from unknown accounts; investigate.
5. Org policy: `EnableAWSServiceAccess` for RAM; `AllowExternalPrincipals=false` on shares.

```bash
aws ram update-resource-share --resource-share-arn "$SHARE_ARN" --no-allow-external-principals
```

### 5. Verify with evidence

1. Participant account sees resource (e.g., subnet visible) and can perform intended action.
2. Account outside principals cannot see/use resource.
3. Share shows correct permission version.

```bash
aws ram get-resource-share-associations --association-type PRINCIPAL --resource-share-arns "$SHARE_ARN"
```

### 6. Observe and harden

1. CloudTrail: `CreateResourceShare`, `AssociateResourceShare`, accept invitation events → alert.
2. Quarterly principal review; remove left-org accounts.
3. Tag shares with Owner and Ticket.

### 7. Hand off

1. Shared services catalog (what is shared, to whom, why).
2. Request process for new consumers.
3. Incident: revoke principal association steps.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Principals | specific OUs | entire org + external true |
| Review | quarterly | set and forget |
| Invites | reject unknown | accept all |
| DB share | narrow consumers | share prod Aurora to sandboxes |
| Perms | default least / custom least | custom broad permissions |
| Docs | catalog + owners | tribal knowledge |

## Output Checklist

- [ ] Resources and consumers recorded
- [ ] Existing shares inventoried (self + other)
- [ ] External principals disabled unless required
- [ ] Managed permissions least privilege
- [ ] Verify consumer allow / outsider deny
- [ ] CloudTrail alerts on share changes
- [ ] Catalog and request process published
- [ ] Access Analyzer reviewed
- [ ] `code-quality-standards` on IaC shares

## Rules

- Authorized org sharing only.
- Default deny external principals.
- Treat shares as permanent attack-surface expansions — review often.
- Prefer OU-aligned shared services accounts.
- Focus on RAM; S3/IAM-specific sharing may use other mechanisms.
