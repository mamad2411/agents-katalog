---
name: data-subject-rights
category: legal
description: 데이터 주체 권리(DSR) 운영 자동화 — 열람·정정·삭제·이동·처리정지·거부·자동결정거부, 본인 인증, 데이터 카탈로그, 백업/Kafka/캐시/검색 전파, Event Sourcing crypto-shredding, 외부 수탁자 통지. PIPA(KR 10일) + 위치정보법 + GDPR(30일) + CCPA(45일) 통합.
license: MIT
---

# Data Subject Rights — DSR 자동화 운영

데이터 주체(이용자)의 권리 행사를 자동화하는 운영 hub. 한국 PIPA 제35~38조 + 위치정보법 제24~25조 + GDPR Articles 15~22 + CCPA를 통합 처리한다. 멀티 리전 SaaS는 가장 짧은 SLA(KR 10일)에 맞춰 운영하면 자동으로 GDPR/CCPA도 충족된다.

> 이 skill은 DSR 운영 hub. 위치정보 결합은 `legal/kr-location-info-act.md`, 미성년 자녀 권리를 부모가 행사하는 케이스는 `legal/child-data-protection.md` §4. 동의·철회 자체 흐름은 `legal/kr-location-info-act.md` §3.

## When to Use

- 사용자 자기정보 열람/정정/삭제/이동/처리정지/거부 요청 자동화
- 멀티 리전 (KR/EU/US) 통합 DSR 처리
- Event Sourcing 환경 삭제권 충족 (crypto-shredding)
- 백업·캐시·검색 인덱스 삭제 전파
- 미성년 자녀 정보를 부모가 대신 행사
- 외부 수탁자 (FCM/AWS/카카오맵) 삭제 통지 자동화
- DSR SLA 모니터링 + 위반 대응
- 자동결정(profiling) 거부권 처리 (PIPA 2024 신설)

**관련 skill (cross-link)**:
- `legal/kr-location-info-act.md` — 위치정보 별도 권리 (제24~25조)
- `legal/child-data-protection.md` — 미성년 부모 대리 행사 (§4)
- `business/audit-log.md` — DSR 요청·처리 audit
- `business/multi-tenancy.md` — tenant 데이터 격리·삭제
- `security/secure-coding.md` — 본인 인증 보안
- `messaging/kafka-patterns.md` — tombstone, retention
- `infrastructure/database-migration.md` — schema 변경 시 DSR 영향
- `platform/secrets-management.md` — KMS 키 회전·폐기 (crypto-shredding)

**관련 agent**: `compliance-auditor`, `security-scanner`, `tech-lead`
**관련 skill**: [`postgresql-operations`](../postgresql-operations/SKILL.md), [`broker-troubleshooting`](../broker-troubleshooting/SKILL.md) (삭제 이벤트 전파)

---

## 1. 권리 매트릭스 — KR vs GDPR vs CCPA

### 1.1 권리 종류

| 권리 | PIPA | 위치정보법 | GDPR | CCPA |
|---|---|---|---|---|
| **열람 (Access)** | 제35조 | 제25조 | Art.15 | Right to Know |
| **정정 (Rectification)** | 제36조 | 제25조 | Art.16 | Right to Correct |
| **삭제 (Erasure / 잊혀질 권리)** | 제36조 | 제25조 | Art.17 | Right to Delete |
| **이동 (Portability)** | 제35조의2 *(2024 신설)* | - | Art.20 | Right to Portability |
| **처리정지 (Restriction)** | 제37조 | - | Art.18 | Limit Use |
| **거부 (Object)** | 제37조 | - | Art.21 | Opt-out (Sale/Sharing) |
| **자동결정 거부** | 제37조의2 *(2024 신설)* | - | Art.22 | - |

### 1.2 SLA 비교

| 항목 | KR (PIPA) | GDPR | CCPA |
|---|---|---|---|
| 1차 응답 | **10일** | 30일 (2개월 연장 가능) | 45일 (45일 연장 가능) |
| 거부 사유 통지 | 즉시 | 1개월 내 | 즉시 |
| 재이의 (행정) | 60일 (개인정보 분쟁조정위) | 감독기관 신고 | CA AG 신고 |
| 검증 비용 | 무료 | 무료 (남용 시 부과) | 무료 |
| 본인 위변조 거부 | 가능 (사유 통지) | 가능 | 가능 |

> 멀티 리전은 **KR 10일** 디폴트. 자동으로 GDPR/CCPA 충족.

---

## 2. 처리 워크플로우

```
1. 요청 접수 (앱 / 웹 / 이메일 / 우편 / 대면)
        │
        ▼
2. 본인 인증 (§3)
        │
        ▼
3. 분류 (열람 / 정정 / 삭제 / 이동 / 처리정지 / 거부 / 자동결정거부)
        │
        ▼
4. 데이터 카탈로그 조회 — "어디에 무엇이 있는가" (§4)
        │
        ▼
5. 처리 (saga / parallel)
   ├─ DB primary
   ├─ DB read replica
   ├─ Cache (Redis)
   ├─ Search index (ES)
   ├─ Event store (Kafka — crypto-shredding 또는 tombstone)
   ├─ Backup (보유 단축 또는 키 폐기)
   └─ External processors (DPA에 따라 통지)
        │
        ▼
6. 결과 통지 + 증명서 (정정/삭제 인증서)
        │
        ▼
7. audit log + 회신 보존 (분쟁 대비 1년+)
```

> 처리 시간이 SLA를 초과할 가능성 있으면 **사전에 연장 사유 + 예상 완료일** 통지 (PIPA 시행령).

---

## 3. 본인 인증

### 3.1 방법별

| 방법 | 신뢰도 | KR 적합 | 비고 |
|---|---|---|---|
| **PASS** | 높음 | ✅ 디폴트 | 휴대폰 본인확인 |
| **공동인증서 / 금융인증서** | 매우 높음 | ✅ | 데스크톱 강함, 모바일 약함 |
| **본인 카드 1원 결제** | 중 | △ | 결제 마찰, 미성년 부적합 |
| **얼굴 인증 (face match + 신분증)** | 중 | △ | API 비용, 위변조 위험 |
| 이메일 + SMS 듀얼 | 낮음 | ❌ | KR 단독 부적합 |
| 부모 인증 + 자녀 권한 위임 | (미성년) | ✅ | `legal/child-data-protection.md` §4 |

### 3.2 인증 강도 결정

| 권리 | 권장 강도 |
|---|---|
| 열람 | PASS 1회 |
| 정정 | PASS 1회 |
| 삭제 | PASS + 추가 확인 (이메일·SMS 코드) — 되돌릴 수 없음 |
| 이동 (export) | PASS 1회 + 다운로드 링크는 시간 제한 |
| 처리정지 / 거부 | PASS 1회 |

> 삭제는 비가역이므로 강한 인증 + 24시간 cooling-off 권장.

---

## 4. 데이터 카탈로그

내가 가진 사용자 데이터의 위치를 모두 추적해야 한다. 카탈로그 없이 DSR은 **누락이 발생**한다.

### 4.1 카탈로그 YAML 예시

```yaml
# data-catalog/user.yaml
user_data:
  - store: postgres
    schema: users
    table: users
    pk: user_id
    pii: [name, phone, email, address]
    actions: [access, rectify, erase]
    retention: until_account_closed

  - store: postgres
    schema: vehicle
    table: boarding_events
    pk: user_id
    pii: [boarded_at, alighted_at, vehicle_id]
    actions: [access, erase]
    retention: 90d  # 위치정보법 즉시 파기 결합

  - store: timescale
    table: tracking.location
    pk: user_id
    pii: [coordinates]
    actions: [access (운행 한정), erase]
    retention: 90d

  - store: mongo
    db: chat
    collection: messages
    pk: sender_id
    pii: [content]
    actions: [access, erase (sender_id 비식별화 옵션)]
    retention: 1y

  - store: kafka
    topic: eodini.user.events
    pii_strategy: crypto-shredding  # 키 폐기로 사실상 삭제
    actions: [erase]

  - store: s3
    bucket: eodini-uploads
    pii_strategy: object_delete + lifecycle_purge
    actions: [access, erase]

  - store: redis
    key_pattern: "user:{user_id}:*"
    actions: [erase]

  - store: opensearch
    index: chat-messages
    actions: [erase]

  - external:
      processor: FCM (Google)
      contract: DPA-2025-FCM
      pii: [device_token, user_id]
      action_api: fcm.deleteUserAccount
```

### 4.2 카탈로그 검증 (CI)

- 새 schema·table·collection 추가 시 카탈로그 누락 검사
- DSR 처리 후 실제 삭제 검증 (canary user로 raw 조회)

---

## 5. 삭제 vs 익명화 결정 트리

```
법적 보관 의무 있나?
    │
    ├─ 있다 (전자상거래법, 세법, 통신비밀보호법 등)
    │    └─> 즉시 삭제 불가
    │        └─> 익명화/가명처리 (user_id 해시 분리)
    │            + 보관 기간 종료 후 즉시 파기
    │
    └─ 없다
         └─> 즉시 파기

위치정보법 적용 데이터?
    └─> 즉시 파기 원칙 (PIPA 일반 보관 디폴트와 다름)
```

### 5.1 가명처리 (Pseudonymization)

| 단계 | 동작 |
|---|---|
| user_id → hashed_id | SHA-256 + per-deployment salt |
| 직접 식별자 (이름·전화·이메일) | 별도 테이블로 분리, 액세스 제한 |
| 간접 식별자 (생일·우편번호 일부) | 일반화 (생일 → 생년) |
| 결합 위험 데이터 | k-anonymity / differential privacy |

> 가명처리는 **삭제 아님**. 보관 기간 종료 후 다시 파기 필요.

---

## 6. Event Sourcing 환경의 삭제 — Crypto-Shredding

### 6.1 문제

- Kafka topic은 append-only, 삭제 어려움
- Event Sourcing은 모든 이력 보존이 디자인 원칙
- → 삭제권 충족이 아키텍처 차원에서 막힘

### 6.2 해결: Crypto-Shredding

사용자별 데이터 암호화 키(Per-User PII Key)를 KMS에 두고, 삭제 요청 시 **키만 폐기**. 데이터는 남아도 복호화 불가 → 사실상 삭제.

```
Event {
  event_id: uuid
  aggregate_id: uuid (clear)
  user_id_pseudonym: hash(user_id)        # 식별자 가명화
  pii_payload_encrypted: AES-256-GCM(payload, PIIKey[user_id])
  non_pii_payload: { timestamp, action_type, ... }
}

KMS:
  PIIKey[user_id] — 사용자당 1개 데이터 키
  마스터 키 → Per-user 키 derive

삭제 요청 시:
  1. PIIKey[user_id] 즉시 폐기 (KMS revoke)
  2. 기존 event는 그대로 남음
  3. 복호화 시도 → 키 없음 → 영구 복호 불가
  4. audit: "key revoked at TIMESTAMP for GDPR Art.17"
```

### 6.3 함정

- **마스터 키 회전 후에도 derive 가능하면 무의미** — 폐기 후 derive 차단 검증
- **백업된 키도 폐기** — 키 백업 정책 동시 운영
- **응답 데이터에 PII 캐시되어 있으면 보강 처리** (Redis, ES 같이 처리)
- **non_pii_payload에 의도치 않은 PII 포함되면** crypto-shred 무용

---

## 7. 백업·캐시·검색 인덱스 삭제 전파

| 저장소 | 삭제 방법 | 함정 |
|---|---|---|
| **PostgreSQL** | DELETE + cascade | replica lag 시 잔존 |
| **MongoDB** | deleteOne / deleteMany + 인덱스 | aggregation cache |
| **Redis** | DEL keys (tag-based 삭제 권장) | RDB 백업 잔존 |
| **TimescaleDB** | DELETE FROM hypertable | chunk 압축 후 어려움 → drop_chunks 정책 |
| **Kafka (compacted)** | tombstone (key=user_id, value=null) | retention X 토픽엔 무효 |
| **Kafka (retention)** | retention.ms 만료 대기 | crypto-shredding 권장 |
| **S3** | DeleteObject + lifecycle | versioning 켜져있으면 노출 |
| **Elasticsearch** | DELETE document + force_merge | 새 인덱스로 reindex 필요할 수 있음 |
| **백업 (DB snapshot)** | (1) 보유 단축 (2) 키 폐기 (3) 별도 처리 | 가장 흔히 누락 |
| **로그 (Loki/Datadog)** | 보존 기간 단축 + PII 마스킹 정책 | 외부 SaaS 정책 확인 |

### 7.1 백업 처리 권장

```
백업 보유 = max(법적 보관, DR 필요) 로 단축
또는 백업도 crypto-shredding (per-user key 사용)
또는 PII 컬럼만 백업에서 제외
```

---

## 8. 외부 수탁자 (Processors) 통지

DPA(Data Processing Agreement)에 따라 수탁자에게 삭제·정정 요청을 전달.

### 8.1 통지 SLA

| 법령 | 수탁자에게 통지 |
|---|---|
| PIPA | 즉시 (위탁 종료 시점에) |
| GDPR | 1개월 내 (Art.19) |
| CCPA | 영업일 15일 |

### 8.2 자주 쓰는 수탁자

| 처리자 | 삭제 API | 비고 |
|---|---|---|
| FCM (Google) | `User Account Deletion API` | device_token 즉시 삭제 |
| AWS | DescribeBackup + DeleteSnapshot | 리전별 일관성 확인 |
| 카카오맵 | (위탁 데이터 거의 없음) | 통지만 |
| Datadog / Sentry | user lookup 삭제 | 라벨링 PII 정리 |
| Twilio / SendGrid | suppress + contact 삭제 | 마케팅 차단 결합 |

---

## 9. 미성년 자녀 권리 행사

- 부모가 자녀 정보 열람·삭제 가능 (`legal/child-data-protection.md` §4)
- 자녀 14세 도래 후 권한 자동 이양 (cron — `legal/child-data-protection.md` §11.4)
- 분리 가족 — 양육권자만 행사. 비양육 부모는 read-only 또는 차단
- 분쟁 시 audit log + 가족관계증명서로 증명

---

## 10. 도메인 매핑 — 통학차량 플랫폼 사례

| 권리 | 데이터 | 처리 위치 | SLA |
|---|---|---|---|
| 열람 | 학부모 → 자녀 위치 이력 | TimescaleDB tracking.location | 10일 |
| 열람 | 운전자 → 자기 운행 이력 | tracking.trip + audit | 10일 |
| 정정 | 학부모 연락처/주소 | users 스키마 | 즉시 |
| 정정 | 차량 등록정보 | vehicle 스키마 | 즉시 (운영자 검토) |
| 삭제 | 학부모 탈퇴 | users + 채팅 + 위탁 통지 | 24h saga |
| 삭제 | 학생 탈퇴 (졸업/이사) | child + family + 채팅 + 위치 | 24h saga |
| 이동 | 운행 통계 export | TimescaleDB → CSV/JSON | 7일 |
| 처리정지 | 학부모 일시 비활성 | flag + tracking OFF | 즉시 |
| 거부 | 마케팅 푸시 거부 | notification opt-out | 즉시 |
| 자동결정 거부 | (Phase 3 ML 노선 최적화) | profiling consent OFF | 즉시 |

---

## 11. 구현 패턴

### 11.1 DSR 요청 큐 (PostgreSQL)

```sql
CREATE TABLE dsr_requests (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  on_behalf_of UUID,           -- 부모가 자녀 대신 행사 시 자녀 user_id
  request_type VARCHAR(30) NOT NULL,
    -- 'access' | 'rectify' | 'erase' | 'portability'
    -- 'restrict' | 'object' | 'auto_decision_object'
  legal_basis VARCHAR(20) NOT NULL,  -- 'pipa' | 'gdpr' | 'ccpa' | 'location_info_act'
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending | verifying | processing | completed | rejected | extended
  rejection_reason TEXT,
  submitted_at TIMESTAMPTZ NOT NULL,
  deadline_at TIMESTAMPTZ NOT NULL,    -- KR 10일 / GDPR 30일 / CCPA 45일
  completed_at TIMESTAMPTZ,
  verification_method VARCHAR(30),
  verification_id TEXT,
  metadata JSONB
);

CREATE INDEX idx_dsr_pending ON dsr_requests (status, deadline_at)
  WHERE status IN ('pending', 'verifying', 'processing');
```

### 11.2 본인 인증 (Go)

```go
type DSRService struct{ ... }

func (s *DSRService) Authenticate(ctx context.Context, req DSRRequest) error {
    if req.RequestType == "erase" {
        // 삭제는 강한 인증 + 24h cooling-off
        if err := s.passVerifier.Verify(ctx, req.UserID); err != nil {
            return fmt.Errorf("primary auth failed: %w", err)
        }
        if err := s.smsCodeChallenge.Confirm(ctx, req.UserID); err != nil {
            return fmt.Errorf("secondary auth failed: %w", err)
        }
        return s.scheduleAfterCoolingOff(ctx, req, 24*time.Hour)
    }
    return s.passVerifier.Verify(ctx, req.UserID)
}
```

### 11.3 삭제 saga (Kafka 이벤트 기반)

```
1. user.erase.requested  → DSR worker
   ├─ 본인 인증 통과 확인
   └─ deadline_at 설정 (KR=submit+10d)

2. user.erase.started → fan-out (parallel):
   ├─ postgres-eraser     (users + cascade)
   ├─ mongo-eraser        (chat messages)
   ├─ redis-purger        (DEL user:{id}:*)
   ├─ timescale-eraser    (tracking.location WHERE user_id=...)
   ├─ kafka-shredder      (KMS PIIKey[user_id] revoke)
   ├─ s3-eraser           (DeleteObject + version purge)
   ├─ opensearch-eraser   (DELETE BY query)
   └─ external-notifier   (FCM/AWS DPA)

3. all-completed → user.erased.confirmed
   └─ audit log: { actor, target_user, channels, completed_at }

4. 실패 시 → user.erase.failed.{channel}
   └─ retry + alert + manual escalation
```

### 11.4 Export (이동권) 패키징

```go
// PIPA 제35조의2 / GDPR Art.20
type ExportPackage struct {
    User     UserSnapshot     `json:"user"`
    Vehicles []VehicleEntry   `json:"vehicles"`
    Trips    []TripSummary    `json:"trips"`
    Messages []ChatMessage    `json:"messages"`
    Consents []ConsentRecord  `json:"consents"`
    Legal    LegalMetadata    `json:"_legal"`  // 발급일/법적근거/유효기간
}

// 전달: 시간 제한 다운로드 링크 (7일) + 비밀번호 + audit
```

### 11.5 SLA 모니터링 (PromQL)

```promql
# 미처리 요청 수 (deadline 임박)
count(dsr_requests{status="pending"})

# SLA 위반 (deadline 지난 미완료)
count(dsr_requests{status!="completed", deadline_at < now()})

# 처리 시간 분포
histogram_quantile(0.95, dsr_processing_duration_seconds)
```

---

## 12. 함정 (자주 빠뜨리는 것)

| 함정 | 결과 | 대응 |
|---|---|---|
| `deleted_at` soft delete만 함 | PIPA 위반 (사실상 보관) | hard delete + audit |
| 백업에서 삭제 누락 | 즉시 파기 위반 | 보유 단축 또는 crypto-shredding |
| Kafka 토픽 무한 보존 (compaction) | 보관 위반 | retention 강제 또는 crypto-shred |
| Redis / ES 잔존 | 부분 삭제 | tag-based 일괄 삭제 |
| 외부 수탁자 통지 누락 | DPA 위반 | 카탈로그에 processor 명시 + 알림 |
| 본인 인증 약함 | 신원 도용 → 무단 삭제 | PASS + 삭제 시 추가 확인 |
| "법적 보관 의무" 핑계로 즉시 파기 안 함 | PIPA 우회 의심 | 익명화 + 보관 기간 종료 후 재파기 |
| DSR 요청 audit 누락 | 분쟁 시 증거 부족 | append-only audit log 1년+ |
| 14세 자녀 권한 이양 후 부모 열람 권한 유지 | 권한 근거 소멸 | cron으로 자동 read-only 강등 |
| 양육권 미확인 부모의 삭제 요청 | 무단 처리 | 가족관계증명서 검증 |
| Export에 다른 사용자 PII 섞임 | 2차 침해 | 친구 목록·채팅 상대 마스킹 |
| crypto-shredding 후 키 백업 잔존 | 사실상 복원 가능 | KMS 키 백업 정책 동시 폐기 |
| canary user로 잔존 검증 안 함 | "삭제했다" 자칭 위험 | 매 분기 raw 조회 검증 |
| profiling 거부권 (PIPA 2024 신설) 미반영 | 신규 의무 위반 | 자동결정 시스템에 opt-out 통합 |
| 정정 요청을 비즈니스 로직과 충돌 시 거부 | 정당성 부족 | 사유 명시 + 분쟁조정위 안내 |

---

## 13. 운영 체크리스트

### 인프라
- [ ] DSR 요청 채널 (앱 / 웹 / 이메일 / 우편 / 대면)
- [ ] PASS 본인 인증 통합
- [ ] 데이터 카탈로그 YAML/DB + CI 누락 검사
- [ ] 삭제 saga 구현 (모든 저장소)
- [ ] crypto-shredding KMS 키 정책 + 백업 키 폐기

### 프로세스
- [ ] SLA 알림 (KR=10일, GDPR=30일, CCPA=45일)
- [ ] 거부 사유 표준 (법적 보관 / 권리 미적용 / 위변조 / 남용)
- [ ] 외부 수탁자 통지 자동화 (DPA 목록 관리)
- [ ] 정정·삭제 증명서 발급
- [ ] audit log 1년+ 보존

### 미성년
- [ ] 부모 권리 행사 흐름 (`legal/child-data-protection.md` §4)
- [ ] 14세 도래 권한 이양 cron + 부모 read-only 강등
- [ ] 분리가족 양육권 검증 SOP

### 모니터링
- [ ] 미처리 요청 대시보드
- [ ] SLA 위반 알림 (Discord/PagerDuty)
- [ ] 처리 후 검증 (canary user raw 조회)
- [ ] crypto-shredding 키 폐기 검증 (복호화 시도 시 차단 확인)

---

## 부록 A: 자주 묻는 질문

**Q. DPA 없는 옛 위탁업체에 어떻게 통지?**
A. DPA 부재 자체가 PIPA 위반. 즉시 DPA 체결 또는 위탁 종료. 통지는 일반 공문으로.

**Q. 사용자가 본인 인증 못 하면?**
A. 본인 인증 보조수단 (이메일+SMS+신분증 사진+질문) 또는 영업장 방문. 60일 내 재신청 가능.

**Q. 14세 자녀 권한 이양 시 부모는 어떻게?**
A. 자동으로 read-only 강등. 자녀가 명시 차단 시까지 위치 보기는 유지 (가족 관계 보호). 채팅·결제는 자녀 본인 동의 필요.

**Q. "법적 보관 의무"를 핑계로 1년 보관하는 게 가능한가?**
A. 통신비밀보호법(접속기록 1년) 등 명확한 근거 있어야 함. 막연한 "분쟁 대비"는 무효. 익명화 + 보관 기간 명시 필수.

**Q. 정정 요청이 비즈니스 로직과 충돌하면?**
A. (1) 시스템상 불가능 (예: 중복 unique 키) → 거부 + 사유 통지. (2) 비즈니스 정책상 거부 → 정당성 약함. 분쟁조정위 안내.

**Q. 분리가족 자녀 정보를 양쪽 모두 열람권 가지나?**
A. 양육권자만. 비양육 부모가 청구 시 가족관계증명서 + 양육권 증빙 필수. 분쟁 시 결정문 제시 전까지 거부.

**Q. crypto-shredding 후 데이터 복원 요구되면 (예: 사용자 재가입)?**
A. 복원 불가. 새 키로 새로 시작. 옛 데이터 복구 안 된다는 사전 안내 필요.

**Q. 자동결정 거부권은 무엇을 거부할 수 있나?**
A. 프로파일링·자동 신용평가·자동 콘텐츠 추천 등. 단순 자동 응답(예: 알림 발송 트리거)은 대상 아님. 통학차량의 ML 노선 최적화(Phase 3)에 적용.

---

## 참고 자료

- 「개인정보 보호법」 제35~38조 + 동법 시행령
- 「위치정보의 보호 및 이용 등에 관한 법률」 제24~25조
- GDPR Articles 15~22 (Chapter III — Rights of the Data Subject)
- CCPA — Cal. Civ. Code §§ 1798.100 et seq.
- 개인정보보호위원회 「정보주체 권리 행사 안내」
- ICO (UK) Right of Access guidance
