---
name: postgresql-operations
category: infrastructure
description: "PostgreSQL 운영 — postgresql.conf 파라미터 튜닝, EXPLAIN ANALYZE 쿼리 최적화, 잠금 진단, PgBouncer 커넥션 풀링, Percona Operator 기반 K8s 운영, 핵심 메트릭·알림. Use when PostgreSQL 성능이 떨어지거나 커넥션이 폭주할 때, K8s 위에서 PostgreSQL 을 운영할 때."
effort: xhigh
deprecated: false
---

# PostgreSQL 운영

성능 튜닝 · 커넥션 풀링 · K8s 운영. 인덱스 설계/N+1 같은 DB 일반론은 [`database`](../database/SKILL.md) 참조.

## Quick Reference (결정 트리)

```
증상은?
    │
    ├─ 특정 쿼리만 느림 ──────> EXPLAIN ANALYZE → 인덱스 (#쿼리-최적화)
    ├─ 전반적으로 느림 ───────> postgresql.conf 파라미터 (#핵심-파라미터)
    ├─ "too many connections" > PgBouncer (#connection-pooling-pgbouncer)
    ├─ 쿼리가 멈춤 ───────────> 잠금 모니터링 (#잠금-모니터링)
    └─ K8s 위 운영 ──────────> Percona Operator (#kubernetes-database-operations)
```

| DB | 강점 | 최적 사용 |
|----|------|----------|
| **PostgreSQL** | ACID, 복잡한 쿼리, JSON | 트랜잭션 중심, 분석 |
| **MySQL** | 읽기 성능, 단순 CRUD | 웹 애플리케이션 ([`mysql-operations`](../mysql-operations/SKILL.md)) |
| **Aurora** | Auto-scaling, 고가용성 | AWS 클라우드 네이티브 |

## PostgreSQL Performance Tuning

### 핵심 파라미터

```ini
# postgresql.conf

# 메모리 (총 RAM의 비율)
shared_buffers = 8GB              # RAM의 25% (32GB 서버 기준)
effective_cache_size = 24GB       # RAM의 75%
work_mem = 256MB                  # 쿼리당 정렬/해시 메모리
maintenance_work_mem = 2GB        # VACUUM, CREATE INDEX용

# 연결 관리 (PgBouncer 사용 시 낮게)
max_connections = 200             # 기본값, pooler 사용 시 100
superuser_reserved_connections = 3

# WAL 설정
wal_buffers = 256MB
checkpoint_completion_target = 0.9
max_wal_size = 4GB
min_wal_size = 1GB

# 병렬 쿼리 (PostgreSQL 17+)
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
parallel_tuple_cost = 0.01
parallel_setup_cost = 100

# I/O
effective_io_concurrency = 200    # SSD: 200, HDD: 2
random_page_cost = 1.1            # SSD: 1.1, HDD: 4.0
```

### 쿼리 최적화

```sql
-- 느린 쿼리 분석
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders
WHERE created_at > '2026-01-01'
AND status = 'pending';

-- 결과 해석
-- Seq Scan → 인덱스 필요
-- Nested Loop → 대량 데이터에서 비효율
-- Sort → work_mem 증가 또는 인덱스

-- 복합 인덱스 생성 (조건 순서 중요)
CREATE INDEX CONCURRENTLY idx_orders_status_created
ON orders (status, created_at DESC)
WHERE status IN ('pending', 'processing');

-- 통계 갱신
ANALYZE orders;

-- 인덱스 사용률 확인
SELECT
    indexrelname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

### 잠금 모니터링

```sql
-- 현재 잠금 대기 확인
SELECT
    blocked.pid AS blocked_pid,
    blocked.usename AS blocked_user,
    blocking.pid AS blocking_pid,
    blocking.usename AS blocking_user,
    blocked.query AS blocked_query
FROM pg_stat_activity blocked
JOIN pg_locks blocked_locks ON blocked.pid = blocked_locks.pid
JOIN pg_locks blocking_locks ON blocked_locks.locktype = blocking_locks.locktype
    AND blocked_locks.relation = blocking_locks.relation
    AND blocked_locks.pid != blocking_locks.pid
JOIN pg_stat_activity blocking ON blocking_locks.pid = blocking.pid
WHERE NOT blocked_locks.granted;

-- 오래 실행 중인 쿼리 종료
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
AND duration > interval '5 minutes';
```

---

## Connection Pooling (PgBouncer)

### 연결 문제 진단

```
연결 수 = (Database max_connections x 0.8) / App instances

예시:
- PostgreSQL max_connections = 200
- 앱 인스턴스 4개
- 인스턴스당 최대 40 connections
```

### PgBouncer 설정

```ini
# pgbouncer.ini

[databases]
mydb = host=postgres port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256

pool_mode = transaction          # session, transaction, statement
default_pool_size = 25           # DB당 기본 연결 수
min_pool_size = 5
reserve_pool_size = 5
max_client_conn = 1000

server_idle_timeout = 300
client_idle_timeout = 300
query_timeout = 30
```

### Kubernetes PgBouncer

```yaml
# bitnami/pgbouncer Deployment (replicas: 2)
# 핵심 env: POSTGRESQL_HOST, PGBOUNCER_POOL_MODE=transaction
# resources: 100m-500m CPU, 128Mi-256Mi Memory
# Percona Operator 사용 시 spec.proxy.pgBouncer로 자동 배포
```

---

## Kubernetes Database Operations

### PostgreSQL Operator (Percona)

```yaml
apiVersion: pgv2.percona.com/v2
kind: PerconaPGCluster
metadata:
  name: production-pg
spec:
  crVersion: 2.4.0
  instances:
    - name: primary
      replicas: 3
      dataVolumeClaimSpec:
        storageClassName: fast-nvme
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 500Gi
  proxy:
    pgBouncer:
      replicas: 2
      config:
        global:
          pool_mode: transaction
          default_pool_size: "50"
  backups:
    pgbackrest:
      repos:
        - name: repo1
          s3:
            bucket: pg-backups
            region: ap-northeast-2
          schedules:
            full: "0 1 * * 0"
            incremental: "0 1 * * 1-6"
  patroni:
    dynamicConfiguration:
      postgresql:
        parameters:
          shared_buffers: 8GB
          effective_cache_size: 24GB
          work_mem: 256MB
```

### 스토리지 선택

| 스토리지 유형 | TPS | 지연 | 사용 |
|--------------|-----|------|------|
| Local NVMe | 15,000+ | <5ms | 프로덕션 (고성능) |
| GP3 (AWS) | 5,000-8,000 | 10-20ms | 일반 프로덕션 |
| PD-SSD (GCP) | 5,000-10,000 | 10-15ms | 일반 프로덕션 |
| 네트워크 스토리지 | 1,000-3,000 | 20-50ms | 개발/테스트 |

---

## Monitoring

### PostgreSQL 핵심 메트릭

```promql
# 연결 사용률
pg_stat_activity_count / pg_settings_max_connections

# 캐시 히트율 (99% 이상 목표)
pg_stat_database_blks_hit /
(pg_stat_database_blks_hit + pg_stat_database_blks_read)

# 트랜잭션 처리량
rate(pg_stat_database_xact_commit[5m]) +
rate(pg_stat_database_xact_rollback[5m])

# 복제 지연 (바이트)
pg_replication_lag_bytes
```

### 알림 규칙

```yaml
groups:
  - name: postgresql-alerts
    rules:
      - alert: HighConnectionUsage
        expr: pg_stat_activity_count / pg_settings_max_connections > 0.8
        for: 5m
        labels:
          severity: warning
      - alert: LowCacheHitRatio
        expr: |
          pg_stat_database_blks_hit /
          (pg_stat_database_blks_hit + pg_stat_database_blks_read) < 0.95
        for: 15m
        labels:
          severity: warning
      - alert: ReplicationLag
        expr: pg_replication_lag_bytes > 100000000
        for: 5m
        labels:
          severity: critical
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| PgBouncer 미사용 | 연결 폭주, OOM | PgBouncer 필수 |
| SELECT * 사용 | 불필요한 I/O | 필요한 컬럼만 조회 |
| 인덱스 과다 | 쓰기 성능 저하 | 미사용 인덱스 제거 |
| VACUUM 방치 | Bloat, 성능 저하 | Autovacuum 튜닝 |
| 모니터링 부재 | 문제 조기 발견 불가 | pg_stat_* 활용 |

## Performance Targets

| 메트릭 | 목표 | 위험 |
|--------|------|------|
| 캐시 히트율 | > 99% | < 95% |
| 연결 사용률 | < 70% | > 85% |
| 복제 지연 | < 1MB | > 100MB |
| 쿼리 지연 (P99) | < 100ms | > 500ms |
| 트랜잭션/초 | 워크로드별 | 급격한 감소 |

---


## 참조 스킬

- [`database`](../database/SKILL.md) — 인덱스 설계 / N+1 / 쿼리 최적화 일반
- [`database-migration`](../database-migration/SKILL.md) — 스키마 마이그레이션 (Flyway / golang-migrate)
- [`expand-contract-pattern`](../expand-contract-pattern/SKILL.md) — 무중단 스키마 변경
- [`db-managed-service-checklist`](../db-managed-service-checklist/SKILL.md) — RDS / Cloud SQL 과 self-hosted 차이
- [`database-sharding`](../database-sharding/SKILL.md) — 수평 확장이 필요해진 시점
- [`mysql-operations`](../mysql-operations/SKILL.md) — MySQL/InnoDB 운영
