---
name: folder-comparison
description: Compare two directories for content-level consistency and structural identity.
tools: rclone, diff
category: Data Management
---

# Folder Comparison Skill

This skill provides a standardized protocol for comparing two directories to ensure data duplicity,
content-level consistency, and structural identity, specifically handling macOS system noise.

## SSOT Reference

This skill is the **Single Source of Truth** for directory comparison procedures. It adheres to the
**Agent Skill Standard (v1.0)** as defined at **agentskills.io**. For underlying data integrity principles,
see **[Data Integrity Rules](../../../ai-agent-rules/ai-agent-planning-rules.md)**.

- **Setup Session**: [Setup Session Log](../../../docs/conversations/2026-02-21-folder-comparison-skill-setup.md)

## 1. Environment & Dependencies

Before executing a comparison, the agent MUST verify the availability of the following tools:

- **rclone**: Used for MD5 hash-based checks and size-only verification.
    - Check: `which rclone`
    - Install (Mac): `brew install rclone`
    - Install (Linux): `sudo apt-get install rclone` (or equivalent)
- **diff**: Used for byte-by-byte recursive structural verification (`diff -qr`).
    - Check: `which diff`
    - Note: Standard on most Unix-like systems (`/usr/bin/diff`).

## 2. Comparison Protocol

The agent MUST use a dual-verification strategy to ensure 100% data integrity.

### 2.1 Content-Level Hash Check (rclone)

Use `rclone check` to perform a fast, hash-based comparison. This ensures the data within the files is identical.

```bash
rclone check <source_path> <destination_path> --one-way --exclude .DS_Store -v
```

- `--one-way`: Check that everything in source exists and matches in destination.
- `--exclude .DS_Store`: Ignore macOS system noise.
- `-v`: Verbose output to capture matched/mismatched file counts.

### 2.2 Byte-by-Byte Structural Check (diff)

- **Byte-by-Byte Verification**: Run `diff -qr <source_path> <destination_path> -x ".DS_Store"`.
  This provides the ultimate structural assurance by decoding the following logic:
    - `-q`: **Brief mode**; only reports if files differ, without showing literal content deltas.
    - `-r`: **Recursive**; descends into all subdirectories for structural parity.
    - `-x ".DS_Store"`: **Exclude** macOS system noise to prevent false positives.

## 3. Discrepancy Resolution

- If **missing files** are found: List them and ask the user for synchronization intent.
- If **content mismatches** are found: Identify the specific file(s) and perform a
  `git diff` or `diff` on the files themselves to show the user the delta.
- **.DS_Store**: Always treat differences in `.DS_Store` as non-critical noise unless explicitly asked to verify them.

## 4. Reporting

The agent MUST provide a summary report:

1. Total files compared.
2. Number of matching files.
3. List of discrepancies (if any).
4. Tooling used for verification.

## 5. Related Skills

- [near-duplicate-file-comparison](../near-duplicate-file-comparison/SKILL.md)
  — when the comparison narrows to **two near-duplicate files** in the
  same directory (e.g. `Foo.java` vs `Foo_old.java`), switch to that
  skill's eight-dimension forensic rubric to decide which file is
  canonical and whether the duplicate can be deleted.
- [git-commit-comparison-audit](../git-commit-comparison-audit/SKILL.md)
  — when the comparison is between two commits rather than two
  directories.
- [archive-size-preflight-and-extract](../archive-size-preflight-and-extract/SKILL.md)
  — **upstream producer** — when one or both directories under comparison
  originated from an archive extraction, use that skill first to pre-flight
  disk-space cost, extract with verification, and confirm the byte count
  matches the archive's reported uncompressed size before running this
  folder comparison.
