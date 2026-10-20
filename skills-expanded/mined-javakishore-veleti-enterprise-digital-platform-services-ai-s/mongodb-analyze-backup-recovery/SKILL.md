---
name: mongodb-analyze-backup-recovery
description: Analyze backup and recovery for self-managed MongoDB, including mongodump/mongorestore, filesystem or volume snapshots, replica-set and sharded-cluster consistency, oplog/PITR strategy, validation, and restore readiness. Use for DR planning or restore incidents.
---

# Analyze Backup and Recovery

1. Identify topology, RPO/RTO, data size, backup mechanism, and restore target.
2. Evaluate logical backups versus storage snapshots against consistency requirements.
3. For replica sets and sharded clusters, verify the backup method preserves a recoverable consistent state.
4. Inspect oplog/PITR dependencies where part of the design.
5. Require restore testing and validation, not backup-job success alone.
6. Do not restore over production data without explicit authorization.

## Output
- Backup Strategy
- Consistency/PITR Findings
- Restore Readiness
- RPO/RTO Risk
- Recommended Action
