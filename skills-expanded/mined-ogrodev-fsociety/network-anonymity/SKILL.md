---
name: network-anonymity
description: |
  Network anonymity and traffic concealment for red team operations. Use this skill whenever
  the user mentions "proxy chain", "proxychains", "SOCKS5", "Tor", "onion routing", "VPN",
  "WireGuard", "OpenVPN", "multi-hop", "IP rotation", "MAC spoofing", "MAC randomization",
  "macchanger", "DNS leak", "WebRTC leak", "IPv6 leak", "identity rotation", "anonymity",
  "traffic analysis", "traffic obfuscation", "SSH tunnel", "stunnel", "domain fronting",
  "DNS over HTTPS", "DoH", "DoT", "DNS privacy", "killswitch", "VPN killswitch",
  "network fingerprint", "hostname spoofing", "OS fingerprint", "TTL manipulation",
  "OPSEC", "operational security", "anonymous operations", "circuit control",
  "bridge relay", "obfs4", or discusses anonymous network operations, concealing network
  identity, preventing traffic correlation, or building anonymity layers for engagements.
  Also trigger when the user needs to verify their anonymity setup, test for leaks, or
  design a multi-hop network architecture for different threat models.
version: 2.0.0
---

# Network Anonymity

Multi-layered network anonymity for red team operations -- proxy chains, VPN tunnels, Tor routing, traffic obfuscation, MAC/fingerprint hardening, DNS privacy, and comprehensive leak prevention. Every technique maps to trenton's four opsec profiles so operators can scale anonymity to their threat model.

## Opsec Profile Integration

Each opsec profile prescribes a different anonymity posture. Read the relevant reference files for implementation details at each level.

| Profile | Network Layers | DNS | MAC/Fingerprint | Leak Testing | Reference Priority |
|---------|---------------|-----|-----------------|--------------|-------------------|
| **loud** | Direct connection | System default | No changes | None | -- |
| **normal** | Single VPN or SOCKS5 proxy | VPN-pushed DNS | Optional MAC rotation | Basic IP check | `vpn-killswitch.md` |
| **stealth** | VPN + Tor chain, killswitch active | Encrypted DNS (DoH/DoT) through tunnel | MAC randomized per session | Full leak suite every 30min | All references |
| **paranoid** | Multi-hop VPN + Tor + proxy, killswitch + IPv6 disabled | DNS over Tor only | MAC + hostname + timezone + OS fingerprint hardened | Continuous monitoring | All references |

Set the active profile before configuring anonymity layers:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/opsec-profile.js" set <profile>
node "${CLAUDE_PLUGIN_ROOT}/scripts/opsec-profile.js" show
```

## Reference Files

Read these based on the task at hand. Each file is self-contained with actionable commands and configurations.

| Reference | When to Read | Contents |
|-----------|-------------|----------|
| `references/proxy-chain-setup.md` | Setting up proxy chains, Tor integration, multi-hop architectures, SOCKS5 routing, identity rotation | Proxychains4 configuration, Tor circuit control, multi-hop designs per opsec profile, operational proxy patterns |
| `references/vpn-killswitch.md` | VPN setup, killswitch configuration, leak prevention, IPv6 hardening | WireGuard/OpenVPN killswitch (iptables/nftables/ufw), IPv6 disable, WebRTC mitigation, comprehensive leak testing |
| `references/dns-privacy.md` | DNS leak prevention, encrypted DNS, DNS over Tor | DoH, DoT, DNSCrypt, DNS over Tor, systemd-resolved lockdown, resolv.conf immutability |
| `references/traffic-obfuscation.md` | Hiding traffic patterns, tunneling through restrictive networks, evading DPI | SSH tunnels, stunnel/TLS wrapping, domain fronting, protocol obfuscation, traffic shaping |
| `references/mac-and-fingerprint.md` | MAC spoofing, hostname changes, OS fingerprint reduction, network metadata cleanup | macchanger workflows, hostname/timezone hardening, TCP/IP stack tuning, passive OS fingerprint evasion |

## Workflow

### 1. Baseline Assessment

Before deploying anonymity layers, capture the current network identity so you can verify changes and detect regressions.

```bash
# Capture current network fingerprint
echo "=== Network Identity Baseline ==="
echo "Public IP: $(curl -s --max-time 5 https://api.ipify.org)"
echo "DNS Resolver: $(dig +short whoami.akamai.net 2>/dev/null || echo 'dig unavailable')"
echo "IPv6: $(curl -6 -s --max-time 5 https://api6.ipify.org 2>/dev/null || echo 'disabled/blocked')"
echo "Hostname: $(hostname)"
echo "MAC (primary): $(ip link show $(ip route show default | awk '/default/ {print $5}') | awk '/ether/ {print $2}')"
```

### 2. Layer Deployment Order

Deploy anonymity layers bottom-up. Each layer builds on the previous one.

```
Layer 0: MAC + hostname + fingerprint hardening  →  references/mac-and-fingerprint.md
Layer 1: VPN tunnel + killswitch                 →  references/vpn-killswitch.md
Layer 2: DNS privacy (encrypted DNS through VPN) →  references/dns-privacy.md
Layer 3: Tor / proxy chain on top of VPN         →  references/proxy-chain-setup.md
Layer 4: Traffic obfuscation (if DPI is a threat) →  references/traffic-obfuscation.md
```

Not every engagement needs all layers. The opsec profile determines which layers to deploy:
- **loud**: Skip all layers
- **normal**: Layer 1 only
- **stealth**: Layers 0-3
- **paranoid**: Layers 0-4

### 3. Verification

After deploying layers, run the leak test suite. See `references/vpn-killswitch.md` for the full test battery.

```bash
# Quick verification (run after every layer change)
echo "Exit IP: $(proxychains4 -q curl -s --max-time 10 https://api.ipify.org 2>/dev/null || curl -s --max-time 10 https://api.ipify.org)"
echo "DNS: $(proxychains4 -q dig +short whoami.akamai.net 2>/dev/null || dig +short whoami.akamai.net)"
echo "IPv6: $(curl -6 -s --max-time 5 https://api6.ipify.org 2>/dev/null && echo 'LEAK DETECTED' || echo 'blocked')"
echo "Tor: $(curl -s --max-time 10 https://check.torproject.org/api/ip 2>/dev/null | grep -o '"IsTor":[a-z]*')"
```

### 4. Continuous Monitoring

For stealth and paranoid profiles, schedule periodic leak checks during operations.

```bash
# Background leak monitor (runs every N seconds based on profile)
INTERVAL=1800  # stealth=1800, paranoid=300
while true; do
    IP=$(curl -s --max-time 10 https://api.ipify.org 2>/dev/null)
    DNS=$(dig +short whoami.akamai.net 2>/dev/null)
    IPV6=$(curl -6 -s --max-time 5 https://api6.ipify.org 2>/dev/null)
    [ -n "$IPV6" ] && echo "[ALERT] IPv6 leak detected: $IPV6"
    echo "[$(date +%H:%M:%S)] IP=$IP DNS=$DNS"
    sleep $INTERVAL
done
```

### 5. Teardown

Reverse the deployment order when ending operations. For paranoid profile, run anti-forensics cleanup afterward (cross-reference: `anti-forensics` skill).

```
Teardown order: Layer 4 → 3 → 2 → 1 → 0
- Remove proxy/Tor configuration
- Restore DNS settings (unlock resolv.conf)
- Disable killswitch, restore original firewall rules
- Restore original MAC and hostname
- Clear connection logs, bash history entries related to anonymity setup
```

## Logging

Log all network anonymity operations for engagement records:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" add \
  --category "network-anonymity" \
  --action "<action>" \
  --detail "<detail>"
```

Log identity changes (MAC, IP, hostname rotations):
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/identity-tracker.js" add \
  <type> <interface> <old-value> <new-value>
```

## Cross-Skill References

| Scenario | Skill | Why |
|----------|-------|-----|
| Hardening the underlying OS before deploying anonymity layers | `system-hardening` | Firewall, kernel params, SSH config |
| Setting up a VPS as a proxy hop or C2 relay | `vps-security` | Encrypted storage, provisioning, auto-updates |
| Cleaning traces after an operation | `anti-forensics` | Log manipulation, metadata stripping, secure deletion |
| Generating opsec compliance reports | `opsec-reporting` | Report templates for documenting anonymity posture |
