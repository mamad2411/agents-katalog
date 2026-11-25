---
name: scapy
description: >
  Build, extend, and operate Scapy — an interactive Python packet manipulation library
  for crafting, sending, sniffing, and dissecting network packets. Use when the user
  asks about Scapy, custom packet crafting, network fuzzing, protocol implementation,
  ARP scanning, SYN scanning, traceroute, DNS queries, pcap analysis, wireless frame
  injection, or scripting automated network probes. Covers interactive mode, layer
  stacking, all major send/receive functions, sniffing with callbacks, ARP/SYN/DNS
  operations, pcap I/O, RadioTap wireless injection, GRE tunneling, and network fuzzing.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/secdev/scapy
---

# scapy Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to craft custom packets at any layer (L2–L7)
- Building network scanners, fuzzers, or protocol testing tools in Python
- Performing ARP scans, SYN scans, or traceroutes with custom logic
- Sniffing and dissecting live traffic or pcap files
- Injecting 802.11 wireless frames or testing tunneled protocols (GRE, VXLAN)
- The user asks about Scapy's send/receive functions or filter syntax

## What Scapy Does

Scapy is a powerful interactive Python library and CLI for low-level packet manipulation.
It can forge or decode packets of a wide number of protocols, send them on the wire, capture
them, match requests and replies, and much more. Unlike libpcap-based tools, Scapy lets you
construct arbitrary packets by stacking protocol layers with the `/` operator, giving complete
control over every field. It is the go-to tool for network research, protocol fuzzing,
custom scanner development, and security testing.

## Installation

```bash
# pip (Python 3)
pip3 install scapy

# With all optional dependencies (plotting, voice, Bluetooth, etc.)
pip3 install scapy[complete]

# Kali/Debian
sudo apt install python3-scapy -y

# Required for raw socket operations
sudo python3 -c "from scapy.all import *"   # Must run as root or with CAP_NET_RAW

# Verify
python3 -c "import scapy; print(scapy.__version__)"
```

## Interactive Mode

```bash
sudo scapy    # Launch interactive REPL (IPython-based if available)
```

Inside the REPL:

```python
# Tab completion on layer fields
IP().  # press tab → shows all IP fields

# Display layer fields and defaults
IP().show()
ls(IP)       # All fields with types and defaults
ls(TCP)
ls(Ether)

# Show protocol hierarchy
lsc()        # List all Scapy commands
conf.iface   # Current default interface
conf.iface = "eth0"   # Set interface
```

## Building Packets

### Layer Stacking with /

```python
from scapy.all import *

# Ethernet / IP / TCP
pkt = Ether() / IP(dst="10.10.10.1") / TCP(dport=80, flags="S")

# IP / UDP
pkt = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="example.com"))

# IP / ICMP
pkt = IP(dst="192.168.1.1") / ICMP()

# Raw payload
pkt = IP(dst="10.10.10.5") / TCP(dport=9001) / Raw(load="GET / HTTP/1.0\r\n\r\n")

# ARP
pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.1")

# Show constructed packet
pkt.show()
pkt.show2()   # With computed fields (checksum, length filled in)
hexdump(pkt)
```

### Specifying Fields

```python
# IP fields
IP(src="1.2.3.4", dst="5.6.7.8", ttl=128, proto=6, id=0x1337)

# TCP fields
TCP(sport=12345, dport=443, seq=1000, ack=0, flags="S", window=65535,
    options=[('MSS', 1460)])

# TCP flags
# S=SYN, A=ACK, F=FIN, R=RST, P=PSH, U=URG, SA=SYN-ACK
TCP(flags=0x002)   # Numeric SYN
TCP(flags="SA")    # SYN-ACK string

# UDP fields
UDP(sport=53, dport=5353)

# ICMP types
ICMP(type=8, code=0)   # Echo request
ICMP(type=3, code=3)   # Port unreachable
```

## Sending and Receiving

### Send Functions Summary

| Function | Layer | Returns | Notes |
|----------|-------|---------|-------|
| `send()` | L3 (IP) | None | Fire and forget |
| `sendp()` | L2 (Ether) | None | Fire and forget |
| `sr()` | L3 | (answered, unanswered) | Send/receive loop |
| `sr1()` | L3 | First response | Most common |
| `srp()` | L2 | (answered, unanswered) | With Ethernet |
| `srp1()` | L2 | First response | Single L2 reply |
| `srpflood()` | L2 | None | Flood, no receive |

### send / sendp

```python
# Send a single IP packet (L3)
send(IP(dst="10.10.10.1") / ICMP(), verbose=0)

# Send multiple packets (loop)
send(IP(dst="10.10.10.1") / ICMP(), count=10, inter=0.1)

# Send L2 packet on a specific interface
sendp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="10.10.10.1"),
      iface="eth0", verbose=0)
```

### sr / sr1 (Send + Receive)

```python
# sr returns (answered, unanswered) pair lists
ans, unans = sr(IP(dst="10.10.10.1") / TCP(dport=80, flags="S"),
                timeout=2, verbose=0)

# Access results
for sent, received in ans:
    print(f"Reply: {received.summary()}")

# sr1 returns only the first response packet
resp = sr1(IP(dst="8.8.8.8") / ICMP(), timeout=2, verbose=0)
if resp:
    resp.show()

# With retry
resp = sr1(IP(dst="10.0.0.1") / TCP(dport=443, flags="S"),
           timeout=3, retry=2, verbose=0)
```

### srp (L2 Send + Receive)

```python
# ARP request/response
ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.1/24"),
             iface="eth0", timeout=2, verbose=0)
for sent, received in ans:
    print(f"{received.psrc} is at {received.hwsrc}")
```

## Common Operations

### ARP Scan

```python
from scapy.all import *

def arp_scan(network):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network),
                 iface="eth0", timeout=2, verbose=0)
    hosts = []
    for sent, received in ans:
        hosts.append({'ip': received.psrc, 'mac': received.hwsrc})
        print(f"{received.psrc:20s} {received.hwsrc}")
    return hosts

arp_scan("192.168.1.0/24")
```

### SYN Scan

```python
from scapy.all import *

def syn_scan(target, ports):
    open_ports = []
    for port in ports:
        resp = sr1(IP(dst=target) / TCP(dport=port, flags="S"),
                   timeout=1, verbose=0)
        if resp is None:
            continue
        if resp.haslayer(TCP):
            if resp[TCP].flags == 0x12:   # SYN-ACK
                open_ports.append(port)
                # Send RST to close gracefully
                send(IP(dst=target) / TCP(dport=port, flags="R"), verbose=0)
            elif resp[TCP].flags == 0x14:  # RST-ACK → closed
                pass
    return open_ports

ports = range(1, 1025)
print(syn_scan("10.10.10.5", ports))
```

### Traceroute

```python
from scapy.all import *

# Built-in traceroute
result, _ = traceroute("8.8.8.8", maxttl=20, verbose=0)
result.show()

# Manual TTL-based traceroute
def my_traceroute(dst, max_hops=30):
    for ttl in range(1, max_hops + 1):
        pkt = IP(dst=dst, ttl=ttl) / ICMP()
        resp = sr1(pkt, timeout=1, verbose=0)
        if resp is None:
            print(f"{ttl:2d}  *")
        elif resp.type == 0:  # ICMP Echo Reply → destination reached
            print(f"{ttl:2d}  {resp.src}  (destination)")
            break
        else:
            print(f"{ttl:2d}  {resp.src}")

my_traceroute("8.8.8.8")
```

### DNS Queries

```python
from scapy.all import *

# A record query
resp = sr1(IP(dst="8.8.8.8") / UDP(dport=53) /
           DNS(rd=1, qd=DNSQR(qname="example.com", qtype="A")),
           timeout=2, verbose=0)
if resp and resp.haslayer(DNS):
    for i in range(resp[DNS].ancount):
        print(resp[DNS].an[i].rdata)

# ANY query
resp = sr1(IP(dst="8.8.8.8") / UDP(dport=53) /
           DNS(rd=1, qd=DNSQR(qname="example.com", qtype="ANY")),
           timeout=2, verbose=0)
resp[DNS].show()

# DNS zone transfer (AXFR via TCP)
resp = sr1(IP(dst="ns1.example.com") / TCP(dport=53) /
           DNS(rd=0, qd=DNSQR(qname="example.com", qtype="AXFR")),
           timeout=5, verbose=0)
```

## Sniffing

### Basic Sniff

```python
from scapy.all import *

# Capture 10 packets on eth0
pkts = sniff(iface="eth0", count=10)
pkts.summary()
pkts[0].show()

# BPF filter
pkts = sniff(iface="eth0", filter="tcp port 80", count=50)

# Callback (process each packet as it arrives)
def process(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        print(pkt[Raw].load)

sniff(iface="eth0", filter="tcp port 80", prn=process, store=0)

# Stop condition
sniff(iface="eth0", stop_filter=lambda p: p.haslayer(ICMP), store=1)

# All interfaces
sniff(filter="arp", prn=lambda p: p.summary())
```

### Credential Sniffing Example

```python
from scapy.all import *

def http_sniffer(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        payload = pkt[Raw].load.decode('utf-8', errors='ignore')
        if 'POST' in payload or 'Authorization' in payload:
            print(f"[{pkt[IP].src}→{pkt[IP].dst}] {payload[:200]}")

sniff(iface="eth0", filter="tcp port 80", prn=http_sniffer, store=0)
```

## Reading and Writing PCAP

```python
from scapy.all import *

# Write packets to pcap
pkts = sniff(iface="eth0", count=100)
wrpcap("/tmp/capture.pcap", pkts)

# Read pcap
pkts = rdpcap("/tmp/capture.pcap")
pkts.summary()

# Append to pcap
pkts2 = sniff(count=50)
wrpcap("/tmp/capture.pcap", pkts2, append=True)

# Process large pcaps with PcapReader (streaming)
with PcapReader("/tmp/large_capture.pcap") as reader:
    for pkt in reader:
        if pkt.haslayer(DNS):
            print(pkt[DNS].qd.qname)
```

## Wireless Injection (802.11)

```bash
# Put adapter in monitor mode first
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# Or: airmon-ng start wlan0 → produces wlan0mon
```

```python
from scapy.all import *

# Send deauth frame (RadioTap + Dot11)
def deauth(target_mac, bssid, iface="wlan0mon", count=100):
    dot11 = Dot11(addr1=target_mac, addr2=bssid, addr3=bssid)
    frame = RadioTap() / dot11 / Dot11Deauth(reason=7)
    sendp(frame, iface=iface, count=count, inter=0.1, verbose=0)

# Beacon flood
def beacon_flood(ssid, iface="wlan0mon"):
    dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff",
                  addr2="aa:bb:cc:dd:ee:ff", addr3="aa:bb:cc:dd:ee:ff")
    beacon = Dot11Beacon(cap="ESS+privacy")
    essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
    frame = RadioTap() / dot11 / beacon / essid
    sendp(frame, iface=iface, count=100, inter=0.1, verbose=0)

# Sniff probe requests
def sniff_probes(iface="wlan0mon"):
    def handler(pkt):
        if pkt.haslayer(Dot11ProbeReq):
            ssid = pkt[Dot11Elt].info.decode('utf-8', errors='ignore')
            print(f"Probe from {pkt.addr2}: {ssid}")
    sniff(iface=iface, prn=handler, store=0)
```

## GRE Tunneling and Custom Protocols

```python
from scapy.all import *

# GRE encapsulation
inner = IP(src="10.0.0.1", dst="10.0.0.2") / TCP(dport=80) / Raw(b"GET / HTTP/1.0\r\n\r\n")
gre_pkt = IP(src="1.2.3.4", dst="5.6.7.8") / GRE() / inner
send(gre_pkt, verbose=0)

# VXLAN (manual construction)
vxlan_hdr = bytes.fromhex("0800000000000a00")  # VXLAN header, VNI 10
inner_eth = Ether() / IP(dst="10.0.0.2") / ICMP()
pkt = IP(dst="5.6.7.8") / UDP(dport=4789) / Raw(vxlan_hdr + bytes(inner_eth))
send(pkt)
```

## Network Fuzzing

```python
from scapy.all import *

# Fuzz a specific field (random values)
fuzz_pkt = IP(dst="10.10.10.5") / fuzz(TCP())
send(fuzz_pkt, verbose=0)

# Fuzz loop
for i in range(100):
    pkt = IP(dst="10.10.10.5") / fuzz(UDP(dport=5060)) / Raw(os.urandom(64))
    send(pkt, verbose=0)

# Mutation fuzzing
base = IP(dst="10.10.10.5") / TCP(dport=80, flags="S")
for length in range(0, 1500, 50):
    pkt = base / Raw(load="A" * length)
    sr1(pkt, timeout=0.5, verbose=0)
```

## Integration with Other Tools

| Tool | Use Case |
|------|----------|
| Wireshark | Open pcaps written by wrpcap() for deep GUI analysis |
| nmap | Use Scapy for custom probe logic nmap can't express |
| Metasploit | Combine ARP scan results with msfconsole targets |
| tshark | Process large pcaps; feed interesting flows to Scapy for reassembly |
| Impacket | Complement Scapy for SMB/LDAP/Kerberos protocol work |

## Troubleshooting

**Permission denied / no route to host:**
```bash
sudo python3 script.py    # Scapy needs root for raw sockets
# Or grant capabilities:
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```

**Interface not found:**
```python
from scapy.all import get_if_list
print(get_if_list())   # List available interfaces
conf.iface = "ens33"   # Set correct interface
```

**Packets not received (sr1 returns None):**
- Check BPF filter isn't too narrow
- Increase timeout: `sr1(..., timeout=5)`
- Verify target is reachable with `send(IP(dst=...) / ICMP())`
- On VMs, check promiscuous mode: `ip link set eth0 promisc on`

**Wireless injection fails:**
```bash
# Confirm monitor mode
iw dev wlan0 info | grep type   # Should show "monitor"
# Some drivers need: iw dev wlan0 set monitor none
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
