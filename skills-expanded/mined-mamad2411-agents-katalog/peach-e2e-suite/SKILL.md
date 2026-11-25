---
name: peach-e2e-suite
description: |
  E2E 단위 시나리오를 조합한 통합 테스트 시나리오를 md로 생성·관리·실행하는 스킬.
  "통합 시나리오", "e2e suite", "통합 테스트", "시나리오 조합",
  "e2e 통합", "전체 흐름 테스트" 키워드로 트리거.
---

# E2E 통합 시나리오 오케스트레이터

단위 시나리오(.js)를 비즈니스 플로우 단위로 조합한 **통합 테스트 시나리오를 md로 생성**하고,
md를 읽어 **순차 실행 + 단계별 검증 + 코드/DB 검증**까지 처리한다.

peach-e2e-scenario(단위 실행)의 상위 오케스트레이션 레이어.

## 모드

| 모드 | 트리거 | 동작 |
|------|--------|------|
| `auto` (기본) | `/peach-e2e-suite [설명]` | 생성 + 실행 |
| `create` | `/peach-e2e-suite create [설명]` | 통합 시나리오 md 생성만 |
| `run` | `/peach-e2e-suite run [md 파일명]` | 기존 md를 읽어 실행 |

## 생성 파일 경로

```
docs/e2e-suite/
└── {업무흐름}-{핵심동작}.md
    예: 재처방-결제-검증.md
        신규주문-전체흐름.md
        회원가입-로그인-검증.md
```

## 워크플로우

### 공통: 환경 확인

```bash
cd e2e && ./e2e.sh setup
cd e2e && ./e2e.sh status
```

`status`에서 `❌ Chrome CDP 미연결`이 보이면 아래 순서로 자동 복구를 먼저 시도한다.

1. `cd e2e && ./e2e.sh chrome &` 실행
2. `sleep 4` 대기
3. `cd e2e && ./e2e.sh status` 재확인
4. 여전히 미연결이면 사용자에게 `cd e2e && ./e2e.sh chrome` 수동 실행을 안내한다

탭 목록을 사용자에게 보여주고 탭 번호 확인.

> Google/OAuth/관리자/결제/기존 Chrome Beta 프로필 세션 유지가 핵심인 통합 흐름은
> md 생성/분석까지만 진행하고, 실제 Step 실행은 사용자 승인 후 시작한다.

> **탭 드리프트 방지**: 탭 번호 응답 후 `agent-browser tab N` 직후
> `agent-browser eval "document.title + ' | ' + location.href"` 로 재검증한다.
> 예상과 다르면 `./e2e.sh status` 재출력 후 재선택.

> **파일 업로드 Step 포함 시**: OS 네이티브 파일 다이얼로그 차단을 위해
> `Page.setInterceptFileChooserDialog` 방식을 사용한다.
> (상세: `peach-e2e-browse/references/SPA-프레임워크-입력패턴.md §3`)

### create 모드

1. **요청 파악** — 사용자의 자연어 요청에서 테스트 대상 업무 플로우 파악
2. **단위 시나리오 탐색** — 기존 시나리오 목록 확인
   ```bash
   cd e2e && ./e2e.sh list
   ls e2e/시나리오/**/*.js
   ```
3. **시나리오 코드 분석** — 관련 단위 시나리오 .js 파일을 읽어 동작/입출력 파악
4. **DOM 선조사** (필요시) — agent-browser eval로 페이지 구조 확인
5. **정보 확인** — 사용자에게 확인:
   - 통합 시나리오 이름 (한글, kebab-case)
   - 포함할 단위 시나리오 목록 + 순서
   - 각 단계별 검증 포인트
   - 코드/DB 검증 항목 (있으면)
6. **md 생성** — `references/suite-템플릿.md` 참조하여 작성
7. **저장** — `docs/e2e-suite/{이름}.md`
   - 폴더 없으면 자동 생성
8. **완료 보고**

### run 모드

1. **md 파일 선택**
   ```bash
   ls docs/e2e-suite/*.md
   ```
   사용자가 파일 지정하거나, 목록에서 선택
2. **md 파싱** — frontmatter + 시나리오 흐름 읽기
3. **사전조건 확인** — md의 사전조건 섹션을 읽고 충족 여부 확인
4. **실행 승인 확인** — 민감 세션/고정 프로필 유지 흐름이면 실제 Step 실행 전 사용자 승인 확인
5. **순차 실행 루프** — 각 Step마다:
   a. 단위 시나리오 실행: `cd e2e && ./e2e.sh run --tab N 시나리오/경로`
   b. 실패 시: peach-e2e-scenario의 자동수정 패턴 적용 (에러 파싱 → DOM 확인 → 수정 → 재실행, 최대 3회)
   c. 검증 포인트 확인: agent-browser eval로 DOM/URL 상태 검증
   d. 전달 데이터 추출: 다음 Step에 필요한 데이터를 컨텍스트에 보관 (예: orderId)
   e. 데이터 주입: 다음 Step 실행 시 환경변수로 전달 (`E2E_ORDER_ID=xxx`)
6. **코드 검증** (md에 섹션이 있으면) — 해당 파일을 Read/Grep으로 확인
7. **DB 검증** (md에 섹션이 있으면) — peach-db-query 스킬 또는 직접 SQL 실행
8. **결과 보고** — 각 Step 결과 + 최종 통합 기준 충족 여부

### auto 모드 (기본)

create → run 연속 실행. 생성 후 바로 실행하여 검증.

## 단계별 실패 처리

| 상황 | 처리 |
|------|------|
| 단위 시나리오 실행 실패 | 자동수정 루프 3회 시도 (peach-e2e-scenario 패턴) |
| 자동수정 3회 실패 | 해당 Step에서 중단, 실패 보고 |
| 검증 포인트 불일치 | 기대값과 실제값을 보고, 사용자 판단 요청 |
| 코드/DB 검증 실패 | 불일치 내용 보고, 사용자 판단 요청 |

> Step 실패 시 후속 Step은 실행하지 않는다 (데이터 의존성 때문).

## 데이터 전달 방식

단위 시나리오는 독립 프로세스(`node`)로 실행되어 메모리 공유 불가.
AI가 중간 데이터를 컨텍스트에 유지하고, 환경변수로 주입한다.

```bash
# Step 1에서 orderId 추출
agent-browser eval "location.pathname.split('/').pop()"
# → orderId = "12345"

# Step 2에 주입
cd e2e && E2E_ORDER_ID=12345 ./e2e.sh run --tab 0 시나리오/2-결제.js
```

> 단위 시나리오 .js 코드에서 `process.env.E2E_ORDER_ID`로 접근 가능.
> connect.js의 `origin`처럼 환경변수 기반 주입이 기존 패턴과 일관된다.

## md 구조

`references/suite-템플릿.md` 참조.

### frontmatter

```yaml
---
name: 재처방-결제-검증
module: tang
created: 2026-04-14
---
```

### 본문 구조

```markdown
# {통합 시나리오 이름}

## 사전조건
- Chrome Beta CDP 연결, 로그인 완료
- {필요한 데이터/상태}
- 탭: {시작 페이지}

## 시나리오 흐름

### Step 1: {단계명}
- 실행: `시나리오/{경로}.js`
- 검증:
  - {DOM/URL 검증 포인트}
- 전달 데이터: `{변수명}` ({추출 방법})

### Step 2: {단계명}
- 실행: `시나리오/{경로}.js`
- 사전 주입: `E2E_{변수명}=${값}`
- 검증:
  - {검증 포인트}

### Step N: 결과 검증
- 실행: 없음 (AI가 직접 확인)
- DB 검증: `{SQL}` → {기대값}
- 코드 검증: `{파일경로}` — {확인할 로직}

## 최종 통합 기준
- {전체 통과 조건}

## 실행 이력
| 일시 | 결과 | 비고 |
|------|------|------|
```

## 핵심 원칙

- 단위 시나리오 .js 파일은 수정하지 않는다 — 통합 시나리오 md가 조합만 정의
- 실행은 반드시 `e2e.sh run`을 통해 — 직접 `node` 호출 금지
- 검증 포인트는 자연어로 기술 — AI가 해석하여 agent-browser eval로 확인
- Step 실패 시 후속 Step 실행 금지 (데이터 의존성)
- 실행 이력은 git log에서 확인한다. suite md 파일은 시나리오 정의만 포함하며 실행 결과로 변경되지 않는다.

## 도구 역할 분담

| 용도 | 도구 |
|------|------|
| 단위 시나리오 실행 | `./e2e.sh run` |
| 검증 포인트 확인 | `agent-browser eval` |
| 코드 검증 | Read, Grep |
| DB 검증 | peach-db-query 또는 직접 SQL |
| iframe 검증 | `./e2e/pwc.sh eval` (fallback) |

## 참조 문서

| 문서 | 용도 | 로드 조건 |
|------|------|-----------|
| `references/suite-템플릿.md` | md 생성 템플릿 | create, auto |

## 완료 후 안내

```
통합 시나리오가 완료되었습니다.

📄 파일: docs/e2e-suite/{이름}.md

**관련 스킬:**
- `/peach-e2e-scenario` — 단위 시나리오 생성/실행/자동수정
- `/peach-e2e-browse` — DOM 탐색/디버깅
- `/peach-e2e-suite run {파일명}` — 이 통합 시나리오 재실행
```
