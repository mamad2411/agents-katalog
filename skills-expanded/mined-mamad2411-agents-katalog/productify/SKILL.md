---
name: productify
description: >
  명세서(sharpen 결과물)나 아이디어를 받아 제품 형태(Claude Code 스킬/스크립트/
  크롬익스텐션/로컬HTML/CLI/서비스 등)를 결정하고, 페이즈별 로드맵을 설계한다.
  경량화 원칙과 보안 최소화를 적용하여 가장 작은 리소스로 문제를 해결하는
  제품 형태를 찾는다.
  "productify", "제품화", "어떻게 만들지", "로드맵 짜줘", "뭐부터 만들지",
  "MVP 플래닝", "단계별로 나눠줘", "페이즈 나눠줘", "어떤 제품으로 만들지"
  등을 언급하면 이 스킬을 사용한다.
argument-hint: "{명세서 경로 또는 Notion URL 또는 아이디어 텍스트}"
allowed-tools:
  # 명세서 읽기 — 로컬 파일
  - Read
  - Glob
  - Grep
  # 명세서 읽기 — 웹/외부 문서
  - WebFetch
  # 명세서 읽기 — Notion
  - mcp__notion__notion-fetch
  # 명세서 읽기 — Google Drive / Docs / Sheets
  - mcp__claude_ai_Google_Drive__google_drive_search
  - mcp__claude_ai_Google_Drive__google_drive_read_file
  # 결과물 저장 — 로컬
  - Write
  # 결과물 저장 — Notion
  - mcp__notion__notion-create-pages
  # Form Judge 서브에이전트
  - Agent
---

# productify -- 제품화 로드맵 설계

명세서(sharpen 결과물) 또는 아이디어를 받아, 어떤 형태의 제품으로 만들지
결정하고 페이즈별 로드맵을 설계한다.

---

## 핵심 원칙 -- 경량화 우선 (Lightweight-first)

모든 판단에 다음 원칙을 적용한다:

1. **가장 가벼운 형태부터 검토한다**
   - 서비스를 띄우기 전에 기존 플랫폼 확장(Apps Script 등)으로 되는지 본다
   - 크롬 익스텐션 전에 북마클릿이나 유저스크립트로 되는지 본다
   - 별도 도구 전에 이미 쓰는 플랫폼 위에서 해결 가능한지 본다
   - 스크립트 전에 Claude Code 스킬로 되는지 본다
2. **API 키는 쓰지 않는 방향이 기본이다**
   - 키 없이 해결 가능한 방법이 있으면 그것을 우선 추천한다
   - 키가 불가피하면 최소 권한(read-only 등)으로 범위를 좁힌다
   - 키를 쓸 때는 구조화된 요청서를 생성한다
3. **외부 의존성은 적을수록 좋다**
   - 외부 서버, 외부 DB, 외부 인증 각각이 리스크다
   - "이게 꼭 필요한가?"를 항상 한 번 더 묻는다

**제품 형태 선호 순서** (경량 → 무거움):

```text
claude-skill > script > local-html > bookmarklet > userscript
> notion-custom-agent > claude-cowork > platform-extension
> apps-script-webapp > chrome-extension > cli-tool > web-service
```

- **notion-custom-agent**: Notion 팀 자동화 에이전트 (Business 이상).
  한 명 세팅 → 팀 공유. Slack 멘션 트리거, 리포트 자동생성, 태스크 태깅.
  서비스·키 불필요. "Notion + Slack 연동"의 기본 첫 선택지.
- **claude-cowork**: Claude Desktop 반복 자동화 (Pro 이상).
  Slack·Notion·GitHub 스케줄링. 서버·인프라 불필요.
- **apps-script-webapp**: Apps Script 웹앱 배포. 고유 URL, G Suite 인증 그대로.
  Sheets·Drive·Gmail 직접 연결. 내부 폼·대시보드·Sheets UI에 최적.
- **platform-extension**: 이미 쓰는 플랫폼 위 확장 (Apps Script, Slack Workflow,
  Notion Automation, Zapier/Make, n8n). 인증은 플랫폼이 처리.
  **n8n**: 복잡한 로직·셀프호스팅이 필요할 때.

무거운 형태를 추천할 때는 반드시 "왜 더 가벼운 형태로는 안 되는지" 설명한다.

---

## 실행 흐름

### 0. 입력 받기

- **Notion URL** (`notion.so/...` 포함):
  `mcp__notion__notion-fetch`로 내용 로드
- **로컬 .md 파일 경로**: `Read`로 파일 읽기
- **텍스트**: 그대로 사용
- **둘 다 없음**: "제품화할 아이디어나 명세서를 붙여넣어 주세요."

입력에서 핵심 문제와 목표를 추출한다.
Notion URL 여부를 기억해둔다 -- 저장 방식 결정에 사용.

---

### 0.5. 서비스 환경 파악

제품 형태 후보를 필터링하기 위해 팀의 서비스 환경을 먼저 확인한다.

**⚠️ 이 단계는 절대 건너뛰지 않는다.**
사용자 입력에 Notion·Slack·Google 등이 이미 언급되어 있어도 마찬가지다.
플랜·티어·설치 여부를 모르면 올바른 형태 판정이 불가능하다.
Step 0.5 완료 전에 Step 1로 넘어가지 않는다.

```text
시작 전에 팀에서 사용 중인 서비스를 알려주세요.
모르는 항목은 "모름"이라고 하셔도 됩니다.

협업/문서
- Notion: 사용 여부 + 플랜 (Free / Plus / Business / Enterprise)
  (Notion AI · Custom Agent는 Business 이상에서 사용 가능)

AI 도구
- Claude: 사용 여부 + 티어 (Free / Pro / Team / Enterprise)
  (Claude Cowork는 Pro 이상에서 사용 가능)

커뮤니케이션
- Slack: 사용 여부, Workflow Builder 사용 가능 여부

Google
- Google Workspace: 사용 여부
  (Apps Script, Sheets, Drive 접근 가능한지)

자동화 도구 (선택)
- Zapier / Make / n8n 사용 여부
  (n8n은 셀프호스팅 가능 — 사용 중이면 버전/호스팅 방식도 알려주세요)

이미 시도한 도구 (선택)
- 구현을 시도해봤다면 어떤 도구로, 어디서 막혔나요?
  (막힌 지점을 알면 같은 도구 재추천 없이 정확한 대안을 찾을 수 있습니다)

기타 (선택)
- GitHub, Jira, Raycast/Alfred 등
```

**응답 처리 규칙**:

| 상황 | 조치 |
|------|------|
| Notion Business 미만 | notion-custom-agent 후보 제외 |
| Claude Free | claude-cowork 후보 제외 |
| Google Workspace 없음 | apps-script-webapp 후보 제외 |
| Slack 없음 | platform-extension(Slack) 제외 |
| "모름" / 무응답 | 후보에 포함하되 "(확인 필요)" 표시 |
| 이미 시도한 도구 언급 | 해당 도구 재추천 금지. `tried_tools`와 막힌 이유를 Form Judge에 전달 |

- **없다고 명시한 것만 제외한다.** 모름은 포함.
- 파악된 환경을 `available_services`로 기억해두고
  Form Judge 호출 시 컨텍스트에 포함한다.

---

### 1. 제품 형태 결정 라운드

```text
제품화를 시작합니다

"{제목 또는 첫 줄 요약}"

해결하려는 문제: {핵심 1-2줄}
목표: {핵심 1-2줄}

어떤 제품으로 만들지 결정해봅시다.
* 경량화 원칙: 가장 가벼운 형태부터 검토합니다.

---

Round 1

{질문 1-2개}
```

라운드당 **최대 2개** 질문. 아래 축 중 가장 모호한 것부터 공략.

| 판단 축 | 배점 | 이럴 때 묻는다 | 질문 예시 |
|--------|-----|-------------|---------|
| Audience / Scope (15) | 15 | 사용 대상 불분명 또는 문제 범위 모호 | "누가 쓰나요?" + "즉각 요구만인가요, 더 넓은 범위(오늘 전체 일정 등)도?" |
| Env (15) | 15 | 실행 환경 미정 | "브라우저? 터미널? 아니면 이미 쓰는 플랫폼(구글시트, 슬랙 등) 위에서?" |
| Lifespan (15) | 15 | 지속성 불명확 | "한 번 쓰고 끝인가요, 계속 유지보수할 건가요?" |
| Constraint (15) | 15 | 기술 제약 미확인 | "특정 언어나 환경 제약이 있나요?" |
| Distribution (10) | 10 | 배포 방식 미정 | "다른 사람이 설치하거나 URL로 접근해야 하나요? 슬랙에서 접근한다면 — 봇/앱 통합이 필요한가요, URL 링크 공유로 충분한가요?" |
| Integration (10) | 10 | 연동 필요 여부 | Notion+Slack이면 Notion Custom Agent, 반복 자동화면 Claude Cowork 먼저 확인 |
| Security (20) | 20 | 외부 의존성 불명 | 아래 Security 질문 참조 |

**Security 축 질문 예시** (가장 중요 -- 배점 최고):

- "이 기능이 외부 서비스(API)를 호출해야 하나요? 로컬 데이터만으로 해결 가능한가요?"
- "사용자 인증이나 로그인이 필요한가요?"
- "민감한 데이터(개인정보, 결제, 의료)를 다루나요?"
- "API 키 없이 같은 결과를 얻을 수 있는 방법이 있나요?"
  (예: 공개 RSS, 브라우저 DOM 직접 읽기, 로컬 파일 처리 등)

**원칙**:

- 이미 명확히 답한 축은 건너뛴다
- **구현 방법을 사용자에게 묻지 않는다** — Form Judge의 몫이다.
  폴링 vs 웹훅, REST vs GraphQL, cron 주기, 실행 환경(GitHub Actions vs 서버 등)은
  Form Judge가 판단한다. 사용자에게 기술 선택을 절대 위임하지 않는다.
- UI/UX 세부사항은 묻지 않는다 -- 형태 결정이 우선
- 답을 유도하지 않는다 ("이건 서비스 아닌가요?" 금지)
- **Security 축이 낮으면 우선 공략한다** -- API 키 필요성을 조기에 확인

**답변 충실도 확인**:

Form Judge를 실행하기 전에 사용자 답변의 충실도를 점검한다.
아래에 해당하면 해당 답변에 대해서만 **1회** 재질문한다.

| 판단 기준 | 예시 | 재질문 방식 |
|----------|-----|-----------|
| 단순 예/아니요 (맥락 없음) | "네" / "아니요" | "어떤 상황에서 쓰시는 건지 조금 더 알려주실 수 있어요?" |
| 5단어 미만 단답 | "그냥 내가 쓸 거" | "어떤 방식으로 쓰실 예정인지 예를 들어주시면 더 맞게 추천해드릴 수 있어요." |
| 회피/무관심 답변 | "아무거나요" / "상관없어요" | "어떤 방향이든 잘 맞춰드릴 수 있어요. 혹시 {해당 축 핵심 기준}을 좀 더 말씀해주실 수 있어요?" |
| 전제 모순 | "서비스로 만들게요, 빠르게 해야 해서" | "빠른 게 목표라면 {더 가벼운 대안}이 오히려 더 빠를 수 있어요. 서비스로 만드셔야 하는 이유가 따로 있으신가요?" |

- 두 번 연속 모호한 답변이 오면 수용하고 해당 축을 "미결"로 기록
- 재질문이 1회를 초과하지 않도록 한다

---

### 2. Form Judge -- 제품 형태 판정

라운드마다 Agent로 형태 판정:

```text
You are deciding the best product form for a given problem.
Evaluate clarity and fit. Score 0-100.

## Mandatory Pattern Pre-Check (점수 계산 전에 먼저 확인)

입력에서 다음 패턴이 감지되면 해당 형태를 반드시 먼저 검토한다.
이 체크를 건너뛰고 script/cli-tool/web-service를 추천하면 오류다.

| 패턴 | 먼저 검토할 형태 | 확인 포인트 |
|------|----------------|-----------|
| Notion + Slack 알림/자동화 | notion-custom-agent | Notion Business+? |
| DB 상태 변경 → 알림 (트리거 1-2개 + 고정 메시지) | platform-extension(Notion Automation / Zapier) | 노코드로 충분한가? |
| 반복 스케줄 + 다중 앱 연결 | claude-cowork | Claude Pro+? |

available_services에서 플랜·티어가 확인되지 않으면 "(확인 필요)" 표시로 포함.
확인이 안 됐다는 이유로 더 무거운 형태를 추천하지 않는다.

## Core Principle: Lightweight-first
ALWAYS prefer the lightest form that solves the problem.
If recommending a heavy form (web-service, cli-tool), you MUST
explain why lighter alternatives fail.

Preference order: claude-skill > script > local-html >
bookmarklet > userscript > notion-custom-agent > claude-cowork >
platform-extension > apps-script-webapp >
chrome-extension > cli-tool > web-service

## Implementation Cost (단순함 강제)

Rate the recommended form's implementation cost:

- 1 = 노코드 즉시 (Notion Automation, Zapier/Make 단순 트리거)
- 2 = 노코드 조합 (notion-custom-agent, n8n 노드, claude-cowork)
- 3 = 최소 코드 (Apps Script, bookmarklet, claude-skill)
- 4 = 코드 작성 필요 (chrome-extension, cli-tool, apps-script-webapp)
- 5 = 풀스택 개발 (web-service)

승격 규칙: competing_forms 중 score_diff ≤ 10이고
implementation_cost가 2 이상 낮은 대안이 있으면,
그 대안을 추천 form으로 승격하고 rationale에 이유를 명시한다.

## Scoring Rubric
| Item         | Max | Criteria                                    |
|--------------|-----|---------------------------------------------|
| Audience     | 15  | 사용 대상이 명확함                          |
| Env          | 15  | 실행 환경이 특정됨                          |
| Lifespan     | 15  | 1회성/지속 여부 결정됨                      |
| Constraint   | 15  | 기술 제약 파악됨                            |
| Distribution | 10  | 배포 방식 결정됨                            |
| Integration  | 10  | 연동 요구사항 파악됨                        |
| Security     | 20  | 외부 의존성/API 키 필요성 평가 완료,        |
|              |     | 키 없는 대안 검토됨, 최소 권한 설계됨       |

## Product Forms (lightest first)
- claude-skill: Claude Code 대화 중 실행, 설치/키 불필요
- script: Shell/Python 로컬, 키 대부분 불필요
- local-html: 브라우저 단일 파일, 오프라인 가능, 키 불필요
- bookmarklet: 브라우저 즐겨찾기 JS 한 줄, 설치 불필요
- userscript: Tampermonkey 등, 브라우저 컨텍스트 접근, 키 불필요
- notion-custom-agent: Notion 팀 자동화 에이전트. 한 명 세팅 → 팀 공유.
  Slack 멘션 트리거, 리포트 생성, 태스크 태깅. 키·서버 불필요.
  Notion+Slack 케이스 기본 첫 검토. 불확실하면 WebFetch로 확인:
  Ref: https://www.notion.com/ko/help/guides/build-your-first-custom-agent
- claude-cowork: Claude Desktop 반복 자동화 (Pro 이상). Slack·Notion·GitHub
  스케줄링. 서버 불필요. 불확실하면 WebFetch: https://claude.com/product/cowork
- platform-extension: 기존 플랫폼 위 확장 (Apps Script, Slack Workflow,
  Notion Automation, Zapier/Make, n8n). 인증 플랫폼 위임.
  n8n: 복잡 로직·셀프호스팅 필요 시.
- apps-script-webapp: Apps Script 웹앱. G Suite 인증, Sheets·Drive·Gmail 연결.
  내부 폼·대시보드 최적. 키·서버 불필요.
- chrome-extension: 브라우저 컨텍스트, 설치형, 키 선택적
- cli-tool: 터미널 기반, 팀 배포, 환경변수 관리 가능
- web-service: 서버 필요, 인증/보안 관리 필수

## Security Evaluation Checklist
1. Need API keys? → Is there a keyless alternative?
2. Notion + Slack automation? → Check notion-custom-agent FIRST
   (1 setup → team shared, Slack trigger, KB answers, zero keys/servers).
3. Recurring multi-app automation? → Check claude-cowork FIRST (Pro+, no server).
4. Existing platform (Sheets, Slack, Notion)? → Prefer platform-extension.
   Simple/no-code: Zapier/Make. Complex/self-hosting: n8n.
   G Suite URL+Sheets: apps-script-webapp.
5. Need a server? → Is serverless possible?
6. Sensitive data? → Can it stay local?
7. User auth? → Reuse existing auth (Google Workspace, Slack SSO)?

## Uncertainty Detection
Read the user's MOST RECENT answer carefully.
If it contains hedging language such as:
- "고민되네", "잘 모르겠어", "어떤 게 나을지"
- "~인 것 같긴 한데", "~도 좋을 것 같고", "일단은 ~"
- "아마", "아마도", "~인 것 같아"

Set "user_uncertain": true.
When user_uncertain is true, do NOT commit to a form even if score ≥ 80.
Instead, identify the single most ambiguous axis and surface one
clarifying question.

Special case — if the user expresses uncertainty about Slack access:
Ask explicitly: "슬랙 봇/앱(관리자 승인 필요) 수준이 필요한가요,
아니면 웹 URL을 automated-messages로 공유하는 것(설치·승인 불필요)으로
충분한가요?"

## Input
{원본 입력 + 모든 Q&A}

## Available Services Context
{available_services — 0.5단계에서 파악한 환경. 없으면 "unknown"}
형태 판정 시 사용 불가 서비스는 후보에서 제외한다.

## Already Tried
{tried_tools — 이미 시도한 도구 + 막힌 이유. 없으면 "none"}
이 도구들은 추천에서 제외하거나, 막힌 이유를 해결하는 대안임을 명시한다.

## Output (JSON only)
{
  "score": 72,
  "form": "chrome-extension",
  "implementation_cost": 4,
  "user_uncertain": false,
  "lighter_alternative": {
    "form": "local-html",
    "viable": false,
    "reason": "브라우저 탭의 DOM에 접근해야 하므로 extension 필요"
  },
  "competing_forms": [
    {
      "form": "apps-script-webapp",
      "score": 68,
      "implementation_cost": 3,
      "pros": ["서버 불필요", "Google 인증 그대로 사용", "Sheets 직접 연결"],
      "cons": ["Google Workspace 계정 필요", "UI 커스터마이징 제한적"],
      "choose_when": "팀이 Google Workspace를 쓰고 Sheets 데이터를 다뤄야 할 때"
    }
  ],
  "breakdown": {
    "audience_scope": {"score": 12, "max": 15, "note": "..."},
    "env": {"score": 13, "max": 15, "note": "..."},
    "lifespan": {"score": 10, "max": 15, "note": "..."},
    "constraint": {"score": 12, "max": 15, "note": "..."},
    "distribution": {"score": 7, "max": 10, "note": "..."},
    "integration": {"score": 5, "max": 10, "note": "..."},
    "security": {"score": 13, "max": 20, "note": "..."}
  },
  "dependencies": [
    {
      "type": "api_key",
      "service": "서비스명",
      "required": true,
      "keyless_alternative": "대안 설명 또는 null",
      "min_scope": "read-only, 특정 엔드포인트만"
    }
  ],
  "weakest": "security",
  "suggestion": "...",
  "rationale": "이 형태를 추천하는 이유 한 줄"
}

competing_forms 작성 규칙:
- 추천 form과 점수 차가 10 이하이고 실제로 viable한 형태만 포함
- 점수 차가 없거나 대안이 없으면 빈 배열 []
- pros/cons는 각 3개 이내, 구체적으로
```

- **80점 이상 + user_uncertain: false** -> Step 3.5 (선행 데이터 작업 확인)로
- **80점 이상 + user_uncertain: true** -> 점수 표시하되 형태 미확정.
  "거의 다 왔는데 한 가지만 더 확인할게요." + 가장 불확실한 축 질문 1개
- **80점 미만** -> 점수 보여주고 다음 라운드
- **최대 7라운드** -> 이후엔 현재 최선 형태로 진행
- **Security 축이 15 미만이면** -> 반드시 Security 관련 질문 추가

---

### 3. 점수 공유 & 다음 라운드

```text
Round {N} 결과 -- 형태 명확성 {score}/100

추천 형태: {form}
이유: {rationale}

{lighter_alternative가 있으면}
  경량 대안: {lighter_form} -- {viable ? "가능하지만 " + 트레이드오프 : reason}

Audience     {bar}  {score}/15
Env          {bar}  {score}/15
Lifespan     {bar}  {score}/15
Constraint   {bar}  {score}/15
Distribution {bar}  {score}/10
Integration  {bar}  {score}/10
Security     {bar}  {score}/20

보강 필요: {weakest축}
-> {suggestion}
```

`competing_forms`가 있으면 (점수 차 10 이하) 추가로 출력:

```text
---

비슷하게 적합한 형태가 있습니다. 비교해보세요:

|  | {추천 form} | {대안 form} |
|--|--|--|
| 적합도 | {score}/100 | {alt_score}/100 |
| 장점 | {pros 각 줄로} | {alt_pros 각 줄로} |
| 단점 | {cons 각 줄로} | {alt_cons 각 줄로} |
| 이럴 때 선택 | {choose_when} | {alt_choose_when} |

어느 쪽으로 가실건가요? (선택하지 않으면 추천 형태로 진행합니다.)
```

이후 계속:

```text
---

Round {N+1}

{질문}
```

---

### 3.5. 선행 데이터 작업 확인

자동화·연동·서비스 형태가 확정되면 묻는다.
(claude-skill, script, local-html, bookmarklet, userscript는 생략)

```text
이 자동화를 실행하기 전에 기존 데이터를 먼저 정리·변환해야 하는
1회성 선행 작업이 있나요?

예: 담당자 이름이 텍스트 값으로 저장되어 있어 Person 필드로 변환 필요,
    레거시 포맷 데이터를 신규 스키마로 마이그레이션 필요 등

없으면 "없어요"라고 하시면 바로 다음 단계로 넘어갑니다.
```

- **있다**: Phase 1 첫 항목에 "선행 데이터 작업 (Claude/AI 활용 권장)"을
  추가한다. Claude, Notion AI 등으로 처리 가능한 경우 방법을 안내한다.
- **없다 / 해당 없음**: 즉시 Step 4로 넘어간다.

---

### 4. 의존성 & 보안 평가 (형태 확정 후)

형태가 확정되면 로드맵 전에 **외부 의존성을 전수 평가**한다.

DB 접속, MCP 연결, 운영 데이터 접근이 포함되면
Step 6 인라인 보안 점검에서 🔴STOP으로 분류된다.
**이 단계의 평가 결과는 Step 6에서 그대로 사용한다 — 재평가하지 않는다.**

```text
제품 형태: {form} (확정)

외부 의존성을 점검합니다.

---

의존성 평가
```

**평가 순서**:

1. 입력/Q&A에서 언급된 모든 외부 서비스/API를 목록화
2. 각 의존성에 대해 3단계 검토:

```text
의존성: {서비스명}
  1단계 -- 필요한가?
    -> {이 기능 없이 핵심 문제를 해결할 수 있는가?}
  2단계 -- 키 없이 가능한가?
    -> {공개 API, RSS, DOM 스크래핑, 로컬 처리 등 대안}
  3단계 -- 최소 권한은?
    -> {read-only, 특정 엔드포인트, rate limit 등}
```

**결과 분류**:

| 분류 | 설명 | 액션 |
|------|------|------|
| 제거 가능 | 키 없이 대안으로 해결 | 대안 방법 로드맵에 반영 |
| 키 필요 (최소) | 키 필수, 최소 권한으로 축소 | API 키 요청서 생성 |
| 키 필요 (넓음) | 넓은 권한 필요 | 요청서 + 보안 리뷰 권고 |

**키 필요 시 확인**: (1) 담당자? (2) 기존/신규? (3) 로컬/프로덕션?

---

### 5. 로드맵 라운드

의존성 평가가 끝나면 페이즈 설계 질문으로 전환한다.

```text
제품 형태: {form} (확정)
외부 의존성: {N}개 ({제거 가능 M개}, {키 필요 K개})

이제 단계를 나눠보겠습니다.

Phase 설계 — {질문 1-2개}
```

페이즈 설계 질문 방향 (MVP 최소 조건 / 사용성 추가 / 배포·확장 시점 /
팀 배포 키 관리). 페이즈는 3개 기본, 필요에 따라 2~5개로 조정.

---

### 6. 완료 -- 로드맵 문서 생성 & 저장

**로드맵 문서 내용**:

```markdown
# {제목} -- 제품화 로드맵

**제품 형태**: {form}
**명확성**: {score}/100 ({rounds}라운드)
**보안 등급**: {최경량 | 경량 | 중간 | 무거움}
**작성일**: {오늘}

---

## 제품 선택 근거

{왜 이 형태가 이 문제에 맞는지 -- 2-3줄}

{더 가벼운 형태가 안 되는 이유 -- 1-2줄. 최경량 형태면 생략}

## 외부 의존성 & 보안

**의존성 요약**: {총 N개 -- 제거 M개, 키 필요 K개}

{키가 필요한 의존성이 없으면}
  이 제품은 외부 API 키 없이 동작합니다.

{키가 필요한 의존성이 있으면, 각각에 대해}
### API 키 요청서 -- {서비스명}

| 항목 | 내용 |
|------|------|
| 서비스 | {서비스명 + URL} |
| 필요 권한(scope) | {read-only, 특정 엔드포인트 등 최소 범위} |
| 사용 목적 | {이 키로 무엇을 하는지 한 줄} |
| 대안 검토 결과 | {키 없이 시도한 방법과 왜 안 되는지} |
| 사용 환경 | {로컬 개발 / 프로덕션 / CI 등} |
| 요청 담당자 | {사용자가 답한 담당자} |
| 키 사용자 | {이 제품을 실행할 사람/시스템} |

> 이 요청서를 키 담당자에게 전달하세요.

## Phase 1 -- MVP

**목표**: {한 줄}
**포함 기능**:
- {기능 1}
- {기능 2}

**보안 체크**:
- [ ] API 키 없이 동작 확인 {또는: 키 환경변수로 분리}
- [ ] 민감 데이터 로컬 처리 확인

**완료 기준**: {검증 가능한 기준}
**예상 소요**: {러프하게}

## Phase 2 -- 사용성

**목표**: {한 줄}
**추가 내용**: {추가 기능/개선}
**완료 기준**: {기준}

## Phase 3 -- 배포/확장

**목표**: {한 줄}
**추가 내용**: {배포 자동화, 문서화, 확장 등}
**보안 체크**: [ ] 키 로테이션 문서화 / [ ] 접근 권한 최소화
**완료 기준**: {기준}

---

## 지금 당장 시작할 것

{Phase 1의 첫 번째 구체적 액션 -- 동사로 시작}

---

## 원본 명세 요약

{입력 원문 핵심 2-3줄}
```

**저장**:

- Notion URL로 시작했으면 ->
  `mcp__notion__notion-create-pages`로 해당 페이지 하위 페이지 생성
- 파일/텍스트로 시작했으면 ->
  `Write`로 현재 작업 디렉토리에 `./{제목}-product-brief.md` 저장

**보안 점검 -- 인라인**:

**Step 4에서 평가한 의존성 결과를 아래 등급으로 판정하고 출력한다.**
질문하지 않는다. 재평가하지 않는다. 생략하지 않는다.

**등급 판정 기준**:

🔴 **STOP** — 설계 중단, 사내 보안 담당에게 리뷰 요청:

- 프로덕션 DB·서비스에 AI 도구가 직접 접근하는 구조
- PII(이름·전화·이메일·의료·결제 정보)가 외부 LLM 서버로 전송 가능
- AI Gateway(PII 가드레일) 없이 DB 쿼리 결과가 LLM으로 흐르는 경로
- 자격증명이 공개 채널·버전관리 저장소에 포함되는 설계

🟡 **REVIEW** — 자가 체크 후 진행:

- 테스트·스테이징 환경 연결 (프로덕션 데이터 미러링 여부 불명)
- 내부 서비스 접근 신규 추가 (MCP, API 키)
- PII 포함 여부 불확실한 데이터 접근

🟢 **SAFE** — 안전 진행:

- 문서·모니터링·코드 전용 도구 (PII 미포함)
- AI Gateway(가드레일 확인됨)를 통한 연결
- 공개 API·익명화 데이터만 사용

**민감 데이터 기준**:

| 등급 | 해당 데이터 |
|------|-----------|
| 🔴 STOP | 이름·전화·이메일·ID번호, 의료·진료 기록, 결제·카드 정보, 인증 토큰·비밀번호 |
| 🟡 REVIEW | 내부 운영 지표·계약 조건, 직원 정보, 시스템 구조·인프라 정보 |
| 🟢 SAFE | 익명화·집계 통계, 코드(자격증명 제외), 공개 API 응답, 공개 문서 |

**출력 형식** (의존성 있을 때):

의존성이 없는 경우:

```text
보안 점검 🟢 SAFE: 외부 의존성 없음.
```

🔴 STOP인 경우:

```text
================================================================
  보안 점검 🔴 STOP -- {의존성명}
================================================================
위험: {무엇이 문제인지 1줄}
이유: {왜 위험한지 — PII 유출 경로, 법적 리스크 등}

진행 전 사내 보안 담당 채널에 아래 리뷰 요청서를 제출하세요:

  [보안 리뷰 요청]
  - 연결 대상: {시스템명}
  - 데이터 유형: {접근하려는 데이터 종류}
  - 사용 목적: {이유}
  - AI 도구: {MCP 서버명, API 클라이언트 등}
  - 환경: {prod / staging / local}
  - 권한: {read-only / read-write}

대안:
  - AI Gateway(PII 가드레일)를 통한 연결
  - 민감 컬럼 제외한 읽기 전용 뷰(view) 접근
  - 로컬 익명화 데이터로 개발 후 리뷰를 거쳐 연결
================================================================
```

🟡 REVIEW인 경우:

```text
================================================================
  보안 점검 🟡 REVIEW -- {의존성명}
================================================================
감지: {무엇을 하려는지}

아래 중 하나라도 해당하면 🔴 STOP:
  - [ ] 프로덕션 환경 데이터에 접근하는가?
  - [ ] PII·민감 데이터가 포함될 수 있는가?
  - [ ] 쿼리 결과가 외부 LLM 서버로 전송되는가?
  - [ ] 자격증명이 공개 채널·저장소에 포함되는가?

설계 가이드:
  - API 키는 환경변수로 분리, 버전관리에서 제외
  - 팀 공유 키는 시크릿 매니저 사용 (직접 공유 금지)
  - 최소 권한(read-only) 원칙
  - DB 직접 접근 시: 민감 컬럼 제외 뷰 + AI Gateway 경유 권장
================================================================
```

🟢 SAFE인 경우:

```text
보안 점검 🟢 SAFE -- {의존성명}: {안전한 이유 1줄}
```

보안 점검 출력 후에 완료 안내를 출력한다.

**완료 안내**:

```text
로드맵이 완성되었습니다.
저장 위치: {Notion 링크 또는 로컬 파일 경로}

제품 형태: {form}
보안 등급: {등급}
Phase 수: {N}개
API 키: {불필요 | N개 필요 -- 위 보안 점검 참조}
지금 시작: {첫 액션}

---

{API 키가 필요하면}
위 보안 점검의 담당자에게 확인 후 Phase 1을 시작하세요.
{API 키가 없으면}
Phase 1을 바로 시작할 수 있습니다.
```

---

## 엣지 케이스

- **sharpen 결과물 없이 아이디어만 입력**: "명세가 없어도 괜찮습니다.
  지금 알고 있는 범위에서 시작하겠습니다."
- **사용자가 형태를 이미 정했을 때**: 해당 형태를 전제로 로드맵 라운드만 진행.
  단, 더 가벼운 형태가 가능하면 한 번은 챌린지.
  ("그 형태를 선택한 이유가 있나요? {더 가벼운 대안}으로도 해결 가능해 보이는데요.")
- **"API 키 써도 됩니다"**: 수용하되, 최소 권한 원칙은 유지.
  요청서는 반드시 생성. "키를 쓰되, 필요한 최소 범위로 제한하겠습니다."
- **"서비스로 만들어야 해"**: 수용하되, 이유를 한 번 확인.
  "서비스가 필요한 핵심 이유가 뭔가요? (다수 동시 접속 / 데이터 중앙 관리 /
  24시간 운영 등)". 이유가 약하면 플랫폼 확장, 크롬 익스텐션, CLI 대안 제안.
- **북마클릿/유저스크립트로 충분한 경우**: 크롬 익스텐션이 추천됐는데
  실제로는 특정 페이지 DOM만 읽으면 되는 경우, 북마클릿이나 유저스크립트가
  더 가볍다. "스토어 등록이나 패키징 없이 해결 가능합니다."
- **사용자가 불확실 신호를 보낼 때** ("고민되네", "~인 것 같긴 한데",
  "어떤 게 나을지 모르겠어" 등): Form Judge `user_uncertain: true`로 처리.
  점수가 80 이상이어도 형태 확정 금지. 가장 모호한 축 1개를 집중 질문.
  슬랙 접근 불확실이면 반드시 물을 것:
  "봇/앱(관리자 승인 필요)이 필요한가요, URL을 automated-messages로
  공유하는 것(설치·승인 불필요)으로 충분한가요?"
- **슬랙에서 접근 + 정보 조회** 조합: 자동으로 slash command나 Bolt App을
  추천하지 말 것. "웹앱/local-html URL + Slack automated-messages 링크 공유"가
  더 가벼운 대안이다. Bot Token 불필요, 관리자 승인 불필요.
  URL만 있으면 팀 전체 접근 가능. Slack 통합의 기본 첫 선택지로 두어야 한다.
- **"Notion+Slack 연결" / "API 다 연결"**: 서비스 전에 3단계 확인:
  1. **Notion Custom Agent**: Slack 멘션 트리거, KB 답변, 리포트. 키·서버 불필요.
  2. **Claude Cowork**: 반복 스케줄. Slack·Notion·GitHub 통합. 서버 불필요 (Pro+).
  3. **Notion Automation**: 트리거 1-2개+고정 메시지. 트리거 3개↑ 또는
     동적 필드 전달 → Custom Agent. **Zapier/Make**: 노코드 300+ 앱.
     **n8n**: 복잡 로직·셀프호스팅.
  위 셋으로 안 될 때만 web-service. "안 되는 이유"를 먼저 확인.
- **"이 정도면 됐어"**: 현재 상태로 즉시 로드맵 생성. 80점 미만이면
  불확실한 항목을 로드맵에 '미결 사항'으로 표시.
- **외부 의존성이 5개 이상**: "외부 의존성이 많습니다. 더 가벼운 형태로
  재검토하거나, 의존성을 Phase별로 나눠 점진 도입하는 것을 권장합니다."
- **페이즈가 너무 많아질 때**: "Phase 3 이후는 현재 시점에선 오버스펙일 수
  있습니다. Phase 1을 끝낸 후 다시 productify를 실행하는 것을 권장합니다."
- **Notion fetch 실패**: "Notion 연결이 필요합니다. MCP 설정을 확인해주세요.
  또는 내용을 직접 붙여넣어 주세요."
