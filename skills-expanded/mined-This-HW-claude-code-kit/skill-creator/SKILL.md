---
name: skill-creator
description: Create new Claude Code skills. Applies standard templates and best practices to scaffold a skill file automatically.
model: sonnet
effort: medium
---

# Skill Creator

> Claude Code 스킬을 빠르고 정확하게 생성

베스트 프랙티스를 적용한 스킬을 자동 생성합니다.

---

## 사용법

### 신규 스킬 생성

```
/skill-creator "데이터 분석" data-analysis
/skill-creator "API 모니터링" api-monitor
/skill-creator "보안 검사" security-audit
```

---

## 생성 워크플로우

### 1. 요구사항 수집

다음 정보를 확인합니다:

- 스킬 이름 (kebab-case)
- 스킬 설명
- 사용 시점 (when to use)
- 필요한 도구
- 모델 (opus/sonnet/haiku)

### 2. Frontmatter 생성

```yaml
---
name: skill-name
description: What it does + when to use
model: sonnet | opus | haiku
effort: low | medium | high | max
---
```

### 3. 본문 작성

**구조:**

1. 개요
2. 사용법
3. 워크플로우
4. 예시
5. 관련 도구

---

## 스킬 위치

`plugins/{domain}/skills/{name}/SKILL.md` 경로에 파일을 생성한다.
**manifest(`plugin.json`)에는 skill 레지스트리가 없다** — 디렉토리에서 자동 발견되므로
등록 단계가 없다.

---

## 스킬 템플릿

### 기본 템플릿

```markdown
---
name: skill-name
description: Brief description. Use when [scenario].
model: sonnet
effort: medium
---

# Skill Title

> One-line tagline

Brief overview of what this skill does.

---

## 사용법

/skill-name [arguments]
/skill-name "specific task"

---

## 워크플로우

### 1. Step One

Description...

### 2. Step Two

Description...

---

## 예시

/skill-name example-input

**Result:** Description of result

---

## 관련 도구

- **related-agent**: Description
```

### Task 에이전트 호출 템플릿

```markdown
---
name: skill-name
description: Orchestrates agents for [purpose].
model: sonnet
effort: high
---

# Skill Title

## 워크플로우

Task tool 사용:
subagent_type: [agent-name]
model: [model]
prompt: |
[프롬프트 내용]
```

---

## 모델 선택 가이드

| 작업 유형           | 권장 모델 | 이유             |
| ------------------- | --------- | ---------------- |
| 전략/분석/리뷰      | `opus`    | 복잡한 추론 필요 |
| 코드 구현/수정      | `sonnet`  | 균형잡힌 성능    |
| 탐색/검증/빠른 작업 | `haiku`   | 빠른 실행        |

---

## effort 선택 가이드

| effort   | 사용 시점                |
| -------- | ------------------------ |
| `low`    | Bash/MCP 단순 실행       |
| `medium` | 단일 에이전트 호출       |
| `high`   | 복수 에이전트 파이프라인 |
| `max`    | 전체 라운드 협업 (30분+) |

---

## 베스트 프랙티스

### $ARGUMENTS 활용

```markdown
에러 정보: $ARGUMENTS
대상: $ARGUMENTS (없으면 전체)
```

### 검증 체크리스트

스킬 생성 후 확인:

- [ ] Frontmatter 완전함 (name, description, model, effort)
- [ ] 설명이 명확함 (what + when to use)
- [ ] 사용법 예시 포함
- [ ] 워크플로우 단계별 설명
- [ ] `plugins/{domain}/skills/{name}/SKILL.md` 경로 준수
