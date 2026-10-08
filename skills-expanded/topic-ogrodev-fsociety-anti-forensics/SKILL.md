---
name: anti-forensics
description: |
  This skill should be used when the user mentions "log cleaning", "clear logs",
  "wipe logs", "timestomp", "timestamp manipulation", "metadata stripping",
  "exiftool", "mat2", "file wiping", "shred", "srm", "secure delete",
  "bleachbit", "memory clearing", "swap wipe", "bash history", "wtmp", "btmp",
  "lastlog", "auth.log", "journal", "journalctl", "forensic artifacts",
  "anti-forensics", "trace removal", "cover tracks", "clean up traces",
  "eliminate footprint", "shell history", "browser artifacts", "dns cache",
  "arp cache", "network artifacts", "filesystem artifacts", "recent files",
  "thumbnails", "memory forensics", "swap artifacts", "proc cleanup",
  "container forensics", "cleanup checklist", "post-op cleanup",
  "artifact minimization", "live forensics evasion", "volatile artifacts",
  or discusses eliminating evidence, minimizing forensic traces, or cleaning
  operational artifacts from systems during or after authorized engagements.
  Make sure to activate this skill even when the user doesn't explicitly say
  "anti-forensics" — any mention of cleaning traces, removing evidence,
  wiping artifacts, or post-operation cleanup should trigger this skill.
version: 2.0.0
---

# Anti-Forensics

Systematic identification and elimination of forensic artifacts across logs, file metadata, filesystem traces, volatile memory, network state, shell history, and application caches. Covers the full artifact lifecycle: pre-operation minimization, in-operation hygiene, and post-operation cleanup.

## Why This Matters

Every action on a system leaves traces. A forensic investigator reconstructs timelines from logs, login records, shell history, file metadata, memory dumps, and network artifacts. Anti-forensics is not about making evidence vanish — it's about understanding exactly what traces exist, which ones matter, and eliminating them selectively without creating new anomalies that scream "someone cleaned up here." The goal is plausible deniability or complete trace elimination, depending on the opsec profile.

## Tool Routing by Category

| Category | Primary Tools | Target Artifacts | Reference |
|----------|--------------|------------------|-----------|
| Log manipulation | `sed`, `utmpdump`, `journalctl`, `auditctl` | auth.log, syslog, wtmp, btmp, lastlog, journal, audit.log | `references/log-manipulation.md` |
| Metadata stripping | `exiftool`, `mat2`, `ffmpeg`, `qpdf` | EXIF, XMP, IPTC, PDF metadata, Office metadata, audio/video tags | `references/metadata-stripping.md` |
| Secure file deletion | `shred`, `srm`, `dd`, `hdparm`, `nvme` | File content, free space, swap, SSD secure erase | `references/secure-deletion.md` |
| Volatile artifacts | `swapon/off`, `sysctl`, `ip`, `iptables` | RAM caches, swap, /proc, /dev/shm, page cache | `references/memory-and-volatile.md` |
| Shell & terminal history | `history`, `unset`, `shred`, `ln` | bash_history, zsh_history, python_history, mysql_history, psql_history, less, vim | `references/shell-history.md` |
| Filesystem artifacts | `find`, `touch`, `debugfs`, `tune2fs` | timestamps, journals, thumbnails, recently-used, trash, MRU lists | `references/filesystem-artifacts.md` |
| Network artifacts | `ip`, `arp`, `resolvectl`, `conntrack`, `ss` | ARP cache, DNS cache, routing table, connection tracking, firewall logs | `references/network-artifacts.md` |
| Browser & application caches | `rm`, `find`, `sqlite3` | browser history, cookies, cache, download history, session data | `references/application-artifacts.md` |

## Opsec Profile Integration

The opsec profile determines the depth and urgency of anti-forensics operations. Always check the active profile before starting cleanup.

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/opsec-profile.js" get
```

| Profile | Cleanup Scope | Timing | Approach | Checklist |
|---------|--------------|--------|----------|-----------|
| `loud` | None — lab/CTF environment | N/A | No cleanup needed | — |
| `normal` | Selective — remove obvious tool traces | Post-operation | Remove command history, temp files, clear auth artifacts | `references/cleanup-checklists.md` section "Normal" |
| `stealth` | Comprehensive — eliminate all recoverable traces | During + post-operation | Full log manipulation, metadata strip, secure delete, memory clear | `references/cleanup-checklists.md` section "Stealth" |
| `paranoid` | Total — assume forensic imaging is imminent | Continuous + post-operation | Everything in stealth + journal tampering, swap wipe, filesystem journal clear, SSD secure erase | `references/cleanup-checklists.md` section "Paranoid" |

## Methodology

### Phase 1 — Pre-Operation Artifact Minimization

Before touching a target, configure the operator's own system to minimize artifact generation. This is cheaper than cleaning up later.

1. **Disable shell history recording** before starting (see `references/shell-history.md`)
2. **Mount sensitive work directories as tmpfs** so data never hits disk
3. **Configure browser for no-trace mode** if browser-based access is needed
4. **Set up encrypted scratch space** for any files that must be written to disk
5. **Disable core dumps**: `ulimit -c 0`
6. **Disable swap** if sufficient RAM: `sudo swapoff -a`

### Phase 2 — In-Operation Hygiene

During active operations, maintain artifact discipline:

1. **Pipe output rather than writing files** — avoid creating temporary files where possible
2. **Use memory-backed storage** (`/dev/shm`, tmpfs mounts) for operational data
3. **Monitor your own footprint** — periodically check what traces you're leaving
4. **Avoid tools that create dot-files** in home directories (or clean them immediately)
5. **Use timestomped file operations** — if you must write files, backdate timestamps to blend with existing files

### Phase 3 — Post-Operation Cleanup

Systematic elimination in priority order:

1. **Shell history** — highest priority, contains exact commands (see `references/shell-history.md`)
2. **Authentication logs** — shows your access times, IPs, usernames (see `references/log-manipulation.md`)
3. **Login records** — wtmp/btmp/lastlog prove you logged in (see `references/log-manipulation.md`)
4. **Filesystem artifacts** — timestamps, journals, recent-file lists (see `references/filesystem-artifacts.md`)
5. **Network artifacts** — ARP cache, DNS cache, connection logs (see `references/network-artifacts.md`)
6. **Application artifacts** — browser data, tool configs, dot-files (see `references/application-artifacts.md`)
7. **File metadata** — EXIF, Office metadata on any dropped files (see `references/metadata-stripping.md`)
8. **Volatile memory** — page cache, swap, /tmp contents (see `references/memory-and-volatile.md`)
9. **Secure deletion** — overwrite and remove any operational files (see `references/secure-deletion.md`)

### Phase 4 — Verification

Re-scan every category to confirm artifact elimination. A cleanup that can't be verified is a cleanup that didn't happen.

```bash
# Verification commands are detailed in each reference file
# General pattern: re-run the detection commands and confirm empty results
```

### Phase 5 — Logging and Reporting

All anti-forensics operations MUST be tracked via ops-tracker, even cleanup itself:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" add \
  --category "anti-forensics" \
  --action "<action>" \
  --detail "<detail>"
```

If the opsec profile is `paranoid`, the ops-tracker data itself should be securely deleted after the engagement report is finalized and archived.

## Cross-Skill References

- **System hardening** (`system-hardening`): Hardening configs can affect what gets logged. Disable verbose logging on operator machines before operations.
- **Network anonymity** (`network-anonymity`): Proxy chains and VPN configs leave artifacts. Clean proxy logs, VPN connection state files, and routing table entries.
- **VPS security** (`vps-security`): VPS disk encryption means secure deletion of the encryption key effectively wipes the entire disk. Use this as a last resort.
- **Opsec reporting** (`opsec-reporting`): Cleanup reports feed into the engagement report. Track everything, then decide what to purge based on opsec profile.

## Detection Awareness

A forensic investigator looks for anti-forensics indicators too. Be aware that the following create their own artifacts:

- **Truncated logs** — log files that suddenly have a size discontinuity or missing time ranges
- **Zeroed sections** — journal or wtmp files with null bytes where records should be
- **Modified timestamps** — atime/mtime/ctime inconsistencies (ctime cannot be faked without raw disk access)
- **Missing history files** — `.bash_history` that's empty or missing when the account has been active
- **Shred patterns** — overwrite patterns visible in unallocated space
- **Log service restarts** — systemd journal showing rsyslog/journald restarts at suspicious times

The references detail how to avoid each of these detection indicators.
