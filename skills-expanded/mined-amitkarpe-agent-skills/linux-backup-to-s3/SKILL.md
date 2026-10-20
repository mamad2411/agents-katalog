---
name: linux-backup-to-s3
description: Set up and review encrypted Linux file backups to Amazon S3 using restic, AWS CLI profile-based credentials, least-privilege S3 buckets, restore tests, and safe retention. Use when Amit asks for Linux backup, S3 backup, restic backup, HDD-break recovery, restore drills, or backup cost/safety review.
---

# Linux Backup To S3

Use this skill for practical Linux workstation/server backups to S3 object storage.

## Default approach

- Prefer `restic` for Linux-to-S3 backup unless Amit asks for Borg or Kopia.
- Use Amazon S3 object storage, not S3 Files, for backup.
- Start with S3 Standard for simple restore; optimize to archive tiers only after restore tests work.
- Encrypt before upload using restic repository password.
- Keep secrets out of git. Store local secrets under `~/.config/restic/`.
- Keep scripts/runbooks in `dotfiles`; keep setup/test evidence under `~/.AGENTS-temp/<repo>/`.

## Safety rules

- Use AWS profile `amit` only when requested or when repo docs say so.
- Load `~/.codex/AWS.md` before creating or changing AWS resources.
- For backup buckets, require:
  - block public access
  - versioning enabled
  - server-side encryption enabled
  - meaningful tags
  - resource record in the owning repo/runbook
- Do not create AWS access keys unless Amit explicitly asks.
- Do not print restic passwords, AWS keys, or token material.
- Do not put `--delete` style mirror logic in the primary backup path.

## Recommended host layout

Tracked:

```text
~/dotfiles/backup/linux-backup-to-s3/
```

Local-only:

```text
~/.config/restic/linux-backup-to-s3/password
~/.config/restic/linux-backup-to-s3/env
~/.AGENTS-temp/dotfiles/linux-backup-to-s3/
```

## Setup workflow

1. Confirm AWS identity and region:

```bash
aws sts get-caller-identity --profile amit
aws configure get region --profile amit
```

2. Create or verify the S3 bucket.
3. Enable bucket versioning, encryption, block public access, and tags.
4. Install `restic` if missing.
5. Create the local restic password file with mode `0600`.
6. Run repository init once.
7. Run the first backup.
8. Run `restic snapshots` and a small restore test.

## Review workflow

When reviewing this setup:

- verify bucket state with `s3api get-bucket-versioning`, `get-public-access-block`, `get-bucket-encryption`, and `get-bucket-tagging`
- verify scripts with `bash -n`
- verify `restic snapshots` if restic and secrets exist
- verify restore with a temporary restore target under `~/.AGENTS-temp/<repo>/`
- report storage cost based on retained backup size, not source size

## Restore principle

The backup is only real after at least one restore test succeeds.

Minimum restore test:

```bash
restic restore latest --target ~/.AGENTS-temp/dotfiles/linux-backup-to-s3/restore-test
```

For full HDD-break recovery, restore to a fresh disk or temporary directory and confirm:

- git repos are present
- dotfiles are present
- Codex guidance and handoff files are present
- expected config files are present
