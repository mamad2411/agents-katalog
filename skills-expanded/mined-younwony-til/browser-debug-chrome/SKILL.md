---
name: browser-debug-chrome
disableModelInvocation: true
description: |
  Chrome in Claude 브라우저 자동화로 웹 프로젝트를 점검합니다 (Chrome-only 레거시 버전).
  기본 동작: 현재 브랜치 변경사항 분석 → QA 시나리오 MD 생성 → Plan 모드 실행 → Chrome 자동화 점검.
  서버가 기동되지 않은 상태에서도 자동 탐지하여 서버를 기동한 뒤 점검을 수행합니다.
  콘솔 에러, 인터랙션 동작, DOM 상태, 네트워크 에러를 자동 검사하고 발견된 이슈를 즉시 수정합니다.

  이 스킬은 Chrome MCP만 사용하는 레거시 버전입니다.
  Playwright + Chrome 2-Layer 버전은 `browser-debug` 스킬을 사용하세요.

  다음 키워드/문맥에서 트리거됩니다:
  - "Chrome-only QA", "크롬 전용 QA"
  - `/browser-debug-chrome` 슬래시 커맨드로 호출
---

# Browser Debug & QA - Chrome 자동화 웹 점검 (Chrome-only)

## 개요

QA 시나리오를 기반으로 Chrome 자동화 점검을 수행한다.
FAIL 발견 시 즉시 코드를 수정하고 재검증한다.

반드시 아래 Phase를 순서대로 수행한다. Phase를 건너뛰지 않는다.

---

## Phase 0: QA 시나리오 확인 (기존 시나리오 체크)

**다음 순서로 `QA-SCENARIOS.html` 파일을 탐색한다:**

1. `.claude/tracks/`에서 status가 `in_progress`인 활성 Track의 `.claude/tracks/{track_id}/QA-SCENARIOS.html`
2. `.claude/docs/QA-SCENARIOS.html`
3. 프로젝트 루트 `QA-SCENARIOS.html` (하위 호환)

### 기존 시나리오가 있는 경우 (QA-SCENARIOS.html 존재)

1. `QA-SCENARIOS.html`를 읽어 내용을 확인한다
2. 시나리오가 유효한지 검증:
   - 시나리오에 명시된 **테스트 URL**이 현재 프로젝트와 일치하는가
   - **변경 파일**과 현재 git 변경사항이 대체로 일치하는가 (완전 일치 불필요)
   - 시나리오에 **P0 시나리오가 1개 이상** 있는가
3. 유효하면 → **Phase 1로 직행**
4. 유효하지 않으면 (오래된 시나리오, 다른 브랜치의 시나리오 등) → 시나리오 재생성

### 기존 시나리오가 없는 경우

1. `qa-scenario` 스킬을 **Skill 도구로 호출**하여 QA 시나리오를 생성한다
   → `Skill("qa-scenario")`
2. `qa-scenario` 스킬이 Plan 모드에서 분석 → 사용자 승인 → `QA-SCENARIOS.html` 생성을 완료한다
3. 생성 완료 후 Phase 1로 진행한다

**핵심 원칙:** QA 시나리오 생성은 `qa-scenario` 스킬의 책임이다. `browser-debug-chrome`은 시나리오 **실행**에 집중한다.

---

## Phase 1: 서버 및 브라우저 준비

### 서버 확인

1. `curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}` 로 서버 상태 확인
2. 서버 미기동 시 → **빌드 → java -jar 기동** 방식으로 자동 시작 (`references/server-detection.md` 참조)
3. 포트 충돌 시 → 대체 포트로 자동 전환하여 기동 (설정 파일 수정 없이 `--server.port` 인자 사용)
4. Health check로 서버 ready 확인 (최대 60초 대기)

### Java 프로젝트 빌드 & 기동 절차

```
1. 빌드 도구 탐지: build.gradle → Gradle / pom.xml → Maven
2. WAR 패키징 여부 확인: build.gradle의 'war' 플러그인 / pom.xml의 <packaging>war</packaging>
3. 빌드 실행:
   - Gradle JAR: gradlew.bat bootJar (Windows) / ./gradlew bootJar
   - Gradle WAR: gradlew.bat bootWar (Windows) / ./gradlew bootWar
   - Maven: mvnw.cmd package -DskipTests (Windows) / ./mvnw package -DskipTests
4. 산출물 탐지:
   - Gradle: build/libs/*.jar 또는 *.war (-plain 제외, 가장 큰 파일 선택)
   - Maven: target/*.jar 또는 *.war (.original 제외, 가장 큰 파일 선택)
5. 포트 결정: 28080부터 체크 (28080 → 28081 → 28082 → 28083 → 28090). 8080은 사용자 자체 테스트용으로 사용 금지.
6. 기동: java -Djasypt.encryptor.password={jasypt_key} -Dspring.profiles.active={profile} -jar {artifact} --server.port={port}
7. Health check 폴링 (3초 간격, 최대 20회)
```

### 포트 충돌 자동 해결

서버 기동 전 반드시 포트 점유 여부를 확인한다:
```bash
# Windows
netstat -ano | findstr :{port} | findstr LISTENING
```

충돌 시 **설정 파일을 수정하지 않고** 커맨드 라인 인자로 포트를 오버라이드한다:
- Spring Boot: `java -jar {artifact} --server.port={alt_port}`
- 기본 포트: 28080 (8080은 사용자 자체 테스트용이므로 사용 금지)
- 대체 포트: 28080 → 28081 → 28082 → 28083 → 28090

대체 포트로 기동한 경우 **QA 시나리오의 테스트 URL도 해당 포트로 자동 조정**한다.

### 서버 재기동이 필요한 경우

다음 파일이 변경된 경우 서버 재기동이 필요하다:
- `tiles*.xml` (Tiles 정의)
- `application*.yml` / `application*.properties` (설정)
- Java 소스 파일 (Controller, Service, Entity 등)
- `build.gradle` / `pom.xml`

서버 재기동이 필요하면 **사용자에게 묻지 않고 Bash로 자체 재기동**한다:
1. 기존 서버 프로세스 종료 (PID 기반)
2. 코드 변경이 있으면 재빌드 (bootJar/bootWar/package)
3. 동일 포트로 `java -jar` 재기동
4. Health check 통과 후 QA 재개

### 브라우저 준비

1. Chrome 도구를 `ToolSearch`로 사전 로드
   → `"select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__read_console_messages,mcp__claude-in-chrome__read_network_requests,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__gif_creator,mcp__claude-in-chrome__form_input,mcp__claude-in-chrome__find"`
2. `tabs_context_mcp`로 현재 탭 상태 확인, 새 탭 생성
3. `read_console_messages` + `read_network_requests` 한 번 호출하여 **트래킹 활성화**
4. 로그인 페이지로 이동 → 자동 로그인 (CLAUDE.md의 로그인 정보 사용)

---

## Phase 2: QA 시나리오 순차 실행

`QA-SCENARIOS.html`의 시나리오를 **P0 → P1 → P2 순서대로** 실행한다.

### 각 시나리오 실행 절차

1. **QA-SCENARIOS.html 업데이트**: 해당 시나리오 결과를 ⬜ → 🔄 실행중으로 변경
2. **사전 준비**: 필요한 페이지 이동, 데이터 준비
3. **액션 수행**: 사용자 액션을 Chrome 자동화로 실행
4. **검증 수행**:
   - `screenshot` → 화면 캡처 후 시각적 확인
   - `javascript_tool` → DOM 상태, 변수 값, 그리드 데이터 확인
   - `read_network_requests` → API 호출 URL, 상태코드, 응답 확인
   - `read_console_messages` → JS 에러, 경고 확인
5. **결과 판정 및 MD 업데이트**:
   - PASS → ✅ PASS
   - FAIL → ❌ FAIL (원인 기록)
   - BLOCKED → ⚠️ BLOCKED (사유 기록)
6. `QA-SCENARIOS.html`의 해당 시나리오 결과를 즉시 업데이트

### FAIL 시 즉시 수정

- FAIL 발견 시 **원인 분석 → 코드 수정 → 재검증**을 즉시 수행
- 수정 후 해당 시나리오를 재실행하여 PASS 확인
- JS/CSS 수정은 브라우저 하드 리프레시(Ctrl+Shift+R)로 즉시 반영
- Java/설정 수정은 서버 재기동 후 재검증
- 수정 내용을 `QA-SCENARIOS.html`의 "발견된 버그" 테이블에 기록
- 결과를 🔧 FIX→PASS로 업데이트

### P0 FAIL 시 중단 정책

- P0 시나리오가 FAIL이면 후속 시나리오 실행을 중단하고 수정에 집중
- P1/P2 FAIL은 기록 후 다음 시나리오 계속 진행

---

## Phase 3: Track 연동 및 결과 보고

### Track 연동

`.claude/tracks/` 디렉토리에서 status가 `in_progress`인 활성 Track을 탐색한다.

활성 Track이 있는 경우:
1. Track의 `plan.md`에서 "브라우저 QA" Phase를 찾는다
2. "브라우저 QA 실행" Task를 `[x]`로 마킹한다
3. **Checkpoint**에 QA 결과 요약을 기록한다:
   ```
   [x] **Checkpoint**: QA 검증 완료
     - 전체: {N}건, PASS: {N}, FIX→PASS: {N}, FAIL: {N}, BLOCKED: {N}
     - QA 문서: QA-SCENARIOS.html
   ```
4. 모든 QA Task가 완료되면 `metadata.json`의 `status`를 `completed`로 변경한다
5. `.claude/tracks/index.md`에서 `[~]` → `[x]`로 변경, Active → Completed로 이동한다

활성 Track이 없는 경우: Track 연동 없이 진행한다.

### 결과 보고

모든 시나리오 실행 후:

1. `QA-SCENARIOS.html`의 모든 시나리오 결과가 업데이트되었는지 확인
2. 미검증 항목이 있으면 사유와 함께 기록
3. QA 과정에서 수정한 파일을 `git add` (commit은 하지 않음)
4. 사용자에게 최종 결과 요약:
   - 전체 시나리오 수 / PASS / FAIL / FIX / BLOCKED 카운트
   - 발견 및 수정한 버그 요약
   - 수정된 파일 목록
5. Track 연동된 경우: Track 완료 상태를 함께 표시

---

## 주의사항

- **모든 ToolSearch는 사전 실행**: Chrome 도구 사용 전 반드시 `ToolSearch`로 로드
- **Console/Network 트래킹 선 활성화**: 페이지 로드 전에 한 번 호출하여 트래킹 시작
- **서버 재기동 자체 처리**: 사용자에게 재기동 요청하지 않고 Bash로 직접 처리
- **QA-SCENARIOS.html 실시간 업데이트**: 각 시나리오 실행 즉시 결과 반영
- **QA-SCENARIOS.html는 git add 대상 제외**: QA 문서는 로컬 참조용
- JavaScript `alert()`, `confirm()`, `prompt()` 등 모달 다이얼로그를 트리거하지 않는다
- 페이지 내 삭제/수정 등 실제 데이터에 영향을 주는 동작은 사용자 확인 후 진행
- 브라우저 확장 프로그램이 응답하지 않으면 2~3회 재시도 후 사용자에게 안내
- 로그인이 필요한 페이지는 사용자에게 로그인 완료를 요청한 후 진행

## 관련 스킬

- `browser-debug`: Playwright + Chrome 2-Layer 버전 (권장)
- `qa-scenario`: QA 시나리오 문서 생성 (Phase 0에서 자동 호출)
