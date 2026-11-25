---
name: nmap
description: >
  Build, extend, and operate nmap — the industry-standard network mapper and port scanner.
  Use when performing host discovery, port scanning, service enumeration, OS detection, or
  running NSE scripts during penetration testing engagements or network audits. Covers host
  discovery techniques, scan types (SYN, TCP, UDP, version, script), timing templates, NSE
  scripting categories, output formats, firewall evasion, performance tuning, and integration
  with Metasploit db_nmap and downstream tools.
license: NPSL / GPLv2
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/nmap/nmap
  language: C/Lua
---

# nmap Agent Skill

## When to Use This Skill

Use this skill when:
- Running port scans or host discovery during a penetration test or network audit
- The user asks about nmap flags, scan types, or NSE scripts
- Enumerating services, versions, or operating systems on a target network
- Writing or running custom NSE scripts
- Evading firewall rules or IDS during authorized red team engagements
- Integrating nmap output with Metasploit, nuclei, or other pipeline tools

## What nmap Does

nmap (Network Mapper) is an open-source tool for network discovery and security auditing. It
uses raw IP packets to determine what hosts are available, what services they run, what OS they
use, and dozens of other characteristics. It is the universal first step in any network-facing
engagement and is bundled with virtually every Linux security distribution.

## Installation

```bash
# Kali / Debian / Ubuntu
sudo apt install nmap

# RHEL / Fedora
sudo dnf install nmap

# macOS
brew install nmap

# Windows — download installer from https://nmap.org/download.html
# Or via Chocolatey:
choco install nmap

# From source
git clone https://github.com/nmap/nmap
cd nmap && ./configure && make && sudo make install

# Verify
nmap --version
```

## Core Concepts

### Host Discovery (Ping Scan)

nmap's first phase determines which hosts are alive before port scanning.

```bash
nmap -sn 192.168.1.0/24         # Ping scan only, no port scan
nmap -Pn 192.168.1.50           # Skip host discovery (treat host as up)
nmap -PS22,80,443 10.0.0.0/24  # TCP SYN ping on ports 22,80,443
nmap -PA80,443 10.0.0.0/24     # TCP ACK ping
nmap -PU53,161 10.0.0.0/24     # UDP ping
nmap -PE 10.0.0.0/24           # ICMP echo ping
nmap -PP 10.0.0.0/24           # ICMP timestamp ping
nmap -PM 10.0.0.0/24           # ICMP address mask ping
nmap -PR 192.168.1.0/24        # ARP ping (LAN only, very fast)
```

### Scan Types

```bash
nmap -sS 10.0.0.1              # SYN scan (stealth, default with root)
nmap -sT 10.0.0.1              # TCP connect scan (no root needed)
nmap -sU 10.0.0.1              # UDP scan (slow, requires root)
nmap -sA 10.0.0.1              # ACK scan (firewall rule mapping)
nmap -sW 10.0.0.1              # Window scan
nmap -sF 10.0.0.1              # FIN scan
nmap -sN 10.0.0.1              # Null scan
nmap -sX 10.0.0.1              # Xmas scan
nmap -sI zombie 10.0.0.1       # Idle (IP ID) scan using zombie host
nmap -sY 10.0.0.1              # SCTP INIT scan
nmap -sO 10.0.0.1              # IP protocol scan
```

## Port Specification

```bash
nmap -p 22,80,443 10.0.0.1         # Specific ports
nmap -p 1-1024 10.0.0.1            # Port range
nmap -p- 10.0.0.1                  # All 65535 ports
nmap -p U:53,161,T:22,80 10.0.0.1  # Mixed TCP and UDP
nmap --top-ports 100 10.0.0.1      # Top 100 most common ports
nmap --top-ports 1000 10.0.0.0/24  # Top 1000 across subnet
nmap -F 10.0.0.1                   # Fast mode (top 100 ports)
nmap -p http,ftp 10.0.0.1          # By service name
```

## Service and Version Detection

```bash
nmap -sV 10.0.0.1                          # Service version detection
nmap -sV --version-intensity 5 10.0.0.1    # Intensity 0-9 (default 7)
nmap -sV --version-light 10.0.0.1          # Intensity 2 (faster)
nmap -sV --version-all 10.0.0.1            # Intensity 9 (most probes)

# Version probes are in /usr/share/nmap/nmap-service-probes
```

## OS Detection

```bash
nmap -O 10.0.0.1                   # OS detection
nmap -O --osscan-guess 10.0.0.1    # Guess OS even if not confident
nmap -O --osscan-limit 10.0.0.1    # Only attempt if ≥1 open+closed port
nmap -A 10.0.0.1                   # Aggressive: -sV -sC -O --traceroute
```

## Timing Templates

```bash
nmap -T0 10.0.0.1   # Paranoid (5 min between probes, IDS evasion)
nmap -T1 10.0.0.1   # Sneaky (15 sec between probes)
nmap -T2 10.0.0.1   # Polite (0.4 sec between probes)
nmap -T3 10.0.0.1   # Normal (default)
nmap -T4 10.0.0.1   # Aggressive (1.25 sec host timeout, CTF/lab use)
nmap -T5 10.0.0.1   # Insane (0.3 sec host timeout, may drop packets)

# Fine-grained timing
nmap --min-rate 1000 10.0.0.1         # At least 1000 packets/sec
nmap --max-rate 500 10.0.0.1          # At most 500 packets/sec
nmap --min-parallelism 10 10.0.0.1    # Min outstanding probes
nmap --max-parallelism 100 10.0.0.1   # Max outstanding probes
nmap --max-retries 2 10.0.0.1         # Reduce retransmissions
nmap --host-timeout 30s 10.0.0.0/24  # Skip hosts taking > 30s
nmap --scan-delay 1s 10.0.0.1        # Delay between probes
```

## NSE Scripting Engine

### Script Categories

```bash
nmap --script auth 10.0.0.1          # Authentication bypass/default creds
nmap --script brute 10.0.0.1         # Brute-force login
nmap --script default 10.0.0.1       # Default scripts (same as -sC)
nmap --script discovery 10.0.0.1     # Service/network discovery
nmap --script exploit 10.0.0.1       # Active exploitation
nmap --script external 10.0.0.1      # Third-party service queries
nmap --script fuzzer 10.0.0.1        # Protocol fuzzing
nmap --script intrusive 10.0.0.1     # Risky/noisy scripts
nmap --script malware 10.0.0.1       # Malware backdoor detection
nmap --script safe 10.0.0.1          # Safe, non-intrusive scripts
nmap --script vuln 10.0.0.1          # Vulnerability checks
```

### Common NSE Scripts

```bash
# SMB enumeration and vulnerabilities
nmap --script smb-vuln-ms17-010 -p 445 10.0.0.1          # EternalBlue check
nmap --script smb-vuln-ms08-067 -p 445 10.0.0.1
nmap --script smb-enum-shares,smb-enum-users -p 445 10.0.0.1
nmap --script smb2-security-mode -p 445 10.0.0.0/24

# HTTP
nmap --script http-title,http-headers -p 80,443,8080 10.0.0.0/24
nmap --script http-robots.txt -p 80 10.0.0.1
nmap --script http-shellshock -p 80 10.0.0.1
nmap --script http-vuln-cve2021-41773 -p 443 10.0.0.1    # Apache path traversal
nmap --script http-auth-finder -p 80,443 10.0.0.1
nmap --script http-enum -p 80 10.0.0.1                   # Directory brute force

# SSH
nmap --script ssh-auth-methods -p 22 10.0.0.1
nmap --script ssh-hostkey --script-args ssh_hostkey=full -p 22 10.0.0.1
nmap --script ssh-brute -p 22 10.0.0.1

# FTP
nmap --script ftp-anon,ftp-bounce,ftp-vsftpd-backdoor -p 21 10.0.0.1

# SNMP
nmap -sU --script snmp-info,snmp-sysdescr -p 161 10.0.0.0/24
nmap -sU --script snmp-brute -p 161 10.0.0.1

# DNS
nmap --script dns-zone-transfer --script-args dns-zone-transfer.domain=example.com -p 53 10.0.0.1
nmap --script dns-brute --script-args dns-brute.domain=example.com 10.0.0.1

# MySQL / MSSQL
nmap --script mysql-info,mysql-empty-password -p 3306 10.0.0.1
nmap --script ms-sql-info,ms-sql-empty-password -p 1433 10.0.0.1

# Script arguments
nmap --script http-brute --script-args userdb=users.txt,passdb=pass.txt -p 80 10.0.0.1
nmap --script-args 'ftp-brute.timeout=5' --script ftp-brute -p 21 10.0.0.1
```

### Writing a Custom NSE Script

```lua
-- /usr/share/nmap/scripts/custom-banner.nse
local nmap    = require "nmap"
local comm    = require "comm"
local stdnse  = require "stdnse"

description = [[Grabs service banner from open port.]]
author      = "operator"
license     = "Same as Nmap"
categories  = {"discovery", "safe"}

portrule = function(host, port)
  return port.state == "open"
end

action = function(host, port)
  local status, response = comm.exchange(host, port, "HEAD / HTTP/1.0\r\n\r\n")
  if status then
    return response:sub(1, 200)
  end
end
```

```bash
# Run custom script
nmap --script ./custom-banner.nse -p 80 10.0.0.1

# Debug NSE output
nmap --script vuln --script-trace -p 443 10.0.0.1
```

## Output Formats

```bash
nmap -oN scan.txt 10.0.0.0/24       # Normal (human-readable)
nmap -oX scan.xml 10.0.0.0/24       # XML (machine-parseable)
nmap -oG scan.gnmap 10.0.0.0/24     # Grepable format
nmap -oJ scan.json 10.0.0.0/24      # JSON (nmap 7.93+)
nmap -oA scan 10.0.0.0/24           # All formats: scan.nmap, scan.xml, scan.gnmap
nmap -oS scan.txt 10.0.0.0/24       # Script kiddie output (novelty)

# Resume interrupted scan
nmap --resume scan.gnmap
```

## Firewall / IDS Evasion

```bash
# Fragment packets (bypass simple packet filters)
nmap -f 10.0.0.1                    # 8-byte fragments
nmap -f -f 10.0.0.1                 # 16-byte fragments
nmap --mtu 24 10.0.0.1              # Custom MTU (must be multiple of 8)

# Decoy scanning (mix real IP with decoys)
nmap -D RND:5 10.0.0.1              # 5 random decoys + real
nmap -D 10.1.1.1,10.1.1.2,ME 10.0.0.1  # Specific decoys

# Source port spoofing (bypass stateless firewall rules)
nmap --source-port 53 10.0.0.1      # Spoof as DNS response
nmap --source-port 20 10.0.0.1      # Spoof as FTP data

# IP spoofing (blind, for IDS confusion only — responses lost)
nmap -S 1.2.3.4 -e eth0 10.0.0.1

# Slow scan for IDS evasion
nmap -T1 --scan-delay 10s 10.0.0.1

# Randomize host order
nmap --randomize-hosts 10.0.0.0/24

# Append random data to packets
nmap --data-length 25 10.0.0.1

# Use specific MAC address
nmap --spoof-mac Apple 10.0.0.0/24
nmap --spoof-mac 00:11:22:33:44:55 10.0.0.0/24
```

## Common Workflows

### Initial Reconnaissance

```bash
# Phase 1: Fast host discovery
nmap -sn -T4 10.0.0.0/24 -oG alive_hosts.gnmap
grep Up alive_hosts.gnmap | awk '{print $2}' > live.txt

# Phase 2: Top port scan on live hosts
nmap -sS -T4 --top-ports 1000 -iL live.txt -oA topscan

# Phase 3: Full port scan on live hosts (background)
nmap -sS -T4 -p- -iL live.txt -oA fullscan --min-rate 2000 &

# Phase 4: Version + script scan on open ports
nmap -sV -sC -O -iL live.txt -p $(grep "open" topscan.gnmap | \
  grep -oP '\d+/open' | cut -d/ -f1 | sort -un | tr '\n' ',') -oA detailscan
```

### Targeted Service Enumeration

```bash
# Web servers
nmap -sV -p 80,443,8080,8443 --script http-title,http-headers,http-enum \
  -iL web_hosts.txt -oA webscan

# SMB / Windows
nmap -sS -p 445,139 --script smb-vuln-*,smb-enum-* \
  -iL windows_hosts.txt -oA smbscan

# Network infrastructure
nmap -sU -p 161 --script snmp-* -iL infra.txt -oA snmpscan
```

### Post-Scan Parsing

```bash
# Extract open ports from grepable output
grep "open" scan.gnmap | awk '{print $2, $5}' | tr ',' '\n'

# Parse XML with Python
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('scan.xml')
for host in tree.findall('.//host'):
    ip = host.find('.//address[@addrtype=\"ipv4\"]').get('addr')
    for port in host.findall('.//port[@protocol=\"tcp\"]'):
        if port.find('state').get('state') == 'open':
            print(ip, port.get('portid'), port.find('service').get('name',''))
"

# ndiff: compare two scans
ndiff scan_before.xml scan_after.xml
```

## Integration with Metasploit

```bash
# In msfconsole
db_nmap -sS -sV -O -p- 10.0.0.0/24   # Runs nmap, imports to msf db
hosts                                   # List discovered hosts
services                                # List discovered services
services -p 445 -S smb                 # Filter by port/service
vulns                                   # Show detected vulns from NSE
```

## Integration with Other Tools

```bash
# nmap → nuclei
nmap -sV --open 10.0.0.0/24 -oG - | \
  awk '/open/{print $2}' | \
  nuclei -l /dev/stdin -t technologies/

# nmap → httpx
nmap -sV -p 80,443,8080 --open 10.0.0.0/24 -oG - | \
  grep "open" | awk '{print $2}' | httpx -silent

# nmap → EyeWitness (screenshots)
nmap -sV -p 80,443 --open 10.0.0.0/24 -oX web.xml
eyewitness --xml web.xml --web -d screenshots/
```

## Advanced Techniques

### Scan Rate Tuning for Large Subnets

```bash
# Scan a /16 quickly
nmap -sS -T4 --min-rate 5000 --max-retries 1 --open \
  -p 22,80,443,445,3389 10.0.0.0/16 -oA bignet

# Parallel nmap with GNU parallel
echo "10.0.0.0/24\n10.1.0.0/24\n10.2.0.0/24" | \
  parallel -j4 nmap -sS -T4 -p- {} -oA scan_{}
```

### IPv6 Scanning

```bash
nmap -6 -sV fe80::1/64
nmap -6 --script ipv6-node-info ::1
```

## Troubleshooting

| Issue | Fix |
|---|---|
| All ports filtered | Use `-Pn` to skip host discovery; target may be firewalled |
| UDP scan extremely slow | Limit ports: `-p U:53,161,500`; increase `--min-rate` |
| Permission denied on SYN scan | Run with `sudo` — raw sockets require root |
| NSE script not found | Update script DB: `sudo nmap --script-updatedb` |
| Too many dropped packets | Reduce `--min-rate`, increase `--max-retries 3` |
| Incorrect OS detection | Add `--osscan-guess`; ensure at least one open and one closed port |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
