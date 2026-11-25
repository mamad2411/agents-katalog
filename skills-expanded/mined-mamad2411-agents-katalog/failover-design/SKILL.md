# Skill: Failover and Redundancy Design (hyb_failover-design)

Design high-availability hybrid connectivity architectures with automatic failover, fast convergence, and tested recovery procedures.

---

## Dual ExpressRoute / Direct Connect Circuits

### Diverse Peering Locations
Deploy two circuits at geographically separate peering locations to protect against single-site failure (fiber cut, facility outage, provider equipment failure).

**Azure ExpressRoute**:
- Circuit A at peering location "Ashburn" (primary), Circuit B at "Dallas" (backup).
- Both circuits connect to the same ExpressRoute Gateway in the target VNet.
- Use BGP local preference on-premises: Circuit A LP 200 (primary), Circuit B LP 100 (backup).
- From Azure side, configure connection weight: primary connection weight 100, backup weight 0 (Azure prefers higher weight for outbound traffic to on-premises).

```bash
# Set connection weight on ExpressRoute connection
az network vpn-connection update \
  --name PrimaryERConnection \
  --resource-group MyRG \
  --routing-weight 100

az network vpn-connection update \
  --name SecondaryERConnection \
  --resource-group MyRG \
  --routing-weight 0
```

**AWS Direct Connect**:
- Connection A at "Equinix DC1" with Private VIF through Direct Connect Gateway.
- Connection B at "CoreSite DC2" with Private VIF through the same Direct Connect Gateway.
- Configure BGP local preference on-premises routers for primary/secondary path selection.
- AWS automatically prefers the path with the shortest AS path for return traffic.

**GCP Cloud Interconnect**:
- Google recommends a "production-grade" topology: 4 VLAN attachments across 2 metro areas, 2 per metro, in different edge availability domains.
- Each metro has 2 connections to different edge availability domains for 99.99% SLA.

---

## VPN Backup for Dedicated Circuits

### ExpressRoute + S2S VPN Failover

Deploy a VPN Gateway alongside the ExpressRoute Gateway in the same VNet for automatic failover when ExpressRoute is unavailable.

**Architecture**:
- ExpressRoute Gateway (ErGw1AZ or higher) handles primary traffic.
- VPN Gateway (VpnGw1AZ or higher, active-active recommended) provides backup.
- BGP is mandatory for both connections — enables automatic route withdrawal and failover.
- On-premises: advertise the same prefixes via both ExpressRoute and VPN BGP sessions.
- Set local preference: ExpressRoute LP 200, VPN LP 100.

**Failover Behavior**:
1. ExpressRoute circuit goes down → MSEE withdraws BGP routes.
2. On-premises router detects BGP session loss (via BFD in ~1s or hold timer in ~90s).
3. On-premises routing table converges — VPN path (LP 100) becomes best path.
4. Traffic shifts to VPN tunnel. Throughput drops to VPN gateway capacity.
5. When ExpressRoute recovers, BGP session re-establishes, LP 200 routes reinstall, traffic shifts back.

**Convergence Time**:
- With BFD: 1–3 seconds detection + 2–5 seconds convergence = **3–8 seconds total**.
- Without BFD: 90 seconds hold timer + 5–15 seconds convergence = **95–105 seconds total**.

### AWS Direct Connect + VPN Backup
- Create a VPN connection to the same VGW or Transit Gateway that terminates Direct Connect.
- AWS path selection: Direct Connect preferred over VPN by default (shorter AS path if Direct Connect is single-hop; VPN traverses Amazon backbone with additional hops).
- For Transit Gateway: configure route table preferences — Direct Connect attachment preferred over VPN attachment.

---

## Active-Active Gateways

### Azure Active-Active VPN Gateway
- Two gateway instances, each with a dedicated public IP.
- Each instance establishes separate S2S tunnels to the on-premises VPN device.
- On-premises device must support two IPsec tunnels and ECMP (Equal-Cost Multi-Path) or BGP multi-path.
- Traffic is distributed across both tunnels. If one instance fails, all traffic shifts to the surviving instance.

```bash
# Create active-active VPN gateway
az network vnet-gateway create \
  --name MyVPNGateway \
  --resource-group MyRG \
  --vnet MyVNet \
  --gateway-type Vpn \
  --sku VpnGw2AZ \
  --vpn-type RouteBased \
  --active-active true \
  --public-ip-addresses MyGwPIP1 MyGwPIP2
```

### GCP HA VPN Gateway
- Two interfaces (interface 0, interface 1), each with a unique external IP.
- Recommended: 4 tunnels (2 per interface) connecting to 2 interfaces on the peer gateway.
- Achieves 99.99% SLA when configured with recommended redundancy.
- Cloud Router handles BGP for all tunnels — automatic failover if any tunnel goes down.

---

## BFD Timer Configuration

BFD is critical for achieving sub-second failover. Timer selection balances detection speed against false-positive risk.

| Environment | TX Interval | RX Interval | Multiplier | Detection Time |
|------------|------------|------------|-----------|---------------|
| Production (conservative) | 1000ms | 1000ms | 3 | 3 seconds |
| Production (standard) | 300ms | 300ms | 3 | 900ms |
| Production (aggressive) | 100ms | 100ms | 3 | 300ms |
| Direct Connect / ER | 300ms | 300ms | 3 | 900ms |

**Recommendations**:
- Start with standard (300ms/3x) and monitor for false positives before reducing intervals.
- Avoid sub-100ms intervals on cloud peering sessions — cloud provider edge routers may not support or may flap.
- Ensure BFD is enabled on both ends — asymmetric BFD configuration causes unpredictable behavior.

---

## Convergence Time Expectations

| Scenario | With BFD | Without BFD |
|---------|---------|------------|
| ExpressRoute primary → ExpressRoute secondary | 1–5s | 30–90s |
| ExpressRoute → VPN backup | 3–8s | 95–105s |
| S2S VPN tunnel failover (active-active) | 1–3s | 10–15s |
| AWS Direct Connect → VPN backup | 3–10s | 60–120s |
| GCP HA VPN tunnel failover | 1–5s | 30–60s |

**Factors Affecting Convergence**:
- BGP scan interval (default 60s on some platforms — reduce to 5–15s).
- BGP next-hop tracking (enables sub-scan-interval convergence).
- Route table size (larger tables take longer to converge).
- TCP session state on firewalls/NVAs (asymmetric routing during failover may cause session drops).

---

## Failover Testing Procedures

### Pre-Test Preparation
1. Document current routing state: BGP neighbor table, routing table, active tunnels/circuits.
2. Identify test window — off-peak hours recommended for first test.
3. Establish monitoring: real-time BGP session status, throughput graphs, application health checks.
4. Notify stakeholders — even planned failovers may cause brief application disruption.

### Test Scenarios

**Scenario 1 — Primary Circuit Shutdown**:
```bash
# On-premises router — shut down primary interface
interface GigabitEthernet0/0
  shutdown
```
- Expected: BFD detects failure → BGP session drops → backup path installs → traffic shifts.
- Measure: Time from shutdown to first packet on backup path. Target: < 10 seconds.

**Scenario 2 — BGP Session Reset**:
```bash
# On-premises router — clear BGP session
clear ip bgp 10.0.0.1
```
- Expected: BGP session goes through Idle → Active → OpenSent → OpenConfirm → Established. Backup path active during re-convergence.
- Measure: Total reconvergence time. Target: < 30 seconds.

**Scenario 3 — Cloud Provider Maintenance Simulation**:
- Disable the ExpressRoute circuit or VPN connection from the cloud portal.
- Validates end-to-end failover including cloud-side routing convergence.

### Post-Test Validation
1. Verify traffic has shifted to backup path (check interface counters, flow logs).
2. Confirm application functionality on backup path (reduced bandwidth may impact performance).
3. Re-enable primary path and verify traffic shifts back (preemptive failback if using LP/weight).
4. Document results: actual convergence time, any application errors, any unexpected behaviors.

**Analysis only — verify against vendor documentation before applying.**
