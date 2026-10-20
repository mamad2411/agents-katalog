---
name: log-custody
description: Use when an item must enter the custody record — hashes it, captures who handed it over and how, copies the original into immutable storage under its own name, and appends one record to the append-only register. Triggers - "log this evidence", "add to the custody register", "record chain of custody for this file".
allowed-tools: Bash(shasum *), Bash(sha256sum *), Bash(b3sum *), Bash(command *), Bash(file *), Bash(stat *), Bash(exiftool *), Bash(cp *), Bash(mkdir *), Bash(date *), Bash(grep *), Bash(wc *), Read, Write
---

# Log Custody

Register an item in the append-only custody record. This is the pivot of the pipeline —
everything before it is acquisition, everything after it refers back to the record
written here.

## When to use

- Every time an item enters the collection, without exception.
- Recording a custody transfer or a correction to an earlier record.

## Inputs

- Path to the item. Required.
- Source, handler, custody notes, confidentiality. Asked for if not supplied.

## Procedure

### 1. Locate the register

Search upward from the working directory and downward from the workspace root for
`evidence/register.jsonl`. If none exists, say so and name the init-evidence-store
skill. Do not create a register as a side effect of logging.

### 2. Hash first, before anything else touches the file

```bash
shasum -a 256 "$TARGET"
```

If the policy in `evidence/POLICY.md` lists more algorithms, compute those too. Hash
the file where it currently sits, before any copy, so the digest describes what was
actually received.

### 3. Check for a duplicate

```bash
grep -F "$SHA256" evidence/register.jsonl
```

If the hash is already present, stop and report the matching record. Ask whether this
is a genuine re-receipt of the same item, a duplicate acquisition, or a mistake. Never
skip silently and never append without saying the duplicate exists.

### 4. Gather the facts the file cannot supply

```bash
file --mime-type -b "$TARGET"
stat -f '%z' "$TARGET"       # macOS
stat -c '%s' "$TARGET"       # GNU
date -u +%Y-%m-%dT%H:%M:%SZ
```

Then ask for what no command can determine:

- **Source** — who or what produced it, and how it reached the collection.
- **Handler** — who is logging it.
- **Custody notes** — the acquisition path, including any gap in the chain. A gap that
  is recorded is survivable; a gap that is hidden is not.
- **Confidentiality** — the handling level for this item.

Where metadata inspection has already run, carry a one-line summary and any anomaly
flags into the record rather than repeating the work.

### 5. Copy the original into place

```bash
mkdir -p evidence/originals
cp -p "$TARGET" "evidence/originals/$STAMPED_NAME"
```

`-p` preserves timestamps. Name the copy with an acquisition date prefix and a
filesystem-safe form of the original name; keep the original name verbatim in the
record. Never modify, re-encode, or strip metadata from this copy. Derived copies of
any kind belong in `evidence/derived/`.

### 6. Append one record

Append exactly one JSON object on one line. Never rewrite an earlier line. A correction
is a new record whose `supersedes` field names the id of the record it replaces.

```bash
printf '%s\n' "$RECORD_JSON" >> evidence/register.jsonl
```

### 7. Report

Give the record id, the SHA-256 in full, the stored path, and the new total record
count. Name any warning raised along the way.

## Output

- One new line in `evidence/register.jsonl`.
- One new file under `evidence/originals/`.
- A log entry under `logs/`.

## Notes

- JSON Lines is used because a single append is atomic and a partially written line is
  detectable. A rewritten JSON array is neither.
- Logging does not anchor the item in time. Use timestamp-evidence for that.
- If the file is still changing — an open document, a live capture — say so and log it
  only once it is final.
