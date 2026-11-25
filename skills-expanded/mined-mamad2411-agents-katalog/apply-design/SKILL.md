---
name: apply-design
description: 붙여넣은 DESIGN.md, shadcn.io Copy markdown, 디자인 토큰, 스타일 설명을 현재 프로젝트용 `DESIGN.md`로 정리하고 요청받으면 UI에 적용한다. 사용자가 "DESIGN.md 만들어줘", "디자인 적용해줘", "이 디자인 느낌으로 해줘", "copy markdown 붙여넣을게"라고 할 때 사용한다.
---

# 디자인 적용 (Apply Design)

목표: 디자인 참고 자료를 프로젝트가 계속 읽을 수 있는 `DESIGN.md`로 만들고, 요청받은 경우 현재 UI에 반영한다.

`DESIGN.md`는 PRD가 아니다. 무엇을 만들지 결정하는 문서가 아니라, 화면을 어떤 시각 언어로 만들지 정하는 디자인 기준이다.

## 입력 (Input)

다음 중 하나를 받을 수 있다.

- shadcn.io/design 같은 곳에서 복사한 DESIGN.md markdown
- YAML frontmatter가 있는 디자인 토큰 문서
- 색, 폰트, 간격, 컴포넌트 느낌을 설명한 텍스트
- 기존 프로젝트의 `DESIGN.md`

붙여넣은 내용이 없으면 먼저 붙여넣어 달라고 말한다.

## 진행 절차 (Workflow)

1. 현재 디렉토리가 프로젝트 루트(root)인지 확인한다.
2. 기존 `DESIGN.md`, `AGENTS.md`, `CLAUDE.md`, `docs/agents/starter-skills.md`, UI 관련 파일을 확인한다.
3. 붙여넣은 내용을 디자인 참고 자료(source design reference)로 읽는다.
4. 브랜드를 그대로 복제하지 않고 현재 프로젝트용 디자인 기준으로 각색한다.
5. 사용자가 `DESIGN.md` 생성이나 UI 적용을 요청했으면 프로젝트 루트에 `DESIGN.md`를 먼저 만들거나 업데이트한다.
6. `DESIGN.md`만 만들라는 요청이면 UI 파일은 수정하지 않는다.
7. 사용자가 "적용해줘"라고 요청한 경우에만 실제 UI/CSS/component 파일을 수정한다.
8. UI를 수정했다면 실행해서 화면을 확인한다. 웹 UI면 브라우저로 확인한다.

## 각색 규칙 (Adaptation Rules)

- 원본 브랜드 이름, 로고, 마크, 제품 고유 UI를 현재 프로젝트의 것처럼 주장하지 않는다.
- proprietary font는 필수 의존성으로 쓰지 않는다. 공개 폰트나 시스템 폰트 대체재를 적는다.
- `seo`, `author`, `website`, `related`, `questions`처럼 원본 페이지 홍보용 정보는 기본적으로 제거한다.
- 색, 타이포그래피, 간격, 컴포넌트 원칙은 프로젝트에 필요한 수준으로 유지한다.
- "Claude처럼", "Stripe처럼" 같은 요청은 정확한 복제가 아니라 "inspired by"로 기록한다.
- 상표, 로고, 브랜드 자산은 사용자가 제공하고 사용할 권리가 명확할 때만 프로젝트 자산으로 넣는다.

## DESIGN.md 형식

가능하면 이 구조를 사용한다. 붙여넣은 원문이 이미 DESIGN.md 형식이면 토큰은 보존하되 프로젝트용으로 정리한다.

```markdown
---
name: "<프로젝트 또는 디자인 이름>"
description: "<이 프로젝트의 디자인 방향>"
inspiredBy: "<선택 사항: 참고한 디자인 시스템>"
colors:
  primary: "#..."
typography:
  body:
    fontFamily: "..."
rounded:
  md: 8px
spacing:
  md: 16px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
---

# DESIGN.md

## 개요 (Overview)

이 프로젝트의 시각적 방향을 설명한다.

## 디자인 원칙 (Design Principles)

- ...

## 토큰 사용 (Token Usage)

색, 글꼴, 간격, radius를 어떻게 쓸지 적는다.

## 컴포넌트 규칙 (Component Rules)

버튼, 카드, 입력, 표, 대시보드, 차트 같은 반복 UI 규칙을 적는다.

## 해야 할 것과 하지 말 것 (Do's and Don'ts)

## 구현 메모 (Implementation Notes)

Tailwind, shadcn/ui, CSS variables, 폰트 대체재를 어떻게 적용할지 적는다.

## 알려진 제한 (Known Gaps)

폰트, 로고, 이미지, 애니메이션처럼 아직 확정되지 않은 것을 적는다.
```

## UI에 적용할 때 (When Applying)

`DESIGN.md`만 만들라는 요청이면 UI 파일을 수정하지 않는다. 이 경우 별도 승인 없이 문서를 작성하고 결과를 보고한다.

UI 적용 요청이면 `DESIGN.md`를 먼저 만든 뒤 그 기준을 읽고 적용한다.

적용 요청이 있으면 다음 순서로 한다.

1. `DESIGN.md`를 먼저 읽는다.
2. 현재 UI 스택을 확인한다. 예: Tailwind, shadcn/ui, CSS variables, `globals.css`, `tailwind.config.*`, `components.json`.
3. 가장 작은 공통 표면부터 바꾼다. 예: CSS variables, layout background, button/card/input 기본 스타일.
4. 기존 화면의 용도와 정보 구조를 유지한다. 디자인 적용을 이유로 기능을 바꾸지 않는다.
5. 사내 업무 도구는 마케팅 랜딩 페이지처럼 만들지 않는다. 읽기 쉬운 밀도, 표, 필터, 상태 표시를 우선한다.
6. 브랜드 참고 자료의 로고나 고유 마크를 복제하지 않는다.
7. 화면을 실행해서 확인한다. 확인하지 못한 것은 명확히 말한다.

## 완료 형식

```markdown
## 디자인 적용 완료 (Design Applied)

**작성/수정한 문서:** ...
**디자인 방향:** ...
**보존한 원본 요소:** ...
**프로젝트용으로 바꾼 요소:** ...
**UI 적용 여부:** ...
**확인한 것:** ...
**확인하지 못한 것:** ...
```
