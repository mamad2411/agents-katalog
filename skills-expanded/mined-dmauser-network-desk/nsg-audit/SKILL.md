# Skill: NSG / Security Group Audit (nsec_nsg-audit)

Audit network security group rules across Azure, AWS, and GCP to identify overly permissive access, unused rules, conflicting priorities, and misconfigurations. This skill provides systematic audit procedures with real CLI commands.

---

## Overly Permissive Rule Detection

### Critical Findings — Immediate Remediation Required

**Any-source access to management ports**:
- SSH (TCP 22) from 0.0.0.0/0 — allows brute-force attacks from the entire internet.
- RDP (TCP 3389) from 0.0.0.0/0 — number one attack vector for ransomware.
- WinRM (TCP 5985/5986) from 0.0.0.0/0 — remote management exposure.

**Any-source access to database ports**:
- MySQL (TCP 3306), PostgreSQL (TCP 5432), SQL Server (TCP 1433), MongoDB (TCP 27017), Redis (TCP 6379) from 0.0.0.0/0.

**Any-protocol any-port rules**:
- Rules allowing all traffic (protocol: *, port: *) from any source — effectively disables the security group.

### Audit Commands

**Azure NSG Audit**:
```bash
# List all NSG rules in a subscription
az network nsg list --query '[].{Name:name, RG:resourceGroup}' -o table

# Show rules for a specific NSG
az network nsg rule list \
  --nsg-name MyNSG --resource-group MyRG \
  --query '[].{Priority:priority, Name:name, Direction:direction, Access:access, Protocol:protocol, SrcAddr:sourceAddressPrefix, SrcPort:sourcePortRange, DstAddr:destinationAddressPrefix, DstPort:destinationPortRange}' \
  -o table

# Find all NSGs with inbound rules allowing 0.0.0.0/0 on port 22 or 3389
az network nsg list --query '[].{name:name, rg:resourceGroup, rules:securityRules[?direction==`Inbound` && access==`Allow` && (sourceAddressPrefix==`*` || sourceAddressPrefix==`0.0.0.0/0` || sourceAddressPrefix==`Internet`)]}' -o json

# Show effective security rules for a specific NIC
az network nic list-effective-nsg --name MyNIC --resource-group MyRG
```

**AWS Security Group Audit**:
```bash
# List all security groups with wide-open inbound rules
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName,VpcId]' \
  --output table

# Find SGs allowing SSH from anywhere
aws ec2 describe-security-groups \
  --filters "Name=ip-permission.from-port,Values=22" \
            "Name=ip-permission.to-port,Values=22" \
            "Name=ip-permission.cidr,Values=0.0.0.0/0" \
  --query 'SecurityGroups[].{ID:GroupId,Name:GroupName}'

# Find SGs allowing RDP from anywhere
aws ec2 describe-security-groups \
  --filters "Name=ip-permission.from-port,Values=3389" \
            "Name=ip-permission.to-port,Values=3389" \
            "Name=ip-permission.cidr,Values=0.0.0.0/0" \
  --query 'SecurityGroups[].{ID:GroupId,Name:GroupName}'
```

**GCP Firewall Rule Audit**:
```bash
# List all firewall rules allowing 0.0.0.0/0 source
gcloud compute firewall-rules list \
  --filter="sourceRanges=0.0.0.0/0 AND direction=INGRESS" \
  --format="table(name,network,allowed,sourceRanges,targetTags)"

# Show detailed firewall rule
gcloud compute firewall-rules describe my-rule --format=json

# List firewall rules with logging disabled (blind spots)
gcloud compute firewall-rules list \
  --filter="logConfig.enable=false" \
  --format="table(name,direction,allowed)"
```

---

## Unused Rule Detection

### Identifying Unused Rules

Rules that have never matched traffic (zero hit count) may indicate:
- Legacy rules from decommissioned applications.
- Duplicate or shadowed rules (a higher-priority rule matches all the same traffic).
- Incorrectly configured rules that don't match the intended traffic.

**Azure**: NSG flow logs (version 2) include rule name per flow — aggregate to find rules with zero hits over 30 days.

**AWS**: VPC Flow Logs don't include SG rule IDs, but CloudTrail tracks SG rule changes. Cross-reference SG rules with actual traffic patterns from flow logs.

**GCP**: Firewall Insights (Network Intelligence Center) provides hit-count data per firewall rule and identifies shadowed rules.
```bash
# GCP — check firewall insights for unused rules
gcloud compute firewall-rules list --format="table(name,direction,disabled)"
# Review in Console: Network Intelligence Center > Firewall Insights
```

---

## Conflicting Priority Analysis

### Azure NSG Priority Conflicts
Azure evaluates NSG rules by priority number (lower = higher priority). A common misconfiguration is having a broad allow rule at a lower priority number that shadows more specific deny rules.

**Example conflict**:
- Priority 100: Allow TCP * from 10.0.0.0/8 (too broad — allows all ports)
- Priority 200: Deny TCP 3389 from 10.0.0.0/8 (never evaluated — shadowed by rule 100)

**Resolution**: Place deny rules at lower priority numbers than allow rules, or use more specific allow rules.

### AWS Security Group Behavior
AWS SGs are stateful and allow-only — there are no explicit deny rules. All rules are evaluated collectively (order doesn't matter). The most permissive matching rule wins. Conflicts manifest as unintended access rather than shadowed rules.

### GCP Firewall Priority Conflicts
GCP evaluates rules by priority (0–65535, lower = higher priority). A lower-priority allow rule can shadow a higher-priority deny rule.

```bash
# GCP — find rules with the same priority (potential conflicts)
gcloud compute firewall-rules list \
  --format="table(name,priority,direction,allowed,denied)" \
  --sort-by=priority
```

---

## Azure NSG Effective Rules vs AWS SG Stateful Behavior vs GCP Priority-Based

| Feature | Azure NSG | AWS Security Groups | GCP Firewall Rules |
|---------|-----------|--------------------|--------------------|
| Statefulness | Stateful | Stateful | Stateful |
| Deny rules | Explicit allow/deny | Allow only (implicit deny) | Explicit allow/deny |
| Evaluation | Priority-ordered | All rules evaluated | Priority-ordered |
| Applied to | Subnet and/or NIC | Instance ENI | Instance (via tags/SA) |
| Default inbound | Deny (except VNet, LB) | Deny all | Deny all (implied) |
| Default outbound | Allow (to Internet) | Allow all | Allow all (implied) |
| Max rules/group | 1000 (augmented) | 60 inbound + 60 outbound | 65535 per network |
**Analysis only — verify against vendor documentation before applying.**
