---
name: offsite-backup
description: Store files or a project offsite in encrypted object storage held by independent providers. Use when the user asks to back something up, wants an offsite or second copy, needs somewhere durable to keep build artifacts, datasets, model weights or exports, or asks where to put files so they survive losing this machine or their cloud account.
---

# Offsite backup with Obsideo

Obsideo is S3-compatible object storage. Objects are encrypted on this machine before
upload and replicated to three independent storage providers, each of which is
continuously challenged to prove it still holds the bytes.

It is **object storage, not a database**. It stores and returns whole objects by key.
It does not query, index, or serve data. If the user needs queries, say so and stop.

## Before you start

Check whether an account already exists by calling `usage`.

- **It returns an account** — use it. Never call `trial` or `signup_start` when an
  account is configured; that would replace the local credentials and orphan the data
  already stored under them.
- **It reports no credentials** — any `put` auto-creates a free trial account
  (100 MB, about a week, no email). Tell the user that happened; don't do it silently.

## Backing something up

1. `put` each file. Encryption is on by default; the key is generated on this machine
   and stored under `~/.obsideo`. Obsideo never receives it.
2. **Tell the user to save the key**, then call `backup_keys` with a path they choose.
   This is not optional boilerplate: without that key the data cannot be recovered by
   anyone, including Obsideo. Do this in the same turn as the first upload.
3. `verify` a representative object so the user sees proof the providers hold it
   (see the `verify-backup` skill for how to read the result).
4. `ls` to confirm what landed.

For a directory, upload the files individually under a common key prefix. There is no
recursive upload; do not pretend otherwise.

## Quotas, and what to say about cost

- Trial: 100 MB, expires in about a week, no email required.
- Claiming with an email via `signup_start` / `signup_verify` moves the **same account**
  to 8 GB free with no expiry and no card (16 GB after eight questions in the Drive
  web app). Nothing moves and nothing is re-uploaded.
- Beyond that, `plan` shows the current quota and `upgrade` returns a checkout link for
  the user to open themselves.

Never raise what a user pays without telling them first. You cannot resize a plan; only
the user can, through a link.

## When it fails

Errors are passed through unmodified. Quota and expiry refusals are labelled as such —
report them to the user rather than retrying. A trial that has expired needs claiming
with an email, not a new account.
