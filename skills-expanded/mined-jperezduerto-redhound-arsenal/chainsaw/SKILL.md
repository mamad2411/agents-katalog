---
name: chainsaw
description: >
  Operate Chainsaw — a fast Windows event log (EVTX) analysis tool with Sigma rule integration for
  rapid threat hunting and incident response. Use when analyzing Windows event logs for lateral
  movement, credential access, persistence, execution, or defense evasion artifacts. Covers
  installation (cargo, releases), hunt mode with Sigma rules, search mode, dump mode, supported
  formats (EVTX, JSON), output formats (ASCII table, CSV, JSON), writing custom detection rules,
  key detection categories, and incident response triage workflows.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/WithSecureLabs/chainsaw
  stars: '3.4k'
  language: Rust
---

# chainsaw Agent Skill

## When to Use This Skill

Use this skill when:
- Conducting incident response and need to triage Windows event logs quickly
- Running threat hunting exercises against collected EVTX files
- Processing Windows event logs from disk images or evidence collection
- Applying Sigma rules to event logs without a SIEM
- Searching for specific keywords, process names, or IOCs across large EVTX sets
- The user asks about Windows event log analysis, EVTX parsing, or Sigma detection

## What Chainsaw Does

Chainsaw is a Rust-based CLI tool that reads Windows Event Log (EVTX) files and either hunts them
against a library of Sigma detection rules or searches them for keywords/patterns. It is designed for
speed — parsing millions of events in seconds — and produces structured output in ASCII table, CSV,
or JSON format. In incident response engagements, Chainsaw replaces slow manual review in Windows
Event Viewer when logs are collected offline.

## Installation

### Method 1 — Download Pre-compiled Release (recommended)

```bash
# Linux (x86_64)
VERSION=$(curl -s https://api.github.com/repos/WithSecureLabs/chainsaw/releases/latest \
  | grep tag_name | cut -d '"' -f4)
wget "https://github.com/WithSecureLabs/chainsaw/releases/download/${VERSION}/chainsaw_x86_64-unknown-linux-musl.tar.gz"
tar -xzf chainsaw_x86_64-unknown-linux-musl.tar.gz
chmod +x chainsaw

# Windows (x86_64)
# Download: chainsaw_x86_64-pc-windows-msvc.zip from releases page

# macOS (Apple Silicon)
# Download: chainsaw_aarch64-apple-darwin.tar.gz from releases page

# Verify
./chainsaw --version
```

### Method 2 — Build from Source (Cargo)

```bash
# Install Rust toolchain if not present
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Clone and build
git clone https://github.com/WithSecureLabs/chainsaw.git
cd chainsaw
cargo build --release
# Binary at: ./target/release/chainsaw
```

### Get Sigma Rules and Mappings

Chainsaw ships with its own rule set and mappings, but supplementing with upstream Sigma rules
improves coverage significantly.

```bash
# Clone Sigma rules repository
git clone https://github.com/SigmaHQ/sigma.git

# Chainsaw's built-in rules and mappings (included in release)
ls chainsaw/
# chainsaw  mappings/  rules/  examples/
# mappings/ contains YAML files mapping Sigma fields to EVTX field names
```

## Core Concepts

### EVTX Format

Windows Event Log files (`.evtx`) are binary files containing structured XML records. Each record has:
- `System.EventID` — event type (e.g., 4624 = Logon, 4688 = Process Creation)
- `System.TimeCreated` — timestamp
- `System.Computer` — host that generated the event
- `System.Channel` — log channel (Security, System, Application, PowerShell, etc.)
- `EventData` — payload fields specific to the event type

Chainsaw parses EVTX files using the `evtx` Rust crate and converts records to JSON internally.

### Sigma Rules

Sigma is a generic signature format for SIEM detection rules. A Sigma rule specifies:
- `detection.selection` — field/value conditions
- `detection.condition` — logical combination of selections
- `logsource` — which log channel/category the rule applies to

Chainsaw uses **mapping files** (`mappings/`) to translate Sigma's generic field names to EVTX's
actual XML field paths, enabling direct application of Sigma rules to raw EVTX files.

### Modes

| Mode | Purpose |
|------|---------|
| `hunt` | Apply Sigma rules to EVTX files; output matching events with rule names |
| `search` | Full-text or field-specific keyword search across EVTX files |
| `dump` | Convert EVTX files to JSON/CSV for external processing |
| `analyse` | Pre-built analysis modules (shimcache, shimdb, etc.) |

## CLI Reference

### Hunt Mode

Hunt mode applies Sigma rules to event logs and surfaces matches with rule name, severity, and event detail.

```bash
# Basic hunt — apply all rules in rules/ directory to an EVTX directory
./chainsaw hunt EVTX_DIR/ -s rules/ -m mappings/sigma-event-logs-all.yml

# Hunt a single EVTX file
./chainsaw hunt Security.evtx -s rules/ -m mappings/sigma-event-logs-all.yml

# Hunt with specific Sigma rule file
./chainsaw hunt EVTX_DIR/ -s rules/windows/process_creation/proc_creation_win_psexec_execution.yml \
  -m mappings/sigma-event-logs-all.yml

# Hunt with output to JSON
./chainsaw hunt EVTX_DIR/ -s rules/ -m mappings/sigma-event-logs-all.yml \
  --output results.json --json

# Hunt with output to CSV
./chainsaw hunt EVTX_DIR/ -s rules/ -m mappings/sigma-event-logs-all.yml \
  --output results.csv --csv

# Hunt and show full event details (not just matching fields)
./chainsaw hunt EVTX_DIR/ -s rules/ -m mappings/sigma-event-logs-all.yml --full

# Hunt with timestamp range filter
./chainsaw hunt EVTX_DIR/ -s rules/ -m mappings/sigma-event-logs-all.yml \
  --from "2026-03-01 00:00:00" --to "2026-04-01 00:00:00"

# Hunt with minimum severity filter (informational, low, medium, high, critical)
./chainsaw hunt EVTX_DIR/ -s rules/ -m mappings/sigma-event-logs-all.yml \
  --level high

# Hunt with specific rule status (stable, test, experimental)
./chainsaw hunt EVTX_DIR/ -s rules/ -m mappings/sigma-event-logs-all.yml \
  --status stable

# Hunt and skip rule loading errors (useful with large mixed rule sets)
./chainsaw hunt EVTX_DIR/ -s rules/ -m mappings/sigma-event-logs-all.yml \
  --skip-errors

# Hunt with progress display
./chainsaw hunt EVTX_DIR/ -s rules/ -m mappings/sigma-event-logs-all.yml --progress

# Hunt multiple EVTX directories
./chainsaw hunt /mnt/evidence/C/Windows/System32/winevt/Logs/ \
  -s rules/ -m mappings/sigma-event-logs-all.yml --output hunt_results.json --json
```

### Search Mode

Search mode does keyword or field-level search across all events without requiring Sigma rules.

```bash
# Search for a keyword across all events
./chainsaw search "mimikatz" EVTX_DIR/

# Search in a specific EVTX file
./chainsaw search "powershell" Security.evtx

# Case-insensitive search
./chainsaw search -i "cobalt strike" EVTX_DIR/

# Search using a regex pattern
./chainsaw search -e "cmd\.exe.*\/c.*whoami" EVTX_DIR/

# Search for specific Event IDs
./chainsaw search --event-id 4624 Security.evtx
./chainsaw search --event-id 4688 Security.evtx    # Process creation
./chainsaw search --event-id 7045 System.evtx       # Service installation

# Search with timestamp filter
./chainsaw search "lateral" EVTX_DIR/ \
  --from "2026-03-15 00:00:00" --to "2026-03-16 23:59:59"

# Search and output to JSON
./chainsaw search "powershell" EVTX_DIR/ --output search_results.json --json

# Search with field-specific match (tau syntax)
./chainsaw search --tau "EventID: 4624 AND LogonType: 3" Security.evtx
```

### Dump Mode

Dump mode converts EVTX files to structured JSON or CSV for external analysis (Splunk, ELK, Excel).

```bash
# Dump all events from EVTX file to JSON
./chainsaw dump Security.evtx --json --output security_dump.json

# Dump to CSV
./chainsaw dump Security.evtx --csv --output security_dump.csv

# Dump multiple files
./chainsaw dump EVTX_DIR/ --json --output all_events.json

# Dump with timestamp range
./chainsaw dump Security.evtx --json \
  --from "2026-04-01 00:00:00" --to "2026-04-02 00:00:00" \
  --output incident_window.json

# Dump specific event IDs only
./chainsaw dump Security.evtx --json --event-id 4624 --output logon_events.json
```

### Analyse Mode

Pre-built analysis for specific forensic artifacts.

```bash
# Analyse shimcache (application execution evidence)
./chainsaw analyse shimcache SYSTEM --output shimcache.json --json

# Analyse amcache (installed programs and execution)
./chainsaw analyse amcache Amcache.hve --output amcache.json --json
```

## Key Detections and Event IDs

### Lateral Movement

| Event ID | Channel | Description | Sigma Rule Category |
|----------|---------|-------------|---------------------|
| 4624 | Security | Successful logon (Type 3 = Network, Type 10 = Remote Interactive) | lateral_movement |
| 4648 | Security | Logon with explicit credentials (Pass-the-Hash indicator) | credential_access |
| 7045 | System | New service installed (PsExec creates services) | lateral_movement |
| 4698 | Security | Scheduled task created | persistence |

### Credential Access

| Event ID | Channel | Description |
|----------|---------|-------------|
| 4661 | Security | SAM/LSA object access (credential dumping) |
| 4663 | Security | Object access — NTDS.dit, SAM hive access |
| 4769 | Security | Kerberos service ticket request (Kerberoasting: RC4 enc type) |
| 4768 | Security | Kerberos TGT request |
| 4771 | Security | Kerberos pre-auth failure (brute force) |

### Execution and PowerShell

| Event ID | Channel | Description |
|----------|---------|-------------|
| 4688 | Security | Process creation (requires audit policy) |
| 4104 | PowerShell | Script block logging — full PS command |
| 4103 | PowerShell | Module logging |
| 400/403 | PowerShell | Engine start/stop |

### Persistence

| Event ID | Channel | Description |
|----------|---------|-------------|
| 4698 | Security | Scheduled task created |
| 4702 | Security | Scheduled task updated |
| 7045 | System | New service registered |
| 4657 | Security | Registry value modified (Run keys, etc.) |

### Defense Evasion

| Event ID | Channel | Description |
|----------|---------|-------------|
| 1102 | Security | Audit log cleared |
| 104 | System | System log cleared |
| 4719 | Security | Audit policy changed |

## Incident Response Workflow

### Step 1 — Evidence Collection

```bash
# Collect all EVTX files from live or imaged Windows system
# Default location: C:\Windows\System32\winevt\Logs\
# Copy to analysis machine
```

### Step 2 — Initial Hunt (High Severity)

```bash
mkdir -p ir_results/

# Hunt for high/critical severity only — fast initial triage
./chainsaw hunt /evidence/Logs/ \
  -s rules/ -m mappings/sigma-event-logs-all.yml \
  --level high --json --output ir_results/high_sev_hits.json

# Review hits immediately
cat ir_results/high_sev_hits.json | jq '.[].name' | sort -u
```

### Step 3 — Targeted Event ID Search

```bash
# Build timeline of specific events
# Logon events
./chainsaw dump /evidence/Logs/Security.evtx --json --event-id 4624 \
  --output ir_results/logon_events.json

# Process creation
./chainsaw dump /evidence/Logs/Security.evtx --json --event-id 4688 \
  --output ir_results/process_creation.json

# PowerShell script blocks
./chainsaw dump /evidence/Logs/Microsoft-Windows-PowerShell%4Operational.evtx \
  --json --event-id 4104 --output ir_results/powershell_scriptblocks.json
```

### Step 4 — IOC Search

```bash
# Search for known IOCs
./chainsaw search -i "C2_domain.com" /evidence/Logs/ \
  --json --output ir_results/ioc_c2.json

./chainsaw search -e "(cobalt|cobaltstrike|beacon\.dll)" /evidence/Logs/ \
  --json --output ir_results/ioc_cobalt.json

./chainsaw search "net user" /evidence/Logs/ \
  --from "2026-04-01 00:00:00" --json --output ir_results/net_user_cmds.json
```

### Step 5 — Full Dump for Timeline

```bash
# Dump all events to JSON for import into timeline tool or SIEM
./chainsaw dump /evidence/Logs/ --json --output ir_results/full_evtx_dump.json

# Or CSV for Excel/timeline analysis
./chainsaw dump /evidence/Logs/ --csv --output ir_results/full_evtx_dump.csv
```

## Custom Detection Rules

Write Sigma rules targeting specific TTPs. Example — detecting PsExec service installation:

```yaml
# rules/custom/detect_psexec_service.yml
title: PsExec Service Installation
status: stable
description: Detects PSEXESVC service creation indicative of PsExec lateral movement
logsource:
  product: windows
  service: system
detection:
  selection:
    EventID: 7045
    ServiceName: 'PSEXESVC'
  condition: selection
falsepositives:
  - Legitimate PsExec use by administrators
level: high
tags:
  - attack.lateral_movement
  - attack.t1569.002
```

```bash
# Apply custom rule
./chainsaw hunt /evidence/Logs/System.evtx \
  -s rules/custom/detect_psexec_service.yml \
  -m mappings/sigma-event-logs-all.yml
```

## Integration with Other Tools

### With Velociraptor / KAPE Evidence Collections

```bash
# KAPE collects EVTX files into structured output dir
# Point chainsaw at KAPE's EVTX output
./chainsaw hunt KAPE_Output/C/Windows/System32/winevt/Logs/ \
  -s rules/ -m mappings/sigma-event-logs-all.yml \
  --json --output chainsaw_kape_results.json
```

### With Hayabusa (complementary tool)

Chainsaw focuses on Sigma rules; Hayabusa is another EVTX tool with its own rule format.
Run both for maximum detection coverage, then merge JSON outputs for timeline analysis.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `No events found` | EVTX path wrong | Verify path; check `ls EVTX_DIR/*.evtx` |
| `Rule parse error` | Incompatible Sigma rule version | Use `--skip-errors` flag |
| `Mapping file not found` | Missing `-m` flag | Always specify `-m mappings/sigma-event-logs-all.yml` |
| Very slow hunt | Large EVTX set, many rules | Filter by `--level high`, use `--from`/`--to` |
| Empty JSON output | No matches | Normal; reduce `--level` threshold, check rule coverage |
| Permission denied on EVTX | Locked by OS | Copy EVTX files off live system with VSS shadow copy |
| Binary not found on Windows | Missing VC++ runtime | Install Microsoft Visual C++ Redistributable |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Your Company Just Got Hit with Ransomware: A 48-Hour Survival Playbook for SMBs](https://redhound.us/ransomware-playbook)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
