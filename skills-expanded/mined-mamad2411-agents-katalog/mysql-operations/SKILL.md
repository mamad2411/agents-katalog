---
name: mysql-operations
category: infrastructure
description: "MySQL/InnoDB 운영 — buffer pool·redo log 등 InnoDB 파라미터 튜닝, EXPLAIN 쿼리 최적화, ProxySQL 커넥션 풀링과 읽기/쓰기 분리, Group Replication InnoDB Cluster HA, K8s 배포, 핵심 메트릭·알림. Use when MySQL 성능이 떨어지거나 읽기/쓰기 분리·HA 구성이 필요할 때."
effort: xhigh
deprecated: false
---

# MySQL / InnoDB 운영

InnoDB 튜닝 · ProxySQL · HA · K8s 운영. 인덱스 설계/N+1 같은 DB 일반론은 [`database`](../database/SKILL.md) 참조.

## Quick Reference (결정 트리)

```
증상은?
    │
    ├─ 특정 쿼리만 느림 ──────> EXPLAIN → 인덱스 (#쿼리-최적화)
    ├─ 전반적으로 느림 ───────> InnoDB buffer pool (#innodb-튜닝)
    ├─ 연결 폭주 ────────────> ProxySQL (#proxysql)
    ├─ 읽기 부하 분산 필요 ───> ProxySQL 쿼리 룰 (#proxysql)
    └─ HA 필요 ──────────────> Group Replication / InnoDB Cluster (#mysql-high-availability)
```

## MySQL Optimization

### InnoDB 튜닝

```ini
# my.cnf

[mysqld]
# Buffer Pool (RAM의 70-80%)
innodb_buffer_pool_size = 24G
innodb_buffer_pool_instances = 8

# 로그 설정
innodb_log_file_size = 2G
innodb_log_buffer_size = 256M
innodb_flush_log_at_trx_commit = 1  # 1=ACID, 2=성능

# I/O
innodb_io_capacity = 2000          # SSD
innodb_io_capacity_max = 4000
innodb_read_io_threads = 8
innodb_write_io_threads = 8

# 연결
max_connections = 500
thread_cache_size = 50

# 쿼리 캐시 (MySQL 8.0에서 제거됨)
# query_cache_type = 0
```

### 쿼리 최적화

```sql
-- 느린 쿼리 분석
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE created_at > '2026-01-01'
AND status = 'pending';

-- 결과 해석
-- type=ALL → 풀 테이블 스캔, 인덱스 필요
-- type=ref → 인덱스 사용 중 (양호)
-- Using filesort → ORDER BY 인덱스 최적화 필요

-- 복합 인덱스 생성
ALTER TABLE orders ADD INDEX idx_status_created (status, created_at DESC);

-- 인덱스 사용 통계 확인
SELECT
    object_schema,
    object_name,
    index_name,
    count_star AS total_access
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE object_schema = 'mydb'
ORDER BY count_star DESC;

-- InnoDB Buffer Pool 히트율 확인
SELECT
    (1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)) * 100
    AS buffer_pool_hit_rate
FROM (
    SELECT
        VARIABLE_VALUE AS Innodb_buffer_pool_reads
    FROM performance_schema.global_status
    WHERE VARIABLE_NAME = 'Innodb_buffer_pool_reads'
) r,
(
    SELECT
        VARIABLE_VALUE AS Innodb_buffer_pool_read_requests
    FROM performance_schema.global_status
    WHERE VARIABLE_NAME = 'Innodb_buffer_pool_read_requests'
) rr;
```

---

## ProxySQL

### 설정

```sql
-- ProxySQL Admin에서 실행

-- 백엔드 서버 추가
INSERT INTO mysql_servers (hostgroup_id, hostname, port)
VALUES
    (10, 'mysql-primary', 3306),
    (20, 'mysql-replica-1', 3306),
    (20, 'mysql-replica-2', 3306);

-- 읽기/쓰기 분리 규칙
INSERT INTO mysql_query_rules (rule_id, active, match_pattern, destination_hostgroup)
VALUES
    (1, 1, '^SELECT .* FOR UPDATE', 10),   -- 쓰기 그룹
    (2, 1, '^SELECT', 20);                  -- 읽기 그룹

-- 연결 풀 설정
UPDATE mysql_servers SET max_connections = 100;

LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
```

### Kubernetes ProxySQL 배포

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: proxysql
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: proxysql
          image: proxysql/proxysql:latest
          ports:
            - containerPort: 6033
              name: mysql
            - containerPort: 6032
              name: admin
          resources:
            requests:
              cpu: "200m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
```

---

## MySQL High Availability

### InnoDB Cluster (Group Replication)

```sql
-- MySQL Shell로 클러스터 생성
-- mysqlsh root@mysql-primary

-- 클러스터 생성
var cluster = dba.createCluster('production', {
    memberSslMode: 'REQUIRED',
    exitStateAction: 'READ_ONLY',
    autoRejoinTries: 3
});

-- 멤버 추가
cluster.addInstance('root@mysql-secondary-1:3306');
cluster.addInstance('root@mysql-secondary-2:3306');

-- 클러스터 상태 확인
cluster.status();
```

### my.cnf HA 설정

```ini
[mysqld]
# Group Replication
plugin_load_add = 'group_replication.so'
group_replication_group_name = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
group_replication_start_on_boot = OFF
group_replication_member_weight = 50
group_replication_consistency = BEFORE_ON_PRIMARY_FAILOVER

# GTID (필수)
gtid_mode = ON
enforce_gtid_consistency = ON
binlog_format = ROW
log_slave_updates = ON

# Crash Safety
relay_log_info_repository = TABLE
relay_log_recovery = ON
```

---

## Monitoring

### MySQL 핵심 메트릭

```promql
# InnoDB Buffer Pool 히트율 (99% 이상 목표)
mysql_global_status_innodb_buffer_pool_read_requests /
(mysql_global_status_innodb_buffer_pool_read_requests +
 mysql_global_status_innodb_buffer_pool_reads)

# 연결 사용률
mysql_global_status_threads_connected / mysql_global_variables_max_connections

# 쿼리 처리량
rate(mysql_global_status_queries[5m])

# Replication 지연 (초)
mysql_slave_status_seconds_behind_master
```

### 알림 규칙

```yaml
groups:
  - name: mysql-alerts
    rules:
      - alert: MySQLHighConnectionUsage
        expr: mysql_global_status_threads_connected / mysql_global_variables_max_connections > 0.8
        for: 5m
        labels:
          severity: warning
      - alert: MySQLLowBufferPoolHitRate
        expr: |
          mysql_global_status_innodb_buffer_pool_read_requests /
          (mysql_global_status_innodb_buffer_pool_read_requests +
           mysql_global_status_innodb_buffer_pool_reads) < 0.95
        for: 15m
        labels:
          severity: warning
      - alert: MySQLReplicationLag
        expr: mysql_slave_status_seconds_behind_master > 30
        for: 5m
        labels:
          severity: critical
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| ProxySQL 미사용 | 연결 폭주, 읽기/쓰기 분리 불가 | ProxySQL 도입 |
| Buffer Pool 부족 | 디스크 I/O 과다 | RAM의 70-80%로 설정 |
| GTID 미사용 | Failover 복구 어려움 | GTID 활성화 |
| SELECT * 사용 | 불필요한 I/O | 필요한 컬럼만 조회 |
| 바이너리 로그 미설정 | 복구/복제 불가 | binlog_format=ROW |

## Performance Targets

| 메트릭 | 목표 | 위험 |
|--------|------|------|
| Buffer Pool 히트율 | > 99% | < 95% |
| 연결 사용률 | < 70% | > 85% |
| Replication 지연 | < 1s | > 30s |
| 쿼리 지연 (P99) | < 100ms | > 500ms |
| QPS | 워크로드별 | 급격한 감소 |

---


## 참조 스킬

- [`database`](../database/SKILL.md) — 인덱스 설계 / N+1 / 쿼리 최적화 일반
- [`database-migration`](../database-migration/SKILL.md) — 스키마 마이그레이션
- [`expand-contract-pattern`](../expand-contract-pattern/SKILL.md) — 무중단 스키마 변경
- [`db-managed-service-checklist`](../db-managed-service-checklist/SKILL.md) — RDS / Cloud SQL 과 self-hosted 차이
- [`database-sharding`](../database-sharding/SKILL.md) — Vitess 기반 수평 확장
- [`postgresql-operations`](../postgresql-operations/SKILL.md) — PostgreSQL 운영
