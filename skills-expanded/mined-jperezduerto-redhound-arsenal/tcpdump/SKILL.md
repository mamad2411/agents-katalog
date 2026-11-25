---
name: tcpdump
description: >
  Build, extend, and operate tcpdump — the command-line packet analyzer for capturing
  and analyzing network traffic. Use when the user asks about tcpdump, packet capture,
  BPF filters, pcap files, network traffic analysis, protocol-specific filtering,
  rotating captures, remote capture over SSH, or integrating with Wireshark. Covers
  capture basics, all major flags, BPF filter syntax, output verbosity, ASCII/hex
  display, timestamp formats, rotating captures, common protocol filters, credential
  extraction patterns, attack analysis, and Wireshark integration.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/the-tcpdump-group/tcpdump
---

# tcpdump Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to capture live network traffic from the command line
- Writing BPF filters to isolate specific protocols, hosts, or ports
- Analyzing pcap files for credentials, attacks, or anomalies
- Performing long-running captures with file rotation
- Capturing traffic remotely over SSH and piping to Wireshark
- The user asks about tcpdump flags, output formats, or filter syntax

## What tcpdump Does

tcpdump is the canonical command-line packet analyzer, available on virtually every Unix-like
system. It uses libpcap to capture packets from a network interface and either displays them
to stdout or writes them to a pcap file. Its Berkeley Packet Filter (BPF) language provides
highly efficient kernel-level packet filtering before capture, minimizing overhead. tcpdump is
the first-line tool for network debugging, traffic analysis, IDS/IPS testing, and security
monitoring on systems where Wireshark is unavailable.

## Installation

```bash
# Debian/Ubuntu/Kali
sudo apt install tcpdump -y

# RHEL/CentOS/Rocky
sudo yum install tcpdump -y

# macOS (pre-installed; update via Homebrew)
brew install tcpdump

# Verify
tcpdump --version
```

**Privileges:** tcpdump requires root or `CAP_NET_RAW`. Grant to non-root user:
```bash
sudo setcap cap_net_raw,cap_net_admin=eip $(which tcpdump)
```

## Core Concepts

### BPF (Berkeley Packet Filter)

BPF filters run in the kernel before packets are handed to tcpdump, making them extremely
efficient. The filter language uses primitives (`host`, `port`, `net`, `proto`) combined with
logical operators (`and`/`&&`, `or`/`||`, `not`/`!`) and grouping with parentheses.

### pcap File Format

tcpdump writes industry-standard `.pcap` files (libpcap format) readable by Wireshark, tshark,
snort, zeek, and most other network analysis tools.

## CLI Reference

### Interface and Basic Capture

```bash
# List available interfaces
tcpdump -D
ip link show   # Alternative

# Capture on specific interface
tcpdump -i eth0

# Capture on any interface
tcpdump -i any

# Capture N packets then stop
tcpdump -i eth0 -c 100

# Do not resolve hostnames (faster, shows IPs)
tcpdump -i eth0 -n

# Do not resolve hostnames or port names
tcpdump -i eth0 -nn

# Write to pcap file
tcpdump -i eth0 -w /tmp/capture.pcap

# Write without name resolution (recommended for forensics)
tcpdump -i eth0 -nn -w /tmp/capture.pcap

# Capture to file + display to stdout simultaneously
tcpdump -i eth0 -w /tmp/capture.pcap | tee /dev/stderr
```

### Output Verbosity

```bash
# Default (one line per packet)
tcpdump -i eth0 port 80

# Verbose (additional fields: TTL, ID, total length)
tcpdump -i eth0 -v port 80

# More verbose (additional IP options, sequence numbers)
tcpdump -i eth0 -vv port 80

# Maximum verbosity (NFS, SMB, DNS decode)
tcpdump -i eth0 -vvv port 53

# Print absolute sequence numbers (easier to follow TCP streams)
tcpdump -i eth0 -S port 80
```

### Packet Content Display

```bash
# ASCII output (readable text payloads)
tcpdump -i eth0 -A port 80

# Hex + ASCII output
tcpdump -i eth0 -X port 80

# Hex only
tcpdump -i eth0 -x port 80

# Hex + ASCII with verbose
tcpdump -i eth0 -Xvvv port 80

# Full packet hex dump (no truncation)
tcpdump -i eth0 -XX port 80

# Set snaplen (capture N bytes per packet, default 262144 in modern tcpdump)
tcpdump -i eth0 -s 0 port 80    # -s 0 = full packet length
```

### Timestamp Formats

```bash
# Default: HH:MM:SS.microseconds
tcpdump -i eth0

# No timestamp
tcpdump -i eth0 -t

# Unix epoch timestamp
tcpdump -i eth0 -tt

# Delta from previous packet (inter-packet timing)
tcpdump -i eth0 -ttt

# Date + time
tcpdump -i eth0 -tttt

# Delta from first packet captured
tcpdump -i eth0 -ttttt
```

### Reading PCAP Files

```bash
# Read pcap file
tcpdump -r /tmp/capture.pcap

# Read with filter
tcpdump -r /tmp/capture.pcap 'port 80'

# Read without name resolution
tcpdump -nn -r /tmp/capture.pcap

# Read and display payload
tcpdump -A -r /tmp/capture.pcap 'tcp port 80'

# Read and count packets
tcpdump -r /tmp/capture.pcap | wc -l
```

### Rotating Captures (Long-Running)

```bash
# Rotate by file size: new file every 100MB (C = 100 MB), keep 10 files (W = 10)
tcpdump -i eth0 -nn -w /tmp/capture-%Y%m%d-%H%M%S.pcap -C 100 -W 10

# Rotate by time: new file every 300 seconds (G = 300s), keep 24 files
tcpdump -i eth0 -nn -w /tmp/capture-%Y%m%d-%H%M%S.pcap -G 300 -W 24

# Rotate by time AND stop after N rotations
tcpdump -i eth0 -nn -w /tmp/cap.pcap -G 60 -W 60  # 60 minutes of capture, 60 files
```

## BPF Filter Reference

### Host and Network Filters

```bash
# Single host (src or dst)
tcpdump host 10.10.10.5

# Source only
tcpdump src host 10.10.10.5

# Destination only
tcpdump dst host 10.10.10.5

# Network/subnet
tcpdump net 192.168.1.0/24
tcpdump src net 10.0.0.0/8

# Exclude host
tcpdump not host 10.10.10.1

# Between two specific hosts
tcpdump 'host 10.10.10.1 and host 10.10.10.2'
```

### Port Filters

```bash
# Single port
tcpdump port 443

# Source port
tcpdump src port 443

# Destination port
tcpdump dst port 80

# Port range
tcpdump portrange 8000-8100

# Combine host and port
tcpdump 'host 10.10.10.5 and port 22'
```

### Protocol Filters

```bash
# Layer 3 protocols
tcpdump ip        # IPv4
tcpdump ip6       # IPv6
tcpdump arp
tcpdump icmp
tcpdump icmp6

# Layer 4 protocols
tcpdump tcp
tcpdump udp

# Protocol by number
tcpdump 'ip proto 47'   # GRE (protocol 47)
tcpdump 'ip proto 50'   # ESP (IPSec)
tcpdump 'ip proto 89'   # OSPF
```

### TCP Flag Filters

```bash
# TCP SYN packets (new connections)
tcpdump 'tcp[tcpflags] & tcp-syn != 0'
# Shorthand:
tcpdump 'tcp[13] & 2 != 0'

# SYN only (not SYN-ACK)
tcpdump 'tcp[tcpflags] == tcp-syn'

# RST packets
tcpdump 'tcp[tcpflags] & tcp-rst != 0'

# FIN packets
tcpdump 'tcp[tcpflags] & tcp-fin != 0'

# PSH+ACK (data packets)
tcpdump 'tcp[tcpflags] & (tcp-push|tcp-ack) != 0'
```

### Protocol-Specific Filters

```bash
# HTTP
tcpdump -A -nn 'tcp port 80 or tcp port 8080'

# HTTPS (shows TLS handshake, not payload)
tcpdump -nn 'tcp port 443'

# DNS (UDP and TCP)
tcpdump -vvv -nn 'port 53'

# DHCP
tcpdump -nn -vv 'udp port 67 or udp port 68'

# ARP
tcpdump -nn 'arp'

# ICMP
tcpdump -nn 'icmp'

# ICMP echo requests only
tcpdump -nn 'icmp[icmptype] == icmp-echo'

# SMB / CIFS
tcpdump -nn 'port 445 or port 139'

# RDP
tcpdump -nn 'port 3389'

# Kerberos
tcpdump -nn 'port 88'

# NTP
tcpdump -nn 'udp port 123'

# SNMP
tcpdump -nn 'udp port 161 or udp port 162'
```

### Complex Compound Filters

```bash
# All traffic to/from a host except SSH
tcpdump 'host 10.10.10.5 and not port 22'

# HTTP traffic between two specific hosts
tcpdump 'port 80 and (host 10.0.0.1 or host 10.0.0.2)'

# Non-ICMP traffic on a subnet
tcpdump 'net 192.168.1.0/24 and not icmp'

# TCP connections (SYN only) to common web ports
tcpdump 'tcp[tcpflags] == tcp-syn and (port 80 or port 443 or port 8080)'

# DNS queries (outbound UDP port 53)
tcpdump 'src port != 53 and dst port 53'

# Large packets (potential data exfiltration or DoS)
tcpdump 'ip[2:2] > 1000'

# Packets with specific payload bytes (e.g., HTTP GET)
tcpdump 'tcp[20:4] = 0x47455420'   # "GET "
```

## Credential Extraction Patterns

```bash
# Capture HTTP Basic Auth credentials
tcpdump -i eth0 -A -nn 'tcp port 80' | grep -i "authorization: basic\|POST\|password="

# Capture FTP credentials
tcpdump -i eth0 -A -nn 'tcp port 21' | grep -E "USER |PASS "

# Capture Telnet characters
tcpdump -i eth0 -A -nn 'tcp port 23'

# Capture POP3 / IMAP plaintext auth
tcpdump -i eth0 -A -nn 'tcp port 110 or tcp port 143' | grep -i "user\|pass\|login"

# Capture SMTP AUTH
tcpdump -i eth0 -A -nn 'tcp port 25 or tcp port 587' | grep -i "AUTH\|MAIL FROM\|RCPT TO"

# Capture SMB NTLMv2 hashes (relay setup)
tcpdump -i eth0 -nn -w /tmp/smb.pcap 'port 445'
# Then process with: impacket-ntlmrelayx or responder
```

## Attack Analysis Patterns

```bash
# Detect SYN scan (many SYN, no ACK)
tcpdump -nn -i eth0 'tcp[tcpflags] == tcp-syn' -c 1000 | \
  awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head -20

# Detect ARP spoofing (duplicate ARP replies)
tcpdump -nn -e 'arp' 2>/dev/null | grep "reply" | \
  awk '{print $NF}' | sort | uniq -c | sort -rn

# Detect DNS tunneling (high-frequency, large DNS queries)
tcpdump -nn -vvv 'udp port 53' 2>&1 | grep "A?" | \
  awk '{print $6}' | sort | uniq -c | sort -rn | head -20

# Detect ICMP tunneling (large ICMP payloads)
tcpdump -nn -vvv 'icmp and ip[2:2] > 100'

# Capture reverse shell traffic (common ports)
tcpdump -i eth0 -nn -A 'tcp port 4444 or tcp port 1234 or tcp port 9001 or tcp port 443'

# Identify hosts doing port scanning
tcpdump -i eth0 -nn 'tcp[tcpflags] == tcp-syn' | \
  awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn
```

## Remote Capture over SSH

```bash
# Capture remotely, pipe to local Wireshark (real-time)
ssh root@10.10.10.1 "tcpdump -nn -w - -i eth0 not port 22" | \
  wireshark -k -i -

# Save remote capture to local file
ssh root@10.10.10.1 "tcpdump -nn -c 10000 -w - -i eth0" > /tmp/remote_capture.pcap

# Capture on remote with filter, pipe to local tshark
ssh root@10.10.10.1 "tcpdump -nn -w - -i eth0 port 80" | \
  tshark -r - -Y 'http.request' -T fields -e http.host -e http.request.uri

# Persistent remote capture (runs until killed)
ssh -o ServerAliveInterval=60 root@10.10.10.1 \
  "tcpdump -nn -w - -i eth0 -s 0 'not port 22'" | \
  tcpdump -r - -w /tmp/remote_$(date +%Y%m%d_%H%M%S).pcap
```

## Integration with Wireshark

```bash
# Open existing pcap in Wireshark
wireshark /tmp/capture.pcap &

# Live capture in tcpdump, analyze in Wireshark via named pipe
mkfifo /tmp/pcap_pipe
wireshark -k -i /tmp/pcap_pipe &
tcpdump -i eth0 -nn -w /tmp/pcap_pipe

# Apply Wireshark display filter after tcpdump BPF capture:
# BPF captures broadly, Wireshark's display filter refines:
tcpdump -i eth0 -w /tmp/cap.pcap
# In Wireshark: http.request.method == "POST"
# In Wireshark: smb2.cmd == 1 (SMB2 Negotiate)
# In Wireshark: kerberos.msg_type == 14 (TGS-REQ)

# tshark (CLI Wireshark) for scripting
tshark -r /tmp/capture.pcap -Y 'http.request' \
  -T fields -e ip.src -e http.host -e http.request.uri -e http.request.method
```

## Common One-Liners

```bash
# Top talkers
tcpdump -nn -c 10000 -i eth0 | awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head

# Extract all URIs from HTTP traffic
tcpdump -A -nn -i eth0 'port 80' | grep "GET\|POST\|Host:" | grep -v "^--"

# Capture only DNS queries and log them
tcpdump -nn -i eth0 'udp port 53' | grep " A?" | awk '{print $NF}' | tee /tmp/dns_queries.log

# Monitor a specific process's network activity (combine with ss/lsof for PID-to-port mapping)
ss -tunap | grep <pid>   # Find the port
tcpdump -nn -i eth0 "port <found_port>"

# Quick credential hunt on a PCAP
tcpdump -A -r /tmp/capture.pcap 'tcp' | strings | grep -i "password\|passwd\|secret\|token\|api_key"
```

## Troubleshooting

**"Permission denied" on interface:**
```bash
sudo tcpdump -i eth0
# Or: sudo setcap cap_net_raw,cap_net_admin=eip $(which tcpdump)
```

**"Interface does not exist":**
```bash
tcpdump -D          # List available interfaces
ip addr show        # Cross-reference
# Use -i any for all interfaces
```

**Captured file has no packets:**
- Check the filter isn't too restrictive: test without filter first
- Verify traffic actually exists: `ping` the target while capturing
- Confirm correct interface: `tcpdump -D` and match to active IP

**Truncated packet content:**
```bash
tcpdump -i eth0 -s 0 ...   # Capture full packets (no truncation)
```

**Cannot read pcap in Wireshark:**
```bash
# Check file is valid pcap
file /tmp/capture.pcap    # Should say "tcpdump capture file"
capinfos /tmp/capture.pcap
# Repair corrupted pcap:
pcapfix /tmp/capture.pcap -o /tmp/repaired.pcap
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [How to Reduce SIEM Alert Noise by 80%](https://redhound.us/reduce-siem-noise)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
