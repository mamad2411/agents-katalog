---
name: work-plan
description: |
  req.md 요구사항 파일을 분석하여 WORK-SPEC.html 작업 명세서를 생성한다. Gemini/Codex 크로스 체크로 계획의 품질을 검증한다.
  "/work-plan", "작업 계획", "구현 계획 세우기", "작업 명세서", "WORK-SPEC 생성", "req.md 분석", "작업 분석", "요구사항 분석해줘", "작업 계획 세워줘", "스펙 정리", "설계해줘" 요청에 트리거된다.
  생성된 WORK-SPEC.html는 `/work-plan-start` 스킬의 입력으로 사용된다.
  req.md가 없어도 사용자가 구두로 요구사항을 설명하면 그것을 기반으로 WORK-SPEC.html를 생성할 수 있다.
---

# Work Plan Skill

req.md를 분석하여 WORK-SPEC.html 작업 명세서를 생성한다.
구현 전에 "무엇을, 어떤 순서로, 어떤 규칙으로" 만들지 확정하기 위함이다.

> ## AI 크로스 체크: `gemini-check` / `codex-check` 하네스로 위임
>
> Gemini/Codex CLI 호출은 더 이상 이 스킬에서 직접 작성하지 않고 두 하네스에 위임한다.
> 호출 정책(timeout 240s, 에러 분류, 1회 재시도, 호출 로그 저장)이 한 곳에 집중되어 일관성을 확보한다.
>
> **위임 호출 패턴 (요약):**
>
> - **Gemini:** `Agent(subagent_type="general-purpose", prompt="당신은 gemini-reviewer 에이전트다. ~/.claude/agents/gemini-reviewer.md를 먼저 읽고 gemini-check 스킬을 실행하라. purpose=work-plan-cross-check, log_dir={Track _workspace/ai-cross-check/gemini/}, prompt_text=<...본문...>", model="opus")`
> - **Codex:** `Agent(subagent_type="general-purpose", prompt="당신은 codex-reviewer 에이전트다. ~/.claude/agents/codex-reviewer.md를 먼저 읽고 codex-check 스킬을 실행하라. mode=exec, purpose=work-plan-cross-check, log_dir={...codex/}, prompt_text=<...>", model="opus")`
>
> 두 호출은 독립적이므로 병렬 실행 가능. 반환 JSON의 `status` 필드로 분기하여 `response`를 사용한다.
> Codex Plugin Skill(`/codex:rescue` 등)은 사용하지 않는다 — codex-check 하네스가 CLAUDE.md 정책을 강제한다.
>
> 본 스킬의 아래 직접 호출 섹션(`where gemini`, `codex exec -` 등)은 호환성을 위해 남아 있으나, 신규 실행은 위 위임 패턴을 사용한다.

## 왜 이 스킬인가?

- **구현 전 설계 확정**: 코드를 쓰기 전에 파일 목록, API, 데이터 모델, Phase를 확정하여 임의 변경을 방지
- **크로스 체크 내장**: Gemini/Codex가 요구사항 누락, 오버엔지니어링, 기술 타당성을 검증
- **팀 워크플로우 연계**: 생성된 WORK-SPEC.html가 `/work-plan-start`의 입력이 되어 에이전트 병렬 디스패치 가능

---

## 실행 방법

```
/work-plan                          # 프로젝트 루트의 req.md 사용
/work-plan path/to/req.md           # 지정 경로의 req.md 사용
/work-plan --cross-check            # Light 모드여도 크로스 체크 강제 실행
/work-plan --no-cross-check         # Full 모드여도 크로스 체크 스킵
/work-plan --design-review          # 설계 리뷰(design-reviewer 에이전트) 활성화
/work-plan path/to/req.md --cross-check  # 경로 + 크로스 체크 강제
```

**플래그:**

| 플래그 | 효과 |
|--------|------|
| `--cross-check` | 복잡도와 무관하게 크로스 체크(Step 4) 강제 실행 |
| `--no-cross-check` | 복잡도와 무관하게 크로스 체크(Step 4) 스킵 |
| `--design-review` | design-reviewer 에이전트(Step 3.7) 활성화 (기본: 스킵) |
| 없음 | 복잡도 게이트 판단에 따름 (Light=스킵, Full=실행) |

---

## 작업 절차

### 1. req.md 읽기

`$ARGUMENTS`가 있으면 해당 경로, 없으면 프로젝트 루트의 `req.md`를 읽는다.

```
경로 우선순위:
1. $ARGUMENTS로 전달된 경로
2. 현재 프로젝트 루트의 req.md
3. 없으면 사용자에게 경로 질문
```

req.md 형식은 자유다. 자연어, 목록, 표 등 어떤 형식이든 분석한다.

### 1.1. Track 설정

req.md를 읽은 직후, 이번 작업의 문서를 저장할 Track 디렉토리를 설정한다.
모든 작업 문서는 `.claude/tracks/{track_id}/` 하위에 생성되어 태스크별로 관리된다.

**절차:**

1. **Jira 번호 추출**: 현재 git branch에서 Jira 번호를 추출한다.
   ```bash
   git branch --show-current 2>/dev/null | grep -oP '^[A-Z]+-\d+' || echo "NO_JIRA"
   ```
   - 추출 실패 시 사용자에게 Jira 번호를 질문하거나, 임의 Track ID를 사용한다.

2. **기존 Track 확인**: `.claude/tracks/` 하위에 해당 Jira 번호로 시작하는 디렉토리를 확인한다.
   ```bash
   ls -d .claude/tracks/{JIRA번호}*/ 2>/dev/null || echo "NO_EXISTING_TRACKS"
   ```

3. **sub-task title 결정**: 같은 Jira 번호의 Track이 이미 존재하면, 사용자에게 sub-task title을 질문한다.
   - AskUserQuestion 도구로 질문: "이번 작업의 Track 이름을 지정해주세요."
   - 옵션: req.md 내용 기반 추천 title 2~3개 + 직접 입력
   - 예시: `shipment-log-sync`, `shipment-status`, `log-migration` 등

4. **Track 디렉토리 생성**:
   - 경로: `.claude/tracks/{JIRA번호}-{sub-task-title}/`
   - 디렉토리가 이미 존재하면 재사용 (사용자 확인 후)

5. **metadata.json 생성**:
   ```json
   {
     "track_id": "{JIRA번호}-{sub-task-title}",
     "description": "{req.md 핵심 목표 1줄}",
     "type": "feature",
     "has_ui": {true/false},
     "status": "in_progress",
     "created_at": "{오늘 날짜}",
     "work_spec_path": "2_WORK-SPEC.html",
     "branch": "{현재 git branch}",
     "parent_track": "{JIRA번호}",
     "total_phases": 0,
     "current_phase": 0
   }
   ```

6. **DOC_DIR 설정**: 이후 모든 문서 생성 시 `{DOC_DIR}` = `.claude/tracks/{track_id}/`를 사용한다.

7. **tracks/index.md 업데이트**: Active 섹션에 새 Track 항목을 추가한다.
   ```markdown
   - [ ] [{description}](./{track_id}/) - {오늘 날짜} 생성
   ```

**Track 이름 규칙:**
- Jira 번호가 있으면: `{JIRA}-{sub-task-title}` (예: `TECH-22386-shipment-log-sync`)
- Jira 번호가 없으면: `{사용자-입력-title}` 또는 `{branch-name}`
- 기존 Track과 동일 이름 불가 (suffix 자동 추가: `-2`, `-3` 등)

**모드 선택 후 안내:**
```
Track 설정: {track_id}
경로: .claude/tracks/{track_id}/
```

### 1.5. 복잡도 판단 (Light / Full 분기)

req.md를 읽은 직후, 요구사항의 복잡도를 판단하여 **Light 모드** 또는 **Full 모드**를 선택한다.
단순 요구사항에 풀 파이프라인을 돌리면 토큰과 시간이 낭비되므로, 복잡도에 맞는 경량 경로를 제공한다.

**판단 기준:**

| 항목 | Light | Full |
|------|-------|------|
| 신규/수정 파일 수 | 1~2개 | 3개+ |
| 요구사항 항목 수 | 1~3개 | 4개+ |
| API/DB/외부 연동 언급 | 없음 | 있음 |
| "간단", "하나만", "테스트", "확인" 등 키워드 | 있으면 Light 가중 | - |
| 멀티 모듈/서비스 간 연동 | 없음 | 있음 |

**모드별 실행 단계:**

| 모드 | 실행 | 스킵 |
|------|------|------|
| **Light** | 1 → 1.1 → 1.5 → 3(축약) → 5(결과 보고) | 2(프로젝트 분석), 3.5(FEATURE-CHECKLIST), 4(크로스 체크) |
| **Light + `--cross-check`** | 1 → 1.1 → 1.5 → 3(축약) → 4(크로스 체크) → 5 | 2, 3.5 |
| **Full** | 1 → 1.1 → 1.5 → 2 → 3 → 3.5 → 4 → 5 | 없음 |
| **Full + `--no-cross-check`** | 1 → 1.1 → 1.5 → 2 → 3 → 3.5 → 5 | 4(크로스 체크) |

**플래그 오버라이드:** `--cross-check` / `--no-cross-check` 플래그는 복잡도 게이트의 크로스 체크 판단을 덮어쓴다. 다른 단계(프로젝트 분석, FEATURE-CHECKLIST)에는 영향 없음.

**Light 모드 WORK-SPEC:**
- 섹션 1(요구사항 요약), 3(파일 변경 목록), 9(작업 단계)만 포함
- 크로스 체크 결과 섹션 생략
- FEATURE-CHECKLIST.html 생략

**모드 선택 후 안내:**
```
복잡도 판단: {Light / Full} 모드
사유: {판단 근거 1줄}
```

### 2. 프로젝트 컨텍스트 분석

req.md를 읽은 후 프로젝트 유형을 자동 판별한다. 기존 코드의 패턴과 스타일을 파악해야 새 코드가 이질적이지 않다.

**판별 기준:**

| 유형 | 판별 조건 |
|------|----------|
| Spring Boot API | `build.gradle`/`pom.xml` + `spring-boot-starter-web` |
| Spring Batch | `spring-boot-starter-batch` |
| TIL 문서 | `cs/` 디렉토리 존재, 마크다운 중심 |
| 알고리즘 | `algorithm/` 디렉토리, 문제 풀이 패턴 |
| 라이브러리/모듈 | 독립 모듈 구조 |
| 프론트엔드 | `package.json` + React/Vue 등 |

**분석 항목:**

1. **기술 스택** - build.gradle / pom.xml / package.json 분석
2. **프로젝트 구조** - 패키지/디렉토리 구조 파악
3. **기존 코드 패턴** - 네이밍 규칙, 아키텍처 패턴, 예외 처리 방식
4. **CLAUDE.md 규칙** - 프로젝트/글로벌 CLAUDE.md에서 코딩 규칙 추출
5. **기존 테스트 패턴** - 테스트 프레임워크, 네이밍, 구조
6. **DB 스키마 탐색** (Spring Boot API / Spring Batch 유형만)

#### 2-6. DB 스키마 탐색

프로젝트 유형이 **Spring Boot API** 또는 **Spring Batch**인 경우, DB 테이블/인덱스 구조를 직접 조회하여 데이터 모델 설계에 반영한다.

**Read 도구로 `references/db-schema-guide.md`를 읽어서 mysqlsh 사용법과 쿼리 템플릿을 참조한다.**

**절차:**

1. **접속 정보 추출**: `application.yml`, `application-local.yml`, `application.properties` 중 하나에서 `spring.datasource.*` 키를 찾는다.
2. **접속 가능 여부 확인**: mysqlsh 설치 여부와 DB 접속 가능 여부를 확인한다.
   ```bash
   where mysqlsh  # 설치 확인
   mysqlsh --sql -u {user} -p{password} -h {host} -P {port} -D {database} -e "SELECT 1;"  # 접속 확인
   ```
3. **스키마 조회**: 접속 가능하면 아래 순서로 조회한다.
   - `SHOW TABLES;` - 전체 테이블 목록
   - `DESCRIBE {table};` - req.md에서 언급된 테이블의 구조
   - `SHOW INDEX FROM {table};` - 관련 테이블의 인덱스
   - 외래키 관계 (INFORMATION_SCHEMA.KEY_COLUMN_USAGE)
4. **결과 활용**: 조회된 스키마 정보를 WORK-SPEC.html의 "데이터 모델" 섹션에 반영한다.

**예외 처리:**
- mysqlsh 미설치 → "mysqlsh 미설치로 DB 스키마 조회를 건너뜁니다" 안내 후 계속
- 접속 정보 없음 → 사용자에게 DB 접속 정보를 질문 (host, port, database, user, password)
- 접속 실패 → "DB 접속 실패로 스키마 조회를 건너뜁니다" 안내 후 계속
- **보안**: `block-dangerous-sql.sh` hook이 읽기 전용 쿼리만 허용한다. DML/DDL은 자동 차단된다.

### 3. WORK-SPEC.html 초안 생성

**Read 도구로 `references/workspec-template.md`를 읽어서 템플릿과 섹션 선택 규칙을 참조한다.**

`{DOC_DIR}/*_WORK-SPEC.html` (예: `2_WORK-SPEC.html`)에 생성한다. 번호는 글로벌 CLAUDE.md의 문서 번호 체계를 따른다.

**핵심 원칙:**
- 해당 없는 섹션은 제거한다. 빈 템플릿을 남기지 않는다.
- 새 코드는 기존 프로젝트의 패턴과 스타일을 따른다.

### 3.5. 기능 체크리스트 생성

WORK-SPEC.html의 "기능 요구사항" 섹션을 기반으로 **사용자/QA 관점의 기능 동작 확인 목록**을 `{DOC_DIR}/*_FEATURE-CHECKLIST.html`에 생성한다.

**목적:** 개발 완료 후 "이 기능이 동작하는가?"를 브라우저에서 하나씩 확인할 수 있는 체크리스트. 개발 코드 체크리스트(`*_PLAN.md`)와는 별개.

**생성 규칙:**
- WORK-SPEC.html의 기능 요구사항을 **사용자 행동 기준**으로 변환 ("~하면 ~한다", "~가 표시된다")
- 카테고리별 그룹화 (WORK-SPEC의 섹션 구조 유지)
- 모든 항목은 `- [ ]` 체크박스 형식
- 기술 구현 세부사항은 제외 (SQL, 클래스명 등)
- UI가 있는 프로젝트(`has_ui: true`)는 Step별 동작 확인 항목 포함

**문서 헤더:**
```markdown
# 기능 체크리스트

> 이 문서는 {기능명}의 사용자/QA 관점 기능 동작 확인 목록입니다.
> 개발 코드 진행률은 [*_PLAN.md](*_PLAN.md), 요구사항 원본은 [*_WORK-SPEC.html](*_WORK-SPEC.html) 참조.
>
> Track ID: {track_id}
```

생성 후 `0_INDEX.html`에 항목을 추가한다.

### 3.7. 설계 리뷰 (Full 모드 + `--design-review` 플래그 시에만)

> **기본 스킵**: 비용 절감을 위해 기본적으로 실행하지 않는다.
> `/work-plan --design-review` 플래그를 명시한 경우에만 실행한다.

`--design-review` 플래그가 없으면 이 단계를 건너뛰고 Step 4로 진행한다.

플래그가 있을 때: WORK-SPEC.html 생성 완료 후 design-reviewer 에이전트를 디스패치하여 코드 설계 품질을 검토한다.
설계 결정(디자인 패턴, SQL 성능, Ops)을 컨텍스트 스위칭 1회로 한 번에 커버한다.

Agent 도구 파라미터:
- `subagent_type`: `"design-reviewer"`
- `prompt`: "{WORK-SPEC.html 전체 내용을 포함} 위 WORK-SPEC.html를 코드 설계(SOLID/패턴), SQL 쿼리 성능, Ops(로깅/롤백) 관점으로 리뷰하고 개선안을 제시해줘."

**결과 반영:**

| 심각도 | 처리 방식 |
|--------|----------|
| 🔴 필수 반영 | WORK-SPEC.html에 즉시 반영 |
| ⚠️ 권장 | Claude가 타당성 판단 후 선택적 반영 |
| 💡 참고 | WORK-SPEC.html 하단 "설계 리뷰 결과" 섹션에 기록 |

### 4. 외부 AI 크로스 체크

WORK-SPEC.html 초안 생성 후, Gemini/Codex CLI로 작업 계획을 크로스 체크한다.
단독 검증은 맹점이 생기기 쉬우므로, 다른 AI의 시선으로 누락과 오류를 잡는다.

#### 4-1. 사전 확인

**각 CLI를 개별 Bash 호출로 확인한다.** 병렬 Bash 호출 시 하나의 에러가 나머지를 취소할 수 있으므로, 반드시 별도 호출로 분리하고 `|| echo` 패턴으로 에러를 흡수한다.

```bash
# 개별 Bash 호출 1
where gemini 2>/dev/null && echo "GEMINI_OK" || echo "GEMINI_SKIP"
```

```bash
# 개별 Bash 호출 2: Codex 설치 여부 확인 (Plugin 우선, CLI fallback)
# 1) Plugin 설치 확인
test -f "$HOME/.claude/plugins/cache/openai-codex/codex/1.0.0/scripts/codex-companion.mjs" && echo "CODEX_PLUGIN_OK" || echo "CODEX_PLUGIN_SKIP"
```

```bash
# 개별 Bash 호출 3: Plugin 미설치 시 CLI fallback 확인
where codex 2>/dev/null && echo "CODEX_CLI_OK" || echo "CODEX_CLI_SKIP"
```

**Codex 사용 방식 결정:**
1. `CODEX_PLUGIN_OK` → **Skill 도구**로 `/codex:rescue` 호출 (Bash 사용 금지)
2. `CODEX_PLUGIN_SKIP` + `CODEX_CLI_OK` → CLI fallback (이때만 Bash `codex exec -` 허용)
3. 둘 다 SKIP → "Codex가 설치되지 않아 크로스 체크를 건너뜁니다" 안내

- 미설치 CLI는 해당 크로스 체크를 건너뛴다 (안내 메시지 출력).
- Gemini/Codex 둘 다 미설치면 "외부 크로스 체크 없이 Claude 단독으로 진행합니다" 안내 후 계속.
- **주의**: `where` 명령이 exit code 1을 반환하면 병렬 호출 시 다른 명령까지 취소될 수 있다. 반드시 `|| echo` 패턴 사용.
- **주의**: Codex Plugin이 설치되어 있으면 **절대 Bash로 codex를 호출하지 않는다**. 반드시 Skill 도구를 사용한다.

#### 4-2. 크로스 체크 실행

Gemini와 Codex는 독립적이므로 **병렬 실행**한다. **Gemini는 Bash 도구, Codex는 Skill 도구**로 호출한다.
**절대 Codex를 Bash(`codex exec -`)로 호출하지 않는다. 반드시 Skill 도구를 사용한다.**

> **⚠️ 중요**: Codex 호출 시 Bash 도구가 아닌 **Skill 도구**(`skill: "codex:rescue"`)를 사용한다.
> Gemini와 Codex를 둘 다 Bash로 병렬 실행하는 것은 **금지된 패턴**이다.

**Gemini** (Bash 도구, **timeout: 240000ms (4분) 필수**):

> ⏱️ **Timeout 정책**: 외부 AI 응답이 4분을 초과하면 hung 상태로 간주하고 강제 종료한다. Bash 도구 호출 시 반드시 `timeout: 240000` 명시.

```bash
(cat {req.md 경로} && echo -e "\n---\n" && cat {WORK-SPEC.html 경로}) | gemini -p "다음은 요구사항 문서(req.md)와 이를 기반으로 생성한 작업 명세서(WORK-SPEC.html)입니다.

## 검증 관점
1. **요구사항 커버리지**: req.md의 모든 요구사항이 WORK-SPEC.html에 반영되었는가?
2. **기술적 타당성**: 선택한 기술 접근 방식이 적절한가? 더 나은 대안이 있는가?
3. **누락된 고려사항**: 예외 처리, 엣지 케이스, 보안, 성능 관점에서 빠진 것은?
4. **작업 범위**: 오버엔지니어링이나 언더엔지니어링이 있는가?
5. **작업 순서**: Phase 분리와 작업 순서가 합리적인가?

## 출력 형식
각 관점별로 발견한 이슈를 심각도(필수 반영 / 권장 / 참고)와 함께 정리해줘.
한국어로 답변해줘." 2>&1 || echo "GEMINI_FAIL"
```

**Codex** (Skill 도구 — Bash가 아님!):

Gemini Bash 호출과 **동시에** Skill 도구로 병렬 호출한다:

```
Skill 도구 호출:
  skill: "codex:rescue"
  args: "다음 WORK-SPEC.html를 검증해줘. {WORK-SPEC.html 경로}를 읽고, 요구사항 커버리지, 기술적 타당성, 누락된 고려사항, 작업 범위, 작업 순서 관점에서 이슈를 심각도와 함께 한국어로 정리해줘."
```

> ⚠️ **Codex Plugin Skill 도구는 Bash timeout이 적용되지 않는다**. 다음 watchdog 정책을 따른다:
>
> 1. **호출 후 5분 한도**: Skill 도구 호출 후 메인이 다른 도구 호출(Gemini Bash 등)을 처리하는 동안 5분 카운트.
> 2. **5분 초과 시**: 메인이 응답 받지 못한 상태라면 `/codex:cancel` Skill 호출로 강제 중단.
> 3. **부분 결과 활용**: cancel 후 `/codex:result`로 부분 결과를 가져와 반영(있는 경우).
> 4. **Claude 단독 진행**: 부분 결과도 없으면 "Codex 크로스 체크 timeout — Claude 단독으로 진행" 안내 후 계속.
>
> args에 협력 지시 추가: "**최대 5분 안에 답변 못 하면 그 시점까지의 부분 분석이라도 반환해줘.**"

**실패 시 재시도:**
1. Plugin(Skill) 1차 실패 또는 5분 timeout → Skill 도구로 재호출 (`skill: "codex:rescue"`, args에 "이전 검증을 이어서 5분 내 완료해줘" 추가)
2. Plugin 2차 실패 → CLI fallback (Bash, **timeout: 240000ms**):
   ```bash
   (echo "검증 요청:" && cat {req.md 경로} && echo -e "\n---\n" && cat {WORK-SPEC.html 경로}) | codex exec - 2>&1 || echo "CODEX_FAIL"
   ```
3. CLI도 실패/timeout → 안내 메시지 출력 후 계속 진행

**올바른 병렬 호출 예시:**
```
동시에 2개 도구 호출:
├─ Bash 도구: gemini -p "..." (timeout: 240000ms)
└─ Skill 도구: skill="codex:rescue", args="...최대 5분 안에 답변..."
   └─ 5분 watchdog: 응답 없으면 /codex:cancel → /codex:result
```

**금지된 패턴:**
```
❌ 동시에 2개 Bash 도구 호출:
├─ Bash 도구: gemini -p "..."
└─ Bash 도구: codex exec -    ← 절대 금지
```

#### 4-3. 피드백 반영

| 심각도 | 처리 방식 |
|--------|----------|
| **필수 반영** | WORK-SPEC.html에 즉시 반영 |
| **권장** | Claude가 타당성 판단 후 선택적 반영 |
| **참고** | WORK-SPEC.html 하단 "크로스 체크 결과" 섹션에 기록 |

피드백 반영 후 WORK-SPEC.html를 최종 업데이트하고, 크로스 체크 결과 섹션을 추가한다.
크로스 체크 결과 섹션의 형식은 `references/workspec-template.md`를 참조한다.

### 5. 사용자 확인

WORK-SPEC.html 생성 후 **Plan Mode로 전환**하여 결과를 보고한다.
사용자가 검토/수정 후 `/work-plan-start`로 실행할 수 있다.

---

## 결과 보고 형식

```
## Work Plan 생성 완료

### 분석 결과
- 프로젝트 유형: {유형}
- 기술 스택: {스택 요약}
- 기존 패턴: {패턴 요약}

### 크로스 체크
- Gemini: {완료 / 건너뜀 (사유)}
- Codex: {완료 / 건너뜀 (사유)}
- 필수 반영 항목: {N}개 (모두 반영 완료)
- 권장 반영 항목: {N}개 중 {M}개 반영

### 생성 파일
- WORK-SPEC.html ({파일 위치})
- FEATURE-CHECKLIST.html ({파일 위치})

### 작업 규모
- 신규 파일: {N}개
- 수정 파일: {N}개
- 테스트 파일: {N}개
- 예상 Phase: {N}단계

### 다음 단계
`/work-plan-start` 로 작업을 시작하세요.
WORK-SPEC.html를 수정한 후 시작해도 됩니다.
```

---

## 주의사항

- **WORK-SPEC.html 위치**: req.md와 같은 디렉토리에 생성한다 (기본: 프로젝트 루트).
- **수정 가능**: 사용자가 WORK-SPEC.html를 직접 수정한 후 `/work-plan-start`를 실행할 수 있다.
- **크로스 체크 실패 허용**: 외부 AI 크로스 체크가 실패해도 Claude 단독 생성 WORK-SPEC.html는 유효하다.
