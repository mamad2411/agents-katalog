---
name: dz-qa-scenario-builder
description: Use when the user asks to create a QA/review scenario sheet from an Amaranth 10 screen design document and a target Google Sheets URL. This skill copies the standard template tab into the destination spreadsheet using Google Sheets MCP tools, renames it, fills header metadata, preserves formulas/formatting, and writes dense step-by-step test cases.
version: 0.1.0
---

# QA 검수시나리오 빌더 (qa-scenario-builder)

화면설계서를 기준으로 검수시나리오 구글시트를 만드는 스킬이다.
Google Sheets MCP 도구를 사용해 템플릿 시트를 복제하고, 상단 메타정보를 채운 뒤, 실무 검수용 밀도의 테스트 케이스를 작성할 때 사용한다.

## 사용할 때

- "화면설계서로 검수시나리오 작성해줘"
- "검수 시트 만들어줘"
- "검수 탭 추가해줘"
- "QA 시나리오 작성해줘"
- "검수시나리오 빌더로 [설계서명] 처리해줘"

## 전제 조건

1. **Google Sheets MCP 연결 확인**
   - `list_sheets`, `get_sheet_data`, `copy_sheet`, `rename_sheet`, `update_cells`, `batch_update_cells`, `find_cells` 도구 가용 여부 확인
   - MCP 미연결 시 → Markdown 형식 테스트 케이스로 대체 가능

2. **sheets-config.json 로드** (있는 경우)
   - 템플릿 스프레드시트 ID와 탭명 확인
   - `templates.qa-scenario` 섹션에서 템플릿 정보 참조

3. **화면설계서 → 메타정보 추출**
   - 메뉴명, LNB 코드, 기능명 확인
   - 테스트 환경/URL/사전조건 파악

## 핵심 원칙

1. 항상 템플릿 시트를 복제해서 시작한다. 새 시트를 빈 상태에서 직접 만들지 않는다.
2. 상단 수식, 조건부 서식, 결과 영역 구조는 유지한다.
3. 상단 `통합테스트 ID`는 `TC-{LNB코드}-001` 규칙을 쓰고, 본문 테스트 케이스 번호는 `1, 2, 3...` 순번으로 작성한다.
4. 테스트 케이스는 `기능명 또는 검수 묶음명`으로 작성하고, 절차/예상결과를 여러 행으로 세분화한다.
5. `1depth~3depth`는 기능이 수행되는 화면 경로를 적는다.
6. 복잡한 화면은 요약하지 말고, 실무자 작성 시트 수준으로 잘게 쪼갠다.
7. 값 입력이나 항목 선택이 필요한 절차는 예시 값 또는 선택 항목을 절차와 예상결과에 함께 적는다.

## 작업 순서

1. 화면설계서명, 대상 구글시트 URL, 요청자 이름을 확인한다.
2. 화면설계서에서 메뉴명, 기능명, LNB 코드, 1depth~3depth 경로를 확인한다.
3. Google Sheets MCP 도구로 템플릿 시트를 대상 구글시트로 복제한다.
4. 새 시트명을 `[검수] {메뉴명 또는 기능명}`으로 바꾼다.
5. 상단 메타정보를 채운다.
6. 검수율 수식과 조건부 서식은 템플릿 값을 유지한다.
7. 화면설계서를 처음부터 끝까지 읽으면서 기능 묶음별 테스트 케이스를 만들고, 각 묶음 아래 절차를 순차적으로 작성한다.
8. 예외 케이스가 있으면 다른 값, 다른 선택 항목, 비정상 입력 기준의 별도 테스트 케이스를 추가한다.
9. 작성이 끝나면 `설계서 누락/예외/Validation/추가 확인 절차` 기준으로 자체 점검하고 필요한 케이스를 보강한다.
10. 보강 후에는 추가된 테스트 케이스가 하단에만 쌓이지 않도록 실제 검수 흐름에 맞게 위치를 다시 정렬한다.
11. 설계서 규칙이 모호하거나 누락된 항목은 `예상결과`에 `화면설계 미기재/재확인 필요` 메모를 추가해 표시한다.
12. 같은 기능의 연관 설계서, 공통 정책, 히스토리 문서가 있으면 함께 대조해 누락된 검수 포인트를 보강한다.

템플릿 복제와 메타정보 채우기 상세는 `references/workflow.md`를 본다.
테스트 케이스를 어느 수준까지 쪼개야 하는지는 `references/case-writing-rules.md`를 본다.

## 빠른 규칙

- 시트명: `[검수] {기획서 기준 메뉴명/기능명}`
- 상단 `통합테스트 ID`: `TC-{LNB코드}-001`
- 본문 `테스트 케이스 번호`: `1, 2, 3...`
- `테스트 케이스`: 화면명이 아니라 검증하려는 기능명
- `1depth~3depth`: 기능이 위치한 메뉴/탭/팝업 경로
- 같은 기능 묶음의 연속 행은 `테스트 케이스`, `1depth~3depth` 셀 병합을 우선 검토
- 입력/선택 절차는 예시 값 또는 선택 항목을 명시
- 예외 케이스는 별도 테스트 케이스로 분리
- 초안 보강 후 추가된 케이스는 하단에 두지 말고, 실제 검수 순서에 맞게 본문 위치를 다시 정렬
- 설계서 미흡 항목은 `예상결과`에 보강 메모를 추가하고, 가능한 경우 붉은색으로 강조
- 작성자: 기본값 `SBUnit {요청자명}`
- 테스트 사전조건: 기본값 유지, 특별한 전제조건이 있으면 교체
- 테스트환경: 기본값 `크롬(Chrome)`
- URL: 별도 URL/계정 정보가 없으면 템플릿 값 유지
- 상세정보: 요청받은 화면설계서명

## MCP 도구 활용

### 템플릿 시트 복제

```
MCP 도구: copy_sheet(
  spreadsheet_id="{템플릿ID}",
  source_sheet_name="{템플릿탭명}",
  destination_spreadsheet_id="{대상시트ID}"
)
```

### 시트탭명 변경

```
MCP 도구: rename_sheet(
  spreadsheet_id="{대상시트ID}",
  old_name="Copy of {템플릿탭명}",
  new_name="[검수] {메뉴명}"
)
```

### 헤더 메타정보 입력

```
MCP 도구: update_cells(
  spreadsheet_id="{대상시트ID}",
  range="'{시트명}'!F2:F8",
  values=[[통합테스트ID], [작성자], [메뉴], [사전조건], [테스트환경], [URL], [상세정보]]
)
```

### 테스트 케이스 본문 작성

```
MCP 도구: batch_update_cells(
  spreadsheet_id="{대상시트ID}",
  data=[
    { "range": "'{시트명}'!A10", "values": [["1"]] },
    { "range": "'{시트명}'!C10", "values": [["기능명"]] },
    ...
  ]
)
```

## 템플릿 정보

Google Sheets MCP가 연결된 경우, `sheets-config.json`의 `templates.qa-scenario` 섹션에서 템플릿 정보를 참조한다:

```json
{
  "templates": {
    "qa-scenario": {
      "spreadsheet_id": "...",
      "sheet_name": "..."
    }
  }
}
```

MCP 미연결 시에는 Markdown 형식으로 테스트 케이스를 작성해 제공한다.

## 주의

- 템플릿 셀 위치를 외우고 바로 덮어쓰기보다, 현재 템플릿 라벨 구조를 먼저 읽고 작업한다.
- 복제 후 상단 수식/서식이 깨졌다면 수동 생성이 아니라 템플릿 복제 절차가 잘못된 것이다.
- 테스트 사이트 비밀번호는 사용자가 원하면 `표시 마스킹 + 내부 원문 유지` 방식으로 관리할 수 있다.
- 검수시나리오가 20~30건으로 끝나면 대개 너무 얕게 쓴 것이다. 복잡한 팝업/메뉴는 더 잘게 쪼갠다.

## 보조 자료

- 복제/채번/헤더 규칙: `references/workflow.md`
- 케이스 밀도와 작성 기준: `references/case-writing-rules.md`


## 마크다운 링크 규칙 (필수)

마크다운 파일 작성·업데이트 시 **모든 경로·파일 참조는 클릭 가능한 상대 링크**로 작성한다.

```markdown
# 나쁜 예 (클릭 불가)
법무관리/tasks/_current.md에서 확인

# 좋은 예 (클릭 가능)
[법무관리/tasks/_current.md](../법무관리/tasks/_current.md)에서 확인
```

- 상대 경로는 현재 파일 위치 기준
- 코드블록 안의 폴더 구조 다이어그램은 예외 (링크 불필요)
- 상세 규칙은 douzone-forge CLAUDE.md의 "마크다운 링크 표기 규칙" 섹션 참조
