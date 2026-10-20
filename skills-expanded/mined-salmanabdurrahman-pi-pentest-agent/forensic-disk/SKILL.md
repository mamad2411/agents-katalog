---
name: forensic-disk
description: Disk image and filesystem forensics — read-only mount discipline, file carving, timeline reconstruction, artifact extraction, and chain-of-custody with no original-evidence modification.
disable-model-invocation: true
risk: passive
allowed-modes: [forensic, blue-team]
authorization-required: conditional
evidence-outputs: [evidence-hash, timeline, carved-files-summary, metadata-report, redacted-evidence]
---

# Disk forensics — image analysis and file recovery

Use this skill to analyze disk images, recover deleted files, reconstruct filesystem timelines, and extract forensic artifacts with strict read-only discipline. Work exclusively on copies of evidence images. Never mount original evidence writable, run executables recovered from disk, or modify filesystem metadata on evidence.

## Required inputs

- Disk image file path confirmed readable, with SHA-256 hash recorded before any analysis step.
- Writeable output directory under `.pi/pentest-agent/` for carved files, timelines, and extracted metadata.
- Confirmation that the image is a copy and that mounting (if required) will be read-only.
- Scope defining which partitions, file types, time windows, and artifact categories are in scope.
- Current authorization cache if disk contents include data from live systems, third-party storage, or personally-identifiable information.
- Filesystem analysis tooling confirmed available: sleuthkit, foremost, bulk_extractor, or equivalents.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` when image origin, target systems, or artifact categories are scoped.
3. `pentest_agent_validate_target` before any analysis that could identify live system details or mount points.
4. `pentest_agent_check_authorization` before any analysis step involving potentially sensitive file contents.
5. `pentest_agent_build_command` for dry-run argv preview before every tool invocation.
6. `pentest_agent_execute_tool` for read-only analysis execution — never raw shell.
7. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — image validation and partition mapping

1. Record the image hash (SHA-256) before any analysis. Log algorithm, timestamp, analyst identifier, and source.
2. Identify the partition table type (MBR, GPT) and list all partitions with their offsets, sizes, and filesystem types. Record the partition layout.
3. For each partition, identify the filesystem (NTFS, ext4, APFS, XFS, FAT32, exFAT) and validate that the filesystem superblock or boot sector is intact.
4. Check for unallocated space between partitions — this may contain remnants from previous partitioning or hidden data.
5. If the image is encrypted (BitLocker, LUKS, FileVault), record the encryption type and scope. Do not attempt decryption without separate authorization and key material.

### Phase 2 — filesystem enumeration and timeline

1. Enumerate every file and directory entry on each partition: full path, size, MACB timestamps (Modified, Accessed, Changed, Birth), inode/file-reference number, and file type.
2. Build a filesystem timeline from the timestamp data. Sort chronologically and annotate each entry with the event type (file created, modified, accessed, metadata changed, deleted).
3. Flag timeline anomalies: file timestamps predating filesystem creation, timestamps in the future, rapid file creation/deletion bursts (potential ransomware or wiper activity), and files modified outside the expected time window.
4. Identify orphaned files: files whose parent directory is deleted, files in unallocated space referenced only by inode/file-record metadata, and files with cross-linked clusters.
5. Map the directory structure and flag: world-writable directories, hidden directories (names starting with `.` on Linux or with the hidden attribute on Windows), directories with names resembling system directories in unexpected locations, and user home directories with unusual permissions.

### Phase 3 — file carving and deleted-file recovery

1. Run file-carving tools against the unallocated space and slack space of each partition. Target file types relevant to the investigation: documents, images, archives, executables, email stores, databases, and log files.
2. For each carved file: hash it (SHA-256), record the byte offset where it was found, note whether it is a partial or complete recovery, and classify by file type.
3. Validate carved files: check file headers and footers, attempt to open or parse with read-only tools, and flag files with corrupted or intentionally-mangled structures.
4. Compare carved files against the active filesystem: do any carved files match known files? Carved files that do not appear in the active filesystem may have been deleted or hidden.
5. Do not execute carved executables, scripts, or macros. Do not open carved documents with macros enabled or in connected environments.

### Phase 4 — artifact-specific analysis

1. **Windows artifacts**: extract and analyze Event Logs (Security, System, Application), Prefetch files (execution evidence), Registry hives (SAM, SYSTEM, SOFTWARE, NTUSER.DAT), LNK/Shortcut files (recently-opened files), Jump Lists, Shellbags (folder access), and Amcache/RecentFileCache (execution evidence). Do not attempt to decrypt stored credentials from SAM/SYSTEM — record their presence only.
2. **Linux/macOS artifacts**: extract shell history files, system logs, crontab and launchd entries, SSH authorized_keys files, recently-opened file lists, and package manager installation logs. Flag: unauthorized cron entries, newly-added SSH keys, and software installed outside the package manager.
3. **Browser artifacts**: extract browser history databases, cookie stores, download records, and cached credentials from browser profile directories. Record: visited URLs (domain only for sensitive/PII URLs), download timestamps, and whether saved credentials are present (never extract the credentials themselves).
4. **Email and communication artifacts**: extract PST/OST/MBOX files, chat logs, and messaging database files if in scope. Record: sender/recipient patterns, attachment names and hashes, and message timestamps. Never store message bodies containing PII or credentials.
5. Hash every extracted artifact before further processing. Log the extraction tool, source offset, timestamp, and hash.

### Phase 5 — metadata aggregation and cross-analysis

1. Extract metadata from all recovered files: EXIF data from images (camera model, GPS coordinates, timestamps), document metadata (author, editor, revision history, printer names), and binary metadata (compile timestamps, imported libraries, debug symbols).
2. Cross-reference metadata across artifacts: does a document author name appear in an email archive? Do GPS coordinates from images match the expected device location? Does a compile timestamp align with the intrusion timeline?
3. Flag metadata anomalies: timestamps that predate the file format, GPS coordinates outside expected geographic range, document revision histories that suggest data exfiltration or tampering, and software compile timestamps within the intrusion window.
4. Build a consolidated artifact-to-timeline mapping: each recovered file, event log entry, browser history record, and metadata extract should correlate to a point or range on the filesystem timeline.
5. Redact sensitive metadata: GPS coordinates of personal devices, document author names that are PII, printer names that reveal internal network topology, and any metadata values that could expose credentials, tokens, or internal hostnames.

## Decision points

- **Escalate on timestamp anomalies**: filesystem timestamps that predate the OS install, are in the future, or show bulk manipulation suggest anti-forensic activity or system compromise.
- **Escalate on hidden or encrypted volumes**: partitions with no recognized filesystem, TrueCrypt/VeraCrypt headers, or large blocks of high-entropy data in unallocated space warrant deeper analysis.
- **Escalate on deleted evidence files**: carved files matching known evidence types (documents, databases, email stores) that do not exist in the active filesystem suggest deliberate deletion.
- **Escalate on credential stores**: SAM/SYSTEM registry hives, browser saved-credential databases, and SSH private key files must be flagged for credential-reset workflows — never extract the credentials.
- **Downgrade on expected system artifacts**: Windows Update logs, browser cache files with no investigation relevance, and OS-generated temporary files are expected and not indicative of compromise without additional context.

## Prohibited behavior

- Mounting the original evidence image writable or modifying filesystem metadata.
- Executing recovered executables, scripts, macros, or installers on any host.
- Extracting and storing credentials, private keys, cookies, or session tokens from artifacts.
- Accessing network shares, cloud storage, or remote filesystems referenced in disk artifacts.
- Running filesystem repair tools (chkdsk, fsck) on the evidence image — this modifies metadata.
- Exporting artifact contents containing PII or credentials outside `.pi/pentest-agent/`.

## Stop conditions

- Image hash verification fails or image shows signs of tampering → stop, record integrity concern.
- Encrypted volume or file container found without authorized decryption key → stop, do not attempt decryption.
- Credential store found (SAM hive, browser saved passwords, SSH private keys) → stop extraction, record metadata, recommend credential reset.
- Evidence contains PII, healthcare data, financial records, or classified material beyond investigation scope → stop, escalate to legal.
- Recovered file appears to be malware or contains active exploit code → stop, do not execute, hand off to malware-triage workflow.

## Evidence — disk forensics matrix

For each disk image analyzed, record:

```text
Image: <filename> | SHA-256: <hash> | Size: <bytes>
Partition layout: <MBR | GPT> — <count> partitions
  Partition 1: <offset>–<end> | <filesystem> | <size> | <label>
  ...

Filesystem summary:
  Total files: <count>
  Total directories: <count>
  Deleted files (carvable): <count>
  Files with anomalous timestamps: <count>

Timeline span: <earliest ISO 8601> → <latest ISO 8601>
  Timeline anomalies: <list — future timestamps, predating timestamps, bursts>

Carved files:
  Total carved: <count>
  By type: <documents: N, images: N, archives: N, executables: N, other: N>
  Complete recoveries: <count>
  Partial recoveries: <count>

Key artifacts:
  Windows Event Logs: <count> | span: <ISO range>
  Prefetch entries: <count>
  Registry hives extracted: <SAM, SYSTEM, SOFTWARE, NTUSER.DAT — count>
  Browser history entries: <count>
  Email/message stores: <count>

Credential stores found: <SAM | browser passwords | SSH keys | none>
Metadata with PII/GPS: <redacted count>
```

Never store: SAM/SYSTEM hive contents with hash material, browser saved-credential databases, SSH private key contents, email message bodies with PII, GPS coordinates from personal devices, or unredacted document metadata containing author names or internal server paths.

## Report handoff

1. `pentest_agent_record_finding` for: timestamp anomalies indicating tampering, hidden/encrypted volumes, deleted evidence files recovered via carving, credential stores requiring reset workflows, and files with indicators of exfiltration or staging.
2. Package the disk forensics matrix with each finding.
3. Hand off carved malware binaries to malware-triage. Hand off email/communication artifacts to the investigation lead. Hand off credential-store metadata to incident response for forced credential rotation.
4. Recommend: preserve the original evidence image in write-once storage, generate a signed hash manifest of all extracted artifacts, correlate disk timeline with memory and network timelines, and document chain-of-custody for every artifact handoff.
