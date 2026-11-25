---
name: restic-backup
description: Fast and secure file backups with Restic
version: 1.0.0
tags: [backup, security, encryption, storage]
---

# Restic – Encrypted Backup Tool

Restic is a fast, secure, and efficient backup program supporting
multiple storage backends with built-in encryption and deduplication.

- **GitHub**: github.com/restic/restic (28 000+ ⭐)
- **License**: BSD-2-Clause
- **Security**: AES-256 encryption. Data integrity verification. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{RESTIC_REPOSITORY}}` | Backup repository location (local, S3, SFTP, etc.) |
| `{{RESTIC_PASSWORD}}` | Repository encryption password |

## Usage Examples

### Initialise a repository

```bash
restic init --repo {{RESTIC_REPOSITORY}}
```

### Create a backup

```bash
restic backup --repo {{RESTIC_REPOSITORY}} /data/important
```

### List snapshots

```bash
restic snapshots --repo {{RESTIC_REPOSITORY}}
```

### Restore from backup

```bash
restic restore latest --repo {{RESTIC_REPOSITORY}} --target /restore
```

## AI Agent Tips

- All data is encrypted and deduplicated automatically.
- Supports S3, GCS, Azure, SFTP, REST, and local backends.
- Incremental backups are fast — only changed blocks are stored.
- Use `restic check` to verify repository integrity regularly.
