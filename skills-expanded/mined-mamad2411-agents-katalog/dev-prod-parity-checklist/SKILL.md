---
name: dev-prod-parity-checklist
category: platform
description: dev/staging/prod 환경 간 configuration drift와 snowflake environment 방지 체크리스트. 12-factor X + Beyond 12-factor 기반. 환경별 매니페스트 diff, 같은 base image, 같은 DB 종류 강제.
---

# Dev/Prod Parity Checklist (M7: 환경 차이 misforecasting)

"Terraform 으로 다 정의했으니 모든 환경이 같다" 는 가장 흔한 착각. 시간이 지나면 dev 와 prod 가 **silently drift** 해서 "dev 에서는 되는데 prod 에서 안 된다" 가 시작된다.

> Claude mental model 오류: "Terraform 코드가 같으면 환경이 같다" → 실제로는 cloud provider 차이 (AWS RDS vs GCP Cloud SQL), instance size 차이, manual config (Cloudflare 대시보드), secret manager 차이, IAM 차이 등이 누적되어 **각 환경이 unique snowflake** 가 된다.

---

## 6차원 Parity 점검

```
┌──────────────────────────────────────────────────┐
│ 1. Backing service (DB / Cache / MQ)             │
│ 2. Tooling (SDK / library / runtime version)     │
│ 3. Time gap (deploy 주기 차이)                   │
│ 4. Personnel (누가 manual 작업?)                 │
│ 5. Config (값 / 형식 / source)                   │
│ 6. Infra topology (NetPol / scaling / replica)   │
└──────────────────────────────────────────────────┘
```

각 차원 환경별 diff 가 없어야 한다.

---

## ❌ Snowflake Environment 5종

### Snowflake 1. Backing service 종류 다름

```
dev:   SQLite (in-memory)
prod:  Cloud SQL PostgreSQL 14
```

문제:
- dev 에서는 transaction 직렬화 / lock 차이
- migration SQL 이 prod 에서만 실패
- `JSONB` / `array` type 등 SQLite 미지원
- 권한 차이 (`cloudsqlsuperuser` ≠ `postgres`)

수정: dev 도 같은 매니지드 DB 사용 (또는 최소 Testcontainers 로 동일 image).

### Snowflake 2. Library 버전 mismatch

```
dev:   spring-boot:3.5.0 (개발자 로컬)
prod:  spring-boot:3.4.2 (Docker base image)
```

수정: **base image 고정** + monorepo `gradle-wrapper.properties` / `package-lock.json` 강제 + CI 에서 reproducible build.

### Snowflake 3. Manual config (IaC 밖)

가장 위험. Cloudflare 대시보드 / AWS 콘솔 / GCP 콘솔에서 수동 변경된 설정.

```
dev:   Cloudflare Workers 미사용
prod:  Cloudflare Workers 가 Host 헤더 override (대시보드에서 수동 설정)
```

수정: **manual-configs.md 명시 의무** + 수동 변경 시 같은 PR 에서 문서 갱신.

### Snowflake 4. IAM / 권한 차이

```
dev:   서비스 계정에 cloud-platform scope (강한 권한)
prod:  최소 scope (실제 운영 권한)
```

→ dev 에서는 모든 API 가 통과 → prod 에서 처음 실패. 수정: IAM policy 도 환경별 Terraform module + 같은 권한 set 으로 시작.

### Snowflake 5. Replica / scaling 차이

```
dev:   1 replica, no HPA
prod:  3-30 replica, HPA + PDB
```

문제:
- Rolling update 중 max 2배 부하 → dev 에서는 검증 안 됨
- session affinity 부재 시 dev 에서만 동작
- DB connection pool: 1 pod × 10 = 10 (dev), 30 pod × 10 = 300 (prod) → DB max_connections 초과

수정: **staging 환경에서 prod-like replica 로 테스트**.

---

## ✅ Parity 강화 5종 패턴

### Pattern 1. 환경별 매니페스트 diff 자동화

```bash
# CI 에서 매 PR 마다 환경 diff 출력
helm template -f values-dev.yaml chart/ > /tmp/dev.yaml
helm template -f values-prod.yaml chart/ > /tmp/prod.yaml
diff /tmp/dev.yaml /tmp/prod.yaml | grep -v '^[+-]+\?-\?$' > diff.txt
```

PR 리뷰어가 diff 를 본다. 의도 외 차이 = 즉시 fix.

### Pattern 2. Same base image, different config

```dockerfile
# dev / prod 모두 같은 Dockerfile
FROM eclipse-temurin:21-jre-alpine
COPY app.jar /app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

차이는 **env variable / ConfigMap** 으로만.

### Pattern 3. Testcontainers — local 도 prod 와 같은 backing service

```java
@Container
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:14")
    .withDatabaseName("test")
    .withUsername("test");
```

CI / 로컬 모두 같은 PG 버전.

### Pattern 4. Manual config 인벤토리 + 정기 reconciliation

`docs/architecture/manual-configs.md` 에 IaC 밖 설정 모두 기록:

```markdown
| 항목 | 위치 | 최종 수정 | Owner |
|---|---|---|---|
| Cloudflare Worker 라우팅 | Cloudflare 대시보드 | 2026-04-10 | @alice |
| Route53 NS delegation | AWS 콘솔 | 2026-03-01 | @bob |
```

분기 1회 reconciliation: 실제 설정 ↔ 문서 일치 확인.

### Pattern 5. Pre-prod = prod-like

staging 또는 pre-prod 환경에 prod 와 같은:
- replica 수 (최소 같은 비율)
- DB instance type
- IAM policy
- Network policy
- Manual config

→ prod 배포 전 staging 에서 24시간 burn-in.

---

## 자가 검증 체크리스트

신규 환경 생성 또는 환경별 변경 시:

- [ ] **Backing service 같은 종류** (DB / Cache / MQ engine + version)?
- [ ] **Same base image** + ConfigMap / env 로만 분기?
- [ ] **CI 에서 환경 diff** 가 매 PR 출력되고 리뷰되는가?
- [ ] **Manual config** 인벤토리가 최신인가? (분기 1회 reconciliation)
- [ ] **IAM policy** 가 환경별 같은 권한 set 으로 시작하는가? (최소 권한 원칙 유지)
- [ ] **Replica scaling** prod-like staging 환경이 있는가?
- [ ] **Library / runtime version** 이 reproducible 한가? (lockfile + base image 고정)
- [ ] 같은 PR 에서 dev / prod values 가 함께 갱신되는가? (drift 차단)

---

## 외부 근거

- [12factor.net X: Dev/prod parity](https://12factor.net/dev-prod-parity)
- [Beyond the Twelve-Factor App: Environment Parity — O'Reilly](https://www.oreilly.com/library/view/beyond-the-twelve-factor/9781492042631/ch09.html)
- [Deployment Environment Consistency — VegaStack](https://vegastack.com/blog/deployment-environment-consistency-dev-test-prod/) — "snowflake environment" 명명
- [Configuration Drift — HashiCorp glossary](https://www.hashicorp.com/resources/what-is-configuration-drift)

---

## 연계 skill

- [`architecture/config-explicit-defaults.md`](../config-explicit-defaults/SKILL.md) — config sprawl(M3) 이 환경별로 다르면 M7 (snowflake)
- [`kubernetes/multi-env-diff-checklist.md`](../multi-env-diff-checklist/SKILL.md) — 환경 diff 자동화 상세
- [`migration/db-managed-service-checklist.md`](../db-managed-service-checklist/SKILL.md) — managed DB 환경 차이

---

## 의외의 발견

- **M3 (config sprawl) → M7 (env sprawl) 인과 관계가 강함** — config 의 SoT 가 분산되면 환경별 drift 가 quasi-자동으로 발생
- 가장 효과적인 단일 조치: **CI 환경 diff 출력 + PR review 의무** (도구 무관, 효과 즉시)
- "manual config 가 0 인 인프라" 는 신화 — 인정하고 인벤토리로 관리하는 것이 현실적
