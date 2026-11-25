---
name: postgres-analyze-backup-pitr
description: Analyze Azure PostgreSQL Flexible Server automated backups, retention, point-in-time restore, geo-redundant backup where configured, recovery objectives, and restore readiness. Use for backup architecture or recovery incidents.
---

# Analyze Backup and PITR

1. Identify backup retention, redundancy configuration, RPO/RTO, and restore target requirements.
2. Inspect available restore window and relevant backup state.
3. Evaluate regional recovery requirements and configured redundancy.
4. Require restore validation rather than treating backup status alone as proof of recoverability.
5. Distinguish PITR from logical export/import requirements.
6. Do not restore over production without explicit authorization.

## Output
- Backup Configuration
- Restore Window
- Regional Recovery
- RPO/RTO Gaps
- Recommended Action
