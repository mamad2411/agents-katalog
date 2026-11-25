---
name: masscan
description: >
  Build, extend, and operate Masscan — the fastest Internet port scanner, capable of scanning
  the entire IPv4 address space in under 6 minutes at 10 million packets/second. Use when performing
  large-scale network reconnaissance, port enumeration, banner grabbing, or building scanning pipelines.
  Use when the user asks about high-speed scanning, comparing Masscan vs nmap, rate tuning, output formats,
  or integrating Masscan with nmap and Nuclei for vulnerability discovery pipelines.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/robertdavidgraham/masscan
  stars: '24.5k'
---

# masscan Agent Skill

## When to Use This Skill

Use this skill when:
- Performing large-scale port discovery across CIDR ranges or the entire Internet
- Building a scanning pipeline (Masscan → nmap service scan → Nuclei vulnerability scan)
- Optimizing scan rate for available bandwidth and target tolerance
- Needing output in JSON, Grepable, XML, or list format for downstream tooling
- Conducting external attack surface discovery during a red team or pentest
- Comparing Masscan performance against nmap or RustScan

## What Masscan Does

Masscan is an asynchronous TCP/UDP port scanner using a custom userspace TCP/IP stack. It transmits SYN packets at user-defined rates (tested up to 25M packets/sec with a 10GbE NIC) and collects SYN-ACK responses without maintaining connection state. This makes it orders of magnitude faster than nmap's connect/SYN scan but provides no service version detection — it only identifies open ports. Masscan is the reconnaissance workhorse in large-scope engagements; nmap then does detailed analysis on discovered open ports.

## Installation

```bash
# Ubuntu/Debian — apt
sudo apt-get install masscan

# From source (recommended — latest version + PF_RING support)
sudo apt-get install git make gcc libssl-dev
git clone https://github.com/robertdavidgraham/masscan.git
cd masscan
make -j$(nproc)
sudo cp bin/masscan /usr/local/bin/

# macOS (Homebrew)
brew install masscan

# Verify
masscan --version
```

### PF_RING Support (High-Speed NICs)

For rates above 2Mpps, install PF_RING:

```bash
git clone https://github.com/ntop/PF_RING.git
cd PF_RING/kernel && make && sudo insmod pf_ring.ko
# Then recompile masscan:
make -j$(nproc) PFRING=1
```

## Core Concepts

### Userspace TCP Stack

Masscan bypasses the kernel TCP stack using raw sockets (Linux) or libpcap (macOS/Windows). This means:
- Masscan SYN packets look stateless to the kernel — the kernel may reply with RST before Masscan sees the SYN-ACK
- Linux fix: `iptables -A INPUT -p tcp --dport 61000 --tcp-flags RST RST -j DROP` (or use `--adapter-port 61000`)
- Masscan must own the adapter or use a raw socket — run as root or with `CAP_NET_RAW`

### Transmission Rate

Rate is packets per second (pps), not bandwidth. A single SYN packet is ~40–60 bytes:
- `--rate 1000` = 1K pps ≈ ~50 KB/s
- `--rate 100000` = 100K pps ≈ ~5 MB/s (safe for most targets)
- `--rate 1000000` = 1M pps (requires 1GbE or faster)

Always check with target/client before high-rate scanning — 500K+ pps can saturate links or trigger IDS.

## Basic Usage

```bash
# Scan single host, common ports
sudo masscan 192.168.1.1 -p 22,80,443,8080,3389

# Scan CIDR range, top ports
sudo masscan 10.0.0.0/8 -p 22,80,443,445,3389 --rate 10000

# Scan all 65535 TCP ports on a range
sudo masscan 192.168.1.0/24 -p 1-65535 --rate 50000

# Scan all ports + all UDP ports (selected)
sudo masscan 10.10.10.0/24 -p 0-65535,U:53,U:161,U:1194 --rate 10000

# Scan from file of targets
sudo masscan -p 80,443 -iL targets.txt --rate 5000

# Ping sweep (ICMP)
sudo masscan 10.0.0.0/16 --ping --rate 5000
```

## Rate Tuning

```bash
# Conservative — safe for client networks, won't flood routers
--rate 1000

# Standard pentest rate — comfortable for /16
--rate 10000

# Aggressive — fast /8 sweep, needs good NIC
--rate 100000

# Internet-scale — 10GbE required, check legal constraints
--rate 1000000

# Adaptive: start slow, monitor packet loss
# Check with: ethtool -S eth0 | grep drop
```

## Output Formats

```bash
# JSON output (most parseable)
sudo masscan 10.0.0.0/24 -p 1-65535 --rate 10000 -oJ results.json

# Grepable (nmap -oG compatible)
sudo masscan 10.0.0.0/24 -p 80,443 --rate 10000 -oG results.gnmap

# XML output
sudo masscan 10.0.0.0/24 -p 1-65535 --rate 10000 -oX results.xml

# List output (ip:port per line)
sudo masscan 10.0.0.0/24 -p 1-65535 --rate 10000 -oL results.list

# Binary output (fastest, needs masscan to parse back)
sudo masscan 10.0.0.0/24 -p 1-65535 --rate 10000 -oB results.bin
# Read binary back:
masscan --readscan results.bin -oJ results.json

# Output to stdout
sudo masscan 10.0.0.0/24 -p 80 --rate 10000 -oJ -
```

### JSON Output Structure

```json
[
  {"ip": "192.168.1.10", "timestamp": "1712345678", "ports": [
    {"port": 80, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 64}
  ]},
  {"ip": "192.168.1.20", "timestamp": "1712345680", "ports": [
    {"port": 443, "proto": "tcp", "status": "open", "reason": "syn-ack", "ttl": 128}
  ]}
]
```

## Banner Grabbing

Masscan can grab banners by completing the TCP handshake and sending a minimal probe:

```bash
# HTTP banner
sudo masscan 10.0.0.0/24 -p 80,443,8080,8443 --banners --rate 5000 -oJ banners.json

# SSH banner
sudo masscan 10.0.0.0/24 -p 22 --banners --rate 5000 -oJ ssh-banners.json

# All banners (slower — reduces effective rate)
sudo masscan 10.0.0.0/24 -p 21,22,25,80,110,443,3306,5432 --banners --rate 1000 -oJ all-banners.json
```

Banner JSON structure adds `"banner"` field: `{"banner": "SSH-2.0-OpenSSH_8.2p1"}`.

**Note:** Banner grabbing requires `--rate` be lowered significantly (1000–5000 pps) as it holds connections open.

## Excluding Ranges

```bash
# Exclude specific IP from scan
sudo masscan 10.0.0.0/8 -p 22,80 --exclude 10.0.0.1 --rate 10000

# Exclude file (one CIDR/IP per line — critical for Internet scans)
# Always exclude non-scannable ranges per RFC 5737, IANA
cat > /etc/masscan/exclude.conf << 'EOF'
0.0.0.0/8
10.0.0.0/8
100.64.0.0/10
127.0.0.0/8
169.254.0.0/16
172.16.0.0/12
192.0.0.0/24
192.168.0.0/16
198.18.0.0/15
198.51.100.0/24
203.0.113.0/24
224.0.0.0/3
240.0.0.0/4
EOF

sudo masscan 0.0.0.0/0 -p 80,443 --excludefile /etc/masscan/exclude.conf --rate 100000
```

## Adapter and Source Configuration

```bash
# Specify network adapter (required on multi-interface systems)
sudo masscan 10.0.0.0/24 -p 1-65535 --adapter eth0 --rate 50000

# Specify source IP (spoof or use specific interface address)
sudo masscan 10.0.0.0/24 -p 80 --adapter-ip 192.168.1.100

# Specify source port range (avoid kernel RST on random high ports)
sudo masscan 10.0.0.0/24 -p 80 --adapter-port 60000-60100

# Specify router MAC (bypass ARP for direct L2 injection)
sudo masscan 10.0.0.0/24 -p 80 --router-mac DE:AD:BE:EF:CA:FE

# Set source MAC
sudo masscan 10.0.0.0/24 -p 80 --adapter-mac 12:34:56:78:90:AB
```

## Configuration Files

```bash
# Generate config file from CLI args
sudo masscan 10.0.0.0/24 -p 1-65535 --rate 10000 --echo > masscan.conf

# masscan.conf contents:
rate = 10000.00
randomize-hosts = true
seed = 42
output-format = json
output-status = open
output-filename = results.json
ports = 1-65535
range = 10.0.0.0/24
excludefile = /etc/masscan/exclude.conf

# Run from config
sudo masscan -c masscan.conf

# Run and resume interrupted scan
sudo masscan 0.0.0.0/0 -p 80 --rate 100000 --resume paused.conf
# (Masscan saves paused.conf automatically on Ctrl+C)
```

## Retries and Reliability

```bash
# Send each probe N times (default 1)
--retries 3

# Wait for responses longer (default 10s)
--wait 30

# Randomize host order (default on) — helps avoid rate-based detection
--randomize-hosts

# Fixed seed for reproducible scans
--seed 12345
```

## Comparison with nmap and RustScan

| Feature | Masscan | nmap | RustScan |
|---------|---------|------|----------|
| Speed | ★★★★★ (25Mpps) | ★★ (depends) | ★★★★ (~3Mpps async) |
| Service detection | None | Full (-sV) | Via nmap handoff |
| Script engine | None | NSE | None |
| OS fingerprinting | None | Yes (-O) | None |
| UDP support | Limited | Full | No |
| Banner grabbing | Basic | Full | None |
| Best use case | Mass port discovery | Detailed service scan | Fast open port → nmap |

**Practical rule:** Use Masscan for the first pass to find open ports, then feed to nmap for `-sV -sC` on confirmed-open ports only.

## Integration Pipeline: Masscan → nmap → Nuclei

```bash
#!/bin/bash
# Full pipeline: fast discovery → service scan → vuln scan
TARGET_RANGE="10.0.0.0/24"
RATE=10000

# Step 1: Masscan — fast open port discovery
sudo masscan "$TARGET_RANGE" -p 1-65535 --rate "$RATE" -oJ masscan-out.json

# Step 2: Parse open ports per host
python3 - << 'EOF'
import json, collections
with open('masscan-out.json') as f:
    data = json.load(f)
hosts = collections.defaultdict(set)
for entry in data:
    for p in entry['ports']:
        hosts[entry['ip']].add(str(p['port']))
with open('nmap-targets.txt', 'w') as f:
    for ip, ports in hosts.items():
        f.write(f"{ip} {','.join(sorted(ports, key=int))}\n")
EOF

# Step 3: nmap service + script scan on confirmed open ports
while read -r ip ports; do
    nmap -sV -sC -p "$ports" --open -oA "nmap-$ip" "$ip"
done < nmap-targets.txt

# Step 4: Nuclei vulnerability scan
cat masscan-out.json | jq -r '.[].ip' | sort -u > live-hosts.txt
nuclei -l live-hosts.txt -t ~/nuclei-templates/ -severity critical,high -o nuclei-out.txt
```

### Quick One-Liner: Live Host Discovery

```bash
# Find all live HTTP servers in range, output IP:port list
sudo masscan 10.0.0.0/8 -p 80,443,8080,8443 --rate 50000 -oL - 2>/dev/null \
  | awk '/open/{print $4":"$3}' | sort -u
```

### Extract Open Ports from JSON for nmap

```bash
# One-liner: masscan JSON → nmap comma-separated port list
cat masscan-out.json | jq -r '.[].ports[].port' | sort -un | tr '\n' ',' | sed 's/,$//'
```

## Advanced Techniques

### Internet-Scale Scanning

```bash
# Scan entire IPv4 Internet for SSH (compliant research use only)
sudo masscan 0.0.0.0/0 -p 22 \
  --rate 1000000 \
  --excludefile /etc/masscan/exclude.conf \
  --randomize-hosts \
  -oJ internet-ssh.json \
  --resume paused.conf
```

### Combining with shodan-cli

```bash
# Alternative: use Shodan facets for Internet-scale data without scanning
shodan stats --facets port country:100 "port:22"
# Then masscan only for scopes Shodan doesn't cover (RFC1918, new ranges)
```

### Scripted Range Splitting (Large Engagements)

```bash
# Split /8 into /16 chunks for parallel workers
for second in $(seq 0 255); do
    echo "10.${second}.0.0/16"
done | parallel -j8 'sudo masscan {} -p 22,80,443 --rate 5000 -oJ "masscan-{}.json"'
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `FAIL: rawsock: socket` | Run as root or with `sudo` |
| High packet loss / low effective rate | Reduce `--rate`; check `ethtool -S eth0` for drops |
| Results empty despite open ports | Kernel sending RST first — add iptables rule to drop RST on adapter-port |
| `no adapter found` | Specify `--adapter eth0` explicitly |
| macOS: `libpcap error` | Install Xcode CLI tools; ensure Wireshark/libpcap installed |
| Scan hangs at 100% | Normal — Masscan waits `--wait` seconds after last packet; let it finish |
| JSON output malformed | Last `}` may be missing if scan interrupted — use `--resume` or strip last line |
| Banner grab rate too slow | Drop `--rate` to 1000; banner mode holds connections open |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
