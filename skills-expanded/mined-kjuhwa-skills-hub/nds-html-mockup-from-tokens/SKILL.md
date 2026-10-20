---
tags: [design, nds, html, mockup, from, tokens]
name: nds-html-mockup-from-tokens
description: lucida-ui 디자인 토큰을 추출하여 실제 제품과 동일한 스타일의 static HTML 목업 생성
version: 0.1.0-draft
category: design
triggers:
  - "HTML 목업"
  - "디자인 목업"
  - "NDS 스타일 HTML"
  - "lucida 디자인으로 HTML"
  - "화면 프로토타입"
source_project: polestar10-auto-pipeline
linked_knowledge:
  - lucida-ui-design-token-reference
---

# NDS 디자인 토큰 기반 HTML 목업 생성

## Purpose
lucida-ui 프로젝트의 실제 SCSS 디자인 토큰을 추출하여, 제품과 동일한 룩앤필의 static HTML 프로토타입을 만든다.
개발 전 디자인 검증 및 이해관계자 리뷰에 사용한다.

## When to Activate
- 사용자가 화면 디자인 목업, HTML 프로토타입 요청
- "디자인을 HTML로 볼 수 있게 해줘", "NDS 스타일로 목업 만들어줘"

## Prerequisites
- lucida-ui 프로젝트 접근 가능 (`D:/21_LUCIDA/lucida-ui/`)
- 또는 linked knowledge `lucida-ui-design-token-reference` 참조

## Steps

### 1. 토큰 소스 파일 읽기
lucida-ui에서 다음 파일들을 읽어 실제 값 확보:
```
packages/sirius/src/styles/
├── base/_palette.scss               → CSS 변수 팔레트 (--indigo-6 등)
├── tokens/base/_demo_size.scss       → spacing, border-radius
├── tokens/base/_demo_font.scss       → font-family, size, weight, line-height
├── tokens/themes/_demo_light-mode.scss → 시맨틱 토큰 (fill, line, text, state, alarm 등)
├── themes/_lightTheme.scss           → 테마 변수 (--background, --border 등)
├── themes/_darkTheme.scss            → 다크 테마 오버라이드
├── base/fonts/_font.scss             → @font-face, $siri-font
└── components/antd/                  → 컴포넌트별 오버라이드 (_button, _modal, _tab 등)
```

### 2. HTML 기본 구조
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    html { font-size: 10px; }  /* rem 기준 */
    body { font: 400 1.4rem/2.2rem 'Spoqa Han Sans Neo','Noto Sans KR','맑은고딕',sans-serif; }
  </style>
</head>
<body data-theme="sirius-theme">
```

### 3. CSS 변수 선언 규칙
- `:root`에 팔레트 + 시맨틱 토큰 모두 CSS 변수로 선언
- **하드코딩 색상 절대 금지** — 모든 곳에서 `var(--토큰명)` 사용
- 사이즈는 rem 단위 (`0.4rem` = 4px, `0.8rem` = 8px 등)

### 4. 컴포넌트별 스타일 (실제 antd 오버라이드 반영)

| 컴포넌트 | 핵심 스타일 |
|---------|-----------|
| Button default | height: 2.8rem, bg fill-standard-default, border 1px solid #d6dadb, border-radius-sm(0.4rem) |
| Button primary | bg fill-primary-default(#004cff), color text-inverse-default(#fff) |
| Select | height: 2.8rem, border-radius-sm |
| Input | border line-secondary-default, border-radius-sm |
| Tab | nav padding 0 2rem, tab padding 0.8rem, ink-bar fill-primary-default, active text-primary-default |
| Modal | bg fill-secondary-default, border-radius-sm, shadow modal-shadow-default, padding 1.6rem 2.4rem |
| Form label | font typography-sm-strong, color text-standard-default |
| Sider | bg #000614, menu color rgba(255,255,255,0.6), item height 3.6rem |
| Grid header | bg fill-tertiary-default, border line-standard-default |
| Summary Card | bg fill-standard-default, border line-standard-default, border-radius-sm |
| Tag | border-radius 999rem (pill) |

### 5. NDS 레이아웃 규칙
- **Title → 콘텐츠**: gap spacing-4 (1.6rem)
- **Subtitle → 콘텐츠**: gap spacing-2 (0.8rem)
- **블록 → 블록**: gap spacing-6 (2.4rem)
- **Summary Card 간**: gap spacing-2 (0.8rem), flex-wrap
- **일반 Card 간**: gap spacing-4 (1.6rem)
- **차트**: 2열 grid, gap spacing-4

### 6. Grid(테이블) 정렬 규칙
- 텍스트: left
- 숫자/퍼센트: right
- 아이콘/상태: center

### 7. 탭 네비게이션 JS
각 화면을 탭으로 분리, JavaScript로 전환 구현.

## Output
- `design-{기능명}.html` — 단일 HTML 파일 (CSS/JS 포함, 외부 의존성 없음)

## Rules
- html font-size: 10px 기반 rem 단위
- 모든 색상 CSS 변수 사용
- data-theme="sirius-theme" 스코핑
- 차트 색상: chart-data-legend-level-1~15 사용
- letter-spacing: 0.3px 전역
- 1200px (120rem) 고정폭 권장
