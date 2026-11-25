---
name: forensic-memory
description: Memory forensics workflow — hash-first RAM dump analysis, process enumeration, injection detection, artifact extraction, and timeline reconstruction with offline-only discipline.
disable-model-invocation: true
risk: passive
allowed-modes: [forensic, blue-team]
authorization-required: conditional
evidence-outputs: [evidence-hash, process-list, injection-notes, timeline-entries, redacted-evidence]
---

# Memory forensics — RAM dump analysis with chain-of-custody

Use this skill to analyze captured RAM images with hash-first evidence handling, offline-only parsing, and chain-of-custody discipline. Work exclusively on copies of evidence images. Never execute binaries extracted from memory, contact live hosts referenced in memory artifacts, or expose credentials found in process memory beyond redacted metadata.

## Required inputs

- Memory image file path confirmed readable, with SHA-256 hash recorded before any analysis step.
- Working directory for output under `.pi/pentest-agent/` with write access.
- Confirmation that the image is a copy — original evidence is preserved unmodified.
- Scope defining which hosts, time windows, and artifact types are in scope. Memory images from out-of-scope systems must not be analyzed.
- Current authorization cache if image contents could reveal data from live systems or third parties; otherwise authorization is conditional on image origin.
- Volatility3 or equivalent memory analysis framework confirmed available (detect only — never auto-install).

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` when image origin or target systems are scoped.
3. `pentest_agent_validate_target` before any analysis that could identify live system details.
4. `pentest_agent_check_authorization` before any analysis step that touches potentially sensitive memory contents.
5. `pentest_agent_build_command` for dry-run argv preview before every tool invocation.
6. `pentest_agent_execute_tool` for read-only analysis execution — never raw shell.
7. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — image identification and integrity

1. Record the image file hash (SHA-256) before any analysis. Log the hashing algorithm, timestamp, analyst identifier, and source path.
2. Identify the operating system, kernel version, and architecture from the image header or banner plugins. Do not assume the OS — validate with tool output.
3. Record the image size, acquisition method (if known), and any acquisition artifacts (smear, truncated regions, compression).
4. Create a working copy of the image if not already on a copy. Never run analysis plugins against the original evidence file.
5. Establish the output directory structure under `.pi/pentest-agent/engagement/<id>/forensics/memory/` with subdirectories for analysis output, extracted artifacts, and chain-of-custody notes.

### Phase 2 — process enumeration and anomaly detection

1. Enumerate all processes from the image: process tree (parent-child relationships), process list (all visible), and process scan (including terminated and hidden processes).
2. Compare the process list against the process scan output. Processes present in the scan but absent from the list may indicate hidden or unlinked processes — flag as suspicious.
3. For each process, record: PID, PPID, process name, executable path, start time, exit time (if terminated), and whether the process is in the process list, scan only, or both.
4. Flag processes with: no associated executable file on disk, executable path in temporary or user-writable directories, hollowed parent-child relationships (different executable names between parent and child where the child should match), or suspicious command-line arguments (base64-encoded, obfuscated, or referencing network shares).
5. Do not dump process memory yet — complete the process inventory first.

### Phase 3 — network artifact extraction

1. Extract all network connection artifacts: active connections, listening sockets, and recently closed connections.
2. For each connection, record: protocol (TCP/UDP), local address and port, remote address and port, connection state, owning process PID, and timestamp if available.
3. Flag connections to: known-bad IPs or domains (check against local threat-intel only — no external lookup without explicit approval), non-standard ports for common protocols (HTTP on port 4444, SSH on port 80), connections with no associated process (kernel-level rootkit indicator), and outbound connections to countries or ASNs outside the expected business range.
4. Extract DNS cache entries if available. Flag: unusually long domain names (potential DNS tunneling), recently resolved domains, and domains with low Time-To-Live values.
5. Redact any discovered credentials, session tokens, or authentication headers from connection metadata — record only their presence and type.

### Phase 4 — code injection and malware detection

1. Scan for injected code regions: detect memory regions with RWX permissions, regions mapped from no associated file, and regions with suspicious instruction patterns.
2. For each flagged region, record: process PID and name, memory address range, permissions, whether the region maps to a file, and the detection reason.
3. Enumerate loaded DLLs/shared libraries per process. Flag DLLs loaded from: temporary directories, user-writable paths, network shares, or paths that differ from the expected system library path.
4. Do not execute or disassemble injected code — record detection metadata only. The binary analysis should be handed off to the reverse-engineering workflow.
5. Hash any extracted memory regions or dumped process images before further analysis.

### Phase 5 — artifact extraction and credential hygiene

1. Extract command-line history across all processes. Record the full command line per process with timestamps where available.
2. Extract cached credential hashes if present. Record the hash type (NTLM, LM, Kerberos ticket), the associated account name (if available), and the source (LSASS, registry, SAM). Never store the raw hash in reports — replace with a redacted prefix and hash type.
3. Extract clipboard contents, browser history artifacts, and recently opened file lists if relevant to the investigation scope.
4. For every extracted artifact: hash it before writing to the output directory, log the extraction tool, timestamp, source process/offset, and hash algorithm.
5. Review extracted artifacts for PII, credentials, tokens, and internal hostnames. Redact before writing to evidence store.

## Decision points

- **Escalate on hidden or unlinked processes**: processes found in scan but absent from the process list are a strong indicator of rootkit or advanced malware activity.
- **Escalate on RWX memory regions in non-browser processes**: executable memory allocated without a backing file in system or security processes suggests code injection.
- **Escalate on C2-like network patterns**: regular-interval outbound connections, connections to known-malicious infrastructure, or long-running sessions on non-standard ports.
- **Escalate on credential-harvesting artifacts**: hashdump output, Kerberos ticket extraction, or clipboard contents containing passwords.
- **Downgrade on process anomalies with benign explanations**: admin tools (PsExec, PowerShell remoting), vulnerability scanner processes, or EDR components may appear suspicious but have documented legitimate use.

## Prohibited behavior

- Executing binaries or DLLs extracted from memory images on any host.
- Contacting network addresses found in memory artifacts (IPs, domains, URLs) for live verification.
- Extracting and storing raw credential material (password hashes, Kerberos tickets, session tokens) in evidence — record metadata (type, account, source) only.
- Modifying the original memory image or working on the original instead of a copy.
- Running memory acquisition tools against live systems — this skill is for offline image analysis only.
- Exporting memory artifacts outside `.pi/pentest-agent/`.

## Stop conditions

- Image hash cannot be verified or the image appears tampered → stop, record integrity concern.
- Analysis requires contacting a live system referenced in memory → stop, do not probe.
- Credential material found → stop extraction, record metadata (type, source process), redact values.
- Evidence includes PII, internal hostnames, or customer data → redact and stop the current extraction phase.
- Memory image appears to contain classified, privileged, or legally-protected data beyond the investigation scope → stop, escalate to legal/incident response.

## Evidence — memory forensics matrix

For each memory image analyzed, record:

```text
Image: <filename> | SHA-256: <hash>
OS: <Windows 10 build 19045 | Ubuntu 22.04 LTS | macOS 14.3>
Acquisition method: <live dump via winpmem | VM snapshot | hibernation file>

Process inventory:
  Total processes: <count>
  Hidden/unlinked: <count and PIDs>
  Suspicious command lines: <count — e.g., base64-encoded, obfuscated>
  Processes from writable paths: <count and paths>

Network artifacts:
  Active connections: <count>
  Listening sockets: <count — flag any on 0.0.0.0/0:port>
  Suspicious destinations: <count — known-bad, non-standard ports, anomalous geolocation>
  DNS anomalies: <count — long domains, low TTL, recently resolved>

Injection indicators:
  RWX memory regions: <count>
  Mismatched DLL paths: <count — user-writable or temporary paths>
  Hollowed processes: <count and PIDs>

Credential exposure:
  Hashdump present: <yes | no>
  Kerberos tickets extracted: <count>
  Cleartext credentials in clipboard/command line: <yes | no — redacted>

Timeline coverage:
  Earliest timestamp: <ISO 8601>
  Latest timestamp: <ISO 8601>
  Notable time gaps: <description>
```

Never store: raw password hashes, Kerberos ticket material, cleartext credentials, session tokens, full memory dumps of sensitive processes in evidence, unredacted browser history URLs containing tokens or credentials, or clipboard contents with PII.

## Report handoff

1. `pentest_agent_record_finding` for: hidden processes, code injection indicators, C2 network artifacts, credential-harvesting evidence, and timeline gaps.
2. Package the memory forensics matrix with each finding.
3. Hand off extracted binaries and injected code regions to the reverse-engineering workflow. Hand off network indicators to the network forensics workflow. Hand off credential exposure metadata to the incident response team for credential reset — never share raw hashes in reports.
4. Recommend: reset all accounts whose credentials were found in memory, investigate the infection vector that led to the memory state, deploy enhanced process logging (Sysmon, auditd), and enable credential guard where supported.
