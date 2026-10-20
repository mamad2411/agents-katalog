---
name: firewall-rule-review
description: >
  Authorized firewall and security-group rule review methodology: inventory, least
  privilege, shadow/redundant rules, overly broad CIDRs, egress control, change hygiene,
  and evidence-based findings. Use when reviewing iptables/nftables, cloud SGs/NSGs/NACLs,
  host firewalls, or network allowlists on systems you own—not for attacking third parties.
---

# Firewall Rule Review

## Scope And Authorization

- **In scope:** network security controls on assets you own or are contracted to review.
- **Out of scope:** scanning or probing third-party networks; “testing” rules by attacking neighbors.
- Prefer read-only inventory first; changes need change windows.
- Redact public IPs tied to home users if sensitive; mark internal diagrams confidential.
- Pair automation with `code-quality-standards`.

## When To Use

- Periodic **firewall / SG / NSG / nftables** hygiene reviews.
- Before exposing a new service or after incidents involving lateral movement.
- Finding `0.0.0.0/0` admin ports, any-any rules, or unused historical allows.
- Aligning documented architecture with enforced rules.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| GCP VPC firewall deep dive | `gcp-firewall-rules` |
| Application authZ bugs | API/IDOR skills |
| WAF/HTTP filtering | WAF/app skills in catalog |
| Host priv-esc after network access | `linux-privilege-escalation` / Windows counterpart |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Stack | Inventory sources |
| --- | --- |
| Linux nft/iptables | `nft list ruleset`, `iptables-save` |
| firewalld | `firewall-cmd --list-all-zones` |
| AWS SG/NACL | EC2 describe-security-groups, NACLs |
| Azure NSG | Network security groups effective rules |
| GCP firewall | `gcloud compute firewall-rules list` |
| Host agents | vendor policy exports |

## Review dimensions

| Dimension | Look for |
| --- | --- |
| Ingress least privilege | Ports/protocols/sources minimized |
| Egress | Defaults allow-all? data exfil paths |
| Shadow rules | Broad rule earlier makes later deny useless (order-sensitive systems) |
| Redundant | Duplicate allows; unused SG attachments |
| Admin surfaces | SSH/RDP/WinRM/DB open to world |
| Logging | Flow logs / deny logs enabled |
| Change control | Who approved rule; expiry on temp allows |

## Workflow

### 1. Confirm scope and success criteria

1. VPCs/subscriptions/hosts in scope; change freeze status.
2. Success: inventory artifact; risk-ranked findings; remediation tickets with owners.
3. Define risk rubric (e.g. world-SSH = critical).

### 2. Inventory rules and attachments

```bash
# Linux host (owned)
sudo nft list ruleset
sudo iptables-save
# AWS example
aws ec2 describe-security-groups --output json > sg.json
aws ec2 describe-network-acls --output json > nacl.json
# GCP example
gcloud compute firewall-rules list --format=json > gcp-fw.json
```

1. Map each rule → resources attached (instances, ENIs, pods).
2. Export effective rules where platform supports (Azure effective NSG).

### 3. Baseline architecture intent

1. Collect intended trust zones (public web, app, data, mgmt).
2. Compare enforced allows to intended north-south / east-west paths.
3. Note temporary incident rules still present.

### 4. Analyze systematically

```text
For each allow rule:
  - source/destination specificity
  - port range width (1 port vs 0-65535)
  - protocol
  - direction
  - hit counters / last used if available
  - attachment still exists?
  - expires?
```

1. Flag `0.0.0.0/0` or `::/0` on mgmt and DB ports.
2. Flag overlapping shadow rules on ordered firewalls.
3. Flag egress any-any from high-sensitivity tiers if policy requires restrict.
4. Check implied default-deny existence.

### 5. Validate carefully (authorized)

1. Prefer config review + flow logs over active port scans.
2. If verification probes needed, only against owned IPs, low rate, scheduled.
3. Confirm intended service still works after proposed tightenings in staging.

### 6. Remediate and verify

```text
# Prefer
# source: corp VPN / bastion SG
# port: 5432
# dest: db SG only
# over
# source: 0.0.0.0/0 port 0-65535
```

1. Remove unused SGs; collapse duplicates.
2. Add deny logging where supported.
3. Re-export inventory post-change; diff.

### 7. Hand off

1. Findings table: id, severity, rule ref, resource, evidence, fix, owner.
2. Temporary exceptions with expiry dates.
3. Automate drift detection in CI for IaC-defined firewalls.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Admin access | VPN/bastion SG only | SSH `/0` |
| Evidence | Rule id + export snippet | “Firewall weak” vibe |
| Temp rules | Ticket + expiry | Forever `/32` of left laptop |
| Egress | Explicit package/CDN allows | Silent full egress on PCI tier |
| Order | Document precedence | Random inserts |
| Scope | Read-only first | Prod lockout Friday |

## Output Checklist

- [ ] Scope and platforms recorded
- [ ] Full rule inventory exported
- [ ] Attachment map complete
- [ ] High-risk world-open and any-any flagged
- [ ] Shadow/redundant analysis done where applicable
- [ ] Egress posture reviewed
- [ ] Remediation tickets with owners/expiry
- [ ] Post-change verification
- [ ] `code-quality-standards` for automation/IaC

## Rules

- Authorized assets only; do not “verify” by attacking third parties.
- Prefer least privilege and default deny; document exceptions.
- Evidence over opinions; include rule identifiers.
- Route cloud-specific deep dives (e.g. GCP) to specialized skills when needed.
