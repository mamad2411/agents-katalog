---
tags: [devops, skill, validator]
name: skill-md-validator
description: "[Tooling] SKILL.md frontmatter + 필수 섹션을 CRITICAL/WARNING 등급으로 검증하는 품질 게이트."
argument-hint: "[skill-name]"
version: 1.0.0
source_project: nkia-skills
category: devops
---

# skill-md-validator

`SKILL.md`가 표준 구조를 충족하는지 frontmatter와 본문을 검사해 **등급별(CRITICAL/WARNING/PASS)** 로 보고합니다. publish 전 품질 게이트로 사용합니다.

## Usage

```bash
/skill-md-validator my-skill     # 단일 검증
/skill-md-validator              # 전체 스킬 순회 검증
```

## Description

`.claude/skills/*/SKILL.md`를 읽어 frontmatter(YAML)와 본문 섹션을 점검합니다. CRITICAL 1건 이상이면 FAIL, WARNING만 있으면 PASS(주의).

## Instructions

### Step 1: 대상 결정
- 인자 있음 → `.claude/skills/{name}/SKILL.md` 한 개.
- 인자 없음 → `.claude/skills/*/SKILL.md` 전체.
- 대상 파일 없음 → 에러.

### Step 2: Frontmatter 검증
| 필드 | 등급 |
|------|------|
| `name` | CRITICAL |
| `description` | CRITICAL |
| `argument-hint` | WARNING |

### Step 3: 본문 섹션 검증 (대소문자 무시, ## 또는 ### 허용)
| 섹션 | 등급 |
|------|------|
| `Usage` 또는 `Instructions` | CRITICAL |
| `Description` 또는 `Purpose` | CRITICAL |
| `Steps`/`Instructions`/`Workflow` 중 하나 | CRITICAL |

### Step 4: 결과 출력
스킬별 상세 + (전체 검증 시) 요약 블록.

### Step 5: 종료 코드
- CRITICAL ≥ 1 → FAIL (publish 차단).
- 그 외 → PASS.

## Notes
- publish 플로우에서 선행 호출 권장.
- 섹션 이름 매칭은 정규식으로 구현하면 오탐/누락이 줄어듬.
