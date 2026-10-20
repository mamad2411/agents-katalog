---
name: forensic-network
description: Network forensic analysis — PCAP, flow-log, and saved-telemetry review with hash-first discipline, traffic reconstruction, C2 detection, and credential redaction.
disable-model-invocation: true
risk: passive
allowed-modes: [forensic, blue-team]
authorization-required: conditional
evidence-outputs: [pcap-summary, session-inventory, ioc-list, redacted-evidence, finding-draft]
---

# Network forensics — packet capture and traffic analysis

Use this skill to analyze captured network traffic (PCAP, flow logs, NetFlow, saved firewall/IDS telemetry) with hash-first evidence handling and offline-only discipline. Reconstruct session timelines, detect C2 patterns, extract file transfers, and identify data exfiltration — all without replaying traffic, contacting external hosts, or storing raw credentials.

## Required inputs

- Capture file path confirmed readable, with SHA-256 hash recorded before any analysis.
- Writeable output directory under `.pi/pentest-agent/` for extracted files, session summaries, and indicator lists.
- Scope defining which IP ranges, protocols, time windows, and hosts are in scope. Traffic involving out-of-scope hosts must not be analyzed.
- Current authorization cache if the capture contains traffic from live or third-party systems; otherwise authorization is conditional on capture origin.
- Capture metadata: time span, capture point (SPAN port, tap, endpoint), and any known capture gaps or filtering.
- Tshark, tcpdump, or equivalent analysis tool confirmed available — detect only, never auto-install.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` when IP ranges, hosts, or protocols are scoped.
3. `pentest_agent_validate_target` before any analysis that identifies live host details.
4. `pentest_agent_check_authorization` before analyzing potentially sensitive traffic.
5. `pentest_agent_build_command` for dry-run argv preview before every tool invocation.
6. `pentest_agent_execute_tool` for read-only analysis execution — never raw shell.
7. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — capture overview and quality assessment

1. Hash the capture file before any analysis. Record algorithm, timestamp, analyst, and source.
2. Extract capture metadata: time span (first and last packet), packet count, data volume, capture interface or tap point, and any truncation or filtering.
3. Enumerate protocols present in the capture: protocol hierarchy with packet and byte counts per protocol layer. Flag unexpected protocols for the environment (e.g., SMB on a DMZ capture, Telnet on a modern network).
4. Identify all unique IP endpoints (source and destination) and their traffic volumes. Classify each endpoint: internal host, external host, broadcast/multicast, or unknown. Flag endpoints with anomalous traffic volumes or bursty patterns.
5. Assess capture quality: are both directions of each connection present? Is there evidence of packet loss (TCP retransmissions, gaps in sequence numbers)? Are timestamps consistent?

### Phase 2 — session reconstruction and traffic classification

1. Enumerate all TCP and UDP conversations: source/destination IPs and ports, connection duration, packet counts and byte volumes in each direction.
2. For each conversation, classify the application protocol using port numbers, protocol dissectors, and traffic patterns. Flag conversations on non-standard ports for their protocol class.
3. Identify long-running sessions: sessions lasting more than one hour, sessions with regular-interval keepalives (potential beaconing), and sessions that span the entire capture window.
4. Flag asymmetric conversations: large data volumes in one direction (potential exfiltration), many small inbound packets with large outbound responses (potential command-and-control), or sessions where the client sends significantly more data than the server.
5. Build a session timeline: plot all conversations chronologically, annotating session start/end, protocol, and data volumes.

### Phase 3 — suspicious traffic and C2 pattern detection

1. **Beaconing detection**: identify sessions with regular timing intervals (e.g., every 60 seconds, every 5 minutes). Use inter-arrival-time analysis on packets or application-layer requests. Flag intervals with low jitter (standard deviation < 5% of interval).
2. **DNS anomaly detection**: identify: unusually long domain names (potential DNS tunneling), domains with entropy suggestive of encoded data, TXT or NULL record queries to rare domains, high-frequency queries to a small set of domains (DGA pattern), and domains with recently-registered or low-TTL values.
3. **C2 framework signatures**: identify traffic patterns matching known C2 frameworks: HTTP requests with minimal or absent headers, TLS connections using self-signed or default certificates on non-standard ports, periodic HTTP GET with no corresponding content-length, and HTTP POST with fixed or padded payload sizes.
4. **Data exfiltration indicators**: flag sessions with large outbound data volumes to external hosts, outbound traffic over non-standard protocols (ICMP tunneling, DNS tunneling on non-DNS ports), and traffic to cloud storage or file-sharing services during unusual hours.
5. Do not contact any identified C2 infrastructure for verification — record indicators for threat-intel lookup only through authorized channels.

### Phase 4 — credential and sensitive-data exposure review

1. Scan for authentication material in cleartext: HTTP Basic Auth headers, FTP USER/PASS commands, SMTP AUTH LOGIN, IMAP/POP3 LOGIN, Telnet login sequences, and SNMP community strings.
2. Scan for credential hashes in network protocols: NTLM challenge-response handshakes (SMB, HTTP-NTLM, LDAP-NTLM), Kerberos ticket exchanges, and NetNTLMv2 responses. Record presence and involved accounts — never extract the hash material into evidence.
3. Scan for session tokens and API keys: HTTP Authorization Bearer headers, cookie headers containing session identifiers, and URL query parameters containing tokens or keys.
4. Identify cleartext PII in application-layer traffic: email addresses, phone numbers, credit card track data, social security numbers, and healthcare identifiers. Record the protocol and session but never extract the values into evidence.
5. Redact all discovered credentials, tokens, and PII before recording evidence. Store only: credential type, protocol, source/destination IPs, and timestamp.

### Phase 5 — file extraction and content triage

1. Extract files transferred over HTTP, SMB, FTP, TFTP, and SMTP. Hash each extracted file before further analysis.
2. Classify extracted files by type: executables, documents, archives, scripts, images, and unknown. Flag: executables transferred over HTTP, scripts downloaded from external hosts, and archives containing executables or scripts.
3. For each extracted file: record filename, source/destination IPs, protocol, transfer direction (upload/download), file size, hash, and timestamp.
4. Do not execute extracted files. Do not open documents with macros enabled. Do not extract embedded objects from documents without hash-first discipline.
5. Cross-reference extracted files with the disk forensics timeline: do any extracted files match files found on disk? Are there files in the capture that do not appear in the filesystem (deleted or memory-only)?

## Decision points

- **Escalate on confirmed C2 beaconing**: regular-interval traffic with low jitter to external hosts is a high-confidence indicator of compromised endpoints.
- **Escalate on large outbound data transfers**: sessions with high byte-count asymmetry to external hosts, especially over non-HTTP/HTTPS protocols, indicate potential data exfiltration.
- **Escalate on cleartext credentials**: any cleartext authentication material in the capture requires immediate credential rotation for the affected accounts.
- **Escalate on lateral-movement protocol usage**: SMB, RDP, SSH, or WinRM sessions between internal hosts, especially from a workstation to a server, may indicate lateral movement.
- **Downgrade on expected administrative traffic**: vulnerability scanner traffic, patch management downloads, and known backup replication flows are expected and not indicative of compromise.

## Prohibited behavior

- Replaying captured traffic against live hosts or networks.
- Contacting external IP addresses or domains found in the capture for verification.
- Extracting and storing cleartext credentials, NTLM hashes, Kerberos tickets, session tokens, or API keys in evidence.
- Extracting and storing PII, healthcare data, financial data, or classified material from traffic payloads.
- Running active network scans or probes to validate capture findings.
- Exporting decoded application-layer payloads containing sensitive data outside `.pi/pentest-agent/`.

## Stop conditions

- Capture contains credentials → stop extracting, record metadata (type, protocol, accounts), recommend credential rotation.
- Capture contains PII or regulated data → stop, escalate to legal/data-protection.
- Traffic pattern suggests an ongoing intrusion → stop, escalate to incident response immediately.
- Capture includes out-of-scope hosts or networks → stop, do not analyze those sessions.
- Extracted file is malware → stop extraction, record hash and metadata, hand off to malware-triage workflow.

## Evidence — network forensics matrix

For each capture analyzed, record:

```text
Capture: <filename> | SHA-256: <hash>
Time span: <earliest ISO 8601> → <latest ISO 8601>
Capture point: <SPAN port | tap | endpoint> | Filter: <none | BPF expression>

Protocol hierarchy:
  Layer 2: <Ethernet | 802.11 | ...>
  Layer 3: <IPv4: N packets/N bytes | IPv6: N packets/N bytes>
  Layer 4: <TCP: N sessions | UDP: N sessions>
  Layer 7: <HTTP: N, DNS: N, TLS: N, SMB: N, ...>

Endpoint inventory:
  Internal hosts: <count>
  External hosts: <count>
  Top talkers (by byte volume): <IP — bytes sent/received>

Session summary:
  Total TCP sessions: <count>
  Total UDP flows: <count>
  Long-running sessions (>1hr): <count>
  Asymmetric sessions (exfil candidates): <count>

Anomaly flags:
  Beaconing candidates: <count — intervals and hosts>
  DNS anomalies: <count — types>
  C2 framework patterns: <count — framework and hosts>
  Cleartext credentials: <count — protocols, accounts redacted>
  NTLM/Kerberos hash material: <present — accounts>
  PII/sensitive data: <present — types, redacted>

Extracted files:
  Total: <count>
  By type: <executables: N, documents: N, scripts: N, images: N, other: N>
  Suspicious: <count — executables over HTTP, scripts from external, etc.>
```

Never store: password hashes, Kerberos tickets, cleartext passwords, session cookies, API keys, PII values, credit card numbers, healthcare data, unredacted application-layer payloads, or extracted files containing credential or PII material.

## Report handoff

1. `pentest_agent_record_finding` for: C2 beaconing, data exfiltration, lateral-movement traffic, cleartext credentials, and protocol anomalies.
2. Package the network forensics matrix with each finding.
3. Hand off extracted files (excluding credential/PII-containing files) to malware-triage or disk-forensics for correlation. Hand off IOCs (IPs, domains, URLs, file hashes) to threat-intel and detection-engineering teams.
4. Recommend: block identified C2 infrastructure at the perimeter, rotate credentials for all accounts with exposed authentication material, enable TLS inspection on egress traffic to detect C2 tunneling, deploy network detection rules for identified beacon patterns, and correlate the network timeline with host-based forensic timelines.
