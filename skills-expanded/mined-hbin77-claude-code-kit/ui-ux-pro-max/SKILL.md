---
name: ui-ux-pro-max
description: AI 기반 디자인 인텔리전스. 49개 산업별 추론 규칙, 40개 UI 스타일, 184개 UX 가이드라인, 색상 팔레트, 타이포그래피 규칙을 이용해 제품 유형에 맞는 전문가급 디자인 시스템을 생성한다.
---

# UI/UX Pro Max — Design Intelligence

Claude Code 내장 디자인 브레인. Python 스크립트 없이 지식 기반으로 동작한다.

## 언제 활성화되는가

### 필수 활성화
- 새 페이지/화면 설계 (대시보드, 관리자, SaaS, 모바일 앱, 랜딩)
- UI 컴포넌트 생성·리팩토링 (버튼, 모달, 폼, 테이블, 차트)
- 컬러 스키마·타이포그래피·레이아웃 시스템 선택
- UI 코드 리뷰 (UX·접근성·시각적 일관성)

### 건너뛰기
- 순수 백엔드 로직
- API / DB 설계
- 인프라/DevOps
- 비시각적 스크립트

## 지식 모듈 (3단 참조 구조)

이 스킬은 규모가 커서 3개 참조 파일로 분리했다. 목적별로 `Read`로 필요한 파일만 로드한다.

| 파일 | 용도 | 언제 읽는가 |
|------|------|------------|
| `reasoning-rules.md` | 49개 산업별 추론 규칙 (제품 유형 → 패턴·스타일·컬러·효과·안티패턴) | Step 2 "디자인 시스템 생성" |
| `styles.md` | 40개 UI 스타일 상세 (글래스모피즘/브루탈리즘/클레이모피즘 등 + 컬러/효과/조합 가이드) | 스타일 선택·대체 시 |
| `ux-guidelines.md` | 184개 UX 체크리스트 (§1–§10) + 전달 전 최종 검증 27개 (접근성·터치·성능·폼·네비게이션·차트) | Step 5 "전달 전 검증" |

## 워크플로우 (4단계)

### Step 1 — 요구사항 분석
요청에서 다음을 추출한다:

- **제품 유형 (Product type)**: SaaS / E-commerce / Fintech / Healthcare / Dating / Social / Productivity / …
- **산업 (Industry)**: B2B / B2C / Luxury / Government / Education / …
- **스타일 키워드 (Tone)**: 미니멀 / 생생한 / 다크 / 플레이풀 / 럭셔리 / 콘텐츠-퍼스트 / …
- **타겟 사용자**: 연령대·사용 문맥
- **스택**: Next.js / React Native / Flutter / …
- **밀도/모드**: data-dense vs content-dense / light vs dark

한 축이라도 불명확하면 **묻기 전에 기본값을 제시**하고 사용자 확인 받는다.

### Step 2 — 디자인 시스템 생성 (필수)
`reasoning-rules.md`를 참조하여 제품 유형에 맞는 설계를 도출한다:

**출력물 (MASTER 설계 시스템):**
```yaml
product_type: <Dating App / SaaS Dashboard / Beauty Service / ...>
recommended_pattern: <Hero + Features + CTA / Data-Dense Dashboard / ...>
style_priority: <Primary Style + Secondary Style>
color_mood: <Navy + Trust Blue + Gold / Warm pastels + Pink / ...>
typography_mood: <Professional + Hierarchy / Friendly + Playful / ...>
key_effects:
  - <animation timing>
  - <hover/press behavior>
  - <transition>
decision_rules:
  if_dashboard_variant: <use-dark-mode>
  if_luxury_variant: <add-gold-accents>
anti_patterns:  # 절대 하지 말 것
  - <ex: Dark mode by default>
  - <ex: AI purple/pink gradients for finance>
severity: HIGH | MEDIUM | LOW
```

**페이지별 override (선택):**
페이지별 특수 요구(예: 체크아웃 페이지는 신뢰성 강조) 있으면 페이지 파일로 분기 작성.

### Step 3 — 디자인 토큰 확정
`styles.md`에서 선택된 스타일의 정확한 값을 가져와 프로젝트 토큰으로 확정한다:

- **Colors**: primary / primary-hover / secondary / neutral-50~950 / success / warning / error / surface / surface-elevated (+ dark variants)
- **Typography**: heading font / body font / mono / scale (12 14 16 18 24 32) / weights (400 500 600 700) / line-heights
- **Spacing**: 4pt/8pt 증분 시스템 (4 8 12 16 24 32 48 64)
- **Radius**: none / sm / md / lg / xl / full
- **Shadows**: xs / sm / md / lg / xl + inner (스타일에 맞게)
- **Animation**: duration tokens (150 / 200 / 300 / 400ms) + easing tokens
- **Breakpoints**: 375 / 768 / 1024 / 1440

WCAG AA 최소 4.5:1 대비는 토큰 확정 시 검증한다.

### Step 4 — Stitch MCP 연동 (선택)
Stitch MCP가 연결되어 있으면 Step 2·3에서 확정된 설계를 기반으로 **구체적 프롬프트**로 목업을 생성한다.

❌ Bad: "Modern SaaS dashboard"
✅ Good: "SaaS dashboard, Glassmorphism + Flat Design style, Trust Blue (#0066CC) primary + Neutral grey, Professional typography hierarchy, subtle 200ms hover transitions, 8pt spacing, sidebar navigation with data-dense KPI cards"

Stitch가 없으면 이 단계는 건너뛰고 바로 코드 구현으로 간다 (디자인 토큰이 이미 확정되었으므로 가능).

### Step 5 — 전달 전 검증 (필수)
`ux-guidelines.md`의 체크리스트를 돌린다. CRITICAL 항목 (접근성·터치 타겟·명암비)은 반드시 통과.
검증 결과의 심각도는 아래 **심각도 체계**의 CRITICAL / WARNING / INFO 3단계로 보고한다.

## 규칙 카테고리 우선순위

| # | 카테고리 | 영향도 | 핵심 체크 |
|---|----------|--------|----------|
| 1 | 접근성 | CRITICAL | 명암비 4.5:1, 포커스 링, ARIA 레이블, 키보드 네비 |
| 2 | 터치 & 상호작용 | CRITICAL | ≥44×44pt 타겟, 8pt 간격, 로딩 피드백, 호버만 의존 금지 |
| 3 | 성능 | HIGH | WebP/AVIF, 레이지 로딩, CLS < 0.1 |
| 4 | 스타일 선택 | HIGH | 제품 유형 매칭, 일관성, SVG 아이콘 (이모지 아이콘 금지) |
| 5 | 레이아웃 & 반응형 | HIGH | 모바일 퍼스트, 가로 스크롤 없음, 안전 영역 |
| 6 | 타이포그래피 & 컬러 | MEDIUM | 본문 ≥16px, 줄높이 1.5+, 시맨틱 토큰 (raw hex 금지) |
| 7 | 애니메이션 | MEDIUM | 150–300ms, 의미 있는 모션, transform/opacity만 |
| 8 | 폼 & 피드백 | MEDIUM | 가시 레이블, 필드 근처 오류, 인라인 검증 |
| 9 | 네비게이션 | HIGH | 하단 네비 ≤5, 예측 가능한 백, 딥 링킹 |
| 10 | 차트 & 데이터 | LOW | 범례, 툴팁, 접근 가능 색상 (색만으로 의미 전달 금지) |

## 심각도 체계 (Severity)

검증·리뷰 결과는 **CRITICAL / WARNING / INFO** 3단계로만 보고한다. `reasoning-rules.md`가 방출하는 규칙 severity(HIGH / MEDIUM / LOW)는 아래 매핑으로 변환한다:

| reasoning-rules severity | 게이트 판정 | 의미 |
|--------------------------|------------|------|
| HIGH | **CRITICAL** | 게이트 차단 — 미해결 시 머지 금지 |
| MEDIUM | **WARNING** | 수정 권장 — 사유 기록 후 조건부 통과 가능 |
| LOW | **INFO** | 참고 — 개선 여지 안내 |

위 "규칙 카테고리 우선순위" 표의 영향도(CRITICAL/HIGH/MEDIUM/LOW)는 **카테고리별 중요도** 척도이며, 개별 검증 결과 보고 시에는 이 3단계(CRITICAL/WARNING/INFO)로 환산해 표기한다. (카테고리 HIGH ⇒ CRITICAL, MEDIUM ⇒ WARNING, LOW ⇒ INFO)

## 자주 무시되는 문제 (전문성 결정 요소)

### 아이콘 & 시각
- **이모지를 아이콘으로 쓰지 말 것** → SVG (Heroicons, Lucide) 사용. 이모지는 폰트 의존·플랫폼 불일치.
- **획 너비 일관성** — 같은 레이어에서 1.5px와 2px 혼용 금지.
- **채워진 vs 아웃라인** — 하나의 계층 레벨에 하나의 스타일만.
- **아이콘 크기 토큰화** — 무작위 20/24/28pt 혼합 금지.

### 상호작용
- **탭 피드백 80–150ms** — 즉시 ripple/opacity/elevation 반응.
- **레이아웃 이동 없는 프레스 상태** — 주변 콘텐츠 움직임 금지.
- **제스처 충돌 방지** — 지역당 하나의 주요 제스처.

### 밝음/다크 모드
- 다크 모드는 **역색이 아니라 탈포화 + 밝은 음**.
- 시맨틱 토큰 사용, 화면별 hex 하드코딩 금지.
- 두 모드에서 독립적으로 명암비 검증.

### 레이아웃
- 안전 영역 (노치/상태바/제스처 바) 존중 — 고정 헤더/탭바/CTA 모두.
- 4/8pt 리듬 유지.
- 스크롤 콘텐츠가 sticky bar 뒤 숨겨지지 않도록 inset 추가.

## 워크플로우 통합

이 스킬은 `~/.claude/rules/workflow.md`의 **Design Phase**가 자동 활성화한다. 사용자가 UI/프론트엔드 작업을 요청하면:

1. Step 1~2를 먼저 실행 (**코드 작성 전**)
2. 사용자에게 MASTER 설계 시스템 보여주고 확인
3. Step 3로 토큰 파일 작성 (`design-system/MASTER.md` 또는 프로젝트 토큰)
4. Step 4 (Stitch 있으면 목업, 없으면 스킵)
5. 구현 후 Step 5로 검증

## 관련 슬래시 커맨드

- `/design-system` — 제품 유형만 주면 MASTER 설계 시스템 자동 생성
- `/design-audit` — 현재 코드의 안티패턴·접근성 위반 스캔
- `/design-setup` — Stitch MCP 연결 가이드 (옵션)
