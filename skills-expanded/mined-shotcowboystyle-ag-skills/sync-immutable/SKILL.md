---
name: sync-immutable
description: Use when verified evidence should be replicated to storage that cannot silently rewrite it — copies to the configured remote, confirms retention settings before writing, and re-verifies what landed. Triggers - "push evidence to immutable storage", "sync to object lock", "back up the evidence bundle".
allowed-tools: Bash(rclone *), Bash(aws *), Bash(command *), Bash(shasum *), Bash(date *), Bash(mkdir *), Read, Write
---

# Sync to Immutable Storage

Replicate verified evidence to the configured destination, then verify what actually
landed there.

## When to use

- After a batch has been logged, timestamped, and verified locally.
- After a bag has been created and validated.

## Inputs

- Path to replicate. Required.
- `--remote <name>` — destination. Defaults to `STORAGE_REMOTE` in `evidence/POLICY.md`.
- `--dry-run` — list what would transfer and change nothing.

## Procedure

### 1. Refuse to sync unverified content

Run verify-bundle over the source first, or confirm a verification from this session.
Replicating corrupted evidence into storage that cannot be rewritten makes the problem
permanent. If verification fails, stop.

### 2. Dry run first

```bash
rclone copy --dry-run "$SOURCE" "$REMOTE:$BUCKET/$PREFIX"
```

Show the user what would transfer, how many files, and how much data. Get agreement
before the real run — this writes to storage outside the machine and, under a retention
lock, cannot be undone.

### 3. Copy, never sync

```bash
rclone copy --checksum --progress "$SOURCE" "$REMOTE:$BUCKET/$PREFIX"
```

Use `copy`, not `sync`. `rclone sync` deletes destination files that are absent from the
source, which is exactly the wrong behaviour for an evidence archive. `--checksum`
compares hashes rather than size and timestamp.

### 4. Apply retention if the destination supports it

```bash
aws s3api put-object-retention \
  --bucket "$BUCKET" --key "$KEY" \
  --retention "Mode=COMPLIANCE,RetainUntilDate=$UNTIL"
```

State the mode and the exact retention date before applying it, and confirm. Compliance
mode cannot be shortened or lifted by anyone until it expires. A legal hold is the
alternative when the end date is not yet known — it has no expiry and is removed
explicitly.

### 5. Verify what landed

```bash
rclone check --checksum "$SOURCE" "$REMOTE:$BUCKET/$PREFIX"
```

This re-derives hashes at the destination rather than trusting the transfer report. If
the remote does not support the hash, say so and describe the check as weaker.

### 6. Record the transfer

Append to `chain-of-custody/` a record of what was replicated, where, when, under which
retention setting, and the result of the check. Note the file count and total size.

## Output

- Objects at the destination.
- A verification result from the destination side.
- A transfer record under `chain-of-custody/`.

## Notes

- Never delete the local copy on the strength of a successful upload. Confirm the
  destination is readable first, in a separate operation.
- Retention locks and credentials are separate concerns. A lock does not protect against
  a leaked key reading the data.
- Egress and retention both cost money. Say what a long retention on a large bundle
  commits the user to before applying it.
