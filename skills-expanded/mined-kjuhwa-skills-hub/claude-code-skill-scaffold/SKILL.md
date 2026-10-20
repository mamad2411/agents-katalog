---
tags: [devops, claude, code, skill, scaffold]
name: claude-code-skill-scaffold
description: "[Tooling] Claude Code 스킬 표준 구조(SKILL.md + prompts/ + scripts/ + references/)를 자동 생성하는 스캐폴딩."
argument-hint: <skill-name>
version: 1.0.0
source_project: nkia-skills
category: devops
---

# claude-code-skill-scaffold

Claude Code 플러그인/로컬 스킬의 **표준 디렉토리 구조와 SKILL.md 보일러플레이트**를 한 번에 생성합니다.

## Usage

```bash
/claude-code-skill-scaffold my-new-skill
```

## Description

호스트 프로젝트의 `.claude/skills/{skill-name}/`에 표준 구조를 생성합니다.
Claude Code 플러그인이든 프로젝트 로컬 스킬이든 동일한 구조를 쓸 수 있습니다.

## Instructions

### Step 1: 입력 검증
1. `<skill-name>` 파싱. 비어있으면 사용법 출력 후 중단.
2. `.claude/skills/{skill-name}/` 존재 시 중복 에러 출력 후 중단.

### Step 2: 디렉토리 구조 생성
```
.claude/skills/{skill-name}/
├── SKILL.md
├── prompts/.gitkeep
├── scripts/.gitkeep
└── references/.gitkeep
```

### Step 3: SKILL.md 템플릿 작성
frontmatter 필수 필드: `name`, `description`, `argument-hint`.
body 필수 섹션: `## Usage`, `## Description`, `## Instructions`.

### Step 4: 완료 안내
생성 경로와 다음 단계(`skill-validate` → `skill-publish`)를 안내.

## Notes
- 스킬 이름은 kebab-case 권장.
- 검증 스킬(`skill-md-validator`)과 함께 쓰면 publish 전 품질이 보장됨.
