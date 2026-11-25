---
name: verify-backup
description: Check that an offsite or cold backup copy is actually still retrievable, by asking the storage providers to prove they hold the bytes. Use when the user asks whether a backup is still good, wants to audit or test a cold copy, doubts a provider really has their data, or asks how to check a backup without downloading it and paying egress.
---

# Verify a cold copy without retrieving it

The usual way to test a backup is to download it, which costs egress and time, so in
practice almost nobody tests theirs. Obsideo's `verify` tool asks each provider holding
an object to answer a fresh cryptographic challenge over the stored bytes. A provider
that no longer has them cannot answer.

This proves **possession of the bytes**, right now, by each provider. That is the whole
claim. It is not a proof that the object decrypts to what the user expects, and it is
not a guarantee about the future.

## Running a check

1. `ls` to list objects, or take the keys the user names.
2. `verify` each key of interest.
3. Report the result as **n of 3 providers proved possession**, not as a bare pass/fail.

## Reading the result

- **3 of 3** — replicated as intended, all three proved possession.
- **1–2 of 3** — the object is below its replication target. It is still retrievable, and
  the network heals under-replicated objects, but say plainly that redundancy is reduced.
- **0 of 3** — do not soften this. No provider proved possession. Tell the user directly
  and recommend they re-upload from source if they still have it.

If the user asks for a whole-account audit, verify a sample across prefixes rather than
every object; say how many you checked out of how many exist. Don't imply full coverage
from a sample.

## What to check after a restore matters

Possession proofs say the ciphertext is there. They say nothing about whether the user
still holds the **encryption key** — and without it the bytes are unrecoverable. When
auditing a backup, confirm the user knows where their key backup is (`backup_keys`
writes one). A verified object plus a lost key is still lost data, and that is worth
saying out loud.
