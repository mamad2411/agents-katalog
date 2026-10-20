---
name: hash-file-verify
description: Compute and verify SHA-256 hash of a file for integrity checking
---

# File Hash Verification

Compute and verify SHA-256 hash of a file for integrity checking

## When to Use

- User wants to verify hash
- User wants to hash file
- Keywords: hash, sha256, verify, integrity

## Required Parameters

- **file_path** (string): Path to file
- **expected_hash** (string): Expected SHA-256 hash (optional)

## Output

- **hash** (string): Computed SHA-256 hash
- **match** (boolean): Whether hash matches expected
- **file_size** (number): File size in bytes

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `read_file` -> 7 steps -> Exit: `ret_match`, `ret_nomatch`, `ret_fail`
