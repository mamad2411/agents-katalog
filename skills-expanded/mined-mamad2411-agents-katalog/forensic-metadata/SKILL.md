---
name: forensic-metadata
description: Metadata preservation and analysis — extract, hash, and cross-reference file metadata without altering original artifacts, with redaction of PII, GPS, credentials, and internal host identifiers.
disable-model-invocation: true
risk: passive
allowed-modes: [forensic, blue-team]
authorization-required: conditional
evidence-outputs: [metadata-summary, evidence-hash, cross-reference-map, redacted-evidence]
---

# Metadata forensics — extraction, preservation, and cross-reference

Use this skill to extract and analyze metadata from files, images, documents, and system artifacts with hash-first discipline. Preserve original timestamps and ownership — never modify artifact metadata in place. Cross-reference metadata across evidence sources to build behavioral timelines and detect tampering. Redact sensitive metadata values (GPS coordinates, PII, internal hostnames) before recording in evidence.

## Required inputs

- File or artifact paths confirmed readable, with SHA-256 hash recorded before any metadata extraction.
- Writeable output directory under `.pi/pentest-agent/` for extracted metadata records.
- Scope defining which files, file types, metadata fields, and time windows are in scope.
- Current authorization cache if metadata includes PII or information about live systems; otherwise authorization is conditional on data sensitivity.
- Metadata extraction tooling confirmed available: exiftool, sleuthkit, or equivalents — detect only.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` when file types, metadata categories, or target systems are scoped.
3. `pentest_agent_validate_target` before analyzing metadata from files that reference live system identifiers.
4. `pentest_agent_check_authorization` before extracting metadata from potentially sensitive files.
5. `pentest_agent_build_command` for dry-run argv preview before every extraction.
6. `pentest_agent_execute_tool` for read-only extraction — never raw shell.
7. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — inventory and integrity baseline

1. For every in-scope file: record the full path, file size, SHA-256 hash, filesystem timestamps (MACB), owner/group (if available), and permissions.
2. Build a file inventory sorted by: modification time (descending), file type, directory, and size. Flag files with anomalous sizes (zero-byte files where data is expected, files larger than the filesystem's reported free space).
3. Identify file-type mismatches: files whose extension does not match their detected type (e.g., `.jpg` file that is actually a ZIP archive, `.txt` file that is an executable). File-type masking is a common anti-forensic technique.
4. Record the inventory baseline before any metadata extraction — this serves as the chain-of-custody record for each file's state at the start of analysis.

### Phase 2 — file-level metadata extraction

1. For each in-scope file, extract: file-system level metadata (timestamps, permissions, attributes, alternate data streams on NTFS, extended attributes on Linux/macOS), embedded metadata (EXIF, IPTC, XMP for images; ID3 for audio; Office document properties; PDF metadata; binary compile/link timestamps), and structural metadata (codec, resolution, bitrate for media; page count, font list for documents; section headers, import table for executables).
2. Record the extraction tool, tool version, extraction timestamp, and source file hash alongside each metadata record.
3. Flag metadata fields that: have been modified (mismatch between filesystem timestamp and embedded timestamp), contain values that differ from the user-expected values (e.g., document author is not the expected user), or are missing entirely when expected (stripped EXIF data from images, absent document revision history).
4. Do not extract metadata from files that are encrypted, password-protected, or require interactive decryption — record their presence and hash only.

### Phase 3 — temporal and behavioral cross-reference

1. Normalize all timestamps to UTC. Flag files whose filesystem timestamps and embedded metadata timestamps disagree — this indicates timestamp manipulation or file copying that did not preserve metadata.
2. Cross-reference timestamps across evidence sources: does a file's creation time on disk align with its download timestamp in a browser history? Does a document's last-modified time correspond to an email attachment timestamp? Does an executable's compile timestamp fall within the intrusion window?
3. Build a behavioral timeline: for each user or process of interest, plot file creation, modification, access, and deletion events chronologically. Overlay with: process execution events from memory forensics, network session start/end from network forensics, and login/logout events from system logs.
4. Flag timeline contradictions: a file modified before the OS was installed, a document created after the user's last login, a deleted file whose deletion timestamp predates its creation timestamp, and rapid sequential modifications of files across unrelated directories (bulk tampering or ransomware).

### Phase 4 — geolocation and device fingerprinting

1. Extract GPS coordinates, altitude, direction, and timestamp from image and video metadata (EXIF GPS, XMP). Flag: coordinates that imply impossible travel between consecutive images, coordinates in unexpected regions, and images where GPS is present but the device does not normally geotag photos.
2. Extract device identifiers: camera make/model/serial number from EXIF, scanner/printer identifiers from document metadata, software name/version from document and media metadata. Cross-reference with known device inventories.
3. Flag device anomalies: a document claiming to be printed on a printer that does not exist in the environment, an image shot with a camera model released after the file's creation timestamp, or metadata referencing software versions not yet released at the purported time.
4. Redact GPS coordinates from personal devices, camera serial numbers, and printer identifiers before recording in evidence — store hashed or generalized versions (city-level only).

### Phase 5 — tampering and anti-forensic detection

1. Check for metadata stripping: files of a type that normally carry metadata (JPEG, Office documents) but have empty or absent metadata fields. Bulk metadata stripping across a set of files suggests deliberate anti-forensic action.
2. Check for metadata forgery: fields with values that are syntactically valid but semantically impossible (e.g., a camera serial number of "00000000", an author name that is a known filler value, a compile timestamp that is exactly midnight on January 1).
3. Check for timestamp manipulation: files with identical timestamps down to the second across unrelated directories, timestamps that are round numbers (exactly on the hour or at midnight), and timestamps that match known anti-forensic tool patterns.
4. Check for file-signature mismatches: a file whose header/footer bytes do not match its extension — this can indicate deliberate file-type masking to hide evidence.
5. Document every tampering indicator with: the file, the specific metadata field or pattern, the expected vs observed value, and the confidence level.

## Decision points

- **Escalate on deliberate metadata stripping**: bulk removal of EXIF data, document revision history, or other standard metadata from multiple files is a strong anti-forensic indicator.
- **Escalate on timestamp forgery**: identical or systematically-manipulated timestamps across unrelated files suggest deliberate timeline obfuscation.
- **Escalate on file-type masking**: files with mismatched extensions and content types are often used to hide evidence (e.g., renaming `.zip` to `.jpg`) or bypass security controls.
- **Escalate on geolocation anomalies**: GPS coordinates indicating impossible travel or presence in unexpected regions for the device owner.
- **Downgrade on metadata absence in expected cases**: files that never carry metadata (plaintext, raw binary dumps), files from sources known to strip metadata (social media uploads, some messaging apps), and files processed through pipelines that intentionally remove metadata.

## Prohibited behavior

- Modifying file timestamps, permissions, or ownership on evidence or working copies.
- Stripping, adding, or altering metadata fields on evidence files.
- Extracting and storing PII from metadata (author names, GPS of personal devices, printer names revealing internal network topology).
- Using metadata-derived credentials, device identifiers, or internal paths for active system access.
- Running automated metadata-extraction tools against live filesystems or mounted network shares.
- Exporting unredacted metadata records containing PII, credentials, or internal identifiers outside `.pi/pentest-agent/`.

## Stop conditions

- Metadata contains PII or credentials → stop extraction, record field type, redact values.
- GPS coordinates found in personal-device images → stop geolocation extraction, generalize to region-level only.
- Evidence of deliberate tampering detected across a large portion of the file set → stop, escalate as a high-priority anti-forensic finding.
- File requires decryption or password for metadata access → stop, do not attempt decryption.
- Metadata references out-of-scope systems, users, or locations → stop, do not record those references.

## Evidence — metadata forensics matrix

For each evidence set analyzed, record:

```text
Evidence set: <description | image name>
File inventory:
  Total files analyzed: <count>
  By type: <images: N, documents: N, archives: N, executables: N, other: N>
  Files with stripped metadata: <count and types>
  Files with mismatched extensions: <count>

Temporal analysis:
  Timeline span: <earliest ISO 8601> → <latest ISO 8601>
  Timestamp anomalies: <count — future, impossibly old, manipulated>
  Cross-reference matches: <count — files correlating with other evidence>
  Cross-reference contradictions: <count>

Geolocation:
  Files with GPS: <count>
  GPS anomalies: <count — impossible travel, unexpected regions>
  Redacted GPS records: <count — personal devices>

Tampering indicators:
  Metadata stripping: <widespread | isolated | none>
  Timestamp forgery: <detected — count of affected files | none>
  File-type masking: <detected — count and types | none>

Device fingerprinting:
  Unique camera models: <count>
  Unique printer/scanner identifiers: <count — redacted>
  Software versions identified: <list>
```

Never store: unredacted GPS coordinates from personal devices, camera serial numbers, printer identifiers with internal network paths, document author names containing PII, software license keys, or metadata fields containing credentials or tokens.

## Report handoff

1. `pentest_agent_record_finding` for: deliberate metadata stripping, timestamp forgery, file-type masking, geolocation anomalies, and device-identity contradictions.
2. Package the metadata forensics matrix with each finding.
3. Hand off the behavioral timeline (correlated across filesystem, memory, and network events) to the investigation lead. Hand off device fingerprint data (hashed/generalized) to asset management for verification.
4. Recommend: preserve original files with unmodified metadata, document every metadata-extraction tool and version used in the chain-of-custody log, correlate metadata timelines with filesystem and network timelines, and flag all anti-forensic indicators for expert review.
