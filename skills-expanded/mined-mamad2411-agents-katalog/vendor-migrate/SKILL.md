# Skill: Vendor Migration

## Purpose

Plan and execute firewall rule-base migrations between any pair of the 14 supported vendor platforms. Produce migration playbooks covering export, normalization, translation, testing, and cutover with rollback procedures.

---

## Common Migration Pairs

| Source | Target | Complexity | Notes |
|--------|--------|------------|-------|
| Cisco ASA → Palo Alto PAN-OS | High | Port-based → App-ID translation required; NAT syntax differs significantly |
| Check Point → Palo Alto PAN-OS | Medium | Both zone-based; App Control → App-ID mapping available via Expedition |
| FortiGate → Palo Alto PAN-OS | Medium | UTM profiles → Security Profiles mapping; policy structure similar |
| Cisco ASA → FortiGate | Medium | ACL-based → policy-based; object syntax differs |
| Any → Azure Firewall | Medium–High | On-prem L7 features may not have cloud equivalents; IaC generation needed |
| Any → AWS Network Firewall | Medium–High | Suricata rule syntax; stateless/stateful split |
| pfSense → OPNsense | Low | Fork relationship; config.xml largely compatible with manual adjustments |
| iptables → nftables | Low–Medium | Direct syntax translation; nftables is more expressive |
| On-prem → Zscaler ZIA | High | Shift from perimeter firewall to cloud-delivered proxy model |
| Juniper SRX → Palo Alto PAN-OS | Medium | Both zone-based; application ID mapping needed |
| Sophos XG → FortiGate | Medium | Zone/object mapping; UTM profile equivalences |
| VyOS → OPNsense/pfSense | Medium | CLI-based → GUI/API-based; zone-policy to interface-rule conversion |

---

## Migration Phases

### Phase 1 — Pre-Migration Assessment

1. **Inventory** the source rule base:
   - Total rule count, object count (addresses, services, groups).
   - Rule hit counts — identify unused rules for exclusion.
   - NAT rules (source NAT, destination NAT, exemptions).
   - VPN policies (if firewall manages VPN).
2. **Audit** the source rules using the [Rule Audit](../rule-audit/SKILL.md) skill — clean up before migrating.
3. **Map features** — identify source features that have no direct target equivalent:
   - App-ID / application control → port-based fallback.
   - Custom IPS signatures → target vendor signature format.
   - Scheduling / time-based rules → target scheduler syntax.
4. **Document** the current topology: interfaces, zones, routing, HA configuration.

### Phase 2 — Export and Normalize

**Export** the source configuration in a structured format:

```bash
# PAN-OS: XML export
curl -k "https://<fw>/api/?type=export&category=configuration&key=<key>" -o pan-config.xml

# FortiGate: Full config backup
FGT# execute backup config tftp <filename> <tftp-server>
# Or REST API:
curl -k "https://<fg>/api/v2/monitor/system/config/backup?scope=global" -H "Authorization: Bearer <token>" -o fg-config.conf

# Cisco ASA: Show running config
ASA# show running-config | redirect tftp://<server>/asa-config.txt

# Check Point: Export via mgmt_cli
mgmt_cli show access-rulebase name "Network" details-level full -f json > cp-rules.json

# Juniper SRX: Export config
> show configuration security | display json | no-more > srx-config.json

# OPNsense: Backup config.xml via API
curl -u "<key>:<secret>" "https://<opnsense>/api/core/backup/download/this" -o opnsense-config.xml

# pfSense: Download config.xml via GUI or SCP from /cf/conf/config.xml

# VyOS: Export configuration commands
$ show configuration commands | grep firewall > vyos-fw-rules.txt

# iptables: Export
iptables-save > iptables-export.txt

# nftables: Export
nft list ruleset > nftables-export.txt
```

**Normalize** to a vendor-neutral intermediate format:

| Field | Description |
|-------|-------------|
| rule_id | Sequential rule number |
| name | Rule name / description |
| source_zone | Source zone name |
| dest_zone | Destination zone name |
| source_addr | Source address objects (CIDR or FQDN) |
| dest_addr | Destination address objects |
| service | Protocol/port or application name |
| action | allow / deny / drop / reject |
| logging | enabled / disabled |
| schedule | Time-based schedule (if any) |
| hit_count | Observed hit count from source |
| comment | Migration notes |

### Phase 3 — Translation

**Key Translation Challenges:**

| Challenge | Details |
|-----------|---------|
| **App-ID → Port-Based** | PAN-OS/FortiGate application objects must be mapped to port/protocol pairs for targets without app awareness (Azure FW, iptables, VyOS, pfSense) |
| **Object Naming** | Each vendor has different naming constraints (length, characters, case sensitivity). PAN-OS allows spaces (in quotes), ASA does not; FortiGate names are case-insensitive; iptables has no named objects |
| **NAT Syntax** | ASA auto-NAT vs twice-NAT; PAN-OS NAT policy; FortiGate central-NAT vs per-policy NAT; iptables SNAT/DNAT/MASQUERADE; nftables `snat`/`dnat`; pfSense/OPNsense NAT via pf.conf |
| **Zone Model** | SRX/PAN-OS are natively zone-based; ASA uses security levels; iptables uses chains; pfSense/OPNsense use interface-based rules; VyOS uses zone-policy |
| **Rule Ordering** | Some platforms are strict sequence (FortiGate, ASA); others use priority numbers (Azure FW, GCP); iptables/pfSense/OPNsense are first-match per chain/interface |
| **Group Nesting** | Some platforms support nested address groups (PAN-OS, Check Point); others do not (ASA, iptables) — flatten groups during translation |
| **Implicit Rules** | Check Point has implicit cleanup rule; pfSense has implicit anti-lockout; VyOS has default-action per zone — account for these in translation |

### Phase 4 — Build and Validate

1. **Build** the target configuration from the normalized rule set.
2. **Lab test** — deploy in a non-production environment and simulate traffic flows.
3. **Validate** using the target vendor's diagnostic tools:
   - PAN-OS: `test security-policy-match`
   - FortiGate: `diagnose firewall iprope lookup`
   - ASA: `packet-tracer`
   - SRX: `show security match-policies`
   - pfSense/OPNsense: `pfctl -sr` + test traffic
   - VyOS: `show firewall name <name> statistics` + test traffic
   - iptables: `iptables -C` (check) + TRACE target

### Phase 5 — Parallel Run and Cutover

1. **Parallel run** — both source and target firewalls process traffic (via traffic mirroring or split routing) for 7–14 days.
2. **Compare hit counts** — rules matching on the source should match on the target. Investigate discrepancies.
3. **Cutover** — redirect traffic to the target firewall:
   - Update routing (BGP/OSPF/static routes).
   - Update cloud route tables (Azure UDR, AWS route tables, GCP routes).
   - Switch DNS if applicable.
4. **Rollback plan** — keep the source firewall ready for immediate revert for a minimum of 7 days post-cutover.
5. **Decommission** — after rollback window, archive the source config and decommission.

---

## Conversion Examples

### Example 1: Cisco ASA → Palo Alto PAN-OS

**Source (ASA):**
```
object network WEB-SERVER
 host 10.1.1.10
object-group service WEB-PORTS tcp
 port-object eq 80
 port-object eq 443
access-list OUTSIDE_IN extended permit tcp any object WEB-SERVER object-group WEB-PORTS
access-group OUTSIDE_IN in interface outside
```

**Target (PAN-OS):**
```
set address WEB-SERVER ip-netmask 10.1.1.10/32
set service WEB-PORTS protocol tcp port 80,443
set rulebase security rules "Allow-Inbound-Web" from untrust to dmz source any destination WEB-SERVER application web-browsing ssl action allow log-end yes
```

### Example 2: iptables → nftables

**Source (iptables):**
```bash
iptables -A FORWARD -i eth0 -o eth1 -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -p tcp --sport 443 -m state --state ESTABLISHED -j ACCEPT
```

**Target (nftables):**
```bash
nft add rule inet filter forward iifname "eth0" oifname "eth1" tcp dport 443 ct state new,established accept
nft add rule inet filter forward iifname "eth1" oifname "eth0" tcp sport 443 ct state established accept
```

### Example 3: pfSense → OPNsense

**Approach:**
1. Export pfSense `config.xml` from Diagnostics > Backup & Restore.
2. OPNsense can import pfSense config.xml during initial setup wizard (with caveats).
3. **Manual adjustments required:**
   - Package differences (pfBlockerNG → OPNsense os-blocklist or Zenarmor).
   - Snort → Suricata (OPNsense uses Suricata natively).
   - Check alias formats — OPNsense aliases may need type adjustments.
   - Verify NAT rules — pf.conf syntax is compatible but GUI representations differ.
4. After import, run `pfctl -sr` on OPNsense to verify loaded rules match expectations.
5. Test CARP/pfsync HA if applicable — OPNsense CARP config may need interface re-mapping.

---

## Automated Migration Tools

| Tool | Vendor Support | Notes |
|------|---------------|-------|
| **Palo Alto Expedition** | Cisco ASA, Check Point, FortiGate → PAN-OS | **EOL/unsupported** — do not plan new migrations around Expedition; use supported Palo Alto migration paths such as Strata Cloud Manager workflows and verify current guidance: https://live.paloaltonetworks.com/t5/expedition-articles/important-update-end-of-life-announcement-for-palo-alto-networks/ta-p/589642 |
| **Tufin SecureTrack/SecureChange** | Multi-vendor policy management and migration | Commercial; supports most enterprise firewalls |
| **AlgoSec FireFlow** | Multi-vendor change management | Commercial; includes migration workflows |
| **FireMon** | Multi-vendor policy analysis | Commercial; helps with pre-migration audit |
| **fwbuilder** | iptables, PF, Cisco, Juniper | Open-source; multi-platform policy compiler |
| **Manual scripting** | Any → Any | Python/Ansible scripts for custom translations; most flexible |

---
**Analysis only — verify against vendor documentation before applying.**
