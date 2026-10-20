# /craft-export — Export for Resumely

Phase 1 분석 결과를 Resumely 호환 Markdown 파일로 내보냅니다. Resumely의 "Pantheon 가져오기"에서 이 파일을 전달하면 LLM이 직접 파싱합니다.

**설계 원칙**: LLM이 읽고 쓰는 포맷은 Markdown이 가장 토큰 효율적. JSON/YAML 중간 변환 없이 Markdown → Markdown으로 전달.

## Usage

```
/craft-export <project-name>
```

## Arguments

- `$ARGUMENTS`: 프로젝트명 (workspace 내). 필수.

## State Machine

### Guard
- `workspace/{project}/.state.yaml` 존재
- `current_state`가 `analyzed` 이상 (Phase 1 완료)
- `analysis/architecture.md`, `analysis/narrative.md`, `analysis/stack-profile.md` 모두 존재

### Event Logging
- export 시작/완료를 `.state.yaml` log에 기록

## Process

### 1. 프로젝트 상태 확인

```
workspace/$ARGUMENTS/.state.yaml
```

- `current_state`가 `analyzed`, `designing`, `design_review`, `building`, `validating`, `build_review`, `deploying`, `done` 중 하나인지 확인
- 아닐 경우 에러: "Phase 1 분석이 완료되지 않았습니다. `/craft-analyze`를 먼저 실행하세요."

### 2. 분석 파일 읽기

다음 5개 파일을 읽습니다:

1. `workspace/$ARGUMENTS/analysis/architecture.md` — 필수
2. `workspace/$ARGUMENTS/analysis/narrative.md` — 필수
3. `workspace/$ARGUMENTS/analysis/stack-profile.md` — 필수
4. `workspace/$ARGUMENTS/analysis/SUMMARY.md` — 선택 (없으면 생략)
5. `workspace/$ARGUMENTS/analysis/experience-blocks.md` — 선택 (없으면 생략)

파일이 없으면 에러와 함께 어떤 파일이 누락되었는지 알려줍니다.

### 3. Markdown 번들 생성

분석 파일들을 하나의 Markdown으로 병합합니다. **요약이 아닌 원문 병합** — Resumely 측 LLM이 직접 파싱합니다.

```markdown
# {project-name} — Pantheon Export

> Exported from open-pantheon | {ISO 8601 timestamp}

---

# Architecture

{architecture.md 전체 내용}

---

# Narrative

{narrative.md 전체 내용}

---

# Stack Profile

{stack-profile.md 전체 내용}

---

# Summary

{SUMMARY.md 전체 내용 — 파일 없으면 이 섹션 생략}

---

# Experience Blocks

{experience-blocks.md 전체 내용 — 파일 없으면 이 섹션 생략}
```

**규칙**:
- 각 파일의 내용을 그대로 포함 (요약/변환 금지)
- 파일 내 H1(`#`)은 H2(`##`)로 한 단계 낮춤 (충돌 방지)
- 섹션 구분은 `---` (horizontal rule)
- 선택 파일이 없으면 해당 섹션 자체를 생략

### 4. 파일 저장

```
workspace/$ARGUMENTS/export/resumely.md
```

`export/` 디렉토리가 없으면 생성합니다.

기존 `resumely.json`이 있으면 삭제합니다 (deprecated).

### 5. 상태 로그 업데이트

`.state.yaml`의 `log`에 다음 이벤트 추가:

```yaml
- timestamp: "ISO 8601"
  event: "export_complete"
  agent: "craft-export"
  message: "Exported for Resumely"
  details:
    target: "resumely"
    format: "markdown"
    output: "export/resumely.md"
```

## Output

성공 시:

```
Exported $ARGUMENTS for Resumely
  workspace/$ARGUMENTS/export/resumely.md

  Resumely에서 가져오기:
  1. Resumely → Experience Hub
  2. "Pantheon 프로젝트 가져오기"
  3. resumely.md 파일 전달
```

## Example

```
/craft-export n8n
/craft-export bim-ontology
```
