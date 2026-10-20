---
name: verify-bundle
description: Use when integrity must be confirmed rather than assumed — recomputes every hash, validates bags and timestamp proofs, and reports an explicit pass or fail naming each diverging file. Triggers - "verify this evidence", "has anything changed", "check the bag is still valid".
allowed-tools: Bash(shasum *), Bash(sha256sum *), Bash(b3sum *), Bash(bagit.py *), Bash(ots *), Bash(command *), Bash(find *), Bash(mkdir *), Bash(date *), Read, Write
---

# Verify Bundle

Recompute what was recorded and report an explicit pass or fail. This skill asserts
nothing it did not check in this run.

## When to use

- Before packaging, handover, or replication.
- After moving or restoring evidence from storage.
- On a schedule, to detect silent corruption early.

## Inputs

- Path to a file, directory, manifest, or bag. Defaults to the working directory.

## Procedure

### 1. Work out what is being verified

Detect the target type and use the matching check. A directory may need more than one:

- A register at `evidence/register.jsonl` — recompute each recorded item's hash.
- A `.sha256` or `.blake3` manifest — check every entry.
- A directory containing `bagit.txt` — validate the bag.
- Any `.ots` proofs found — verify each.

### 2. Check a manifest

```bash
shasum -a 256 -c manifests/batch.sha256
```

On GNU systems the equivalent is `sha256sum -c`. Both print `OK` or `FAILED` per line
and exit non-zero if any entry failed. Capture the exit status; do not judge by eye.

### 3. Check the register

For every record, recompute the hash of the file at its recorded path and compare with
the recorded digest. Three distinct outcomes, all of which must be reported separately:

- **Match** — the item is intact.
- **Mismatch** — the file at that path is no longer the file that was logged.
- **Missing** — the recorded path does not resolve.

A mismatch and a missing file are different problems. Collapsing them into one count
hides which one happened.

### 4. Validate bags

```bash
bagit.py --validate "$BAG_DIR"
```

### 5. Verify timestamp proofs

```bash
ots verify "$PROOF"
```

Distinguish three results: verified, pending upgrade, and failed. A pending proof is
not a failure — it means the attestation has not landed yet.

### 6. Report

Lead with `PASS` or `FAIL`. Then give counts by outcome, and name every file that
mismatched or went missing, one per line, with its recorded and recomputed digest. A
summary without the file names is not usable.

Write the full result to `logs/verify-<timestamp>.md` so the check itself is on the
record.

### 7. Stop on failure

Do not continue into packaging, syncing, or export after a FAIL. Report and wait.

## Output

- A pass or fail verdict with per-file detail.
- A log file under `logs/`.

## Notes

- Verification proves the bytes are unchanged since they were recorded. It cannot show
  the bytes were correct when first recorded.
- Run it against storage that was written elsewhere, not only against the local copy —
  a local check cannot detect corruption that happened during replication.
