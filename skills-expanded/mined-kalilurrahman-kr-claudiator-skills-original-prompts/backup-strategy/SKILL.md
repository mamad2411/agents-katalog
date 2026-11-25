---
name: backup-strategy
description: Design backup and disaster recovery strategies with 3-2-1 rule, automated testing, and recovery procedures. Outputs backup schedules, retention policies, and RTO/RPO targets.
argument-hint: [data criticality, recovery time objectives, compliance requirements]
allowed-tools: Read, Write, Bash
---

# Backup & Disaster Recovery Strategy

Design reliable backup and recovery systems. Not "we back up daily" — tested recovery procedures, retention policies, and RTO/RPO SLAs.

## Process

1. **Classify data.** Critical, important, archival by recovery priority.
2. **Define RTO/RPO.** Recovery time objective, recovery point objective per system.
3. **Choose strategy.** Full, incremental, differential backups.
4. **Implement 3-2-1 rule.** 3 copies, 2 media types, 1 offsite.
5. **Automate backups.** Scheduled jobs, verification, alerts on failure.
6. **Test recovery.** Quarterly restore drills, document procedures.
7. **Monitor compliance.** Backup success rate, storage costs, retention adherence.

## Output Format

### Backup Strategy: [System Name]

**RTO:** 4 hours (must restore within 4 hours)  
**RPO:** 15 minutes (max data loss: 15 minutes)  
**Schedule:** Full weekly, incremental hourly  
**Retention:** 7 daily, 4 weekly, 12 monthly  
**3-2-1:** Disk + S3 Glacier + offsite datacenter

---

## RTO vs RPO

```
RTO (Recovery Time Objective): How fast must we recover?
- 1 hour: Mission-critical (payment processing)
- 4 hours: Business-critical (CRM, ERP)
- 24 hours: Important (analytics, reports)

RPO (Recovery Point Objective): How much data loss acceptable?
- 0 minutes: Zero data loss (synchronous replication)
- 15 minutes: Minimal loss (continuous backup)
- 24 hours: Daily snapshots acceptable
```

**Cost tradeoff:**
```
Lower RTO/RPO = Higher cost

RTO 1h + RPO 5min: Hot standby, real-time replication
RTO 4h + RPO 1h: Warm standby, hourly backups
RTO 24h + RPO 24h: Cold backups, daily snapshots
```

---

## 3-2-1 Backup Rule

```
3: Three copies of data
   - 1 production
   - 2 backups

2: Two different media types
   - Local disk
   - Cloud storage (S3, GCS)
   - Tape (long-term archival)

1: One copy offsite
   - Different datacenter
   - Different region
   - Different cloud provider

Prevents: Single point of failure, ransomware, regional disasters
```

---

## Backup Types

### Full Backup
```
Backs up: Everything
Frequency: Weekly
Restore time: Fastest (single file)
Storage: Highest
```

```bash
# Full PostgreSQL backup
pg_dump -h localhost -U postgres -F c mydb > /backups/full_$(date +%Y%m%d).dump

# Full directory backup
tar -czf /backups/app_$(date +%Y%m%d).tar.gz /var/www/app
```

### Incremental Backup
```
Backs up: Changes since last backup (full OR incremental)
Frequency: Hourly/daily
Restore time: Slower (need full + all incrementals)
Storage: Lowest
```

```bash
# rsync incremental
rsync -av --link-dest=/backups/latest /data/ /backups/$(date +%Y%m%d_%H%M%S)/
ln -snf /backups/$(date +%Y%m%d_%H%M%S) /backups/latest
```

### Differential Backup
```
Backs up: Changes since last FULL backup
Frequency: Daily
Restore time: Medium (need full + latest differential)
Storage: Medium
```

**Strategy comparison:**
```
Full weekly + Incremental hourly:
- Monday: Full (100GB)
- Tuesday-Sunday: Incremental (5GB each day)
- Total storage: 100GB + 6×5GB = 130GB/week

Full weekly + Differential daily:
- Monday: Full (100GB)
- Tuesday: Diff (5GB)
- Wednesday: Diff (10GB cumulative)
- Sunday: Diff (30GB cumulative)
- Total storage: 100GB + 30GB = 130GB/week
```

---

## Automated Backup Scripts

### PostgreSQL Backup
```bash
#!/bin/bash
# /usr/local/bin/backup-postgres.sh

set -e

DB_NAME="production"
BACKUP_DIR="/backups/postgres"
S3_BUCKET="s3://company-backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
pg_dump -h localhost -U postgres -F c $DB_NAME > $BACKUP_DIR/$DB_NAME_$DATE.dump

# Compress
gzip $BACKUP_DIR/$DB_NAME_$DATE.dump

# Upload to S3
aws s3 cp $BACKUP_DIR/$DB_NAME_$DATE.dump.gz $S3_BUCKET/postgres/

# Verify backup integrity
if ! gunzip -t $BACKUP_DIR/$DB_NAME_$DATE.dump.gz; then
    echo "Backup verification failed!" | mail -s "BACKUP FAILED" ops@company.com
    exit 1
fi

# Delete local backups older than 7 days
find $BACKUP_DIR -name "*.dump.gz" -mtime +7 -delete

# Delete S3 backups older than 30 days
aws s3 ls $S3_BUCKET/postgres/ | while read -r line; do
    createDate=$(echo $line|awk {'print $1" "$2'})
    createDate=$(date -d "$createDate" +%s)
    olderThan=$(date -d "30 days ago" +%s)
    if [[ $createDate -lt $olderThan ]]; then
        fileName=$(echo $line|awk {'print $4'})
        aws s3 rm $S3_BUCKET/postgres/$fileName
    fi
done

echo "Backup completed successfully: $DB_NAME_$DATE.dump.gz"
```

### MySQL Backup
```bash
#!/bin/bash
# Automated MySQL backup with rotation

MYSQL_USER="backup"
MYSQL_PASS="$(cat /etc/mysql/backup.password)"
BACKUP_DIR="/backups/mysql"

# Full backup on Sunday, incremental Monday-Saturday
DAY=$(date +%u)

if [ $DAY -eq 7 ]; then
    # Full backup
    mysqldump -u$MYSQL_USER -p$MYSQL_PASS --all-databases \
        --single-transaction --quick --lock-tables=false \
        > $BACKUP_DIR/full_$(date +%Y%m%d).sql
else
    # Incremental (binlog backup)
    mysql -u$MYSQL_USER -p$MYSQL_PASS -e "FLUSH LOGS;"
    cp /var/log/mysql/mysql-bin.* $BACKUP_DIR/incremental/$(date +%Y%m%d)/
fi
```

---

## Continuous Backup

### PostgreSQL WAL Archiving
```bash
# postgresql.conf
archive_mode = on
archive_command = 'test ! -f /mnt/archive/%f && cp %p /mnt/archive/%f'
wal_level = replica

# Backup WAL files to S3
#!/bin/bash
while inotifywait -e create /mnt/archive/; do
    for file in /mnt/archive/*; do
        aws s3 cp $file s3://backups/wal/
        rm $file
    done
done
```

**Point-in-Time Recovery (PITR):**
```bash
# Restore to specific timestamp
pg_basebackup -h primary -D /var/lib/postgresql/data -U replication -Fp -Xs -P

# recovery.conf
restore_command = 'aws s3 cp s3://backups/wal/%f %p'
recovery_target_time = '2024-03-22 10:30:00'
```

---

## Backup Verification

### Automated Restore Testing
```python
import subprocess
from datetime import datetime

def test_backup_restore(backup_file):
    """Test if backup can be restored"""
    
    try:
        # Create test database
        subprocess.run([
            'createdb', '-h', 'localhost', '-U', 'postgres', 'test_restore'
        ], check=True)
        
        # Restore backup
        subprocess.run([
            'pg_restore', '-h', 'localhost', '-U', 'postgres',
            '-d', 'test_restore', backup_file
        ], check=True)
        
        # Verify table count
        result = subprocess.run([
            'psql', '-h', 'localhost', '-U', 'postgres', 'test_restore',
            '-t', '-c', 'SELECT COUNT(*) FROM pg_tables WHERE schemaname=\'public\''
        ], capture_output=True, text=True)
        
        table_count = int(result.stdout.strip())
        
        # Drop test database
        subprocess.run([
            'dropdb', '-h', 'localhost', '-U', 'postgres', 'test_restore'
        ], check=True)
        
        if table_count > 0:
            print(f"✅ Backup valid: {backup_file} ({table_count} tables)")
            return True
        else:
            print(f"❌ Backup invalid: {backup_file} (no tables)")
            return False
    
    except Exception as e:
        print(f"❌ Restore failed: {backup_file} - {str(e)}")
        return False

# Test latest backup
latest_backup = '/backups/postgres/production_20240322.dump'
if not test_backup_restore(latest_backup):
    alert("Backup verification failed!")
```

---

## Retention Policies

### Grandfather-Father-Son (GFS)
```
Daily (Son): 7 backups (Monday-Sunday)
Weekly (Father): 4 backups (last 4 weeks)
Monthly (Grandfather): 12 backups (last 12 months)

Total: 7 + 4 + 12 = 23 backup files
```

```bash
#!/bin/bash
# GFS backup rotation

DAILY_RETENTION=7
WEEKLY_RETENTION=4
MONTHLY_RETENTION=12

DATE=$(date +%Y%m%d)
DAY=$(date +%u)  # 1-7 (Monday-Sunday)
DOM=$(date +%d)  # 01-31

# Daily backup
cp /data /backups/daily/backup_$DATE

# Promote to weekly (Sunday)
if [ $DAY -eq 7 ]; then
    cp /backups/daily/backup_$DATE /backups/weekly/
fi

# Promote to monthly (1st of month)
if [ $DOM -eq 01 ]; then
    cp /backups/daily/backup_$DATE /backups/monthly/
fi

# Delete old backups
find /backups/daily -mtime +$DAILY_RETENTION -delete
find /backups/weekly -mtime +$((WEEKLY_RETENTION * 7)) -delete
find /backups/monthly -mtime +$((MONTHLY_RETENTION * 30)) -delete
```

---

## Cloud Backup (AWS)

### S3 Lifecycle Policies
```json
{
  "Rules": [
    {
      "Id": "BackupRetention",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

**Cost optimization:**
```
S3 Standard: $0.023/GB/month (first 30 days)
S3 Standard-IA: $0.0125/GB/month (30-90 days)
S3 Glacier: $0.004/GB/month (90-365 days)
Deleted after 1 year

100GB backup:
Month 1: $2.30
Month 2-3: $1.25
Month 4-12: $0.40
Total year: $7.20 (vs $27.60 all Standard)
```

### AWS Backup
```python
import boto3

backup = boto3.client('backup')

# Create backup plan
response = backup.create_backup_plan(
    BackupPlan={
        'BackupPlanName': 'DailyBackups',
        'Rules': [
            {
                'RuleName': 'DailyRule',
                'TargetBackupVault': 'Default',
                'ScheduleExpression': 'cron(0 5 ? * * *)',  # 5 AM daily
                'StartWindowMinutes': 60,
                'CompletionWindowMinutes': 120,
                'Lifecycle': {
                    'DeleteAfterDays': 30,
                    'MoveToColdStorageAfterDays': 7
                }
            }
        ]
    }
)

# Assign resources to backup plan
backup.create_backup_selection(
    BackupPlanId=response['BackupPlanId'],
    BackupSelection={
        'SelectionName': 'ProductionDB',
        'IamRoleArn': 'arn:aws:iam::123456789:role/AWSBackupRole',
        'Resources': [
            'arn:aws:rds:us-east-1:123456789:db:production'
        ]
    }
)
```

---

## Disaster Recovery Procedures

### Recovery Runbook
```markdown
## Database Recovery Procedure

**RTO:** 4 hours  
**RPO:** 1 hour

### Steps

1. **Assess situation** (10 minutes)
   - Identify failure type (corruption, deletion, hardware)
   - Determine recovery point needed
   - Notify stakeholders

2. **Provision infrastructure** (30 minutes)
   - Launch new RDS instance OR
   - Repair existing instance

3. **Restore backup** (2 hours)
   ```bash
   # Download latest backup
   aws s3 cp s3://backups/postgres/latest.dump.gz /tmp/
   
   # Restore
   gunzip /tmp/latest.dump.gz
   pg_restore -h new-db -U postgres -d production /tmp/latest.dump
   ```

4. **Apply incremental changes** (1 hour)
   - Replay WAL logs from backup point to desired recovery time

5. **Verify data** (30 minutes)
   - Check row counts
   - Verify recent transactions
   - Run smoke tests

6. **Update application** (15 minutes)
   - Point app to restored database
   - Monitor error rates

7. **Document incident** (15 minutes)
   - What failed
   - What was lost
   - Lessons learned
```

---

## Monitoring

```python
from prometheus_client import Gauge, Counter

backup_age_hours = Gauge(
    'backup_age_hours',
    'Hours since last successful backup',
    ['database']
)

backup_size_bytes = Gauge(
    'backup_size_bytes',
    'Size of latest backup',
    ['database']
)

backup_success_total = Counter(
    'backup_success_total',
    'Total successful backups',
    ['database']
)

backup_failures_total = Counter(
    'backup_failures_total',
    'Total failed backups',
    ['database']
)

# Alert if backup age > 24 hours
alert: BackupStale
expr: backup_age_hours{database="production"} > 24
severity: critical
```

---

## Ransomware Protection

### Immutable Backups
```bash
# S3 Object Lock (WORM - Write Once Read Many)
aws s3api put-object-lock-configuration \
    --bucket company-backups \
    --object-lock-configuration \
    'ObjectLockEnabled=Enabled,Rule={DefaultRetention={Mode=GOVERNANCE,Days=30}}'

# Cannot be deleted or modified for 30 days, even by AWS root account
```

### Offline Backups
```bash
# Air-gapped backup - disconnected storage
# 1. Backup to external drive
rsync -av /data/ /mnt/external/backup/

# 2. Unmount and physically disconnect
umount /mnt/external

# 3. Store drive in secure location
# Ransomware cannot encrypt what it can't access
```

## Rules

- Test restores quarterly — untested backups are worthless.
- 3-2-1 rule minimum — single copy or single location = data loss risk.
- Automate verification — manual checks missed 100% of the time.
- Define RTO/RPO before choosing strategy — drives backup frequency and tooling.
- Retention matches compliance requirements — GDPR, HIPAA dictate minimum retention.
- Monitor backup age — alert if backup older than RPO.
- Encrypt backups at rest and in transit — stolen backup = data breach.
- Document recovery procedures — 3 AM recovery not time for guessing.
- Separate backup credentials from production — ransomware with prod access shouldn't reach backups.
- Calculate backup costs — 100GB daily × 365 days = storage bill surprises.
