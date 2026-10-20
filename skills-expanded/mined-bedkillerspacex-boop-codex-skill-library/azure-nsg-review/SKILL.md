---
name: azure-nsg-review
description: >
  Authorized Azure Network Security Group (NSG) and related ASG review for owned
  virtual networks: inventory rules, flag 0.0.0.0/0 and Internet sources, priority
  conflicts, stale rules, service tags, and effective security rules on NICs. Use when
  hardening subnets or investigating unexpected exposure — not for unauthorized
  Internet scanning.
---

# Azure NSG Review

## Scope And Authorization

- **In scope:** NSGs, ASGs, subnets, and NICs in Azure networks you own or are authorized to assess.
- **Out of scope:** Port scanning third parties; using open management ports for exploitation outside scope.
- Rule removals can break apps — coordinate owners and change windows.
- Pair edge WAF with `azure-frontdoor-waf`; AWS SG analog is `aws-security-groups-review`.

## When To Use

- Periodic VNet posture review or Defender recommendations on overly permissive NSGs.
- SSH/RDP/SQL open to Internet findings.
- Micro-segmentation between app tiers using ASGs.
- Debugging connectivity via effective security rules.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AWS security groups | `aws-security-groups-review` |
| Front Door WAF | `azure-frontdoor-waf` |
| PIM / identity | `azure-pim-eligible-roles` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Priority | Lower number wins; first match |
| Deny/Allow | Explicit deny useful; default rules exist |
| Service tags | `VirtualNetwork`, `AzureLoadBalancer`, `Internet`, `Storage`, … |
| ASG | Application Security Groups as source/dest |
| Effective rules | NIC + subnet NSG combined evaluation |
| Tooling | `az network nsg`, effective-rules APIs, Network Watcher, Policy |

## Workflow

### 1. Confirm scope and success criteria

1. Subscriptions, VNets, subnets, app owners, authorization.
2. Success: no unexpected Internet management/DB exposure; documented exceptions; effective rules match intent.
3. Snapshot NSG JSON before changes.

### 2. Inventory NSGs and associations

```bash
az account show
az network nsg list -o table
az network nsg show -g "$RG" -n "$NSG" -o jsonc > nsg-$NSG.json
az network nsg list --query "[].{name:name,rg:resourceGroup,subnets:subnets,nics:networkInterfaces}" -o jsonc
az network nic list-effective-nsg -g "$RG" -n "$NIC" -o jsonc
```

1. Map each NSG to subnets and NICs.
2. List ASGs and membership.
3. Note Azure Firewall / NVA that may supersede NSG intent.

### 3. Risk analysis baseline

| Pattern | Risk | Action |
| --- | --- | --- |
| Inbound 22/3389 from `*` / Internet | High | Bastion / Just-in-time / private only |
| DB ports from Internet | High | App subnet/ASG only |
| Allow `*` any any high priority | Critical | Split rules |
| Stale IP ranges | Medium | Update or remove |
| Missing deny for sensitive subnet | Medium | Explicit deny + allowlist |

### 4. Remediate rules

```bash
# Remove dangerous rule
az network nsg rule delete -g "$RG" --nsg-name "$NSG" -n "allow-ssh-internet"

# Prefer ASG-based allow app → db
az network nsg rule create -g "$RG" --nsg-name "$NSG-db" -n "allow-app-to-db" \
  --priority 200 --direction Inbound --access Allow --protocol Tcp \
  --destination-port-ranges 1433 \
  --source-asgs "$ASG_APP_ID" --destination-asgs "$ASG_DB_ID"

# Service tag example: allow Azure LB probe
az network nsg rule create -g "$RG" --nsg-name "$NSG" -n "allow-azlb" \
  --priority 100 --direction Inbound --access Allow --protocol '*' \
  --source-address-prefixes AzureLoadBalancer --destination-port-ranges '*'
```

1. Attach NSG at subnet for default posture; NIC NSG only when required.
2. Use service tags over wide IP lists when accurate.
3. Document temporary wide rules with expiry.
4. Align IaC so portal fixes are not reverted incorrectly.

### 5. Verify with evidence

```bash
az network nsg rule list -g "$RG" --nsg-name "$NSG" -o table
az network nic list-effective-nsg -g "$RG" -n "$NIC" -o jsonc
# Network Watcher IP flow verify (authorized)
az network watcher test-ip-flow --direction Inbound --protocol TCP \
  --local "$VM_IP":22 --remote 203.0.113.10:50000 \
  --vm "$VM" -g "$RG" --nic "$NIC" --location "$LOC"
```

1. App connectivity tests after tightening.
2. Defender/Policy compliance improved.
3. Keep redacted before/after rule lists.

### 6. Observe and harden

1. Alert on NSG writes that add Internet source on admin ports.
2. Flow logs / Traffic Analytics for accepted Internet flows.
3. Prefer Azure Bastion + JIT over permanent SSH rules.

### 7. Hand off

1. NSG ownership and naming standards.
2. ASG tier model documentation.
3. Exception register with review dates.

## NSG Evaluation Tips

| Tip | Why |
| --- | --- |
| Check effective rules | NIC + subnet both apply |
| Priority gaps | Leave room between rules |
| Default rules | 65000+ system defaults matter |
| UDRs / Firewall | Path may never hit expected NSG |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Admin access | Bastion / JIT | RDP `*` inbound |
| Tiers | ASG micro-segmentation | One NSG any-any for whole VNet |
| Tags | Service tags | Random public IP lists stale years |
| Change | Snapshot + staged | Delete rules mid-incident blindly |
| Verify | Effective rules + flow verify | “Ping worked once” |

## Output Checklist

- [ ] VNets/NSGs/associations inventoried
- [ ] High-risk Internet rules triaged
- [ ] Least-privilege rules applied or ticketed
- [ ] Effective rules validated on sample NICs
- [ ] App connectivity verified
- [ ] Monitoring/Policy considered
- [ ] Exceptions documented with expiry
- [ ] IaC updated; `code-quality-standards` applied

## Rules

- Authorized networks only.
- Prefer deny-by-default and ASG/service tags.
- No permanent Internet admin ports without risk acceptance.
- Evidence via effective rules and flow tools.
- Coordinate with firewall/WAF architecture.
