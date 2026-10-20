---
name: admin-api-keys
category: business
description: "Admin API Keys — API Keys / Personal Access Tokens / Service Tokens — 외부 통합·CLI·자동화·서비스 간 인증. 발급/회전/폐기, scope 권한, 안전 저장(hashing), prefix 노출, 이벤트 추적, Use when working with business 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Admin API Keys

API Keys / Personal Access Tokens / Service Tokens — 외부 통합·CLI·자동화·서비스 간 인증. 발급/회전/폐기, scope 권한, 안전 저장(hashing), prefix 노출, 이벤트 추적, rate limit 통합. SaaS 부트스트랩 필수.

세션 토큰 ≠ API Key. 사용자 브라우저 = 세션, 자동화/통합 = API Key. **유출되면 가장 위험한 자산** — 다층 방어 필요.

## When to Use

- 외부 통합 ("우리 SaaS API를 고객 앱이 호출")
- CLI 도구 (사용자가 PAT으로 인증)
- CI/CD에서 우리 API 호출
- Webhook 검증 (HMAC signing)
- Service-to-service 인증 (M2M, OAuth client_credentials 대안)
- Pro plan + 외부 API 액세스 차등

**관련 skill**: `business/auth-oauth-social.md`, `business/multi-tenancy.md`, `business/audit-log.md`, `business/rate-limiting.md`, `security/secure-coding.md`
**관련 agent**: `security-scanner`, `compliance-auditor`

---

## 1. 토큰 종류 분류

| 종류 | 발급 주체 | 소유자 | 만료 | 용도 |
|---|---|---|---|---|
| **Personal Access Token (PAT)** | 사용자 | 개인 | 90일~365일 | CLI, 개인 통합 |
| **Service Token / Bot Token** | Tenant Admin | 시스템/봇 | 무기한 또는 1년 | CI/CD, 서버 통합 |
| **OAuth Bearer Token** | OAuth flow | 사용자 | 1시간 (refresh) | Third-party app |
| **OAuth Client Credentials** | Tenant | 클라이언트 앱 | 1시간 | M2M (서버 ↔ 서버) |
| **Webhook Signing Secret** | Tenant | Endpoint | 영구 (rotate) | Webhook 페이로드 검증 |

> **선택 가이드**:
> - 사람이 사용 → PAT
> - 시스템이 사용 (CI 등) → Service Token (사용자와 분리, 사용자 퇴사 시 영향 X)
> - 외부 앱 → OAuth (사용자 동의 명시)

### Opaque vs JWT (자주 헷갈림)

| 측면 | **Opaque Token** (random + DB lookup) | **JWT** (self-contained, signed) |
|---|---|---|
| 검증 | DB 조회 필수 (1 round-trip) | 서명 검증만 (stateless) |
| 폐기 | 즉시 (DB 플래그) | **즉시 폐기 어려움** (만료까지 유효) → 블랙리스트 필요 |
| 페이로드 | 없음 (모두 DB) | 사용자/scope 내장 (자기서술) |
| 크기 | 작음 (~40 bytes) | 큼 (~수백 bytes, claims 따라 KB까지) |
| 회전 | 즉시 (DB 갱신) | refresh token 흐름 필요 |
| 분산/마이크로서비스 | DB 공유 필요 | service 간 검증 쉬움 (public key) |
| 적합 | **API Key (회전·폐기 자주)**, 세션 | service-to-service, OAuth access token |

> **API Key는 거의 항상 Opaque 권장**. JWT는 폐기가 어려워서 유출 시 만료까지 노출. 짧은 수명(15분)+refresh 흐름 아니면 부적합.

---

## 2. 토큰 포맷 (식별 가능 + 안전)

```
sk_live_xK7p9dQwR3mF2nL8vY4uT6sB1aE5cZ0iH9oNgX...
└┬─┘ └┬─┘ └────────────── 36+ chars random ──────────────┘
 │    │
 │    환경 (live / test)
 │
 prefix (sk = secret key, pk = public key, pat = personal)
```

**관행 (Stripe/GitHub 패턴)**:
- **prefix로 식별 가능** — `sk_live_`, `ghp_`, `xoxb_` 등. 시크릿 스캐너가 잡을 수 있음.
- **환경 표시** — live/test 분리, 사고 방지
- **충분한 entropy** — 최소 256-bit (32 bytes random base62)
- **prefix만 화면 노출** — 발급 후 1회만 전체 표시, 이후 `sk_live_xK7p...` 형태

**생성 코드 (의사)**:
```
random_bytes = secure_random(36)
encoded = base62(random_bytes)
token = "sk_live_" + encoded
prefix = token[:12]  // 식별용 (DB 저장)
hash = bcrypt(token, cost=12)  // 검증용 (DB 저장)
return token  // 사용자에게 1회만
```

---

## 3. 안전 저장 (Hashing)

> **DB에 raw 토큰 절대 저장 X**. 비밀번호와 동일.

```
api_keys 테이블:
  id
  tenant_id
  name              ("Production CI Bot")
  prefix            ("sk_live_xK7p")  ← 식별/검색용
  hash              (bcrypt/argon2)   ← 검증용
  scopes            (JSON: ["read:users", "write:orders"])
  expires_at
  last_used_at
  last_used_ip
  created_by
  revoked_at
```

**검증 흐름**:
```
요청 헤더: Authorization: Bearer sk_live_xK7p9dQwR...
  ↓
1. prefix 추출 → DB SELECT WHERE prefix = ?
   (인덱스 빠름, full hash compare 회피)
2. bcrypt.verify(token, row.hash) → 일치 확인
3. expires_at, revoked_at 체크
4. scope 검증
5. last_used_at, last_used_ip 업데이트 (비동기)
```

**대안: HMAC-SHA256**:
- bcrypt는 느림 (의도적). 매 요청마다 100ms는 부담.
- **PAT는 bcrypt** (저빈도 사용)
- **Service token은 HMAC-SHA256(pepper)** (고빈도, 빠름) + Redis 캐시

---

## 4. Scope (권한) 설계

```
스코프 네이밍: <action>:<resource>

예시:
  read:users          users 읽기
  write:users         users 쓰기/삭제
  read:orders
  write:orders
  admin:tenant        tenant 설정 변경
  admin:billing       결제 관련
  webhooks:manage     webhook CRUD
  *                   전체 (위험, 발급 신중)
```

**원칙**:
- **최소 권한** — 발급 시 명시 선택, 기본값 X
- **Resource 단위 분리** — `read:users`와 `write:users` 구분
- **Admin scope는 별도** — 일반 PAT는 admin scope 발급 불가
- **Custom scope 가능** — 큰 SaaS는 사용자 정의 (Stripe Restricted Keys)

### 검증

```
endpoint 요구: scope = "write:orders"
token scope: ["read:users", "read:orders"]
→ 거부 (403 Forbidden + 부족한 scope 명시)
```

---

## 5. Token 사용 패턴

### 인증 헤더

```http
Authorization: Bearer sk_live_xK7p9dQwR...
```

> Basic Auth 사용 X (URL 인코딩 깨짐, 로깅 위험)

### URL 파라미터로 절대 X

```
❌ GET /users?api_key=sk_live_...
   → 액세스 로그, 브라우저 history, referrer 헤더 유출
```

### Webhook Signing

```
Server: payload + secret → HMAC-SHA256 → "X-Signature"
Client: 수신 후 동일하게 계산, timing-safe compare
```

→ 결제 webhook 검증: [.claude/skills/business/payment-integration.md](../payment-integration/SKILL.md)

---

## 6. Lifecycle 관리

### 발급 (Create)

```
사용자/Admin → "API Key 발급" UI
  ↓
1. name, scopes, expires_at 입력
2. 서버: token 생성 + hash 저장
3. 1회만 전체 토큰 화면 표시 ("두 번 다시 못 봅니다")
4. audit log: api_key.created
5. 알림: 같은 tenant Owner들에게 "X님이 새 키 발급"
```

### 회전 (Rotate) — Zero-Downtime 운영 흐름

```
사용자 → "Rotate" 클릭
  ↓
1. 새 token 발급 + 표시 (기존 token은 아직 유효)
2. 사용자가 코드/CI/secrets store 업데이트 (배포 진행)
3. 모니터링: 기존 prefix 사용 카운트 감시 → 0 도달 확인
4. 기존 token: rotated_at 기록 + 즉시 폐기 (또는 grace 후)
5. audit log: api_key.rotated
```

**Grace Period 패턴** (권장):
- 기본 24h dual-support (두 키 동시 유효)
- 사용자가 "이전 키 즉시 폐기" 버튼으로 수동 단축 가능 (유출 의심 시)
- Grace 중 기존 키 사용 시 응답 헤더에 `Deprecation: <rotated_at>`, `Sunset: <expiry>` 노출 → 클라이언트가 자동 알림

**Bad pattern** (피하기):
```
회전 = "기존 키 즉시 폐기 + 새 키 발급"
  → 배포 타이밍 어긋나면 prod 다운
  → 사용자가 회전 회피 → 키 노화 → 영구 위험
```

**자동 회전 알림 스케줄**:
- 만료 30일 전 — Email (Owner)
- 만료 7일 전 — Email + Slack
- 만료 1일 전 — Slack mention + 모니터링 critical 알림
- 만료 후 — 자동 폐기 + 사후 알림 ("키가 폐기되어 N개 요청 401 발생")

### 폐기 (Revoke)

```
즉시 사유:
  - 유출 의심 (gitleaks 탐지)
  - 사용자 퇴사
  - 의심 행위 (deny 5회 + 새벽 활동)

자동 폐기 트리거:
  - 30일 미사용 → Owner 알림 → 응답 없으면 자동 폐기
  - last_used_ip 갑자기 다른 국가 → 의심 알림 + 토큰 일시 정지
```

---

## 7. Multi-Tenancy 통합

```
PAT: 사용자 소유 → "이 사용자가 속한 모든 tenant" 액세스 가능
     OR (권장) tenant_id 명시 — "이 토큰은 tenant X 전용"

Service Token: 항상 tenant 단위 발급
```

**권장**: PAT도 tenant 명시 — token 자체에 tenant_id 바인딩.
이유: 사용자가 N개 tenant 멤버일 때, 한 토큰으로 다른 tenant 데이터 접근 위험.

→ multi-tenancy: [.claude/skills/business/multi-tenancy.md](../multi-tenancy/SKILL.md)

---

## 8. Rate Limiting 통합

```
Limit 키 우선순위:
  1) per_api_key   ← 가장 정확
  2) per_tenant
  3) per_ip
```

- Service token은 일반적으로 PAT보다 ↑ limit (자동화 워크로드)
- Pro 플랜 키 > Free 플랜 키
- Endpoint별 차등 (login은 별도 key 단위 limit X — 봇 탐지 우회 위험)

→ rate limiting: [.claude/skills/business/rate-limiting.md](../rate-limiting/SKILL.md)

---

## 9. 유출 대응 (Compromise Response)

### 자동 탐지

- **Secret scanner 통합**: GitHub Secret Scanning → 자동 webhook → 즉시 폐기
- **이상 행위**: 갑작스런 IP 변경, 새 endpoint 호출 패턴 → 알림
- **거부율 spike**: scope 외 endpoint 시도

### 알림 채널 (다층)

```
1. Email — Owner / 발급자
2. Slack — #security 채널
3. In-app banner — "키 유출 의심, 폐기됨"
4. Audit log + incident ticket 자동 생성
```

### 사후 조치

- 폐기된 키로 마지막 7일 이벤트 reconstruct
- 영향 범위 산정 (어떤 데이터 조회/변경됐는지)
- GDPR 대상이면 사용자 통지 필요

→ incident: [.claude/skills/observability/observability-incident-playbook.md](../observability-incident-playbook/SKILL.md)

---

## 10. 안티패턴

| 안티패턴 | 위험 | 올바른 방법 |
|---|---|---|
| Raw 토큰 DB 저장 | DB 유출 = 전체 키 유출 | bcrypt/argon2/HMAC hash |
| URL 파라미터로 전달 | 로그/referrer 유출 | Authorization 헤더 |
| 만료 없음 | 영구 위험 | 90일~365일, 자동 알림 |
| Scope 없이 발급 (`*`) | 최소 권한 위반 | 명시 선택 강제 |
| 발급 시 audit 없음 | 추적 불가 | api_key.created 이벤트 |
| 발급/회전 알림 없음 | 모르고 지나감 | Owner에게 즉시 통지 |
| prefix로 식별 X | 시크릿 스캐너 미탐지 | `sk_live_` 같은 prefix |
| live/test 같은 키 | 사고 시 prod 영향 | 환경 분리 |
| 로그에 토큰 출력 | 내부자 유출 | 마스킹 (`sk_live_xK7p...`) |
| Owner 외 발급 권한 | 무분별 생성 | Admin 권한 + scope 제한 |
| 사용 통계 없음 | 미사용 키 누적 | last_used_at + 30일 알림 |
| 회전 어려움 (grace period X) | 회전 회피 → 키 노화 | 24h grace + dual support |
| Rate limit 통합 X | 키 단위 abuse 무방 | per-key limit |
| 유출 자동 폐기 X | 대응 지연 | GitHub Secret Scanning 통합 |

---

## 11. 모니터링

```
지표:
  api_key_authentications_total{result="success|failed", reason}
  api_key_active_count{tenant}
  api_key_unused_30d_count
  api_key_age_days_p99
  api_key_rotation_overdue_count

알림:
  - 인증 실패율 > 5% (brute force 또는 키 변경 누락)
  - 30일 미사용 키 > N% → Owner 정리 알림
  - 만료 임박 (7일) — Owner에게 회전 요청
  - 새로운 IP/국가에서 사용 → 의심 알림
  - scope 밖 endpoint 시도 (10회+) → 즉시 알림
```

---

## 12. UI/UX

### API Key 관리 페이지

```
조직 설정 → API Keys
  ├─ 활성 키 목록 (name, prefix, scopes, last_used, expires)
  ├─ "새 키 발급" 버튼
  ├─ 발급 시: scope 선택, 만료일, name
  ├─ 발급 직후: 1회 전체 토큰 + "복사 후 안전한 곳에 저장" 경고
  ├─ Rotate / Revoke 버튼
  └─ 사용 이력 (마지막 N일 호출 수, 에러율)
```

**UX 원칙**:
- 발급 직후 화면을 떠나면 토큰 다시 못 봄 (강조)
- "복사" 버튼은 1회 누르면 비활성화 + 마스킹
- prefix는 항상 보이게 (구분용)
- Service token은 발급자/소유자 분리 노출

---

## 13. ADR 템플릿 — API Key 결정

```markdown
## API Key ADR

| 항목 | 결정 | 대안 | 근거 |
|---|---|---|---|
| 토큰 종류 | PAT + Service Token 분리 | 단일 | 사람·봇 분리, 퇴사 영향↓ |
| 포맷 | sk_live_<base62> + prefix | UUID | 시크릿 스캐너 호환 |
| 저장 | bcrypt(cost=12) + prefix index | raw / SHA256 | 비밀번호 수준 보안 |
| 검증 캐시 | Redis 5min (success만) | 매번 bcrypt | 성능 |
| Scope | resource × action 조합, 명시 발급 | `*` 기본 | 최소 권한 |
| Tenant 바인딩 | 토큰에 tenant_id 명시 | 사용자만 | cross-tenant 사고 방지 |
| 만료 | 90일 default + 자동 알림 | 무기한 | 위험 노출 ↓ |
| 회전 | 24h grace period | 즉시 폐기 | zero-downtime |
| 유출 대응 | GitHub Secret Scanning + 자동 폐기 | 수동 | 분 단위 노출 ↓ |
| Audit | 모든 lifecycle 이벤트 audit log | 없음 | 규제 + 추적 |
| Rate limit | per-key + per-tenant 결합 | per-tenant만 | abuse 방지 |
```

---

## 14. Quick Start Checklist

- [ ] API Key ADR (종류/포맷/저장/회전 정책)
- [ ] 토큰 포맷 (`sk_live_` prefix + base62 256-bit)
- [ ] 저장 방식 (bcrypt/argon2 + prefix index)
- [ ] Scope 시스템 (resource × action)
- [ ] api_keys 테이블 + 인덱스 (prefix, tenant_id)
- [ ] 발급 플로우 (1회 노출, 복사 강조)
- [ ] 회전 플로우 (grace period)
- [ ] 폐기 (즉시 + 사후 분석)
- [ ] 만료 정책 + 알림 (30일/7일/1일 전)
- [ ] Audit log 통합 (created/rotated/revoked/used)
- [ ] Rate limit 통합 (per-key)
- [ ] Multi-tenancy 바인딩
- [ ] GitHub Secret Scanning 연동
- [ ] 이상 행위 탐지 (IP 변경, scope 외 시도)
- [ ] 모니터링 + 알림
- [ ] UI: Key 관리 페이지 + 사용 통계
- [ ] CLI/SDK 가이드 (안전한 보관)

---

## 15. 관련 자원

**우리 시스템 내부**:
- `skills/business/auth-oauth-social.md` — 사용자 인증 (대비)
- `skills/business/multi-tenancy.md` — tenant 바인딩
- `skills/business/audit-log.md` — lifecycle 추적
- `skills/business/rate-limiting.md` — per-key limit
- `skills/business/feature-flags.md` — flag 변경 권한
- `skills/business/payment-integration.md` — webhook signing
- `skills/security/secure-coding.md` — 시크릿 처리
- `skills/security/auth-patterns.md` — JWT/OAuth 패턴
- `agents/security-scanner` — 유출 탐지
- `agents/compliance-auditor` — 규제 매핑

**외부 자원**:
- Stripe API Keys docs (포맷 참고)
- GitHub PAT scopes (scope 설계 참고)
- GitHub Secret Scanning (탐지 통합)
- OAuth 2.1 RFC (Bearer token)
- OWASP API Security Top 10

---

## 16. 다음 단계

1. **Workload Identity (M2M)** — SPIFFE/SPIRE, OAuth client_credentials 대체
2. **mTLS 옵션** — Service token + 클라이언트 인증서 결합
3. **Just-In-Time tokens** — 단명(15분) + 자동 발급 (vault)
4. **Capability-based** — scope을 capability로 (Macaroons 등)
5. **Marketplace integration** — OAuth App 등록 + 사용자 동의 흐름
