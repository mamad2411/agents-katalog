---
name: dr-patterns
description: "Disaster recovery patterns: 3-2-1-1-0 backup architecture, pgBackRest configuration, Velero Kubernetes backups, cross-account AWS Backup, a DR runbook template, and a chaos testing plan. Use when implementing backups or writing and testing recovery procedures."
---

# DR Patterns

Disaster recovery patterns with Velero, pgBackRest, AWS Backup, chaos testing, and runbook templates.

## 3-2-1-1-0 Backup Architecture

```
Production Data
├── Copy 1: Live database (PostgreSQL primary)
├── Copy 2: WAL archive to S3 (same region, different AZ)
│   └── pgBackRest continuous WAL push to S3
├── Copy 3: Daily backup copy to S3 (DR region)
│   └── pgBackRest full backup replicated cross-region
└── Immutable copy: S3 Object Lock (WORM, 30-day compliance)

Recovery options:
- Point-in-time recovery: WAL replay to any second in the last 7 days
- Daily restore: Full backup from previous midnight
- DR failover: Restore from cross-region backup (~1-2hr RTO)
```

## pgBackRest Configuration

```ini
# /etc/pgbackrest/pgbackrest.conf on DB server
[global]
repo1-type=s3
repo1-s3-bucket=myapp-db-backups-prod
repo1-s3-region=us-east-1
repo1-s3-key=<access-key>          # Use IAM role instead
repo1-s3-key-secret=<secret-key>   # Use IAM role instead
repo1-path=/pgbackrest
repo1-retention-full=7             # Keep 7 full backups
repo1-retention-diff=14            # Keep 14 differential backups
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=<vault-secret>

# Cross-region DR repo
repo2-type=s3
repo2-s3-bucket=myapp-db-backups-dr
repo2-s3-region=us-west-2
repo2-path=/pgbackrest
repo2-retention-full=3

[global:archive-push]
compress-level=3

[main]
pg1-path=/var/lib/postgresql/15/main
pg1-user=postgres

# postgresql.conf additions
# archive_mode = on
# archive_command = 'pgbackrest --stanza=main archive-push %p'
# restore_command = 'pgbackrest --stanza=main archive-get %f "%p"'
# recovery_target_action = promote
```

```bash
# Backup operations
pgbackrest --stanza=main stanza-create
pgbackrest --stanza=main backup --type=full
pgbackrest --stanza=main backup --type=diff   # Incremental from last full
pgbackrest --stanza=main info                  # List backups

# Point-in-time restore to 14:30 UTC yesterday
pgbackrest --stanza=main restore \
  --target="2024-01-15 14:30:00+00" \
  --target-action=promote \
  --delta \
  --log-level-console=detail

# Verify backup integrity (no restore required)
pgbackrest --stanza=main check
pgbackrest --stanza=main verify
```

## Velero Kubernetes Backup

```bash
# Install Velero with AWS backend
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket myapp-k8s-backups \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1 \
  --secret-file ./velero-credentials

# Create on-demand backup
velero backup create prod-backup-$(date +%Y%m%d) \
  --include-namespaces production,monitoring \
  --wait

# Check backup status
velero backup describe prod-backup-20240115 --details

# Restore to different cluster
velero restore create \
  --from-backup prod-backup-20240115 \
  --include-namespaces production \
  --namespace-mappings production:production-restored
```

```yaml
# Velero backup schedule with pre-hook for PostgreSQL
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-production-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"
  template:
    includedNamespaces: ["production", "monitoring", "ingress-nginx"]
    excludedResources: ["events", "events.events.k8s.io", "nodes"]
    ttl: 720h0m0s
    storageLocation: default
    volumeSnapshotLocations: [default]
    hooks:
      resources:
        - name: postgres-quiesce
          includedNamespaces: [production]
          labelSelector:
            matchLabels: {app: postgres}
          pre:
            - exec:
                container: postgres
                command: ["/bin/bash", "-c", "psql -U postgres -c 'CHECKPOINT;'"]
                timeout: 30s
```

## AWS Backup Cross-Account Setup

```hcl
# terraform/backup.tf
resource "aws_backup_vault" "production" {
  name        = "production-vault"
  kms_key_arn = aws_kms_key.backup.arn

  tags = {
    Environment = "production"
  }
}

# Vault Lock prevents deletion (ransomware protection)
resource "aws_backup_vault_lock_configuration" "production" {
  backup_vault_name   = aws_backup_vault.production.name
  min_retention_days  = 7
  max_retention_days  = 90
  # changeable_for_days = 3  # Grace period before lock is final
}

resource "aws_backup_plan" "production" {
  name = "production-backup-plan"

  rule {
    rule_name         = "hourly-rds"
    target_vault_name = aws_backup_vault.production.name
    schedule          = "cron(0 * * * ? *)"

    lifecycle {
      cold_storage_after = 30
      delete_after       = 90
    }

    copy_action {
      destination_vault_arn = "arn:aws:backup:us-west-2:${var.account_id}:backup-vault:dr-vault"
      lifecycle {
        delete_after = 30
      }
    }
  }

  rule {
    rule_name         = "daily-full"
    target_vault_name = aws_backup_vault.production.name
    schedule          = "cron(0 3 * * ? *)"

    lifecycle {
      cold_storage_after = 7
      delete_after        = 365
    }
  }
}

resource "aws_backup_selection" "production_rds" {
  name         = "production-rds-databases"
  iam_role_arn = aws_iam_role.backup.arn
  plan_id      = aws_backup_plan.production.id

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "BackupPolicy"
    value = "production"
  }
}
```

## DR Runbook Template

```markdown
# DR Runbook: PostgreSQL Primary Failure

**Classification**: P1 - Critical
**RTO Target**: 30 minutes
**RPO Target**: 5 minutes (WAL archiving lag)
**Last Tested**: 2024-01-01
**Owner**: Platform Engineering

## Trigger Criteria
- PostgreSQL primary fails health checks for >2 consecutive minutes
- Replication lag exceeds 10 minutes on replica
- Primary host unreachable from application and monitoring

## Escalation
1. On-call engineer via PagerDuty (auto-page)
2. DBA lead: +1-XXX-XXX-XXXX
3. Engineering manager: +1-XXX-XXX-XXXX (if >15min)

## Recovery Steps

### Phase 1: Assess (0-5 min)
- [ ] Confirm primary is unreachable: `pg_isready -h db-primary.prod -p 5432`
- [ ] Check replication standby health: `pg_isready -h db-standby.prod -p 5432`
- [ ] View last WAL position on standby:
      `psql -h db-standby.prod -c "SELECT pg_last_wal_replay_lsn(), now() - pg_last_xact_replay_timestamp() AS lag;"`
- [ ] Check application error rates in Grafana (confirm DB is root cause)

### Phase 2: Failover (5-15 min)
- [ ] Promote standby to primary:
      `pg_ctl promote -D /var/lib/postgresql/15/main`
      OR `SELECT pg_promote();`
- [ ] Verify standby is now accepting writes:
      `psql -h db-standby.prod -c "SELECT pg_is_in_recovery();"  -- should return false`
- [ ] Update DNS CNAME: `db.prod.example.com` -> standby IP
      `aws route53 change-resource-record-sets --hosted-zone-id Z... --change-batch file://dns-failover.json`
- [ ] Verify application connects to new primary (check logs for connection errors)

### Phase 3: Verify (15-25 min)
- [ ] Run application smoke tests
- [ ] Confirm write operations succeed (create a test record)
- [ ] Check replication lag is now 0 (no replica yet)
- [ ] Notify stakeholders: "Database failover complete. Monitoring for stability."

### Phase 4: Stabilize (25-30 min)
- [ ] Begin provisioning new standby replica
- [ ] Update monitoring alerts with new primary endpoint
- [ ] Document exact timeline for postmortem

## Verification Commands
```bash
# Confirm new primary
psql -h db.prod.example.com -c "SELECT inet_server_addr(), pg_is_in_recovery();"

# Check write capability
psql -h db.prod.example.com -c "CREATE TABLE dr_test (t timestamp); DROP TABLE dr_test;"

# Confirm no data loss (compare with WAL archive)
pgbackrest --stanza=main check
```

## Rollback
If failover causes more issues: revert DNS to original primary (if recoverable), declare situation, escalate to DBA lead.

## Communication Template
```
[STATUS] Database failover in progress. We are promoting our standby database.
Impact: [describe]. ETA to resolution: 20 minutes.
Next update: [time].
```
```

## Chaos Testing Schedule

```yaml
# AWS FIS experiment: terminate 1 AZ of ECS tasks
resourceType: aws:ecs:task
selectionMode: PERCENT(33)
filters:
  - path: Tags.Environment
    values: [production]
actions:
  - stopTask
duration: PT5M

# Validation: service auto-healing within 5 minutes
# Alert: no customer-visible errors (check error rate dashboard)
# Success criteria: tasks back to desired count, latency normal
```

| Test Type | Frequency | What to Test |
|-----------|-----------|--------------|
| Backup restore | Monthly | Restore DB to test environment, verify row counts |
| Failover drill | Quarterly | Full region failover, measure actual RTO/RPO |
| AZ failure | Monthly | Terminate one AZ, verify auto-healing |
| Individual service | Weekly | Kill random pod/instance, verify recovery |
