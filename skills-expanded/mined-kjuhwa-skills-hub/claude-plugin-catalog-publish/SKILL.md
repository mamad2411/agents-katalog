---
tags: [devops, claude, plugin, catalog, publish]
name: claude-plugin-catalog-publish
description: "[Tooling] 로컬 스킬을 원격 Git repo에 배포하고 AGENTS.md 카탈로그를 자동 갱신하는 publish 플로우."
argument-hint: <skill-name>
version: 1.0.0
source_project: nkia-skills
category: devops
---

# claude-plugin-catalog-publish

로컬 `.claude/skills/{skill-name}/`을 **원격 Claude Code 스킬 저장소**에 복사·커밋·push하고, 저장소 루트의 `AGENTS.md` 카탈로그를 자동으로 갱신합니다.

## Usage

```bash
/claude-plugin-catalog-publish my-skill
```

## Description

검증 게이트(`skill-md-validator`) 통과 후에만 진행합니다. `mktemp → git clone --depth 1 → 복사 → AGENTS.md 갱신 → commit → push → 정리`의 임시 디렉토리 패턴을 씁니다.

## Instructions

### Step 1: 입력 + 레지스트리 설정 읽기
- `<skill-name>` 파싱, 로컬 경로 존재 확인.
- `.claude/skill-registry.yaml`에서 `registry.remote_url`, `registry.branch` 읽기. 없으면 에러.

### Step 2: 사전 검증 (품질 게이트)
`skill-md-validator`와 동일한 규칙으로 검증. FAIL이면 중단.

### Step 3: Shallow clone + 복사
```bash
tmp_dir=$(mktemp -d)
git clone --depth 1 --branch {branch} {remote_url} "$tmp_dir"
mkdir -p "$tmp_dir/skills/{skill-name}"
cp -r .claude/skills/{skill-name}/* "$tmp_dir/skills/{skill-name}/"
```

### Step 4: 기존 스킬 덮어쓰기 확인
clone 시점에 이미 존재하면 사용자에게 확인.

### Step 5: AGENTS.md 카탈로그 갱신
| 컬럼 | 값 |
|------|-----|
| 스킬 이름 | `{skill-name}` |
| 설명 | frontmatter `description` |
| 배포일 | 오늘 |
| 배포자 | `git config user.name` |

같은 이름 행이 있으면 **갱신**(중복 추가 금지).

### Step 6: commit + push
```bash
git add skills/{skill-name}/ AGENTS.md
git commit -m "publish: {skill-name} by {git-user}"
git push origin {branch}
```

### Step 7: 임시 디렉토리 정리 (`rm -rf "$tmp_dir"`)

## Notes
- 임시 디렉토리는 성공/실패 모두 정리(trap 권장).
- 원격 인증은 SSH key 또는 HTTPS token 선확인.
- 검증-실패-시 절대 push 금지.
