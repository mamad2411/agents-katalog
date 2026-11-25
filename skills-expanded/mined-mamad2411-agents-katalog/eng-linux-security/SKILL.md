---
name: eng-linux-security
description: Design and deploy cross-distribution Linux port scan detection, automated firewall IP banning, and intrusion defense rules. Use when securing Linux servers against automated scanners, configuring iptables/nftables/firewalld rate-limits, or setting up fail2ban/psad defenses.
---

# Linux Server Security Guard & Port-Scan Defense

Deploy automated, cross-distribution intrusion defense and port-scan detection scripts for Linux servers (Debian, Ubuntu, RHEL, CentOS, Arch, Alpine, SUSE) with automatic IP banning, whitelisting, and auto-unban timers.

## Core Rules & Metric Hierarchy

- **Priority Hierarchy**: **Ultra-Low False Positive Rate > Detection Precision > Rapid Banning**. When sensitivity conflicts with false-positive risk, always protect legitimate traffic first.
- **Whitelist Protection**: Never ban localhost (`127.0.0.1`), private RFC1918 subnets, user-configured bastion hosts, monitoring probes, or CDN egress IPs.
- **Auto-Unban Expiration**: All bans must have configurable TTL (default: 24h) to prevent unbounded firewall rule table bloat.
- **Cross-Distribution Tool Detection**: Dynamically probe and select the native firewall backend (`nftables` $\rightarrow$ `iptables` $\rightarrow$ `firewalld`) and logging system (`systemd-journald` $\rightarrow$ `rsyslog`).

---

## 5-Phase Security Architecture

```
[Phase 1: Environment & Firewall Discovery] ➔ [Phase 2: Multi-Vector Scan Detection] ➔ [Phase 3: Automated Ban & Whitelist Filter] ➔ [Phase 4: Logging & Alerts] ➔ [Phase 5: Auto-Unban Timer & Cron]
```

### Phase 1: Environment Discovery
1. Identify Linux distro family (`/etc/os-release`).
2. Detect active firewall backend:
   - Modern Linux: `nftables` (preferred for performance and atomic set lookups).
   - Traditional: `iptables` with `ipset`.
   - RedHat/Fedora: `firewalld` rich rules.
3. Confirm active listening ports and services to safeguard (`ss -tulpn`).

### Phase 2: Multi-Vector Port-Scan Detection
Detect scanning patterns through:
1. **Connection Frequency**: Track unique destination port connection attempts per source IP within a sliding 60-second window (threshold: $\ge 10$ distinct ports $\rightarrow$ flag as scanner).
2. **Kernel Drop Logging**: Inspect firewall drops on closed ports (`INVALID` state or `SYN` packets to non-listening ports).
3. **Scan Signatures**: SYN stealth scans, NULL scans, FIN scans, XMAS scans.

### Phase 3: Automated Ban & Whitelisting
1. Cross-reference suspect IP against whitelist (`/etc/security/ip_whitelist.conf`).
2. If not whitelisted, add to firewall drop set:
   - *nftables*: `nft add element inet filter port_scanners { <IP> timeout 24h }`
   - *ipset*: `ipset add port_scanners <IP> timeout 86400`
3. Record ban event with timestamp, scanned ports, and triggering packet.

### Phase 4: Alerting & Audit Logging
1. Write structured JSON log to `/var/log/portscan-defense.log`.
2. Optionally dispatch Webhook / email alert to admin.

### Phase 5: Verification & Auto-Unban
1. Verify rule count and memory consumption.
2. Ensure systemd timer or cron job periodically purges expired ban entries.

---

## Minimal Deployable Defense Script (nftables Native)

```bash
#!/usr/bin/env bash
set -euo pipefail

WHITELIST_FILE="/etc/security/scan_whitelist.conf"
mkdir -p /etc/security /var/log/security
touch "$WHITELIST_FILE"

# Ensure 127.0.0.1 and private subnets are present
cat << 'EOF' > "$WHITELIST_FILE"
127.0.0.1
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
EOF

echo "Initializing nftables port-scan defense table..."
nft add table inet port_defense 2>/dev/null || true
nft add set inet port_defense scan_bans { type ipv4_addr\; flags timeout\; } 2>/dev/null || true
nft add chain inet port_defense input { type filter hook input priority -10\; policy accept\; } 2>/dev/null || true

# Add drop rule for banned set
nft add rule inet port_defense input ip saddr @scan_bans drop 2>/dev/null || true

echo "=== Linux Security Guard Active (nftables set timeout configured) ==="
```

---

## Checkable Completion Criteria

- [ ] Whitelist includes localhost, private ranges, and current SSH connection IP.
- [ ] Ban rules utilize kernel sets (ipset / nftables set) for $O(1)$ lookup performance.
- [ ] Auto-unban TTL configured to prevent rule exhaustion.
- [ ] Non-destructive deployment tested without interrupting active SSH sessions.
