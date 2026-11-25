---
name: init-evidence-store
description: Use when starting a new evidence collection or adding custody handling to an existing workspace — creates the evidence directory tree, an empty append-only register, and a written record of the hashing policy in force. Triggers - "start an evidence store", "set up chain of custody here", "create the evidence register".
allowed-tools: Bash(mkdir *), Bash(test *), Bash(touch *), Bash(find *), Read, Write
---

# Initialise Evidence Store

Create the directory tree and the empty append-only register that every other skill in
this pipeline reads and writes.

## When to use

- Starting a new evidence collection from nothing.
- Adding custody handling to a workspace that was provisioned for a matter but has no
  evidence subtree yet.

## Inputs

- Target directory. Defaults to the current working directory.
- Hashing policy. Defaults to SHA-256 only. BLAKE3 can be added as a second algorithm.

## Procedure

### 1. Refuse to clobber

```bash
test -e evidence/register.jsonl && echo "register already exists"
```

If a register already exists at the target, stop and report its path and record count.
Never truncate or recreate an existing register. Offer to operate on it instead.

### 2. Create the tree

```bash
mkdir -p evidence/originals evidence/derived manifests chain-of-custody logs
touch evidence/register.jsonl
```

Directory roles:

- `evidence/originals/` — acquisitions exactly as received. Read-only from here on.
- `evidence/derived/` — every copy that has been converted, unpacked, redacted, or
  re-rendered. Never mixed with originals.
- `manifests/` — hash manifests, one per ingest batch.
- `chain-of-custody/` — timestamp proofs, signatures, and transfer records.
- `logs/` — one log per operation, named `<operation>-<timestamp>.md`.

### 3. Record the policy

Write `evidence/POLICY.md` stating the facts later operations depend on, so they need
not be re-asked:

```
CASE_REF:
HASH_ALGOS: sha256
TIMESTAMPING: none | opentimestamps
CONFIDENTIALITY:
STORAGE_REMOTE:
```

Ask for the case reference and confidentiality level. Leave the rest at their defaults
until the relevant skill configures them.

### 4. Protect originals where the platform allows

Suggest, but do not silently apply, making `evidence/originals/` read-only once items
have been placed in it:

```bash
chmod -R a-w evidence/originals
```

This is advisory, not a security control. Say so.

## Output

- The directory tree above.
- An empty `evidence/register.jsonl`.
- `evidence/POLICY.md` with the answers given.

## Notes

- The tree may live at any depth inside a larger workspace. Other skills locate the
  register by searching, not by assuming a fixed path.
- Nothing here is specific to one operating system or one AI runtime.
