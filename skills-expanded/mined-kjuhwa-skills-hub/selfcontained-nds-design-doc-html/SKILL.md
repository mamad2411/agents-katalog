---
version: 0.1.0-draft
name: selfcontained-nds-design-doc-html
description: 외부 CSS/JS 의존 없이 단일 .html로 완성되는 Lucida/NDS 톤 디자인 문서 템플릿. As-Is/To-Be, 페이지 맥락 목업, 다이얼로그, 인터랙션, API 테이블, MoSCoW Phase 카드 등 10개 섹션 카드로 구성. 메일/Slack/PR에 첨부해도 깨지지 않는 self-contained 아티팩트가 필요할 때 사용.
category: design
tags: [html, mockup, nds, lucida, self-contained, design-doc]
---

# Self-contained NDS 스타일 디자인 문서 HTML

## 언제 쓰는가

- 기획서(.md)와 **쌍으로 붙일 비주얼 목업**이 필요한데, Figma 링크 공유가 제한적이거나 오프라인 리뷰 상황
- 이해관계자에게 메일/Slack/PR로 **HTML 하나만 던져도 그대로 보이는** 문서가 필요할 때
- Lucida의 NDS 팔레트·톤(심각도 색, brand blue, line/muted 중립톤)을 대충이라도 유지하고 싶을 때

Figma가 확보되면 `nds-html-mockup-from-tokens` 쪽이 상위 호환이다. 이 스킬은 **Figma 없이** 기획서만 가지고 도면을 뽑는 용도.

## 핵심 원칙

1. **외부 요청 금지** — Google Fonts, CDN icon, fetch 전부 금지. `<style>` 한 블록 + 인라인 SVG만.
2. **CSS 변수로 NDS 톤 근사치**를 먼저 정의. 하드코딩된 색 값 반복 금지.
3. **섹션 카드 패턴** — `<section class="card">` + `<h2><span class="num">{N}</span> ...</h2>` + `<div class="body">`. 번호는 기획서 섹션과 1:1.
4. 목업은 **실제 컴포넌트를 흉내낸 div 구조**로 그린다. `<img>` placeholder 금지.

## 팔레트 (복붙용)

```css
:root{
  --bg:#f4f6fa; --panel:#ffffff; --ink:#1b1f27; --muted:#6b7380;
  --line:#e4e7ee; --line-strong:#c9cfdb;
  --brand:#1c6dd0; --brand-weak:#e9f1fb;
  --sev-crit:#d23f3f; --sev-warn:#e08a1a; --sev-caut:#e0b41a; --sev-ok:#2b8a58;
  --chip:#eef1f6; --chip-ink:#3a4453;
  --accent:#7a3ff2;
  --mono: ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --shadow: 0 6px 24px rgba(18,30,55,0.08);
  --radius: 10px;
}
body{font:14px/1.55 "Pretendard","Apple SD Gothic Neo","Segoe UI",system-ui,sans-serif;color:var(--ink);background:var(--bg);margin:0}
```

## 권장 섹션 구성 (10 카드)

| # | 섹션 | 주 콘텐츠 |
|---|---|---|
| 1 | 요약 · 핵심 변경점 | 3열 그리드 카드, 한 줄 hook + 한 문장 설명 |
| 2 | As-Is vs To-Be | `compare.col` 2열, As-Is는 빨강 태그·To-Be는 초록 태그, `<ul>` 대비 리스트 |
| 3 | 페이지 맥락 | 탭·액션바·테이블 목업. 심각도 `.sev.crit/warn/caut/info/ok` 뱃지, `.truncate`로 말줄임 연출 |
| 4 | 다이얼로그 목업 | `.stage`(줄무늬 배경)에 `.modal` 올리기. 상단 툴바 + `.collist`(☰ 핸들 + .checkbox + 뱃지) + 하단 좌:위험버튼 / 우:취소·저장 |
| 5 | 핵심 인터랙션 | 드래그 재배치·너비 리사이즈·우클릭 메뉴·확인 모달. 2×2 그리드 |
| 6 | 사용자 시나리오 | `.steps`에 번호 달린 5 스텝 카드, 각 스텝 상단 원형 번호 뱃지 |
| 7 | API 설계 | Method 칩(GET/POST/PUT/PATCH/DELETE 색상 구분) + 경로 + 용도 테이블 + 다크 codeblock(JSON) + 에러 응답 테이블 |
| 8 | Phase (MoSCoW) | Must/Should/Could/Won't 4열 카드, 색상 태그 구분 |
| 9 | 수용 기준 | 체크박스 box UI로 시각적 체크리스트 |
| 10 | Open Questions | `<ol>` 단순 나열 |

각 카드 스타일(권장):
```css
section.card{background:#fff;border:1px solid var(--line);border-radius:10px;
  box-shadow:var(--shadow);margin:18px 0;overflow:hidden}
section.card > h2{margin:0;padding:16px 22px;border-bottom:1px solid var(--line);
  font-size:15px;background:#fbfcff;display:flex;align-items:center;gap:10px}
section.card > h2 .num{display:inline-flex;align-items:center;justify-content:center;
  width:22px;height:22px;border-radius:6px;background:var(--brand);color:#fff;font-size:12px;font-weight:700}
section.card > .body{padding:22px}
```

## 관용 마이크로 컴포넌트

- `.btn` / `.btn.primary` / `.btn.danger` / `.btn.sm` — 9~13px 패딩, 5~6px radius, 라인 버튼 기본
- `.sev.{crit|warn|caut|info|ok}` — `::before` 원형 점 + pill 스타일 뱃지
- `.chip` — 선택된 컬럼 등 태그 표현. `.x`로 제거 아이콘
- `.collist .row` — 드래그 핸들(☰) + checkbox div + name + 우측 width meta
- `.m.{GET|POST|PUT|PATCH|DELETE}` — HTTP method 태그, 각 색상 고유
- `.codeblock` — 다크(#0f172a) JSON/코드 블록, `.k/.s/.c` span으로 키/문자열/주석 색 구분

## 검증

태그 밸런스 체크는 항상 마지막에:
```bash
node -e "const fs=require('fs');const s=fs.readFileSync('{path}','utf8');
['section','div','table','ul'].forEach(t=>{
  const o=(s.match(new RegExp('<'+t+'(?:\\\\s|>)','g'))||[]).length;
  const c=(s.match(new RegExp('</'+t+'>','g'))||[]).length;
  console.log(t, o, '/', c);
});"
```

브라우저에서 열었을 때:
1. 스크롤 시 섹션 헤더가 sticky하지 않도록(기본 그대로 둘 것). 긴 스크롤 허용.
2. 960px 미만에서 `.grid-2`·`.grid-3`·`.phase`·`.steps`가 1~2열로 접히는지.
3. 브라우저 인쇄 시 다이얼로그 `.stage`의 줄무늬 배경이 잉크 낭비라 `@media print{.stage{background:none}}` 추가 가능.

## 실패 모드

| 상황 | 대처 |
|---|---|
| 기획서에 API 설계 없음 | 섹션 7 자체 삭제하고 남은 번호 재정렬. 빈 카드 두지 말 것. |
| 한국어 폰트가 두꺼워 보임 | `Pretendard`가 없으면 `Apple SD Gothic Neo` fallback. Noto Sans KR CDN은 금지(외부 요청). |
| 다크모드 요청 | CSS 변수를 `@media (prefers-color-scheme: dark)`로 재정의. 기본은 라이트 고정(리뷰 환경이 대개 라이트). |
| 파일이 커짐(>50KB) | 인라인 SVG 반복 제거, 목업 테이블 행 수 줄이기. 30KB 내외가 이상적. |

## 참고 결과물

- `specs/alarm/design/알람이벤트_컬럼_개인화설정_디자인.html` (605줄, 31KB, 섹션 10 / div 153, 모두 쌍 밸런스)
