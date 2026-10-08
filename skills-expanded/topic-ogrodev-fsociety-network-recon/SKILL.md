---
name: network-recon
description: |
  Activate this skill whenever the user mentions port scan, port scanning, nmap, nmap scan,
  masscan, rustscan, service detection, service enumeration, service fingerprinting,
  network scan, network scanning, network mapping, network discovery, network topology,
  open ports, closed ports, filtered ports, banner grabbing, banner grab,
  host discovery, live hosts, ping sweep, ARP scan, ARP discovery,
  OS fingerprinting, OS detection, operating system detection, TCP fingerprinting,
  SYN scan, TCP scan, UDP scan, ACK scan, FIN scan, XMAS scan, NULL scan,
  stealth scan, half-open scan, connect scan, idle scan,
  timing template, scan evasion, IDS evasion, IPS bypass, firewall evasion,
  fragmentation scan, decoy scan, source port manipulation,
  DNS reconnaissance, DNS recon, zone transfer, subdomain enumeration,
  subdomain discovery, amass, subfinder, dnsx, dnsenum, fierce,
  DNS brute force, DNS cache snooping, DNSSEC walking,
  network pivoting, SSH tunnel, SOCKS proxy, port forwarding,
  chisel, ligolo, ligolo-ng, double pivot, pivot chain,
  vulnerability scanning, vulnerability scan, Nessus, OpenVAS, nuclei network,
  vulnerability correlation, CVE mapping, service vulnerability,
  autorecon, comprehensive scan, full port scan, top ports,
  SNMP enumeration, SMB enumeration, LDAP enumeration,
  network segmentation, VLAN discovery, subnet scanning,
  internal network scan, external network scan, perimeter scan.
version: 2.0.0
---

# Network Reconnaissance

Network reconnaissance is the systematic process of discovering hosts, mapping open ports, fingerprinting services and operating systems, and identifying vulnerabilities across target networks. It is the foundation of every penetration test -- everything downstream (web testing, exploitation, lateral movement) depends on the quality of your initial network recon.

## Reconnaissance Methodology

Follow this sequence. Each phase feeds the next. Skip phases only when scope explicitly restricts them.

### Phase 1 -- Passive Reconnaissance

Gather intelligence without sending a single packet to the target. This phase has zero detection risk.

**Objectives**: Identify IP ranges, ASNs, known services, historical scan data, DNS records.

```bash
# Passive subdomain enumeration
subfinder -d target.com -silent -o subdomains.txt

# OSINT-based port data (Shodan, Censys)
# Use ctx_execute or Hexstrike MCP tools for API queries
```

**Integration**: Store discovered targets immediately.
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" network "passive-subdomains" "$(wc -l < subdomains.txt) subdomains found" --source "subfinder"
```

### Phase 2 -- Host Discovery

Determine which hosts are alive before port scanning. Scanning dead hosts wastes time and generates noise.

**Tool Selection**:
- **Same LAN**: ARP scan (most reliable, cannot be firewalled)
- **Remote targets**: TCP SYN ping + ICMP + UDP combined
- **Firewall-heavy**: TCP ping on known-open ports (80, 443)

Load: `ToolSearch` -> `select:mcp__hexstrike-ai__arp_scan_discovery` (LAN targets)

```bash
# ARP discovery (local network only)
arp-scan --localnet --interface eth0

# Nmap host discovery combinations
nmap -sn -PE -PP -PS80,443,22 -PU53,161 -T3 10.0.0.0/24    # Standard
nmap -sn -PS80,443,8080,22,25 10.0.0.0/24                    # TCP-only (ICMP blocked)
nmap -sn -PR 10.0.0.0/24                                      # ARP only (local subnet)
```

See `references/host-discovery.md` for complete host discovery methodology.

### Phase 3 -- Port Scanning

Discover open ports on live hosts. Tool selection depends on scope size and OPSEC requirements.

**Tool Ladder** (select based on scenario):

| Scenario | Tool | Speed | Accuracy | Stealth |
|----------|------|-------|----------|---------|
| Quick triage / CTF | RustScan | Fastest | Ports only | None |
| Large scope (>256 hosts) | Masscan | Fast | Ports only | Low |
| Standard engagement | Nmap SYN | Moderate | Good | Moderate |
| Stealth required | Nmap with evasion | Slow | Good | High |
| Maximum accuracy | Nmap TCP connect | Slow | Best | Low |

Load: `ToolSearch` -> `select:mcp__hexstrike-ai__rustscan_fast_scan` (quick discovery)
Load: `ToolSearch` -> `select:mcp__hexstrike-ai__masscan_high_speed` (large scope)
Load: `ToolSearch` -> `select:mcp__hexstrike-ai__nmap_scan` (standard)
Load: `ToolSearch` -> `select:mcp__hexstrike-ai__nmap_advanced_scan` (deep)

```bash
# Standard SYN scan -- all ports
nmap -sS -p- -T4 --open --reason -oA full-syn target.com

# Masscan for speed, then nmap for accuracy
masscan -p1-65535 --rate=1000 -oL masscan-results.txt 10.0.0.0/24
nmap -sV -sC -p$(cat masscan-results.txt | grep open | cut -d' ' -f4 | sort -u | tr '\n' ',') target
```

See `references/port-scanning.md` for scan types, timing, and evasion techniques.

### Phase 4 -- Service Enumeration

Identify service versions, technologies, and configurations on discovered ports.

```bash
# Version detection + default scripts on discovered ports
nmap -sV -sC -p22,80,443,445,3389 -oA service-enum target.com

# Aggressive service detection with OS guess
nmap -sV --version-intensity 9 -A -p- target.com
```

**Post-enumeration**: Log every discovered service to target-intel.
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" service "22/tcp" "OpenSSH 8.9p1 Ubuntu" --source "nmap"
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" service "443/tcp" "nginx 1.18.0" --source "nmap"
```

See `references/service-enum.md` for per-service enumeration tools and techniques.

### Phase 5 -- OS Fingerprinting

Determine operating systems to prioritize exploits and understand the target environment.

```bash
# Active OS detection
nmap -O --osscan-guess target.com

# Combined with service version for best accuracy
nmap -O -sV --version-intensity 5 target.com
```

See `references/os-fingerprinting.md` for active and passive fingerprinting methods.

### Phase 6 -- DNS Reconnaissance

Map the target's DNS infrastructure. Zone transfers, subdomain enumeration, and record analysis.

```bash
# Comprehensive subdomain enumeration
amass enum -d target.com -active -o amass-results.txt

# DNS record types
dig target.com ANY +noall +answer
dig target.com AXFR @ns1.target.com    # Zone transfer attempt
```

See `references/dns-recon.md` for DNS enumeration methodology.

### Phase 7 -- Vulnerability Correlation

Cross-reference discovered services with known vulnerabilities. Map CVEs to exploit potential.

```bash
# Nmap vuln scripts
nmap --script vuln -p22,80,443 target.com

# Nuclei network templates
nuclei -t network/ -target target.com:443
```

See `references/vulnerability-scanning.md` for vulnerability scanning and correlation.

### Phase 8 -- Network Pivoting

When you compromise a host, use it to reach previously inaccessible networks.

See `references/network-pivoting.md` for tunneling, port forwarding, and multi-hop pivot chains.

## OPSEC Profiles and Scan Timing

Every scan decision must account for the active OPSEC profile. Check the current profile before scanning:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/scan-profile.js get
```

### Profile Matrix

| Profile | Nmap Timing | Masscan Rate | Scan Type | Parallelism | Notes |
|---------|-------------|--------------|-----------|-------------|-------|
| **loud** | `-T5` | `--rate=10000` | `-sS` full range | Max parallel | Lab/CTF only. Fastest. No evasion. |
| **normal** | `-T3` | `--rate=1000` | `-sS` with `-sV` | Moderate | Standard authorized tests. Default scripts. |
| **stealth** | `-T2` | `--rate=100` | `-sS` with fragmentation | Sequential | IDS present. Fragment packets. Randomize hosts. |
| **paranoid** | `-T1` or `-T0` | `--rate=10` | `-sS` with full evasion | Single host | Active monitoring. Full evasion suite. |

### Evasion Techniques by Profile

**stealth** profile additions:
```bash
nmap -sS -T2 -f --data-length 24 --randomize-hosts -D RND:5 target
```

**paranoid** profile additions:
```bash
nmap -sS -T1 -f -f --mtu 16 --data-length 48 --randomize-hosts \
  --scan-delay 5s --max-retries 1 --source-port 53 \
  -D RND:10,ME --spoof-mac 0 target
```

See `references/port-scanning.md` for complete evasion flag reference.

## Decision Trees

### Scan Strategy by Engagement Type

```
External Pentest:
  -> Start with passive DNS/OSINT (Phase 1)
  -> Subdomain enumeration (Phase 6)
  -> Port scan discovered hosts (Phase 3)
  -> Service enum on open ports (Phase 4)
  -> Vuln correlation (Phase 7)

Internal Pentest:
  -> ARP scan for host discovery (Phase 2)
  -> Full port scan all live hosts (Phase 3)
  -> Service enum + OS fingerprint (Phase 4-5)
  -> SMB/LDAP/Kerberos enumeration
  -> Vuln scan + lateral movement planning

Red Team:
  -> Passive only initially (Phase 1)
  -> Targeted port scans on high-value hosts (Phase 3, paranoid profile)
  -> Minimal service probes (Phase 4, specific ports only)
  -> Pivot planning (Phase 8)

Bug Bounty:
  -> Subdomain enumeration (Phase 6)
  -> Port scan on in-scope assets (Phase 3)
  -> Web service identification (Phase 4, HTTP/HTTPS focus)
  -> Skip OS fingerprinting unless relevant
```

### Tool Selection by Target Count

```
1 host         -> Nmap full (-p- -sV -sC -A) or AutoRecon
2-10 hosts     -> Nmap with parallelism (--min-hostgroup 4)
11-50 hosts    -> Nmap phased (discovery -> targeted service enum)
51-256 hosts   -> Masscan discovery -> Nmap service enum on hits
256+ hosts     -> Masscan at scale -> Nmap top-ports on hits -> deep enum on interesting
```

Load: `ToolSearch` -> `select:mcp__hexstrike-ai__autorecon_comprehensive` (single-target full auto)

## Data Layer Integration

### Logging Techniques

After every scan, log it to the techniques tracker:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add \
  "nmap" "target.com" "SYN scan full port range" "success" \
  --report "reports/nmap-full-syn.txt" \
  --notes "Found 12 open ports, 3 filtered"
```

### Storing Discovered Intelligence

Store everything in target-intel for cross-session persistence:

```bash
# Services
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" service "80/tcp" "Apache 2.4.52" --source "nmap"

# Network info
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" network "os-guess" "Ubuntu 22.04 (Linux 5.15)" --source "nmap-os"

# Defenses detected
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" defense "firewall" "Filtered ports: 135,139,445" --source "nmap"

# Tech stack
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add "target.com" tech-stack "web-server" "nginx/1.18.0" --source "nmap"
```

### Recording Findings

When scans reveal vulnerabilities, log them immediately:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "target.com:21" "config" "anonymous-ftp" "MEDIUM" \
  "FTP anonymous login enabled with directory listing"
```

## Workflow Integration

### Standard Engagement Flow
1. **RustScan** or **Masscan** for fast port discovery
2. **Nmap** `-sV -sC` on discovered ports for service versions + default scripts
3. **Nmap** `--script vuln` for vulnerability detection
4. **Service-specific tools** based on what is found (enum4linux for SMB, etc.)
5. Log everything to findings-tracker, techniques-tracker, and target-intel
6. Run chain-detector to identify exploit chains

### Handoff to Other Skills

- **HTTP/HTTPS found** -> Route to `web-assessment` skill
- **WordPress detected** -> Route to `wordpress-hacking` skill
- **Cloud metadata found** -> Route to `cloud-lateral` skill
- **API endpoints found** -> Route to `api-testing` skill
- **Credentials needed** -> Route to `password-attacks` skill
- **WAF detected** -> Route to `waf-bypass` skill

## References

| Reference | Coverage |
|-----------|----------|
| `references/port-scanning.md` | SYN/TCP/UDP/ACK/FIN scan types, masscan, timing templates, evasion flags, IDS/IPS bypass, firewall evasion |
| `references/host-discovery.md` | ARP scanning, ICMP probes, TCP/UDP ping, DNS-based discovery, passive methods, Shodan/Censys |
| `references/service-enum.md` | Per-service enumeration (SMB, SSH, HTTP, FTP, MySQL, RDP, LDAP, RPC, SNMP, etc.), NSE scripts, tool mapping |
| `references/os-fingerprinting.md` | Active vs passive fingerprinting, nmap -O, p0f, TTL analysis, TCP window size, stack fingerprinting |
| `references/dns-recon.md` | Zone transfers, subdomain enumeration (amass, subfinder, dnsx), cache snooping, DNSSEC walking, DNS tunneling detection |
| `references/network-pivoting.md` | SSH tunnels, SOCKS proxies, chisel, ligolo-ng, port forwarding chains, double pivots, pivot through compromised hosts |
| `references/vulnerability-scanning.md` | Nessus, OpenVAS, nuclei network templates, nmap vuln scripts, CVE correlation, vulnerability prioritization |
