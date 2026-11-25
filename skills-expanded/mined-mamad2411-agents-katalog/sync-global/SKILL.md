---
name: sync-global
description: >
  글로벌 Claude Code 설정(skills, commands, hooks, rules, agents, CLAUDE.md)을
  프로젝트 .claude/ 디렉토리와 동기화하는 스킬.
  여러 PC에서 작업할 때 Git 프로젝트를 동기화 채널로 활용하여 설정 일관성을 유지한다.
  "/sync-global", "설정 동기화", "글로벌 싱크", "스킬 동기화", "global sync" 요청 시 트리거.
  push(글로벌→프로젝트), pull(프로젝트→글로벌), status(비교만) 3가지 모드를 지원한다.
---

# Sync Global

글로벌 `~/.claude/` 설정과 프로젝트 `.claude/` 설정을 동기화한다.
여러 PC에서 동일한 Claude Code 환경을 유지하기 위해, Git 프로젝트를 동기화 채널로 사용한다.

## 동기화 대상

아래 디렉토리/파일만 동기화한다. 그 외는 무시한다.

| 대상 | 설명 |
|------|------|
| `skills/` | 스킬 디렉토리 전체 (SKILL.md + scripts/, references/ 등 하위 파일 모두) |
| `commands/` | 커맨드 파일 (.md) |
| `hooks/` | 훅 스크립트 (.sh) |
| `rules/` | 룰 파일 (.md) |
| `agents/` | 에이전트 정의 (.md) |
| `templates/` | 문서 폼 템플릿 (.html — report-template 등) |
| `CLAUDE.md` | 글로벌 설정 문서 — **프로젝트 측 경로는 `.claude/sync/GLOBAL-CLAUDE.md`** |

> **CLAUDE.md 경로 주의**: 프로젝트 `.claude/CLAUDE.md`는 Claude Code가 프로젝트 지침으로 자동 로드하므로, 글로벌 사본을 거기 두면 글로벌과 이중 로드된다(토큰 낭비 + 드리프트 시 규칙 충돌). 따라서 글로벌 CLAUDE.md의 동기화 사본은 자동 로드되지 않는 `.claude/sync/GLOBAL-CLAUDE.md`에 둔다. 프로젝트에 구버전 `.claude/CLAUDE.md`가 남아 있으면 동기화 시 삭제를 제안한다.

**절대 동기화하지 않는 항목:**
- `settings.json`, `settings.local.json` (머신별 환경 설정)
- `.credentials.json`, `.mcp.json` (시크릿/머신별 MCP)
- `plans/`, `sessions/`, `cache/`, `transcripts/`, `projects/` 등 임시 데이터
- `plugins/`, `chrome/`, `debug/`, `downloads/` 등 런타임 데이터

## 경로 규칙

```
GLOBAL_DIR = ~/.claude/          (글로벌 설정 디렉토리)
PROJECT_DIR = <프로젝트루트>/.claude/  (프로젝트 설정 디렉토리)
```

동기화 시 디렉토리 구조를 그대로 유지한다.
예: `~/.claude/skills/docker-up/SKILL.md` → `.claude/skills/docker-up/SKILL.md`

## 실행 흐름

### 인자 파싱

`$ARGUMENTS`에서 모드를 판별한다:
- `push` → 글로벌 → 프로젝트
- `pull` → 프로젝트 → 글로벌
- `status` (또는 인자 없음) → 비교만, 변경 없음

### Step 1: 파일 목록 수집

Bash를 사용하여 양쪽 디렉토리의 동기화 대상 파일 목록을 수집한다.

```bash
# 글로벌 파일 목록
GLOBAL="$HOME/.claude"
find "$GLOBAL/skills" "$GLOBAL/commands" "$GLOBAL/hooks" "$GLOBAL/rules" "$GLOBAL/agents" "$GLOBAL/templates" \
  -type f 2>/dev/null | sed "s|$GLOBAL/||"

# CLAUDE.md 별도 체크 (프로젝트 측 대응 경로: .claude/sync/GLOBAL-CLAUDE.md)
[ -f "$GLOBAL/CLAUDE.md" ] && echo "CLAUDE.md"
```

프로젝트 측도 동일하게 수집한다. 단 `CLAUDE.md`만 경로 매핑이 다르다:
`~/.claude/CLAUDE.md` ↔ `<프로젝트>/.claude/sync/GLOBAL-CLAUDE.md`

### Step 2: 파일 비교

각 파일을 내용 기준으로 비교한다. `diff -q`를 사용한다.

비교 결과를 3가지로 분류:
- **NEW**: 소스에만 존재 (대상에 없음)
- **MODIFIED**: 양쪽 모두 존재하지만 내용이 다름
- **DELETED**: 대상에만 존재 (소스에서 삭제됨)

방향에 따라 소스/대상이 달라진다:
- `push`: 소스=글로벌, 대상=프로젝트
- `pull`: 소스=프로젝트, 대상=글로벌

### Step 3: 변경 리포트 출력

아래 형식으로 리포트를 출력한다. mtime도 함께 표시하여 어느 쪽이 최신인지 알 수 있게 한다.

```
=== sync-global {mode} ===
방향: {소스} → {대상}

[NEW]      skills/weekly-retro/SKILL.md
[NEW]      commands/weekly-retro.md
[MODIFIED] skills/docker-up/SKILL.md (소스: 2일 전 | 대상: 5일 전)
[MODIFIED] hooks/block-dangerous.sh (소스: 1일 전 | 대상: 3일 전)
[DELETED]  skills/old-skill/SKILL.md (대상에만 존재, 소스에서 삭제됨)

--- 요약 ---
NEW:      2개
MODIFIED: 2개
DELETED:  1개
합계:     5개 변경
```

`status` 모드일 경우 여기서 끝. 양방향으로 각각 보여준다.

### Step 4: 사용자 확인

`push` 또는 `pull` 모드에서 변경사항이 있으면 AskUserQuestion으로 확인한다.

- 변경이 없으면: "이미 동기화 상태입니다." 출력 후 종료
- 변경이 있으면: 리포트를 보여주고 "위 변경사항을 적용하시겠습니까?" 질문
- DELETED 항목은 주의 문구 추가: "DELETED 항목은 대상에서 파일을 삭제합니다."

### Step 5: 동기화 실행

승인 후 파일을 복사/삭제한다.

```bash
# NEW/MODIFIED: 소스 → 대상 복사
# 디렉토리가 없으면 생성
mkdir -p "$(dirname "$TARGET_PATH")"
cp "$SOURCE_PATH" "$TARGET_PATH"

# DELETED: 대상에서 삭제
rm "$TARGET_PATH"
# 빈 디렉토리 정리
rmdir --ignore-fail-on-non-empty "$(dirname "$TARGET_PATH")"
```

### Step 6: push 모드 git add

`push` 모드에서만 동기화된 파일을 git add 한다.
이 스킬의 push 결과물은 `.claude/` 하위이지만, 동기화 목적이므로 예외적으로 git add를 수행한다.

```bash
# 동기화된 파일만 개별 git add
git add .claude/skills/docker-up/SKILL.md
git add .claude/commands/weekly-retro.md
# ... 각 변경 파일별로
```

**절대 git add 하지 않는 파일:**
- `.claude/settings.json`, `.claude/settings.local.json`
- `.claude/.credentials.json`, `.claude/.mcp.json`
- `.claude/plans/`, `.claude/projects/` 하위

### Step 7: 결과 보고

```
=== 동기화 완료 ===
복사: 4개 파일
삭제: 1개 파일

{push 모드일 때}
git add 완료. commit은 사용자 요청 시 수행합니다.
```

## mtime 계산 방법

```bash
# Windows Git Bash에서 mtime을 "N일 전" 형태로 표시
stat -c %Y "$FILE_PATH"  # epoch seconds
# 현재 시각과 비교하여 일수 계산
```

Git Bash에서 `stat` 명령이 없거나 다르게 동작할 수 있으므로, 대안으로:
```bash
# date 기반 mtime 확인
date -r "$FILE_PATH" "+%Y-%m-%d %H:%M"
```

## 주의사항

- `status` 모드는 읽기 전용이므로 항상 안전하게 실행 가능
- `push`/`pull` 모드는 반드시 리포트 확인 후 사용자 승인을 받아야 함
- DELETED 처리는 신중하게 — 사용자가 한쪽에만 의도적으로 추가한 파일일 수 있음
- 스킬 디렉토리는 내부 파일 전체(SKILL.md, scripts/, references/, assets/)를 재귀적으로 동기화
- 바이너리 파일(.png, .jpg 등)도 동기화 대상에 포함 (스킬 assets에 있을 수 있음)
