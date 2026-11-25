---
name: volatility3
description: >
  Perform memory forensics using Volatility3 — the Python framework for analyzing
  RAM dumps from Windows, Linux, and macOS systems. Use when investigating malware
  infections, rootkits, credential theft, injected code, lateral movement artifacts,
  or any scenario requiring process, network, file, or registry analysis from a
  memory image. Covers installation, acquiring memory dumps, all key plugins
  (pslist, pstree, netscan, malfind, hashdump, dumpfiles, cmdline), symbol table
  creation, Linux analysis, rootkit detection, and full malware analysis workflows.
metadata:
  author: redhoundinfosec
  version: '1.0'
  reference: https://github.com/volatilityfoundation/volatility3
---

# volatility3 Agent Skill

## When to Use This Skill

Use this skill when:
- Analyzing memory dumps from compromised Windows or Linux systems
- Hunting for injected code, process hollowing, or reflective DLL injection
- Extracting credentials from LSASS memory (`windows.hashdump`)
- Investigating network connections, open files, or registry state at time of capture
- Detecting rootkits via DKOM, hidden processes, or hook detection
- Building symbol tables for unfamiliar kernel versions
- The user asks about `vol.py`, Volatility3 plugins, or memory forensics workflow

## What Volatility3 Does

Volatility3 is a Python 3 rewrite of the Volatility Framework for memory forensics.
It analyzes raw memory images (physical RAM snapshots) and applies OS-aware parsing
to reconstruct kernel data structures, process lists, network state, file handles,
and more. Unlike Volatility 2, Volatility3 uses an ISF (Intermediate Symbol Format)
JSON symbol table system instead of profiles, enabling better cross-version support
without manual profile matching.

## Installation

```bash
# From PyPI
pip install volatility3

# From source (recommended — gets latest plugins)
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
pip install -e .

# Verify
python3 vol.py --help

# Install with all optional dependencies
pip install volatility3[full]
# Includes: pycryptodome, capstone, yara-python, leechcore
```

## Acquiring Memory Dumps

### Windows — WinPmem
```powershell
# Download WinPmem from GitHub
winpmem_mini_x64_rc2.exe --output memory.dmp
# Or to raw file:
winpmem_mini_x64_rc2.exe -o memory.raw
```

### Windows — ProcDump (LSASS only)
```powershell
procdump.exe -ma lsass.exe lsass.dmp
# Then parse with vol.py windows.hashdump or pypykatz
```

### Linux — AVML
```bash
# Acquire physical memory on Linux
sudo avml /tmp/memory.lime
# AVML: https://github.com/microsoft/avml
```

### Linux — LiME (Loadable Kernel Module)
```bash
git clone https://github.com/504ensicsLabs/LiME.git
cd LiME/src && make
# Load and capture to file
sudo insmod lime-$(uname -r).ko "path=/tmp/memory.lime format=lime"
# Or over network
sudo insmod lime-$(uname -r).ko "path=tcp:4444 format=lime"
# On attacker: nc VICTIM_IP 4444 > memory.lime
```

### macOS — osxpmem
```bash
sudo osxpmem.app/osxpmem -o memory.aff4
# Convert to raw:
sudo osxpmem.app/osxpmem -o memory.raw --format raw
```

## Key Windows Plugins

All commands assume: `python3 vol.py -f memory.dmp [PLUGIN]`

### System Information
```bash
# OS version, kernel base, PDB GUID
python3 vol.py -f memory.dmp windows.info

# List loaded kernel modules
python3 vol.py -f memory.dmp windows.modules

# List drivers (useful for rootkit detection)
python3 vol.py -f memory.dmp windows.driverlist
```

### Process Analysis
```bash
# List all processes (EPROCESS linked list)
python3 vol.py -f memory.dmp windows.pslist

# Tree view of parent/child relationships
python3 vol.py -f memory.dmp windows.pstree

# Detect hidden processes (DKOM — not in linked list)
python3 vol.py -f memory.dmp windows.psscan

# Cross-reference pslist vs psscan to find hidden procs
python3 vol.py -f memory.dmp windows.pslist > pslist.txt
python3 vol.py -f memory.dmp windows.psscan > psscan.txt
diff <(awk '{print $1}' pslist.txt) <(awk '{print $1}' psscan.txt)

# Command-line arguments for each process
python3 vol.py -f memory.dmp windows.cmdline

# Process environment variables
python3 vol.py -f memory.dmp windows.envars --pid 1234

# Process privileges
python3 vol.py -f memory.dmp windows.privileges --pid 1234
```

### Network Analysis
```bash
# Active and recently closed connections (Vista+)
python3 vol.py -f memory.dmp windows.netscan

# Older connection table (XP/2003)
python3 vol.py -f memory.dmp windows.connections

# Filter for established connections
python3 vol.py -f memory.dmp windows.netscan | grep ESTABLISHED

# Identify C2 connections: external IPs on uncommon ports
python3 vol.py -f memory.dmp windows.netscan | grep -v '127.0.0.1\|:445\|:139\|:80\|:443' \
  | grep ESTABLISHED
```

### File System Analysis
```bash
# Scan for FILE_OBJECT structures in memory
python3 vol.py -f memory.dmp windows.filescan

# Dump specific file by offset (from filescan output)
python3 vol.py -f memory.dmp windows.dumpfiles --virtaddr 0xfffffa8002d41060

# Dump all files matching pattern
python3 vol.py -f memory.dmp windows.dumpfiles --physaddr 0x1a2b3c4

# All files referenced by a process
python3 vol.py -f memory.dmp windows.handles --pid 1234 --object-type File
```

### Handles and DLLs
```bash
# All handles for a process (files, registry, mutants, events)
python3 vol.py -f memory.dmp windows.handles --pid 1234

# Loaded DLLs for all processes
python3 vol.py -f memory.dmp windows.dlllist

# DLLs for specific process
python3 vol.py -f memory.dmp windows.dlllist --pid 1234

# Detect hollowing: VAD entries vs DLL list discrepancies
python3 vol.py -f memory.dmp windows.vadlist --pid 1234
```

### Malware Detection
```bash
# Find injected code: executable + non-image VAD regions
python3 vol.py -f memory.dmp windows.malfind

# Malfind for specific PID
python3 vol.py -f memory.dmp windows.malfind --pid 1234

# Dump all malfind regions (for further analysis)
python3 vol.py -f memory.dmp windows.malfind --dump

# Detect API hooks in SSDT
python3 vol.py -f memory.dmp windows.ssdt

# IAT/EAT hook detection (via volshell or third-party plugins)
python3 vol.py -f memory.dmp windows.callbacks
```

### Credential Extraction
```bash
# Dump NTLM hashes from SAM/SYSTEM hive
python3 vol.py -f memory.dmp windows.hashdump

# LSA secrets
python3 vol.py -f memory.dmp windows.lsadump

# Cached domain credentials (DCC2 hashes)
python3 vol.py -f memory.dmp windows.cachedump
```

### Registry Analysis
```bash
# List all registry hives in memory
python3 vol.py -f memory.dmp windows.registry.hivelist

# Print all keys and values in a hive
python3 vol.py -f memory.dmp windows.registry.printkey \
  --offset 0xfffffa8001234000

# Common persistence keys
python3 vol.py -f memory.dmp windows.registry.printkey \
  --key "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

python3 vol.py -f memory.dmp windows.registry.printkey \
  --key "SYSTEM\CurrentControlSet\Services"
```

### Timeline
```bash
# Generate unified timeline of all artifacts
python3 vol.py -f memory.dmp timeliner > timeline.csv

# Sort by time
sort -t',' -k1 timeline.csv | less

# Filter to a time window (2024-01-15)
grep "2024-01-15" timeline.csv
```

## Linux Plugins

```bash
# Basic system info
python3 vol.py -f memory.lime linux.bash         # Bash history from memory
python3 vol.py -f memory.lime linux.pslist       # Process list
python3 vol.py -f memory.lime linux.pstree       # Process tree
python3 vol.py -f memory.lime linux.netstat      # Network connections
python3 vol.py -f memory.lime linux.lsof         # Open files
python3 vol.py -f memory.lime linux.malfind      # Injected code
python3 vol.py -f memory.lime linux.check_syscall  # Syscall table hooks
python3 vol.py -f memory.lime linux.check_modules  # Hidden kernel modules
python3 vol.py -f memory.lime linux.lsmod        # Loaded kernel modules
python3 vol.py -f memory.lime linux.bash --pid 1234  # Specific PID bash history
```

## Creating Symbol Tables

Volatility3 requires ISF JSON symbol tables instead of legacy profiles.

```bash
# For Windows: automatic download from Microsoft symbol server
# Vol3 downloads automatically if internet connected; or pre-cache:
python3 vol.py -f memory.dmp windows.info  # triggers auto-download

# Manual: download PDB, convert to ISF
pip install pdbconv
pdbconv.py -f ntkrnlmp.pdb -o ntkrnlmp.json
mkdir -p volatility3/volatility3/symbols/windows/
cp ntkrnlmp.json volatility3/volatility3/symbols/windows/

# For Linux: build ISF from running kernel (on the target)
git clone https://github.com/volatilityfoundation/dwarf2json.git
cd dwarf2json && go build .
sudo ./dwarf2json linux --elf /boot/vmlinuz-$(uname -r) \
  --system-map /boot/System.map-$(uname -r) > $(uname -r).json
# Copy JSON to: volatility3/volatility3/symbols/linux/
```

## Malware Analysis Workflow

### Step 1: Initial Triage
```bash
python3 vol.py -f memory.dmp windows.info        # Confirm OS version
python3 vol.py -f memory.dmp windows.pslist      # Baseline processes
python3 vol.py -f memory.dmp windows.netscan     # Network connections
python3 vol.py -f memory.dmp windows.cmdline     # Command lines
```

### Step 2: Identify Suspicious Processes
```bash
# Parent/child anomalies (e.g., Word spawning cmd.exe)
python3 vol.py -f memory.dmp windows.pstree | less

# Unknown processes not in pstree (DKOM)
python3 vol.py -f memory.dmp windows.psscan | grep -v [known_procs]

# Suspicious names (misspellings: svch0st, lsasss)
python3 vol.py -f memory.dmp windows.pslist | grep -iE "svch0|lsas[^s]|svchost[^.exe]"
```

### Step 3: Code Injection Analysis
```bash
python3 vol.py -f memory.dmp windows.malfind --dump
# Output files land in current directory as pid.*.dmp

# Check with YARA
yara malware_rules.yar *.dmp

# Disassemble suspicious region
python3 vol.py -f memory.dmp windows.disassemble --address 0xVAD_BASE --pid 1234
```

### Step 4: Persistence and Artifacts
```bash
python3 vol.py -f memory.dmp windows.registry.printkey --key "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
python3 vol.py -f memory.dmp windows.filescan | grep -i "startup\|appdata\|temp"
python3 vol.py -f memory.dmp windows.dlllist | grep -v "C:\\Windows"
```

### Step 5: Credential Extraction
```bash
python3 vol.py -f memory.dmp windows.hashdump
python3 vol.py -f memory.dmp windows.lsadump
```

## Rootkit Detection

```bash
# DKOM: compare pslist (linked list) vs psscan (pool tag scan)
python3 vol.py -f memory.dmp windows.psscan > psscan.txt
python3 vol.py -f memory.dmp windows.pslist > pslist.txt

# SSDT hooks
python3 vol.py -f memory.dmp windows.ssdt | grep -v "ntoskrnl\|win32k"

# IRP hook detection (driver-level hooks)
python3 vol.py -f memory.dmp windows.driverirp --driver DRIVER_NAME

# Kernel callbacks
python3 vol.py -f memory.dmp windows.callbacks
```

## Troubleshooting

**No symbol table found**: Run `windows.info` once to trigger auto-download.
If offline, manually download from the SpecterOps symbol server or build via dwarf2json.

**`ERROR: Unsupported page fault at`**: Memory dump is incomplete or corrupt.
Try `--single-location` flag or skip the problematic offset range.

**Plugin not found**: Ensure you're running from the volatility3 source directory
or that pip install completed fully. Check: `python3 vol.py --help | grep plugin_name`.

**Linux analysis fails**: Symbol table JSON must match the exact kernel version.
Re-generate with dwarf2json on the same kernel version.

**Malfind produces too many FPs**: Focus on VAD regions with `PAGE_EXECUTE_READWRITE`
protection AND a PE header (MZ). Filter: `windows.malfind | grep MZ`.
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Your Company Just Got Hit with Ransomware: A 48-Hour Survival Playbook for SMBs](https://redhound.us/ransomware-playbook)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
