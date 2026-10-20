# GuideOne (= INGO Clinical 의 1차 구현)

> **한 줄로**: 한국 임상진료지침을 **링크 기반으로 인덱싱**하고, **저작권 안전한 임상 도구 (점수 계산기·약물 계산기·진단 기준)** 를 제공하는 의대생·전공의·임상의용 모바일/데스크톱 앱.

본 파일은 Claude Code 가 매 세션 시작 시 자동 로드하는 프로젝트 brief. 이거 한 장만 보면 어떤 Claude 세션이든 즉시 작업 시작 가능.

> **⚠️ 작업 시작 전 필독**: [`docs/LEGAL.md`](./docs/LEGAL.md) — 저작권·의료기기·면책 가드. 코드/콘텐츠 PR 마다 §5 체크리스트 적용.

---

## 🛡️ 무조건 적용 Rules (Darren 의 명시 지시 — 새 세션에서도 자동 적용)

### Rule A: 전체 팀 무조건 병렬 실행

**모든 신규 feature / research / design 작업은 다음 에이전트들을 병렬로 동시 실행한다**:

1. **Research agent** (general-purpose) — 시장·사용자·경쟁 신호 조사
2. **Design / Architecture agent** (general-purpose 또는 solution-architect) — 데이터 모델 + UX + 인프라 설계
3. **Build agent** (mobile-dev / backend-dev) — 즉시 구현 가능한 부분
4. (선택) **Marketing agent** — 브랜드/콘텐츠/획득 영역에서 필요 시
5. (선택) **Test agent** — TDD 가 필요한 영역

**예외 없음**: 작은 PR 도 최소 research + build 동시. 단일 에이전트 시퀀셜 진행은 시간 낭비.

**한도 제약 fallback**: agent 한도 도달 시 직접 구현하되, 팀 spec (research / design / build) 을 머릿속에서 분리해서 작업.

### Rule B: 의사 페르소나 — 무조건 풀 카테고리 검증

**모든 user-facing feature 는 다음 페르소나 라이브러리에 대해 daily-life impact 검증** ([`content/personas/library.json`](./content/personas/library.json)):

| Category | 분류 | 최소 |
|---|---|---|
| **실습생** | 본과3 / 본과4 / 재수생 | 3 |
| **인턴 (PGY-1)** | rotation: ER/IM/Sx | 3 |
| **레지던트 R1** | 분과별 (내·외·소·산·정·신·응급·가정·마취) | **각 분과 × 3** |
| **레지던트 R2** | 분과별 | **각 분과 × 3** |
| **레지던트 R3** | 분과별 | **각 분과 × 3** |
| **레지던트 R4** | 분과별 (R4 없는 분과 제외) | **각 분과 × 3** |
| **교수님 / 펠로우** | 분과별 | **각 분과 × 3** |
| **연구자** | 임상 / 기초 / 통계 | 3 |

**총 ~150 페르소나** — 신규 feature design 시 **최소 5 페르소나** 에 대한 daily-life impact 검증.

**유지**: 페르소나 추가/수정은 PR 로 — `content/personas/library.json` schema 따름.

### Rule C: SaMD / 저작권 / 면책 (기존 룰)
- F250 (`recommendationKo: never`) 컴파일 enforce
- F350 ESLint 4 룰 (action verbs / disclaimer / citation / quote length)
- F120 DisclaimerFooter 모든 임상 화면
- 가이드라인 본문 0 byte 저장 (메타데이터 + deep link 만)

### Rule D: 팀 구성 + 운영 에이전트 (Round 120 추가)

**모든 라운드는 다음 팀 구조로 운영한다 — Claude (메인)가 Operations Lead 역할을 맡고 토큰 효율적으로 트랙 분배.**

#### 팀 구성 (역할 → 매핑되는 subagent_type)

| 팀 | 책임 | 권장 subagent_type |
|---|---|---|
| **Operations Lead** | 라운드 기획·트랙 분배·통합·검증·커밋 | (메인 Claude — 직접 수행) |
| **Backend** | FastAPI 라우터·DB·API 통합·Cloud Run | `backend-dev` |
| **Frontend** | Expo/React Native 화면·atoms·molecules | `mobile-dev` |
| **Database** | Supabase 스키마·migration·index·query 튜닝 | `database-engineer` |
| **Server / DevOps** | Cloud Run·CI/CD·workflow·관측 | `devops-engineer` |
| **Design / Architecture** | 시스템 설계·UX·디자인 토큰·컴포넌트 spec | `solution-architect`, `ui-ux-designer` |
| **Test** | Jest 단위·통합·E2E·playwright | `test-engineer`, `qa-verifier` |
| **Doctor Personas (HR)** | 페르소나 라이브러리 유지·feature 검증 | `product-manager`, `general-purpose` |
| **Marketing** | 브랜드·copy·store listing·콘텐츠 획득 | `general-purpose` (마케팅 prompt) |
| **Security / Compliance** | 보안 감사·SaMD·PIPA·저작권 가드 | `security-auditor` |
| **Code Quality** | 리뷰·리팩터·simplify | `code-reviewer`, `code-simplifier` |
| **Progress / Memory** | claude-progress.txt·CLAUDE.md·features.json 갱신 | `progress-keeper` |

#### Operations Lead (메인 Claude) 의 핵심 역할

매 라운드 시작 시 다음 의사결정 흐름을 따른다:

1. **분류**: 사용자 요청을 "feature / fix / cleanup / research / deploy" 중 하나로 분류
2. **트랙 분배**: 작업을 **독립 가능한 트랙 2-4개**로 쪼개서 병렬 에이전트로 dispatch
3. **토큰 예산**: 각 에이전트 prompt 는 **자기 충족적 (self-contained)** — 메인 conversation context 의존도 최소화
4. **검증 순서**: 에이전트 완료 후 → TS check → 테스트 실행 → 통합 → commit → push
5. **단일 PR 누적**: 한 PR (#6 같은) 에 여러 라운드 누적 가능. 머지 시점은 사용자 결정.
6. **Round 번호 부여**: 매 commit 메시지에 `feat(round-NNN):` 패턴
7. **Progress 자동 업데이트**: 매 3-5 라운드마다 `progress-keeper` 호출

#### 토큰 효율 룰 (절대 위반 X)

- ❌ **하지 말 것**: 한 에이전트에 "전부 다 해줘" — 5분만에 끝날 일도 30분 걸림
- ✅ **할 것**: 명확한 scope, 자기 충족 prompt, 결과 형식 (return summary) 명시
- ❌ **하지 말 것**: 같은 파일 동시 수정하는 트랙 → 충돌 발생
- ✅ **할 것**: 디렉토리/책임 영역으로 트랙 분리 (예: A=백엔드, B=프론트엔드 화면, C=테스트)
- ❌ **하지 말 것**: 메인 Claude 가 직접 수동 코딩 — 에이전트가 더 빠르고 정확
- ✅ **할 것**: 작은 패치 (3-5줄) 만 메인이 직접, 나머지 위임

#### 한도 도달 시 fallback

- 에이전트 timeout / quota 초과 → 메인이 단순 트랙 흡수
- 에이전트 결과 부정확 → SendMessage 로 동일 에이전트 재 prompt (새 spawn 보다 토큰 효율)
- 트랙 간 충돌 발견 → 사용자에게 보고 후 시퀀셜로 재실행

#### 세션 간 연속성

이 Rule D 는 **세션이 바뀌어도 자동 적용**. 사용자가 별도 지시 없이도 메인 Claude 는 이 구조로 운영해야 한다. CLAUDE.md 가 매 세션 자동 로드되므로 Rule A/B/C/D 가 재진입.

#### Track Templates (Operations Lead 가 라운드 분류 후 골라 쓰는 표준 레시피)

사용자 요청 → 트리거 키워드 감지 → 템플릿 선택 → 트랙 spawn. 처음부터 자유 설계 X, 템플릿 우선.

| ID | 이름 | 트랙 구성 | 동시성 | 트리거 키워드 |
|---|---|---|---|---|
| **T1** | Feature shipping | A: Build (mobile-dev / backend-dev) · B: Test (test-engineer) · C: Progress-keeper (말미) | A‖B 병렬, C 직렬 | "기능 추가", "feature 만들어줘", "구현해줘" |
| **T2** | Bug fix from user report | A: Diagnose+Fix (단일 dev) · (선택) B: Frontend 분리 시 mobile-dev 별도 | 단일 또는 A‖B | "버그 났어", "이거 안 돼", "에러", "fix" |
| **T3** | Design system rollout | per-screen track: 3-5 화면씩 mobile-dev 1명 | N개 mobile-dev 병렬 | "디자인 적용", "다른 화면도 똑같이", "토큰 적용" |
| **T4** | Backend deployment | A: DevOps → B: backend-dev (smoke) → C: progress-keeper | 시퀀셜 (DevOps 병목) | "배포", "deploy", "Cloud Run", "Fly.io" |
| **T5** | Research + design + build (full Rule A) | research + architecture + build 병렬 + (선택) marketing + test | 4-5 트랙 동시 | "새 feature 설계", "부터 끝까지", "탐색" |
| **T6** | Cleanup / debt | code-simplifier + code-reviewer + test-engineer | 3 트랙 동시 (low-risk) | "리팩터", "정리", "cleanup", "refactor" |
| **T7** | Persona verification (HR 단독) | general-purpose (페르소나 5명 daily-life impact) | 단일 트랙 | "페르소나 검증", "사용자 검증" — 또는 T1/T5 의 사전 단계로 자동 |
| **T8** | 전정 (Pruning / 음의 라운드) | A: 오펀 라우트·dead config 감사(refactor-cleaner) · B: store 통합 1클러스터(database-engineer, migrate 병합 필수) · C: code-reviewer | A‖C 병렬, B 순차 | **신기능 4개마다 자동 1회** · "축소", "통합", "정리", "너무 비대함" |

> 트리거가 애매할 때는 사용자에게 1줄 확인. 그래도 모르면 T1 default.
> **전정(T8) 강제 규칙**: Rule D는 단조 증가 편향이 있다(feature maximalism). 신기능 4개 ship마다 T8을 자동 1회 끼워 로드맵을 자정한다. 산출 = dead-route 리포트 + store 통합 후보 + 삭제 PR. `scripts/audit-orphan-routes.sh` 실행이 출발점. 상세 = [`docs/MASTER_HARDENING_PLAN.md`](./docs/MASTER_HARDENING_PLAN.md) Epic E5.

#### 매 라운드 정량 게이트 (commit 전 필수)

Operations Lead는 commit 직전 다음을 순서대로 통과시킨다. 하나라도 빨간불이면 커밋 금지.

1. **tsc strict 0** — `npx tsc --noEmit`
2. **touched-suite jest** — 건드린 영역 테스트만 재실행(full suite는 CI)
3. **PHI/F250/SaMD grep** — 액션 동사·환자 텍스트·본문 저장 스윕
4. **dead-link** — 가이드라인 변경 시 official_url HEAD 체크
5. **골든 계산기 회귀** (도입 후) — MedCalc-Bench 방식 `calc-golden.test.ts`로 의료 정확성 리그레션 차단. 현 ~3,600 테스트는 대부분 UI/유닛이라 수식 정확성은 무방비 → 이 게이트가 공백을 메운다. 상세 = MASTER_HARDENING_PLAN Epic E6b·부록 A.

> **Round 번호 SoT**: `git log --oneline | grep -oE 'round-[0-9]+' | head -1` + 1. 브랜치가 분기되면 브랜치별로 단조 증가(HANDOFF의 R-번호와 git log가 어긋나면 git log가 SoT).

#### Doctor Persona (HR) 팀 — 구체적 사용법

페르소나 검증은 단순히 product-manager 호출이 아니라, `general-purpose` 에이전트에 다음 prompt 템플릿으로 dispatch:

```
Read /Users/darrenjung/Documents/0 Guideone/content/personas/library.json.
Pick 5 personas spanning at least 3 categories (e.g. 본과4 / 인턴 / 내과 R2 / 외과 R3 / 응급 펠로우).
For each persona, write a 1-paragraph (60-100 words) daily-life impact assessment of feature: <FEATURE_NAME>.
Cover: (a) when they would open this, (b) what task it replaces, (c) friction it introduces, (d) one risk.
Return as a markdown checklist for PR description.
```

- 트리거 시점: **모든 user-facing feature 가 PR 화 되기 전** — Operations Lead 가 자동 spawn
- 결과는 PR description 의 "## Persona impact" 섹션에 그대로 붙여넣음
- Rule B 의 "최소 5 페르소나" 정량 기준 충족 검증

#### 토큰 예산 가이드라인 (구체적 수치)

| 항목 | 목표 | 상한 |
|---|---|---|
| 에이전트 prompt 크기 | 200-800 단어 | 1,200 단어 |
| 에이전트 1회 런타임 | 30-90 초 | 5 분 (초과 시 sub-track 분할) |
| Operations Lead 라운드 요약 (사용자 회신) | ≤200 단어 | 400 단어 |
| 라운드당 Sonnet token 비용 | <$0.50 | $1.50 (초과 시 회고) |
| 1 라운드의 commit 수 | 1 commit | 3 commit (초과 시 라운드 쪼개기) |

> Prompt 가 50 단어 미만이면 너무 모호해서 hallucination 발생. 5,000 단어 초과면 self-contained 실패 — 작업을 트랙으로 더 쪼갰어야 함.

#### Failure modes + 복구 플레이북

| 실패 모드 | 신호 | 복구 |
|---|---|---|
| **Agent timeout** | 5 분 무응답 | SendMessage 동일 에이전트로 "continue / report current state". 새 spawn X (토큰 낭비) |
| **Agent hallucination** (없는 파일 인용 등) | grep 결과 0, 파일 존재 X | 다음 prompt 에 명시: "Read <abs_path> first before editing. Do not invent paths." |
| **Track conflict** (같은 파일 동시 수정) | `git status -s \| sort \| uniq -c` 결과 중복 | 두 번째 트랙 abort → 순차 재실행. 또는 Operations Lead 가 직접 merge |
| **Test regression** | jest/tsc 빨간불 | failure log + 최근 diff 를 prompt 로 묶어 debugger agent dispatch |
| **TS error 폭증** (>20 errors) | `tsc --noEmit` 결과 | strict 끄지 말 것. 트랙 rollback 후 더 작게 쪼개서 재시도 |
| **에이전트 결과 부정확** | 검토 시 spec 미충족 | SendMessage 로 동일 에이전트 재 prompt — 결과 형식 강제 (e.g. "Return JSON: {files_changed:[], tests_added:N}") |

#### Inter-track 조정 룰

트랙 간 충돌은 토큰 낭비 1순위. 다음 룰 강제:

- **각 트랙은 명확히 경계된 파일 집합 소유** — prompt 에 절대경로로 명시
  - 예: 트랙 A = `mobile/app/(tabs)/scores/**`, 트랙 B = `backend/api/scores/**`
- **Lock list 멘탈 모델**: Operations Lead 는 라운드 시작 시 "이번 라운드에서 건드릴 디렉토리 = ?" 를 머릿속에 그림. 같은 디렉토리에 두 에이전트 X
- **공유 유틸리티 (theme.ts, design tokens, types/ 글로벌)** = Operations Lead 가 직접 atomic edit. 절대 위임 X — race condition 발생
- **package.json / tsconfig / 설정 파일**: 항상 Operations Lead 단독 수정. 트랙 spawn 전 미리 확정

#### Round 번호 부여 규칙

- **모든 commit** 은 `feat(round-NNN): ...` 또는 `fix(round-NNN): ...` 또는 `chore(round-NNN): ...` 패턴
- **1 라운드 = 1 응집된 변경 묶음 → 1 push 단위**. 1 commit 이 디폴트, 최대 3 commit
- **Round 번호는 단조 증가, 재사용 X, skip X**
- **다음 번호 SoT**: `git log --oneline | grep -oE 'round-[0-9]+' | head -1` + 1
  - 라운드 시작 직후 위 명령 실행 → 변수에 저장 → 모든 commit 메시지에 적용
- **문서 명** (`docs/round-NNN-*.md`) 도 동일 번호 사용

#### GuideOne 코드베이스 anti-pattern (라운드 회고에서 축적)

다음 패턴은 PR review 에서 **자동 reject 사유**. 발견 즉시 수정 또는 트랙 abort.

| Anti-pattern | 올바른 방법 | 라운드 출처 |
|---|---|---|
| `bg-emerald-500`, `text-blue-600` 등 직접 utility | `bg-accent-500`, `text-fg-primary` 등 design token | R116 |
| 인라인 섹션 라벨 (`<Text>Section</Text>`) | `<Eyebrow>` atom 사용 | R117 |
| "Backend OFF", "Mock mode" 같은 영어/기술 UX 문구 | "데모 모드" 한국어 친화적 표현 | R120 |
| `#0a7ea4` 또는 Expo 기본 청록 | 디자인 토큰 외 hex 금지 | R116 |
| UI 문자열에 액션 동사 ("처방", "투여", "권고", "시행") | "참고 점수", "분류 결과" 등 정보 표현 | F250 enforce |
| 환자 실명 / 주민번호 / 차트번호 | aliasGuard 필터 통과한 alias 만 | PIPA blocker |
| 가이드라인 본문 텍스트 DB / 시드 / 코드 저장 | 메타데이터 + deep link 만 | Rule C |
| 한 에이전트에 "전부 다 해줘" 통째로 위임 | 명확한 scope, 200-800 단어 self-contained prompt | Rule D 토큰 룰 |
| `npm install` 후 lock 파일 미커밋 | `package-lock.json` 항상 함께 commit | DevOps |
| TS error 우회용 `// @ts-ignore` 추가 | strict 유지, 타입 fix. ignore 는 외부 라이브러리만 | tsconfig strict |

> 새 anti-pattern 발견 시 라운드 회고 (`docs/round-NNN-*.md`) 에 기록 후 다음 PR 에서 위 표에 추가.

### Rule E: 세션 인계 (Token-Out Survival)

**모든 라운드는 다음 세션이 즉시 이어받을 수 있도록 인계 기록을 남긴다.**

매 commit 직후 또는 라운드 전환 시점에 `docs/HANDOFF.md` 갱신. 토큰 한도 hit 신호 (agent timeout, monthly limit response) 감지 시 즉시 다음 5개 섹션 작성:

#### 인계 기록 5 섹션 (필수)

1. **현재 진행 상태** (Done):
   - 직전 라운드 N 까지의 산출물 (commit hash + summary)
   - 사용자 보고 사항 status (close / partial / pending)
   - features.json passing count + 주요 milestone
   - 검증 통과 항목 (TS errors / test count / deploy status)

2. **다음 라운드 즉시 시작 가능한 작업** (Next):
   - Track A/B/C 별 self-contained prompt
   - 이미 식별된 root cause + 수정 위치 (file:line)
   - dependent agent type 명시
   - 토큰 예산 추정 (small/medium/large)

3. **블록 / 사용자 액션 대기 항목** (Blocked):
   - GCP 셋업 / Supabase / EAS 등 사용자 manual action
   - 인증/결제/계정 관련 wait
   - 외부 service 응답 wait

4. **오류 history** (Errors):
   - 라운드별 발견된 버그 + root cause + fix commit
   - agent failure (timeout / hallucination / usage limit)
   - 재발 시 빠르게 진단 가능하도록 signature 기록

5. **Open follow-ups** (Backlog):
   - features.json passing: false 와 cross-reference
   - 다음 사용자 보고 가능성 시나리오
   - 디자인 / 데이터 / 인프라 별 우선순위 분류

#### 자동 갱신 메커니즘

`scripts/handoff-update.sh`: 매 commit 후 실행 가능한 헬퍼.
- `git log --oneline -1` → 라운드 번호 추출
- `npm test --silent | tail -3` → 테스트 카운트
- `gh pr list --state open` → 활성 PR
- 결과를 `docs/HANDOFF.md` 의 "현재 진행 상태" 섹션에 저장

#### 닫힌/머지된 PR 재사용 금지

새 라운드는 **새 branch + 새 PR** — 닫히거나 머지된 PR 재사용 X. 이유:
- merge 후 추가 push 는 GitHub 가 PR 재오픈 X (R116 학습)
- diverged history 정리 비용 > 신규 PR 생성 비용
- 신규 PR = clean review surface

예외: hot-patch 동일 사용자 보고 1건에 대해서만 동일 PR 안에 추가 commit 허용.

#### Token-out 신호 + 즉시 행동

다음 신호 시 즉시 인계 모드 전환:
- agent 응답에 "monthly usage limit" / "context length" 포함
- 5분 이상 무응답
- 같은 commit 3회 이상 retry

행동:
1. 진행 중 트랙 abort
2. `docs/HANDOFF.md` 5 섹션 강제 갱신
3. commit + push 즉시
4. 사용자에게 한 줄 보고: "토큰 한도, R-NNN까지 인계 기록 완료"

#### 세션 간 연속성

이 Rule E 는 **세션 바뀌어도 자동 적용**. 새 세션 메인 Claude 는 시작 시점에:
1. `docs/HANDOFF.md` 읽기 (필수)
2. "다음 라운드 즉시 시작 가능한 작업" 의 Track 목록 확인
3. 사용자 별도 지시 없어도 해당 Track 부터 dispatch 가능

CLAUDE.md 가 매 세션 자동 로드되므로 Rule A/B/C/D/E 모두 재진입.

---

## 페르소나 검증 로그 (Rule B 준수)

신규 user-facing feature 마다 [`docs/persona-verification.md`](./docs/persona-verification.md) 에 ≥5 페르소나 daily-life impact 기록. **Round 126 첫 batch** — 6 shipped features (CR01/02/03 · RD01 · GL02 · F250) × 5 personas = 30 assessments, 8/8 카테고리 커버. 신규 feature PR 시 동일 파일에 섹션 추가 + `features.json` 의 `_persona_verified: true / _persona_count: 5 / _persona_categories: [...]` 플래그 갱신.

---

## 현재 상태 (2026-05-10, Rounds 116-129 shipped, PR #6 ready for merge review)

- **Phase**: 0 demo hardened + Phase 1 베타 전환 임박. Round 116-129 (~14 rounds, PR #6). ClinRef 4-module fully wired, Rounds mode E2E + security audit (6 P0 fixes), Design system atoms/molecules/organisms complete. Persona library 141. TypeScript strict 0 errors sustained. ~3,500 tests passing (mobile 3,465 + backend 139 = 3,604 total).
- **최신 진행**: PR #6 (feat/round-116-cloud-run-fix-and-play-store), R116-R129 통합:
  • R116-R118: ClinRef 4-module + DS01 font stack (Plus Jakarta Sans/Inter/IBM Plex Mono/Pretendard Variable) + TypeScript strict 0 errors.
  • R119-R121: Backend smoke test (5 P1 bugs caught), Guidelines 3-level fallback (network → cache → bundled 665 entries), Rounds mode hardening.
  • R122-R126: Persona library 78→141, ClinRef backend wiring (useTutorAsk/useMcqGenerate/useClinicalSearch), 2 atoms extracted (TierLegendStrip/PillTabBar), Modals.jsx integration, F250 ban-word test (141 tests, 0 violations).
  • R128: 캐시 copy across 4 surfaces, STUB/FALLBACK 5→15, medical synonyms 76 groups, i18n 171→228 keys, 3,455 tests.
  • R129: CardLongPressPreview molecule (long-press → bottom-sheet preview, no navigation), GuidelineRow wired, 10 new tests, 3,465 total.
- **GuideOne ≡ INGO Clinical 구현체**: 같은 코드베이스, 같은 GitHub repo. 이름은 GuideOne 유지, 스펙은 ingo_clinical 따름. 보험 layer + publish flow 포함.
- **저작권 회피 핵심 전략**: 가이드라인 본문은 절대 DB·코드·시드에 저장 X. 메타데이터 + 학회 사이트 deep link 만 보유. 교과서/케이스 인덱스 (메타만) 포함. 3-level fallback (network → SQLite cache → bundled JSON). Clinical reference 4-module (search/education/calculators/dosing/notes) = 정보 제공 + 시뮬레이션 (진단 권고 X).
- **의료기기 회피 핵심 전략**: 점수 계산기 = 점수만 출력. "권고/시행/처방" 등 액션 단어 F250 컴파일 거부 (141 tests verified). Mock cases = fictional 27×9 specialty scenarios (SaMD 회피). Modals = 면책 + 알림 (action advice X).
- **다음**: GitHub PR #6 merge → Apple Developer + Google Play 등록 (1-3일 본인인증) + Supabase + API keys → 본격 베타. EAS Build 첫 native 빌드 → TestFlight + Play Internal.
- **Repo**: https://github.com/ingo-lab/Guideone (Phase 0 demo live, 100+ commits, PR #6 ready for merge review)

---

## 무엇을 owning 하는가

| 파일 | owner agent | 상태 |
|---|---|---|
| `docs/00_ORIGINAL_BRIEF.md` | Darren | ✅ 완성 (source of truth) |
| `docs/01_ATELIER_PLAN.md` | orchestrator | ✅ v1 (보험 layer + Publish 추가됨) |
| `docs/PRD.md` | product-manager | ✅ v0 (시험 후 인터뷰로 검증·갱신) |
| `docs/ARCHITECTURE.md` | solution-architect | ✅ v0 |
| `docs/DESIGN.md` | ui-ux-designer | ✅ v0 (텍스트 wireframe; Figma 는 시험 후) |
| `features.json` | product-manager | ✅ v0 (~30개 P0/P1 항목; 인터뷰로 50+ 확장 예정) |
| `content/samples/stemi-card.json` | content-curator | ✅ DRAFT (의학 reviewer 사인오프 전) |
| `content/samples/stemi-insurance-cards.json` | insurance-data-curator | ✅ DRAFT (HIRA 검증 전) |
| `policies/privacy-policy-ko.md` | legal-counsel + compliance-officer | ✅ v0 (변호사 자문 전) |
| `policies/medical-disclaimer-ko.md` | legal-counsel | ✅ v0 |
| `policies/medical-disclaimer-en.md` | legal-counsel + localization-qa | ✅ v0 |
| `policies/terms-of-service-ko.md` | legal-counsel | ✅ v0 (변호사 자문 전) |
| `mobile/` | mobile-dev | ⏳ scripts/setup.sh 실행 후 |
| `backend/` | backend-dev | ⏳ scripts/setup.sh 실행 후 |

---

## 팀 (Atelier+ 35명)

기존 Atelier 16명 + 신규 19명. 자세한 명단은 `docs/01_ATELIER_PLAN.md` 섹션 3.

**현재 활성**: orchestrator, product-manager, solution-architect, ui-ux-designer, content-curator, insurance-data-curator, legal-counsel, compliance-officer.

**시험 후 활성 예정**: mobile-dev, backend-dev, database-engineer, vector-search-engineer, guideline-pipeline-engineer, partnership-coordinator, user-researcher.

---

## 작업 원칙

1. **모든 카드는 reviewer 사인오프 후 published**. AI draft 는 항상 status="draft" + 면책 표시.
2. **failing tests get fixed, never deleted.** features.json 의 acceptance 는 절대 약화 X.
3. **면책 (F120, F121) 은 ANY build 에서 깨지면 안 됨**. 자동 monitor.
4. **환자 PHI 입력 X**. 자동 마스킹은 backup, 사용자 안내는 onboarding 부터.
5. **보험 카드는 분기마다 재검수.** 90일 이상 미갱신 = 경고 배지, 180일 = 빨강.
6. **SaMD 회피 — 자연어 케이스 입력은 v1.0 X**. 키워드/시나리오 매칭만.
7. **Delegate, don't do.** orchestrator 는 위임만, 코드 작성 X.

---

## 기술 스택 (확정)

- **Mobile**: Expo SDK 52+ · React Native 0.76+ · TypeScript strict · NativeWind · expo-router · Zustand · TanStack Query · expo-sqlite + Drizzle · expo-secure-store
- **Backend**: FastAPI (Python 3.12) · Supabase Postgres + pgvector · Upstash Redis · Anthropic Claude (Sonnet + Haiku) · OpenAI text-embedding-3-large
- **Bot**: Kakao i Open Builder
- **Hosting**: Fly.io (Tokyo → Seoul v2) · Supabase (Singapore → Seoul v1.5+) · CloudFront CDN
- **Mobile build**: EAS Build + EAS Submit
- **배포 아키텍처**: 자세한 mobile vs web 분리는 [`docs/ARCHITECTURE_DEPLOYMENT.md`](./docs/ARCHITECTURE_DEPLOYMENT.md) 참조

---

## 진행 워크플로우

### `/new-app GuideOne` 트리거 시
1. orchestrator 가 docs/PRD.md + ARCHITECTURE.md + DESIGN.md + features.json 읽음
2. 누락된 갭 (없으면 skip), 인터뷰 결과 (시험 후 추가) 반영해 v1 으로 갱신
3. 병렬 빌드: database-engineer (schema migrate) + backend-dev (FastAPI 스캐폴드 채움) + mobile-dev (Expo 화면 구현) + content-curator (가이드라인 5개 디지털화)
4. test-engineer 가 features.json acceptance → 테스트 코드
5. code-reviewer + security-auditor + clinical-validator + insurance-data-curator + qa-verifier (병렬)
6. progress-keeper 매 sprint 종료 시 claude-progress.txt 갱신

### 코드 변경 시 매번
- code-reviewer: 모든 PR
- security-auditor: auth/data/PII 변경 시
- clinical-validator: 콘텐츠 변경 시
- qa-verifier: features.json passing flip 전 무조건

---

## Git 워크플로우

- main 브랜치 보호 (직접 push X)
- feature 브랜치: `feat/F010-search-korean`
- 커밋: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`)
- PR 템플릿: 무엇 / 왜 / 어떻게 검증 / 면책 영향 (의료 앱 특화)
- main → staging 자동 배포 (Fly.io + EAS internal channel)

---

## 환경 변수

`.env.example` 참고. **절대 commit X**. Doppler 또는 1Password Secrets Automation 사용.

---

## Open Questions (시험 후 해결)

- OQ-1 보험 데이터 — HIRA OpenAPI 가용 endpoint 실제 검증
- OQ-2 카카오 봇 — i Open Builder vs 비즈 메시지 latency 측정
- OQ-3 Embedding 모델 — text-embedding-3-large vs multilingual-e5-large 한국 의학 용어 sample 비교
- OQ-4 PDF 파서 — Claude Vision vs Unstructured.io
- OQ-5 한국 region 데이터 거주성 — Supabase Seoul 필수 시점

자세한 내용은 `docs/ARCHITECTURE.md` 섹션 10.

---

## 다음 한 걸음

**현재 위치 (2026-05-10, Round 118 shipped)**:
- ✅ Rounds Mode (Phase 0 demo, audit close)
- ✅ ClinRef 4-module (search / education / calculators / dosing / notes)
- ✅ Design System atoms (Eyebrow / BackendHealthPill / QuickActionTile)
- ✅ specialtyTaxonomy (24→9 mapping auto-fallback)
- ✅ TypeScript strict mode (0 errors, 2318 tests all green)

**병렬 진행 (외부 의존성)**:
```
# Track A: Backend wiring (GCP Cloud Run)
1. GCP 프로젝트 + 결제 + WIF 셋업 (~30분)
   → docs/DEPLOY_CLOUD_RUN.md 참고
2. GitHub Secrets 등록 (GOOGLE_CLOUD_PROJECT_ID, etc.)
3. 첫 deploy → backend URL 수신

# Track B: Mobile native 출시 (Apple + Google)
1. Expo 계정 + Apple Developer 가입 ($99/년, 1-3일 인증)
   → docs/DEPLOY_MOBILE.md 참고
2. Play Console 가입 ($25, ~1일)
3. EAS init + TestFlight + Play Internal track 시작

# Track C: 콘텐츠 wiring
1. Backend 연결 후 → Supabase RLS + embedding vector
2. ClinRef case 화면 live data wiring (현재 mockCases stub)
3. Textbook navigator 실제 linking (currently index only)

# Track D: Google Play Store submission (병렬)
1. docs/STORE_METADATA.md — KR/EN store listing (F250 SaMD guard 완료)
2. 데이터 보안 양식 + IARC rating (의료 앱 분류)
3. Review guideline 체크리스트 (privacy / disclaimer / no medical advice)
