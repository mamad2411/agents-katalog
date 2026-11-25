---
tags: [design, plan, screen, spec, conversion]
name: plan-to-screen-spec-conversion
description: PLAN 작업지시서를 rules/fe/02-screen-spec-template.md 형식의 화면 스펙 문서로 변환
version: 0.1.0-draft
category: workflow
triggers:
  - "PLAN을 스펙으로"
  - "작업지시서를 화면 스펙으로"
  - "screen spec 변환"
  - "기획서를 스펙 템플릿으로"
source_project: polestar10-auto-pipeline
linked_knowledge:
  - lucida-ui-design-token-reference
---

# PLAN → 화면 스펙 변환

## Purpose
PLAN 작업지시서(자유 형식 기획서)를 `rules/fe/02-screen-spec-template.md` 표준 화면 스펙 형식으로 변환한다.
변환된 스펙은 `/generate-screen` 스킬의 입력으로 사용할 수 있다.

## When to Activate
- 사용자가 PLAN 또는 기획서를 화면 스펙으로 변환 요청
- "기획서 기반으로 스펙 만들어줘", "PLAN을 스펙으로 변환해줘"

## Input
- PLAN 작업지시서 파일 경로 (예: `examples/custom-table/PLAN_CUSTOM_TABLE_WIDGET.md`)

## Steps

### 1. PLAN 읽기 및 분석
- PLAN 파일을 읽고 핵심 구조를 파악:
  - 화면 목적, 데이터 구조, 엔티티, API, UI 흐름

### 2. 템플릿 참조
- `rules/fe/02-screen-spec-template.md`를 읽어 필수 섹션 구조 확인

### 3. 섹션별 매핑

| PLAN 섹션 | 스펙 섹션 |
|-----------|----------|
| 개요/목적 | 📋 기본 정보 + 🎯 화면 목적 |
| 엔티티/필드 정의 | 📊 데이터 구조 (필드/타입/설명/필수 테이블) |
| 프론트엔드 UI 구성 | 🎨 UI 요구사항 (레이아웃 ASCII + Sirius 컴포넌트 매핑) |
| API 엔드포인트 | 🔌 API 명세 (모두 POST 규칙 적용) |
| 보안 고려사항 | 🔒 권한 및 예외 처리 |
| 구현 순서 | 📝 추가 고려사항 |

### 4. Sirius 컴포넌트 매핑
PLAN의 UI 요소를 NDS/Sirius 컴포넌트로 매핑:
- 테이블 → `GridScroll` (AG Grid 기반)
- 폼 → `FormItem` (Vertical 기본)
- 팝업/다이얼로그 → `Modal` / `Confirm`
- 드롭다운 → `Select` / `Dropdown`
- 토글 → `Switch`
- 상태표시 → `Tag`
- 빈 상태 → `Empty`

### 5. i18n 키 생성
- 네임스페이스: `{모듈}.{기능}` (예: `widget.customTable`)
- 공통 키 사용: `cmm.search`, `cmm.reset`, `cmm.create` 등
- 화면 고유 키 목록 작성

### 6. 스펙 파일 생성
- 동일 디렉토리에 `SPEC_{기능명}.md` 파일 생성
- 체크리스트 섹션 포함

## Output
- `SPEC_{기능명}.md` — 화면 스펙 템플릿 형식 문서

## Rules
- API는 모두 POST (`05-api-guide.md` 규칙)
- Ant Design 직접 참조 금지 → Sirius 컴포넌트만
- 모든 UI 텍스트 → `tt()` 함수 (i18n)
- Grid → `GridScroll` (AG Grid), `Table` 사용 금지
- Form → `FormItem`, `Form.Item` 사용 금지
