---
name: timestamp-evidence
description: Use when a file's existence at a point in time needs to be provable independently of the filesystem — anchors its hash with OpenTimestamps and stores the proof alongside the custody record. Triggers - "timestamp this evidence", "prove this existed today", "opentimestamps this file".
allowed-tools: Bash(ots *), Bash(command *), Bash(shasum *), Bash(cp *), Bash(mkdir *), Bash(date *), Read, Write
---

# Timestamp Evidence

Anchor a file's hash so its existence at a point in time can be shown without relying
on the filesystem, the operating system clock, or anyone's word.

## When to use

- Immediately after an item is logged, while the acquisition is fresh.
- Before handing a bundle to another party.
- Verifying or completing a proof taken earlier.

## Inputs

- Path to a file, or to an existing `.ots` proof. Required.
- `--verify` — check an existing proof instead of creating one.
- `--upgrade` — complete a pending proof once its attestation has landed.

## Procedure

### 1. Create a proof

```bash
ots stamp "$TARGET"
```

This writes `$TARGET.ots` next to the file. The proof commits to the file's hash, not
to its contents, so the file itself is never uploaded anywhere.

### 2. Explain the wait

A fresh proof is *incomplete*. It records a commitment to a calendar server and only
becomes independently verifiable once the Bitcoin attestation confirms, which takes
hours rather than minutes. Say this plainly at creation time — a proof that has not
been upgraded will fail verification, and that failure is expected, not an error.

### 3. Upgrade later

```bash
ots upgrade "$TARGET.ots"
```

Run this once the attestation has had time to land. On success the proof becomes
self-contained and no longer depends on the calendar server being reachable.

### 4. Verify

```bash
ots verify "$TARGET.ots"
```

Report the attested time exactly as the tool gives it, and state clearly what it means:
the file existed in this form no later than that time. It does not establish when the
file was created, who made it, or that its contents are true.

### 5. File the proof

```bash
mkdir -p chain-of-custody
cp -p "$TARGET.ots" chain-of-custody/
```

Keep the proof with the custody records rather than loose beside the evidence, and note
its path in the item's register record.

## Output

- A `.ots` proof beside the file and a copy under `chain-of-custody/`.
- For a verification, the attested time and an explicit statement of what it proves.

## Notes

- Only the hash leaves the machine. The file's contents are never transmitted.
- A proof is bound to exact bytes. Re-encoding, re-saving, or stripping metadata from
  the file invalidates it — timestamp the original, never a derived copy.
- Timestamping is not signing. It says when, not who. Pair it with a signature if
  authorship needs to be shown.
