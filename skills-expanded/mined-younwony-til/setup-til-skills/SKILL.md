---
name: setup-til-skills
description: |
  새 PC에서 TIL 저장소(또는 다른 프로젝트)를 클론한 직후 한 번 실행하여, ATLASSIAN_API_TOKEN/MCP/hooks/Docker/Confluence 페이지 ID 등 모든 hard dependency를 묻고 세팅하는 skill입니다.
  ADR 0001 (Skill Hard/Soft Dependency 분류)을 입력으로 사용하여, 어떤 skill이 어떤 사전 조건을 요구하는지 자동 진단하고, 충족되지 않은 항목만 사용자에게 묻습니다.
  Matt Pocock의 setup-matt-pocock-skills 패턴을 차용했습니다.

  다음 키워드/문맥에서 트리거됩니다:
  - "setup", "초기 세팅", "환경 세팅", "초기 설정"
  - "새 PC", "방금 클론", "처음 시작"
  - "skill 환경 점검", "MCP 점검", "사전 조건 확인"
  - "/setup-til-skills" 슬래시 커맨드로 직접 호출

  새 환경에서 TIL을 처음 열거나, 어떤 skill이 동작 안 한다는 진단이 필요할 때 사용하세요.
---

# Setup TIL Skills

새 PC 또는 새 프로젝트에서 한 번 실행하면, **글로벌 + 로컬 skill 60여 종이 동작 가능한 상태**로 환경을 세팅한다. 이미 충족된 항목은 건너뛰고, 빠진 것만 묻고 채운다.

## 왜 이 스킬이 필요한가

새 환경에서 `/work-log` 같은 skill을 실행했더니 ATLASSIAN_API_TOKEN 누락 에러가 뜬다. 그제서야 토큰을 찾고 `~/.bashrc`를 고친다. 다음에는 Slack MCP 연결이 안 됐다는 걸 발견한다. 그 다음에는 hook 실행 권한이 빠졌다.

이런 시행착오를 한 번에 끝낸다. ADR 0001의 Hard/Soft 분류 표를 입력으로 받아, **충족 안 된 항목만 인터랙티브하게 처리**한다.

---

## 워크플로우

### Step 1: ADR 0001 로드

`.claude/docs/adr/0001-skill-dependency-classification.md` 를 읽어 Hard dependency 표를 메모리에 적재.

이 표가 없으면:
- "ADR 0001이 없습니다. 기본 표로 진행할까요? (Y/n)"
- 기본 표 (이 SKILL.md 끝의 BUILTIN_DEPS 사용).

### Step 2: 환경 진단 (병렬 실행)

다음을 모두 동시에 실행하여 현황 파악:

| 점검 항목 | 명령 | 기대 |
|---------|------|------|
| OS / Shell | `uname -a`, `echo $SHELL` | 정보성 |
| Git | `git --version` + `git config user.name/email` | 둘 다 설정됨 |
| GitHub CLI | `gh auth status` | logged in |
| Node.js | `node --version` | v18+ |
| Java | `java -version` | TIL이라면 17+ |
| Docker | `docker info` (성공 여부) | 정상 |
| `mysqlsh` | `which mysqlsh` | DB 점검 skill 필요 시 |
| ATLASSIAN_API_TOKEN | `[ -n "$ATLASSIAN_API_TOKEN" ] && echo SET \|\| echo MISSING` | SET |
| Codex CLI | `which codex` | 있으면 work-plan 크로스체크 가능 |
| Gemini CLI | `which gemini` | 있으면 work-plan 크로스체크 가능 |
| Hooks 실행 권한 | `[ -x .claude/hooks/block-dangerous.sh ]` | 실행 가능 |

> 실패해도 멈추지 않는다. 결과를 표로 모아 Step 3에 전달.

### Step 3: 진단 보고서 출력

```markdown
## 환경 진단 결과

### ✅ 충족됨 (N개)
- Git (user.name=youn, user.email=...)
- Node v22.1.0
- Docker (running)
- GitHub CLI (logged in as younwony)

### ⚠️ 미충족 (M개)
- ATLASSIAN_API_TOKEN: 환경변수 없음 → work-log/work-share/meeting-notes/slack-to-confluence 차단
- Slack MCP: 연결 안 됨 → slack-* skill 7종 차단
- Jira MCP: 연결 안 됨 → jira-report/jira-notify 차단
- mysqlsh: 미설치 → db-inspect/db-tune/prod-db-inspect 차단
- Hooks 실행 권한: block-dangerous-ssh.sh 권한 없음

### 영향
미충족으로 인해 차단되는 skill: M개
지금 setup하면 즉시 사용 가능한 skill: N개 + 추가 K개
```

### Step 4: 인터랙티브 setup (미충족 항목만)

각 미충족 항목에 대해 **한 번에 하나씩** 처리. 사용자 답변을 받기 전에 다음 항목으로 가지 않는다.

#### 4-1. ATLASSIAN_API_TOKEN

```
ATLASSIAN_API_TOKEN이 설정되지 않았습니다.

이 토큰은 다음 skill에서 사용됩니다:
- /work-log, /work-share (Confluence 작업 로그)
- /meeting-notes (회의록 → Confluence)
- /slack-to-confluence

생성 방법:
  1. https://id.atlassian.com/manage-profile/security/api-tokens 방문
  2. "Create API token" 클릭
  3. 토큰 복사

지금 설정할까요?
  (a) 지금 환경변수에 추가 (~/.bashrc 또는 ~/.zshrc)
  (b) 나중에 직접 추가하겠음 (skip)
  (c) 토큰 값을 입력 (이 세션에만 export)
```

선택 (a) 시:
```bash
SHELL_RC="$HOME/.$(basename $SHELL)rc"
echo "export ATLASSIAN_API_TOKEN='YOUR_TOKEN_HERE'" >> "$SHELL_RC"
```
(YOUR_TOKEN_HERE 자리는 사용자가 직접 채우도록 안내).

#### 4-2. MCP 연결 (Slack/Jira/Atlassian/Pencil/Figma 등)

```
다음 MCP가 연결되지 않았습니다:
- Slack MCP (영향: slack-* 7종)
- Jira MCP (영향: jira-* 2종)

연결 방법: ~/.claude/mcp.json (또는 프로젝트 .claude/mcp.json) 편집

지금 진행할까요?
  (a) ~/.claude/mcp.json 열어서 추가 가이드 보기
  (b) skip (해당 skill은 동작 안 함)
```

선택 (a) 시 `~/.claude/mcp.json` 의 현재 상태 출력 + 누락된 MCP 항목의 템플릿 제시.

#### 4-3. Hook 실행 권한

```
다음 hook 파일이 실행 권한이 없습니다:
- .claude/hooks/block-dangerous-ssh.sh
- .claude/hooks/log-edits.sh

지금 권한 부여할까요? (Y/n)
```

Y → `chmod +x .claude/hooks/*.sh`

#### 4-4. mysqlsh / Docker / 기타 도구

```
mysqlsh가 설치되지 않았습니다.

영향: db-inspect, db-tune, prod-db-inspect (DB skill 3종)

설치 명령:
  - macOS:   brew install mysql-shell
  - Windows: scoop install mysql-shell  또는  공식 인스톨러
  - Linux:   apt install mysql-shell  또는  rpm

지금 설치 명령 실행할까요? (Y/n/skip)
```

#### 4-5. Confluence 페이지 ID

```
work-log/work-share용 Confluence 부모 페이지 ID:

CLAUDE.md에 등록된 기본값:
- 사이트: https://temcolabs.atlassian.net
- 홈페이지 ID: 1983742135
- 개인 스페이스: ~645023757

다른 값을 사용하시겠습니까?
  (a) 기본값 사용 (skip)
  (b) 새 값 입력
```

#### 4-6. Codex / Gemini CLI (선택)

```
Codex CLI / Gemini CLI가 설치되지 않았습니다.

이건 hard dependency가 아니지만, 있으면 다음 skill의 품질이 향상됩니다:
- /work-plan (계획 크로스체크)
- /3ai-plan (3-AI 협업) ← Hard
- /self-review, /review-pr, /team-review (외부 검증)

설치 안내:
  - Codex: npm install -g @openai/codex
  - Gemini: https://github.com/google-gemini/gemini-cli

지금 설치하시겠어요? (Y/n/later)
```

### Step 5: 산출물 — `.claude/docs/setup-state.json`

setup 결과를 저장하여, 다음 실행 시 변경 사항만 처리.

```json
{
  "version": 1,
  "setup_at": "2026-04-29T15:30:00+09:00",
  "host": "WIN-...",
  "status": {
    "git": "ok",
    "gh_cli": "ok",
    "atlassian_token": "ok",
    "slack_mcp": "skipped",
    "jira_mcp": "skipped",
    "mysqlsh": "installed",
    "docker": "ok",
    "codex_cli": "missing",
    "gemini_cli": "missing",
    "hooks_executable": "ok"
  },
  "blocked_skills": [
    "slack-to-jira", "slack-digest", ...
  ],
  "available_skills": [
    "work-plan", "work-plan-start", ...
  ]
}
```

### Step 6: 최종 보고

```markdown
## Setup 완료

### 즉시 사용 가능한 skill (N개)
- work-plan, work-plan-start, self-review, qa-scenario, browser-debug, ...

### 차단된 skill (M개)
- slack-* (Slack MCP 미연결)
- jira-* (Jira MCP 미연결)
→ 나중에 `/setup-til-skills` 다시 실행 시 진행 가능.

### 다음 단계
- 첫 작업: `/work-plan path/to/req.md` (또는 그냥 `/work-plan`)
- Track 현황 보기: `/track-status`
- 도메인 용어 확인: `.claude/CONTEXT.md`
```

---

## Built-in 기본 의존성 표 (ADR 0001 없을 때 fallback)

```yaml
hard_dependencies:
  ATLASSIAN_API_TOKEN:
    skills: [work-log, work-share, meeting-notes, slack-to-confluence]
  slack_mcp:
    skills: [slack-to-jira, slack-digest, slack-remind, standup-summary, sprint-start-notify, slack-to-confluence, meeting-notes]
  jira_mcp:
    skills: [jira-report, jira-notify]
  figma_team_mcp:
    skills: [figma-read]
  pencil_mcp:
    skills: [pencil-screen, pencil-update, pencil-to-code]
  chrome_mcp_or_playwright:
    skills: [browser-debug, browser-debug-chrome]
  mysqlsh:
    skills: [db-inspect, db-tune, prod-db-inspect]
  ssh_keys:
    skills: [ssh-server-inspect]
  docker:
    skills: [docker-up, docker-update, docker-down, docker-logs, docker-status]
  gh_cli:
    skills: [pr, review-pr]
  excel_tool:
    skills: [excel-reader]
  codex_or_gemini:
    skills: [3ai-plan]   # 둘 다 필요
  workspec_md:
    skills: [work-plan-start]
  feature_checklist_md:
    skills: [feature-check]

soft_dependencies:
  context_md:
    enhances: [zoom-out, improve-codebase-architecture, code-refactor]
  codex_or_gemini_optional:
    enhances: [work-plan, self-review, review-pr, team-review]
```

---

## 주의사항

- **destructive 명령은 사용자 명시적 승인 후에만**. `chmod +x`도 yes/no를 묻는다.
- 이 skill은 **idempotent** 해야 한다. 두 번 실행해도 안전.
- 환경변수는 `.bashrc`/`.zshrc`에만 추가. 이미 있으면 중복 추가 X.
- API 토큰 값을 직접 출력하지 않는다 (`echo $TOKEN` 금지). 존재 여부만 확인.
- `setup-state.json`은 `.claude/docs/` 에 저장 (`.claude/`는 git add 안 됨 — 안전).
- 이 skill의 SKILL.md를 수정했으면 `/sync-global push`로 양쪽 동기화.
