---
name: autorecon
description: >
  Operate AutoRecon — a multi-threaded network reconnaissance tool that automatically
  runs appropriate enumeration tools based on detected services. Use during OSCP labs,
  CTF initial enumeration, or real-world external/internal network pentests to automate
  the discovery phase. Covers installation, target specification, port scan profiles,
  per-service tool execution, custom plugins, output structure, concurrency controls,
  and a full OSCP/CTF enumeration workflow.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/Tib3rius/AutoRecon
  language: Python
---

# autorecon Agent Skill

## When to Use This Skill

Use this skill when:
- Starting a new CTF box or OSCP lab machine and need comprehensive initial enumeration
- Running parallel reconnaissance against multiple targets (pentest internal network)
- Automating the "run all the things" phase: nmap → per-service tools → report-ready output
- Customising AutoRecon plugins to add bespoke enumeration tools
- Understanding AutoRecon's output directory structure to navigate findings quickly
- Building an OSCP methodology around AutoRecon as the enumeration backbone

## What AutoRecon Does

AutoRecon (Tib3rius/AutoRecon, ~5.6k GitHub stars) is a Python-based multi-threaded
reconnaissance tool that runs multiple scanners simultaneously. It starts with broad port
discovery, then automatically launches service-specific enumeration tools for every
open port it finds — HTTP ports get nikto/feroxbuster/whatweb, SMB ports get enum4linux/
smbclient, FTP gets anonymous login checks, and so on. The result is a structured output
directory containing all scan results, ready for manual review.

## Installation

### pip (recommended)
```bash
# Python 3.8+ required
pip3 install autorecon

# Verify
autorecon --help
```

### pipx (isolated environment, no conflicts)
```bash
pipx install autorecon
pipx inject autorecon toml   # if needed
```

### From Source
```bash
git clone https://github.com/Tib3rius/AutoRecon.git
cd AutoRecon
pip3 install -r requirements.txt
python3 autorecon.py --help
```

### Required External Tools
AutoRecon calls external tools — they must be installed separately:
```bash
# Core
sudo apt install -y nmap curl wget seclists

# Web
sudo apt install -y nikto gobuster feroxbuster whatweb wkhtmltopdf

# SMB / Windows
sudo apt install -y enum4linux smbclient smbmap nbtscan

# LDAP / AD
sudo apt install -y ldap-utils

# FTP / other services
sudo apt install -y ftp tnftp onesixtyone snmp

# DNS
sudo apt install -y dnsrecon dnsenum

# Brute force
sudo apt install -y hydra medusa

# NFS
sudo apt install -y nfs-common
```

### Verify Tool Availability
```bash
autorecon --list-plugins          # List all plugins and their required tools
# AutoRecon will skip plugins whose required tools are missing
```

## Core Concepts

### Scan Phases
1. **Port Discovery**: Fast TCP/UDP port scans using nmap
2. **Service Detection**: Nmap service version detection against open ports
3. **Service Enumeration**: Per-service plugins run automatically based on detected services
4. **Reporting**: All output written to structured directory tree

### Plugin System
AutoRecon uses a TOML-based plugin configuration. Each plugin defines:
- Which service tags trigger it (e.g., `http`, `https`, `smb`, `ftp`)
- The command to run (with template variables)
- Output file name
- Whether it's run once per host or once per port

### Template Variables
Available in plugin commands:
```
{address}     — Target IP address
{port}        — Port number
{scheme}      — http or https
{hostname}    — Resolved hostname (if available)
{scandir}     — Output directory for this target
{nmap_extra}  — Extra nmap flags from --nmap-append
```

## CLI Reference

### Basic Usage
```bash
# Single target
autorecon 10.10.10.10

# Single target with hostname
autorecon 10.10.10.10 --single-target

# Domain name (resolves to IP)
autorecon target.htb

# CIDR range
autorecon 10.10.10.0/24

# Multiple targets
autorecon 10.10.10.10 10.10.10.20 10.10.10.30

# Targets from file
autorecon -t targets.txt
```

### Output Directory
```bash
# Default output location: ./results/
# Custom output directory
autorecon 10.10.10.10 -o /opt/engagements/target/

# Results structure:
# results/10.10.10.10/
# ├── scans/
# │   ├── _full_tcp_nmap.txt          (all TCP ports)
# │   ├── _top_udp_nmap.txt           (top 20 UDP ports)
# │   ├── tcp_22_ssh_nmap.txt         (SSH-specific nmap scripts)
# │   ├── tcp_80_http_nikto.txt       (nikto output)
# │   ├── tcp_80_http_feroxbuster.txt (feroxbuster output)
# │   ├── tcp_445_smb_enum4linux.txt  (enum4linux output)
# │   └── ...
# ├── exploit/                        (manual exploitation notes placeholder)
# ├── loot/                           (captured credentials, hashes, etc.)
# └── proof.txt                       (proof placeholder)
```

### Concurrency Controls
```bash
# Max concurrent targets (default: 5)
autorecon 10.10.10.0/24 -ct 3

# Max concurrent scans per target (default: 10)
autorecon 10.10.10.10 -cs 5

# Max concurrent plugins of the same type
autorecon 10.10.10.10 --single-target -cs 3

# Useful for slow/fragile targets
autorecon 10.10.10.10 -cs 2 -ct 1
```

### Port Scan Profiles
AutoRecon uses profile TOML files to define scan strategies:

```bash
# List available profiles
ls $(pip3 show autorecon | grep Location | awk '{print $2}')/autorecon/config/

# Use a specific profile
autorecon 10.10.10.10 --profile default
autorecon 10.10.10.10 --profile udp

# Custom profile file
autorecon 10.10.10.10 --profile-file /opt/myprofiles.toml
```

Default profile behaviour:
1. `nmap -p- --min-rate=2500` (full TCP)
2. `nmap -sV -sC -p {open_ports}` (service detection on found ports)
3. `nmap -sU --top-ports=20` (top UDP ports)

### Nmap Customisation
```bash
# Append extra nmap flags to all nmap scans
autorecon 10.10.10.10 --nmap-append "--script-timeout 5s"

# Override nmap scan speed
autorecon 10.10.10.10 --nmap-append "-T4"

# Add nmap scripts
autorecon 10.10.10.10 --nmap-append "--script=vuln"
```

### Verbosity and Logging
```bash
# Verbose (see commands as they run)
autorecon 10.10.10.10 -v

# Very verbose (see all output)
autorecon 10.10.10.10 -vv

# Heartbeat (show progress every N seconds)
autorecon 10.10.10.10 --heartbeat 30

# Disable heartbeat
autorecon 10.10.10.10 --heartbeat 0
```

### Tags and Plugin Filtering
```bash
# Only run specific service plugins
autorecon 10.10.10.10 --only-scans-dir --tags http

# Exclude specific plugins
autorecon 10.10.10.10 --exclude-tags brute

# Run only a specific plugin
autorecon 10.10.10.10 --plugins "nikto"

# Skip UDP scanning (faster for CTF boxes)
autorecon 10.10.10.10 --exclude-tags udp
```

## Per-Service Tool Matrix

### HTTP / HTTPS (tcp/80, tcp/443, tcp/8080, tcp/8443)
| Tool | What It Does |
|------|-------------|
| nmap http scripts | `http-title`, `http-server-header`, `http-methods`, `http-auth` |
| whatweb | Technology fingerprinting (CMS, frameworks, plugins) |
| nikto | Known vulnerabilities, misconfigs, default files |
| gobuster/feroxbuster | Directory and file brute-force |
| curl -k | Grab full response headers |
| wkhtmltopdf | Screenshot the page for report |

### SMB (tcp/445, tcp/139)
| Tool | What It Does |
|------|-------------|
| nmap smb scripts | `smb-os-discovery`, `smb-security-mode`, `smb-vuln-ms17-010` |
| enum4linux | Null session enumeration: users, shares, groups, policies |
| smbclient | List shares, attempt anonymous auth |
| smbmap | Map shares and permissions |
| nbtscan | NetBIOS name scan |

### FTP (tcp/21)
| Tool | What It Does |
|------|-------------|
| nmap ftp scripts | `ftp-anon`, `ftp-bounce`, `ftp-syst` |
| AutoRecon plugin | Attempt anonymous login and list files |
| hydra (if tagged) | Brute-force FTP credentials |

### SSH (tcp/22)
| Tool | What It Does |
|------|-------------|
| nmap ssh scripts | `ssh-hostkey`, `ssh-auth-methods` |
| AutoRecon plugin | Enumerate supported auth methods |

### DNS (tcp/53, udp/53)
| Tool | What It Does |
|------|-------------|
| nmap dns scripts | `dns-zone-transfer`, `dns-recursion` |
| dnsrecon | Zone transfer, reverse lookup, brute |
| dnsenum | Zone transfer, Google enumeration |

### SNMP (udp/161)
| Tool | What It Does |
|------|-------------|
| onesixtyone | Community string brute-force |
| snmpwalk | Full MIB walk with found community strings |

### LDAP (tcp/389, tcp/636)
| Tool | What It Does |
|------|-------------|
| nmap ldap scripts | `ldap-rootdse`, `ldap-search` |
| ldapsearch | Anonymous bind, base DN dump |

### NFS (tcp/2049)
| Tool | What It Does |
|------|-------------|
| nmap nfs scripts | `nfs-showmount`, `nfs-ls` |
| showmount | List exported shares |

## Custom Plugin Development

### Plugin TOML Structure
```toml
[plugin.custom-wfuzz]
name = "Custom WFuzz Scan"
tags = ["http", "custom"]
ports.tcp = [80, 443, 8080, 8443]
run_once_per = "service"

[plugin.custom-wfuzz.command]
linux = "wfuzz -c -z file,/usr/share/seclists/Discovery/Web-Content/common.txt \
  --hc 404 -u {scheme}://{address}:{port}/FUZZ \
  -o {scandir}/tcp_{port}_{scheme}_wfuzz.txt 2>&1"
```

### Where to Place Custom Plugins
```bash
# User plugin directory (created automatically)
mkdir -p ~/.config/AutoRecon/plugins/

# Copy existing plugin as template
cp $(pip3 show autorecon | grep Location | awk '{print $2}')/autorecon/plugins/http_nikto.toml \
  ~/.config/AutoRecon/plugins/http_custom.toml

# Edit and reload
autorecon --list-plugins | grep custom
```

### Plugin Variables Reference
```toml
# In command string, use these templates:
{address}    # target IP
{port}       # target port
{scheme}     # http or https
{hostname}   # resolved hostname
{scandir}    # scan output directory for this target
{nmap_extra} # nmap extra flags from CLI
{wordlist}   # default wordlist (configurable)
```

## OSCP / CTF Enumeration Workflow

### Standard Box Workflow
```bash
# Step 1: Start AutoRecon (add to /etc/hosts first if needed)
echo "10.10.10.10  target.htb" >> /etc/hosts
autorecon 10.10.10.10 --single-target -v

# Step 2: While AutoRecon runs, review nmap results as they appear
tail -f results/10.10.10.10/scans/_full_tcp_nmap.txt

# Step 3: Check service-specific results
ls -la results/10.10.10.10/scans/

# Step 4: Prioritise findings
# HTTP: cat results/10.10.10.10/scans/tcp_80_http_whatweb.txt
# SMB: cat results/10.10.10.10/scans/tcp_445_smb_enum4linux.txt
# FTP: cat results/10.10.10.10/scans/tcp_21_ftp_nmap.txt

# Step 5: Manual investigation of flagged services
```

### Multi-Target Internal Network Scan
```bash
# Create target list from CIDR
nmap -sn 192.168.1.0/24 -oG - | grep Up | awk '{print $2}' > live_hosts.txt

# Run AutoRecon against all live hosts
autorecon -t live_hosts.txt -o /opt/engagement/recon/ -ct 5 -cs 10 -v

# Review results
ls /opt/engagement/recon/

# Aggregate HTTP findings
grep -r "200 OK\|302\|401\|403" /opt/engagement/recon/*/scans/*http*ferox* 2>/dev/null
```

### Quick UDP Scan Only
```bash
# AutoRecon includes UDP scanning — ensure it runs
autorecon 10.10.10.10 --single-target --profile udp -v
cat results/10.10.10.10/scans/_top_udp_nmap.txt
```

### Reading Output Efficiently
```bash
# See all scan files sorted by service
ls results/10.10.10.10/scans/ | sort

# Quick wins: find interesting strings across all results
grep -r -i "password\|admin\|secret\|flag\|login\|token\|api.key" \
  results/10.10.10.10/scans/ 2>/dev/null

# Find all discovered web paths
grep -r "200\|301\|403" results/10.10.10.10/scans/*ferox* \
  results/10.10.10.10/scans/*gobuster* 2>/dev/null | \
  awk '{print $NF}' | sort -u
```

## Advanced Techniques

### Running AutoRecon Without Root (No SYN Scan)
```bash
# TCP connect scan instead of SYN scan
autorecon 10.10.10.10 --nmap-append "-sT" --single-target
# Note: slower but works without root
```

### Integrating Custom Wordlists
```bash
# Override default wordlist in plugin config
# Edit: ~/.config/AutoRecon/config.toml
[global]
wordlist = "/usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt"
```

### Saving and Archiving Results
```bash
# Tar results for transfer
tar -czf target_10.10.10.10_recon.tar.gz results/10.10.10.10/

# Search all results for creds
grep -r -E "(user|pass|password|username|credential)" \
  results/10.10.10.10/ --include="*.txt" -i | \
  grep -v "Binary"
```

## Troubleshooting

**AutoRecon exits immediately with no output**
```bash
# Check Python version (needs 3.8+)
python3 --version

# Run with max verbosity to see errors
autorecon 10.10.10.10 -vv

# Check required tools are installed
autorecon --list-plugins
```

**Missing plugin results**
```bash
# Tool not installed — install it
sudo apt install -y feroxbuster nikto

# Or exclude missing tool's plugin
autorecon 10.10.10.10 --exclude-tags feroxbuster
```

**Scans running too slowly**
```bash
# Increase concurrent scans
autorecon 10.10.10.10 -cs 20

# Disable UDP (slowest phase)
autorecon 10.10.10.10 --exclude-tags udp

# Use faster nmap timing
autorecon 10.10.10.10 --nmap-append "-T4"
```

**Out of memory on large CIDR scans**
```bash
# Reduce concurrent targets
autorecon 10.10.10.0/24 -ct 2 -cs 5
```

**Gobuster/feroxbuster not found**
```bash
sudo apt install -y gobuster feroxbuster
# Or specify alternative in plugin config
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
