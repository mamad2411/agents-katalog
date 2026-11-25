---
name: rustscan
description: >
  Operate RustScan — an extremely fast modern port scanner that scans all 65,535 ports in
  seconds and automatically passes results to Nmap for deep service/script scanning. Use when
  the user needs fast port discovery, when the user asks about RustScan, when conducting
  external or internal network reconnaissance, or when standard Nmap scans are too slow.
  Covers installation (cargo, Docker, package managers, releases), batch size tuning,
  timeout configuration, Nmap integration, custom scripts, accessible mode, performance
  tuning, and how RustScan compares to and chains with Nmap and masscan.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/bee-san/RustScan
---

# rustscan Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs fast port discovery against one or many hosts
- The user asks about RustScan, fast scanning, or replacing Nmap for initial discovery
- Conducting recon in CTFs, bug bounties, or pentest engagements where speed matters
- The user needs to pipe port scan results directly into Nmap service detection
- The user wants to scan all 65,535 ports without waiting for slow Nmap default scans

## What RustScan Does

RustScan is a Rust-built port scanner engineered for speed — it can scan all 65,535 TCP ports on a single host in under 3 seconds by using asynchronous socket connections in large batches. Its design philosophy is narrow: do port discovery fast, then hand results off to Nmap (or a custom script) for the actual service fingerprinting. RustScan is not a replacement for Nmap — it is a rapid first-pass engine that feeds Nmap exactly the open ports to investigate, eliminating the overhead of Nmap scanning closed ports.

## Installation

### Cargo (Rust package manager — recommended)

```bash
# Install Rust if needed
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Install RustScan
cargo install rustscan
```

### Package Managers

```bash
# macOS (Homebrew)
brew install rustscan

# Arch Linux
pacman -S rustscan
yay rustscan    # AUR

# Kali Linux / Debian (manual .deb from releases page)
wget https://github.com/bee-san/RustScan/releases/latest/download/rustscan_*_amd64.deb
dpkg -i rustscan_*_amd64.deb
```

### Docker

```bash
# Pull image
docker pull cmnatic/rustscan:latest

# Alias for seamless use
alias rustscan='docker run -it --rm --network host cmnatic/rustscan:latest'

# Run directly
docker run -it --rm --network host cmnatic/rustscan:latest -a 192.168.1.1

# Scan with Nmap passthrough via Docker
docker run -it --rm --network host cmnatic/rustscan:latest -a 10.10.10.10 -- -sC -sV
```

### Binary Releases

```bash
# Download from GitHub releases
wget https://github.com/bee-san/RustScan/releases/latest/download/rustscan
chmod +x rustscan
./rustscan --help
```

### Build from Source

```bash
git clone https://github.com/bee-san/RustScan
cd RustScan
cargo build --release
./target/release/rustscan --help
```

## Core Concepts

### How RustScan Works

RustScan opens a configurable number of sockets simultaneously (`--batch-size`), connects to each port asynchronously, and waits only `--timeout` milliseconds before marking a port closed. Open ports are collected and written to a temporary file, then passed as `-p <ports>` to Nmap (or a custom script). This two-phase approach means:

1. **Phase 1** — RustScan finds all open ports in seconds
2. **Phase 2** — Nmap performs deep service/version detection only on confirmed open ports

### Ulimit and File Descriptors

RustScan's speed depends on the OS allowing many simultaneous open file descriptors. On Linux/macOS:

```bash
# Check current limit
ulimit -n

# Increase for the current session
ulimit -n 65535

# Or set per run
rustscan --ulimit 5000 -a 10.10.10.10
```

Low ulimit values cause missed ports and false negatives. RustScan will warn if it detects an insufficient limit. On most Linux systems the default is 1024 — always raise it before scanning.

## CLI Reference

### Core Flags

```
-a, --addresses <IP/CIDR/hostname,...>  Target(s) — comma-separated or CIDR
-p, --ports <ports>                     Specific ports to scan (default: all 65535)
-r, --range <start-end>                 Port range (e.g., 1-1000)
-b, --batch-size <n>                    Sockets per batch (default: 4500)
-t, --timeout <ms>                      Timeout per port in milliseconds (default: 1500)
--ulimit <n>                            Set ulimit for this run
-u, --ulimit <n>                        (alias)
--tries <n>                             Number of attempts per port (default: 1)
--scan-order <serial|random>            Port scan order (default: serial)
-g, --greppable                         Greppable output (machine-readable, no Nmap)
-q, --quiet                             Quiet mode — suppress non-essential output
--accessible                            Accessible mode — no special characters or color
--no-config                             Ignore config file
--top                                   Scan top 1000 ports (Nmap's top list)
-n                                      No DNS resolution
--scripts <custom_script>              Path to a custom Lua/Python/Shell script
-- [nmap args]                          Everything after -- is passed directly to Nmap
```

### Addressing Formats

```bash
# Single host
rustscan -a 192.168.1.1

# Multiple hosts (comma-separated)
rustscan -a 192.168.1.1,192.168.1.2,192.168.1.3

# CIDR range
rustscan -a 192.168.1.0/24

# Hostname
rustscan -a example.com

# From file (pipe via stdin workaround)
cat hosts.txt | xargs -I{} rustscan -a {}
```

## Basic Usage

```bash
# Scan all 65535 ports (default behavior)
rustscan -a 10.10.10.10

# Scan all ports with Nmap service + script detection
rustscan -a 10.10.10.10 -- -sC -sV

# Scan only specific ports
rustscan -a 10.10.10.10 -p 80,443,8080,8443

# Scan a port range
rustscan -a 10.10.10.10 -r 1-10000

# Scan top 1000 ports (faster, common services)
rustscan -a 10.10.10.10 --top

# Suppress banner, greppable output only
rustscan -a 10.10.10.10 -g -q
```

## Nmap Integration

Everything after `--` is appended directly to the Nmap command that RustScan constructs. RustScan builds: `nmap -vvv -p <open_ports> <target> [your flags]`.

```bash
# Service + default scripts (most common usage)
rustscan -a 10.10.10.10 -- -sC -sV

# Service detection + aggressive OS detection
rustscan -a 10.10.10.10 -- -sC -sV -O

# Nmap UDP scan on specific ports (combine with -p)
rustscan -a 10.10.10.10 -p 53,67,68,161,162 -- -sU -sV

# Save Nmap output in all formats
rustscan -a 10.10.10.10 -- -sC -sV -oA scan_results

# Specific Nmap NSE scripts
rustscan -a 10.10.10.10 -- --script=http-title,http-headers,ssl-cert

# Slow stealth scan (after fast discovery)
rustscan -a 10.10.10.10 -- -sS -T2

# Vuln scanning
rustscan -a 10.10.10.10 -- --script=vuln

# Skip Nmap entirely (port list only)
rustscan -a 10.10.10.10 -g
```

## Performance Tuning

### Batch Size (`--batch-size` / `-b`)

Batch size controls how many ports are tested simultaneously. Higher = faster but more likely to miss ports on congested or rate-limiting targets.

```bash
# Fast (default 4500 — good for local networks and VPNs like HTB/THM)
rustscan -a 10.10.10.10 -b 4500

# Aggressive (fast internet-connected hosts, high ulimit required)
rustscan -a 10.10.10.10 -b 65535

# Conservative (unreliable networks, rate-limited targets)
rustscan -a 10.10.10.10 -b 500

# Slow / stealthy (avoid IDS triggers)
rustscan -a 10.10.10.10 -b 100 -t 5000
```

### Timeout (`--timeout` / `-t`)

Timeout in milliseconds before a port is declared closed. Increase for high-latency links.

```bash
# Fast local network
rustscan -a 192.168.1.0/24 -t 500

# Default (good for VPN/HTB)
rustscan -a 10.10.10.10 -t 1500

# High latency (cloud, transatlantic)
rustscan -a 203.0.113.1 -t 5000

# Very slow / hostile networks
rustscan -a 203.0.113.1 -t 10000 -b 100
```

### Network Condition Profiles

| Environment | Recommended Flags |
|---|---|
| Local LAN | `-b 65535 -t 500 --ulimit 65535` |
| HTB / THM VPN | `-b 4500 -t 1500` (default) |
| Bug bounty (internet) | `-b 1000 -t 3000` |
| Rate-limited target | `-b 100 -t 5000` |
| High-latency WAN | `-b 500 -t 8000` |

## Custom Scripting Engine

RustScan supports custom scripts (Lua, Python, Shell) that replace or supplement Nmap. Scripts receive open port data and can run arbitrary logic.

```bash
# Use a custom script instead of Nmap
rustscan -a 10.10.10.10 --scripts custom --script-path /path/to/script.py

# Script receives ports as argument — example Python script:
# #!/usr/bin/env python3
# import sys, subprocess
# ports = sys.argv[1]   # comma-separated open ports
# subprocess.run(["nmap", "-p", ports, "-sV", sys.argv[2]])
```

## Accessible Mode

`--accessible` removes all special Unicode characters and ANSI color codes from output. Use this in:
- Screen reader environments
- Logging pipelines where escape codes break parsing
- Automated scripts that parse RustScan output

```bash
rustscan -a 10.10.10.10 --accessible
rustscan -a 10.10.10.10 --accessible -g   # combine with greppable for clean automation
```

## Config File

RustScan reads `~/.rustscan.toml` for persistent defaults:

```toml
# ~/.rustscan.toml
batch_size = 2500
timeout = 2000
tries = 1
scan_order = "Serial"
accessible = false
# Addresses = ["192.168.1.0/24"]   # optional default targets
```

```bash
# Override config for a single run
rustscan -a 10.10.10.10 -b 500 --no-config
```

## Greppable / Machine-Readable Output

```bash
# Greppable output (ports only, no Nmap)
rustscan -a 10.10.10.10 -g
# Output: 10.10.10.10 -> [22, 80, 443, 8080]

# Parse open ports from greppable output
rustscan -a 10.10.10.10 -g | grep -oP '\[\K[^\]]+' | tr ',' '\n'

# Feed directly to Nmap manually
PORTS=$(rustscan -a 10.10.10.10 -g -q | grep -oP '\[\K[^\]]+')
nmap -p "$PORTS" -sC -sV 10.10.10.10 -oA full_scan
```

## Common Workflows

### HTB / CTF Standard Approach

```bash
# Fast all-port discovery then deep Nmap
rustscan -a 10.10.10.10 -- -sC -sV -oA nmap/initial

# With ulimit raised for maximum speed
ulimit -n 65535
rustscan -a 10.10.10.10 -b 65535 -t 1000 -- -sC -sV -oA nmap/full
```

### Bug Bounty Subdomain + Port Sweep

```bash
# Discover live hosts via httpx/subfinder first, then port scan
cat live_hosts.txt | xargs -P4 -I{} rustscan -a {} -b 1000 -t 3000 -g

# Or use CIDR sweep
rustscan -a 203.0.113.0/24 -b 500 -t 3000 -g | tee open_ports.txt
```

### Internal Network Wide Sweep

```bash
# Sweep entire /24 for common ports
rustscan -a 192.168.1.0/24 --top -b 2000 -t 1000 -g

# Then target specific open hosts with full scan
rustscan -a 192.168.1.50 -b 65535 -- -sC -sV -O
```

### Comparing RustScan vs Nmap vs masscan

| Tool | Speed | Accuracy | Service Detection | Best Use |
|---|---|---|---|---|
| **RustScan** | ~3s / 65535 ports | High (adjustable) | Via Nmap passthrough | Fast first-pass → Nmap |
| **masscan** | ~5m / internet | Moderate (SYN only) | None | Internet-wide surveys |
| **Nmap** | ~15min / 65535 ports | Very High | Built-in (NSE scripts) | Deep single-host analysis |

RustScan is not designed to replace masscan (which does internet-scale SYN scanning) or Nmap (which provides authoritative service fingerprinting). Chain them: masscan → RustScan (host confirmation) → Nmap (service depth).

## Integration with Other Tools

### Typical Pentest Pipeline

```bash
# 1. Fast port discovery
rustscan -a 10.10.10.10 -b 4500 -g -q | tee ports.txt

# 2. Parse ports
PORTS=$(cat ports.txt | grep -oP '\[\K[^\]]+')

# 3. Deep Nmap service scan
nmap -p "$PORTS" -sC -sV -O -oA nmap/detailed 10.10.10.10

# 4. Pipe HTTP ports into web recon tools
echo "$PORTS" | tr ',' '\n' | grep -E "^(80|443|8080|8443|8000|8888)$" | \
  xargs -I{} sh -c 'gobuster dir -u http://10.10.10.10:{} -w /usr/share/seclists/Discovery/Web-Content/common.txt'
```

### With Metasploit

```bash
# Discover ports, then load into MSF db
rustscan -a 10.10.10.10 -- -sV -oX scan.xml
msfconsole -q -x "db_import scan.xml; hosts; services"
```

### With EyeWitness / Aquatone (Web Screenshot)

```bash
# Get open web ports
rustscan -a 10.10.10.0/24 -p 80,443,8080,8443,8000 -g | \
  grep -oP '(\d+\.\d+\.\d+\.\d+) -> \[\K[^\]]+' | \
  while read line; do echo "http://$line"; done | \
  eyewitness --web -f - --no-prompt
```

## Troubleshooting

| Issue | Fix |
|---|---|
| Ports missed / false negatives | Raise `ulimit -n 65535`, lower `-b` (try 1000), increase `-t` |
| `too many open files` error | `ulimit -n 65535` before running, or use `--ulimit 5000` |
| RustScan hangs on Nmap phase | Nmap not in PATH — install nmap or use `-g` to skip Nmap |
| Docker can't reach targets | Ensure `--network host` flag on docker run |
| Slow scan despite high `-b` | Target may be rate-limiting — reduce `-b` and increase `-t` |
| CIDR not scanning all hosts | Verify ulimit is high enough; split large CIDRs into /25 or /26 |
| Config file ignored | File must be `~/.rustscan.toml`; use `--no-config` to confirm conflict |
| Greppable output format changed | Parse with `grep -oP '\[\K[^\]]+'` for port list extraction |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
