# Skill: Firewall Policy Design

## Purpose

Design zone-based firewall policy architectures from requirements. Produce structured policy sets with explicit allow rules, default deny, application-aware inspection, NAT design, and logging strategy — tailored to the target vendor platform.

---

## Core Design Principles

1. **Default Deny** — Every zone transition that is not explicitly permitted is denied. The last rule in every policy set is an explicit deny-all with logging enabled.
2. **Least Privilege** — Rules specify the narrowest source, destination, and service possible. No `any/any` unless there is a documented, risk-accepted justification.
3. **Zone-Based Architecture** — Traffic policy is defined by zone transitions (from-zone → to-zone), not by interface. Zones abstract the underlying topology.
4. **Application Awareness** — Where the platform supports it (PAN-OS App-ID, FortiGate App Control, Check Point App Control, SRX AppSecure), prefer application-level policies over port-based rules.
5. **Logging by Default** — All allow rules log at session-end (or equivalent). Deny rules log at session-start. Management zone traffic may log at a reduced level to avoid noise.

---

## Zone Taxonomy

| Zone | Purpose | Typical Assets | Trust Level |
|------|---------|----------------|-------------|
| **Trust** (Inside/LAN) | Internal corporate network | Workstations, internal servers, printers | High |
| **Untrust** (Outside/WAN) | Internet, external networks | External endpoints, SaaS, CDNs | None |
| **DMZ** | Publicly accessible services | Web servers, reverse proxies, mail relays | Low |
| **Management** | Device management plane | Firewall GUI/SSH, SNMP, syslog collectors | Highest (restricted) |
| **Guest** | Untrusted internal users | BYOD, visitor Wi-Fi | None (treated as untrust) |
| **Database** | Data tier | Database servers, data warehouses | High (isolated) |
| **Application** | Application tier | App servers, middleware, API gateways | Medium-High |

---

## Zone-Transition Policy Matrix Template

| From \ To | Untrust | DMZ | Trust | Database | Application | Management |
|-----------|---------|-----|-------|----------|-------------|------------|
| **Untrust** | — | Allow (HTTPS, SMTP) | Deny | Deny | Deny | Deny |
| **DMZ** | Allow (outbound updates) | — | Deny | Allow (DB port) | Allow (API port) | Deny |
| **Trust** | Allow (web, DNS, VPN) | Allow (management) | — | Allow (DB port) | Allow (app ports) | Allow (SSH, HTTPS) |
| **Database** | Deny | Deny | Allow (responses) | — | Deny | Deny |
| **Application** | Allow (API calls) | Deny | Allow (responses) | Allow (DB queries) | — | Deny |
| **Management** | Deny | Allow (monitoring) | Allow (monitoring) | Allow (monitoring) | Allow (monitoring) | — |

Each cell represents a policy — expand into specific rules with source/destination objects, services, and application IDs.

---

## L3/L4 vs L7 Policy Guidance

| Layer | Use When | Vendor Features |
|-------|----------|-----------------|
| **L3/L4** (IP, port) | Simple allow/deny by network and port; legacy apps; high-throughput paths where DPI is not needed | All platforms support L3/L4 |
| **L7** (Application) | Distinguishing apps on the same port (e.g., YouTube vs Google Drive on 443); granular SaaS control; threat inspection | PAN-OS App-ID, FortiGate App Control, Check Point App Control, SRX AppSecure, Zscaler app-aware policies, Sophos application rules |
| **Hybrid** | L7 where supported, L3/L4 as fallback for platforms without application awareness | OPNsense (Zenarmor plugin), pfSense (Snort/Suricata for IDS but not inline app policy), VyOS (L3/L4 only), iptables/nftables (L3/L4 only, use L7 proxies for app control) |

---

## Per-Vendor Zone Mapping

### Azure Firewall
- Zones map to Azure VNet subnets or IP Groups.
- Rule Collection Groups act as zone-transition containers (priority-ordered).
- Use Application Rule Collections for L7 (FQDN, HTTP/S) and Network Rule Collections for L3/L4.

### AWS Network Firewall
- Zones map to VPC subnets; route table entries steer traffic through firewall endpoints.
- Stateful rule groups define zone-transition policies.
- Domain-based filtering available via stateful rules with HTTP host header inspection.

### GCP Cloud Firewall
- Zones map to VPC networks or target tags / service accounts.
- Priority-based rules; lower number = higher priority.
- Hierarchical firewall policies for organization-wide zone policy.

### Palo Alto Networks (PAN-OS)
- Native zone-based architecture: `set network zone <name>`.
- Policies: `set rulebase security rules <name> from <zone> to <zone>`.
- App-ID replaces port-based rules for supported applications.

### Fortinet FortiGate
- Zones created via `config system zone`; interfaces assigned to zones.
- Policy: `config firewall policy` with `srcintf` / `dstintf` referencing zones.
- Application control profile attached to policies for L7 inspection.

### Check Point
- Zones defined as network objects (networks, groups) in SmartConsole.
- Security Policy layers: Access Control → Threat Prevention → HTTPS Inspection.
- App Control blade for L7 application awareness.

### Cisco ASA / FTD
- ASA: security levels per interface (0=untrust, 100=trust); nameif assigns zone names.
- FTD: security zones defined in FMC; policies reference zone pairs.
- ACLs bound to interfaces via `access-group`.

### Juniper SRX
- Native zone model: `set security zones security-zone <name> interfaces <iface>`.
- Policies: `set security policies from-zone <src> to-zone <dst> policy <name>`.
- AppSecure for application identification.

### Zscaler
- Zones defined as locations / sub-locations (ZIA) or app segments (ZPA).
- Firewall filtering rules apply to internet-bound traffic (ZIA).
- ZPA policies define access per application — no traditional zone model.

### Sophos XG / XGS
- Zones are interface groupings (LAN, WAN, DMZ, VPN, Wi-Fi, custom).
- Firewall rules reference source/destination zones.
- Application control and IPS profiles attach to rules.

### OPNsense
- No native zone object — zones are represented by interface groupings and aliases.
- Rules are per-interface (floating rules for cross-interface policy).
- Zone-policy model achieved via: interface rules + floating rules for inter-zone control.
- Zenarmor plugin adds application-layer visibility and policy.

### pfSense
- Similar to OPNsense — zones map to interfaces (LAN, WAN, OPT1, OPT2, etc.).
- Rules are per-interface, processed top-down, first-match wins.
- Floating rules for cross-interface policies.
- Application-layer filtering via Snort/Suricata packages (IDS/IPS mode, not inline app policy).

### VyOS
- Zone-policy model: `set zone-policy zone <name> interface <iface>`.
- Firewall rulesets assigned to zone transitions: `set zone-policy zone <name> from <zone> firewall name <ruleset>`.
- Default action per zone: `set zone-policy zone <name> default-action drop`.
- L3/L4 only — no native application awareness.

### iptables / nftables
- Zones map to interfaces or interface groups.
- Chain design:
  - `INPUT` — traffic to the firewall itself (management zone).
  - `FORWARD` — traffic passing through the firewall (inter-zone).
  - `OUTPUT` — traffic from the firewall itself.
- Custom chains for per-zone-pair policies: e.g., `TRUST_TO_DMZ`, `DMZ_TO_DB`.
- nftables equivalent: named chains within the `inet filter` table.

```bash
# iptables zone-chain example
iptables -N TRUST_TO_DMZ
iptables -A FORWARD -i eth1 -o eth2 -j TRUST_TO_DMZ
iptables -A TRUST_TO_DMZ -p tcp --dport 443 -j ACCEPT
iptables -A TRUST_TO_DMZ -j DROP

# nftables equivalent
nft add chain inet filter trust_to_dmz
nft add rule inet filter forward iifname "eth1" oifname "eth2" jump trust_to_dmz
nft add rule inet filter trust_to_dmz tcp dport 443 accept
nft add rule inet filter trust_to_dmz drop
```

---

## Logging and Alerting Strategy

| Zone Transition | Log Level | Alert |
|-----------------|-----------|-------|
| Untrust → Any | All denied, all allowed (session-end) | Alert on any allowed (new rule match) |
| Any → Management | All (every packet) | Alert on any non-whitelisted access |
| DMZ → Database | All allowed and denied | Alert on denied (potential compromise) |
| Trust → Untrust | Session-end logging | Alert on unusual volume or destinations |
| Intra-zone (same zone) | Denied only | Alert on repeated denies (lateral movement) |

---

## Design Deliverables

1. **Zone diagram** — visual representation of zones and allowed transitions.
2. **Zone-transition matrix** — table of from/to zone with allowed services.
3. **Object definitions** — address objects/groups, service objects/groups, application groups.
4. **Rule set** — ordered list of rules per zone transition.
5. **NAT rules** — source NAT, destination NAT, and NAT exemptions.
6. **Logging policy** — per-rule logging configuration and log forwarding destinations.
7. **Vendor-specific config** — ready-to-review configuration in the target vendor's syntax.

---
**Analysis only — verify against vendor documentation before applying.**
