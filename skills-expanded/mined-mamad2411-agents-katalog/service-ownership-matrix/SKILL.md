---
name: service-ownership-matrix
category: architecture
description: 책임 경계 불명확으로 인한 의사결정 정체·장애 미대응을 막는 RACI / Shared Responsibility Model 작성 가이드. "platform team" 같은 모호한 owner 표기를 금지하고 개인/직무 단위로 명시.
---

# Service Ownership Matrix (M2: 책임 경계 misunderstanding)

서비스/리소스/설정의 "owner" 가 불명확하면 장애 시 누가 결정·실행·통보·검증을 책임지는지 합의가 없어 **MTTR 이 폭증**한다. 클라우드 / 멀티팀 환경에서 가장 흔한 운영 안티패턴.

> Claude mental model 오류: "어차피 Cloudflare/AWS/플랫폼팀이 책임지지 않나" → 공유 책임 모델(Shared Responsibility) 의 경계가 정확히 어디인지, 사고 시 누가 buck 을 잡는지 명시 없으면 **모든 사람이 다른 사람을 기다린다**.

---

## RACI Matrix 기본

| 약자 | 의미 | 1개 리소스에 부여 가능 인원 |
|------|------|---------------------------|
| **R** Responsible | 실제 작업 수행 | 1명 이상 (반드시 존재) |
| **A** Accountable | 최종 의사결정·승인 | **반드시 1명** (다수 = 책임 회피) |
| **C** Consulted | 작업 전 의견 청취 (양방향) | N명 |
| **I** Informed | 결과 통보 (단방향) | N명 |

R 과 A 는 같은 인원이어도 무방하나, **A 는 항상 단일 인원**.

---

## ❌ 안티패턴: 팀 이름만 적힌 RACI

```
Service           | R              | A              | C        | I
DB schema change  | platform team  | platform team  | data eng | -
NetworkPolicy     | platform team  | platform team  | -        | -
Secret rotation   | platform team  | platform team  | -        | -
```

문제:
- "platform team" 안에 5명이 있다면 **누가** 책임지는지 불확정 → 모두 서로 기다림
- 야간/주말 on-call 매핑 불가
- 휴직/이직 시 인수인계 누락 (이름 없음)

---

## ✅ 권장: 개인 또는 직무 명시

```
Service           | R                       | A              | C              | I
DB schema change  | @alice (DB engineer)    | @bob (DBA lead)| @data-team    | #infra
NetworkPolicy     | @charlie (platform eng) | @bob (DBA lead)| @app-team     | #infra
Secret rotation   | @automation (CI bot)    | @bob (DBA lead)| -              | #security
```

원칙:
- A 는 **항상 1인의 사람 이름** (또는 role title 1개 + 현재 holder 명시)
- R 은 사람 또는 자동화 ID (`@automation`, `@argocd-bot` 등 명시적 식별자)
- C/I 는 채널 또는 그룹 OK (`#infra`, `@app-team`)
- holder 변경 시 같은 PR 에서 `OWNERS.md` 갱신

---

## Cloud Shared Responsibility Model (필수 점검 영역)

매니지드 서비스의 "공유 책임"은 layer 별로 분기된다. 모호한 영역에서 사고가 터진다.

### Kubernetes (EKS / GKE / AKS)

| Layer | 클라우드 | 고객 |
|-------|---------|------|
| Control plane (apiserver, etcd) | ✅ | - |
| Control plane patch | ✅ | minor 버전 결정·승인 |
| Node OS patch | ✅ (managed node group) | ❌ (self-managed node) |
| **node IAM / network policy** | - | **✅** |
| **workload RBAC, NetworkPolicy** | - | **✅** |
| **Secret encryption KMS** | - | **✅ key 선택** |

함정: "EKS 가 알아서 한다" → workload 단 NetworkPolicy / RBAC / PSP 는 **고객 책임**. OWASP K8s Top 10 의 대부분이 여기.

### Managed DB (RDS / Cloud SQL / Aurora)

| Layer | 클라우드 | 고객 |
|-------|---------|------|
| HW / OS / DB engine patch | ✅ | minor 버전 승인 |
| Backup 인프라 | ✅ | retention/PITR 정책 |
| **백업 검증 (실복원 테스트)** | ❌ | **✅** |
| **스키마 변경 / 마이그레이션** | - | **✅** |
| **권한·사용자 관리** | - | **✅** |
| **`COPY FROM 'file'` 등 OS 권한 명령** | ❌ (차단됨) | application code 수정 |

함정: "백업 자동이라 안전" → **실제 복원 검증**을 분기에 1회라도 안 하면 백업이 손상돼 있어도 모름.

### CDN / Edge (Cloudflare / CloudFront)

| Layer | 벤더 | 고객 |
|-------|------|------|
| TLS termination | ✅ | 인증서 발급/갱신 정책 |
| **Host 헤더 override** (Cloudflare Workers) | ✅ 자동 | application 에서 의존 금지 |
| **Route / Origin 매핑** | - | ✅ |
| Cache invalidation | API 제공 | 호출 책임 |

함정: Workers `fetch()` 가 자동으로 Host 를 override 한다 → 앱이 `request.headers.get('host')` 를 신뢰하면 라우팅 오류.

---

## 작성 절차 (1시간 워크숍 템플릿)

1. **리소스 인벤토리** (15분): 8~12개 핵심 리소스 나열 (DB, K8s, NetworkPolicy, Secret, IAM, CI, 모니터링 등)
2. **각 리소스에 R/A/C/I 부여** (30분): 1인당 A 가 ≥3개 면 위임 검토
3. **A 가 비어있거나 "팀명"인 row 적색 표시** (10분): 사고 전 반드시 해소
4. **OWNERS.md 커밋** (5분): 코드 옆에 저장, 변경 시 PR 리뷰

---

## 자가 검증 체크리스트

- [ ] 모든 row 에 **A 가 정확히 1인**인가?
- [ ] R/A 가 **개인 이름 또는 식별자**인가? ("팀명" 단독 금지)
- [ ] **공유 책임 모델**의 vendor / 고객 경계가 명시되었는가?
- [ ] holder 변경 시 OWNERS.md PR 리뷰 워크플로우가 있는가?
- [ ] 야간/주말 on-call 매핑이 OWNERS.md 의 A 와 일치하는가?
- [ ] 새 서비스 추가 PR template 에 OWNERS 항목이 포함되는가?

---

## 외부 근거

- [Create a RACI/RASCI matrix for cloud operating model — AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/create-a-raci-or-rasci-matrix-for-a-cloud-operating-model.html)
- [IT Roles & Responsibilities Matrix — Azure-Noob](https://azure-noob.com/blog/it-roles-responsibilities-matrix/) — "platform team ownership ambiguity" 사례
- [Shared Responsibility Model — AWS](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [Shared responsibility in the cloud — Microsoft](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility)

---

## 의외의 발견 (운영 사례 누적)

- **platform team ownership ambiguity** 가 가장 잦은 함정. "Cloud Team" 단일 표기로 의사결정이 정체된 사례 다수.
- **자동화 ID (`@bot`, `@argocd`) 도 R 로 명시** 해야 사후 추적 가능. "ArgoCD 가 했다"는 추적되지 않음 → ArgoCD Application 명 + 트리거한 PR 까지 함께 기록.
- M3 (config sprawl) 과 강하게 연결. ownership 부재 → 누가 어떤 config 를 owning 하는지 불분명 → drift 발생.
