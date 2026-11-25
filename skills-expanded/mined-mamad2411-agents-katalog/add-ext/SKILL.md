---
name: add-ext-skill
description: 확장 스킬 추가 (외부 SKILL.md 동적 로드)
user-invocable: true
type: utility
---

# Add External Skill

[ADD-EXT-SKILL 스킬 활성화]

## 목표

외부 SKILL.md 파일을 `skills/` 디렉토리에 동적으로 추가하여 플러그인 기능을 확장함.

## 활성화 조건

사용자가 `/claude-skills:add-ext-skill` 호출 시 또는 "확장 스킬 추가", "스킬 설치" 키워드 감지 시.

## 워크플로우

### Step 1: SKILL.md 경로 또는 URL 질문

`AskUserQuestion` 도구로 사용자에게 질문:

**질문**: "추가할 SKILL.md 파일의 경로 또는 URL을 입력하세요."

**입력 형식**:
- 로컬 파일 경로: `C:\path\to\SKILL.md` 또는 `/path/to/SKILL.md`
- URL: `https://example.com/path/to/SKILL.md`

### Step 2: 파일 읽기

입력된 경로/URL에서 SKILL.md 파일을 읽음:
- 로컬 경로: `Read` 도구 사용
- URL: `Bash` 도구로 `curl {URL} > /tmp/external-skill.md` 후 Read

### Step 3: frontmatter 검증

읽어온 파일의 YAML frontmatter를 검증:

**필수 필드**:
- `name`: 스킬 ID (kebab-case)
- `description`: 한 줄 설명

**검증 실패 시**: 사용자에게 오류 메시지 출력 후 중단.

```yaml
---
name: my-custom-skill
description: 커스텀 스킬 설명
---
```

### Step 4: skills/{name}/SKILL.md 복사

frontmatter의 `name` 필드를 사용하여 대상 디렉토리 생성 및 파일 복사:

```bash
mkdir -p skills/{name}
# 파일 복사 (Write 도구 사용)
```

### Step 5: commands/{name}.md 자동 생성

진입점 파일 자동 생성:

**파일 경로**: `commands/{name}.md`

**내용 템플릿**:

```markdown
---
description: {frontmatter의 description 값}
---

Use the Skill tool to invoke the `claude-skills:{name}` skill with all arguments passed through.
```

### Step 6: Core 스킬 라우팅 테이블 추가 안내

사용자에게 안내 메시지 출력:

```
확장 스킬 '{name}'이 성공적으로 추가되었습니다.

자동 라우팅을 활성화하려면 `skills/core/SKILL.md`의 라우팅 테이블에 다음 항목을 추가하세요:

| {키워드} | {name} |

예시:
| "my-keyword", "custom" | my-custom-skill |
```

### Step 7: 완료 보고

추가된 스킬 정보 요약:
- 스킬명: `{name}`
- 설명: `{description}`
- 위치: `skills/{name}/SKILL.md`
- 진입점: `commands/{name}.md`
- 슬래시 명령: `/claude-skills:{name}`

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | frontmatter 필수 필드(name, description) 검증 필수 |
| 2 | name 필드가 kebab-case인지 확인 |
| 3 | 기존 스킬명과 중복 시 사용자에게 확인 |
| 4 | commands/{name}.md 자동 생성 필수 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | frontmatter 검증 없이 파일 복사 금지 |
| 2 | 기존 스킬을 덮어쓰지 않음 (중복 시 사용자 확인) |
| 3 | Core 스킬 라우팅 테이블을 자동 수정하지 않음 (안내만) |

## 검증 체크리스트

- [ ] frontmatter에 name, description, user-invocable: true 포함
- [ ] AskUserQuestion 사용하여 경로/URL 입력
- [ ] frontmatter 검증 로직 포함
- [ ] skills/{name}/ 디렉토리 생성 및 파일 복사
- [ ] commands/{name}.md 자동 생성
- [ ] Core 라우팅 테이블 추가 안내
- [ ] MUST 규칙, MUST NOT 규칙 섹션 포함
