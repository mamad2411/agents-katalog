# Skill: BGP Routing Design (hyb_routing-design)

Design BGP routing architectures for hybrid cloud connectivity. This skill covers AS path manipulation, route filtering, BGP communities, local preference, MED, BFD, route summarization, and default route injection.

---

## AS Path Manipulation

AS path is the primary BGP path selection attribute (after local preference and weight). Manipulating AS path length influences how remote ASes select their preferred path to reach your prefixes.

### AS Path Prepending
Artificially lengthens the AS path to make a route less preferred by external peers. Used to influence **inbound** traffic engineering when you advertise the same prefix through multiple points of presence.

```
# On-premises router — prepend AS 65001 twice on backup ExpressRoute circuit
route-map BACKUP-ER-OUT permit 10
  set as-path prepend 65001 65001
!
router bgp 65001
  neighbor 10.0.0.1 route-map BACKUP-ER-OUT out
```

**Caution**: Prepending beyond 3x rarely provides additional benefit and may trigger AS-path length limits on receiving routers. Some providers filter paths with AS path length > 10.

### AS Path Filtering (AS-Path ACLs)
Filter routes based on the AS path attribute. Used to accept/reject routes from specific ASes or through specific transit paths.

```
# Accept only routes originating from AS 12076 (Microsoft)
ip as-path access-list 10 permit ^12076$
!
route-map ACCEPT-MSFT permit 10
  match as-path 10
route-map ACCEPT-MSFT deny 20
!
router bgp 65001
  neighbor 10.0.0.1 route-map ACCEPT-MSFT in
```

---

## Route Filtering

### Prefix Lists
Filter routes based on IP prefix and prefix length. More efficient and predictable than access lists for route filtering.

```
# Accept only Azure VNet prefixes — deny all others
ip prefix-list AZURE-VNETS seq 10 permit 10.1.0.0/16
ip prefix-list AZURE-VNETS seq 20 permit 10.2.0.0/16
ip prefix-list AZURE-VNETS seq 30 permit 172.16.0.0/12 le 24
ip prefix-list AZURE-VNETS seq 999 deny 0.0.0.0/0 le 32
!
route-map FROM-AZURE permit 10
  match ip address prefix-list AZURE-VNETS
route-map FROM-AZURE deny 20
```

### Outbound Route Filtering
Control which on-premises prefixes are advertised to cloud providers. Never advertise more specific routes than necessary — use summary routes to reduce the routing table and prevent hitting cloud-side route limits.

```
# Advertise only summary route to Azure (not individual /24 subnets)
ip prefix-list TO-AZURE seq 10 permit 10.0.0.0/8
ip prefix-list TO-AZURE seq 999 deny 0.0.0.0/0 le 32
!
route-map TO-AZURE-OUT permit 10
  match ip address prefix-list TO-AZURE
```

**Cloud Provider Route Limits**:
- Azure ExpressRoute Private Peering: 4,000 routes (Standard), 10,000 routes (Premium)
- AWS Direct Connect Private VIF: 100 routes from AWS to on-premises
- GCP Cloud Router: 100 learned routes per BGP session (configurable up to 1,000 with quota increase)

---

## BGP Communities

### Standard Communities (AA:NN Format)
Tag routes with community values to signal routing policy intent to peers. Communities can be matched by route maps on receiving routers to apply specific policies.

### Well-Known Communities
- **NO_EXPORT (65535:65281)**: Do not advertise to external BGP peers.
- **NO_ADVERTISE (65535:65282)**: Do not advertise to any BGP peer.
- **NO_EXPORT_SUBCONFED (65535:65283)**: Do not advertise outside the local confederation sub-AS.

### Cloud Provider Communities

**Azure ExpP Route Regional Communities**:
- Format: `12076:5XYYY` where X = region group, YYY = region identifier.
- Example: `12076:51004` = East US, `12076:51006` = East US 2, `12076:52004` = West Europe.
- Use to identify the Azure region from which a route was advertised. Apply on-premises routing policy based on region proximity.

**AWS Direct Connect Communities**:
- `7224:8100` — routes in the same AWS region as the Direct Connect location.
- `7224:8200` — routes in the same continent as the Direct Connect location.
- `7224:8300` — global routes (all AWS regions).
- Customer can set communities on advertised routes to control scope: `7224:9100` (local region), `7224:9200` (continent), `7224:9300` (global).

---

## Local Preference

Local preference is the highest-priority BGP path selection attribute (after weight, which is Cisco-specific). It determines the preferred **outbound** path from the local AS. **Higher local preference is preferred.**

### Primary/Backup Path Design
```
# Primary path via ExpressRoute — LP 200
route-map ER-PRIMARY-IN permit 10
  set local-preference 200
!
# Backup path via VPN — LP 100
route-map VPN-BACKUP-IN permit 10
  set local-preference 100
!
router bgp 65001
  neighbor 10.0.0.1 route-map ER-PRIMARY-IN in   # ExpressRoute peer
  neighbor 10.0.1.1 route-map VPN-BACKUP-IN in    # VPN peer
```

Under normal conditions, all traffic to Azure prefixes uses the ExpressRoute path (LP 200). If the ExpressRoute BGP session goes down, the VPN path (LP 100) becomes the only available route and traffic fails over automatically.

---

## MED (Multi-Exit Discriminator)

MED influences **inbound** path selection by a neighboring AS. **Lower MED is preferred.** MED is compared only among routes from the same neighboring AS (unless `bgp always-compare-med` is configured).

```
# Advertise routes with lower MED on preferred circuit
route-map TO-AZURE-PRIMARY permit 10
  set metric 100
!
route-map TO-AZURE-SECONDARY permit 10
  set metric 200
```

**Important**: Azure ExpressRoute MSEEs compare MED across paths. AWS VGW/TGW also evaluate MED. GCP Cloud Router honors MED on Interconnect VLAN attachments. However, not all cloud providers or ISPs honor MED in all scenarios — always validate with the specific provider.

---

## Bidirectional Forwarding Detection (BFD)

BFD provides sub-second failure detection for BGP sessions, dramatically reducing convergence time compared to BGP hold timer expiry (default 90 seconds).

### BFD Parameters
- **Desired Min TX Interval**: How often to send BFD packets (e.g., 300ms).
- **Required Min RX Interval**: Minimum interval at which BFD packets can be received (e.g., 300ms).
- **Detect Multiplier**: Number of missed BFD packets before declaring failure (e.g., 3 — session down after 3 × 300ms = 900ms).

### Configuration
```
# Enable BFD on BGP neighbor
router bgp 65001
  neighbor 10.0.0.1 fall-over bfd
!
interface GigabitEthernet0/0
  bfd interval 300 min_rx 300 multiplier 3
```

**Cloud Provider BFD Support**:
- **Azure ExpressRoute**: BFD enabled by default on MSEEs. Customer router must enable BFD on the BGP session.
- **AWS Direct Connect**: BFD supported. Configure on customer router with 300ms intervals and multiplier 3 (recommended minimum).
- **GCP Cloud Router**: BFD supported with configurable intervals (minimum 1000ms TX/RX, multiplier 5 by default).

---

## Route Summarization

Aggregate more-specific routes into summary routes to reduce routing table size, improve convergence time, and stay within cloud provider route limits.

```
# Summarize 10.0.0.0/24 through 10.0.15.0/24 as 10.0.0.0/20
router bgp 65001
  aggregate-address 10.0.0.0 255.255.240.0 summary-only
```

The `summary-only` keyword suppresses the more-specific routes — only the aggregate is advertised. Remove `summary-only` to advertise both the aggregate and the specifics (useful for backup path signaling).

---

## Default Route Injection

Advertise a default route (0.0.0.0/0) from on-premises to cloud to force internet-bound traffic from cloud VMs through the on-premises security stack (forced tunneling).

**Azure**: Enable forced tunneling by advertising 0.0.0.0/0 via BGP over ExpressRoute or VPN. This overrides the system route for internet traffic on all subnets associated with the VNet gateway.

**AWS**: Advertise 0.0.0.0/0 via BGP over Direct Connect or VPN. Ensure VPC route table has route propagation enabled from VGW.

**GCP**: Advertise 0.0.0.0/0 via Cloud Router BGP. Configure `--advertise-mode custom` on the Cloud Router to control which routes GCP advertises back.

**Caution**: Forced tunneling increases latency for internet-bound traffic and creates a bottleneck at the on-premises egress point. Consider split tunneling for Microsoft 365 and SaaS traffic.

**Analysis only — verify against vendor documentation before applying.**
