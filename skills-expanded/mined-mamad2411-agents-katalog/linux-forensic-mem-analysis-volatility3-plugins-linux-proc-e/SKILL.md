---
name: linux-forensic-mem-analysis-volatility3-plugins-linux-proc-exploit
description: "6. Cross-validate with @kernel-analyst for DKOM/eBPF hiding techniques 7."
domain: cybersecurity
---

## Rules for Agents

1. ANY process running from a deleted binary = **HIGH** — escalate immediately
2. /etc/ld.so.preload exists = **CRITICAL** rootkit indicator
3. RWX anonymous mappings = **HIGH** — dump and analyse with @memory-analyst
4. PID gaps (hidden process) = **CRITICAL** — run `unhide` and escalate
5. Log all anomalous PIDs with cmdline, PPID, user, and binary path to `iocs.md`
6. Cross-validate with @kernel-analyst for DKOM/eBPF hiding techniques
7. Sync all process IOCs to shared memory at session end
