---
name: notification-multichannel
category: business
description: "Multi-Channel Notification — 멀티채널 알림 시스템 — Push/Email/SMS/Slack/In-App. User Preferences, Fallback chain, Notification Center, Digest. 채널 추가에 강한 추상화. 신규 SaaS 알림 부트스트랩. Use when working with business 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Multi-Channel Notification

멀티채널 알림 시스템 — Push/Email/SMS/Slack/In-App. User Preferences, Fallback chain, Notification Center, Digest. 채널 추가에 강한 추상화. 신규 SaaS 알림 부트스트랩.

신규 SaaS의 알림 시스템을 0에서 만들지 않도록 검증된 추상화 + 운영 패턴.
**핵심 원칙**: 알림 의도(intent)와 전송(delivery)을 분리. 채널 추가는 어댑터만 작성.

## When to Use

- 통학차량/심리상담 등 신규 서비스에 알림 붙이기
- 결제 성공/실패, 댓글, 주문 상태 등 사용자 알림 필요
- 한 채널만 (Push)에서 시작했다가 여러 채널로 확장
- 사용자별 채널 선호 관리 (이메일은 받고 SMS는 거부 등)
- 중요/일반 알림 우선순위 분리

**관련 skill**: `msa/msa-event-driven.md`, `msa/task-queue.md`, `messaging/redis-streams.md`
**관련 agent**: `architect-agent`
**관련 skill**: [`broker-troubleshooting`](../broker-troubleshooting/SKILL.md), [`kafka-patterns`](../kafka-patterns/SKILL.md)

---

## 1. 핵심 추상화 — Intent vs Delivery

```
[Application Layer]
  → "사용자 X에게 '주문 완료' 알림" (Intent)

[Notification Service]
  ├─ User Preferences 조회 (X는 어떤 채널 선호?)
  ├─ Template 렌더링 (채널별 다른 표현)
  ├─ Routing (Push 우선 → 실패 시 Email)
  └─ Channel Dispatcher
        ├─ PushAdapter → FCM / APNs
        ├─ EmailAdapter → SES / SendGrid
        ├─ SmsAdapter → Twilio / NHN Cloud (한국)
        ├─ SlackAdapter → Slack Webhook
        └─ InAppAdapter → DB (Notification Center)
```

**핵심**:
- **Application은 채널 모름** — "주문 완료 알림 보내라"만 알림
- **Channel 추가 시 어댑터만 작성** — Application 코드 변경 X
- **사용자 선호는 Notification Service가 결정** — Application 책임 아님

---

## 2. 알림 도메인 모델

```
NotificationIntent
  ├─ id (uuid)
  ├─ user_id
  ├─ event_type: order.paid | comment.created | system.alert
  ├─ priority: critical | high | normal | low
  ├─ data: JSON (template 변수)
  └─ created_at

UserNotificationPreference (사용자 1 → N preferences)
  ├─ user_id
  ├─ event_type (또는 category)
  ├─ channels: [push, email]   (선호 채널 배열)
  ├─ enabled: bool
  └─ quiet_hours: 22:00-08:00  (선택)

NotificationDelivery (Intent → 여러 채널 시도 추적)
  ├─ intent_id
  ├─ channel: push | email | sms
  ├─ provider: fcm | ses | twilio
  ├─ status: queued | sent | delivered | failed | bounced
  ├─ provider_message_id
  └─ attempt_n
```

**핵심 원칙**:
- **Intent 1개 → Delivery N개** (다채널, 재시도)
- **Preference는 사용자가 변경 가능** (UI 제공 필수)
- **Delivery 추적**으로 디버깅/지표 산출

---

## 3. 라우팅 & Fallback Chain

### Critical 알림 (결제 실패, 보안 이상)

```
1. Push (즉시 시도)
   └─ 실패 (디바이스 없음/expired) → Step 2
2. SMS (Push fallback)
   └─ 실패 → Step 3
3. Email (최종 보장)
```

### Normal 알림 (마케팅, 일반)

```
1. User Preference 채널 (예: Email만)
   └─ 실패 → Retry 3회 (Exponential backoff)
   └─ 그래도 실패 → DLQ로 보내고 Alert
```

### 운영 알림 (CI 실패, 시스템 이상)

```
Slack 채널만. SMS/Push 사용 X (소음).
```

**핵심**:
- **Critical은 Fallback 강함**, Normal은 사용자 선호 존중
- **Quiet Hours 존중** — 사용자가 설정한 시간엔 보내지 않음 (Critical 예외)
- **Rate Limit 사용자별** — 1시간 100건 등 (스팸 방지)

---

## 4. Provider 결정 매트릭스

### Push (Mobile/Web)

| Provider | 적합 |
|---|---|
| **FCM (Firebase Cloud Messaging)** | iOS+Android+Web 통합. 무료. 기본 선택. |
| **APNs 직접** | iOS 전용. FCM 거치지 않음. 엔터프라이즈/규제. |
| **OneSignal** | 다채널 통합 SaaS. 작은 팀에 빠름. |
| **Pusher / Ably** | 실시간 (in-app) 위주. WebSocket 기반. |

### Email

| Provider | 적합 |
|---|---|
| **AWS SES** | 가성비 ($0.10/1000), 인프라 통합 시 1순위 |
| **SendGrid** | 템플릿/분석 강함. 마케팅 이메일 |
| **Postmark** | Transactional 전문. 도착률 우수 |
| **Resend** | DX 우수, Next.js 생태계 |

### SMS

| Provider | 적합 |
|---|---|
| **Twilio** | 글로벌 표준 |
| **NHN Cloud (구 토스트)** | 한국 시장 가성비 |
| **Aligo / Coolsms** | 한국 시장, 알리미톡 가능 |
| **AWS SNS** | 인프라 통합. 한국 SMS는 약함 |

> **한국 시장 팁**: SMS 대신 **카카오 알림톡** (정보성)이 가성비 + UX 우수. 친구톡(마케팅)은 별도 정책.
> Provider: NHN Cloud, Aligo, Bizppurio.

---

## 5. Template 관리

### Anti-pattern: 코드 안에 하드코딩

```python
# BAD
send_email(user.email, f"안녕하세요 {user.name}님, 주문이 완료되었습니다...")
```

### Pattern: 템플릿 분리

```
templates/
  ├─ order.paid/
  │   ├─ push.json    (title, body)
  │   ├─ email.html   (HTML 템플릿)
  │   ├─ email.txt    (Plain text fallback)
  │   ├─ sms.txt      (90자 이내)
  │   └─ slack.json   (Block Kit)
  └─ ...
```

**채널별 차이 인정**:
- Push: 짧음 (제목 50자, 본문 100자)
- Email: 길고 풍부함 (HTML)
- SMS: 90자, 링크 포함 시 단축 URL
- Slack: Block Kit으로 인터랙티브

**i18n**: 사용자 locale 기반 템플릿 선택. Notification Service에서 처리, Application은 모름.

---

## 6. Notification Center (In-App)

웹/앱 안에서 보는 알림 목록 (Bell 아이콘).

```
NotificationCenter API:
  GET  /notifications           (사용자의 최근 N개)
  POST /notifications/:id/read  (읽음 처리)
  POST /notifications/read-all  (전체 읽음)
  GET  /notifications/unread-count

DB 모델:
  InAppNotification
    ├─ id, user_id
    ├─ title, body, link
    ├─ icon, category
    ├─ read_at (null 또는 timestamp)
    └─ created_at
```

**실시간 갱신**:
- WebSocket / SSE (Server-Sent Events)
- 또는 폴링 (30초 간격)

**라이브러리**: Knock, Courier, Novu가 React/Mobile 컴포넌트 제공.

---

## 7. Digest / Batching (소음 줄이기)

### 사례

> 사용자 A가 1시간에 게시글 50개에 댓글 받음 → 알림 50개 보내면 안 됨

### Digest 패턴

```
1. Comment 이벤트 발생 → Notification Service
2. Service: "이 사용자에게 최근 1시간 내 같은 카테고리 알림 N개 있는가?"
3. 5개 이상 → Digest 모드로 전환
4. 1시간마다 모은 N개를 1통의 알림으로 발송
   "최근 1시간 동안 47개의 새 댓글이 있어요"
```

**구현**:
- Redis ZSET (시간 기반 sorted)으로 sliding window
- 백그라운드 Cron으로 1시간마다 flush
- 사용자가 수동으로 "즉시 받기" 모드 선택 가능

---

## 8. 안티패턴 모음

| 안티패턴 | 위험 | 올바른 방법 |
|---|---|---|
| Application이 직접 SES/FCM 호출 | 채널 추가 시 Application 변경 | Notification Service 추상화 |
| User Preference 무시 | GDPR 위반, 신뢰 ↓ | UI로 사용자 제어 가능 |
| 동기 발송 (요청-응답 안에서) | API 응답 지연, 실패 시 사용자 영향 | 큐 위임, 비동기 |
| 템플릿 코드 하드코딩 | 비개발자 변경 불가 | 별도 템플릿 파일 + i18n |
| Quiet Hours 무시 | 사용자 신뢰 ↓ | 시간대 존중 (critical 예외) |
| 같은 알림 중복 발송 | 사용자 짜증 | Idempotency key |
| SMS로 마케팅 (한국) | 정보통신망법 위반 | 정보성만 (광고는 별도 동의) |
| 실패 시 무한 재시도 | DLQ 폭주 | 3회 후 DLQ + Alert |

---

## 9. 한국 시장 — 카카오 알림톡

```
정보성 알림 → 알림톡 (가성비 좋음, 차단 불가)
마케팅 알림 → 친구톡 (사용자 동의 필수)

Provider: NHN Cloud, Aligo, Bizppurio
Template 사전 등록 (카카오 심사 필요)
```

**주의**:
- 알림톡 ≠ SMS. 카카오톡 친구가 아닌 사용자에겐 미발송 → SMS fallback 필요
- Template 변경 시 재심사 (1~3일)

---

## 10. 보안 / 개인정보

- **PII 로깅 금지** — 이메일/전화번호를 평문 로그에 남기지 않음
- **Provider 응답 raw 저장 시 마스킹** — Twilio/SES 응답에 전화번호/이메일 포함됨
- **Unsubscribe 링크 필수** — 마케팅 이메일은 법적 의무 (GDPR/CAN-SPAM/한국 정보통신망법)
- **Rate Limit 사용자별** — 알림 폭주 (악성 또는 버그) 시 사용자 보호
- **Provider Secret** — 환경변수/Secret Manager (코드 X)

---

## 11. ADR 템플릿 — 알림 시스템 결정

```markdown
## 알림 ADR

| 항목 | 결정 | 대안 | 근거 |
|---|---|---|---|
| Push Provider | FCM | OneSignal | 무료 + 통합 |
| Email Provider | SES | SendGrid | 가성비 |
| SMS Provider | NHN Cloud + 알림톡 | Twilio | 한국 시장 |
| 큐 | Redis Streams | Kafka / SQS | 기존 인프라 |
| Notification Center | 자체 + WebSocket | Knock SaaS | 비용 |
| Fallback Chain | Critical만 (Push→SMS→Email) | 모든 알림 | 비용 |
| Digest | 댓글/좋아요 1시간 배치 | 즉시 | UX |
```

---

## 12. Quick Start Checklist

- [ ] Provider 결정 (Push/Email/SMS 매트릭스)
- [ ] Notification Service 별도 모듈 (Application 분리)
- [ ] NotificationIntent + Delivery 도메인 모델
- [ ] UserNotificationPreference UI
- [ ] Template 파일 분리 (i18n 고려)
- [ ] Channel Adapter 인터페이스 (PushAdapter, EmailAdapter, ...)
- [ ] Fallback Chain 정책 (Critical/Normal/Operational)
- [ ] Idempotency key (중복 방지)
- [ ] Rate Limit (사용자별)
- [ ] Quiet Hours 존중
- [ ] Digest/Batching (필요 시)
- [ ] Notification Center API + 실시간 갱신
- [ ] 모니터링: 채널별 성공률/지연/bounce, 사용자 unsubscribe 비율
- [ ] Unsubscribe 링크 (법적 의무)

---

## 13. 관련 자원

**우리 시스템 내부**:
- `skills/msa/msa-event-driven.md` — 알림 의도를 이벤트로 발행
- `skills/msa/task-queue.md` — 비동기 발송 큐
- `skills/messaging/redis-streams.md` — 큐 구현
- `skills/messaging/kafka.md` — 대규모 이벤트 (선택)
- `skills/observability/observability-otel.md` — 발송 지표/추적
- [`broker-troubleshooting`](../broker-troubleshooting/SKILL.md) — 큐 진단 / [`kafka-patterns`](../kafka-patterns/SKILL.md) — 큐 설계
- `agents/architect-agent` — 추상화 설계 위임

**외부 자원**:
- Knock (knock.app) — Notification Infrastructure SaaS 참고
- Courier (courier.com) — 통합 API SaaS
- Novu (novu.co) — Open-source 대안
- 카카오 비즈니스: https://business.kakao.com/

---

## 14. 다음 단계

1. **사용자 행동 트리거** → "마지막 로그인 7일 후 알림" 같은 행동 기반 → marketing automation tool 검토
2. **A/B 테스트 알림 카피** → Feature Flag와 결합 (P2: feature-flags)
3. **국가별 규제** → GDPR/CAN-SPAM/한국 정보통신망법 컴플라이언스 (`skills/security/compliance-frameworks.md`)
4. **알림 분석** → Open rate, Click rate, 채널별 ROI
