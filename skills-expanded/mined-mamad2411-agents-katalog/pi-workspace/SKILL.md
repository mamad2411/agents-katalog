---
name: pi-workspace
description: YoloBox + Pi + mise agent workspace를 관리한다. 초기화·검증·갱신·서브에이전트 구성·확장 설치·에이전트 지침 프롬프트 합성을 담당. 파일을 직접 작성하지 말고 반드시 mise 태스크를 실행한다.
---

# Pi Workspace

YoloBox + Pi + mise 기반 agent workspace를 새 프로젝트에 생성하거나 기존 workspace를 갱신·검증·설정한다.

## 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/pi-workspace:scaffold` | 새 프로젝트에 workspace 생성 |
| `/pi-workspace:subagents` | 인증된 프로바이더 기반 서브에이전트 구성 |
| `/pi-workspace:extensions` | pi 확장 패키지 카탈로그 조회·선택 설치 |
| `/pi-workspace:prompts` | 에이전트 지침 프롬프트 관리·합성 |
| `/pi-workspace:verify` | workspace 무결성 검증 |
| `/pi-workspace:update` | managedFiles 갱신 |
| `/pi-workspace:doctor` | 환경 상태만 확인 |
| `/pi-workspace:report` | 이슈를 GitHub에 리포팅 |

## 설치 확인

`/pi-workspace:scaffold` 같은 서브커맨드가 스킬 목록에 없으면 `--full-depth` 없이 설치된 것이다.
에이전트는 이 상황을 감지하면 사용자에게 재설치를 제안한다:

```bash
mkdir -p .claude
npx skills add siren403/pi-workspace --full-depth
```

감지 기준: 사용자가 `/pi-workspace:scaffold` 등을 호출했는데 스킬을 찾을 수 없다는 응답이 오거나,
현재 스킬 목록에 `pi-workspace-scaffold` 가 없는 경우.

## 기본 동작 `/pi-workspace`

서브커맨드 없이 호출되면 doctor를 실행하고 현재 상태에 따라 다음 단계를 제안한다.

```bash
cd .pi/skills/pi-workspace && mise run doctor -- --target <target>
```

상태별 제안:
- `.agent-workspace.json` 없음 → `/pi-workspace:scaffold` 안내
- workspace 있음 + agentOverrides 없음 + pi-subagents 설치됨 → `/pi-workspace:subagents` 안내
- workspace 있음 + 설정 완료 → 현재 구성 요약 출력
- doctor ERROR → 오류 항목과 수정 방법 안내 후 종료

## 실행 규칙

**에이전트는 파일을 직접 작성하지 않는다.**

모든 파일 생성·갱신은 이 스킬의 mise 태스크가 수행한다.

스킬 디렉토리에서 실행:
```bash
cd .pi/skills/pi-workspace

mise run doctor    -- --target <path>
mise run scaffold  -- --target <path>
mise run subagents -- --target <path>
mise run extensions -- --target <path>
mise run extensions -- --target <path> --install context-mode,pi-lens
mise run prompts   -- --target <path>
mise run prompts   -- --target <path> --preview karpathy
mise run prompts   -- --target <path> --install karpathy
echo "<content>" | mise run prompts -- --target <path> --write --section <name>
mise run verify    -- --target <path>
mise run update    -- --target <path>
```

scaffold 후 pi 실행:
```bash
mise run pi              # pi 세션 시작
mise run pi:fork         # 폴더 격리 환경
mise run pi:shell -- list  # 비대화형 검증
```

## /pi-workspace:scaffold 플로우

1. **doctor** 실행 → 결과 사용자에게 보고
2. ERROR 있으면 중단. 사용자가 수정 후 재실행 요청할 때까지 대기.
3. WARN은 사용자에게 안내 후 진행 여부 확인.
4. 모두 OK → **scaffold** 실행
5. scaffold 완료 후 **verify** 실행
6. 결과 요약 보고 + extensions·subagents 후속 안내

## /pi-workspace:subagents 플로우

> 선행 조건: pi 인증 완료 (`pi /login`), pi-subagents 설치 (`pi install npm:pi-subagents -l`)

1. `pi --list-models` 실행 → 인증된 프로바이더·모델 목록 파악
2. 역할별 모델 후보 제안 (scout=저비용·빠름, oracle=고성능)
3. 사용자 확인 또는 수정
4. `.pi/settings.json` agentOverrides 작성
5. `.pi/agents/*.md` model 필드 주입

## /pi-workspace:extensions 플로우

1. `mise run extensions -- --target <path>` → 카탈로그 + 현재 설치 상태 출력
2. 사용자가 설치할 패키지 선택
3. `mise run extensions -- --target <path> --install <name,...>` 실행
4. `pi install npm:<pkg> -l` 프로젝트 스코프로 설치

## /pi-workspace:prompts 플로우

AGENTS.md에 에이전트 행동 지침 프롬프트를 관리한다.

### 지원 args

| args | 동작 |
|------|------|
| (없음) | **스마트 모드** — 프로젝트 상태 파악 후 다음 행동 제안 |
| `list` | 카탈로그 목록 출력 |
| `preview <slug\|owner/repo>` | 템플릿 내용 출력 |
| `install <slug>[,<slug\|owner/repo>...]` | AGENTS.md에 정적 주입 |
| `suggest` | 프로젝트 분석 후 적합한 템플릿 추천 |
| `compose [<slug\|owner/repo>...]` | 지정 템플릿(들)을 프로젝트에 맞게 합성 |
| `"<자유 요청>"` | 의도를 파악해 위 args 중 적합한 흐름으로 라우팅 |

### args → mise task 매핑

```
# ── 1. 스마트 모드 (args 없음) ──────────────────────────────────────────────
/pi-workspace:prompts
  → mise run prompts -- --target <target> --context  ← 프로젝트 상태 수집
  → 상태별 판단:
      · AGENTS.md에 pi-prompts 섹션 없음  → suggest 흐름 진입
      · 섹션 있음 + 오래된 마커 감지      → update/compose 제안
      · 섹션 있음 + 최신                  → 현재 구성 요약 출력

# ── 2. 명시적 args ───────────────────────────────────────────────────────────
/pi-workspace:prompts list
  → mise run prompts -- --list

/pi-workspace:prompts preview karpathy
  → mise run prompts -- --preview karpathy

/pi-workspace:prompts install karpathy
  → mise run prompts -- --target <target> --install karpathy

/pi-workspace:prompts install karpathy,owner/repo
  → mise run prompts -- --target <target> --install karpathy,owner/repo

/pi-workspace:prompts suggest
  → mise run prompts -- --target <target> --context
  → 에이전트가 출력을 분석해 적합한 슬러그 추천 + 이유 설명
  → 사용자 확인 후 → install 또는 compose 진행

/pi-workspace:prompts compose
/pi-workspace:prompts compose karpathy
/pi-workspace:prompts compose karpathy,owner/repo
  → mise run prompts -- --target <target> --context
  → mise run prompts -- --preview <slug>  (지정된 슬러그 각각)
  → 에이전트가 프로젝트 컨텍스트 + 템플릿 내용으로 맞춤 합성
  → 결과를 사용자에게 제안 — 확인 전 파일에 쓰지 않는다
  → 승인 후: echo "<합성 내용>" | mise run prompts -- --target <target> --write --section <name>

# ── 3. 자유 요청 ─────────────────────────────────────────────────────────────
/pi-workspace:prompts "<자유 요청>"
  → 의도를 파악해 위 흐름 중 하나로 라우팅한다.

  라우팅 기준:
  · "추천", "뭐가 좋아", "어떤 거 쓸까"          → suggest
  · "합성", "조합", "맞게", "다듬어", "최적화"    → compose (슬러그 명시 시 포함)
  · "추가", "설치", "넣어줘" + 슬러그/레포 명시   → install
  · "보여줘", "내용", "뭐가 있어"                 → preview 또는 list
  · 의도 불명확 → 스마트 모드(--context)로 현황 파악 후 되묻기
```

### suggest / compose 상세 절차

`suggest`와 `compose` args는 **에이전트가 실행하는 흐름**이다. mise task 자체에 AI가 없다.

1. `--context` 플래그로 프로젝트 정보 수집
   - 현재 AGENTS.md 내용 및 기존 설치 섹션
   - `.pi/settings.json` (프로바이더·모델)
   - `package.json` / `.mise.toml` (기술 스택)
   - 카탈로그 목록

2. `compose`에 슬러그가 지정된 경우 `--preview`로 각 템플릿 내용 fetch

3. 에이전트가 컨텍스트를 바탕으로:
   - `suggest`: 적합한 템플릿 추천 + 이유 제시
   - `compose`: 템플릿 섹션 선별·통합, 중복 제거, 프로젝트 특화 규칙 추가

4. 결과를 사용자에게 제안 — **확인 전에 절대 파일에 쓰지 않는다**

5. 사용자 승인 후 task로 기록:
   ```bash
   echo "<합성 내용>" | mise run prompts -- --target <path> --write --section <name>
   ```

### 섹션 마커 형식

```
<!-- pi-prompts:karpathy:start -->
...내용...
<!-- pi-prompts:karpathy:end -->
```

기존 마커가 있으면 교체, 없으면 AGENTS.md 끝에 추가.

## 인터렉션 방식

사용자에게 선택지를 제시할 때 실행 환경에 따라 다음 순서로 도구를 선택한다.

1. `ask_user_question` 도구가 있으면 → **pi 환경** — 해당 도구 사용
2. `AskUserQuestion` 도구가 있으면 → **Claude Code 환경** — 해당 도구 사용
3. 둘 다 없으면 → 텍스트로 선택지 나열 후 응답 대기

환경 이름을 추정하지 않는다. 도구 가용 여부로만 판단한다.

## 금지

- auth.json, API key, .env, 시크릿 생성·복사 금지
- mise, bun, node 자동 설치 금지 (mise 없으면 중단하고 안내만)
- `--force` 없이 기존 파일 덮어쓰기 금지
- doctor ERROR 상태에서 scaffold 진행 금지
- `/pi-workspace:subagents` 실행 전 pi 인증 여부 반드시 확인
