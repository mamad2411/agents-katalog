---
name: wireshark
description: >
  Capture, analyze, and dissect network traffic with Wireshark and tshark. Use when
  analyzing PCAPs, performing live network capture, decrypting TLS/SSL traffic, debugging
  protocols, hunting for credentials or sensitive data in network streams, or automating
  packet analysis. Covers capture vs display filters, BPF syntax, stream following,
  protocol hierarchy, IO graphs, tshark CLI, ring buffer capture, SSL/TLS decryption
  with pre-master secrets, WiFi and USB capture, expert info, statistics, and coloring
  rules for penetration testing and network forensics workflows.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/wireshark/wireshark
---

# wireshark Agent Skill

## When to Use This Skill

Use this skill when:
- Analyzing captured `.pcap`/`.pcapng` files for credentials, tokens, or sensitive data
- Performing live packet capture during a penetration test or network assessment
- Decrypting TLS traffic using pre-master secret logs or private keys
- Automating PCAP processing with `tshark` in scripts and pipelines
- The user asks about display filters, capture filters, BPF syntax, or stream following
- Capturing WiFi or USB traffic for hardware/wireless analysis

## What Wireshark Does

Wireshark is the world's leading network protocol analyzer, capable of live capture and offline analysis of hundreds of protocols. It provides both a GUI (Wireshark) and a CLI equivalent (tshark) for automation. In offensive security contexts it is used for credential harvesting from cleartext protocols, certificate inspection, session token extraction, protocol reverse engineering, and PCAP-based evidence review.

## Installation

```bash
# Kali / Debian / Ubuntu
sudo apt update && sudo apt install wireshark tshark
# During install: allow non-root capture? → Yes (adds user to wireshark group)
sudo usermod -aG wireshark $USER && newgrp wireshark

# macOS
brew install --cask wireshark
brew install wireshark  # tshark only (no GUI)

# Windows
# Download installer from https://www.wireshark.org/download.html
# Installs WinPcap/Npcap driver automatically

# Verify
wireshark --version
tshark --version
```

## Core Concepts

### Capture Filters vs Display Filters

| Type | Language | Applied | Purpose |
|------|----------|---------|---------|
| Capture filter | BPF (Berkeley Packet Filter) | At capture time | Reduce file size; cannot see filtered packets later |
| Display filter | Wireshark DFL | At analysis time | Non-destructive; original packets retained |

**Rule**: Always use capture filters when doing long-term captures to conserve disk. Use display filters during analysis — they are reversible.

### BPF Syntax (Capture Filters)

```
# Protocol filters
tcp
udp
icmp
arp

# Host / port
host 10.10.10.10
not host 10.10.10.10
src host 10.10.10.10
dst host 10.10.10.10
net 10.10.10.0/24
port 80
not port 22
portrange 8000-8080

# Logical operators
tcp and host 10.10.10.10
udp or icmp
not arp and not broadcast

# Protocol + port
tcp port 443
udp port 53
tcp port 80 or tcp port 443

# Capture only first 96 bytes of each packet (headers only)
-s 96   # snaplen flag in tshark/tcpdump
```

### Display Filter Syntax (DFL)

```
# Protocol
http
dns
tls
smb
smb2
ftp
smtp
pop
imap
ssh
rdp
kerberos
ldap
icmp

# Field comparisons
ip.addr == 10.10.10.10
ip.src == 10.10.10.10
ip.dst == 10.10.10.10
ip.addr != 192.168.1.1
ip.addr >= 10.0.0.1 && ip.addr <= 10.0.0.254

# Port filters
tcp.port == 443
tcp.port in {80 443 8080 8443}
udp.port == 53
tcp.srcport == 4444
tcp.dstport == 80

# TCP flags
tcp.flags.syn == 1
tcp.flags.ack == 1
tcp.flags.fin == 1
tcp.flags.reset == 1
tcp.flags == 0x002    # SYN only
tcp.flags == 0x018    # PSH+ACK (data packets)
tcp.analysis.retransmission   # Retransmissions
tcp.analysis.duplicate_ack    # Duplicate ACKs

# HTTP
http.request.method == "POST"
http.response.code == 200
http.response.code >= 400
http contains "password"
http.request.uri contains "login"
http.host == "target.com"
http.cookie contains "session"

# DNS
dns.qry.name == "target.com"
dns.qry.type == 1       # A records
dns.qry.type == 28      # AAAA
dns.qry.type == 15      # MX
dns.flags.response == 1 # DNS responses only

# TLS
tls.handshake.type == 1   # ClientHello
tls.handshake.type == 2   # ServerHello
tls.record.version == 0x0303  # TLS 1.2
ssl.handshake.ciphersuite  # cipher suite field

# SMB
smb.cmd == 0x72         # Negotiate
smb2.cmd == 1           # SESSION_SETUP
smb2.filename contains "password"

# Kerberos
kerberos.msg_type == 10   # AS-REQ
kerberos.msg_type == 11   # AS-REP
kerberos.msg_type == 12   # TGS-REQ

# NTLM (in HTTP/SMB)
ntlmssp.messagetype == 1  # NEGOTIATE
ntlmssp.messagetype == 2  # CHALLENGE
ntlmssp.messagetype == 3  # AUTHENTICATE

# Frame / length
frame.len > 1000
frame.len < 100
frame.number == 42

# String searches
frame contains "password"
frame contains "Authorization"
tcp contains "GET /"

# Logical operators
http && ip.src == 10.10.10.10
dns || dhcp
!(arp || icmp || dns)   # Exclude noise
http.request && http.request.method == "POST"
```

## CLI Reference — tshark

```bash
# List available interfaces
tshark -D
# Example output: 1. eth0  2. wlan0  3. lo  4. any

# Live capture
tshark -i eth0
tshark -i eth0 -w capture.pcapng       # Write to file
tshark -i eth0 -c 1000 -w out.pcapng  # Capture 1000 packets then stop
tshark -i any -w all_ifaces.pcapng    # Capture on all interfaces

# Apply capture filter
tshark -i eth0 -f "tcp port 80" -w http.pcapng

# Read PCAP and apply display filter
tshark -r capture.pcapng -Y "http.request.method == POST"
tshark -r capture.pcapng -Y "dns" -T fields -e dns.qry.name | sort -u

# Field extraction (-T fields -e <field>)
tshark -r capture.pcapng \
  -Y "http.request" \
  -T fields \
  -e ip.src -e http.host -e http.request.uri -e http.request.method

# Extract HTTP POST bodies
tshark -r capture.pcapng \
  -Y "http.request.method == POST" \
  -T fields \
  -e http.file_data \
  -e ip.src -e http.host

# Follow TCP stream to file (stream 0)
tshark -r capture.pcapng -q -z follow,tcp,ascii,0

# Follow specific stream
tshark -r capture.pcapng -Y "tcp.stream eq 5" \
  -T fields -e tcp.payload | xxd

# Protocol statistics
tshark -r capture.pcapng -q -z io,phs          # Protocol hierarchy
tshark -r capture.pcapng -q -z conv,tcp        # TCP conversations
tshark -r capture.pcapng -q -z endpoints,ip    # IP endpoints
tshark -r capture.pcapng -q -z http,tree       # HTTP statistics

# Extract files (HTTP objects, SMB files, etc.)
tshark -r capture.pcapng --export-objects http,/tmp/http_objects/
tshark -r capture.pcapng --export-objects smb,/tmp/smb_objects/
tshark -r capture.pcapng --export-objects dicom,/tmp/dicom/
tshark -r capture.pcapng --export-objects tftp,/tmp/tftp/

# Read key log file for TLS decryption
tshark -r tls_capture.pcapng \
  -o "tls.keylog_file:/tmp/ssl_keylog.txt" \
  -Y "http" \
  -T fields -e http.request.uri

# Output formats
tshark -r capture.pcapng -T json > packets.json
tshark -r capture.pcapng -T jsonraw > packets_raw.json
tshark -r capture.pcapng -T pdml > packets.xml
tshark -r capture.pcapng -T ek  > packets_elk.json  # Elasticsearch format

# Ring buffer capture (long-term)
tshark -i eth0 -b filesize:50000 -b files:10 -w /tmp/ring/capture.pcapng
# Keeps 10 files × 50MB = 500MB max rolling window

# Time-limited capture
tshark -i eth0 -a duration:3600 -w /tmp/hourly.pcapng  # Capture 1 hour
tshark -i eth0 -a packets:10000 -w /tmp/10k.pcapng     # Stop at 10k packets
```

## Common Workflows

### Extracting Credentials from Cleartext Protocols

```bash
# HTTP Basic Auth (Base64-encoded)
tshark -r capture.pcapng -Y "http.authorization" \
  -T fields -e ip.src -e http.authorization | \
  while IFS=$'\t' read ip auth; do
    creds=$(echo "$auth" | sed 's/Basic //' | base64 -d)
    echo "$ip → $creds"
  done

# FTP credentials
tshark -r capture.pcapng -Y "ftp.request.command == USER || ftp.request.command == PASS" \
  -T fields -e ip.src -e ftp.request.command -e ftp.request.arg

# SMTP AUTH
tshark -r capture.pcapng -Y "smtp.req.parameter" \
  -T fields -e ip.src -e smtp.req.command -e smtp.req.parameter

# Telnet (raw stream)
tshark -r capture.pcapng -q -z follow,tcp,ascii,0 2>/dev/null | grep -i "login\|pass"

# POP3
tshark -r capture.pcapng -Y "pop.request" \
  -T fields -e ip.src -e pop.request.command -e pop.request.parameter
```

### TLS/SSL Decryption

```bash
# Method 1: Pre-master secret log (SSLKEYLOGFILE — most reliable)
# In browser or application: export SSLKEYLOGFILE=/tmp/ssl_keys.log
# Then capture traffic while the browser runs, then open PCAP in Wireshark:
# Edit → Preferences → Protocols → TLS → (Pre)-Master-Secret log filename → /tmp/ssl_keys.log

# CLI decryption with keylog
tshark -r encrypted.pcapng \
  -o "tls.keylog_file:/tmp/ssl_keys.log" \
  -Y "http" \
  -T fields -e http.request.uri -e http.file_data

# Method 2: RSA private key (only works for non-PFS cipher suites)
# Edit → Preferences → Protocols → TLS → RSA keys list
# Host: 10.10.10.10, Port: 443, Protocol: http, Key file: /path/server.key

# tshark with RSA key
tshark -r encrypted.pcapng \
  -o "tls.keys_list:10.10.10.10,443,http,/path/to/server.key" \
  -Y "http"
```

### WiFi Capture

```bash
# Put interface into monitor mode
sudo airmon-ng start wlan0
# Interface becomes wlan0mon

# Capture with tshark on specific channel
sudo tshark -i wlan0mon -f "channel 6" -w wifi_capture.pcapng

# In Wireshark GUI: Capture → Interfaces → wlan0mon → start
# Display filter for specific BSSID:
wlan.bssid == aa:bb:cc:dd:ee:ff
# WPA handshake capture:
eapol
```

### USB Capture

```bash
# Linux: load usbmon kernel module
sudo modprobe usbmon
tshark -D | grep usb  # Lists usbmon0, usbmon1, etc.
sudo tshark -i usbmon0 -w usb_capture.pcapng

# Wireshark display filters for USB
usb.transfer_type == 0x03   # Interrupt transfers (keyboards, mice)
usb.data_len > 0
# HID keyboard decode: use Wireshark plugin or manual lookup table
```

## Advanced Techniques

### Extracting NTLM Hashes for Cracking

```bash
# Find NTLM authentication attempts
tshark -r capture.pcapng \
  -Y "ntlmssp.messagetype == 0x00000003" \
  -T fields \
  -e ntlmssp.auth.domain \
  -e ntlmssp.auth.username \
  -e ntlmssp.auth.hostname \
  -e ntlmssp.ntlmserverchallenge \
  -e ntlmssp.auth.ntresponse
# Format captured hash into NTLMv2 format for hashcat -m 5600
```

### Automating PCAP Analysis

```bash
#!/bin/bash
# Extract all DNS queries from a PCAP
tshark -r "$1" -Y "dns.qry.type == 1" \
  -T fields -e frame.time -e ip.src -e dns.qry.name \
  2>/dev/null | sort -u | tee dns_queries.txt

# Find large transfers (potential exfil)
tshark -r "$1" -q -z conv,tcp 2>/dev/null | \
  sort -k3 -rn | head -20

# Extract all URIs
tshark -r "$1" -Y "http.request" \
  -T fields -e http.host -e http.request.uri 2>/dev/null | \
  sed 's/\t//' | sort -u | tee uris.txt
```

### Ring Buffer for Long-Term Capture

```bash
# Capture indefinitely, rotate every 100MB, keep last 20 files
tshark -i eth0 \
  -b filesize:102400 \
  -b files:20 \
  -w /captures/ring.pcapng \
  -f "not arp and not broadcast" &

# Stop after 24 hours
tshark -i eth0 -a duration:86400 \
  -b filesize:102400 -b files:48 \
  -w /captures/daily.pcapng
```

### Custom Coloring Rules (GUI)

View → Coloring Rules (or `colorfilters` file in Wireshark profile):
```
# Example entries (Name, Filter, Foreground, Background)
Bad TCP      | tcp.analysis.flags && !tcp.analysis.window_update | Red | White
HTTP POST    | http.request.method == "POST" | Black | Yellow
Kerberos     | kerberos | White | Purple
NTLM         | ntlmssp | White | Dark Blue
DNS Fail     | dns.flags.rcode != 0 | White | Red
```

### IO Graphs and Statistics

```
# GUI: Statistics → IO Graph
# Add multiple lines per filter to compare traffic volumes

# GUI: Statistics → Protocol Hierarchy → reveals protocol breakdown
# GUI: Statistics → Conversations → TCP/UDP/IP tabs
# GUI: Statistics → Endpoints → see top talkers

# Expert Info (Analyze → Expert Information)
# Shows: Errors (TCP resets), Warnings (retransmits), Notes (sequence issues)
```

## Troubleshooting

**No interfaces listed (Linux non-root):**
```bash
sudo usermod -aG wireshark $USER && newgrp wireshark
# Or run: sudo setcap cap_net_raw,cap_net_admin=eip $(which dumpcap)
```

**TLS decryption not working:**
- Confirm key log is from the same session as the PCAP
- RSA key decryption only works if the handshake used RSA key exchange (not ECDHE/DHE — those use PFS)
- Check Wireshark version: TLS 1.3 requires key log file, not RSA key

**Performance with large PCAPs:**
```bash
# Split large PCAP before opening in GUI
editcap -c 100000 large.pcapng split_out.pcapng   # 100k packets per file
editcap -A "2024-01-01 00:00:00" -B "2024-01-01 01:00:00" large.pcapng sliced.pcapng
```

**tshark field returns empty:**
- Verify field name with `tshark -G fields | grep -i "field_keyword"`
- Some fields only exist in specific directions (req vs resp)

**Capture drops packets at high rate:**
- Increase ring buffer, reduce snaplen: `tshark -s 96` (headers only)
- Offload to `tcpdump` for raw capture, analyze with `tshark` offline
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [How to Reduce SIEM Alert Noise by 80%](https://redhound.us/reduce-siem-noise)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
