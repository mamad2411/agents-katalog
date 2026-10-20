---
name: child-data-protection
category: legal
description: 만14세 미만 아동 개인정보·위치정보 처리 — 법정대리인 동의 검증, 추적 사실 가시화, 가족 계정 모델, 데이터 최소화, 미성년 채팅 모더레이션, 광고/마케팅 금지. 한국 PIPA 제22조의2 + 위치정보법 결합 + COPPA/GDPR Art.8 비교. 통학·교육·소셜·헬스케어 SaaS 필수.
license: MIT
---

# Child Data Protection — 만14세 미만 아동 데이터 보호

만14세 미만 아동은 일반 사용자와 다른 운영 룰이 적용된다. 법정대리인 동의가 디폴트가 아니라 "**검증 가능한** 동의 + **추적 가시화** + **데이터 최소화** + **광고 금지**"가 묶음으로 와야 한다. 학교·기관의 일괄 동의로 갈음할 수 없다.

> 이 skill은 한국 기준 hub. 위치정보 결합은 `legal/kr-location-info-act.md`, 권리 행사(DSR)는 `legal/data-subject-rights.md`. COPPA(미국)·GDPR Art.8(EU)와 차이점을 §2 매트릭스에 정리.

## When to Use

- 통학차량/학원/유치원/어린이집/교육 SaaS 설계
- 미성년자 소셜 (채팅·게임·SNS) 모더레이션 정책
- 헬스케어·심리상담 (소아·청소년) 동의 흐름
- 부모-자녀 가족 계정 모델 설계
- 학교·기관 통합 동의의 적법성 검토
- COPPA/GDPR/PIPA 멀티 리전 운영
- 14세 생일 도래 시 권한 이양 처리
- 분리 가족(이혼·조부모 양육) 동의 주체 결정

**관련 skill (cross-link)**:
- `legal/kr-location-info-act.md` — 위치정보 결합 (§3.3)
- `legal/data-subject-rights.md` — 자녀 정보에 대한 부모 권리 행사
- `business/audit-log.md` — 동의·철회·접근 기록
- `business/auth-oauth-social.md` — 본인확인(PASS) 통합
- `business/multi-tenancy.md` — 학원/학교 단위 격리
- `business/notification-multichannel.md` — 추적 가시화 알림
- `security/auth-patterns.md` — 부모-자녀 권한 위임 모델
- `frontend/css-design-system.md` — 동의 UX 일관성

**관련 agent**: `compliance-auditor`, `tech-lead`, `frontend-expert`, `security-scanner`

---

## 1. 적용 결정 트리

```
대상 연령은?
    │
    ├─ 만8세 이하 ─────> 위치정보법 + PIPA — 가장 강한 보호
    │   └─ 법정대리인 동의 + 본인 인지 + 추적 가시화 + 광고 전면 금지
    │
    ├─ 만8세 ~ 14세 미만 ─> PIPA 제22조의2 — 법정대리인 동의 필수
    │   └─ 가입·서비스 이용 동의 모두 법정대리인
    │   └─ 위치 처리 결합 시 위치정보법 적용 (legal/kr-location-info-act.md)
    │
    ├─ 만14세 ~ 18세 ────> 본인 동의 가능
    │   └─ 단, 광고·마케팅·민감정보·신용 관련은 별도 보호자 동의
    │
    └─ 연령 미확인 ──────> 가입 차단
        └─ 본인확인(PASS/공동인증) 또는 보호자 인증 강제
```

> **착각 금지**: "학원·유치원이 일괄 동의 받으면 되겠지" → **안 됨**. 학교·기관은 정보주체 아님. 개별 부모 동의 필수. 단체 약관으로 갈음 시 동의 무효.

---

## 2. 동의 매트릭스 — KR vs COPPA vs GDPR Art.8

| 항목 | KR (PIPA + 위치) | COPPA (US) | GDPR Art.8 (EU) |
|---|---|---|---|
| 보호 연령 | 만14세 미만 (위치 별도 8세) | 만13세 미만 | 만13~16세 (회원국별) |
| 동의 주체 | 법정대리인 | 부모/법정후견인 | 부모/책임자 |
| 검증 강도 | 휴대폰 본인확인·신용카드·공동인증서 | **verifiable** parental consent (FTC 7가지 방법) | reasonable effort |
| 학교 동의 갈음 | 불가 (개별 부모 필수) | 학교 동의 허용 (FERPA 결합) | 회원국별 상이 |
| 위반 처벌 | 5천만 + 5년 (형사) | $51,744/위반 (FTC 2024 기준) | 매출 4% (최대 2천만 EUR) |
| 광고/마케팅 | 행태정보 수집 제한 | targeted ads **금지** | profiling 동의 별도 |
| 권리 SLA | 10일 (PIPA) | parental review 즉시 | 30일 |
| 책임 주체 | 회사 + 보호책임자 + (위치 시 형사) | 회사 | 회사 + DPO |

> 한국은 **위치정보법 결합 시 형사책임**, COPPA는 **민사 + 광고 금지가 명시**, GDPR은 **profiling 권리** 강조. 멀티 리전 서비스는 가장 엄격한 기준으로 통합.

---

## 3. 검증 가능한 법정대리인 동의 (Verifiable Parental Consent)

### 3.1 검증 방법 비교

| 방법 | 신뢰도 | 비용 | UX 마찰 | KR 적합 |
|---|---|---|---|---|
| **휴대폰 본인확인 (PASS)** | 높음 | 건당 ~50원 | 중 | ✅ 표준 |
| **공동인증서 / 금융인증** | 매우 높음 | 무료 | 높음 | ✅ |
| **신용카드 1원 결제** | 중 | 결제수수료 | 중 | △ (성인 카드 필수) |
| **부모 신분증 사진 + face match** | 중 | API 비용 | 높음 | △ (위변조 위험) |
| **이메일 더블 옵트인** | 낮음 | 거의 무료 | 낮음 | ❌ (한국 단독 부적합) |
| **영상통화 본인확인** | 매우 높음 | 인건비 | 매우 높음 | △ (특수 케이스) |
| **학교 발급 코드** | 낮음 (위임) | 무료 | 낮음 | ❌ |

### 3.2 운영 권장

- **1차**: 휴대폰 본인확인 (PASS) — 한국 표준, 통신3사 + 알뜰폰 지원
- **2차 폴백**: 공동인증서 (전자정부) — PASS 이용 불가 시
- **금지**: 이메일·SMS만으로 검증 (위변조 차단 불가)

### 3.3 검증 결과 보존

```sql
CREATE TABLE parental_consents (
  id UUID PRIMARY KEY,
  child_user_id UUID NOT NULL,
  guardian_user_id UUID NOT NULL,
  relationship VARCHAR(20) NOT NULL,
    -- 'mother' | 'father' | 'legal_guardian' | 'foster_parent'
  verification_method VARCHAR(30) NOT NULL,
    -- 'pass' | 'gongdong_cert' | 'credit_card_1won' | ...
  verification_provider VARCHAR(50),
    -- 'NICE' | 'KCB' | 'KGINICIS' | ...
  verification_id TEXT NOT NULL,
    -- 인증사가 발급한 트랜잭션 ID (재검증용)
  consented_at TIMESTAMPTZ NOT NULL,
  withdrawn_at TIMESTAMPTZ,
  consent_text_hash CHAR(64) NOT NULL,
  ip_address INET,
  user_agent TEXT
);

CREATE UNIQUE INDEX one_active_guardian
  ON parental_consents (child_user_id, guardian_user_id)
  WHERE withdrawn_at IS NULL;
```

> 한 자녀에 부모 둘 다 등록 가능. 단 동의는 1명의 법정대리인이면 충분 (제3자 분쟁은 §부록 Q 참조).

---

## 4. 가족 계정 모델 (Parent ↔ Child)

### 4.1 핵심 데이터 모델

```
Family
  ├─ FamilyMember (parent)   ─── 인증 가능, 동의 권한
  └─ FamilyMember (child)    ─── 인증 제한, 부모 위임으로 운영

ChildAccount
  ├─ owner: parent_user_id   ─── 법정대리인
  ├─ guardians: [parent_id]  ─── 추가 보호자 (조부모, 분리가족)
  ├─ visible_to_child: bool  ─── 자녀 앱 노출 여부
  └─ delegated_actions: enum ─── 위임된 행동 (위치보기, 채팅보기 등)
```

### 4.2 계정 분리 원칙

- 자녀 계정은 **별도 user_id** (부모 계정 종속 X)
- 부모는 자녀 계정의 **위임된 행동만** 수행 (모든 권한 X)
- 자녀가 14세 도래 시 자녀 계정으로 권한 이양 (§부록 Q)

### 4.3 분리 가족 / 다중 보호자

| 케이스 | 권장 운영 |
|---|---|
| 부모 둘 모두 보호자 | 1명 동의로 충분, 둘 다 등록 가능 |
| 이혼 (양육권 단독) | 양육권자 동의만 유효, 비양육 부모는 read-only 또는 차단 |
| 조부모·삼촌 등 | 법정대리인 자격 증빙 (가족관계증명서) 필요 |
| 보호시설 | 시설장 + 가족관계 증빙 |

> 분쟁 발생 시 audit log + 가족관계증명서로 증명. `business/audit-log.md` 참조.

---

## 5. 추적 사실 가시화 의무

위치추적·활동기록을 부모가 보더라도, **자녀가 그 사실을 인지**해야 한다 (위치정보법 제26조 관련 의무).

### 5.1 가시화 패턴

```
자녀 앱 화면 (모든 화면 상단)
┌─────────────────────────────────┐
│  📍 부모님이 내 위치를 볼 수 있어요  │  ← 항상 표시
│  [자세히]                        │
└─────────────────────────────────┘

부모가 위치 조회 시 (이벤트 알림)
┌─────────────────────────────────┐
│  엄마가 1분 전에 내 위치를 확인했어요 │
│  하루 평균 5회 확인               │
└─────────────────────────────────┘
```

### 5.2 가시화 강도 (연령별)

| 연령 | 가시화 |
|---|---|
| 만8세 이하 | 글자 + 픽토그램 (읽기 어려운 경우 대비) |
| 만8세 ~ 12세 | 텍스트 + 조회 횟수 통계 |
| 만13세 ~ 14세 | 텍스트 + 조회 시점 알림 + 거부 옵션(부모 알림) |

### 5.3 거부할 권리

자녀가 14세 미만이라도 추적을 **거부할 권리**는 있다 (헌법상 인격권).
- 거부 시 부모에게 통지
- 부모는 거부 사유와 무관하게 동의 철회 가능
- 거부와 부모 동의 충돌 시 — 법적으로 부모 우선이지만 UX는 협의 옵션 제공

---

## 6. 데이터 최소화

### 6.1 수집 항목별 결정

| 데이터 | 일반 사용자 | 만14세 미만 | 사유 |
|---|---|---|---|
| 생년월일 | 풀 입력 | **만나이만** | 정확 생일 불필요 |
| 주소 | 풀 주소 | **시·구 단위** | 위치는 별도 동의 |
| 사진 | 자유 업로드 | **부모 사전 검토** | 초상권 + 그루밍 위험 |
| 친구 추천 | 주소록 매칭 | **금지** | 미성년 사회망 노출 |
| 행태정보 | 분석 가능 | **금지** | 광고 결합 차단 |
| 결제 정보 | 본인 카드 | **부모 카드 + 한도** | 충동구매 차단 |
| 민감정보 (건강/종교) | 별도 동의 | **수집 금지 원칙** | 학습 발달 보호 |

### 6.2 만나이 처리

```typescript
// 풀 생년월일 대신 만나이만 수집
function calculateKoreanAge(birthDate: Date): number {
  const today = new Date();
  let age = today.getFullYear() - birthDate.getFullYear();
  const m = today.getMonth() - birthDate.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) age--;
  return age;
}

// DB에는 birth_year만 (생일·일은 저장 X)
// 14세 도래 판정용으로 birth_year_month까지만
```

---

## 7. 미성년 채팅 모더레이션

### 7.1 자동 필터링 (필수)

| 카테고리 | 차단 패턴 |
|---|---|
| 욕설·혐오 | 한국어 욕설 사전 + 변형 (ㅅㅂ, ㄱㅅㄲ, etc.) |
| 그루밍 의심 | 만나자 + 비밀 + 사진 보내달라 (조합 점수) |
| 개인정보 | 전화번호 / 주소 / 학교명 정규식 |
| 외부 링크 | http, kakao 오픈채팅, 디스코드 등 |
| 결제 유도 | 송금·기프티콘 키워드 |

### 7.2 보호자 모니터링 권한

- 부모는 **모든 메시지 read-only 접근** 가능 (자녀에게 가시화 필수)
- 1:1 채팅 vs 단톡: 단톡은 다른 자녀 부모 동의 결합 (모더레이터 관리)
- 모더레이션 우회 시도 (이미지로 전화번호 등) 자동 신고

### 7.3 신고 → 처리 SLA

| 신고 유형 | 1차 응답 | 처리 |
|---|---|---|
| 그루밍 의심 | 즉시 (자동 차단) | 1시간 내 운영자 검토 |
| 욕설·혐오 | 자동 마스킹 | 24시간 내 |
| 일반 갈등 | 24시간 | 72시간 |

---

## 8. 광고·마케팅 제한

| 행위 | 일반 | 만14세 미만 |
|---|---|---|
| 행태정보 수집 (cookie/ID) | 동의 시 가능 | **금지 원칙** |
| 타겟 광고 | 별도 동의 | **금지** (COPPA 명시, KR 제한) |
| 푸시 마케팅 | 별도 동의 | **부모 동의 + 자녀 거부권** |
| 인앱 결제 유도 | 가능 | **부모 동의 게이트** |
| 다크 패턴 (FOMO/카운트다운) | 자제 권장 | **금지** (소비자보호법) |
| 인플루언서/광고 표시 | 표시 의무 | **분명한 시각 라벨** |

---

## 9. 학교·기관 통합 동의 — 적법성

### 9.1 가능 / 불가능

| 케이스 | 가능 여부 |
|---|---|
| 학교가 보낸 가입 안내 → 부모가 직접 동의 | ✅ |
| 학교가 부모 명단 → 회사가 부모 직접 연락 | ✅ (위탁 동의 포함 시) |
| **학교가 일괄 가입 처리 (부모 미인지)** | ❌ |
| **학원이 약관에 "위치추적 포함" 끼워 넣고 학생 가입** | ❌ |
| 학교 행정업무 (출결·급식) 기존 위탁 처리 | ✅ (FERPA 유사) |

### 9.2 위탁 처리와 동의 처리 구분

- **위탁** (학교 → 회사): 학교가 처리 주체 유지, 회사는 수탁자. 학교가 부모 동의 보유 필요.
- **동의** (부모 → 회사): 회사가 직접 처리 주체. 부모 본인 동의 검증.

---

## 10. 도메인 매핑 — 통학차량 플랫폼 사례

| 컴포넌트 | 적용 항목 | 운영 행동 |
|---|---|---|
| 학생 회원가입 | PIPA 제22조의2 | 부모 PASS 인증 후 자녀 계정 생성 |
| 학생 위치 추적 (차량 좌표) | 위치정보법 제26조 + PIPA | 부모 동의 + 학생 앱 가시화 |
| 부모 ↔ 학생 채팅 | 미성년 채팅 | 모더레이션 ON, 부모 read-only |
| 운전자 ↔ 학생 채팅 | 미성년 채팅 | **개별 1:1 금지**, 노선 단톡만 (운영자 모더) |
| 학생 사진 업로드 (프로필) | 데이터 최소화 | 부모 사전 검토, 캐릭터 이미지 권장 |
| 푸시 알림 (탑승/하차) | 마케팅 X / 정보성 O | 정보성 디폴트 ON, 마케팅 OFF |
| 학원·유치원 가입 안내 | 학교 동의 갈음 X | 학원이 부모 명단 위탁 → 회사 직접 연락 |
| 14세 생일 학생 | 권한 이양 | 자녀 계정 권한 자동 승급, 부모 권한 read-only |

---

## 11. 구현 패턴

### 11.1 가입 플로우 (Flutter)

```dart
final kidSignupFlow = [
  ChildAgeCheckScreen(),         // 1: 만나이 입력 (생일 X)
  GuardianContactScreen(),       // 2: 부모 연락처
  GuardianPassAuthScreen(),      // 3: 부모 PASS 인증
  ConsentChildPipaScreen(),      // 4: 자녀 정보 처리 동의 (별도)
  ConsentChildLocationScreen(),  // 5: 자녀 위치 처리 동의 (별도)
  ChildVisibilityNoticeScreen(), // 6: 자녀에게 추적 사실 안내
  ChildOnboardingScreen(),       // 7: 자녀 앱 첫 진입
];
// 만14세 이상이면: 본인 PASS 인증 + 일반 동의 흐름
```

### 11.2 추적 가시화 위젯 (자녀 앱)

```dart
class ChildTrackingBanner extends StatelessWidget {
  final int viewsToday;

  Widget build(BuildContext context) {
    return Container(
      color: Colors.blue.shade50,
      padding: EdgeInsets.all(8),
      child: Row(children: [
        Icon(Icons.location_on, color: Colors.blue),
        SizedBox(width: 8),
        Expanded(child: Text(
          "부모님이 오늘 $viewsToday번 위치를 확인했어요",
        )),
        TextButton(
          onPressed: () => _showRefuseDialog(context),
          child: Text("거부 요청"),
        ),
      ]),
    );
  }
}
```

### 11.3 채팅 모더레이션 (Go)

```go
type ModerationResult struct {
    Allow      bool
    Reason     string  // "grooming_suspect" | "phone_number" | ...
    Confidence float64
    Action     string  // "block" | "mask" | "warn" | "report"
}

func (m *Moderator) Check(ctx context.Context, msg ChatMessage) ModerationResult {
    if matches := m.phoneRegex.FindAllString(msg.Text, -1); len(matches) > 0 {
        return ModerationResult{Allow: false, Reason: "phone_number", Action: "mask"}
    }
    if score := m.groomingScorer.Score(msg.Text); score > 0.7 {
        return ModerationResult{Allow: false, Reason: "grooming_suspect", Action: "block_and_report"}
    }
    // ... 욕설, 결제유도 등
    return ModerationResult{Allow: true}
}
```

### 11.4 14세 도래 권한 이양 (cron)

```sql
-- 매일 자정 실행
UPDATE child_accounts ca
SET status = 'graduated_to_self_managed',
    parent_role = 'read_only'
FROM users u
WHERE u.id = ca.child_user_id
  AND u.birth_year * 12 + u.birth_month <= (
        EXTRACT(YEAR FROM NOW())::int * 12
      + EXTRACT(MONTH FROM NOW())::int - 14*12
      )
  AND ca.status = 'minor';

-- audit log + 부모/자녀 양쪽 푸시 알림 트리거
```

---

## 12. 함정 (자주 빠뜨리는 것)

| 함정 | 결과 | 대응 |
|---|---|---|
| 학원·유치원 일괄 동의로 처리 | 동의 무효 | 개별 부모 PASS 인증 |
| 이메일·SMS만으로 부모 동의 검증 | 검증 실패 (위변조) | PASS / 공동인증 |
| 부모 동의 후 자녀에게 추적 사실 비공개 | 가시화 의무 위반 | 자녀 앱 항상 표시 |
| 자녀 생년월일 풀 저장 | 데이터 최소화 위반 | birth_year_month까지만 |
| 14세 생일 도래 후 부모 권한 유지 | 동의 근거 소멸 | cron으로 권한 이양 |
| 단톡방에 운전자·학생 1:1 가능하게 둠 | 그루밍 위험 | 노선 단톡 + 운영자 모더 |
| 결제 유도 / 충동 인앱 결제 | 소비자보호법 + COPPA | 부모 게이트 |
| 행태정보 수집해서 광고 타게팅 | 명백 위반 | 미성년 행태정보 OFF |
| 분리가족(이혼) — 비양육 부모도 동의 권한 | 양육권 미확인 시 무효 | 가족관계증명서 검증 |
| 채팅 사진에 위치 메타데이터 (EXIF) | 개인정보 노출 | EXIF strip |
| 부모 모니터링 — 자녀 동의 없이 도청 | 인격권 침해 | 가시화 + 거부권 |
| 푸시 마케팅 — "정보성"으로 가장 | KR 광고규제 | 분명히 [광고] 라벨 |

---

## 13. 운영 체크리스트

### 가입 / 동의
- [ ] 부모 검증 — PASS 또는 공동인증 강제
- [ ] 자녀 정보 처리 동의 (PIPA) 별도 화면
- [ ] 자녀 위치 정보 동의 (위치정보법) 별도 화면 (`legal/kr-location-info-act.md`)
- [ ] 추적 사실 자녀 앱 가시화

### 데이터
- [ ] 생년월일 → 만나이/birth_year_month로 최소화
- [ ] 주소 → 시·구 단위
- [ ] 사진 → 부모 검토 흐름 (또는 캐릭터 디폴트)
- [ ] 행태정보 수집 OFF (cookie, ID, fingerprint)

### 운영
- [ ] 채팅 모더레이션 자동 + 24시간 신고 처리
- [ ] 운전자·학생 1:1 채팅 차단
- [ ] 광고 타게팅 OFF
- [ ] 인앱 결제 부모 게이트

### 권리
- [ ] 부모 자녀정보 열람 (DSR — `legal/data-subject-rights.md`)
- [ ] 자녀 추적 거부 → 부모 알림
- [ ] 14세 생일 권한 이양 cron + 알림
- [ ] 분리가족 양육권 검증 SOP

### 외부
- [ ] 학교·기관 위탁 vs 직접 동의 구분
- [ ] 위탁계약서에 미성년 보호 조항 명시
- [ ] 침해사고 시 부모 별도 통지

---

## 부록 A: 자주 묻는 질문

**Q. 부모 둘 중 한 명만 동의해도 되는가?**
A. 단독 양육권자 1명이면 충분. 분리가족(이혼) 케이스는 양육권자 동의가 우선. 비양육 부모 거부 시 분쟁 → audit log로 기록.

**Q. 14세 생일 당일 어떻게 처리하는가?**
A. 자정 cron으로 자녀 계정 권한 이양 + 부모/자녀 양쪽 통지. 부모는 read-only로 유지(자녀가 명시 차단 전까지).

**Q. 조부모가 보호자인 경우?**
A. 가족관계증명서·후견 결정문 등으로 법정대리인 자격 증빙 후 등록. 비공식 양육은 인정 X.

**Q. 학원이 학생 가입을 대신 처리해도 되는가?**
A. 학원이 부모에게 연락해서 부모가 직접 동의·인증하는 절차여야 함. 학원이 부모 ID·인증 정보를 대신 입력하면 무효.

**Q. 자녀가 추적을 거부하면 어떻게 되는가?**
A. 거부 자체로 부모 동의가 무효되지는 않으나, 부모에게 거부 사실을 통지하고 동의 철회 옵션 제공. 가족 협의 후 결정.

**Q. 만14세 이상 학생도 보호자 동의 필요한가?**
A. 일반 가입은 본인 동의 가능. 단 광고·마케팅·민감정보·결제 한도 변경은 미성년자(만19세 미만) 보호자 동의 필요.

**Q. 가족 단톡방에서 부모가 한 발언이 자녀에게 부적절한 경우?**
A. 모더레이션 룰은 부모에게도 적용 (욕설·혐오 등). 부모 발언 차단 시 부모 본인에게 알림.

**Q. COPPA 미국 사용자도 함께 받으려면?**
A. 회원가입 시 거주국 확인 → 미국이면 COPPA 흐름(verifiable consent), 한국이면 PIPA 흐름. 가장 엄격한 기준으로 통합 운영도 가능.

---

## 참고 자료

- 「개인정보 보호법」 제22조의2 (아동의 개인정보 보호)
- 개인정보보호위원회 「아동·청소년 개인정보보호 가이드라인」
- 「위치정보의 보호 및 이용 등에 관한 법률」 제26조 (8세 이하 아동등의 보호)
- COPPA — 15 U.S.C. §§ 6501–6506 / FTC 16 CFR Part 312
- GDPR Article 8 (조건부 동의)
- ICO (UK) Children's Code (Age Appropriate Design Code)
- 「청소년 보호법」 (광고·콘텐츠 제한)
