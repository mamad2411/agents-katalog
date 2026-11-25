---
name: ackup
description: Backup System - Comprehensive backup for personal AI infrastructure. Backup files, docs, important thoughts, AI system, profile, and memory. Use when you need to backup your Obsidian vault, AI configuration, personal profile, or memory.
---

# Backup System Skill (/ackup)

Comprehensive backup solution for your Personal AI Infrastructure (PAI). Backup all important components including your Obsidian vault, AI system, personal profile, and memory.

## Quick Start

```bash
# Full backup of all components
python3 _scripts/backup_system.py

# List available backups
python3 _scripts/backup_system.py --list
```

## What It Backs Up

1. **Files** - Complete Obsidian vault contents
2. **Docs** - Important documents from Sources folder
3. **Important Thoughts** - Key notes from Atlas and Inbox
4. **AI System** - Scripts, configuration, and .claude folder
5. **Profile** - Personal information and profile data
6. **Memory** - Complete LLM context and memory system

## Options

- `--dir PATH`: Directory to store backups (default: ~/pai_backups)
- `--components [files docs thoughts ai-system profile memory]`: Specific components to backup (default: all)
- `--list`: List available backups
- `--save`: Save backup report to vault (Sources/Backup Report - YYYY-MM-DD.md)

## Examples

```bash
# Full backup with report saved
python3 _scripts/backup_system.py --save

# Backup specific components
python3 _scripts/backup_system.py --components files memory

# Use custom backup directory
python3 _scripts/backup_system.py --dir ~/custom_backups

# List all backups
python3 _scripts/backup_system.py --list

# List backups from custom directory
python3 _scripts/backup_system.py --dir ~/custom_backups --list
```

## Backup Structure

Backups are created as timestamped tar.gz archives:

```
~/pai_backups/
├── pai_backup_20260218_234200.tar.gz
├── pai_backup_20260217_183000.tar.gz
└── ...
```

Each backup contains:
- `vault/` - Complete Obsidian vault
- `docs/` - Important documents
- `thoughts/` - Key notes and insights
- `ai_system/` - AI scripts and configuration
- `profile/` - Personal profile information
- `memory/` - LLM context and memory

## Restore Instructions

To restore from a backup:

```bash
# Create temporary directory
mkdir -p /tmp/pai_restore
cd /tmp/pai_restore

# Extract backup
tar -xzf ~/pai_backups/pai_backup_20260218_234200.tar.gz

# Copy components back to vault as needed
```

## Why This Matters

- **Data Safety**: Protect your personal AI infrastructure from data loss
- **Version History**: Keep multiple timestamped backups
- **Selective Backup**: Choose which components to backup
- **Complete Coverage**: All important data is included in backups
- **Easy Restoration**: Simple to restore from any backup

## Output

- **Terminal**: Backup progress and summary report
- **Archive**: Tar.gz file in backup directory
- **Saved note**: (Optional) `Sources/Backup Report - YYYY-MM-DD.md`
