---
name: file-backup
description: Backup before modification. Trigger: backup, copy, save original, .bak, snapshot.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\scripts\software_cracker.py
x-alice-class: reverse
---# file-backup

## Trigger
`backup, copy, save original, `

## Flow
```
cp $TARGET $TARGET.bak -> sha256 verify
```

## Script
`scripts/file_backup.py`
