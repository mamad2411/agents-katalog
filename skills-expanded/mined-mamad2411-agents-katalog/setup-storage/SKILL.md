---
name: setup-storage
description: Use when configuring where evidence is replicated — walks through defining a storage remote, confirms its retention or write-once behaviour, and records the destination policy without ever touching credentials. Triggers - "set up evidence storage", "configure the rclone remote", "where should evidence be backed up".
allowed-tools: Bash(rclone *), Bash(aws *), Bash(command *), Bash(mkdir *), Read, Write
---

# Set Up Storage

Define where verified evidence is replicated, and confirm that the destination actually
resists rewriting before anything is trusted to it.

## When to use

- During onboarding, once the local pipeline works.
- Adding a second, independent destination.
- Auditing whether an existing destination really is immutable.

## Procedure

### 1. Choose the protection model

Ask which of these applies, because they fail differently:

- **Object storage with a retention lock** — S3 Object Lock or an equivalent. Objects
  cannot be deleted or overwritten until their retention expires. Requires versioning
  to be enabled on the bucket first.
- **Append-only or immutable-tier storage** — provider-enforced, no client cooperation
  needed.
- **Physical write-once media** — an optical disc or a WORM cartridge. Immutable by
  construction, offline by default, and slow to recover from.
- **An ordinary remote** — no protection at all. Usable as a second copy, but must not
  be described as immutable.

Be direct if the chosen destination provides no protection. An ordinary bucket with
careful habits is not immutable storage.

### 2. Define the remote

```bash
rclone config
rclone listremotes
```

`rclone` reads credentials from its own configuration or from the environment. Never
ask for a secret in conversation, never echo one, and never write one into the
workspace.

### 3. Confirm the bucket's actual settings

```bash
aws s3api get-bucket-versioning --bucket "$BUCKET"
aws s3api get-object-lock-configuration --bucket "$BUCKET"
```

Report what these return rather than what was intended. Object Lock cannot be enabled
on an existing bucket that was created without it, and versioning must be on for it to
work at all — check, do not assume.

Note which retention mode is configured. Governance mode can be bypassed by a
sufficiently privileged user; compliance mode cannot be bypassed by anyone, including
the account root, until retention expires. That difference is the whole point, and it
is also irreversible — say so before anyone chooses compliance mode.

### 4. Test with a throwaway object

Write a small file, read it back, then attempt to delete it. Under a working retention
lock the delete must fail. If it succeeds, the destination is not immutable, whatever
the configuration claims.

### 5. Record the policy

Write the destination, protection model, retention period, and the date of this test
into `evidence/POLICY.md` under `STORAGE_REMOTE`. Record the test result, not the
intention.

## Output

- A configured remote and a recorded destination policy.
- The result of an actual immutability test.

## Notes

- A retention lock protects against deletion, not against a bad object being written in
  the first place. Verify before syncing, not after.
- Retention periods cost money for their whole duration. State that before a long
  period is set.
- One copy in one region is not a backup. Prefer two destinations with different
  failure modes.
