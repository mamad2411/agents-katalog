---
name: publish-persona
description: 페르소나를 GitHub에 퍼블리시할 때 호출. 리포 생성, remote 설정, push까지 진행.
allowed-tools: Read, Edit, Write, Bash, Glob
---

# Publish Persona to GitHub

## 중요: 현재 작업 디렉토리 확인

빌더 세션의 cwd는 페르소나 디렉토리 자체이다 (예: `data/personas/탐정/`).
이 디렉토리에 **독립 `.git`이 없을 수 있다** — 메인 서비스 리포(`C:/repository/claude bridge/.git`)만 존재하는 상태.

### `.git` 존재 여부 확인
```bash
# 현재 디렉토리에 .git이 있는지 확인
ls -la .git 2>/dev/null || echo "NO_GIT"
```

**`.git`이 없는 경우** (대부분의 첫 퍼블리시):
```bash
git init
git config user.name "Claude Play"
git config user.email "bridge@local"
```

**`.git`이 있는 경우**: 이미 독립 리포가 있으므로 그대로 진행. 단, author 설정 확인:
```bash
git config user.name "Claude Play"
git config user.email "bridge@local"
```

**주의**: `git status`를 실행했을 때 상위 메인 리포의 파일(`../../../server.ts` 등)이 보이면 독립 `.git`이 없다는 뜻이다. 반드시 `git init`부터 실행할 것.

## 절차

### 1. persona.json 확인/생성
- `persona.json`이 없으면 생성:
  ```json
  {
    "displayName": "(persona.md 첫 줄에서 추출)",
    "description": "(사용자에게 물어보거나 persona.md에서 요약)",
    "tags": [],
    "version": "1.0.0",
    "author": "(사용자 GitHub 유저명)"
  }
  ```
- 이미 있으면 version 업데이트 여부를 사용자에게 확인

### 2. .gitignore 확인
다음 파일들이 `.gitignore`에 포함되어 있는지 확인. 없으면 추가:
- `chat-history.json`
- `memory.md`
- `builder-session.json`
- `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`
- `.claude/`, `.agents/`, `.gemini/`, `.codex/`

### 3. 이미 tracked된 민감 파일 제거
```bash
git rm --cached chat-history.json memory.md builder-session.json 2>/dev/null || true
```

### 4. GitHub 리포 생성 및 Push

#### 리포 이름 규칙
리포 이름은 `claudeplay-` 프리픽스를 붙이도록 가이드한다.
- 리포 이름은 영문으로 작성 (GitHub 리포명 규칙)
- 예: `claudeplay-detective`, `claudeplay-fantasy-knight`, `claudeplay-cafe-owner`
- 페르소나 폴더명이 한글이면 영문으로 번역해서 제안
- 사용자가 다른 이름을 원하면 존중하되, 기본 제안은 항상 `claudeplay-`로 시작

#### GitHub MCP 또는 GitHub CLI(`gh`)가 있는 경우:
1. 리포 생성 (기본 이름: `claudeplay-<영문명>`)
2. `git remote add origin <url>`
3. `git add -A && git commit -m "Publish persona"`
4. `git push -u origin master` (또는 현재 브랜치)

#### GitHub MCP / CLI 모두 없는 경우:
1. 사용자에게 GitHub에서 빈 리포를 직접 만들라고 안내 (이름 제안: `claudeplay-<영문명>`)
2. URL을 받아서 `git remote add origin <url>`
3. `git add -A && git commit -m "Publish persona"`
4. `git push -u origin master`

### 5. 이후 업데이트 Push
이미 remote가 설정된 경우:
```bash
git add -A
git commit -m "Update persona"
git push
```
