---
name: kr-location-info-act
category: legal
description: 한국 위치정보법(「위치정보의 보호 및 이용 등에 관한 법률」) 운영 — 사업 신고/허가, 별도 동의(약관·개인정보와 분리), 만8세 이하/14세 미만 법정대리인 동의, 즉시 파기, 매년 통계 보고. 차량/사람/IoT GPS를 다루는 한국 SaaS의 필수 컴플라이언스 hub.
license: MIT
---

# Korean Location Information Act — 위치정보법 운영

「위치정보의 보호 및 이용 등에 관한 법률」 운영 가이드. 차량·사람·디바이스 GPS를 다루는 한국 SaaS는 일반 PIPA(개인정보 보호법)와 **별도로** 위치정보법이 동시 적용된다. 사업 신고/허가 의무가 있고, 약관·개인정보 동의와 **분리된** 별도 동의를 받지 않으면 무효이며, 위반 시 형사처벌(최대 5년/5천만원)을 받는다.

> **GDPR/PIPA만으로 충분하다고 가정하면 사고가 난다.** 위치정보법은 한국 단독 법령으로 (1) 사업 신고/허가, (2) 별도 동의, (3) 즉시 파기, (4) 매년 통계 보고 등 추가 의무를 부과한다. 이 skill은 한국 위치정보법 운영 hub. 일반 글로벌 컴플은 `security/compliance-frameworks.md`, 14세 미만 결합은 `legal/child-data-protection.md`, 데이터 주체 권리 운영은 `legal/data-subject-rights.md`.

## When to Use

- 한국에서 GPS 추적 서비스 출시 (통학차량/배달/택시/물류/반려동물/차량공유)
- 일반 SaaS 한국 진출 시 컴플라이언스 점검
- 위치 동의 UX 설계 (가입 플로우 / 약관 화면 분리)
- 위치 데이터 보유·파기 정책 자동화 (DB + Kafka + 백업)
- 위치 데이터 위탁 (FCM / 카카오맵 / AWS) 동의 설계
- 어린이/미성년자 위치 추적 (PIPA 14세 + 위치정보법 8세 결합)
- 침해사고 대응 24시간 신고 SOP

**관련 skill (cross-link)**:
- `legal/child-data-protection.md` — 만14세 미만 동의 UX, 가족 계정, 추적 가시화
- `legal/data-subject-rights.md` — DSR(열람/정정/삭제/이동) 자동화
- `security/compliance-frameworks.md` — 글로벌 컴플 (GDPR/HIPAA/SOC2/PCI-DSS) 비교
- `business/audit-log.md` — 동의 수집·철회·접근 audit
- `business/notification-multichannel.md` — 추적 사실 가시화 알림
- `business/multi-tenancy.md` — 기관(학원) 단위 위치정보 격리
- `security/secure-coding.md` — 좌표 암호화, 마스킹
- `observability/logging-compliance.md` — 위치 로그 보존/파기

**관련 agent**: `compliance-auditor`, `security-scanner`, `tech-lead`
**관련 skill**: [`postgresql-operations`](../postgresql-operations/SKILL.md)

---

## 1. 적용 결정 트리

```
어떤 데이터인가?
    │
    ├─ 식별 가능한 개인 + 위치 (좌표, 주소, IP기반 위치)
    │      └─> 개인위치정보 → 강한 규제 (제15조 이하)
    │
    ├─ 사물(차량/IoT 디바이스) 위치, 사람과 분리됨
    │      └─> 사물위치정보 → 약한 규제 (사업 신고만)
    │
    └─ 차량 위치 + 운전자 1:1 매칭
           └─> 사실상 개인위치정보 (실무 통설)
                 → 운전자 동의 필요

위치정보를 어떤 입장에서 다루는가?
    │
    ├─ 직접 수집·전송하는 사업자 ────> 위치정보사업자
    │   ├─ 개인위치정보 ────────────> 방통위 허가 (3년)
    │   └─ 사물위치정보 ────────────> 방통위 신고
    │
    └─ 받아서 가공·서비스 제공 ──────> 위치기반서비스사업자 (LBS App, 신고)
```

> **착각 금지**: "차량 GPS는 사물이라 사물위치정보 아닌가?" → 차량과 운전자가 1:1 매칭되면 운전자 행적이 노출되므로 개인위치정보로 본다. 통학차량·배달·택시는 모두 개인위치정보.

---

## 2. 사업 분류 매트릭스

| 사업 분류 | 정의 | 관할 절차 | 갱신 |
|---|---|---|---|
| 위치정보사업자 (개인) | 개인위치정보 직접 수집·제공 | 방통위 **허가** | 3년 |
| 위치정보사업자 (사물) | 사물위치정보 직접 수집·제공 | 방통위 **신고** | - |
| 위치기반서비스사업자 (LBS) | 위치정보를 받아 서비스 제공 | 방통위 **신고** | - |

**통학차량 플랫폼 사례 적용**:
- 운전자 앱이 직접 GPS 송신 → 사용자 디바이스가 수집 주체. 플랫폼은 받아서 가공·제공 → **위치기반서비스사업자 신고** 의무
- 차량 좌표를 학부모에게 제공하는 부분은 운전자 위치를 노출하므로 **개인위치정보**로 본다 → 운전자 동의 필수
- 학생 입장에서도 차량 위치 ≒ 학생 위치이므로 **간접 개인위치정보** → 학생 법정대리인 동의 필수

---

## 3. 동의 수집 (제18조)

### 3.1 별도 동의 — 가장 자주 위반하는 항목

```
❌ 무효 패턴 (한 체크박스로 묶음)
┌────────────────────────────────────┐
│  □ 약관 / 개인정보 / 위치 모두 동의   │
│  [확인]                            │
└────────────────────────────────────┘

✅ 유효 패턴 (화면/체크박스 분리)
┌────────────────────────────────────┐
│  ① 서비스 약관 동의 (필수)            │  ← 별도 화면
│  ② 개인정보 처리 동의 (필수)          │  ← 별도 화면
│  ③ 위치정보 처리 동의 (필수)          │  ← 별도 화면 강력 권장
│  ④ 마케팅 수신 동의 (선택)            │
└────────────────────────────────────┘
```

### 3.2 동의 항목 분리 (5종)

| 동의 항목 | 의무 | 위반 시 형량 |
|---|---|---|
| 수집·이용 | 별도 동의 | 5년 / 5천만 |
| 제공 (제3자) | 별도 동의 | 5년 / 5천만 |
| 위탁 (수탁자) | 별도 동의 + 공시 | 1년 / 1천만 |
| 처리 위탁 | 동의 + 통지 | - |
| 국외 이전 | 별도 동의 | 1년 / 1천만 |

### 3.3 만8세 이하 / 14세 미만 (제26조 결합)

| 대상 | 동의 주체 | 추가 의무 |
|---|---|---|
| 만8세 이하 / 피후견인 | 법정대리인 | 본인 인지 (추적 사실 알림) |
| 만14세 미만 (PIPA 결합) | 법정대리인 | 추적 사실 즉각 가시화 (제26조 관련 의무) |
| 만14세 이상 | 본인 | - |

> **핵심**: 부모가 동의했다고 자녀에게 비밀로 추적 불가. 자녀가 추적되고 있다는 사실을 **앱 UI에서 가시화**해야 한다. 자세한 UX 패턴은 `legal/child-data-protection.md`.

---

## 4. 보유·이용·파기 (제23조)

### 4.1 즉시 파기 의무

> **목적 달성 즉시 파기.** PIPA처럼 "1년 보관"이 디폴트가 아니다. 보관하려면 **별도 법적 근거**가 있어야 한다.

| 단계 | 통학차량 예시 | 권장 정책 |
|---|---|---|
| 실시간 좌표 | Redis 캐시 | 운행 종료 + 5분 TTL |
| 일·주 분석 | TimescaleDB hot | 30일 후 cold tier 이동 |
| 장기 통계 | TimescaleDB cold | 90일 후 익명화 또는 삭제 |
| 백업 | S3 / DB snapshot | 보유 기간 도래 시 백업 폐기 |
| 이벤트 스토어 | Kafka topic | retention 강제 (compaction X) |

### 4.2 파기 자동화 (K8s CronJob 예시)

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: location-purge
spec:
  schedule: "0 3 * * *"  # 매일 03:00
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: purge
            command: ["/bin/sh", "-c"]
            args:
              - |
                psql -c "DELETE FROM tracking.location WHERE recorded_at < NOW() - INTERVAL '90 days'"
                psql -c "DELETE FROM tracking.trip     WHERE ended_at    < NOW() - INTERVAL '180 days'"
                # Kafka topic은 broker retention 정책으로 강제
                # Redis는 SET ... EX 시점에 TTL 자동
```

### 4.3 백업 잔존 함정

> **가장 흔한 위반**: DB는 90일 후 삭제했는데 **백업 스냅샷에 그대로 남아 있음**. 즉시 파기 위반.

대응:
- 백업 보유 기간을 즉시 파기 정책에 맞춰 단축 (예: 30일)
- 또는 PII/위치 컬럼만 백업에서 제외
- 또는 컬럼 단위 암호화 + 키 폐기 (**crypto-shredding** — `legal/data-subject-rights.md` 참조)

---

## 5. 위탁·국외 이전 (제22조)

### 5.1 처리 위탁 매트릭스 (실무 자주 쓰는 외부 서비스)

| 외부 서비스 | 종류 | 한국 리전 여부 | 의무 |
|---|---|---|---|
| AWS Seoul (ap-northeast-2) | 인프라 | O | 위탁 동의 + 공시 |
| AWS US/EU | 인프라 | X | **국외 이전 동의** |
| Firebase Cloud Messaging | 푸시 | X (글로벌) | **국외 이전 동의** |
| 카카오맵 API | 지도 | O | 위탁 동의 |
| Google Maps API | 지도 | X | **국외 이전 동의** |
| OpenAI / Claude API | AI | X | **국외 이전 동의** |
| Sentry / Datadog | 모니터링 | 리전별 상이 | 리전 확인 필수 |
| Twilio / SendGrid | SMS/메일 | X | **국외 이전 동의** |

### 5.2 국외 이전 동의 요건

별도 동의 + 공시 필수 (제21조):
- 이전받는 자 (회사명, 국가)
- 이전 항목
- 이전 목적·기간
- 거부 권리 + 거부 시 서비스 영향

---

## 6. 운영 의무

### 6.1 정기 의무

| 의무 | 주기 | 관할 |
|---|---|---|
| 통계 보고 | 매년 1월 31일까지 | 방통위 |
| 운영지침서 비치 | 상시 (2년 보관) | 사업장 |
| 위치정보 관리책임자 지정·공시 | 상시 | 개인정보처리방침 |
| 침해사고 신고 | 24시간 이내 | KISA |

### 6.2 이용자 권리 (제24~25조)

- 열람·정정·삭제 요청 시 즉시 처리 (3영업일 권고)
- 동의 철회 즉시 반영 (1초 단위)
- 운영 자동화는 `legal/data-subject-rights.md` 참조

---

## 7. 위반 시 처벌 (제40~43조)

| 위반 | 형사 처벌 | 비고 |
|---|---|---|
| 동의 없이 개인위치정보 수집 | 5년 이하 / 5천만 이하 | 가장 무거움 |
| 사업 신고/허가 위반 | 3년 이하 / 3천만 이하 | 무신고 운영 시 |
| 보호조치 의무 위반 | 2년 이하 / 2천만 이하 | 암호화·접근통제 |
| 위탁/국외 이전 위반 | 1년 이하 / 1천만 이하 | |
| 통계보고 누락 등 | 과태료 1천만 이하 | |

> **GDPR과 결정적 차이**: 한국법은 **형사처벌**이 동반된다. CEO/CTO/CISO 개인이 형사 책임을 질 수 있다. 회사 벌금이 아니라 **개인이 징역** 가능.

---

## 8. 도메인 매핑 — 통학차량 플랫폼 사례

| 컴포넌트 | 위치정보법 적용 | 운영 행동 |
|---|---|---|
| 운전자 앱 GPS 송신 (MQTT) | 개인위치정보 수집 | 운행 중에만 ON, 종료 시 자동 OFF |
| Tracking 서비스 Redis 캐시 | 보유 (단기) | 운행 종료 + 5분 TTL |
| TimescaleDB tracking.location | 보유 (장기) | 90일 후 자동 파기 |
| Kafka eodini.tracking.location | 임시 처리 | retention 7일 강제 |
| 학부모 앱 위치 조회 (SSE) | 제공 (제3자) | 동의받은 학부모만, 운행 시간 한정 |
| 학생 좌표 추정 (차량=학생) | 간접 위치정보 | 학생 법정대리인 동의 필수 |
| FCM 푸시 (위치 변동 알림) | 국외 이전 | 별도 동의 |
| 카카오맵 표출 | 위탁 | 동의 + 공시 |
| AWS Seoul | 위탁 | 공시만 |

---

## 9. 구현 패턴

### 9.1 별도 동의 DB 스키마

```sql
CREATE TABLE location_consents (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  consent_type VARCHAR(20) NOT NULL,
    -- 'collect' | 'provide' | 'entrust' | 'cross_border'
  consented BOOLEAN NOT NULL,
  consented_at TIMESTAMPTZ NOT NULL,
  withdrawn_at TIMESTAMPTZ,
  legal_basis TEXT NOT NULL DEFAULT '위치정보법 제18조',
  consent_text_hash CHAR(64) NOT NULL,
    -- SHA-256 of consent text shown to user (화면이 바뀌면 hash 변동)
  consent_ui_version VARCHAR(20) NOT NULL,
  ip_address INET,
  user_agent TEXT,
);

-- 활성 동의는 type별 1개만: partial unique index (PG 모든 버전 호환)
CREATE UNIQUE INDEX one_active_per_consent_type
  ON location_consents (user_id, consent_type)
  WHERE withdrawn_at IS NULL;

-- 동의 audit는 append-only (business/audit-log.md 참조)
-- consent_text_hash로 "그때 어떤 문구에 동의했는지" 검증 가능
```

### 9.2 동의 화면 분리 (Flutter)

```dart
// 잘못된 패턴 — 한 화면에 묶음 (동의 무효)
Column(children: [
  Checkbox(value: agreeAll), // 모든 동의 한 번에
  Text("약관, 개인정보, 위치정보 모두 동의"),
])

// 올바른 패턴 — 화면 분리
final flow = [
  TermsScreen(),           // 1단계: 서비스 약관 (필수)
  PrivacyScreen(),         // 2단계: 개인정보 (필수)
  LocationConsentScreen(), // 3단계: 위치정보 (별도 화면)
  CrossBorderScreen(),     // 4단계: FCM 등 국외 이전 (별도)
  OptionalConsentScreen(), // 5단계: 마케팅 (선택)
];
```

### 9.3 운행 중 한정 수집 (운전자 앱)

```dart
// 운행 시작 ↔ 종료 사이에만 GPS 활성화
class DrivingSession {
  StreamSubscription<Position>? _sub;

  void start({required String tripId}) {
    _sub = Geolocator.getPositionStream(
      locationSettings: LocationSettings(
        accuracy: LocationAccuracy.high,
        distanceFilter: 10,
      ),
    ).listen(_onPosition);
    audit.log('driving.started', tripId: tripId);
  }

  void end({required String tripId}) {
    _sub?.cancel();
    _sub = null; // 즉시 OFF
    audit.log('driving.ended', tripId: tripId);
    // 즉시 파기 트리거: Redis 운행ID 키 5분 후 만료
  }
}
```

### 9.4 동의 철회 즉시 반영 (서버)

```go
// Tracking Service — consent withdrawal handler
func (s *TrackingService) OnConsentWithdrawn(
    ctx context.Context, userID uuid.UUID, consentType string,
) error {
    // 1. 활성 SSE 연결 종료 (학부모 측 위치 스트림)
    s.sseHub.Disconnect(userID)

    // 2. Redis 위치 캐시 즉시 삭제
    s.redis.Del(ctx, fmt.Sprintf("location:%s", userID))

    // 3. MQTT subscription 즉시 해제 (운전자 측)
    s.mqttBroker.Unsubscribe(fmt.Sprintf("driver/%s/+", userID))

    // 4. audit log (append-only)
    s.audit.Log(ctx, AuditEvent{
        Action:     "location.consent.withdrawn",
        ActorID:    userID,
        ConsentType: consentType,
        LegalBasis: "위치정보법 제18조",
    })
    return nil
}
```

---

## 10. 함정 (자주 빠뜨리는 것)

| 함정 | 결과 | 대응 |
|---|---|---|
| 약관 안에 위치정보 동의 끼워넣기 | 동의 무효 → 5년/5천만 | 별도 화면 강제 |
| 백업/스냅샷에 위치 데이터 잔존 | 즉시 파기 위반 | 백업 보유 단축 또는 crypto-shredding |
| Kafka 토픽 무한 보존 (compaction) | 보유 기간 초과 | retention.ms 강제, compaction 비허용 |
| FCM/Firebase = 글로벌 = 국외 이전 인지 못 함 | 1년/1천만 | 별도 동의 |
| 부모 동의로 자녀 비밀 추적 | 추적 가시화 의무 위반 | 자녀 앱 UI에 추적 표시 |
| 동의 철회 후 다음 사이클까지 수집 지속 | 동의 없는 수집 | 이벤트 기반 즉시 반영 |
| 매년 통계 보고 누락 | 과태료 | 1월 reminder 자동화 |
| 위탁업체(카카오맵 등) 공시 누락 | 위탁 위반 | 개인정보처리방침 자동 갱신 |
| 운전자 운행 종료 후에도 GPS 수집 | 목적 외 수집 | 세션 기반 ON/OFF + 백그라운드 권한 최소화 |
| 한 번 받은 동의로 수년 사용 | 변경 시 무효 | 약관/문구 변경 시 재동의 (`consent_text_hash` 비교) |
| API key/admin 토큰으로 우회 조회 | 동의 없는 제공 | RBAC + 모든 조회 audit |
| "테스트 환경"에 실데이터 사용 | 동의 없는 처리 | dev/staging 합성 데이터 강제 |

---

## 11. 운영 체크리스트

### 사업 등록
- [ ] 위치기반서비스사업자 신고 완료 (방통위)
- [ ] 위치정보 관리책임자 지정 + 처리방침 공시
- [ ] 운영지침서 비치 (사내, 2년 보관)

### 동의 인프라
- [ ] 약관 / 개인정보 / 위치정보 동의 화면 분리 검증
- [ ] 14세 미만 법정대리인 동의 플로우 (PIPA 결합)
- [ ] 자녀 앱에 추적 사실 가시화 (제26조의2)
- [ ] 동의 철회 1초 이내 반영 검증 (E2E 테스트)
- [ ] `consent_text_hash` 기반 변경 추적

### 데이터 거버넌스
- [ ] 보유 기간 명시 (각 데이터 카테고리별)
- [ ] 자동 파기 cron + 검증 (백업 포함)
- [ ] Kafka retention 강제 (compaction 비허용 토픽)
- [ ] 위탁업체 (FCM/카카오맵/AWS) 공시 + 갱신

### 권리 보장
- [ ] 열람·정정·삭제 SOP (`legal/data-subject-rights.md`)
- [ ] 동의 철회 UI (앱/웹)
- [ ] audit log (collect/provide/entrust/withdraw)

### 침해 대응
- [ ] 침해사고 SOP — 24시간 내 KISA 신고 (`operations/incident-postmortem.md` 결합)
- [ ] 매년 1월 31일 통계 보고 자동 reminder

---

## 12. 비교: GDPR vs PIPA vs 위치정보법

| 항목 | GDPR (EU) | PIPA (한국) | 위치정보법 (한국) |
|---|---|---|---|
| 동의 형식 | 명시적 | 명시적 | **별도 동의** (분리) |
| 14세 미만 | 부모 동의 (Art.8) | 법정대리인 (제22조의2) | **8세 이하 + 14세 미만** + 추적 가시화 |
| 보유 원칙 | data minimization | 명시 보관 | **즉시 파기** |
| 위반 처벌 | 매출 4% (최대 2천만 EUR) | 5천만 + 5년 | **5천만 + 5년 (형사)** |
| 사업 등록 | DPO 지정 | 처리자 지정 | **방통위 허가/신고** |
| 권리 SLA | 30일 | 10일 | 즉시 (3영업일 권고) |
| 국외 이전 | 적정성 결정 / SCC | 동의 + 공시 | **별도 동의** |
| 책임 주체 | 회사 | 회사 + 개인정보 보호책임자 | **회사 + 대표자/책임자 (형사)** |

> 한국 SaaS는 **3개를 동시에** 충족해야 한다. 위치정보법이 가장 엄격하며, 형사처벌이 결합되어 GDPR/PIPA보다 개인 책임이 크다.

---

## 부록 A: 자주 묻는 질문

**Q. 통학차량 위치는 차량(사물) 정보 아닌가?**
A. 운전자와 1:1 매칭되어 행적이 노출되므로 개인위치정보. 학생 입장에서도 차량 위치 = 학생 위치이므로 학생의 (간접) 개인위치정보.

**Q. 부모가 자녀 동의 대신해도 되는가?**
A. 동의는 가능하나 **자녀가 추적되고 있다는 사실 인지**는 별도 의무 (제26조의2). 자녀 앱 UI에 표시. `legal/child-data-protection.md` 상세.

**Q. 학교/기관이 일괄 동의 받으면 되는가?**
A. 안 됨. 개별 부모 동의 필수. 학교는 정보주체가 아니다. 단체 약관으로 갈음 시도 시 동의 무효.

**Q. 운행 종료 후 좌표를 분석용으로 보관해도 되는가?**
A. 보관 가능. 단 (1) 보유 기간 명시, (2) 익명화 또는 가명처리, (3) 종료 시점에 파기 정책 발동. `legal/data-subject-rights.md` 참조.

**Q. 만 14세 미만 학생을 학부모가 위치 추적할 때 학부모만 동의하면 되는가?**
A. 학부모 동의 + 학생 본인 인지(앱 UI 표시) 필수. 자녀 동의는 법적 요건 아니지만 인지는 의무. `legal/child-data-protection.md`.

**Q. 동의 철회 시 과거 데이터까지 삭제해야 하는가?**
A. 철회 이후 신규 수집은 즉시 중단. 과거 데이터는 (1) 보관 법적 근거 있으면 유지, (2) 없으면 즉시 파기. 운영지침서에 명시 필수.

**Q. 사업 신고 없이 운영 중인데 어떻게 되나?**
A. 3년 이하 / 3천만 이하 형사. 발견 즉시 신고 + 자진시정 권장.

---

## 참고 자료

- 「위치정보의 보호 및 이용 등에 관한 법률」 (대한민국 법률)
- 동법 시행령 / 시행규칙
- 방송통신위원회 `위치정보사업 관리·감독 가이드라인`
- 개인정보보호위원회 `아동·청소년 개인정보보호 가이드라인` (PIPA 결합)
- KISA `개인위치정보 처리 안내서`
- 「개인정보 보호법」 (PIPA, 결합 적용)
