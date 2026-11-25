---
name: aws-rds-public-access
description: >
  Harden public accessibility of Amazon RDS/Aurora for owned accounts: PubliclyAccessible
  flag, subnet groups (public vs private), security groups, TLS, and safe remote admin
  patterns. Use when closing internet-exposed databases or reviewing misconfigurations —
  not for scanning or exploiting third-party RDS endpoints.
---

# AWS RDS Public Access

## Scope And Authorization

- **In scope:** RDS/Aurora instances and clusters in accounts you own or assess with authorization.
- **Out of scope:** Port-scanning or credential attacks against third-party databases.
- Internet-facing DB engines are high risk — default target is **private only**.
- Temporary public access for migration requires ticket, IP allowlist, short expiry.
- Pair with `aws-rds-iam-auth`, `aws-rds-proxy`, SG hygiene, `code-quality-standards`.

## When To Use

- Finding `PubliclyAccessible=true` instances.
- Moving DBs to private subnets / fixing subnet groups.
- Tightening SG ingress (no 0.0.0.0/0 on 3306/5432/1433).
- Designing bastion/SSM/VPN/Proxy patterns for admin access.
- Responding to Security Hub / Config findings on open RDS.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| IAM DB authentication | `aws-rds-iam-auth` |
| Connection pooling | `aws-rds-proxy` |
| Aurora Global DR | `aws-aurora-global-db` |
| GuardDuty malware | `aws-guardduty-malware` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Target state |
| --- | --- |
| `PubliclyAccessible` | `false` |
| Subnet group | Private subnets only |
| Security group | App/proxy SG sources only; no world |
| TLS | Required for clients |
| Admin path | SSM Session Manager, VPN, or bastion — not open 5432/world |
| Snapshots | Private; encrypted |

## Public Exposure Paths

```text
PubliclyAccessible=true + public subnet + SG 0.0.0.0/0:3306 → Internet can reach engine
PubliclyAccessible=false but SG open still limits to VPC (safer, still tighten)
Public snapshot share → data leak without live endpoint
```

## Workflow

### 1. Confirm scope and success criteria

1. Record instances/clusters, Environments, business justification if any public.
2. Success: no prod DB publicly accessible; no 0.0.0.0/0 on DB ports; private subnet groups; Config compliant.
3. Plan cutover for apps if DNS endpoints change after subnet moves.

### 2. Inventory

```bash
aws rds describe-db-instances --query "DBInstances[].{Id:DBInstanceIdentifier,Public:PubliclyAccessible,SGs:VpcSecurityGroups,Subnets:DBSubnetGroup.Subnets[*].SubnetIdentifier,Addr:Endpoint.Address}" --output table
aws rds describe-db-clusters --query "DBClusters[].{Id:DBClusterIdentifier,Public:PubliclyAccessible}"
aws ec2 describe-security-groups --filters Name=ip-permission.from-port,Values=3306,5432,1433
```

1. Flag public subnets in DB subnet groups (map route 0.0.0.0/0 to IGW).
2. Security Hub controls / Config `rds-instance-public-access-check`.
3. Snapshot public attributes.

### 3. Baseline

1. Export current SG rules and subnet group membership.
2. App connection strings inventory.
3. Change window for making private (may need recreate/subnet group change patterns).

### 4. Remediate

**Disable public accessibility:**

```bash
aws rds modify-db-instance \
  --db-instance-identifier "$ID" \
  --no-publicly-accessible \
  --apply-immediately
```

**Subnet group:** ensure only private subnets; modifying may require maintenance — follow AWS guidance for your topology (sometimes new instance/restore safer).

**Security group:**

```bash
# Remove 0.0.0.0/0 and ::/0 on DB ports; allow only sg-app / sg-proxy
aws ec2 revoke-security-group-ingress --group-id sg-db \
  --ip-permissions '[{"IpProtocol":"tcp","FromPort":5432,"ToPort":5432,"IpRanges":[{"CidrIp":"0.0.0.0/0"}]}]'
aws ec2 authorize-security-group-ingress --group-id sg-db \
  --protocol tcp --port 5432 --source-group sg-app
```

**Admin access patterns**

1. SSM port forwarding through bastion/instance in private subnet.
2. VPN / Client VPN to VPC.
3. RDS Proxy private endpoint for apps.
4. Never long-term `MyIP` open without automation to revoke.

**TLS & auth**

1. Force SSL parameters (`require_secure_transport`, rds.force_ssl).
2. Prefer IAM auth or rotated secrets — not weak passwords on any residual exposure.

### 5. Verify with evidence

```bash
aws rds describe-db-instances --db-instance-identifier "$ID" --query "DBInstances[].PubliclyAccessible"
# From Internet workstation (authorized test): connection should fail
# From app SG: connection succeeds
aws ec2 describe-security-groups --group-ids sg-db
```

1. Config/Security Hub finding resolves.
2. Snapshots not public.
3. Route tables confirm DB subnets lack IGW default route.

### 6. Observe and harden

1. Config continuous compliance; SCP prevent `PubliclyAccessible` if org-ready.
2. Alert on SG rules opening DB ports to world.
3. Periodic review of temporary admin rules.

### 7. Hand off

1. Private connectivity diagram for developers.
2. Runbook for emergency admin access with expiry.
3. IaC defaults: `publicly_accessible = false`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Accessibility | false | true for convenience |
| SG | app/proxy SG only | 0.0.0.0/0:5432 |
| Subnets | private | public subnet group |
| Admin | SSM/VPN temporary | laptop open to Internet forever |
| Snapshots | private encrypted | public snapshot |
| Findings | remediate + prevent | ignore Config |

## Output Checklist

- [ ] All instances/clusters inventory for PubliclyAccessible
- [ ] Subnet groups private
- [ ] SG world-open rules removed
- [ ] App connectivity validated privately
- [ ] TLS/auth baseline confirmed
- [ ] Snapshots privacy checked
- [ ] Config/Security Hub clean or excepted
- [ ] Admin access runbook with expiry
- [ ] IaC defaults prevent regression
- [ ] Related IAM auth/proxy reviewed

## Rules

- Authorized assessments only; do not attack external RDS.
- Default deny Internet exposure of database engines.
- Temporary public access requires ticket and expiry.
- Defense in depth: private + SG + TLS + strong auth.
- Focus on exposure; proxy and IAM auth skills handle adjacent controls.
