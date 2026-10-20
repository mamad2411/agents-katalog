---
name: forensics-investigate
description: Full multi-agent investigation workflow
agent: forensics-orchestrator
category: forensics-investigation
argument-hint: "<target> [--scope triage|full|targeted-ssh|container|cloud] [--skip-stage stage]"
---

# /forensics-investigate

Orchestrate a complete digital forensics investigation by coordinating all specialized agents through the full workflow: reconnaissance, triage, acquisition, multi-domain analysis, timeline building, IOC extraction, and report generation. Suitable for incident response and proactive threat hunting.

## Usage

`/forensics-investigate <target> [options]`

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| target | Yes | SSH connection string, cloud target, or findings directory path |
| --scope | No | Investigation scope: `triage`, `full`, `targeted-ssh`, `container`, `cloud` (default: `full`) |
| --skip-stage | No | Skip a specific stage: `recon`, `triage`, `acquire`, `analysis`, `timeline`, `ioc`, `report` |
| --resume | No | Resume a previously interrupted investigation from last checkpoint |
| --output | No | Output directory (default: `.aiwg/forensics/`) |
| --parallel | No | Run analysis agents in parallel where possible (default: true) |
| --notify | No | Webhook URL for stage completion notifications |

## Behavior

When invoked, this command:

1. **Initialize Investigation**
   - Create investigation workspace at `.aiwg/forensics/`
   - Assign investigation ID (`INV-<date>-<host>`)
   - Record start time, investigator, and scope
   - Check for existing investigation to resume

2. **Reconnaissance (recon-agent)**
   - Profile target system and establish baseline
   - Document services, users, and network configuration
   - Save to `profiles/<hostname>/`

3. **Triage (triage-agent)**
   - Capture volatile data per RFC 3227 order
   - Score initial threat level
   - Identify active indicators requiring immediate attention
   - Save to `findings/<hostname>/volatile/`

4. **Acquisition (acquisition-agent)**
   - Collect logs, configurations, and artifacts per triage findings
   - Establish chain of custody for all evidence
   - Compute and verify SHA-256 hashes
   - Save evidence manifest to `acquisition/`

5. **Analysis (parallel agent coordination)**
   - **Log Analyst**: Auth logs, syslog, journal entries
   - **Persistence Hunter**: Crons, systemd units, SSH keys, rootkits
   - **Network Analyst**: Connections, DNS, beaconing, lateral movement
   - **Container Analyst**: Docker/Kubernetes artifacts (if applicable)
   - **Memory Analyst**: Volatility 3 analysis (if memory image available)
   - **Cloud Analyst**: CloudTrail, IAM, flow logs (if cloud target)
   - Save findings to `analysis/<agent>/`

6. **Timeline Building (timeline-builder)**
   - Correlate events across all analysis findings
   - Normalize timestamps to UTC
   - Reconstruct attack chain with MITRE ATT&CK mapping
   - Save to `timeline/incident-timeline.md`

7. **IOC Extraction (ioc-analyst)**
   - Extract indicators from all findings
   - Enrich with threat intelligence
   - Map to STIX 2.1 observables
   - Save to `ioc/ioc-register.md`

8. **Report Generation (reporting-agent)**
   - Compile executive summary and technical findings
   - Include severity-classified evidence table
   - Generate remediation plan with prioritized actions
   - Save to `reports/forensic-report.md`

9. **Quality Gate**
   - Verify all stages completed or explicitly skipped
   - Confirm evidence chain of custody integrity
   - Check report completeness before marking investigation closed

## Scope Profiles

| Scope | Stages | Use Case |
|-------|--------|----------|
| `triage` | recon, triage | Initial rapid assessment |
| `targeted-ssh` | recon, triage, acquire, logs, persistence, network | SSH-compromised host |
| `container` | recon, triage, acquire, container, network | Container escape or image compromise |
| `cloud` | recon, acquire, cloud, ioc, report | Cloud account breach |
| `full` | All stages | Comprehensive incident response |

## Examples

### Example 1: Full investigation
```bash
/forensics-investigate ssh://admin@192.168.1.50 --scope full
```

### Example 2: Quick triage only
```bash
/forensics-investigate ssh://admin@192.168.1.50 --scope triage
```

### Example 3: Container sweep
```bash
/forensics-investigate ssh://root@docker-host --scope container
```

### Example 4: Cloud audit
```bash
/forensics-investigate aws://123456789012/us-east-1 --scope cloud
```

### Example 5: Resume interrupted investigation
```bash
/forensics-investigate ssh://admin@192.168.1.50 --resume
```

### Example 6: Skip memory analysis
```bash
/forensics-investigate ssh://admin@host --scope full --skip-stage memory
```

## Output

All artifacts are saved under `.aiwg/forensics/`:

```
.aiwg/forensics/
├── investigation.yaml             # Investigation metadata and state
├── profiles/
│   └── web01-2026-02-27/
│       └── system-profile.md
├── findings/
│   └── web01-2026-02-27/
│       ├── triage-summary.md
│       └── volatile/
├── acquisition/
│   ├── evidence-manifest.yaml
│   └── custody-log.yaml
├── analysis/
│   ├── logs/
│   ├── persistence/
│   ├── network/
│   └── ioc/
├── timeline/
│   └── incident-timeline.md
├── ioc/
│   └── ioc-register.md
└── reports/
    └── forensic-report.md
```

### Sample Progress Output

```
Investigation: INV-2026-02-27-web01
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[14:30:00] Stage 1/8: Reconnaissance     RUNNING
[14:31:42] Stage 1/8: Reconnaissance     COMPLETE  (102s)
[14:31:42] Stage 2/8: Triage             RUNNING
[14:34:15] Stage 2/8: Triage             COMPLETE  (153s) [CRITICAL - active compromise]
[14:34:15] Stage 3/8: Acquisition        RUNNING
[14:39:02] Stage 3/8: Acquisition        COMPLETE  (287s) [14 artifacts collected]
[14:39:02] Stage 4/8: Analysis           RUNNING   (parallel: 5 agents)
[14:39:02]   Log Analyst                 RUNNING
[14:39:02]   Persistence Hunter          RUNNING
[14:39:02]   Network Analyst             RUNNING
[14:52:18]   Log Analyst                 COMPLETE  [8 findings]
[14:53:41]   Persistence Hunter          COMPLETE  [3 findings]
[14:55:09]   Network Analyst             COMPLETE  [5 findings]
[14:55:09] Stage 4/8: Analysis           COMPLETE  (976s) [16 total findings]
[14:55:09] Stage 5/8: Timeline           RUNNING
[14:57:33] Stage 5/8: Timeline           COMPLETE  (144s)
[14:57:33] Stage 6/8: IOC Extraction     RUNNING
[14:59:01] Stage 6/8: IOC Extraction     COMPLETE  (88s)  [12 IOCs extracted]
[14:59:01] Stage 7/8: Report Generation  RUNNING
[15:01:44] Stage 7/8: Report Generation  COMPLETE  (163s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Investigation Complete: INV-2026-02-27-web01
Duration: 31m 44s

Findings: 16 total (2 CRITICAL, 5 HIGH, 6 MEDIUM, 3 LOW)
IOCs: 12 extracted (4 enriched with threat intel)
Report: .aiwg/forensics/reports/forensic-report.md
```

## References

- @agentic/code/frameworks/forensics-complete/agents/forensics-orchestrator.md - Orchestrator
- @agentic/code/frameworks/forensics-complete/agents/manifest.json - All agent definitions
- @agentic/code/frameworks/forensics-complete/commands/forensics-report.md - Report generation
- @agentic/code/frameworks/forensics-complete/commands/forensics-status.md - Status monitoring
