---
name: auth-oauth-social
category: business
description: "OAuth Social Login — OAuth 2.0 / OIDC 소셜 로그인 통합 — Google/Apple/Kakao, PKCE, State CSRF 방지, Magic Link, 2FA. 한국 시장 우선 (Kakao) + 글로벌. 신규 SaaS 인증 부트스트랩. Use when working with business 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# OAuth Social Login

OAuth 2.0 / OIDC 소셜 로그인 통합 — Google/Apple/Kakao, PKCE, State CSRF 방지, Magic Link, 2FA. 한국 시장 우선 (Kakao) + 글로벌. 신규 SaaS 인증 부트스트랩.

신규 SaaS/서비스 인증을 0에서 만들지 않도록 검증된 OAuth/OIDC 통합 패턴.
**Kakao 우선 (한국 시장)** + Google/Apple (글로벌) + Magic Link/Passkey 옵션.

## When to Use

- 통학차량/심리상담 같은 신규 도메인에 로그인 붙이기
- "회원가입 폼 만들지 vs 소셜만 갈지" 결정
- 한국 시장 → Kakao 필수, B2C SaaS 표준
- 글로벌 → Google + Apple
- 모바일 앱 → PKCE 필수
- 비밀번호 없이 → Magic Link / Passkey

**관련 skill**: `security/auth-patterns.md`, `security/secure-coding.md`, `security/owasp-top10.md`
**관련 agent**: `security-scanner` (구현 후 검증)

---

## 1. Provider 결정 매트릭스

| 시장 / 사용자 | 1순위 | 2순위 | 비고 |
|---|---|---|---|
| 한국 B2C | **Kakao** | Naver, Apple | Kakao 점유율 높음. Naver는 시니어 층 |
| 한국 + 글로벌 | **Kakao + Google** | Apple | iOS는 Apple 필수 (App Store 정책) |
| 글로벌 B2C | **Google** | Apple, Facebook | Apple은 iOS 앱 시 필수 |
| B2B SaaS | **Google Workspace** | Microsoft, LinkedIn | 회사 계정 활용 |
| 개발자 도구 | **GitHub** | GitLab, Google | 개발자 친화 |
| 비밀번호 거부 | **Magic Link** | Passkey | 이메일만 있으면 됨 |

> **Apple Sign In 정책**: iOS 앱이 다른 소셜 로그인 제공 시 **Apple도 필수 제공**. App Store Review 거절 사유 1순위.

---

## 2. OAuth 2.0 Flow 선택

### Authorization Code + PKCE (현대 표준, 모든 케이스)

```
1. Client → Generate code_verifier (random 43-128자) + code_challenge (SHA256)
2. Client → /authorize?code_challenge=...&state=<csrf-random>
3. User → Provider 동의 화면
4. Provider → Client redirect_uri?code=...&state=<csrf-random>
5. Client → state 검증 (CSRF 방지)
6. Client → /token endpoint (code + code_verifier 전달)
7. Provider → access_token + id_token + refresh_token 반환
8. Client → id_token 검증 (서명/iss/aud/exp)
9. Server → 우리 시스템에 사용자 등록/로그인
```

**금지 Flow**:
- ❌ Implicit Flow (`response_type=token`) — 토큰 URL 노출, deprecated
- ❌ Resource Owner Password — 비밀번호 직접 받음, 소셜 로그인 의미 상실
- ❌ Client Credentials — 사용자 인증이 아닌 머신 간 인증용

### Mobile App / SPA → 반드시 PKCE

PKCE 없으면:
- 인가 코드 가로채기 공격(authorization code interception) 가능
- iOS/Android URL scheme 가로채기

---

## 3. CSRF 방지 — `state` 파라미터

```
Client (서버 사이드):
  state = secure_random(32 bytes, base64url)
  session.set("oauth_state", state)
  redirect → /authorize?state=<state>

Provider:
  redirect → /callback?code=...&state=<state>

Client (callback):
  if request.state != session.get("oauth_state"):
    throw "CSRF detected"
  session.delete("oauth_state")
  // continue with code
```

**핵심**:
- state는 **서버 세션에 저장** (쿠키 단독 X)
- 사용 후 즉시 삭제 (재사용 방지)
- Provider별로 다 다른 state 사용

---

## 4. id_token 검증 (OIDC)

Provider가 반환한 `id_token` (JWT)을 **반드시 서버에서 검증**:

```
1. JWT 서명 검증 (Provider의 JWKS 공개키)
2. iss (issuer) == 예상 Provider URL
3. aud (audience) == 우리 client_id
4. exp (expiry) > 현재 시각
5. nonce (있다면) == 우리가 보낸 nonce
6. email_verified == true (Google/Apple은 이 필드 제공)
```

**라이브러리 사용 권장** (직접 구현 X):
- Node.js: `openid-client`, `passport-openidconnect`
- Java: `nimbus-jose-jwt`, Spring Security OAuth2
- Python: `authlib`
- Go: `coreos/go-oidc`

---

## 5. 사용자 매칭 전략

### Strategy A — Email 기반 자동 매칭 (편함, 위험)

```
이메일 같으면 같은 사용자로 매칭
→ Provider A로 가입, Provider B로 로그인 시 자동 연결
→ 위험: Provider가 email_verified=false면 계정 탈취 가능
```

**보안 조건**: Provider의 `email_verified == true`만 허용.

### Strategy B — 명시적 연결 (안전)

```
Provider A로 가입 → user_id 발급
Provider B로 로그인 시:
  - 동일 이메일 발견 → "기존 계정과 연결할까요?" 물음
  - 본인 인증 (기존 Provider로 한 번 더 로그인) 후 연결
```

**B2C/SaaS는 Strategy B 권장**. 보안 사고 예방.

### 사용자 데이터 모델

```
User (1) ── (N) SocialIdentity
              ├─ provider: kakao | google | apple
              ├─ provider_user_id (Provider 고유 ID, 변경 안 됨)
              ├─ email (Provider 응답, 변경 가능)
              └─ created_at

User:
  ├─ id (uuid)
  ├─ email (primary, 변경 가능)
  ├─ email_verified
  └─ ...
```

**핵심**: `provider_user_id`로 매칭 (이메일 변경되어도 같은 사람).

---

## 6. Provider별 핵심 주의사항

### Kakao

```
Endpoint: https://kauth.kakao.com/oauth/authorize, /token
Scope: profile_nickname, profile_image, account_email
주의:
  - email은 사용자가 동의해야 받을 수 있음 (필수 동의 X 가능)
  - 비즈 앱 전환 필요 (이메일 받으려면)
  - id_token 발급 안 함 (OIDC 미완전 지원, 자체 user info API 사용)
  - 상세: https://developers.kakao.com/docs/latest/ko/kakaologin/common
```

### Google

```
Endpoint: https://accounts.google.com/o/oauth2/v2/auth
Scope: openid email profile
주의:
  - OIDC 완전 지원 (id_token 사용)
  - One Tap UI 권장 (sign-in 마찰 ↓)
  - hd 파라미터로 Workspace 도메인 제한 가능 (B2B)
```

### Apple

```
Endpoint: https://appleid.apple.com/auth/authorize
Scope: email name
주의:
  - email 첫 로그인 시 한 번만 제공 (이후 호출 X) → 반드시 첫 응답에서 저장
  - Private Relay 이메일 (랜덤 @privaterelay.appleid.com) 처리
  - JWT client_secret 매 6개월 갱신 필요
  - iOS 앱 시 다른 소셜 로그인 제공하면 Apple도 필수
```

### Naver (한국)

```
Endpoint: https://nid.naver.com/oauth2.0/authorize
주의:
  - id_token 미발급, user info API 사용
  - 시니어 층 사용자 많음 (B2C 카페/쇼핑몰 시 고려)
```

---

## 7. Magic Link (비밀번호 없는 로그인)

비밀번호 거부 + 소셜 의존 회피:

```
1. User → /login?email=foo@bar.com
2. Server → token = signed_jwt(email, exp=15min, nonce=random)
3. Server → Email "Click to login: https://app/auth?t=<token>"
4. User → Click link
5. Server → token 검증 (서명/exp/nonce 1회 사용)
6. Server → 세션 발급
```

**핵심**:
- Token exp **15분 이내** (24시간은 위험)
- nonce **1회 사용** (재사용 방지, Redis SET)
- Rate limit (이메일당 분당 1회)
- 외부 노출 link → "최근 N분 안에 요청한 기기에서만 동작" 체크 (선택)

**라이브러리**: Clerk, Supabase Auth, Auth0, NextAuth가 내장.

---

## 8. 2FA / Passkey (강한 인증)

### 2FA (TOTP)

```
가입 시 → QR 코드 (otpauth://...) 표시 → Google Authenticator 등록
로그인 시 → 비밀번호 입력 → 6자리 OTP 입력
백업 코드 8~10개 발급 (분실 대비)
```

**관리자/결제 권한 사용자에게 필수화** 권장.

### Passkey (WebAuthn) — 2026 표준 향하는 중

```
가입 시 → 디바이스 생체인증 등록 (지문/Face ID)
로그인 시 → 디바이스 인증으로 즉시 로그인
```

**장점**: Phishing 면역, 비밀번호 없음.
**단점**: 디바이스 종속 (다중 디바이스 등록 필요).

→ 라이브러리: `simplewebauthn/server` (Node.js), `webauthn4j` (Java).

---

## 9. 토큰 저장 — 어디에?

| 토큰 | 저장 위치 | 이유 |
|---|---|---|
| **Session token** | HttpOnly + Secure + SameSite=Lax/Strict 쿠키 | XSS 면역 |
| **Refresh token** | HttpOnly 쿠키 또는 서버 세션 DB | 클라이언트 노출 X |
| **Access token (JWT)** | 메모리 (변수) — **LocalStorage 절대 X** | XSS 시 탈취 |
| **id_token** | 검증 후 폐기 | 1회용 |
| **Provider refresh token** | 서버 사이드 암호화 저장 | API 위임 호출 시 사용 |

**금지**:
- ❌ JWT를 LocalStorage 저장 (XSS 1방에 탈취)
- ❌ Refresh token을 클라이언트 JS에서 접근 가능하게
- ❌ 평문 Provider refresh token 저장

---

## 10. 안티패턴 모음

| 안티패턴 | 위험 | 올바른 방법 |
|---|---|---|
| state 파라미터 생략 | CSRF 공격 | secure_random, 세션 저장 |
| id_token 클라이언트 검증만 | 위변조 가능 | 서버에서 서명+iss+aud 검증 |
| email 자동 매칭 무조건 | 계정 탈취 (email_verified=false) | email_verified 체크 또는 명시 연결 |
| Apple email 첫 응답 후 무시 | 영구 손실 | 첫 응답에서 즉시 저장 |
| Implicit Flow 사용 | 토큰 URL 노출 | Authorization Code + PKCE |
| client_secret 모바일 앱에 | 디컴파일로 노출 | PKCE만 사용 (secret 없음) |
| Magic Link 24시간 만료 | 이메일 가로채기 시 위험 | 15분 + 1회 사용 |
| LocalStorage에 토큰 | XSS 즉시 탈취 | HttpOnly 쿠키 또는 메모리 |

---

## 11. ADR 템플릿 — 인증 결정

```markdown
## 인증 ADR

| 항목 | 결정 | 대안 | 근거 |
|---|---|---|---|
| Provider | Kakao + Google + Apple | Kakao만 / 다 | 한국+글로벌 + iOS 정책 |
| Flow | Authorization Code + PKCE | Implicit | 모바일 + SPA 표준 |
| 사용자 매칭 | email_verified + 명시 연결 | 자동 매칭 | 보안 |
| 토큰 저장 | Session = HttpOnly 쿠키 | LocalStorage JWT | XSS 방어 |
| 2FA | Admin/결제권한 사용자 필수 | 전체 옵션 | 보안 vs UX 균형 |
| Magic Link | 도입 안 함 (V2) | 즉시 도입 | MVP 범위 축소 |
```

→ `agents/tech-lead` 호출하여 ADR 작성.

---

## 12. Quick Start Checklist (신규 프로젝트)

- [ ] Provider 결정 (시장/플랫폼 매트릭스)
- [ ] OAuth 라이브러리 선택 (직접 구현 X)
- [ ] PKCE 활성화 (모바일/SPA)
- [ ] state 파라미터 + CSRF 방지
- [ ] id_token 서버 검증
- [ ] 사용자 매칭 전략 결정 (Strategy A vs B)
- [ ] User + SocialIdentity 도메인 모델
- [ ] Apple email 첫 응답 즉시 저장 로직
- [ ] Kakao 비즈 앱 전환 (이메일 필요 시)
- [ ] HttpOnly 쿠키 + Secure + SameSite 설정
- [ ] Refresh token 회전 (rotation)
- [ ] 로그아웃 시 토큰 즉시 무효화
- [ ] Rate limit (로그인 시도, OTP 시도)
- [ ] 2FA 옵션 (관리자/결제권한 강제)

---

## 13. 관련 자원

**우리 시스템 내부**:
- `skills/security/auth-patterns.md` — 일반 인증 패턴
- `skills/security/secure-coding.md` — 입력 검증
- `skills/security/owasp-top10.md` — A07: Identification & Auth Failures
- `skills/platform/secrets-management.md` — Provider Secret 관리
- `skills/business/multi-tenancy.md` — Org 컨텍스트와 결합 (P1)
- `agents/security-scanner` — 구현 후 보안 검증
- `rules/security.md` — 보안 룰

**외부 표준**:
- OAuth 2.1 (RFC 9700, 2025) — Implicit/Password Flow deprecated 명시
- OIDC Core 1.0
- WebAuthn Level 3
- Kakao Login Docs / Google Identity / Apple Sign In with Apple

---

## 14. 다음 단계

1. **B2B 회사 인증** → SAML/SSO 도입 (이 skill 범위 밖, 별도 skill 필요 시)
2. **권한 관리** → RBAC/ABAC 패턴 (`skills/security/auth-patterns.md`)
3. **세션 관리** → Redis 세션 스토어 (`skills/messaging/redis-streams.md` 참조)
4. **Audit Log** → 로그인 이벤트 기록 (P2 예정)
