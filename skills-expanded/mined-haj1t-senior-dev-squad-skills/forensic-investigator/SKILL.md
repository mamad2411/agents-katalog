---
name: forensic-investigator
description: "DFIR — memory dumps, log analysis, timeline mapping, root cause analysis. Use when investigating incidents or performing forensic post-mortems."
---

# Forensic Investigator

## Overview

This skill is used within development environments to analyze security incidents, trace attacker footprints, and interpret digital evidence. It extracts security indicators from memory dumps (crash dumps, heap dumps), scans application/audit/access logs for anomalous behavior, constructs unified event timelines from multiple data sources, and identifies the root cause of an attack vector from initial compromise to ultimate impact. The goal is to answer: "What happened, how did it happen, what was the blast radius, and how do we prevent a recurrence?"

**Core principle:** No forensics can occur without evidence integrity. Any step that compromises the chain of custody invalidates the findings legally and technically.

## The Iron Law

```
NO FORENSIC FINDING CAN BE REPORTED WITHOUT FULLY DOCUMENTING THE CHAIN OF CUSTODY AND VERIFYING EVIDENCE INTEGRITY.
```

If the chain of custody is broken, the entire analysis report will be rejected during audits, legal proceedings, or post-mortem reviews.

## When to Use

**Use this when:**
- A security incident is detected, and you need to determine its scope.
- An application crash dump or heap dump is captured, and you need to check for indicators of compromise (IoCs).
- Anomalous access patterns are detected in access, audit, or system logs.
- You need to build a unified event timeline from multiple sources (logs, network captures, filesystem changes).
- You need to map out the entire lifecycle of an attack from the initial entry vector to the final impact.
- You are writing a root cause analysis report for a post-mortem review.

**Use this ESPECIALLY when:**
- An unexplained data leak or privilege escalation occurs on a production system — systematic analysis is required rather than panic actions.
- The team asserts "this was just a bug, not an exploit" — forensics can isolate the truth.
- You need to harvest and verify historical incident evidence before audits or legal audits.

**Don't skip when:**
- The system has already been completely wiped or redeployed with no backups — you cannot extract evidence from non-existent data.
- You are only performing standard live application debugging without any security implications.

## Phase 1: Evidence Harvesting and Chain of Custody

**BEFORE proceeding:**

Clarify the incident type (unauthorized access, exfiltration, RCE, DoS) and isolate affected systems. Notify response stakeholders.

1. **Identify evidence sources** — Memory dumps, log files, filesystem images, network packet captures (pcap), process trees, active network sockets.
2. **Harvest in order of volatility** — Volatile memory > process trees > network sockets > disks > log files.
3. **Perform hash verification** — Compute the SHA-256 hash of every harvested evidence file immediately and store it in a secure location.
4. **Document the Chain of Custody** — Record who collected the evidence, at what time, from which system, and for what purpose.

```bash
# Hash verification of a memory dump
sha256sum memory_dump.raw > memory_dump.raw.sha256

# Digital signature of a log file
gpg --detach-sign --armor auth.log
```

## Phase 2: Memory Dump Analysis

**BEFORE proceeding:**

Ensure the target system was not powered down before extracting memory. Memory is volatile unless captured before rebooting or cold boot attacks.

1. **Identify the OS profile** using Volatility to match the target kernel.
2. **Extract the process list** (`pslist`, `psscan`) — flag anomalous or hidden processes.
3. **Audit network sockets** (`netscan`) — log connections going to unlisted IPs.
4. **Scan for DLL/Module injection** (`ldrmodules`, `malfind`) — locate hidden or encrypted memory sections.
5. **Inspect CLI command history** (`cmdscan`, `consoles`) — recover executed command strings.
6. **Analyze heap dumps** (Java/.NET) — search memory pools for plain-text credentials or API secrets.

```python
# Example: Identifying suspicious processes with Volatility
# volatility -f memory.dump --profile=Win10x64 pslist
suspicious_processes = [
    {"pid": 4521, "name": "svch0st.exe", "parent": "services.exe"},  # Typo squatting
    {"pid": 6723, "name": "powershell.exe", "parent": "winword.exe"},  # Word macro spawning execution
    {"pid": 8891, "name": "rundll32.exe", "parent": "outlook.exe"},  # Outlook OLE execution
]

heap_strings = {
    "file": "heap_dump_java.bin",
    "secrets_found": ["AKIA...", "password=..."],
    "risk": "HIGH - Secrets leak confirmed in memory"
}
```

## Phase 3: Log Audits and Anomaly Patterns

**BEFORE proceeding:**

Collect all log files (application logs, audit logs, access logs, syslog, cloud trails) and centralize them.

1. **Establish the timeline window** — Retrieve log entries going back at least 72 hours prior to the detection of the incident.
2. **Scan for brute-force signatures** — Multiple failed logins followed by a single success; credential stuffing signatures.
3. **Locate off-hours or geographic anomalies** — Access logs showing logins during atypical hours or from unexpected geographic locations.
4. **Audit for IDOR and privilege escalation patterns** — Logs showing a user account accessing records outside their authorization scope.
5. **Identify injection payloads** — Check parameters for SQL injection, XSS, or command injection strings.
6. **Examine exfiltration signatures** — Unusually high Content-Length values in responses or frequent connections to external endpoints.

```python
# Regex log signature matching examples
log_patterns = {
    "brute_force": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.*401.*",
    "off_hours": r"(0[0-2]|2[0-3]):[0-5][0-9]:[0-5][0-9]",
    "suspicious_user_agent": r"(curl|python-requests|Go-http-client|wget).*(POST|PUT)",
    "large_response": r".*Content-Length: [5-9]\d{5,}",  # 500KB+
}

findings = {
    "brute_force_attempts": 1523,
    "successful_after_brute": 1,
    "off_hours_access": 47,
    "suspicious_data_exports": 3,
    "source_ips": ["185.220.101.x", "91.121.87.x"]
}
```

## Phase 4: Constructing a Unified Timeline

**BEFORE proceeding:**

Verify all memory dump analyses and log audits are complete, with findings tagged.

1. **Aggregate timestamps** from logs, file modifications, network connections, and process start/stop events.
2. **Sort chronologically** from the earliest recorded event to the latest.
3. **Map findings to the attack kill chain:**
   - Reconnaissance: Port scanning, endpoint fuzzing.
   - Initial Access: Vulnerability exploit, compromised credentials.
   - Execution: Malicious payload execution.
   - Persistence: Backdoors, cron jobs, scheduled tasks.
   - Lateral Movement: Spawning connections to adjacent systems.
   - Exfiltration: Exfiltrating compressed data.
4. **Highlight logging gaps** — Note time periods with missing log records.

```
INCIDENT TIMELINE
=======================================
Timestamp              Event                           Source
---------------------------------------------------
2026-05-17 03:12:45    Port scan detected (22, 443)    firewall.log
2026-05-17 03:14:02    HTTP 200 /wp-admin              access.log
2026-05-17 03:14:30    POST /wp-login.php (Failed x47) access.log
2026-05-17 03:17:12    POST /wp-login.php (SUCCESS)    access.log
2026-05-17 03:18:44    wp-admin plugin upload          access.log
2026-05-17 03:20:01    webshell.php written to disk    file_audit.log
2026-05-17 03:25:33    curl request to 185.220.101.x   process.log
2026-05-17 04:12:00    PostgreSQL dump executed        db_audit.log
2026-05-17 04:45:00    Data compression utility run    process.log
2026-05-17 04:47:00    SCP egress transfer to remote   firewall.log
---------------------------------------------------
INITIAL ENTRY: 03:17:12 — EGRESS: 04:47:00 (Duration: 94 min)
```

## Phase 5: Root Cause Analysis and Remediation

**BEFORE proceeding:**

Ensure the timeline is fully populated and events are mapped to the kill chain.

1. **Isolate the entry vector** — Vulnerability, compromised credential, insider threat, or supply chain attack.
2. **Define the impact** — Compromised data records, host compromise, data integrity status.
3. **List containment actions** — Network segmentation, patches, MFA enforcement, principal of least privilege.
4. **Propose remediations** — Short-term (24 hours), medium-term (1 week), long-term (1 month).
5. **Finalize the incident report** with summaries for both management and technical stakeholders.

## Final Verification Check:

- [ ] Are all evidence files cataloged with SHA-256 hashes?
- [ ] Is the Chain of Custody log complete?
- [ ] Has the memory dump been analyzed with Volatility or equivalent tools?
- [ ] Does log analysis cover the 72-hour period pre-compromise?
- [ ] Are any log gaps documented?
- [ ] Is the initial entry vector (root cause) identified?
- [ ] Are events mapped to the attack kill chain?
- [ ] Does the report contain a non-technical executive summary?
- [ ] Are remediation suggestions assigned to owners with priorities?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "This log is old, let's skip it and focus on recent events" — **Old logs often contain the initial reconnaissance phase; verify back 72 hours.**
- "I'll compute the SHA-256 hashes later when I compile the report" — **Modifying files post-acquisition without baseline hashes invalidates the evidence.**
- "The memory dump has no findings, so no exploit occurred" — **Exploits can scrub memory or deploy kernel-level rootkits; check for anti-forensic patterns.**
- "We only need the application logs, syslog is unnecessary" — **Attackers hide their footprints by deleting application files; audit all system logs.**
- "This source IP belongs to a trusted CDN, it is not malicious" — **Attackers route their egress traffic through trusted CDNs; audit geographic and payload behaviors.**

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Did you verify the hash of this log file?" — You skipped validating evidence hashes.
- "Where is the Chain of Custody document?" — You failed to log evidence transfers.
- "Did you map the attacker's kill chain?" — Your timeline is missing phases.
- "Is there an alternative explanation for this log signature?" — You jumped to conclusions without testing other possibilities.
- "The remediation plan is too vague; what code needs to be modified?" — Make suggestions actionable.
- "What was the window of compromise?" — Define the timeline limits clearly.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Hashing is just double work." | Hashing is the only way to prove evidence integrity. Without it, logs are dismissed as untrusted. |
| "A memory dump is too large to scan; logs are sufficient." | Memory contains volatile runtime parameters (e.g., active sockets, keys) that logs cannot capture. |
| "We couldn't find anomalies, so no breach occurred." | Attackers can scrub logs; a gap in log entries is itself a critical finding. |
| "Writing a timeline is too time-consuming." | Without a chronological timeline, you cannot identify how the entry vector relates to egress. |
| "We shut down the host, so the threat is contained." | Shutting down the host clears memory, destroying volatile evidence. Analyze before shutdown. |

## Related Skills

- **purple-team-analyzer** — Simulate the incident workflow to test detection capabilities.
- **mitre-attack-mapper** — Map timeline events to MITRE ATT&CK techniques.
- **nist-csf-scanner** — Connect root causes to NIST CSF gaps.

## Self-Review

After completing this process:

1. **Integrity Audit:** Do all collected evidence records have verifiable hashes?
2. **Kill Chain Balance:** Are all phases of the attack represented in the timeline?
3. **Actionability Check:** Does the remediation roadmap provide line-level code suggestions?
4. **Iron Law Audit:** Has the Chain of Custody been documented and evidence integrity verified?
