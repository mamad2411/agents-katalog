---
name: peach-gen-diagram
description: |
  워크플로우, 시스템 구조, 아키텍처, 세션 흐름, 에이전트 협업, 문서 구조를 다이어그램으로 생성하는 스킬.
  "다이어그램 그려줘", "흐름도 만들어줘", "구조도", "아키텍처 다이어그램", "워크플로우 시각화",
  "Unicode box-drawing", "터미널풍 다이어그램", "Mermaid로 그려줘", "이미지처럼 다이어그램" 키워드로 트리거.
  DB 테이블 관계/ERD가 목적이면 peach-erd를 우선 사용하고, 이 스킬은 ERD 외 범용 다이어그램에 사용한다.
---

# 다이어그램 생성 스킬

## 목적

사용자의 설명, 문서, 코드 구조를 읽고 목적에 맞는 다이어그램 형식을 제안한 뒤 실제 다이어그램을 생성한다.

이 스킬은 ERD가 아닌 범용 시각화에 사용한다.
- 워크플로우
- 시스템/모듈 구조
- 세션 흐름
- 에이전트 협업 구조
- 문서/지식관리 구조
- 사용자 여정
- 배포/운영 흐름

## 핵심 원칙

- 먼저 목적과 독자를 파악한다.
- 형식이 명확하지 않으면 예시 형식을 보여주고 사용자가 선택하게 한다.
- 사용자가 빠른 결과를 원하면 AI가 가장 적합한 형식을 고르고, 선택 이유를 짧게 밝힌 뒤 바로 그린다.
- 형식 미지정 요청은 목적에 따라 자동 선택한다. 조건 분기, 합류, 계층 구조, 아키텍처, 상태 흐름, 렌더링 문서가 목적이면 **Mermaid**를 우선한다.
- 단순 CLI 절차, 짧은 사용 플로우, 원문 가독성이 중요한 안내는 **Unicode**를 사용한다.
- 사용자가 Mermaid, D2, PNG/SVG 렌더링, sequenceDiagram, C4 등 특정 형식을 명시하면 해당 형식을 우선하고 box-drawing 후보를 별도로 제안하지 않는다.
- 복잡한 관계, GitHub 렌더링, 장기 유지보수, 파일 산출이 핵심이면 Mermaid 또는 D2를 우선 고려한다.
- pure ASCII는 기본 후보에서 제외한다. 사용자가 명시하거나 Unicode 문자가 깨지는 환경이 확인된 경우에만 사용한다.
- DB 테이블 관계는 `peach-erd` 범위이므로 이 스킬에서 임의로 ERD 워크플로우를 대체하지 않는다.

## 형식 선택 가이드

| 형식 | 적합한 경우 | 산출물 |
|------|-------------|--------|
| Mermaid flowchart | 조건 분기, 합류, 업무 흐름, 시스템 흐름, 계층 구조, 아키텍처 개요, hook/command 파이프라인 | `.mmd`, Markdown Mermaid |
| Mermaid sequenceDiagram | 주체 간 호출 순서, API 요청/응답, 에이전트 협업 순서 | `.mmd`, Markdown Mermaid |
| Mermaid stateDiagram | 상태 전이, 승인/검증 단계, 작업 라이프사이클 | `.mmd`, Markdown Mermaid |
| Mermaid mindmap | 개념 분류, 기능 목록, 문서 목차 | `.mmd`, Markdown Mermaid |
| Unicode box-drawing | 짧은 절차, 단순 목록형 흐름, README에서 렌더링 없이 원문 그대로 읽는 안내. 터미널풍 표현이 필요한 경우 | Markdown `text` 코드블록 |
| D2 | 미감이 중요한 아키텍처/서비스 관계도, 발표·문서용 SVG 산출 | `.d2`, SVG/PNG |
| C4 스타일 | 시스템 경계, 컨테이너, 모듈 책임을 보여줄 때 | Mermaid/D2/Structurizr 중 선택 |

## 워크플로우

### 1단계: 입력 파악

다음 중 무엇을 받았는지 확인한다.
- 자연어 설명
- 이미지/스케치 설명
- 문서 경로
- 코드/디렉터리 구조
- 기존 Mermaid/ASCII 초안

파일이나 코드 기반 요청이면 먼저 관련 파일을 읽어 근거를 확보한다. `qmd`가 설치되어 있고 대상 프로젝트 지침에 인덱스명이 있으면 해당 인덱스로 위치를 먼저 찾는다.

### 2단계: 형식 제안 또는 자동 선택

사용자가 형식을 지정하지 않았고 선택이 필요한 경우 아래처럼 제안한다. 조건 분기·합류·계층 구조는 Mermaid를 기본 추천으로 두고, 짧은 절차나 원문 가독성이 핵심이면 Unicode를 추천한다.

```text
다이어그램 형식 후보입니다.

1. Mermaid flowchart
   - 장점: 흐름과 분기를 깔끔하게 렌더링 가능, SVG/PNG 저장 가능
   - 단점: 렌더러 문법에 민감하므로 라벨 작성 규칙을 지켜야 함

2. Unicode box-drawing
   - 장점: Markdown/위키 원문에서 바로 읽기 좋고 렌더링 도구가 필요 없음
   - 단점: 복잡한 관계나 자동 렌더링에는 약함. 한글 박스 정렬은 폰트/렌더러마다 흔들릴 수 있음

3. D2
   - 장점: 아키텍처/서비스 관계도를 더 현대적인 시각 품질로 렌더링하기 좋음
   - 단점: Mermaid보다 기본 지원 생태계가 좁음

제 판단으로는 [추천 형식]이 가장 적합합니다. 이유: [짧은 이유]
선택해주시면 그 형식으로 그리겠습니다. 바로 진행해도 되면 추천 형식으로 작성하겠습니다.
```

사용자가 "알아서", "추천해서", "바로 그려줘"라고 하면 선택 질문 없이 진행한다.

### 3단계: 다이어그램 작성

#### Unicode box-drawing

아래 규칙을 따른다.
- `text` 코드블록으로 제공한다.
- 상단 제목 박스를 둔다.
- 주요 노드는 `┌─┐`, `│`, `└─┘` 기반 사각형 박스로 표현한다.
- 주요 노드를 사각형 박스로 표현할 때는 라벨을 짧게 쓰고, 한글/영문 혼합으로 긴 문장을 넣지 않는다.
- 한글이 들어간 박스형 다이어그램은 표시폭이 렌더러/폰트마다 흔들릴 수 있으므로, 최종 문서에서 표시 상태를 확인한다.
- 흐름 방향은 `│`, `▼`, `├`, `└` 등 box-drawing과 잘 맞는 문자를 사용한다.
- 보조 설명은 다이어그램 아래 짧은 bullet로 둔다.

예시:

```text
┌──────────────────────────────────────────────┐
│                CLAUDE SESSION                │
└──────────────────────────────────────────────┘

┌────────────────────┐
│ SessionStart hook  │
│ cat wiki/hot.md    │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ prior context      │
│ injected           │
└─────────┬──────────┘
          ▼
┌──────────────────────────────────────────────┐
│       conversation + slash commands          │
└───────┬──────────────┬──────────────┬────────┘
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ wiki-ingest  │ │ save [slug]  │ │ autoresearch │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       └────────────────┴────────────────┘
                        ▼
                ┌──────────────┐
                │ git commit   │
                │ + push       │
                └──────┬───────┘
                       ▼
                ┌──────────────┐
                │ Stop hook    │
                │ update hot   │
                └──────────────┘
```

#### Mermaid

기본은 Markdown Mermaid 코드블록으로 제공한다.

```mermaid
flowchart TD
    A[SessionStart hook] --> B[prior context injected]
    B --> C[conversation + slash commands]
    C --> D[/wiki-ingest]
    C --> E[/save slug]
    C --> F[/autoresearch x]
    D --> G[git commit + push]
    E --> G
    F --> G
    G --> H[Stop hook updates wiki/hot.md]
```

Mermaid 작성 규칙:
- 노드 라벨은 짧게 쓴다.
- 복잡한 설명은 노드 밖의 설명으로 분리한다.
- 한국어 라벨을 사용할 수 있으나 특수문자가 많으면 따옴표로 감싼다.
- 렌더링 오류가 날 수 있는 괄호, 콜론, 슬래시는 필요한 경우 라벨 문자열로 감싼다.
- `/peach-*` 같은 슬래시 명령은 반드시 `Skill["/peach-team-dev"]`처럼 quoted label로 작성한다. `Skill[/peach-team-dev]` 형태는 렌더러에서 파싱 오류가 날 수 있다.
- 조건 분기와 합류는 Mermaid가 Unicode보다 시인성이 좋은 경우가 많으므로, 문서용 워크플로우라도 분기가 핵심이면 Mermaid를 우선한다.

### 4단계: 저장 여부 판단

사용자가 파일 저장을 요청하면 기본 경로를 제안한다.

| 산출물 | 기본 경로 |
|--------|-----------|
| Mermaid 소스 | `docs/diagrams/{slug}.mmd` |
| Unicode box-drawing 다이어그램 | `docs/diagrams/{slug}.md` |
| D2 소스 | `docs/diagrams/{slug}.d2` |
| Markdown 삽입 문서 | 요청 문서 내부 |
| PNG/SVG 렌더링 | `docs/diagrams/{slug}.png`, `docs/diagrams/{slug}.svg` |

저장 경로가 지정되어 있으면 사용자의 경로를 우선한다.

### 5단계: Mermaid 렌더링

Mermaid 파일을 저장했고 사용자가 PNG/SVG 저장 또는 미리보기를 원하면 CLI를 사용한다.

```bash
npx @mermaid-js/mermaid-cli@latest \
  -i docs/diagrams/{slug}.mmd \
  -o docs/diagrams/{slug}.png \
  -s 2

npx @mermaid-js/mermaid-cli@latest \
  -i docs/diagrams/{slug}.mmd \
  -o docs/diagrams/{slug}.svg
```

렌더링 실패 시 Mermaid 문법을 수정하고 한 번 재시도한다.

### 6단계: 검증

완료 전 다음을 확인한다.
- 형식이 사용자 목적에 맞는가
- 형식 미지정 요청에서 목적에 따라 Mermaid/Unicode/D2를 선택했는가
- 자동 선택 요청에서는 선택한 형식이 목적·독자·저장/렌더링 요구에 맞는가
- Mermaid는 문법 오류 가능성이 낮은가
- Mermaid에 `/peach-*` 슬래시 명령이 있으면 quoted label을 사용했는가
- Unicode 박스형에 한글이 들어가면 표시폭 흔들림 위험을 점검했는가
- 저장 요청이 있었다면 실제 파일이 생성되었는가
- 렌더링 요청이 있었다면 PNG/SVG 생성 결과를 확인했는가

## 응답 형식

생성만 요청받은 경우:

```text
추천 형식: [형식]
이유: [한 문장]

[다이어그램]
```

사용자가 형식을 명시한 경우에는 추천 형식/후보 목록을 생략하고 바로 해당 형식으로 작성한다.

파일까지 만든 경우:

```text
생성 완료:
- 소스: docs/diagrams/{slug}.mmd
- 렌더링: docs/diagrams/{slug}.png, docs/diagrams/{slug}.svg

검증:
- Mermaid CLI 렌더링 성공
```
