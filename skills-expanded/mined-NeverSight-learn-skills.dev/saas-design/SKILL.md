---
name: saas-design
description: SaaS 디자인 가이드 스킬 - 독창적이고 기억에 남는 UI/UX 설계
triggers:
  - saas 디자인
  - ui 설계
  - 디자인 시스템
  - 컬러 팔레트
  - 타이포그래피
---

# SaaS Design Skill

독창적이고 프로덕션 수준의 SaaS UI/UX를 설계하기 위한 디자인 철학과 가이드입니다.

## 핵심 원칙

> "의도적인 것이 강렬한 것보다 중요하다. 대담한 맥시멀리즘과 정제된 미니멀리즘 모두 작동한다 - 핵심은 의도성이다."

## Design Thinking 프로세스

코드 작성 전, 맥락을 이해하고 **대담한 미적 방향**을 결정:

### 1. Purpose (목적)
- 이 SaaS가 해결하는 문제는?
- 타겟 사용자는 누구인가?
- 사용자의 감정적 상태는? (급함? 여유? 전문적?)

### 2. Tone (톤)
극단적인 미적 방향 중 선택:

| 스타일 | 설명 | 적합한 SaaS |
|-------|------|------------|
| Brutally minimal | 극도로 절제, 여백 중심 | 생산성, 노트 |
| Maximalist chaos | 풍부하고 레이어드 | 크리에이티브, 게임 |
| Retro-futuristic | 복고 + 미래 | 테크, AI |
| Organic-natural | 유기적 곡선 | 웰니스, 환경 |
| Luxury-refined | 고급스러운 | 프리미엄, 금융 |
| Playful-toy-like | 재미있고 친근한 | 교육, 소셜 |
| Editorial-magazine | 잡지 스타일 | 미디어, 콘텐츠 |
| Brutalist-raw | 거칠고 원시적 | 개발자 도구 |
| Art deco-geometric | 기하학적 대칭 | 부동산, 럭셔리 |
| Industrial-utilitarian | 기능적, 산업적 | B2B, 엔터프라이즈 |

### 3. Constraints (제약)
- 기술 요구사항 (반응형, 접근성)
- 성능 목표 (로딩 시간, Core Web Vitals)
- 브랜드 가이드라인 (있는 경우)

### 4. Differentiation (차별화)
- 무엇이 이것을 **잊을 수 없게** 만드는가?
- 경쟁사와 어떻게 다른가?
- 한 가지 기억에 남을 요소는?

---

## 피해야 할 것 (AI Slop)

### ❌ 타이포그래피
- Inter, Roboto, Arial, system-ui
- 모든 SaaS가 똑같이 보이는 폰트

### ❌ 컬러
- 흰색 배경 + 보라색 그라데이션
- #6366f1 (indigo-500) 남용
- 과도하게 균등한 색상 분배

### ❌ 레이아웃
- 예측 가능한 hero → features → pricing
- 좌우 대칭의 모든 것
- 동일한 카드 그리드 반복

### ❌ 패턴
- 떠다니는 보라색 블롭
- 동일한 그라데이션 버튼
- 과도한 둥근 모서리 (rounded-2xl 남용)

---

## 지향해야 할 것

### ✅ 타이포그래피
```
디스플레이 폰트 (헤딩):
- 영문: Space Grotesk, Clash Display, Cabinet Grotesk, Instrument Sans
- 한글: Pretendard, SUIT, Wanted Sans, 본고딕

본문 폰트:
- 영문: Geist, Söhne, Satoshi
- 한글: Pretendard, SUIT, Noto Sans KR
```

전략: 개성 있는 디스플레이 폰트 + 읽기 쉬운 본문 폰트 조합

### ✅ 컬러
```css
/* 예시: 지배색 + 날카로운 악센트 */
:root {
  --color-bg: #0a0a0a;
  --color-text: #fafafa;
  --color-accent: #00ff88;  /* 예상치 못한 악센트 */
  --color-muted: #737373;
}
```

전략:
- 지배색이 80% 이상 차지
- 악센트는 5-10%만
- 예상치 못한 컬러 조합

### ✅ 레이아웃
- 비대칭 배치
- 요소 오버랩
- 대각선 흐름
- 그리드를 깨는 요소
- 넉넉한 여백 OR 의도적인 밀도

### ✅ 모션
```css
/* 순차적 등장 */
.item { animation: fadeIn 0.5s ease-out forwards; }
.item:nth-child(1) { animation-delay: 0.1s; }
.item:nth-child(2) { animation-delay: 0.2s; }
.item:nth-child(3) { animation-delay: 0.3s; }

/* 스크롤 트리거 */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

전략:
- 한 번의 잘 조율된 페이지 로드 애니메이션
- 예상치 못한 호버 상태
- 스크롤 트리거 효과

### ✅ 배경 & 디테일
맥락에 맞는 효과:
- 그라데이션 메시
- 노이즈/그레인 텍스처
- 기하학적 패턴
- 레이어드 투명도
- 드라마틱한 그림자
- 장식적 보더
- 커스텀 커서

---

## SaaS 필수 화면

### 1. 랜딩 페이지
```
구성:
- 히어로 (강렬한 헤드라인 + CTA)
- 소셜 프루프 (로고, 사용자 수)
- 기능 소개 (3-5개 핵심 기능)
- 스크린샷/데모
- 가격표
- FAQ
- 푸터 CTA
```

### 2. 로그인/회원가입
```
구성:
- 심플한 폼
- 소셜 로그인 (Google, GitHub)
- 비밀번호 찾기 링크
- 브랜딩 요소
```

### 3. 대시보드
```
구성:
- 환영 메시지 / 상태 요약
- 핵심 지표 카드
- 퀵 액션 버튼
- 최근 활동
- 사이드바 네비게이션
```

### 4. 설정
```
구성:
- 프로필 편집
- 구독/결제 관리
- 팀 멤버 관리
- 알림 설정
- API 키 (개발자용)
```

### 5. 가격/결제
```
구성:
- 플랜 비교표
- 월간/연간 토글
- 결제 폼
- 영수증/청구서
```

### 6. 온보딩
```
구성:
- 환영 모달
- 단계별 설정 위저드
- 첫 사용 가이드 투어
- 빈 상태 (empty state) 가이드
```

---

## 복잡도 매칭

디자인 비전에 맞는 구현 복잡도:

| 비전 | 구현 |
|-----|-----|
| 맥시멀리스트 | 정교한 코드, 풍부한 애니메이션, 레이어드 효과 |
| 미니멀리스트 | 절제, 정밀한 여백, 미묘한 디테일 |

> "Claude는 놀라운 창작 능력을 가지고 있습니다. 틀을 벗어나 생각하고, 독특한 비전에 완전히 몰입할 때 진정으로 무엇을 만들 수 있는지 보여주세요."
