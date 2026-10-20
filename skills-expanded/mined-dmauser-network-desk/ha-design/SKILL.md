# Skill: High-Availability Design

## Purpose

Design and recommend high-availability (HA) architectures for firewall deployments across all 14 supported platforms. Cover HA modes, session synchronization, configuration synchronization, heartbeat design, and cloud-specific HA patterns.

---

## HA Modes by Vendor

| Vendor | Active/Passive | Active/Active | Clustering | Notes |
|--------|:-:|:-:|:-:|-------|
| **Azure Firewall** | — | ✓ (built-in) | — | Managed service; HA built into the platform via availability zones |
| **AWS Network Firewall** | — | ✓ (built-in) | — | Managed service; multi-AZ endpoint deployment |
| **GCP Cloud Firewall** | — | ✓ (built-in) | — | Managed service; globally distributed |
| **Palo Alto PAN-OS** | ✓ | ✓ | ✓ (PA-7000) | Active/passive or active/active with floating IP and session sync |
| **FortiGate** | ✓ | ✓ | ✓ (FGCP/FGSP) | FGCP (config+session sync) or FGSP (session-only sync for active/active) |
| **Check Point** | ✓ | ✓ (ClusterXL) | ✓ (VSX) | ClusterXL with Load Sharing or HA; Maestro for hyperscale |
| **Cisco ASA/FTD** | ✓ | ✓ | ✓ (FTD multi-instance) | ASA failover (active/standby or active/active for multi-context); FTD HA via FMC |
| **Juniper SRX** | ✓ | ✓ | ✓ (chassis cluster) | Chassis cluster with redundancy groups; `reth` interfaces |
| **Zscaler** | — | ✓ (built-in) | — | Cloud-native; resilience via Zscaler cloud fabric |
| **Sophos XG/XGS** | ✓ | — | ✓ (HA cluster) | Active/passive with dedicated HA link |
| **OPNsense** | ✓ (CARP) | — | — | CARP for VIP failover, pfsync for state sync |
| **pfSense** | ✓ (CARP) | — | — | CARP for VIP failover, pfsync for state sync, xmlrpc for config sync |
| **VyOS** | ✓ (VRRP) | — | — | VRRP for gateway failover; conntrack-sync for state sync |
| **iptables/nftables** | ✓ (keepalived/VRRP) | — | — | keepalived for VRRP + conntrackd for state sync |

---

## Session and Config Synchronization

### Session Sync
Session synchronization replicates the connection/state table between HA peers so that active sessions survive a failover without requiring re-establishment.

| Vendor | Session Sync Mechanism | Key Config |
|--------|----------------------|------------|
| PAN-OS | HA2 link (dedicated interface) | `set deviceconfig high-availability interface ha2` |
| FortiGate (FGCP) | Session sync over HA heartbeat link | `config system ha` → `set session-pickup enable` |
| FortiGate (FGSP) | TCP session sync over dedicated link | `config system standalone-cluster` |
| Check Point | State sync (CCP protocol) over sync interface | ClusterXL sync interface in cluster object |
| ASA | LAN-based failover link (stateful) | `failover link <name> <iface>` + `failover interface ip` |
| SRX | Chassis cluster fabric (fab0/fab1) and control link (em0) | `set chassis cluster` |
| OPNsense | pfsync over dedicated interface | System > HA > State Synchronization > Synchronize Interface |
| pfSense | pfsync over dedicated interface | System > HA > State Synchronization Settings |
| VyOS | conntrack-sync | `set service conntrack-sync interface <iface>` |
| iptables | conntrackd (userspace daemon) | `/etc/conntrackd/conntrackd.conf` — multicast or unicast sync |

### Config Sync
Configuration synchronization ensures both peers have identical policy and settings.

| Vendor | Config Sync Method |
|--------|-------------------|
| PAN-OS | HA1 link — automatic config sync; primary pushes config to secondary |
| FortiGate | HA heartbeat — config sync is automatic in FGCP mode |
| Check Point | SmartConsole installs policy to all cluster members simultaneously |
| ASA | Standby replicates running-config from active unit |
| SRX | Chassis cluster — RE0 (primary) syncs config to RE1 |
| OPNsense | XMLRPC sync from master to backup (System > HA > Settings) |
| pfSense | XMLRPC sync from primary to secondary (System > HA > Settings) |
| VyOS | Manual — no native config sync; use automation (Ansible/scripts) |
| iptables | Manual — use `iptables-save`/`iptables-restore` with rsync or config management |

---

## Heartbeat Network Design

### Dedicated HA Interface Recommendations
- **Minimum**: one dedicated heartbeat link (direct cable or dedicated VLAN).
- **Recommended**: two heartbeat links for redundancy (management + dedicated HA VLAN).
- **Never** route heartbeat traffic through production data interfaces.
- Use a dedicated, non-routable subnet (e.g., 169.254.x.x link-local or a /30 private subnet).

### Heartbeat Timers
| Setting | Typical Value | Purpose |
|---------|---------------|---------|
| Hello interval | 1 second | Frequency of heartbeat probes |
| Dead/hold time | 3–6 seconds | Time before declaring peer dead |
| Preemption delay | 300 seconds | Wait time before primary reclaims after recovery |

> **Split-brain prevention**: Always use at least two independent heartbeat paths. Configure a management interface as a secondary heartbeat. Some vendors support a "monitor" interface that must be up for the node to remain active — use to detect upstream/downstream link failures.

---

## Cloud-Specific HA Patterns

### Azure — Load Balancer + NVA
```
Internet → Azure LB (Standard, HA ports rule) → NVA-1 (active)
                                               → NVA-2 (standby or active)
           Internal LB (HA ports) ← NVA-1 / NVA-2 ← spoke VNets (via UDR)
```
- Use **Azure Standard Load Balancer** with HA ports rule (protocol=all, port=0) for transparent traffic steering.
- **Health probes** determine which NVA receives traffic; failed probe removes NVA from pool.
- **UDRs** in spoke subnets point to the internal LB frontend IP as next hop.
- Azure Firewall has HA built-in — no LB pattern needed.

### AWS — Gateway Load Balancer (GWLB)
```
VPC Route Table → GWLB Endpoint → GWLB → NVA-1 (target group)
                                        → NVA-2 (target group)
```
- **GWLB** distributes traffic to multiple NVA instances in a target group using GENEVE encapsulation.
- Cross-AZ deployment for resilience; health checks remove unhealthy targets.
- **Transit Gateway** integration for centralized inspection.
- AWS Network Firewall is managed — HA is built-in with multi-AZ endpoints.

### GCP — Internal Load Balancer + NVA
```
VPC Routes → Internal TCP/UDP LB → NVA-1 (instance group)
                                  → NVA-2 (instance group)
```
- Use **Internal TCP/UDP Load Balancer** as next-hop for routes.
- Health checks determine active NVA.
- GCP Cloud Firewall is managed — no HA pattern needed.

### Floating IP / EIP Failover (Any Cloud)
- Assign an **Elastic IP** (AWS) or **Secondary IP** (Azure, GCP) to the active NVA.
- On failover, a script or API call moves the floating IP to the standby NVA.
- Slower than LB-based failover (API call latency: 10–30 seconds vs probe-based: 5–15 seconds).

---

## Open-Source HA Patterns

### OPNsense CARP
```bash
# Master node: System > High Availability > Settings
# - Synchronize Interface: em2 (dedicated HA link)
# - pfsync Synchronize Peer IP: 10.0.99.2
# - XMLRPC Sync: enable, target 10.0.99.2
# - Synchronize: Rules, Aliases, NAT, Virtual IPs, Users, DHCP

# Create CARP VIPs: Interfaces > Virtual IPs > Add
# Type: CARP, Interface: LAN, Address: 10.1.1.1/24
# VHID: 1, Advbase: 1, Advskew: 0 (master=0, backup=100)
```

### pfSense CARP / pfsync
```bash
# Primary node: System > High Availability
# State Synchronization Settings:
#   Synchronize States: checked
#   Synchronize Interface: SYNC (dedicated HA interface)
#   pfsync Synchronize Peer IP: 10.0.99.2

# XMLRPC Sync:
#   Synchronize Config to IP: 10.0.99.2
#   Remote System Username: admin
#   Remote System Password: <password>
#   Select: Toggle All (sync firewall rules, NAT, aliases, etc.)

# Create CARP VIPs on both WAN and LAN:
#   Firewall > Virtual IPs > Add
#   Type: CARP, Interface: WAN, Address: <public-VIP>
#   VHID: 1, Advertising Frequency: Base=1, Skew=0 (primary)
```

### VyOS VRRP
```bash
# Configure VRRP on primary
set high-availability vrrp group LAN-GW interface eth1
set high-availability vrrp group LAN-GW vrid 10
set high-availability vrrp group LAN-GW virtual-address 10.1.1.1/24
set high-availability vrrp group LAN-GW priority 200
set high-availability vrrp group LAN-GW preempt true
set high-availability vrrp group LAN-GW preempt-delay 300

# Conntrack sync for session state
set service conntrack-sync accept-protocol tcp,udp,icmp
set service conntrack-sync interface eth2    # dedicated sync interface
set service conntrack-sync mcast-group 225.0.0.50
set service conntrack-sync disable-external-cache

commit
save
```

### iptables + keepalived + conntrackd
```bash
# keepalived.conf on primary
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 200
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass <secret>
    }
    virtual_ipaddress {
        10.1.1.1/24
    }
}

# conntrackd.conf — sync state over dedicated interface
Sync {
    Mode FTFW {
        DisableExternalCache On
    }
    Multicast {
        IPv4_address 225.0.0.50
        Group 3780
        IPv4_interface 10.0.99.1   # dedicated sync IP
        Interface eth2             # dedicated sync interface
    }
}
```

---

## Design Checklist

1. [ ] HA mode selected (active/passive, active/active, clustering) with justification.
2. [ ] Dedicated heartbeat/HA interfaces provisioned (minimum two paths).
3. [ ] Session synchronization configured and verified (stateful failover).
4. [ ] Configuration synchronization enabled (or automated via config management).
5. [ ] Health probes configured (cloud deployments) or heartbeat timers tuned.
6. [ ] Split-brain prevention addressed (dual heartbeat, monitoring interfaces).
7. [ ] Preemption policy decided (preempt on recovery or manual failback).
8. [ ] Failover tested end-to-end with traffic flowing during failover event.
9. [ ] Rollback/recovery procedure documented for HA configuration changes.

---
**Analysis only — verify against vendor documentation before applying.**
