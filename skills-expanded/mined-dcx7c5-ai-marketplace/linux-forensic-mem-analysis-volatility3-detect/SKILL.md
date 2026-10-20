---
name: linux-forensic-mem-analysis-volatility3-detect
description: "6. Heavy root usage expected — always verify `AgentRootPermission` before /proc/mem access 7."
domain: cybersecurity
---

## Rules for Agents

1. RWX anonymous mappings = **HIGH** — dump region and pass to @reverse-engineer
2. DKOM-hidden processes confirmed = **CRITICAL** — escalate immediately
3. Credentials found in memory = **HIGH** — redact values, log type and PID only in `iocs.md`
4. Suspicious eBPF programs = **HIGH** — dump and analyse bytecode
5. Always pair with @kernel-analyst for kernel-level confirmation
6. Heavy root usage expected — always verify `AgentRootPermission` before /proc/mem access
7. Sync all memory IOCs to shared memory at session end
