# Skill: Hardening Checklist

## Purpose

Assess firewall configurations against security hardening best practices. Produce a checklist of findings with CIS Benchmark references where available, covering both management plane and data plane hardening across all 14 supported platforms.

---

## Universal Hardening Items

These apply to **every** firewall platform regardless of vendor:

### Management Plane

| # | Check | Description | CIS Reference |
|---|-------|-------------|---------------|
| M1 | **Restrict management access** | Management interfaces (SSH, HTTPS, API) accessible only from dedicated management zone/subnet | CIS general: 1.x |
| M2 | **Enforce strong authentication** | Require MFA for admin access; use RADIUS/TACACS+/SAML/LDAP integration — no local-only accounts in production | CIS general: 1.x |
| M3 | **Minimum password complexity** | Enforce password length ≥14 characters, complexity requirements, and account lockout after failed attempts | — |
| M4 | **Role-based access control** | Implement RBAC with least-privilege admin roles (read-only, policy-admin, superadmin) | — |
| M5 | **Disable unused management protocols** | Disable HTTP (use HTTPS only), Telnet (use SSH only), SNMPv1/v2 (use v3 or disable) | CIS general: 2.x |
| M6 | **NTP synchronization** | Configure authenticated NTP from trusted sources; accurate timestamps are critical for log correlation | — |
| M7 | **Secure syslog/logging** | Forward logs to external SIEM over TLS; local log storage as backup only | — |
| M8 | **Firmware/OS patching** | Run a supported, patched firmware version; subscribe to vendor security advisories | — |
| M9 | **Configuration backups** | Automate configuration backups; store encrypted copies off-device | — |
| M10 | **Banner/MOTD** | Display legal warning banner on management interfaces | — |

### Data Plane

| # | Check | Description |
|---|-------|-------------|
| D1 | **Default deny** | Last rule in every policy/chain is an explicit deny-all with logging |
| D2 | **No any/any allow** | No rules permitting all traffic between zones without restriction |
| D3 | **Anti-spoofing** | Enable RPF (reverse path forwarding) or equivalent on all interfaces |
| D4 | **Fragment protection** | Drop or reassemble fragmented packets that could bypass inspection |
| D5 | **ICMP rate limiting** | Allow necessary ICMP types (echo-reply, unreachable, TTL exceeded) but rate-limit |
| D6 | **Bogon filtering** | Block RFC 1918, RFC 5737, RFC 6598 on external interfaces (unless NAT applies) |
| D7 | **SYN flood protection** | Enable SYN cookies or SYN proxy on internet-facing interfaces |
| D8 | **Session timeout tuning** | Set appropriate TCP/UDP/ICMP session timeouts — not too long (resource exhaustion) or too short (breaking legitimate flows) |

---

## Per-Vendor Hardening Specifics

### Azure Firewall
- Enable **Threat Intelligence** in "Alert and deny" mode (Standard/Premium).
- Enable **IDPS** in "Alert and deny" mode (Premium).
- Enable **TLS Inspection** for outbound traffic (Premium) — requires CA certificate.
- Use **Structured Logs** (resource-specific tables) over legacy `AzureDiagnostics`.
- Configure **Diagnostic Settings** to send logs to Log Analytics workspace.
- Use **Azure Policy** to enforce Firewall Policy compliance at scale.
- Ref: [CIS Microsoft Azure Foundations Benchmark](https://www.cisecurity.org/benchmark/azure).

### AWS Network Firewall
- Enable **alert and flow logging** to S3 / CloudWatch Logs.
- Use **managed rule groups** (AWS-managed threat signatures) alongside custom rules.
- Enable **strict rule ordering** for stateful rule groups to ensure predictable evaluation.
- Restrict firewall endpoint subnet routing — only route inspected traffic through firewall subnets.
- Ref: [AWS Network Firewall Best Practices](https://docs.aws.amazon.com/network-firewall/latest/developerguide/best-practices.html).

### GCP Cloud Firewall
- Use **service account-based targeting** instead of network tags (more secure, less spoofable).
- Enable **Firewall Rules Logging** on all rules.
- Implement **hierarchical firewall policies** at the organization/folder level for baseline rules.
- Use **Firewall Insights** to identify overly permissive rules and shadowed rules.
- Set VPC-level default to **deny all ingress, allow all egress** (and tighten egress).
- Ref: [CIS Google Cloud Platform Benchmark](https://www.cisecurity.org/benchmark/google_cloud_computing_platform).

### Palo Alto Networks (PAN-OS)
- Enable **Security Profiles** on all allow rules (AV, Anti-Spyware, Vulnerability Protection, URL Filtering, WildFire).
- Configure **Zone Protection Profiles** for flood protection, packet-based attacks, and reconnaissance.
- Enable **User-ID** only on trusted zones — never on untrust.
- Restrict management access via **Permitted IP Addresses** on the management interface.
- Disable **unused GlobalProtect portals/gateways**.
- Enable **log forwarding profiles** on all rules — forward to Panorama/syslog/SIEM.
- Ref: [CIS Palo Alto Networks Firewall Benchmark](https://www.cisecurity.org/benchmark/palo_alto_networks).

### Fortinet FortiGate (FortiOS)
- Enable **UTM profiles** (AV, IPS, Web Filter, App Control) on all allowed traffic policies.
- Set `set admin-sport` to a non-default HTTPS port for management.
- Disable `admin-telnet` and `admin-http`.
- Enable **two-factor authentication** for admin accounts (`config system admin` → `set two-factor`).
- Configure **trusted hosts** for admin accounts to restrict management source IPs.
- Enable `set strong-crypto enable` under `config system global`.
- Disable **auto-install** and **USB auto-install** for firmware/config.
- Ref: [CIS Fortinet FortiGate Benchmark](https://www.cisecurity.org/benchmark/fortinet).

### Check Point (R81+)
- Enable **HTTPS Inspection** blade for encrypted traffic visibility.
- Enable **Anti-Bot**, **Anti-Virus**, **IPS**, and **Threat Emulation** blades.
- Configure **Implicit Cleanup Rule** to log (not just drop silently).
- Restrict SmartConsole access via **GUI Clients** object.
- Disable **cpridstop** — use SIC for secure communication only.
- Enable **Multi-Factor Authentication** for SmartConsole login.
- Ref: [CIS Check Point Firewall Benchmark](https://www.cisecurity.org/benchmark/check_point_firewall).

### Cisco ASA / FTD
- Set `no asdm history enable` if ASDM is not used.
- Enable `threat-detection statistics access-list` for ACL hit monitoring.
- Set `service-policy global_policy global` with inspections for critical protocols.
- Enable **LINA** and **Snort** logging on FTD.
- Disable **unused interfaces** — `shutdown` state.
- Configure `ssh stricthostkeycheck` and limit SSH access via `ssh <ip> <mask> <iface>`.
- Ref: [CIS Cisco Firewall Benchmark](https://www.cisecurity.org/benchmark/cisco).

### Juniper SRX
- Enable **screen** profiles for flood protection, port scanning detection, and IP spoofing.
- Configure `set security zones security-zone <zone> screen <profile>`.
- Disable `set system services telnet` and `set system services finger`.
- Enable `set system login retry-options` for brute-force protection.
- Use `set security log mode stream` and forward to external SIEM.
- Ref: [CIS Juniper Benchmark](https://www.cisecurity.org/benchmark/juniper).

### Zscaler (ZIA / ZPA)
- Enable **SSL Inspection** for all allowed web traffic categories.
- Configure **DLP policies** for sensitive data egress prevention.
- Enable **Cloud Sandbox** (Advanced Cloud Sandbox) for zero-day detection.
- Restrict admin access with **IP-based SAML assertions**.
- Review **default allow rules** — Zscaler ships with permissive defaults.

### Sophos XG / XGS
- Enable **Heartbeat** (Synchronized Security) to integrate with Sophos endpoint agents.
- Set **web admin port** to non-default; disable HTTP access.
- Enable **IPS** and **Application Control** on firewall rules.
- Configure **device access** to restrict management protocols per zone.
- Enable **ATP** (Advanced Threat Protection) for C&C callback detection.

### OPNsense
- **Disable the default anti-lockout rule** after configuring a proper management access rule (System > Settings > Administration > uncheck anti-lockout).
- **Harden the web GUI**: change default port, bind to management interface only, enforce HTTPS with a valid certificate.
- **SSH hardening**: disable password auth (`PasswordAuthentication no`), use key-based auth only, restrict to management interface via System > Settings > Administration.
- Enable **syslog forwarding** over TLS to external SIEM (System > Settings > Logging > Remote).
- Enable **bogon/RFC1918 blocking** on WAN interface (Interfaces > WAN > Block private/bogon networks).
- Disable **unused plugins and services** (VPN servers, DNS resolvers if not needed).
- Configure **rate limiting** via `max-src-conn` and `max-src-conn-rate` on rules.

### pfSense
- **Disable the default anti-lockout rule** (System > Advanced > Admin Access > uncheck anti-lockout) after creating an explicit management rule.
- **Harden web GUI**: bind to LAN/management interface only, use HTTPS with a trusted certificate, change default port.
- **SSH hardening**: disable password authentication, use SSH keys, restrict to management subnet via firewall rules.
- Disable **unused services** (UPnP, mDNS, IGMP Proxy if not needed).
- Enable **bogon and RFC1918 blocking** on WAN (Interfaces > WAN > Block private/bogon networks).
- Configure **pfBlockerNG** for IP reputation and DNS blocklists.
- Disable **DNS Resolver** on WAN if not providing external DNS.

### VyOS
- **Restrict console access**: configure `set system login user <admin>` with strong password and SSH key authentication.
- **Disable unused services**: `delete service telnet`, `delete service dns forwarding` (if not needed), `delete service https` (if managing via SSH only).
- **SSH hardening**: `set service ssh port <non-default>`, `set service ssh disable-password-authentication`.
- **Default DROP policy**: `set firewall name <name> default-action drop` for all rulesets.
- **Rate limiting**: use `set firewall name <name> rule <n> recent count <N> time <seconds>` for SYN flood protection.
- **Connection tracking**: `set system conntrack timeout tcp established 7200` — tune timeouts.
- **Syslog**: `set system syslog host <server> facility all level info` — forward to SIEM.
- **NTP**: `set system ntp server <server>` — use authenticated NTP.

### iptables / nftables
- **Default DROP policy** on all chains:
  ```bash
  iptables -P INPUT DROP
  iptables -P FORWARD DROP
  iptables -P OUTPUT DROP   # or ACCEPT if egress filtering is handled differently
  ```
- **Rate limiting** for SSH and management:
  ```bash
  iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW \
    -m recent --set --name SSH
  iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW \
    -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
  ```
- **Connection tracking** — allow established/related early in chains:
  ```bash
  iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
  iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
  ```
- **Drop invalid packets**:
  ```bash
  iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
  ```
- **Anti-spoofing via RPF**: enable `rp_filter` in sysctl:
  ```bash
  sysctl -w net.ipv4.conf.all.rp_filter=1
  ```
- **Persist rules**: use `iptables-persistent` or `nft list ruleset > /etc/nftables.conf` with systemd unit.

---

## Checklist Output Format

```
=== FIREWALL HARDENING ASSESSMENT ===
Platform:     [vendor / version]
Date:         [assessment date]

MANAGEMENT PLANE
  [✓] M1 — Management access restricted to 10.0.0.0/24
  [✗] M2 — MFA not enabled for admin accounts
  [✓] M3 — Password policy meets complexity requirements
  ...

DATA PLANE
  [✓] D1 — Default deny rule present with logging
  [✗] D2 — Rule 14 has any/any allow (Critical)
  [✓] D3 — Anti-spoofing (RPF) enabled on all interfaces
  ...

VENDOR-SPECIFIC
  [✗] VS1 — Zone Protection Profile not applied to untrust zone
  [✓] VS2 — Security profiles attached to all allow rules
  ...

Score: 18/25 checks passed (72%)
Critical Gaps: 2 (M2, D2)
```

---
**Analysis only — verify against vendor documentation before applying.**
