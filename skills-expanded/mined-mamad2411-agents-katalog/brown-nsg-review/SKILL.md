---
name: brown-nsg-review
description: |
  Audit, review, and author NSG rules for Brown & Brown Azure VNets across
  the Wholesale (346) and Decus (537) fleets. Use when the user mentions NSG,
  network security group, subnet rules, NSG symmetry, traffic flow, or when
  adding/changing bicep NSG rules in any brown repository. Also use when
  diagnosing connectivity failures that might involve NSG blocking.
---

# Brown NSG Review

Author and audit NSG (Network Security Group) rules across the
Wholesale (WHS-346) and Decus (WHS-537) Azure fleets. Every Brown VNet
uses a shared architecture: multiple subnets (APP, DATA, VNetIntegration,
MDOP), each with its own NSG, with traffic forced through a Palo Alto NVA
via `0.0.0.0/0 → VirtualAppliance 10.222.252.4`.

## When to use

- User asks about NSG rules, network security, subnet connectivity
- User is adding or changing a bicep NSG rule
- User is debugging a connectivity timeout (TCP, SQL, HTTPS)
- User mentions "traffic flow", "allow rule", "deny rule", "NSG gap"
- User is comparing wholesale vs decus network patterns

## Core principle: NSG symmetry

**Every traffic flow needs TWO NSG rules** — one on the source NSG
(outbound) and one on the destination NSG (inbound). Missing either
side produces a silent TCP timeout (not a connection refused). This
is the #1 cause of multi-hour NSG debugging sessions.

Check both directions every time:

```
Source NSG (OUTBOUND)        Destination NSG (INBOUND)
┌──────────────────┐         ┌──────────────────┐
│ Allow Src→Dest   │ ──────→ │ Allow Src→Dest   │
│ direction: Out    │         │ direction: In     │
└──────────────────┘         └──────────────────┘
```

## Fleet NSG maps

### Decus 537 (this repo)

VNet: `VNET-WHS-537-EastUS2-DEV` (`10.218.56.0/22`)

| Subnet | Prefix | NSG | Resources |
|--------|--------|-----|-----------|
| SNET-APP | `10.218.56.0/26` | NSG-WHS-537-APP | Aggregates API, App Services |
| SNET-DATA | `10.218.57.0/26` | NSG-WHS-537-DATA | SQL PE (10.218.57.7), KV PE, AppConfig PE |
| SNET-VNetInt | `10.218.58.0/26` | NSG-WHS-537-VNetIntegration | VNet-integrated apps |
| SNET-MDOP | `10.218.59.0/26` | NSG-WHS-537-MDOP | Managed DevOps Pool agents |

Route: All subnets use `RT-PaloFirewallDefault` → `0.0.0.0/0 → NVA 10.222.252.4`
(BGP propagation disabled). Intra-VNet traffic is forced through the NVA.

**Allowed flows (codified from bicep `main.bicep`):**

| Flow | Src NSG | Dest NSG | Ports |
|------|---------|----------|-------|
| ZTA VPN → APP:443 | — | APP In 200 | 443 |
| vNetInt → APP:443 | — | APP In 210 | 443 |
| APIM → APP:443 | — | APP In 220 | 443 |
| APP → DATA:1433 | **APP Out 200** | **DATA In 215** | 1433, 11000-11999 |
| APP → Internet:443 | **APP Out 210** | — | 443 |
| ZTA VPN → DATA:1433 | — | DATA In 200 | 1433 |
| vNetInt → DATA:1433 | vNetInt Out 200 | DATA In 210 | 1433, 11000-11999 |
| **MDOP → DATA:1433** | **MDOP Out 250** | **DATA In 220** | 1433, 11000-11999 |
| MDOP → ADO:443 | MDOP Out 200 | — | 443 |
| MDOP → Azure:443 | MDOP Out 210 | — | 443 |
| MDOP → Internet:443 | MDOP Out 220 | — | 443 |
| MDOP → DNS:53 | MDOP Out 230 | — | 53 |
| MDOP → Monitor:443 | MDOP Out 240 | — | 443 |
| vNetInt → Internet:443 | vNetInt Out 210 | — | 443 |

### Wholesale 346

VNet: `VNET-WHS-346-CentralUS-DEV` (documented in
`bicep/foundation/network/nsgs/` as snapshots)

| Subnet | NSG Pattern |
|--------|-------------|
| Application | `NSG-WHS-346-APP-CentralUS-{ENV}` |
| Data | `NSG-WHS-346-DATA-CentralUS-{ENV}` |
| ManagedPool | `NSG-WHS-346-ManagedPool-CentralUS-{ENV}` |
| VNetIntegration | `NSG-WHS-346-905-VNetIntegration-CentralUS-{ENV}` |
| VDI | `NSG-WHS-346-905-VDI-CentralUS-{ENV}` |

**Managed Pool NSG snapshot** (the reference pattern for pool rules):

The 346 ManagedPool NSG has 12 rules. Key ones for pool agents:

| Rule | Dir | Pri | Ports | Description |
|------|-----|-----|-------|-------------|
| AllowBastionInBound | In | 500 | 22,3389 | RDP/SSH from Bastion |
| AllowDNSOutBound | Out | 1001 | 53 | DNS to internal servers |
| Allow_Outbound_From_ManagedDevOpsPool | Out | **1010** | **443,1433** | **Pool → internal subnets** |
| CustomAllowInternetOutBound | Out | 3500 | * | All Internet |
| CustomAllowAllCustomSubnetInBound | In | 4095 | * | Intra-subnet traffic |
| CustomAllowAllCustomSubnetOutBound | Out | 4095 | * | Intra-subnet traffic |
| CustomDenyAllInBound | In | 4096 | * | Default deny |
| CustomDenyAllOutBound | Out | 4096 | * | Default deny |

The critical rule is `Allow_Outbound_From_ManagedDevOpsPool` (1010) —
it allows **both 443 and 1433** from the pool to internal subnets.
This is the pattern we missed in the 537 fleet until run 61786.

## Common pitfalls

### 1. Inbound-only thinking
You add an inbound allow on the destination NSG, forget the matching
outbound on the source NSG. Result: TCP timeout, 30+ min debugging.

**Check**: For every new `Allow*Inbound`, search for the corresponding
`Allow*Outbound` on the source subnet's NSG.

### 2. Forced tunneling through NVA
All subnets route `0.0.0.0/0 → NVA`. Even intra-VNet traffic
(MDOP → DATA) goes through the NVA. The NSG may allow it but the
NVA may drop it. When adding internal flows, verify the NVA
allows the traffic or add a `VirtualNetwork` next-hop route.

### 3. Service tag vs prefix mismatch
Azure service tags (`AzureCloud`, `AzureDevOps`) are scoped to
public endpoints. Internal subnet-to-subnet flows must use CIDR
prefixes (`net.dataPrefix`), not service tags.

### 4. Port range for Azure SQL Redirect
Azure SQL connections on 1433 may redirect to ports 11000-11999.
Rules must allow BOTH ranges or connections timeout silently.

### 5. Missing deny baselines
Every NSG must end with explicit `DenyAllInbound` and `DenyAllOutbound`
at priority 4096. Without these, Azure defaults apply (which may
differ between subscriptions).

## Audit checklist

When reviewing NSG rules:

1. List every cross-subnet flow the architecture requires
2. For each flow, verify source NSG outbound AND destination NSG inbound
3. Check port ranges include Azure SQL Redirect (11000-11999) if needed
4. Verify deny baselines exist at priority 4096 on both directions
5. Check route table: does `0.0.0.0/0 → NVA` intercept intra-VNet traffic?
6. For new MDOP rules, reference the 346 ManagedPool NSG snapshot