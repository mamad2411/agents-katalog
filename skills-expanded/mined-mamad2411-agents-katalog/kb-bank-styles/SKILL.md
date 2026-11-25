---
name: kb-bank-styles
description: KB국민은행 / KB스타뱅킹의 시각 언어를 따라 한국 금융권(뱅킹 앱·웹) UI를 만드는 스타일 가이드. "KB 스타일", "국민은행 스타일", "한국 뱅킹 UI", "한국 금융권 UI" 같은 요청에 사용한다. 토큰(컬러·타이포·스페이싱)·컴포넌트 스니펫·홈/송금/내역 페이지 템플릿을 제공한다.
---

# KB Bank Style Guide (KB국민은행 / KB스타뱅킹 UI)

이 스킬은 KB금융그룹 / KB국민은행 / KB스타뱅킹의 시각 언어를 토대로
한국형 인터넷뱅킹 UI를 빠르게 구축하기 위한 가이드와 토큰·컴포넌트 모음이다.

---

## 1. 디자인 정체성

| 요소 | 톤 |
|---|---|
| 인상 | 신뢰감 있고 명료한 / 정보 밀도가 높지만 답답하지 않은 |
| 분위기 | 화이트 캔버스 + 강한 옐로우 포인트 + 진한 본문 그레이 |
| 형태 | 큰 라운딩(12–20px), 옅은 그림자, 카드 단위 정보 그룹화 |
| 모션 | 과하지 않게. 누름 상태(scale 0.98) + 토글 트랜지션 위주 |
| 보이스 | "○○님, ~하세요/했어요" 친근한 존댓말. 숫자는 천단위 콤마 + "원" |

KB의 시각적 코어는 단 두 가지다:
1. **스타-비(Star-b) 옐로우** — 단일 강한 액센트
2. **두꺼운 본문 그레이/블랙** — 가독 중심 정보

→ 이 두 개를 깨지 않고 보조 컬러(민트·코랄·앰버)는 거래 분류용으로만 절제 사용.

---

## 2. 분기: 모바일 앱 vs 웹

이 스킬은 두 프리셋을 제공한다.

| 항목 | 모바일 (KB스타뱅킹 톤) | 웹 (kbstar.com 톤) |
|---|---|---|
| 배경 | `#FFFFFF` 또는 `#F7F8FA` | `#F4F6F9` |
| 카드 | 그림자 있는 화이트 카드 | 보더 위주, 그림자 약함 |
| 본문 폰트 크기 | 15–17px | 14–15px |
| 정보 밀도 | 낮음 (큰 잔액·큰 버튼) | 높음 (테이블·폼·탭 많음) |
| 헤더 | 콤팩트 + 검색/알림/MY | GNB 2단(상단 유틸 + 메인 메뉴) |
| 주 사용처 | 홈/송금/카드/자산 | 조회/거래/상품가입/고객센터 |

요청에 "앱"/"모바일"/"스타뱅킹" 키워드가 있으면 모바일 프리셋, "웹"/"인터넷뱅킹"/"홈페이지"이면 웹 프리셋을 우선 사용한다. 명시 없으면 모바일을 기본으로 한다.

---

## 3. 컬러 토큰

KB의 정확한 브랜드 컬러는 KB금융그룹 CI 가이드(별색 기준)에 정의되어 있으며,
공개 자료 기반의 가장 널리 알려진 근사값은 다음과 같다.

```css
/* assets/tokens.css 와 동일 */
@theme {
  /* Brand */
  --color-kb-yellow:        #FFBC00;  /* Star-b Yellow (KB 시그니처) */
  --color-kb-yellow-strong: #FFCC00;  /* 강조/상태(클릭) */
  --color-kb-yellow-soft:   #FFF7DB;  /* 노랑 톤 배경 */
  --color-kb-dark:          #60584C;  /* KB 보조 다크 (스톤 그레이) */
  --color-kb-black:         #1A1A1A;  /* 본문 강조 블랙 */

  /* Surface (Mobile preset) */
  --color-bg:        #F7F8FA;
  --color-surface:   #FFFFFF;
  --color-line:      #EEF0F3;
  --color-line-2:    #E5E8EC;

  /* Text — 한국 금융권 표준 그레이 스케일 */
  --color-ink:    #191F28;  /* 본문 강조 */
  --color-ink-2:  #4E5968;  /* 본문 보조 */
  --color-ink-3:  #8B95A1;  /* 캡션/메타 */
  --color-ink-4:  #B0B8C1;  /* placeholder/disabled */

  /* Semantic */
  --color-positive: #1EC894;  /* 입금/상승 */
  --color-negative: #F04452;  /* 출금/하락 (위험·삭제 전용) */
  --color-warn:     #FFB020;
  --color-info:     #3182F6;  /* 링크·정보 */

  /* Category (거래/소비 차트용 절제 팔레트) */
  --color-cat-1: #FFBC00;
  --color-cat-2: #FF8A3D;
  --color-cat-3: #1EC894;
  --color-cat-4: #5D7BFF;
  --color-cat-5: #B795FF;
}
```

**사용 규칙**
- **주 액션 버튼**: KB옐로우 배경 + **검정 텍스트**. 옐로우 위 흰색 텍스트는 가독성이 부족하며 KB의 실제 패턴도 검정.
- **보조 액션**: `--color-line` 배경 + `--color-ink` 텍스트
- **링크/정보**: `--color-info` (파란색은 거래내역 입금 표시에도 쓰임)
- **빨강은 위험·삭제·하락에만**. 출금 거래는 빨강이 아니라 본문 그레이(`--color-ink`)로 표시 (KB스타뱅킹 패턴)

---

## 4. 타이포그래피

이 스킬은 **KB금융그룹 내부 사용**을 전제로 하며, KB금융체(**KBFG Display / KBFG Text**)를 **기본 폰트로 사용한다.**

- **KBFG Display** (제목): Bold / Medium / Medium Italic / Light
- **KBFG Text** (본문): Bold / Medium / Light — 본문/숫자/UI 전반의 표준

폰트는 `examples/tokens.css` 안에서 `assets/fonts.css`(KBFG 웹폰트 `@font-face`)를 자동 import하며, `--font-sans` / `--font-display` 토큰이 KBFG를 직접 가리킨다. 폴백은 시스템 폰트만 둔다.

```css
@theme {
  --font-sans:    'KBFG Text', -apple-system, system-ui, sans-serif;
  --font-display: 'KBFG Display', 'KBFG Text', -apple-system, system-ui, sans-serif;
}
```

**타입 스케일 (모바일 프리셋)**

| 토큰 | 크기 / 줄간 / 굵기 | 용도 |
|---|---|---|
| display-1 | 36 / 1.1 / 700 | 큰 잔액 ("12,442,910원") |
| display-2 | 28 / 1.2 / 700 | 페이지 헤딩 ("안녕하세요, 이수진님") |
| heading | 18 / 1.4 / 700 | 섹션 타이틀 |
| body | 15 / 1.55 / 500 | 본문 |
| body-strong | 15 / 1.55 / 700 | 거래 금액·계좌명 |
| caption | 12 / 1.4 / 500 | 메타·시간·계좌번호 |
| micro | 11 / 1.4 / 600 | 배지·태그 |

숫자는 항상 `tabular-nums`. 금액은 `font-bold` + 천단위 콤마 + `원` 접미사.

---

## 5. 스페이싱·라운딩·그림자

| 토큰 | 값 | 용도 |
|---|---|---|
| `--radius-sm` | `8px` | 칩, 작은 버튼 |
| `--radius-md` | `12px` | 입력, 중간 카드 |
| `--radius-lg` | `16px` | 표준 카드 |
| `--radius-xl` | `20px` | 메인 잔액 카드 |
| `--radius-full` | `9999px` | 필터 칩, 아바타 |
| `--shadow-card` | `0 2px 10px rgba(25,31,40,0.04)` | 표준 카드 |
| `--shadow-pop` | `0 8px 24px rgba(25,31,40,0.08)` | 모달, 토스트 |

레이아웃 거터: 모바일 24px, 웹 데스크톱 max-width 1200px + 24~32px 패딩.
세로 간격은 24px(섹션 간) / 16px(카드 내부) / 12px(리스트 행) 기준.

---

## 6. 컴포넌트 라이브러리 (`examples/`)

이 스킬은 다음 React + Tailwind v4 컴포넌트 예시를 포함한다.

**기본 (홈/리스트)**
| 파일 | 설명 |
|---|---|
| `examples/tokens.css` | `@theme` 토큰 (앱에 그대로 import 가능) |
| `examples/Button.tsx` | Primary(KB옐로우) / Secondary / Ghost / Danger 변형 |
| `examples/AccountCard.tsx` | 계좌 잔액 카드 (송금/내역/ATM 액션 버튼 포함) |
| `examples/TransactionItem.tsx` | 거래 1행 (입금·출금·자동이체) |
| `examples/QuickMenuGrid.tsx` | 자주 쓰는 메뉴 4×N 그리드 |
| `examples/HomePage.tsx` | 모바일 프리셋 홈 페이지 풀 템플릿 |

**송금·인증 (Transfer / Auth)**
| 파일 | 설명 |
|---|---|
| `examples/AmountInput.tsx` | 금액 입력 + 천단위 콤마 + 빠른 추가 칩 |
| `examples/NumericKeypad.tsx` | 숫자/보안 키패드 (shuffle 옵션) |
| `examples/PINInput.tsx` | 간편비밀번호 도트 표시 |
| `examples/BottomSheet.tsx` | 모바일 표준 바텀시트 (dim·body 잠금) |
| `examples/TransferConfirmSheet.tsx` | "정말 보낼까요?" 송금 확인 |
| `examples/ReceiptCard.tsx` | 송금 영수증 (캡처/공유용, 톱니 디테일) |

**카드·차트 (Card / Insights)**
| 파일 | 설명 |
|---|---|
| `examples/VirtualCard.tsx` | 가상 카드 (번호 마스킹 토글) |
| `examples/SpendingBar.tsx` | 멀티 세그먼트 소비 바 + 카테고리 범례 |
| `examples/CategoryDonut.tsx` | SVG 도넛 차트 (의존성 없음) |

**상태·약관 (Feedback / Forms)**
| 파일 | 설명 |
|---|---|
| `examples/Feedback.tsx` | `EmptyState`, `Skeleton`, `AccountCardSkeleton`, `Toast` 묶음 export |
| `examples/TermsAccordion.tsx` | 약관 동의 (필수/선택, 전체동의 토글) |

각 파일은 최소 의존성으로 작성되어 있고, `examples/tokens.css`만 import하면 그대로 동작한다.

---

## 7. 동작 흐름 (스킬 사용 시)

요청이 들어오면 다음 순서로 동작한다.

### 1단계 — 컨텍스트 파악
- 요청에 "앱/모바일/스타뱅킹" → 모바일 프리셋
- 요청에 "웹/인터넷뱅킹/홈페이지" → 웹 프리셋
- 명시 없음 → 모바일 프리셋

### 2단계 — 토큰 주입
프로젝트의 메인 CSS 파일(예: `src/index.css`)에 `examples/tokens.css`의 내용을 머지한다. 이미 `@theme` 블록이 있으면 토큰 키를 추가만 하고, 충돌하는 키는 **건드리지 않고** 사용자에게 차이만 보고한다.

### 3단계 — 폰트 주입
KBFG 웹폰트는 `examples/tokens.css`에서 자동으로 import된다. 별도 작업 불필요.
(KBFG 로드 실패 시에는 시스템 기본 sans 폰트로 자연 대체된다.)

### 4단계 — 컴포넌트 생성
요청한 페이지/컴포넌트에 따라 `examples/`의 파일들을 `src/components/kb/` 또는 사용자가 지정한 경로로 복사한다. 이미 같은 이름의 컴포넌트가 있으면 덮어쓰지 않고 충돌을 보고한다.

### 5단계 — 사용 가이드 출력
- 어떤 토큰/컴포넌트가 추가됐는지 요약
- 라이선스 주의사항 (KB CI 사용 금지, 폰트 라이선스 확인)

---

## 8. 작성 규칙 (체크리스트)

KB 스타일로 UI를 작성할 때 항상 지킬 것:

- [ ] 강조 색은 KB옐로우 1개. 보조 액션은 회색.
- [ ] 옐로우 위 텍스트는 흰색 ❌ → **검정 또는 진한 그레이** ⭕
- [ ] 출금 거래는 빨강 ❌ → **본문 그레이** ⭕ (입금만 파란색·민트로 강조)
- [ ] 금액 표기: `12,442,910원` (콤마 + "원" 접미사 + tabular-nums)
- [ ] 본문은 KBFG Text, 절대 시스템 기본 sans 노출 금지
- [ ] 카드 라운딩 16~20px, 그림자는 매우 옅게 (`rgba(25,31,40,0.04)`)
- [ ] 친근 존댓말: "안녕하세요, ○○님 / ~했어요 / ~하세요"
- [ ] 정보 단위는 카드로 그룹. 카드 간 충분한 세로 간격(24px)
- [ ] 모바일은 최대 너비 480px 가정, 웹은 1200px 가정
