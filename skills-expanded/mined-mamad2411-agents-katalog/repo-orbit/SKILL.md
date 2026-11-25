---
name: repo-orbit
license: Apache-2.0
metadata:
  version: 1.5.0
description: >
  레포지터리를 7가지 관점(SAFE/ARCH/DEP/BUILD/DATA/OPS/DOC)으로 자동 분석하고
  기준을 통과한 기술 이슈만 GitHub/GitLab 이슈로 발행하는 코드베이스 점검 파이프라인.
  "레포 분석해줘", "코드베이스 점검", "기술 부채 찾아줘", "이슈 자동 등록",
  "CI 빠졌는지 봐줘", "의존성 점검", "테스트 커버리지 확인", "$repo-orbit" 같은
  요청이 오면 반드시 이 스킬을 사용한다.
  레포 URL 또는 로컬 경로가 있으면 바로 실행하고, 없으면 먼저 물어본다.
---

# repo-orbit 🪐

7개 관점(view)을 요일마다 하나씩 고정 배정해 레포를 분석하고, 기준을 통과한 finding만 이슈로 발행한다.
각 view는 **3개의 서브 에이전트**를 병렬 실행하고, **Orchestrator**가 사실 관찰을 병합해 채점한다.

이 문서는 **core 규칙**만 담는다.
실제 view별 에이전트 지시는 `agents/`, JSON 스키마와 템플릿은 `references/`, 반복 실행 로직은 `scripts/`에서 읽는다.

## 디렉터리 구조

```text
repo-orbit/                          # 스킬 루트
├── SKILL.md                         # 스킬 메인 규칙과 실행 흐름
├── assets/                          # README용 시각 에셋
│   └── repo-orbit.png               # repo-orbit 대표 이미지
├── agents/                          # view별 에이전트와 Orchestrator 지침
│   ├── orchestrator.md              # 공통 제어, 병합, triage, 발행 규칙
│   ├── SAFE.md                      # 변경 안전성 view 지침
│   ├── ARCH.md                      # 경계 건강도 view 지침
│   ├── DEP.md                       # 의존성/설정 안정성 view 지침
│   ├── BUILD.md                     # 빌드/배포 재현성 view 지침
│   ├── DATA.md                      # 데이터 구조 & 흐름 view 지침
│   ├── OPS.md                       # 운영 관측성 view 지침
│   └── DOC.md                       # 지식 내구성 view 지침
├── references/                      # 공통 참조 문서와 출력 계약
│   ├── agent-playbook.md            # 에이전트 공통 조사 원칙과 승격 조건
│   ├── execution-lifecycle.md       # Step 3~4.5 실행 세부 규칙
│   ├── triage-rules.md              # triage override와 재검토 기준
│   ├── output-templates.md          # 이슈 본문과 최종 보고 템플릿
│   ├── coverage-log-schema.md       # coverage-log/result 저장 스키마
│   └── view-playbooks.md            # 과거 플레이북 호환 안내
└── scripts/                         # 자동 발행과 테스트 스크립트
    ├── publish_issue.py             # GitHub/GitLab 이슈 create/update/reopen
    └── test_publish_issue.py        # 발행 스크립트 회귀 테스트
```

## Quick Start

```text
# 기본 실행 (오늘 요일에 맞는 view 자동 선택)
$repo-orbit https://github.com/owner/repo

# 현재 디렉터리가 레포일 때
$repo-orbit .

# 특정 view 강제 지정 (요일 무관)
$repo-orbit https://github.com/owner/repo --view SAFE

# 분석만 하고 이슈는 발행하지 않음 (안전하게 결과 미리 보기)
$repo-orbit https://github.com/owner/repo --dry-run

# triage 기준 완화 (이슈가 너무 안 올라올 때)
$repo-orbit https://github.com/owner/repo --triage-min-impact 3
```

레포 URL을 제공하지 않으면 현재 작업 디렉터리가 git 레포인지 먼저 확인하고,
그것도 아니면 사용자에게 URL을 요청한다.

## 요일별 View 배정

| 요일 | view_id | 관점 | 핵심 질문 |
|------|---------|------|-----------|
| 월 | `SAFE`  | 변경 안전성 | 핵심 흐름에 테스트·검증 게이트가 있는가 |
| 화 | `ARCH`  | 경계 건강도 | FSD 레이어 의존성이 올바른 방향인가, 슬라이스 경계가 지켜지는가 |
| 수 | `DEP`   | 의존성/설정 안정성 | 환경변수·버전 고정이 분산·중복되지 않는가 |
| 목 | `BUILD` | 빌드/배포 재현성 | 로컬과 CI가 같은 경로를 타는가 |
| 금 | `DATA`  | 데이터 구조 & 흐름 | 데이터가 단일 출처에서 예측 가능한 경로로 흐르는가 |
| 토 | `OPS`   | 운영 관측성 | 장애 시 로그·알림·복구 경로를 빠르게 찾을 수 있는가 |
| 일 | `DOC`   | 지식 내구성 | 문서·의사결정 기록·온보딩 경로가 남아 있는가 |

## 실행 방식

이 스킬은 별도 옵션 없이 실행한다.
오늘 날짜 기준으로 view 하나를 선택해 Step 1~6을 순서대로 수행한다.

## 파이프라인 핵심

1. **View 결정**: 오늘 날짜 기준으로 기본 view를 선택한다.
2. **레포 구조 파악**: 상위 트리와 설정 파일을 확인해 스킵 조건을 판정한다.
3. **사실 관찰 수집**: 선택된 view의 서브 에이전트 3개를 병렬 실행해 사실 관찰만 받는다.
4. **병합·채점**: 중복 관찰을 병합하고 Orchestrator가 impact/urgency/confidence/actionability를 부여한다.
5. **Triage**: 통과 조건을 만족하는 finding만 이슈화 대상으로 고른다.
6. **발행**: triage 통과 finding마다 `scripts/publish_issue.py`를 호출해 이슈를 생성·업데이트한다.

`Step 4.5` 재조사는 **초기 채점 뒤, triage 전에** 선택적으로 발생한다.
정확한 흐름은 [`references/execution-lifecycle.md`](references/execution-lifecycle.md)를 읽는다.

## Step 1 — 레포 접근 + View 결정

### 레포 접근

실행 시작 전 레포에 접근할 수 있는지 확인한다.

1. **URL 제공된 경우**: 임시 디렉터리에 shallow clone한다.
   ```bash
   git clone --depth=1 <repo_url> /tmp/repo-orbit-<timestamp>
   ```
2. **`.` 또는 로컬 경로 제공된 경우**: `git fetch origin` 을 실행한다.
3. **아무것도 없는 경우**: 현재 디렉터리에 `.git`이 있는지 확인하고,
   있으면 fetch, 없으면 사용자에게 레포 URL을 요청한다.

접근 자체가 실패하면 `[error] 레포 접근 실패: <사유>`를 남기고 중단한다.

### View 결정

프롬프트에 `--view <VIEW>` 옵션이 있으면 요일과 무관하게 해당 view를 사용한다.
없으면 오늘 날짜 기준으로 아래 매핑을 따른다.

```text
월 SAFE
화 ARCH
수 DEP
목 BUILD
금 DATA
토 OPS
일 DOC
```

- `--dry-run` 옵션이 있으면 Step 6 발행 단계를 건너뛰고 이슈 payload를 출력만 한다.
- 날짜·요일은 항상 확인하되, 요일과 view가 달라도 오류가 아니다.
- Step 1 완료 후 최소한 아래를 보고한다.

```text
날짜 : YYYY-MM-DD (요일)
view : DATA — 데이터 구조 & 흐름
레포 : owner/repo
유형 : Node Backend          ← Step 2에서 판정 후 기입
옵션 : --dry-run (있을 때만)
```

## Step 2 — 레포 구조 파악 + 유형 판정

Orchestrator가 직접 아래를 확인한다.
목적은 **레포 유형 판정**과 **서브태스크 스킵 조건 판단**이다.

레포 유형(FSD Frontend / Generic Frontend / Node Backend / Python Backend / Go·Rust·Java / Monorepo / Microservices / Library / CLI / Static Site)에 따라 각 view 에이전트의 조사 경로가 달라진다.
유형 판정 기준과 view별 적용 가이드는 [`references/repo-types.md`](references/repo-types.md)를 읽는다.
판정 결과를 Step 1 보고에 한 줄 추가한다: `유형 : Monorepo (turborepo)`

**브랜치 기준:** Step 1에서 이미 clone/fetch를 완료했으므로 추가 fetch는 불필요하다.
분석 기준은 `origin/main` 또는 `origin/master`의 최신 HEAD다.
(shallow clone인 경우 HEAD만 존재한다. 깊은 히스토리가 필요한 분석은 그 시점에 `--unshallow`를 실행한다.)

- 파일 트리 상위 2단계
- `package.json`, `vite.config.*`, `tsconfig.*`
- CI 설정 파일 존재 여부 (`.github/`, `.gitlab-ci.yml` 등)
- 상태관리 라이브러리 사용 여부
- 테스트 파일 존재 여부 (`*.test.*`, `*.spec.*`)
- FSD 구조 여부 (`src/app/`, `src/pages/`, `src/features/` 등)

처리 원칙은 아래와 같다.

- 파일 트리 확인 자체가 불가능하면 실행을 중단하고 `[error] 레포 접근 실패: <사유>`를 남긴다.
- 일부 설정 파일만 없는 경우는 있는 것만 읽고 계속 진행한다.
- 선택된 view에 해당하는 파일이 없어 모든 서브태스크가 스킵되면 findings `0`으로 정상 종료한다.

## Step 3 — 사실 관찰 수집

선택된 view의 서브태스크 3개를 병렬 실행한다.
공통 제어 규칙은 [`agents/orchestrator.md`](agents/orchestrator.md)를, view별 역할과 스킵 조건은 `agents/<VIEW>.md`를 읽는다.

### 핵심 원칙

- Orchestrator는 **선택된 view 파일 하나만** 읽고 서브 에이전트를 띄운다.
- 서브 에이전트는 **사실 관찰만** 반환한다.
- 점수(impact, urgency, confidence, actionability)는 서브 에이전트가 붙이지 않는다.
- 관찰에는 직접 읽은 `file:line` 근거가 있어야 한다.
- 1라운드 결과가 2개 이상이면 2라운드 교차 반박을 진행한다.
- 채점 전 의문이 남으면 3라운드 Orchestrator 질의를 선택적으로 수행한다.

### 타임아웃 · 실패 처리 (인라인 요약)

에이전트별 제한:

| 상황 | 처리 |
|------|------|
| 에이전트 결과 미반환 (timeout/오류) | 나머지 결과만으로 계속 진행. `agent_errors`에 기록 |
| 결과 반환 에이전트 1개만 남음 | 2라운드 교차 반박 생략 |
| 전체 에이전트 실패 | 실행 중단, `[error] 모든 에이전트 실패` 보고 |

재시도는 하지 않는다. 실패한 에이전트가 맡았던 서브태스크 범위를 최종 보고에 명시한다.

### 반환 형식 요약

**1라운드 — observation** (서브 에이전트 → Orchestrator)

```json
{
  "agent": "A",
  "observations": [
    {
      "claim": "문제 한 문장",
      "evidence": ["src/path/file.ts:42"],
      "impact_surface": "영향 범위",
      "next_step": "구체적 다음 행동 한 문장"
    }
  ]
}
```

규칙: `impact`, `urgency`, `confidence`, `actionability`는 observation에 넣지 않는다.
추정·가능성만 있는 claim은 evidence 없으므로 올리지 않는다.

**2라운드 — rebuttal** (서브 에이전트 → Orchestrator)

직접 읽은 파일/코드와 충돌하는 claim에 한정한다.

```json
{
  "agent": "B",
  "rebuttals": [
    {
      "target_agent": "A",
      "target_claim": "반박 대상 claim 요약",
      "rebuttal": "반박 근거 한 문장",
      "evidence": ["반박을 뒷받침하는 파일:줄"]
    }
  ]
}
```

규칙: evidence 없는 rebuttal은 참고만 하고 confidence에 반영하지 않는다.
evidence 있는 rebuttal이 하나라도 있으면 해당 claim의 confidence는 `low` 후보가 된다.

**3라운드 — query_response** (서브 에이전트 → Orchestrator, 선택적)

Orchestrator가 사실 불명확 시 특정 에이전트에게 재확인을 요청할 때만 발생한다.

```json
{
  "agent": "A",
  "query_response": {
    "query": "Orchestrator 질의 내용 요약",
    "finding": "직접 확인한 결과 한 문장",
    "evidence": ["확인한 파일:줄"],
    "conclusion": "claim 유지 | claim 수정 필요 | claim 철회"
  }
}
```

규칙: 질의는 finding당 최대 1회, 에이전트당 최대 1회다.
`claim 철회` 시 finding을 제거하고 `queries_withdrawn`에 기록한다.

result.json 전체 스키마, comment_history, 병합 규칙은 [`references/execution-lifecycle.md`](references/execution-lifecycle.md)를 읽는다.

## Step 4 — 병합·채점

Orchestrator가 수집된 관찰을 병합하고 finding 단위로 채점한다.

핵심 원칙:

- 같은 `file:line`을 가리키는 관찰은 하나로 병합한다.
- 병합된 finding의 `agents`에는 원본 에이전트를 모두 남긴다.
- finding ID는 `evidence[0]` 경로 알파벳순으로 정렬한 뒤 `E1`, `E2`, `E3`로 부여한다.

채점 기준의 핵심은 아래와 같다.

### impact

| 점수 | 기준 |
|------|------|
| 5 | 핵심 비즈니스 경로 또는 보안/인증에 직접 영향 |
| 4 | 배포·CI·공통 모듈 등 넓은 범위에 영향 |
| 3 | 특정 기능이나 페이지에 국한 |
| 2 | 단일 컴포넌트 또는 비핵심 경로 |
| 1 | 코드 스타일·주석 수준 |

### urgency

| 점수 | 기준 |
|------|------|
| 5 | 현재 production에서 재현 가능 |
| 4 | 다음 배포 또는 신규 환경에서 즉시 재현 가능 |
| 3 | 조건부 재현 |
| 2 | 장기적 리스크 |
| 1 | 이론적 리스크 |

### confidence

- `high`: 직접 읽은 `file:line` 근거가 있고, evidence를 가진 반박이 없다
- `low`: 근거가 없거나 추정만 있거나, evidence를 가진 반박이 들어왔다
- `medium`: 위 두 조건 사이의 나머지

### Step 4.5 — 재심 (선택적)

채점 직후, triage 전에 두 가지 경로로 재심이 발생할 수 있다.

#### (a) Orchestrator 주도 재조사 (기존)

Orchestrator가 채점 결과에 기술적 의문을 가지면 해당 에이전트에게 재조사를 건다.

발동 조건:

- evidence 있는 rebuttal이 claim을 **일부만** 뒤집는 경우
- source와 generated 산출물이 서로 다른 사실을 가리키는 경우
- 테스트는 있지만 핵심 경로 커버 여부가 불명확한 경우
- 문서와 실제 코드 경로가 충돌하는 경우

#### (b) 에이전트 주도 이의 제기 (신규)

Orchestrator가 채점 결과를 에이전트에게 공유한 뒤, 에이전트가 점수에 동의하지 않으면 **추가 근거**를 들고 이의를 제기할 수 있다.

발동 조건:

- 에이전트의 finding이 triage 기준 미달로 스킵 예정일 때
- 에이전트가 원래 observation에 포함하지 않았던 **새 evidence**를 제시할 수 있을 때

이의 제기 형식:

```json
{
  "agent": "A",
  "objection": {
    "finding_id": "E2",
    "contested_field": "impact",
    "current_score": 3,
    "argument": "추가 근거로 영향 범위가 더 넓음을 확인했다",
    "new_evidence": ["src/api/routes.ts:42", "src/middleware/auth.ts:15"],
    "requested_score": 4
  }
}
```

규칙:

- 새 evidence가 없는 이의는 기각한다. "동의하지 않는다"만으로는 부족하다.
- finding당 이의 1회, 에이전트당 이의 1회.
- Orchestrator는 새 evidence를 확인하고 `sustained` (인용) 또는 `overruled` (기각)로 판정한다.
- `sustained`: 해당 필드를 재채점하고 triage를 다시 적용한다.
- `overruled`: 원래 점수를 유지한다. 판정은 최종이며 추가 항소 없음.

#### 공통 규칙

(a)와 (b) 모두 finding당 최대 1회. 하나가 발동하면 다른 하나는 발동하지 않는다.
`claim_refined / claim_withdrawn / claim_upheld / sustained / overruled` 중 하나로 귀결된다.
정확한 JSON 스키마는 [`references/execution-lifecycle.md`](references/execution-lifecycle.md)를 읽는다.

## Step 5 — Triage

모든 finding에 아래 기준을 순서대로 적용한다.
하나라도 스킵 조건에 걸리면 이슈화하지 않는다.

### 통과 조건

```text
1) impact >= 4 AND urgency >= 3
2) confidence != low
3) actionability.score >= 3
```

### actionability.score

아래 규칙의 합으로 계산한다. 재량 채점은 없다.

| 규칙 | 점수 |
|------|------|
| next_step에 파일 경로 포함 | +2 |
| next_step에 식별자 포함 | +1 |
| next_step에 CLI 명령어 포함 | +1 |
| next_step이 한 문장 이하 | +1 |

최대 점수는 `5`, 이슈화 최소 점수는 `3`이다.

### 자동 스킵 사유

| 조건 | skip_reason |
|------|-------------|
| impact < 4 | `low_impact` |
| urgency < 3 | `low_urgency` |
| confidence == "low" | `low_confidence` |
| actionability.score < 3 | `low_actionability` |

triage 통과 finding이 0개여도 실패가 아니다.
override 옵션, 재검토 트리거, 상세 예시는 [`references/triage-rules.md`](references/triage-rules.md)를 읽는다.

## Step 6 — 발행

`--dry-run` 옵션이 있으면 실제 API 호출 없이 이슈 payload만 출력하고 종료한다.

```bash
# dry-run: 이슈 payload 출력만 (API 호출 없음)
python3 scripts/publish_issue.py \
  --repo-url  https://github.com/owner/repo \
  --title     "[view: SAFE] ..." \
  --body-file /tmp/repo-orbit-issue.md \
  --fingerprint "pipeline:owner/repo:SAFE:E1" \
  --labels    automation \
  --dry-run
```

dry-run이 아닌 경우 triage 통과 finding마다 `python3 scripts/publish_issue.py`를 호출해 발행한다.
직접 `curl`과 `grep`으로 JSON을 파싱하지 않는다.

### 발행 전 사전 확인 (Preflight)

| 항목 | 확인 방법 | 없을 때 |
|------|-----------|---------|
| 레포 URL | Step 1에서 이미 확인 | Step 1에서 처리 완료 |
| `--dry-run` 옵션 | 프롬프트 확인 | 없으면 실제 발행 진행 |
| `scripts/publish_issue.py` | 파일 존재 여부 확인 | 실행 중단 + `[error] publish_issue.py 없음` |
| Python 3 | `python3 --version` | 실행 중단 + `[error] Python 3 필요` |
| 인증 토큰 | 환경변수 → `~/.repo-orbit/auth.json` 순으로 탐색 | 사용자에게 입력 요청. 없으면 manual payload로 종료 가능. dry-run이면 토큰 불필요 |

### 토큰 로드

`~/.repo-orbit/auth.json`을 읽은 뒤 해당 플랫폼 토큰을 추출한다.
환경변수 `GITHUB_TOKEN` / `GITLAB_TOKEN`이 있으면 우선 사용한다.
토큰이 없으면 사용자에게 직접 요청하고, 응답이 없으면 스크립트의 manual payload를 그대로 출력한다.

`auth.json` 구조는 `references/coverage-log-schema.md` 참조.

### 플랫폼 감지

| 레포 URL 패턴 | 플랫폼 | API Base |
|--------------|--------|----------|
| `github.com` 포함 | GitHub | `https://api.github.com` |
| 그 외 | GitLab | `auth.json`의 `gitlab_base_url` 또는 레포 URL scheme+host |

### Fingerprint 중복 체크

`scripts/publish_issue.py`가 아래를 모두 담당한다.

- 페이지네이션 처리
- JSON 구조 파싱
- 동일 fingerprint open 이슈 update
- 동일 fingerprint closed 이슈 → reopen하지 않고 `skipped_closed`로 반환
- 토큰/네트워크 오류 시 manual payload 반환

Orchestrator는 중복 체크용 임시 `grep` 로직을 만들지 않는다.

### 호출 예시

```bash
python3 scripts/publish_issue.py \
  --repo-url  https://github.com/owner/repo \
  --title     "[view: BUILD] 로컬과 CI 빌드 경로 일치" \
  --body-file /tmp/repo-orbit-issue.md \
  --fingerprint "pipeline:owner/repo:BUILD:E1" \
  --labels    automation
```

### 핵심 규칙

- 제목은 50자 이내로 자른다.
- 이슈 본문 하단에 `format_version: repo-orbit/v2.0.1`와 `fingerprint`를 반드시 포함한다.
- 동일 fingerprint open 이슈 → 제목·본문·label을 현재 포맷으로 update.
- 동일 fingerprint closed 이슈 → reopen하지 않는다. 최종 보고에 "이미 닫힌 이슈" 항목으로 기록하고, 사용자가 원하면 새 이슈를 열 수 있음을 안내한다.
- update 성공만 발행 성공 건수에 포함한다. `skipped_closed`는 별도 항목으로 집계한다.
- 발행 실패 항목이 있어도 나머지 finding은 계속 진행한다.
- 스크립트가 `manual_required`를 반환하면 title/body/labels/fingerprint를 그대로 최종 보고에 포함한다.

`format_version`은 상단 카드 구조나 필수 섹션 구성이 바뀔 때만 올린다.
이슈 본문 템플릿과 최종 실행 보고 템플릿은 [`references/output-templates.md`](references/output-templates.md)를 읽는다.

## 출력 계약

실행 종료 후 최소한 아래 항목은 항상 보고한다.

- 날짜
- 레포
- view
- 서브 에이전트 상태
- raw 관찰 수
- 병합 후 finding 수
- triage 통과/스킵 수
- 발행 성공/실패 수
- 내일 view

정확한 포맷은 [`references/output-templates.md`](references/output-templates.md)를 읽는다.

## Guide

필요한 문서만 읽고, 무조건 전부 읽지 않는다.

- [`agents/orchestrator.md`](agents/orchestrator.md)
  - Step 2~6 공통 제어 순서와 어떤 파일을 언제 읽는지 필요할 때
- `agents/<VIEW>.md`
  - 선택된 view의 서브태스크와 스킵 조건이 필요할 때
- [`references/agent-playbook.md`](references/agent-playbook.md)
  - view 공통 조사 우선순위, finding 승격 조건, 반례 처리 규칙이 필요할 때
- [`references/execution-lifecycle.md`](references/execution-lifecycle.md)
  - observation/rebuttal/query/result.json/comment_history/reexamination의 정확한 형식이 필요할 때
- [`references/triage-rules.md`](references/triage-rules.md)
  - triage override, 재검토 트리거, 상세 스킵 정책이 필요할 때
- [`references/output-templates.md`](references/output-templates.md)
  - 이슈 본문과 최종 실행 보고 템플릿이 필요할 때
- [`references/repo-types.md`](references/repo-types.md)
  - 레포 유형 판정 기준과 유형별 view 적용 가이드가 필요할 때
  - Monorepo, Microservices, Library, CLI, Python/Go/Rust 등 비 FSD 레포를 분석할 때
- [`references/coverage-log-schema.md`](references/coverage-log-schema.md)
  - coverage-log 저장 위치와 스키마, 에이전트 실패 기록 방식이 필요할 때
- [`scripts/publish_issue.py`](scripts/publish_issue.py)
  - 발행 로직, fingerprint 처리, manual payload 형식이 필요할 때

## 최소 규칙

- 근거 없는 claim을 만들지 않는다.
- 서브 에이전트는 점수 없이 사실만 반환한다.
- Orchestrator만 병합, 채점, triage, 발행 판단을 한다.
- Step 3에서는 선택된 view 파일만 읽는다.
- fingerprint는 `pipeline:<repo>:<view_id>:<finding_id>`를 유지한다.
- 동일 fingerprint open 이슈는 스킵하지 않고 최신 `format_version`으로 update한다.
- 동일 fingerprint closed 이슈는 reopen하지 않는다. 최종 보고에 별도 항목으로 표시하고 사용자에게 안내한다.
