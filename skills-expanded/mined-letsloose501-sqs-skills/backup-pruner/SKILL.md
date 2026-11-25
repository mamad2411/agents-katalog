---
name: backup-pruner
description: Keeps a backup folder to a fixed size by removing the oldest archives first. Use when the backup disk is filling up, when the user asks how many backups are kept, or when a retention policy has to be applied.
version: 2.1.0
---

# Backup pruner

1. List the archives in the folder the user named, oldest first.
2. Keep the newest seven daily and the newest four weekly archives.
3. Before removing anything, print the list and wait for the user to confirm.
4. Move the rest into `to-delete/` rather than deleting them.
