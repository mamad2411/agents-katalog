---
name: forensic-chain-of-custody
description: Chain-of-custody documentation — record evidence provenance, handling, transfers, hashes, and analysis steps with explicit gap-logging and no fabrication of missing records.
disable-model-invocation: true
risk: report-only
allowed-modes: [forensic, blue-team]
authorization-required: no
evidence-outputs: [chain-of-custody-log, custody-transfer-records, evidence-hash-manifest, audit-notes]
---

# Chain of custody — evidence provenance and handling log

Use this skill to document the chain of custody for every piece of evidence across the forensic investigation lifecycle. Record who provided each artifact, when it was received, where it is stored, every copy and transfer, every analysis step applied, and every hash taken. Flag gaps explicitly — never invent provenance, assume custody continuity, or fabricate timeline certainty. This is a report-only skill; it documents evidence already collected and does not authorize new collection or active system contact.

## Required inputs

- Evidence inventory: list of all artifacts (disk images, memory dumps, PCAP files, extracted files, log exports, physical media) with unique identifiers.
- For each artifact: original source (who provided it, when, from which system), acquisition method, initial hash (SHA-256 minimum), and storage location.
- Analysis log: record of every tool executed against each artifact, with timestamps, tool name/version, command arguments, and output artifacts produced.
- Transfer records: for every handoff between analysts or systems — who transferred, who received, when, and hash verification before and after transfer.
- Scope and authorization records confirming the investigation boundary and approval.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before documentation.
2. `pentest_agent_parse_scope` to confirm evidence falls within investigation scope.
3. `pentest_agent_validate_target` only if documenting evidence from a live system — confirm the system is in scope.
4. `pentest_agent_list_evidence` to inventory already-collected artifacts.
5. `pentest_agent_list_findings` to cross-reference custody records with findings.
6. `pentest_agent_render_report` to produce the custody report — never raw shell.

## Workflow

### Phase 1 — evidence intake and identification

1. For each evidence item received: assign a unique evidence ID (format: `EVID-<YYYY>-<NNNN>`). Record: date and time of receipt, receiving analyst, provider name and organization, and method of transfer (physical handoff, secure file transfer, chain-of-custody form).
2. Record the evidence description: type (disk image, memory dump, physical drive, USB device, mobile device, document, log file), make/model/serial number for physical items, logical size in bytes, and any visible markings, labels, or damage.
3. Take the initial hash (SHA-256 minimum). Record: hashing tool and version, hash algorithm, hash value, timestamp, and analyst. If the artifact is physical and cannot be hashed directly, hash the first forensic image taken.
4. Photograph physical evidence if applicable — record the photo filename and hash. Never store photos containing PII, credentials, or classified markings in unredacted form.
5. Seal and store the original evidence: record the storage location (safe number, evidence locker ID, secure file path), storage timestamp, and any access controls (combination, key holder, encryption key custodian).

### Phase 2 — custody transfer documentation

1. For every transfer of evidence between analysts, systems, or locations: record the transfer date/time, transferring analyst, receiving analyst, transfer reason (assignment, escalation, storage relocation), and method of transfer.
2. Before transfer: the transferring analyst verifies the evidence hash matches the intake hash. Record the verification result (matched / mismatch — if mismatch, stop transfer and escalate).
3. After transfer: the receiving analyst independently verifies the evidence hash. Record the verification result.
4. For electronic transfers: record the transfer protocol or method (SFTP, encrypted USB, secure file share), the source and destination paths, and any encryption applied during transit.
5. Flag any transfer where hash verification was not performed or could not be completed — record the gap explicitly and the reason.

### Phase 3 — analysis step logging

1. For every analysis step performed on an evidence item or its working copy: record the date/time, analyst, tool name and version, command arguments (redacted if they contain paths with PII), input artifact ID, and output artifact IDs.
2. For each output artifact produced: assign a new evidence ID, take a hash, and record its relationship to the source evidence item. Link output artifacts to the analysis step that produced them.
3. If analysis is performed on a working copy rather than the original: record that a copy was made, the copy's evidence ID and hash, and confirm the original was not modified.
4. Log any unexpected tool behavior, errors, or results that could affect evidence integrity.
5. Never log: raw credential values, PII from command arguments, unredacted file paths containing usernames, or internal hostnames in tool output unless the output is already redacted.

### Phase 4 — gap identification and explicit logging

1. Review the full custody timeline for gaps: periods where evidence location is unknown, transfers without recorded hash verification, analysis steps performed without tool/version logging, and artifacts without initial hashes.
2. For each gap identified: record the time period or event, the missing information, the reason the gap exists (analyst unavailable, tool failure, procedural oversight, evidence received from third party without initial hash), and whether the gap can be remediated (retrospective hashing, witness statement) or must remain as a documented gap.
3. Do not fill gaps with assumptions. If the custody record shows a 48-hour period with no recorded evidence location, document "Custody gap: 2026-06-15 14:00 to 2026-06-17 14:00 — evidence location unrecorded." Never write "Evidence was presumably in storage" without supporting documentation.
4. Flag gaps that affect evidence admissibility: gaps in physical custody of original devices, transfers without verification, and analysis steps performed by unidentified or unauthorized analysts.
5. Classify each gap: admissible (minor gap with documented explanation and no evidence of tampering), concerning (gap that could be questioned but hash integrity is maintained), and critical (gap that could compromise admissibility — missing initial hash, unmonitored physical access, unknown analyst).

### Phase 5 — hash manifest and final verification

1. Build a complete hash manifest: every evidence item (original, working copy, and output artifact) with its evidence ID, description, hash algorithm, hash value, and relationship to parent evidence.
2. Verify every hash in the manifest against the current state of stored evidence. Flag any mismatches between the manifest hash and the current hash — this indicates evidence tampering, storage corruption, or recording error.
3. For any hash mismatch: stop further analysis on that item, record the mismatch, and escalate. Do not attempt to explain the mismatch without forensic investigation.
4. Generate the chain-of-custody report: evidence inventory, intake records, transfer log, analysis log, gap analysis, hash manifest, and final verification results.
5. Sign the custody report: analyst name, date, and a statement that the report is complete and accurate to the best of the analyst's knowledge. Include a digital signature or hash of the report itself.

## Decision points

- **Escalate on hash mismatch**: any evidence item whose current hash does not match the manifest hash — this is a critical custody failure.
- **Escalate on critical gaps**: unmonitored physical access to original evidence, missing initial hash, or analysis by unauthorized personnel — these may compromise admissibility.
- **Escalate on chain break**: evidence transferred without documentation — the chain is broken and must be reported, not concealed.
- **Escalate on evidence tampering indicators**: hashes that change after custody was established, signs of physical tampering on sealed evidence, or unexplained modifications to working copies.
- **Downgrade on minor procedural gaps**: a missing timestamp on a copy operation where the original hash is intact, or a transfer documented in email but not yet recorded in the custody log — record the gap but note that evidence integrity is not compromised.

## Prohibited behavior

- Inventing custody records for undocumented periods — gaps must be logged as gaps, never filled with assumptions.
- Modifying evidence hashes to match manifest records after evidence has changed.
- Altering timestamps on custody log entries after the fact without noting the correction and reason.
- Using custody documentation as a vehicle for storing raw evidence content, PII, or credentials.
- Exporting custody records with unredacted analyst personal information, internal storage paths, or evidence content outside `.pi/pentest-agent/`.

## Stop conditions

- Hash mismatch detected → stop, escalate, do not continue analysis on affected evidence.
- Gap discovered that cannot be explained → document the gap, flag if critical, but do not stop the entire investigation — only affected evidence items are impacted.
- Evidence provenance cannot be established (unknown source, received anonymously) → document as a critical gap, evidence may be inadmissible.
- Custody log would expose PII, credentials, or classified content → redact before recording.

## Evidence — chain-of-custody records

For the investigation, produce:

```text
Case ID: <CASE-YYYY-NNNN>
Investigation period: <start ISO 8601> → <end ISO 8601 | ongoing>
Lead analyst: <name | ID>

Evidence inventory:
  EVID-YYYY-0001: <type — disk image> | source: <system/host> | hash: SHA-256: <hash> | intake: <ISO 8601> | analyst: <ID> | storage: <location ID>
  EVID-YYYY-0002: <type — memory dump> | source: <system/host> | hash: SHA-256: <hash> | intake: <ISO 8601> | analyst: <ID> | storage: <location ID>
  ...

Custody timeline:
  <ISO 8601> | EVID-YYYY-0001 | INTAKE | analyst: <ID> | provider: <name> | hash verified: yes
  <ISO 8601> | EVID-YYYY-0001 | TRANSFER | from: <ID> → to: <ID> | hash before: match | hash after: match
  <ISO 8601> | EVID-YYYY-0001 | ANALYSIS | analyst: <ID> | tool: <name v1.2.3> | action: <filesystem timeline> | output: EVID-YYYY-0010
  ...

Gap analysis:
  Gap 1: <ISO start> → <ISO end> | EVID-YYYY-0003 | location unrecorded | severity: concerning | remediation: <none — documented gap>
  Gap 2: <ISO timestamp> | EVID-YYYY-0005 | transfer without hash verification | severity: critical | remediation: <retrospective hash taken, matches manifest>

Hash manifest:
  EVID-YYYY-0001 | SHA-256: <hash> | type: original | verified: <ISO 8601> | status: match
  EVID-YYYY-0010 | SHA-256: <hash> | type: output from EVID-YYYY-0001 | verified: <ISO 8601> | status: match
  ...

Final verification:
  Manifest entries: <count>
  Verified matches: <count>
  Mismatches: <count — evidence IDs>
  Critical gaps: <count>
```

Never store: unredacted analyst personal contact information, physical storage location details that could compromise evidence security (safe combinations, locker access codes), raw evidence content in custody records, or transfer records containing unredacted PII of providers or witnesses.

## Report handoff

1. `pentest_agent_record_finding` for: hash mismatches indicating tampering, critical custody gaps affecting admissibility, and chain breaks where evidence provenance is lost.
2. Package the chain-of-custody report with the investigation case file.
3. Hand off to legal or compliance: the custody report, gap analysis, and hash manifest. If the case may proceed to legal action, ensure the custody report is signed, dated, and accompanied by analyst credentials.
4. Recommend: maintain the custody log as a living document throughout the investigation, re-verify evidence hashes at case closure, store the final custody report with the evidence in write-once storage, and ensure every analyst who handles evidence understands that undocumented handling is a custody gap — not an acceptable shortcut.
