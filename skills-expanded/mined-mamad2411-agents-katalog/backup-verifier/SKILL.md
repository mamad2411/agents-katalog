---
name: backup-verifier
description: Verify that server backups are working correctly. Checks backup timer status, last run, rclone remote health, and optionally restores latest SQLite backups to verify integrity. Use when the user says "check backups", "are backups working", "verify backup", "when was the last backup", "test restore", or invokes /verify-backup. Also trigger proactively when backup-related issues are suspected.
allowed-tools: [Bash, Read, Grep]
---

# /verify-backup

Verify the newna.ai daily backup pipeline is working correctly.

## Backup System

- **Script:** `/home/sabro/scripts/server-backup.sh`
- **Schedule:** Daily at 03:00 UTC (systemd timer: `server-backup.timer`)
- **Destination:** Google Drive via rclone
- **Contents:** System configs, SQLite databases, project files, Docker volumes

## Verification Steps

### 1. Timer status
```bash
systemctl status server-backup.timer --no-pager
systemctl list-timers server-backup.timer --no-pager
```
Confirm the timer is active and shows next/last trigger times.

### 2. Last run result
```bash
journalctl -u server-backup.service --since "48 hours ago" --no-pager -n 20
```
Check for errors, completion status, duration.

### 3. Rclone remote health
```bash
rclone lsd gdrive: 2>/dev/null | head -5
```
Verify the rclone remote is reachable.

### 4. Latest backup files
```bash
rclone ls gdrive:server-backups/ --max-depth 1 2>/dev/null | sort -k2 | tail -10
```
Check that recent backup files exist and have reasonable sizes.

### 5. Test restore (ask user first)

This step restores the latest SQLite backup to a temp directory and runs integrity checks. It does NOT touch production databases.

```bash
TEMP_DIR=$(mktemp -d)
# Copy latest backup from rclone
rclone copy gdrive:server-backups/latest/admin.db "$TEMP_DIR/" 2>/dev/null
# Test integrity
sqlite3 "$TEMP_DIR/admin.db" "PRAGMA integrity_check;" 2>/dev/null
# Clean up
rm -rf "$TEMP_DIR"
```

### 6. Report

- Timer: active/inactive, last trigger, next trigger
- Last run: success/failure, duration, errors
- Remote: reachable/unreachable
- Latest files: count, most recent date, total size
- Test restore: integrity pass/fail (if run)
