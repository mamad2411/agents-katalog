---
name: mitmproxy
description: >
  Operate, script, and extend mitmproxy — an interactive TLS-capable intercepting proxy with
  three interfaces (console, web, scriptable dump). Use when working with mitmproxy/mitmproxy,
  when the user needs to intercept and modify HTTP/HTTPS traffic, write Python addons to
  automate request/response manipulation, replay flows, export to curl/httpie, analyze mobile
  app traffic, or run in transparent/reverse/upstream proxy modes. Covers all three binaries,
  proxy modes, CA installation, flow filtering, Python scripting API, addons, and Android/iOS
  configuration.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/mitmproxy/mitmproxy
  language: Python
---

# mitmproxy Agent Skill

## When to Use This Skill

Use this skill when:
- Intercepting and modifying HTTP/HTTPS traffic interactively
- Writing Python scripts to automate request/response manipulation
- Testing mobile applications (Android/iOS) by proxying their traffic
- Analyzing API traffic for security research or bug bounty
- Running as a transparent proxy on a network segment
- Replaying recorded HTTP flows for testing
- The user asks about mitmproxy, mitmweb, mitmdump, or TLS interception

## What mitmproxy Does

mitmproxy is a TLS-capable intercepting proxy with three interfaces: an interactive console
(`mitmproxy`), a browser-based UI (`mitmweb`), and a non-interactive scriptable tool
(`mitmdump`). All three share the same core engine and Python addon API. It performs TLS
interception by acting as a CA, dynamically generating per-site certificates. It supports
regular, transparent, reverse, upstream, and SOCKS proxy modes, and provides a powerful
Wireshark-inspired filter language for targeting specific flows.

## Installation

### pip (recommended)
```bash
pip install mitmproxy
# Installs mitmproxy, mitmweb, mitmdump

# Upgrade
pip install -U mitmproxy
```

### pipx (isolated environment)
```bash
pipx install mitmproxy
```

### Pre-built binaries
```bash
VERSION=10.4.2
curl -sSL https://downloads.mitmproxy.org/${VERSION}/mitmproxy-${VERSION}-linux-x86_64.tar.gz \
  | tar -xz
# Extracts mitmproxy, mitmweb, mitmdump
sudo mv mitmproxy mitmweb mitmdump /usr/local/bin/
```

### Docker
```bash
docker pull mitmproxy/mitmproxy
docker run --rm -it -p 8080:8080 -p 127.0.0.1:8081:8081 \
  -v ~/.mitmproxy:/home/mitmproxy/.mitmproxy \
  mitmproxy/mitmproxy mitmweb --web-host 0.0.0.0
```

### macOS
```bash
brew install mitmproxy
```

## Core Concepts

### Three Binaries
| Binary | Interface | Best For |
|---|---|---|
| `mitmproxy` | Terminal TUI | Interactive, real-time inspection |
| `mitmweb` | Browser UI at :8081 | GUI-friendly, shareable |
| `mitmdump` | Non-interactive | Scripting, CI, headless automation |

### Proxy Modes
| Mode | Flag | Description |
|---|---|---|
| Regular | (default) | HTTP proxy; clients must be configured to use it |
| Transparent | `--mode transparent` | ARP spoof or iptables redirect; clients unaware |
| Reverse | `--mode reverse:http://backend` | Proxy in front of a specific server |
| Upstream | `--mode upstream:http://proxy` | Chain through another proxy |
| SOCKS5 | `--mode socks5` | SOCKS5 proxy endpoint |
| WireGuard | `--mode wireguard` | Route via WireGuard interface (transparent on macOS/Linux) |

### CA Certificate
```
~/.mitmproxy/mitmproxy-ca-cert.pem      (PEM format)
~/.mitmproxy/mitmproxy-ca-cert.p12      (PKCS12)
~/.mitmproxy/mitmproxy-ca-cert.cer      (DER / Windows)
```
Generated automatically on first run. Must be installed on clients for TLS interception.

## Starting mitmproxy

```bash
# Interactive console proxy on port 8080 (default)
mitmproxy

# Web UI on port 8080 (proxy) + 8081 (web dashboard)
mitmweb
mitmweb --web-port 9090 --web-host 0.0.0.0   # Custom port, any interface

# Non-interactive dump (like tcpdump for HTTP)
mitmdump
mitmdump -w /tmp/capture.mitm    # Save flows to file
mitmdump -r /tmp/capture.mitm    # Replay/read flows from file

# Custom proxy port
mitmproxy -p 9090
mitmweb --listen-port 9090

# Bind to specific interface
mitmproxy --listen-host 0.0.0.0 -p 8080

# Quiet (suppress flow printing)
mitmdump -q

# Load an addon script
mitmproxy -s my_addon.py
mitmdump -s my_addon.py

# Transparent proxy mode
mitmproxy --mode transparent --showhost

# Reverse proxy
mitmproxy --mode reverse:https://api.example.com --listen-port 8080

# SOCKS5 proxy
mitmproxy --mode socks5 --listen-port 1080
```

## CA Certificate Installation

### Linux (system-wide)
```bash
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy.crt
sudo update-ca-certificates
```

### Firefox
Navigate to `about:preferences#privacy` → Certificates → View Certificates → Authorities →
Import → select `~/.mitmproxy/mitmproxy-ca-cert.pem`.

### Chrome/Chromium (Linux)
```bash
certutil -d sql:$HOME/.pki/nssdb -A -t CT,, -n mitmproxy -i ~/.mitmproxy/mitmproxy-ca-cert.pem
```

### macOS system keychain
```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain \
  ~/.mitmproxy/mitmproxy-ca-cert.pem
```

### Android (via device or emulator)
```bash
# Rename cert to hash format required by Android
openssl x509 -inform PEM -subject_hash_old \
  -in ~/.mitmproxy/mitmproxy-ca-cert.pem | head -1
# e.g., outputs: c8750f0d
cp ~/.mitmproxy/mitmproxy-ca-cert.pem c8750f0d.0

# Android 7+ requires root for system CA installation
adb root && adb shell mount -o rw,remount /system
adb push c8750f0d.0 /system/etc/security/cacerts/
adb shell chmod 644 /system/etc/security/cacerts/c8750f0d.0
adb reboot

# Alternative (Android 14+): use a network security config in the APK
# or use Frida to bypass cert pinning
```

### iOS
Send `mitm.it` URL from proxied browser → follow on-screen instructions, or manually:
Settings → General → VPN & Device Management → install profile → Settings → General →
About → Certificate Trust Settings → enable full trust.

## Flow Filtering (mitmproxy Filter Language)

mitmproxy uses a Wireshark-style filter expression language. Use in the REPL, `--intercept`, or
`--filter` flags.

```
~u REGEX          URL matches regex
~d DOMAIN         Domain matches
~m METHOD         HTTP method (GET, POST, etc.)
~s REGEX          Response body matches
~q REGEX          Request body matches
~h REGEX          Any header matches
~hq REGEX         Request header matches
~hs REGEX         Response header matches
~c CODE           Status code matches (exact or prefix: 2xx)
~t MIMETYPE       Content-Type matches
~tcp              TCP flow (not HTTP)
~websocket        WebSocket flow
~replay           Replayed flow
~e                Flow with error
~src IP           Source IP/CIDR
~dst IP           Destination IP/CIDR
! EXPR            NOT
EXPR & EXPR       AND
EXPR | EXPR       OR
```

```bash
# Examples
mitmproxy --intercept "~d api.example.com & ~m POST"
mitmproxy --intercept "~u /login & ~m POST"
mitmdump --filter "~d example.com" -w example-flows.mitm

# In REPL (press f to set filter)
# ~d example.com & ~c 200
# ~q password | ~q api_key
```

## Modifying Requests/Responses (Interactive)

### In mitmproxy TUI
- Arrow keys to select a flow
- `Enter` to view
- `e` to edit (select: method, url, http version, headers, body)
- `r` to replay request
- `a` to resume intercepted flow
- `d` to delete flow
- `D` to duplicate flow
- `x` to kill (reject) intercepted flow
- `i` to set intercept filter
- `w` to save flow to file
- `l` to load flows from file
- `z` to clear flow list
- `C` to export flow as curl command

## Python Scripting API (Addons)

mitmproxy's Python API uses event hooks. Create a class or module with hook functions.

### Addon hook reference
```python
# addon.py
import mitmproxy.http

class MyAddon:
    def request(self, flow: mitmproxy.http.HTTPFlow):
        """Called for every HTTP request before it's forwarded."""
        pass

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """Called for every HTTP response before it's returned to client."""
        pass

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        """Headers received, body not yet available."""
        pass

    def responseheaders(self, flow: mitmproxy.http.HTTPFlow):
        """Response headers received."""
        pass

    def tls_start_client(self, tls_start):
        """Called when TLS handshake to client begins."""
        pass

addons = [MyAddon()]
```

### Example: Log all POST bodies to file
```python
# log_posts.py
class PostLogger:
    def response(self, flow):
        if flow.request.method == "POST":
            with open("/tmp/posts.log", "a") as f:
                f.write(f"[{flow.request.host}] {flow.request.url}\n")
                f.write(flow.request.get_text() + "\n---\n")

addons = [PostLogger()]
```

### Example: Modify request headers
```python
# inject_header.py
class HeaderInjector:
    def request(self, flow):
        flow.request.headers["X-Forwarded-For"] = "127.0.0.1"
        flow.request.headers["X-Custom-Header"] = "injected"

addons = [HeaderInjector()]
```

### Example: Replace response body
```python
# patch_response.py
class BodyPatcher:
    def response(self, flow):
        if "api.example.com" in flow.request.pretty_host:
            if flow.response.status_code == 200:
                body = flow.response.get_text()
                body = body.replace('"admin": false', '"admin": true')
                flow.response.set_text(body)

addons = [BodyPatcher()]
```

### Example: Extract credentials from form posts
```python
# cred_harvest.py
from urllib.parse import parse_qs

class CredHarvester:
    def request(self, flow):
        ct = flow.request.headers.get("content-type", "")
        if "application/x-www-form-urlencoded" in ct:
            params = parse_qs(flow.request.get_text())
            interesting = {k: v for k, v in params.items()
                           if any(x in k.lower() for x in ["pass", "user", "email", "token"])}
            if interesting:
                print(f"[CRED] {flow.request.url}: {interesting}")

addons = [CredHarvester()]
```

### Example: Block specific domains
```python
# block_domain.py
from mitmproxy.http import HTTPFlow

BLOCKED = {"ads.example.com", "tracker.io"}

class Blocker:
    def request(self, flow: HTTPFlow):
        if flow.request.pretty_host in BLOCKED:
            flow.response = mitmproxy.http.Response.make(
                403, b"Blocked", {"Content-Type": "text/plain"}
            )

addons = [Blocker()]
```

## Replaying Flows

```bash
# Record flows
mitmdump -w recorded.mitm

# Replay all recorded requests (client replay)
mitmdump -r recorded.mitm --client-replay recorded.mitm

# Replay with modification via script
mitmdump -r recorded.mitm -s modify_replay.py

# In mitmproxy TUI
# Select a flow → r to replay
# Select multiple flows → R to replay all selected
```

## Exporting Flows

```bash
# In mitmproxy TUI: select a flow → E → choose format
# Formats: curl, httpie, raw_request, raw_response, har

# mitmdump one-liner: convert to HAR
mitmdump -r capture.mitm -w - | python3 -c "
import sys, mitmproxy.io, json, mitmproxy.flowfilter
# (use mitmproxy-har package for full HAR export)
"

# Export as curl (all flows)
mitmdump -r capture.mitm -ns -q 2>/dev/null | \
  python3 - --export curl   # Or use mitmproxy TUI

# Install mitmproxy-har for clean HAR export
pip install mitmproxy-har
mitmdump -s mitmproxy_har/har_dump.py --set hardump=./dump.har -r capture.mitm
```

## Mobile App Traffic Interception

### Android (non-root, Android ≤ 6)
```bash
# Configure WiFi proxy on device: Settings → WiFi → Modify → Proxy → Manual
# Host: attacker IP, Port: 8080
# Browse to mitm.it on device to install CA
mitmproxy --listen-host 0.0.0.0 -p 8080
```

### Android 7+ (user CA not trusted for apps)
```bash
# Option 1: Root + system CA install (see CA section above)
# Option 2: Repackage APK with network_security_config.xml
# Option 3: Use Frida to bypass SSL pinning
# Option 4: Use objection for runtime bypass
objection -g com.example.app explore --startup-command "android sslpinning disable"
```

### iOS
```bash
# Settings → WiFi → network → HTTP Proxy → Manual
# Host: attacker IP, Port: 8080
# Browse to mitm.it on device → install profile → trust in Certificate Trust Settings
mitmproxy --listen-host 0.0.0.0 -p 8080
```

## Transparent Proxy Mode (iptables redirect)

```bash
# On the proxy machine (Linux)
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# Redirect HTTP and HTTPS to mitmproxy
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80  -j REDIRECT --to-port 8080
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8080

# Start in transparent mode
mitmproxy --mode transparent --showhost -p 8080

# Route traffic through this machine (ARP spoof target host → use bettercap)
```

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| TLS handshake failed | CA not trusted by client | Install mitmproxy CA cert |
| Certificate pinning bypass fails | App uses cert pinning | Use Frida/objection or patch APK |
| No traffic appearing | Proxy not configured on client | Verify system/app proxy settings |
| Transparent mode drops packets | IP forwarding disabled | `echo 1 > /proc/sys/net/ipv4/ip_forward` |
| `AddressAlreadyInUse` | Port 8080 in use | Use `-p 9090` |
| Addon import errors | Python path issues | Run `mitmproxy -s addon.py` from correct venv |
| iOS traffic still encrypted | Profile not trusted | Settings → About → Certificate Trust Settings |
| QUIC/HTTP3 not interceptable | UDP-based; not supported | Force HTTP/2: block UDP 443 via iptables |

```bash
# Debug: run with verbose output
mitmproxy -v

# Test CA installation
curl --proxy http://127.0.0.1:8080 https://example.com

# Inspect saved flows
mitmdump -r capture.mitm -n  # Replay without sending (dry run)
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
