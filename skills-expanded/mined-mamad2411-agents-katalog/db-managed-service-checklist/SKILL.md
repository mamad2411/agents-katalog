---
name: db-managed-service-checklist
category: migration
description: 매니지드 DB 서비스(RDS, Cloud SQL, Aurora 등)와 self-hosted/local DB의 차이를 점검하는 체크리스트. superuser 권한, schema, extension, 백업 정책 차이로 인한 마이그레이션 사고 방지.
---

# Managed DB Service Migration Checklist

self-hosted PostgreSQL / MySQL 에서 매니지드 서비스(AWS RDS, Cloud SQL, Aurora 등)로 이전하거나, dev/prod 간 DB 종류가 다를 때 적용하는 체크리스트.

> ⚠️ Java/ORM 환경에서 DB 자동 처리에 익숙해진 팀이 Go / 매니지드 환경에 진입할 때 가장 흔히 놓치는 영역. 권한/스키마 차이가 silent하게 실패한다.

---

## 카테고리별 체크리스트

### 1. Superuser / 권한 차이

매니지드 서비스의 "superuser"는 **OS-level superuser가 아니다**. 일부 명령은 차단된다.

| 환경 | "최상위" 권한 | 제약 |
|------|------------|------|
| Self-hosted PG | `postgres` (OS-level superuser) | 제약 없음 |
| AWS RDS PG | `rds_superuser` 멤버 | replication, file_fdw, plperlu 등 차단 |
| GCP Cloud SQL PG | `cloudsqlsuperuser` | 일부 extension 설치 / 파일 시스템 접근 차단 |
| Aurora PG | `rds_superuser` 변형 | RDS 와 유사 + Aurora 특화 차이 |

체크:
- [ ] 사용 중인 extension이 매니지드 서비스에서 허용되는가? (`pg_available_extensions` 확인)
- [ ] `COPY FROM/TO 'filepath'`(서버 파일) 사용 코드가 있는가? — 매니지드에서 차단
- [ ] `pg_read_server_files()`, `pg_ls_dir()` 등 file system 함수 사용 여부
- [ ] custom function with `LANGUAGE C` / `plperlu` 사용 여부

### 2. Schema / search_path 의존성

```sql
-- ❌ public schema 가정한 코드 (search_path 변경 시 깨짐)
SELECT * FROM users WHERE id = 1;

-- ✅ schema 명시
SELECT * FROM app.users WHERE id = 1;

-- ✅ 또는 startup에서 search_path 명시 설정
SET search_path TO app, public;
```

체크:
- [ ] 모든 query가 schema-qualified인가? 또는 startup에서 `search_path` 설정?
- [ ] migration tool (Flyway, Liquibase, golang-migrate) 의 default schema 설정 확인
- [ ] 다중 schema 사용 시 backup / restore 시 schema 누락 안 되는지

### 3. Extension 설치

| Extension | RDS | Cloud SQL | 비고 |
|-----------|-----|-----------|------|
| `uuid-ossp` | ✅ | ✅ | 일반적으로 OK |
| `pg_stat_statements` | ✅ (파라미터 그룹) | ✅ (flag) | 사용 전 활성화 필수 |
| `pgcrypto` | ✅ | ✅ | OK |
| `pg_trgm` | ✅ | ✅ | OK |
| `pg_repack` | ❌ | ❌ | online VACUUM 대체 필요 |
| `pglogical` | ✅ (제한) | ❌ | Cloud SQL은 native logical replication만 |
| `pg_partman` | ✅ | ❌ | 파티셔닝 자동화 차이 |

체크:
- [ ] `SELECT * FROM pg_available_extensions;` 로 매니지드 서비스 지원 목록 확인
- [ ] 미지원 extension의 대체 솔루션 확인

### 4. Connection / Pool 한도

매니지드 서비스는 instance type별 `max_connections` 한도가 있다.

| 서비스 | 기본값 | 조정 |
|--------|--------|------|
| RDS PG (db.t3.medium) | ~430 | 파라미터 그룹 |
| Cloud SQL PG (db-custom-1-3840) | 100 | flag (`max_connections`) |
| Aurora PG | instance type별 | 파라미터 그룹 |

체크:
- [ ] application pool size × replica 수 ≤ DB max_connections × 안전 계수(1.2)
- [ ] PgBouncer / RDS Proxy 도입 검토 (transaction-level pooling)
- [ ] 새 마이크로서비스 추가 시 connection budget 재계산

### 5. Timezone / Locale

- [ ] DB instance timezone (`SHOW TIMEZONE`) 명시 확인
- [ ] 애플리케이션 timezone과 일치하는가? (UTC 권장)
- [ ] `TIMESTAMP WITH TIME ZONE` vs `WITHOUT TIME ZONE` 일관성

### 6. Backup / PITR / Replication

| 기능 | RDS | Cloud SQL | Self-hosted |
|------|-----|-----------|-------------|
| 자동 백업 | ✅ (보존 1-35일) | ✅ (보존 1-365일) | pg_dump 스크립트 |
| PITR | ✅ | ✅ | WAL 아카이브 |
| Read replica | ✅ | ✅ | streaming replication 수동 |
| Cross-region replica | ✅ | ✅ (외부 read replica) | 수동 |

체크:
- [ ] PITR 보존 기간이 비즈니스 요구 (감사, 복구) 충족
- [ ] failover 시 application reconnect 로직 검증

### 7. SSL / TLS 강제

- [ ] 매니지드 서비스의 SSL 강제 여부 (Cloud SQL은 기본 강제 가능)
- [ ] connection string 에 `sslmode=require` 명시
- [ ] CA 인증서 다운로드 / 컨테이너 이미지에 포함

### 8. Migration tool 사용 시

```bash
# golang-migrate 예시 — 매니지드 서비스로 첫 마이그레이션 전 dry-run
migrate -path migrations -database "postgres://user:pass@host:5432/db?sslmode=require" up 1
```

체크:
- [ ] migration tool 의 lock 메커니즘이 매니지드에서 동작 (advisory lock 등)
- [ ] `CREATE EXTENSION` 명령은 별도 superuser 권한으로 실행
- [ ] schema migration 과 data migration 분리 (대용량 데이터는 별도)

---

## pg_restore / mysqldump 시 주의

```bash
# ❌ FK 순서 무시한 pg_restore — FK violation 다발
pg_restore -d target dump.sql

# ✅ FK 비활성 후 restore, 마지막에 활성화
pg_restore --disable-triggers -d target dump.sql

# 또는 schema → data 분리
pg_restore --schema-only -d target dump.sql
pg_restore --data-only --disable-triggers -d target dump.sql
```

체크:
- [ ] 큰 데이터셋 restore 시 single transaction 회피 (`--single-transaction` 안전성 vs 시간 trade-off)
- [ ] sequence 값이 max(id) 보다 크게 설정됐는가? (`SELECT setval(...)`)
- [ ] view / function / trigger 의 schema 의존성

---

## 실제 사고 패턴

| 사고 | 원인 | 방지 |
|------|------|------|
| Cloud SQL extension 설치 실패 | `cloudsqlsuperuser`로 일반 superuser 명령 시도 | 사전 지원 extension 확인 |
| metrics-collector 가 `public` schema 못 찾음 | search_path 가정 + Cloud SQL default 다름 | schema-qualified query 또는 명시 |
| replica 증가 후 connection refused | DB max_connections 한도 초과 | replica × pool ≤ max × 1.2 |
| timezone 오프셋 1시간 차이 | DB instance timezone Asia/Seoul + app UTC | UTC 통일 |
| SSL handshake 실패 | sslmode 누락 또는 CA 인증서 없음 | sslmode=require + CA 패키지 포함 |
| pg_restore 후 FK violation | --disable-triggers 누락 | FK 비활성 후 restore |

---

## Migration PR 자기 점검

DB 마이그레이션 / 신규 매니지드 서비스 도입 PR 작성 후:

- [ ] superuser 권한 차이 (extension, 시스템 함수) 검증
- [ ] schema / search_path 명시
- [ ] `max_connections` × pool 사전 계산
- [ ] timezone 통일 (UTC)
- [ ] SSL/TLS 강제 + CA 인증서
- [ ] migration tool lock 동작 확인
- [ ] backup / PITR 정책 확정
- [ ] failover 시 application 동작 검증
