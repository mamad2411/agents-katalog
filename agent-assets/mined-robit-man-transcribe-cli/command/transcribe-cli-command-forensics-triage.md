---
name: forensics-triage
description: Quick triage investigation following RFC 3227 volatility order
agent: triage-agent
category: forensics-triage
argument-hint: "<target> [--output path] [--scope network|process|all]"
---

# /forensics-triage

Perform rapid triage of a potentially compromised system by capturing volatile data in order of volatility per RFC 3227. Identifies active threats, running malicious processes, suspicious network connections, and immediate red flags within minutes of invocation.

## Usage

`/forensics-triage <target> [options]`

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| target | Yes | SSH connection string (`ssh://user@host:port`) |
| --output | No | Output directory (default: `.aiwg/forensics/findings/<hostname>-<date>/`) |
| --scope | No | Triage scope: `network`, `process`, `filesystem`, or `all` (default: `all`) |
| --fast | No | Skip slower checks; capture critical volatile data only |
| --no-hash | No | Skip file hashing for speed (not recommended for evidence) |

## Behavior

When invoked, this command:

1. **Establish Baseline Connection**
   - Connect to target via SSH
   - Record exact timestamp (UTC) of triage start
   - Note investigator identity and tool version
   - Capture system clock drift vs. investigator clock

2. **Volatile Data Capture (RFC 3227 Order)**
   - CPU registers and running state (process list snapshot)
   - Network connections and ARP cache
   - Login sessions and active users
   - Contents of memory (process memory maps)
   - Temporary file system state (`/tmp`, `/dev/shm`)
   - Swap space indicators
   - Disk mount state

3. **Red Flag Detection**
   - Processes with deleted binaries (`/proc/*/exe` pointing to deleted files)
   - Processes listening on unexpected ports
   - Base64 or encoded strings in process command lines
   - World-writable files recently modified
   - Unexpected cron entries or scheduled tasks
   - Suspicious SUID/SGID binaries
   - Outbound connections to non-RFC-1918 addresses

4. **Network Snapshot**
   - All established and listening connections with PIDs
   - ARP table for lateral movement indicators
   - DNS cache contents
   - Routing table anomalies
   - Active traffic rates per interface

5. **Process Inventory**
   - Full process tree with parent-child relationships
   - Processes running from unusual locations (`/tmp`, `/dev/shm`, hidden dirs)
   - Processes with suspicious names or masquerading as system processes
   - CPU/memory outliers suggesting crypto mining or exfiltration
   - Open file handles for suspicious processes

6. **Quick Assessment and Scoring**
   - Assign threat score (0-100) based on red flags found
   - Classify finding severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)
   - Determine recommended next steps
   - Flag whether live response escalation is needed

7. **Save Triage Artifacts**
   - Write `triage-summary.md` with findings and threat score
   - Save raw volatile data captures to `volatile/`
   - Record chain-of-custody entry with hashes
   - Update investigation state file

## Examples

### Example 1: Standard triage
```bash
/forensics-triage ssh://admin@192.168.1.50
```

### Example 2: Network-focused triage
```bash
/forensics-triage ssh://admin@192.168.1.50 --scope network
```

### Example 3: Fast capture (critical data only)
```bash
/forensics-triage ssh://root@10.0.0.5 --fast
```

### Example 4: Custom output directory
```bash
/forensics-triage ssh://admin@host --output .aiwg/forensics/incident-2026-02-27/
```

## Output

Artifacts are saved to `.aiwg/forensics/findings/<hostname>-<date>/`:

```
.aiwg/forensics/findings/web01-2026-02-27/
├── triage-summary.md         # Threat assessment and findings
├── volatile/
│   ├── process-list.txt      # Running processes at capture time
│   ├── network-connections.txt
│   ├── arp-cache.txt
│   ├── login-sessions.txt
│   ├── open-files.txt
│   └── memory-maps.txt
├── chain-of-custody.yaml     # Evidence integrity log
└── checksums.sha256
```

### Sample Output

```
Triaging Target: 192.168.1.50
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Triage started: 2026-02-27T14:32:01Z
Clock drift: +0.3s

Step 1: Capturing volatile data (RFC 3227 order)
  Process list: 187 processes captured
  Network connections: 42 connections captured
  ARP cache: 8 entries captured
  Login sessions: 3 active sessions
  Open files: 1,847 handles captured

Step 2: Red flag detection
  [CRITICAL] Process 'kworker' running from /tmp/kworker (deleted binary)
  [HIGH] Outbound connection to 185.220.101.42:4444 (known C2 range)
  [HIGH] Base64 in process args: PID 3847 (/bin/bash -c 'echo <b64>...')
  [MEDIUM] Unusual SUID binary: /usr/local/bin/.hidden (modified 2h ago)
  [MEDIUM] Cron entry added 4h ago: * * * * * /tmp/.update

Step 3: Network snapshot
  Established: 42 connections
  Suspicious outbound: 2 connections to non-RFC-1918
  DNS anomaly: None detected

Step 4: Process assessment
  Suspicious processes: 3
  Crypto mining indicators: None
  Masquerading processes: 1 ('kworker' from /tmp)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Threat Score: 87/100 (CRITICAL)

IMMEDIATE ACTION REQUIRED
Active compromise indicators detected.

Next Steps:
  /forensics-acquire ssh://admin@192.168.1.50 --logs --memory
  /forensics-investigate ssh://admin@192.168.1.50 --scope full
```

## References

- @agentic/code/frameworks/forensics-complete/agents/triage-agent.md - Triage Agent
- @agentic/code/frameworks/forensics-complete/templates/triage-report.md - Report template
- @agentic/code/frameworks/forensics-complete/commands/forensics-acquire.md - Evidence acquisition
- @agentic/code/frameworks/forensics-complete/commands/forensics-investigate.md - Full investigation
