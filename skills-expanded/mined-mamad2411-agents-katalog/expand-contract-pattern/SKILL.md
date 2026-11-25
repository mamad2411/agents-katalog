---
name: expand-contract-pattern
category: migration
description: Zero-downtime DB schema migration을 위한 Expand-Contract (Parallel Change) 패턴. NOT NULL 컬럼 추가/컬럼명 변경/타입 변경을 3단계 PR로 분할. Atlas + Fowler bliki 기반.
---

# Expand-Contract Pattern (M8: Stateful 운영 가정 부재)

DB schema 를 **single PR 로 변경** 하면 application 과 schema 가 lockstep 으로 배포되어야 한다 → zero-downtime 불가능 + 롤백 시 데이터 손실 위험. Expand-Contract (Martin Fowler 의 Parallel Change) = 3단계로 분할해서 항상 양 버전 호환.

> Claude mental model 오류: "schema 변경은 그냥 ALTER TABLE 한 번이면 됨" → rolling update 중 old pod 는 old schema 기대 / new pod 는 new schema 기대 → 일시적 503 발생 + rollback 시 데이터 손실.

---

## 3-Phase 패턴

```
Phase 1: EXPAND
  → 새 컬럼 / 테이블을 NULLABLE 로 추가
  → application 은 두 path 모두 처리 (이중 write)
  → old reader 도 동작 (NULL 안전)

Phase 2: MIGRATE
  → backfill (배경 job 으로 기존 row 채움)
  → application 이 새 컬럼을 primary 로 read
  → old 컬럼은 mirror

Phase 3: CONTRACT
  → application 이 old 컬럼 미사용
  → old 컬럼 DROP
```

각 phase 는 **independent deploy + rollback 가능**.

---

## 사례 1: NOT NULL 컬럼 추가

### ❌ 단일 PR (Goti 안티패턴)

```sql
ALTER TABLE users ADD COLUMN phone_verified BOOLEAN NOT NULL DEFAULT FALSE;
```

문제:
- 대형 테이블 → `ALTER TABLE` 이 long lock → 운영 중 503
- old application code 는 `phone_verified` 컬럼을 모름 → INSERT 누락 → DEFAULT 적용 OK 지만 의도와 다름
- 롤백 시 컬럼은 그대로 남음

### ✅ Expand-Contract

**Phase 1 (Expand) — schema only**:
```sql
ALTER TABLE users ADD COLUMN phone_verified BOOLEAN;   -- NULLABLE
```

```java
// application 변경 없음 (column 사용 안 함)
```

**Phase 2 (Migrate) — application + backfill**:
```sql
-- 배경 job (배치 1만 row 단위)
UPDATE users SET phone_verified = FALSE WHERE phone_verified IS NULL;
```

```java
// application 코드: 새 컬럼 read/write
class User {
    Boolean phoneVerified;   // 기본 false
}
```

이중 write 의무: old code 는 INSERT 에 phone_verified 미포함 → DEFAULT FALSE (Phase 3 까지). 새 code 는 INSERT 에 명시.

**Phase 3 (Contract) — NOT NULL 강제**:
```sql
-- backfill 완료 확인 후
ALTER TABLE users ALTER COLUMN phone_verified SET DEFAULT FALSE;
ALTER TABLE users ALTER COLUMN phone_verified SET NOT NULL;
```

---

## 사례 2: 컬럼명 변경 (`email` → `email_address`)

**Phase 1 (Expand)**:
```sql
ALTER TABLE users ADD COLUMN email_address TEXT;
```

```java
// application: dual write
user.setEmail(email);          // old
user.setEmailAddress(email);   // new
```

**Phase 2 (Migrate)**:
```sql
UPDATE users SET email_address = email WHERE email_address IS NULL;
```

```java
// read 는 new 컬럼 우선
return user.getEmailAddress() != null ? user.getEmailAddress() : user.getEmail();
```

**Phase 3 (Contract)**:
```sql
ALTER TABLE users DROP COLUMN email;
```

```java
// dual write 제거
user.setEmailAddress(email);
```

---

## 사례 3: 컬럼 타입 변경 (`varchar(100)` → `varchar(255)`)

`varchar` 확대는 PG / MySQL 모두 lock-free (대부분) → 단순 ALTER 가능.

타입 변경 (e.g., `int` → `bigint`) 은:
- PG: in-place 변경 시 long lock → Expand-Contract 권장
- 새 컬럼 + dual write + backfill + drop

---

## Backfill 운영 원칙

```sql
-- ❌ 한 번에 다 UPDATE → long lock + WAL 폭증
UPDATE users SET phone_verified = FALSE WHERE phone_verified IS NULL;

-- ✅ 배치 + sleep
DO $$
DECLARE
    rows_updated INT;
BEGIN
    LOOP
        UPDATE users SET phone_verified = FALSE
        WHERE id IN (
            SELECT id FROM users WHERE phone_verified IS NULL LIMIT 1000
        );
        GET DIAGNOSTICS rows_updated = ROW_COUNT;
        EXIT WHEN rows_updated = 0;
        PERFORM pg_sleep(0.1);   -- replica lag 방지
    END LOOP;
END $$;
```

체크:
- batch size = 1000~10000 row (테이블 크기 / replica 영향에 따라)
- batch 사이 sleep (replica lag 모니터링)
- WAL 모니터링 (`pg_stat_replication`)
- index 가 backfill 후에 생성되면 더 빠름

---

## Rollback 안전성

| Phase | 롤백 시 데이터 손실? |
|-------|-------------------|
| Phase 1 (Expand) 후 application 배포 안 함 | ❌ (컬럼 추가만, 사용 안 함) |
| Phase 1 + application Phase 2 배포 | ❌ (dual write — old code 도 동작) |
| Phase 2 + application Phase 3 배포 | ❌ (new 컬럼 의존이지만 old code 는 default 값 사용) |
| Phase 3 DROP 후 | ⚠️ (old 컬럼 제거됨 — rollback 불가) |

→ Phase 3 DROP 은 **production 에서 충분히 burn-in 후** 실행.

---

## ❌ Schema migration 7대 죄

1. **NOT NULL + DEFAULT 없이 추가** → 기존 row insert 실패
2. **Long-running ALTER 를 운영 중 실행** → table lock
3. **단일 PR 에 schema + application 변경** → rollback 불가
4. **Backfill 없이 NOT NULL 강제** → 마이그레이션 실패
5. **DROP COLUMN 즉시 실행** → 모든 캐시된 query plan 무효화
6. **Replica lag 모니터링 없이 backfill** → read replica timeout
7. **Migration tool 의 transaction 가정** — PG DDL 은 transactional, MySQL DDL 은 implicit commit (rollback 불가)

---

## 자가 검증 체크리스트

DB schema migration PR 작성 시:

- [ ] **3 phase** 로 분할되었는가? (Expand / Migrate / Contract)
- [ ] 각 phase 가 **independent rollback** 가능한가?
- [ ] 새 컬럼이 **NULLABLE** 또는 **DEFAULT** 값을 가지는가?
- [ ] Backfill 이 **배치 + sleep** 으로 실행되는가?
- [ ] Application 코드가 **양 schema 동시 호환**인가? (dual read/write)
- [ ] `ALTER TABLE` 의 **lock mode** 를 확인했는가? (PG / MySQL 별 차이)
- [ ] Replica lag 모니터링이 backfill 중 살아있는가?
- [ ] DROP 전에 **production 에서 N일 burn-in** 했는가?

---

## 외부 근거

- [Parallel Change — Martin Fowler bliki](https://martinfowler.com/bliki/ParallelChange.html) — Expand-Contract 의 정식 명칭
- [The Hard Truth about GitOps and DB Rollbacks — Atlas blog](https://atlasgo.io/blog/2024/11/14/the-hard-truth-about-gitops-and-db-rollbacks)
- [How to Correctly Handle DB Schemas During Kubernetes Rollouts — Weave Works](https://www.weave.works/blog/how-to-correctly-handle-db-schemas-during-kubernetes-rollouts)
- [expand-contract-db-pattern (clnnn) — GitHub](https://github.com/clnnn/expand-contract-db-pattern)
- [Online schema migration tool — gh-ost (GitHub)](https://github.com/github/gh-ost) — MySQL 전용
- [pg_repack / pg_squeeze](https://github.com/reorg/pg_repack) — PG online 재구성

---

## 연계 skill

- [`migration/db-managed-service-checklist.md`](../db-managed-service-checklist/SKILL.md) — 매니지드 DB 권한 차이
- [`testing/negative-path-coverage.md`](../negative-path-coverage/SKILL.md) — backfill 중 timeout / replica lag
- [`architecture/config-explicit-defaults.md`](../config-explicit-defaults/SKILL.md) — schema migration 도 config 의 일부
