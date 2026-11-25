---
name: yara
description: >
  Write, compile, and apply YARA rules for malware detection and threat hunting.
  Use when the user needs to create pattern-matching rules for malware samples,
  write detection signatures for threat intelligence, scan files or process memory,
  integrate YARA with ClamAV or LOKI, or work with the YARA-X Rust rewrite.
  Covers rule syntax, string types, conditions, modules (pe, elf, math, hash,
  cuckoo), CLI usage, writing detection rules for real-world malware families,
  and integration into SOC/IR workflows.
metadata:
  author: redhoundinfosec
  version: '1.0'
  reference: https://github.com/VirusTotal/yara
---

# yara Agent Skill

## When to Use This Skill

Use this skill when:
- Writing malware detection signatures for threat hunting
- The user needs to identify specific malware families by byte patterns or strings
- Performing incident response and scanning a host for known-bad indicators
- Creating YARA rules from malware samples (static analysis)
- Integrating YARA with LOKI, Thor, ClamAV, or custom scan pipelines
- The user asks about YARA-X (the Rust-based rewrite) features
- Scanning process memory for injected shellcode or unpacked malware

## What YARA Does

YARA is a pattern-matching engine designed for malware researchers. Rules describe
patterns (strings, bytes, regular expressions) and logical conditions that combine
them. When executed, YARA tests files, directories, or running process memory
against the ruleset and reports matches. It is the de facto standard for malware
signature creation and is embedded in nearly every major threat intelligence and
IR platform.

## Installation

```bash
# Package manager (Ubuntu/Debian)
sudo apt install yara

# Homebrew (macOS)
brew install yara

# From source (with all modules)
sudo apt install automake libtool make gcc pkg-config \
  libssl-dev libjansson-dev libmagic-dev libcrypto++-dev

git clone https://github.com/VirusTotal/yara.git
cd yara
./bootstrap.sh
./configure --with-crypto --enable-cuckoo --enable-magic --enable-dotnet
make
sudo make install

# Python bindings (yara-python)
pip install yara-python

# YARA-X (Rust rewrite)
cargo install yara-x
# or download binary from: https://github.com/VirusTotal/yara-x/releases
```

## Rule Syntax

### Basic Rule Structure

```yara
rule RuleName {
    meta:
        description = "Detects Example Malware"
        author      = "analyst@example.com"
        date        = "2024-04-01"
        hash        = "d41d8cd98f00b204e9800998ecf8427e"
        severity    = "high"
        family      = "ExampleFamily"
        reference   = "https://example.com/analysis"

    strings:
        $s1 = "malicious_string"
        $s2 = { 4D 5A 90 00 03 00 00 00 }
        $s3 = /malware_\w{4,8}\.exe/i

    condition:
        uint16(0) == 0x5A4D and   // MZ header
        filesize < 1MB and
        any of ($s*)
}
```

## String Types

### Text Strings
```yara
// Case-insensitive
$s1 = "CreateRemoteThread" nocase

// Wide (UTF-16LE — common in Windows binaries)
$s2 = "cmd.exe" wide

// Both ASCII and wide
$s3 = "powershell" wide ascii

// Full word matching (not substring)
$s4 = "evil" fullword
```

### Hex Strings (Byte Patterns)
```yara
// Fixed bytes
$h1 = { 55 8B EC 83 EC 20 }

// Wildcards (any single byte)
$h2 = { 55 8B ?? 83 EC ?? }

// Nibble wildcards
$h3 = { E8 ?5 00 00 00 }

// Alternation
$h4 = { ( 55 | 56 ) 8B EC }

// Jumps (between 4 and 8 bytes of anything)
$h5 = { 55 8B EC [4-8] 83 EC 28 }

// Infinite jumps
$h6 = { 55 8B EC [-] C3 }
```

### Regular Expressions
```yara
// IPv4 address
$re1 = /\b(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}\b/

// Base64-encoded string
$re2 = /[A-Za-z0-9+\/]{50,}={0,2}/

// URL pattern
$re3 = /https?:\/\/[^\s"']{10,}/

// Registry key
$re4 = /HKEY_(LOCAL_MACHINE|CURRENT_USER)\\[^\x00]{5,100}/i
```

## Conditions

### Counting and Selection
```yara
// All strings must match
condition: all of them

// Any one string matches
condition: any of them

// At least 3 of the $s* strings
condition: 3 of ($s*)

// All hex patterns, any string
condition: all of ($h*) and any of ($s*)

// Specific string count (occurs at least twice)
condition: #s1 >= 2

// Specific string count (exactly 3 times)
condition: #s1 == 3
```

### Offset and Range Conditions
```yara
// String at specific offset
condition: $s1 at 0

// String in first 512 bytes
condition: $s1 in (0..512)

// String at PE entry point (requires pe module)
condition: $s1 at pe.entry_point

// In last 1024 bytes
condition: $s1 in (filesize-1024..filesize)
```

### File Size and Type
```yara
condition: filesize < 500KB
condition: filesize > 1MB and filesize < 10MB

// MZ header check (PE file)
condition: uint16(0) == 0x5A4D

// ELF header
condition: uint32(0) == 0x464C457F

// PDF header
condition: uint32(0) == 0x46445025
```

## Modules

### PE Module
```yara
import "pe"

rule PEAnalysis {
    condition:
        pe.is_pe and
        pe.number_of_sections > 5 and
        pe.imphash() == "d41d8cd98f00b204e9800998ecf8427e" and
        pe.exports("EvilExport") and
        pe.imports("kernel32.dll", "VirtualAlloc") and
        pe.imports("kernel32.dll", "WriteProcessMemory") and
        pe.timestamp > 1704067200 and   // After 2024-01-01
        pe.is_signed == false
}

// Check for specific section name or high entropy (packed/encrypted)
rule SuspiciousPE {
    condition:
        pe.is_pe and
        for any i in (0..pe.number_of_sections - 1): (
            pe.sections[i].name == ".upx0" or
            pe.sections[i].entropy > 7.5
        )
}
```

### ELF Module
```yara
import "elf"

rule SuspiciousELF {
    condition:
        elf.type == elf.ET_EXEC and
        elf.number_of_sections > 20 and
        elf.symtab_entries > 0
}
```

### Math Module
```yara
import "math"

rule HighEntropy {
    condition:
        // High entropy in first 8KB suggests packing/encryption
        math.entropy(0, 8192) > 7.5
}

rule SuspiciousData {
    condition:
        math.mean(0, filesize) < 100  // Most bytes are low values (shellcode NOP sleds)
}
```

### Hash Module
```yara
import "hash"

rule KnownBadHash {
    condition:
        // Match by MD5 of a specific section
        hash.md5(0, filesize) == "d41d8cd98f00b204e9800998ecf8427e"
}
```

### Cuckoo Module (Sandbox Integration)
```yara
import "cuckoo"
rule NetworkBeacon {
    condition:
        cuckoo.network.dns_lookup(/malware\.c2\.com/) or
        cuckoo.network.http_get(/\/gate\.php/)
}
```

## YARA CLI Usage

```bash
# Scan a single file
yara rules.yar /path/to/sample.exe

# Scan a directory recursively
yara -r rules.yar /path/to/samples/

# Scan all running processes
yara rules.yar -p $(ps aux | awk 'NR>1 {print $2}' | paste -sd,)
# Or process-by-process:
for pid in $(ps aux | awk 'NR>1 {print $2}'); do yara rules.yar $pid 2>/dev/null; done

# Print matching strings
yara -s rules.yar sample.exe

# Print tags
yara -g rules.yar sample.exe

# Print metadata
yara -m rules.yar sample.exe

# Negate — only report non-matching files
yara -n rules.yar /path/to/samples/

# List matching rule names only
yara -r rules.yar /samples/ 2>/dev/null | awk '{print $1}' | sort | uniq -c | sort -rn

# Timeout per file (seconds)
yara --timeout=30 rules.yar /samples/

# Compile rules to binary (faster repeated scanning)
yarac rules.yar compiled.yarc
yara compiled.yarc /samples/

# Scan with multiple rule files
yara rule1.yar rule2.yar sample.exe
```

## Writing Effective Detection Rules

### Step 1: Identify Unique Artifacts
From a malware sample, extract:
- Unique strings (error messages, C2 paths, mutex names, registry keys)
- Byte sequences (function prologues, shellcode stubs, decryption routines)
- Behavioral indicators (API call sequences, file name patterns)

```bash
# Extract strings from binary
strings -n 8 sample.exe
strings -e l sample.exe  # wide strings (UTF-16LE)

# Hex dump for byte patterns
xxd sample.exe | head -50
```

### Step 2: Avoid FP-Prone Patterns
- Avoid common Windows API names alone (use combinations)
- Prefer fullword or context-anchored strings
- Test against clean file collections before deploying

### Step 3: Write Layered Conditions
```yara
rule AgentTesla_Stealer {
    meta:
        description = "Detects Agent Tesla infostealer"
        family      = "AgentTesla"
        severity    = "high"

    strings:
        // Unique strings from samples
        $s1 = "get_Browsers" nocase
        $s2 = "SmtpClient"
        $s3 = "AgentTesla" nocase
        $s4 = "SMTP_HOST" fullword

        // .NET artifacts
        $n1 = { 72 [3] 70 28 [3] 0A }   // ldstr + call pattern

        // Mutex name pattern
        $m1 = /[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}/ nocase

    condition:
        uint16(0) == 0x5A4D and
        filesize < 5MB and
        (
            2 of ($s*) or
            ($n1 and 1 of ($s*))
        )
}
```

## YARA-X (yara-x)

YARA-X is the Rust rewrite of YARA with improved performance and correctness.

```bash
# Install
cargo install yara-x-cli

# Scan (similar CLI to yara)
yr scan rules.yar sample.exe
yr scan -r rules.yar /samples/

# Compile rules
yr compile rules.yar -o compiled.yarc

# Dump rule AST (debugging)
yr dump rules.yar

# Check rules for warnings
yr check rules.yar
```

Key differences from YARA classic:
- Stricter type checking (fewer silent failures)
- Faster scanning on large file collections
- `base64` and `base64wide` string modifiers built-in
- `xor` modifier supports key ranges: `$s = "key" xor(1-255)`

## Integration with Other Tools

### LOKI (Compromise Scanner)
```bash
pip install loki
# Drop YARA rules in: loki/signature-base/yara/
python3 loki.py -p /path/to/scan --noindicator
```

### ClamAV Integration
```bash
# Convert YARA rule to ClamAV database
sigtool --yara-import=rules.yar > rules.ndb
cp rules.ndb /var/lib/clamav/
freshclam && clamscan -r /path/to/scan
```

### Python Scripting
```python
import yara

# Compile from string
rule = yara.compile(source='''
rule Test {
    strings:
        $s = "evil"
    condition:
        $s
}
''')

# Scan file
matches = rule.match('/tmp/sample.exe')
for m in matches:
    print(f"[+] Match: {m.rule}")
    for s in m.strings:
        print(f"    {s}")

# Scan process memory
matches = rule.match(pid=1234)

# Scan bytes in memory
data = open('/tmp/sample.exe', 'rb').read()
matches = rule.match(data=data)
```

### Threat Intelligence Workflow
```bash
# Download community rulesets
git clone https://github.com/Neo23x0/signature-base.git

# Scan malware zoo
yara -r signature-base/yara/ /opt/malware_samples/ 2>/dev/null \
  | sort | uniq -c | sort -rn > detections.txt

# Quick triage of unknown file
yara -s signature-base/yara/gen_suspicious_strings.yar unknown_file.exe
```

## Common Rule Patterns for Malware Families

```yara
// Detect Cobalt Strike beacon (common patterns)
rule CobaltStrike_Beacon {
    strings:
        $s1 = "%s (admin)" fullword
        $s2 = "beacon.x64.dll"
        $h1 = { FC 48 83 E4 F0 E8 }    // beacon shellcode stub
        $h2 = { 48 83 EC 20 48 8B 05 } // x64 reflective loader
    condition:
        uint16(0) == 0x5A4D and any of them
}

// Detect Mimikatz
rule Mimikatz {
    strings:
        $s1 = "sekurlsa::" nocase
        $s2 = "kerberos::" nocase
        $s3 = "lsadump::" nocase
        $s4 = "mimikatz" nocase
        $s5 = "gentilkiwi" nocase
    condition:
        3 of them
}
```

## Troubleshooting

**Rule compilation error**: Use `yara --fail-on-warnings rules.yar /dev/null` to
catch all issues. Check for unclosed strings, missing `import` statements, or
invalid regex syntax.

**High false positive rate**: Add `fullword`, `nocase` selectively, anchor to
file offsets or PE structure. Test against clean corpora (Windows system files).

**Slow scanning**: Compile rules first with `yarac`. For directory scans, use
`-r` with specific file extensions: `find /samples -name "*.exe" | xargs yara rules.yar`.

**Process scan permission denied**: Run as root or with `CAP_SYS_PTRACE`. On
Linux: `setcap cap_sys_ptrace+ep $(which yara)`.

**Module not found**: Recompile YARA from source with `--with-crypto`,
`--enable-cuckoo`, `--enable-magic` flags.
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Your Company Just Got Hit with Ransomware: A 48-Hour Survival Playbook for SMBs](https://redhound.us/ransomware-playbook)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
