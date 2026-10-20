---
name: aws-security-groups-review
description: >
  Authorized AWS Security Group (SG) and related NACL review for owned accounts:
  inventory rules, flag 0.0.0.0/0 and ::/0, unused or stale rules, SG-to-SG references,
  least-privilege ports, and stateful SG vs stateless NACL semantics. Use when reviewing
  VPC security groups, inbound/outbound rules, console or CLI exports, or IaC-defined
  SGs — not for unauthorized Internet scanning or third-party account probing.
---

# AWS Security Groups Review

## Scope And Authorization

- **In scope:** Security groups, ENI attachments, and optional NACLs in VPCs you own or are authorized to assess.
- **Out of scope:** Port-scanning third-party infrastructure; using open SG findings to attack systems outside scope.
- Prefer read-only inventory first; rule removals need change windows and application owners.
- Redact internal CIDRs only if policy requires; never publish live production SG exports publicly.
- Pair IaC fixes with `code-quality-standards`.

## When To Use

- Periodic VPC posture review, M&A cloud due diligence (authorized), or CIS/Security Hub SG findings.
- Investigating unexpected exposure (SSH/RDP/DB ports open to the world).
- Tightening micro-segmentation (app SG → data SG) and removing legacy any-any rules.
- Differentiating SG (stateful) issues from NACL (stateless) misconfiguration.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org-wide SCPs / region lock | `aws-scps-organization` |
| Azure NSG review | `azure-nsg-review` |
| WAF / L7 bot controls | `aws-waf-bot-control` |
| Engagement methodology | `recon-and-methodology` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Inbound | Prefer SG-to-SG or prefix lists over wide CIDRs; no admin ports on `0.0.0.0/0` |
| Outbound | Default allow-all is common — tighten for regulated tiers |
| References | Source SG IDs enable tiers without brittle IPs |
| Stale rules | Detached SGs, rules for decommissioned CIDRs, duplicate SGs per app |
| NACL | Stateless; ephemeral return ports required; use sparingly as subnet guardrail |
| Tooling | `ec2 describe-security-groups`, Config, Security Hub, Reachability Analyzer, IaC |

## Workflow

### 1. Confirm scope and success criteria

1. Record accounts, regions, VPC IDs, app owners, authorization.
2. Success: no unexpected world-open admin/DB ports; documented exceptions; unused SGs ticketed for delete.
3. Rollback: keep rule snapshots before revoke.

### 2. Inventory security groups and attachments

```bash
aws sts get-caller-identity
aws ec2 describe-vpcs --query "Vpcs[].VpcId" --output text
aws ec2 describe-security-groups --output json > sg-inventory.json
aws ec2 describe-network-interfaces --query "NetworkInterfaces[].{ID:NetworkInterfaceId,SGs:Groups,Subnet:SubnetId,PrivateIp:PrivateIpAddress}"
aws ec2 describe-security-group-references --group-id sg-xxxxxxxx
```

1. Map each SG to ENIs / instances / load balancers / RDS / Lambda Hyperplane ENIs.
2. List NACLs if subnet-level denies are suspected: `aws ec2 describe-network-acls`.

### 3. Baseline risk analysis

Flag high-risk patterns:

| Pattern | Risk | Typical action |
| --- | --- | --- |
| Inbound TCP 22/3389 from `0.0.0.0/0` | Brute force / RCE path | Restrict to bastion / VPN / SSM |
| DB ports (5432/3306/1433/27017) from `0.0.0.0/0` | Data breach | App SG only |
| All traffic `-1` from `0.0.0.0/0` | Flat network | Split by tier |
| Outbound all + sensitive data plane | Exfil ease | Egress proxy / prefix allow |
| Orphan SG (0 ENIs) | Drift / confusion | Delete after confirm |

```bash
# Example: jq-style review locally on export (illustrative)
# Find IPv4 world-open ingress
python - <<'PY'
import json
data=json.load(open("sg-inventory.json"))
for sg in data.get("SecurityGroups",[]):
  for p in sg.get("IpPermissions",[]):
    for r in p.get("IpRanges",[]):
      if r.get("CidrIp")=="0.0.0.0/0":
        print(sg["GroupId"], sg.get("GroupName"), p.get("IpProtocol"), p.get("FromPort"), p.get("ToPort"))
PY
```

### 4. Apply least-privilege changes

```bash
# Revoke world SSH (example)
aws ec2 revoke-security-group-ingress --group-id sg-app --protocol tcp --port 22 --cidr 0.0.0.0/0
# Prefer SSM Session Manager over bastion SSH when possible
# Authorize app → db using source SG
aws ec2 authorize-security-group-ingress --group-id sg-db --protocol tcp --port 5432 \
  --source-group sg-app
```

1. Prefer prefix lists for corporate egress IPs.
2. Split “shared default SG” into per-service SGs.
3. Document temporary wide rules with owner + expiry ticket.
4. Align Terraform/CloudFormation so Console fixes are not reverted.

### 5. Verify with evidence

```bash
aws ec2 describe-security-groups --group-ids sg-app sg-db
aws ec2 describe-network-interfaces --filters Name=group-id,Values=sg-app
# Optional authorized path test from bastion host only
# aws ec2 search-transit-gateway-routes ... / Reachability Analyzer in Console
```

1. App health after rule change; DB connectivity from app only.
2. Security Hub / Config (`restricted-ssh`, unrestricted common ports) re-check.
3. Attach before/after JSON diffs (redacted) to change ticket.

### 6. Observe and harden

1. Alert on `AuthorizeSecurityGroupIngress` with `0.0.0.0/0` via CloudTrail → SIEM.
2. Periodic unused-SG report; VPC Flow Logs for unexpected accepts.
3. Prefer IMDSv2 + no public instance IPs when SG allows broad ingress by mistake.

### 7. Hand off

1. Owner matrix: which team owns which SG naming prefix.
2. Standard modules: `sg-web`, `sg-app`, `sg-data` patterns.
3. Exceptions list with review dates.

## SG vs NACL (quick)

| | Security group | NACL |
| --- | --- | --- |
| State | Stateful | Stateless |
| Attach | ENI | Subnet |
| Default | Deny inbound (custom SG) | Custom rules vary |
| Use | Primary micro-segmentation | Coarse subnet guardrail / deny known bad |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Admin access | SSM + private subnets | SSH `0.0.0.0/0` |
| Data tier | Ingress only from app SG | Same SG for web and DB |
| Change mgmt | Snapshot + staged revoke | Delete rules mid-incident without owner |
| IaC | SG rules in code review | Snowflake Console rules only |
| Verification | Flow logs + probe from allowed path | “Port closed in my browser” |

## Output Checklist

- [ ] Scope, VPCs, accounts, authorization recorded
- [ ] Full SG inventory + attachment map captured
- [ ] World-open and high-risk ports triaged
- [ ] Stale/orphan SGs listed
- [ ] Least-privilege changes applied or ticketed
- [ ] App connectivity verified after changes
- [ ] CloudTrail/Config monitoring considered
- [ ] Exceptions have owner + expiry
- [ ] IaC updated; `code-quality-standards` applied

## Rules

- Authorized VPCs only; do not scan or exploit third parties.
- Prefer SG-to-SG references over wide CIDRs.
- Never leave temporary `0.0.0.0/0` without expiry.
- Remember NACLs are stateless when debugging asymmetric failures.
- Evidence over assumptions; Flow Logs beat guesses.
