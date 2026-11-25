---
name: system-monitor
description: Inspect system telemetry and summarize CPU, memory, disk, process, and network anomalies.
category: utilities
aliases:
- system
- monitor
- telemetry
- metrics
- performance
triggers:
- Check system status
- System health
- Server metrics
- CPU usage
- Memory check
keywords:
- system
- monitor
- cpu
- memory
- disk
- network
- metrics
- telemetry
dependencies:
- optional:system-tools
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- system-monitor
- utilities
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- cpu
- memory
- monitor
- system
- utilities
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# System Monitor

## Purpose
Inspect system telemetry and provide clear summaries of CPU usage, memory allocation,
disk space, running processes, and network activity. The skill highlights anomalies
and helps diagnose performance issues.

## When to Use
- Checking system health and resource usage
- Diagnosing performance problems
- Monitoring server or workstation status
- Investigating resource bottlenecks

## When NOT to Use
- Real-time continuous monitoring (use dedicated monitoring tools)
- Accessing systems without authorization
- Automated remediation without human approval

## Capabilities
- CPU usage and load average
- Memory utilization and swap
- Disk space and I/O statistics
- Running processes (top consumers)
- Network connections and throughput
- Temperature and hardware sensors (where available)
- Anomaly detection and alerting
- Historical trend analysis (if data available)

## Inputs
- `target` (optional) — system hostname or local (default: local)
- `scope` (optional) — all, cpu, memory, disk, network, processes
- `timeframe` (optional) — current, last-hour, last-day
- `alert_threshold` (optional) — custom alert levels

## Workflow
1. **Connect** — Establish access to target system
2. **Collect** — Gather telemetry data
3. **Analyze** — Compare against baselines, detect anomalies
4. **Summarize** — Present findings in clear format
5. **Alert** — Flag any critical issues
6. **Recommend** — Suggest investigation steps if needed

## Tools
- System utilities (top, htop, ps, df, netstat, etc.)
- Platform-specific tools (Windows Task Manager equivalent, Linux sysstat)

## Examples
**User:** "Check system health"
**Response:**
```
System Status: Healthy

CPU: 34% utilized (normal)
Memory: 67% used, 4.2GB available
Disk: 45% used (120GB / 256GB)
  - /home: 78% (warning)
  - /var: 52%
Network: Normal activity

Anomalies:
âš ï¸ /home partition above 75% threshold
âœ“ No other issues detected
```

## Safety
- Only access systems with proper authorization
- Never store sensitive system data beyond the session
- Use read-only commands by default
- Confirm before any system modifications

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical utilities category.
