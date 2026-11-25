---
name: aws-scps-organization
description: >
  AWS Organizations service control policies (SCPs) for owned multi-account estates:
  deny-list vs allow-list strategies, OU attachment, guardrails (regions, root actions,
  leaving org, risky services), and testing with policy simulator. Use when designing
  or reviewing org SCPs, fixing unexpected AccessDenied from SCPs, or hardening
  management/member accounts — not for IAM identity policies alone or third-party orgs.
---

# AWS Organizations SCPs

## Scope And Authorization

- **In scope:** AWS Organizations you own or administer under explicit change authority (management account / delegated admin).
- **Out of scope:** Applying or testing SCPs against organizations you do not control; disrupting production without a change window.
- SCPs can lock out entire OUs — always validate in a sandbox OU first; keep break-glass paths documented.
- Redact account lists and org structure when exporting outside the company.
- Pair policy-as-code with `code-quality-standards`.

## When To Use

- Multi-account landing zone guardrails (Security OU, Workloads OU, Sandbox OU).
- Denying dangerous actions: leave organization, disable CloudTrail, create keys without MFA patterns, unapproved regions.
- Investigating `AccessDenied` that identity policies allow but SCPs block.
- Migrating from FullAWSAccess-only to layered deny SCPs or permission boundaries hybrids.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| IAM role/user permission design | IAM / SSO permission-set skills (`aws-sso-permission-sets`) |
| S3 bucket public access hardening | `aws-s3-bucket-hardening` |
| Secrets rotation | `aws-secrets-manager-rotation` |
| Implementation quality baseline | `code-quality-standards` |
| Engagement recon methodology | `recon-and-methodology` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| SCP effect | Filters max permissions for principals in member accounts (except management account root quirks — still protect management) |
| Not identity | SCP does not grant access; identity + resource policies must still allow |
| Inheritance | SCPs on root + OUs + account all apply (intersection of allows / union of denies depending design) |
| FullAWSAccess | Default AWS-managed allow-all; removing it without replacement can brick accounts |
| Tooling | `organizations` CLI, Console, CloudFormation/StackSets, Control Tower controls, IAM policy simulator |

## Workflow

### 1. Confirm scope and success criteria

1. Record management account ID, org ID, OU tree, target accounts, change ticket, rollback owner.
2. Success: SCP attached; sandbox principal denied risky action; legitimate workload actions still succeed.
3. Identify break-glass: emergency admin role path, SCP detach authority, AWS Support contacts.

### 2. Inventory organization and existing SCPs

```bash
aws sts get-caller-identity
aws organizations describe-organization
aws organizations list-roots
aws organizations list-organizational-units-for-parent --parent-id "$ROOT_ID"
aws organizations list-policies --filter SERVICE_CONTROL_POLICY
aws organizations list-policies-for-target --target-id "$OU_ID" --filter SERVICE_CONTROL_POLICY
aws organizations describe-policy --policy-id "$SCP_ID"
```

1. Map which OUs get which guardrails (prod vs sandbox).
2. List Control Tower / landing-zone managed SCPs to avoid conflicting edits.
3. Note regions and services in use so deny-region SCPs do not break workloads.

### 3. Baseline

1. Export all custom SCP JSON documents with versions/hashes.
2. Capture a known-good action matrix: deploy, read logs, assume roles, use KMS.
3. Document accounts that must keep broad permissions (shared services, networking).

### 4. Design and apply SCP changes

**Prefer additive deny guardrails** over rewriting FullAWSAccess until design is mature.

Example deny: leave org + disable security services (illustrative — tailor actions):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyLeaveOrganization",
      "Effect": "Deny",
      "Action": ["organizations:LeaveOrganization"],
      "Resource": "*"
    },
    {
      "Sid": "DenyStopCloudTrail",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotLike": {
          "aws:PrincipalARN": [
            "arn:aws:iam::*:role/BreakGlassAdmin",
            "arn:aws:iam::*:role/org-security-admin"
          ]
        }
      }
    },
    {
      "Sid": "DenyUnapprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "iam:*",
        "organizations:*",
        "sts:*",
        "support:*",
        "budgets:*",
        "globalaccelerator:*",
        "cloudfront:*",
        "route53:*",
        "wafv2:*",
        "shield:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": ["us-east-1", "eu-west-1"]
        }
      }
    }
  ]
}
```

```bash
aws organizations create-policy \
  --content file://scp-guardrails.json \
  --description "Baseline deny guardrails" \
  --name scp-workloads-guardrails \
  --type SERVICE_CONTROL_POLICY

aws organizations attach-policy --policy-id "$SCP_ID" --target-id "$SANDBOX_OU_ID"
# Promote to workloads OU only after tests pass
```

1. Size limits: SCP document size and count per entity — consolidate statements carefully.
2. Avoid denying `organizations:*` / `sts:AssumeRole` paths needed for your automation without exceptions.
3. Management account is not constrained by SCPs the same way — still harden it; do not run workloads there.

### 5. Verify with evidence

```bash
# From a member account principal in the OU:
aws cloudtrail stop-logging --name org-trail   # expect AccessDenied if SCP applies
aws ec2 describe-instances --region ap-southeast-2  # expect deny if region not allowed
aws s3 ls  # expect success if still allowed
aws organizations list-policies-for-target --target-id "$ACCOUNT_ID" --filter SERVICE_CONTROL_POLICY
```

1. Use IAM policy simulator / Access Analyzer where helpful; remember SCP evaluation is org-side.
2. Run CI/CD deploy of a canary stack in sandbox after attach.
3. Confirm break-glass role still works for emergency procedures.

### 6. Observe and harden

1. CloudTrail organization trail: `AttachPolicy`, `DetachPolicy`, `UpdatePolicy`, `DeletePolicy`.
2. Alert on SCP detach from prod OUs and on creation of new accounts outside expected OUs.
3. Periodic review: unused regions, new services, exception principal ARNs.

### 7. Hand off

1. Publish SCP catalog (name, intent, OUs, exception roles) in the security wiki.
2. Encode SCPs in IaC with PR review — avoid Console-only drift.
3. Schedule quarterly effectiveness review with platform + security.

## SCP Design Patterns

| Pattern | Pros | Cons |
| --- | --- | --- |
| Deny-list on FullAWSAccess | Safer incremental adoption | Misses novel risky APIs |
| Allow-list (replace FullAWSAccess) | Strong least privilege at org layer | High maintenance; easy to brick |
| Region lock | Reduces attack surface / data residency | Breaks global service nuances if NotAction incomplete |
| Service lockdown (e.g. no IAM users) | Forces federation | Needs exception for break-glass |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Sandbox OU → nonprod → prod | Attach untested SCP at root |
| Exceptions | Named break-glass roles + MFA | `StringNotEquals` Principal `*` mistakes |
| FullAWSAccess | Keep until allow-list proven | Delete FullAWSAccess with empty replacement |
| Debugging | Check SCP before rewriting IAM | Endless identity policy edits ignoring SCP |
| Workloads in mgmt | None | Production apps in management account |

## Output Checklist

- [ ] Org structure, target OUs/accounts, change authority recorded
- [ ] Existing SCPs exported and conflicts reviewed
- [ ] New/changed SCP validated in sandbox OU
- [ ] Legitimate workload + CI actions verified after attach
- [ ] Denied actions evidenced (AccessDenied samples)
- [ ] Break-glass path tested and documented
- [ ] CloudTrail/monitoring for SCP changes enabled
- [ ] IaC ownership and next review date set
- [ ] `code-quality-standards` applied if policy code shipped

## Rules

- Authorized org administration only; SCPs can cause org-wide outage.
- Never experiment on root/prod OUs first.
- Document every principal exception with owner and expiry.
- SCPs are not a substitute for least-privilege IAM or resource policies.
- Keep management account minimal and highly protected.
