---
name: auto-dev
description: Automated development pipeline. Runs a completed Planning Work through Development and Validation phases end-to-end.
model: sonnet
effort: high
---

# Auto-Dev 스킬

Work 파일과 Task 시스템을 통합하여 Development → Validation 파이프라인을 자동 실행합니다.

---

## Step 0: Work 컨텍스트 + Task 시스템 초기화 [건너뛰기 금지]

### 진입 확인 [건너뛰기 금지]

Work ID가 제공된 경우, `planning-results.md` 존재 여부 확인:

```bash
ls docs/works/active/W-XXX-*/planning-results.md 2>/dev/null \
  || ls docs/works/idea/W-XXX-*/planning-results.md 2>/dev/null
```

- **파일 있음** → 계속
- **파일 없음** → "planning-results.md를 찾을 수 없습니다. `/plan-task W-XXX`를 먼저 실행하세요." 출력 후 중단

Work ID 없이 새 요청으로 진입한 경우 (`/auto-dev 로그인 기능 추가` 형식):
- `work.sh new`로 Work 생성 후 → **즉시 `/plan-task W-XXX`로 위임** (planning-results.md 없이 Step 1 진행 금지)
- 이는 `brainstorming → plan-task → auto-dev` 체인 준수를 위함

Fallback 모드(`docs/works/` 폴더 자체가 없는 경우)에서는 이 확인을 스킵합니다.

### Work ID가 제공된 경우 (예: `/auto-dev W-042`)

1. Work 파일 위치 탐색: `docs/works/idea/` 또는 `docs/works/active/`
2. `W-XXX-{slug}/W-XXX-{slug}.md` 와 `planning-results.md` 읽기
3. frontmatter `status`, `current_phase`, `phases_completed` 확인

**idea 상태면 자동 전환:**

```bash
./scripts/work.sh start W-042
# idea/ → active/ 이동, status: active, started_at 기록
```

**current_phase에 따른 시작 위치:**

| current_phase | 시작 위치       |
| ------------- | --------------- |
| `planning`    | Step 1부터 전체 |
| `development` | Step 2부터 재개 |
| `validation`  | Step 3부터 재개 |

### Work ID가 없는 경우 (예: `/auto-dev 로그인 기능 추가`)

`docs/works/` 폴더 존재 여부 확인:

- **존재하면** → `work.sh new`로 새 Work 생성 후 Step 1부터 진행:
  ```bash
  ./scripts/work.sh new "<요청 제목>"
  ```
- **없으면** → Step 4 fallback

### Task 시스템 초기화 [건너뛰기 금지]

Work ID 확보 후 반드시 실행:

1. `ToolSearch("select:TaskCreate,TaskUpdate,TaskList")` — 스키마 fetch

> **Task 도구가 없으면 멈추지 말고 대체 경로로 간다** — `ToolSearch`가 Task 계열을
> 반환하지 않는 호스트/세션이 있다(F-038). 그때는 `./scripts/checklist.sh` 기반
> durable checklist로 추적한다. 규율 SSOT: `skills/plan-task/references/task-tools-fallback.md`.
2. `TaskList` 실행 → subject가 `[W-XXX]`로 시작하는 Task 있으면 상태 확인 후 재개 (재생성 스킵, W-XXX는 현재 Work ID)
3. Task 없으면 → Step 1: Development Tasks 생성으로 이동

---

## Step 1: Development Tasks 생성

`planning-results.md`의 구현 계획 항목 분석 + **소스코드 직접 탐색**:

1. 구현 계획 항목 목록화
2. 코드베이스 직접 탐색 (에이전트 위임 아님):
   - 이미 구현된 파일/함수 확인
   - 해당 항목은 ✅ 완료로 마킹 (Task 생성 스킵)
3. 미완료 항목만 TaskCreate:

**분리 기준:**

- 독립적으로 구현 가능한 항목 → 별도 Task (병렬 실행)
- 다른 항목에 의존하는 항목 → `addBlockedBy` 설정

**Task 네이밍:** `[W-XXX][Dev] {구현 항목명}`

**TaskCreate 시 모든 Task에 metadata 포함:**

```json
{ "work_id": "W-XXX", "phase": "development" }
```

**예시 구조:**

```
T-dev-1: [W-042][Dev] 데이터 모델 정의       ← 독립 (병렬)
T-dev-2: [W-042][Dev] API 엔드포인트 구현    ← blockedBy: T-dev-1
T-dev-3: [W-042][Dev] 프론트엔드 컴포넌트   ← blockedBy: T-dev-1
T-dev-4: [W-042][Dev] 테스트 작성            ← blockedBy: T-dev-2, T-dev-3
```

`progress.md` Task Map 생성/갱신 (description 컬럼 포함).

---

## Step 2: Development 실행

각 Task를 `implement-code` 에이전트에 위임 (isolation: worktree):

**병렬 실행 원칙 (스케일별 — Spec 2 / W-006):**

blockedBy 없는 Task가 2개 이상이면 동일 응답에서 동시 dispatch:

```
Agent(task_A) ─┐
Agent(task_B) ─┼─ 동일 응답에서 동시 dispatch
Agent(task_C) ─┘
```

**dispatch 전 파일 소유권 확인 (rules/parallel-worktree.md) [건너뛰기 금지]:**
병렬 안전은 병합 직렬화가 아니라 **dispatch 시점의 파일 분리**로 확보한다(메인은
서브에이전트의 ExitWorktree 타이밍을 직렬화할 수 없다). 따라서:

1. 병렬 청크의 수정 대상 파일이 disjoint한지 확인한다. disjoint하면 각 에이전트가
   언제 복귀하든 트리 충돌이 없다.
2. 겹침을 피할 수 없으면 해당 청크들을 **순차 dispatch**로 강등한다(하나 dispatch →
   ExitWorktree까지 완료 확인 → 다음). 의존성 상류(공유 타입/유틸) 청크를 먼저.
3. 공유 파일(설정·배럴 export·라우트 등록부)은 병렬 청크에 배정하지 않고 마지막에
   메인 세션이 단독 수정한다.

**Worktree 복귀 (병렬 dispatch 후):**

- 각 에이전트가 worktree 안 검증(린트+관련 테스트) 그린 후 **스스로** `ExitWorktree`로
  복귀한다(각 에이전트 본문 "Worktree 복귀 프로토콜"). disjoint 전제가 지켜지면 동시
  복귀도 안전하다.
- 병합 충돌 발생 시(전제가 깨진 경우): 임의 해결 금지 → `git-workflow`에 위임해 충돌
  파일/내용 보고 + NEED_USER_INPUT(ours/theirs/manual) 에스컬레이션.
- 같은 지점 충돌 2회 반복 = 청크 분해 오류 → 남은 dispatch 중단, plan 단계로 돌아가
  청크 경계(파일 소유권)를 재설계한다.

**Large 라우팅:** Work `size: Large`이고 unblocked 병렬 청크가 **10개 이상**이면,
스킬 주도 dispatch는 main 컨텍스트에 부담이 큽니다. 이 경우 청크 목록을 정리해
사용자에게 네이티브 `ultracode`(dynamic workflow) 트리거를 안내하세요
(`ultracode`는 대화형 전용 — 스킬에서 자동 트리거 불가). 10개 미만이면 현행 dispatch.

**Task 완료 시 매번 의무:**

1. `TaskUpdate(id, status="completed")`
2. `progress.md` Task Map: 해당 행 상태 ✅로 수정
3. `progress.md` Task 업데이트 로그에 완료 시각 기록
4. Work frontmatter `updated_at` 갱신
5. `TaskList`로 unblocked Task 확인 → 즉시 실행

**Durable executor 규율 (W-013 — 장기·다세션 실행):**

- **미완 1항목/iteration**: 한 iteration은 checklist 미완 항목 **하나**만 목표로 한다
  (한 번에 다수 항목을 "완료"로 몰아 찍지 않는다 — 검증 없는 일괄 통과 방지).
- **verify 통과 전 passes 금지**: `checklist.json`의 `passes:true`는 오직
  `./scripts/checklist.sh pass <id>`가 항목의 `verify` 명령을 **실제 실행해 exit 0**일 때만
  전환된다. 모델 판단으로 completed를 self-mark하지 않는다.
- **상태 쓰기는 메인 세션 소유**: `checklist.json`·`progress.md` 쓰기는 **메인 세션**만
  수행한다. worktree subagent는 코드만 변경하고 상태 파일은 건드리지 않는다
  (`rules/parallel-worktree.md` 병합 충돌 해소 — 상태는 단일 writer).

모든 Dev Task 완료 후:

```bash
./scripts/work.sh next-phase W-042
# current_phase: development → validation
# phases_completed에 development 추가
```

---

## Step 3: Validation Tasks 생성 및 실행

Dev 완료 직후 Validation을 3단계로 실행합니다:

```
T-spec   (스펙 준수 확인, 단독 선행)
  ↓ 통과 후
T-review + T-security (병렬)
  ↓ 완료 후
T-merge  (결과 통합)
```

### T-spec: 스펙 준수 확인 (선행 실행)

Task 생성:
```
T-spec: [W-XXX][Validation/C] 스펙 준수 확인   — blockedBy: 모든 Dev Tasks
```

TaskCreate 시 metadata:
```json
{ "work_id": "W-XXX", "phase": "validation" }
```

**T-spec 실행 내용:**
1. `planning-results.md`의 `## 구현 계획` 항목 목록화
2. 실제 변경된 코드(`git diff` 또는 worktree 변경 파일)와 대조:
   - 모든 항목 구현 확인 → T-review + T-security 병렬 실행으로 진행
   - 누락/불일치 항목 발견 → **T-spec 실패 흐름** 실행

**T-spec 실패 흐름:**
1. 누락/불일치 항목 목록을 사용자에게 보고
2. 누락 항목에 대한 추가 Dev Task만 생성 (기존 완료 Task 유지)
3. 추가 Dev Task 완료 후 T-spec 재실행
4. **최대 2회 재시도** — 초과 시 사용자에게 판단 요청 후 파이프라인 중단

T-spec 통과 후 아래 T-review, T-security를 동시 생성 후 **병렬 실행**:

```
T-review:   [W-042][Validation/A] 코드 리뷰   — blockedBy: T-spec
T-security: [W-042][Validation/B] 보안 스캔   — blockedBy: T-spec
```

TaskCreate 시 metadata:

```json
{ "work_id": "W-XXX", "phase": "validation" }
```

**병렬 실행:**

- `T-review` → `review-code` 에이전트
- `T-security` → `security-scan` 에이전트

두 Task 모두 완료 후 결과 통합 Task 생성:

```
T-merge: [W-042][Validation] 결과 통합   — blockedBy: T-review, T-security
```

### Feedback ledger 캡처 (Spec 3 / W-007) [건너뛰기 금지]

review-code/security-scan 결과에 **발견된 결함이 있으면(pass·fail 무관)** 각 결함을 정규화해 ledger에 upsert합니다. 같은 실수를 다음 작업에서 사전 차단하는 학습 루프입니다.

```bash
# category ∈ {lint, security, architecture, test, convention}
# severity ∈ {critical, high, medium, low}
# (work.sh와 동일한 ./scripts 관례 — CLAUDE_PLUGIN_ROOT 의존 없음)
./scripts/feedback.sh upsert <category> <severity> "<결함 요지>"
```

- 발견된 결함만 기록 (통과 시 회피 패턴은 노이즈라 기록 안 함)
- ledger 로직(상한·중복제거·감쇠)은 헬퍼가 보장 — 직접 테이블 편집 금지
- 다음 세션 session-start가 상위 빈도 교훈을 `=== LESSONS ===`로 주입

### T-merge 판정 기준 [건너뛰기 금지]

#### Iron Law — 완료 주장 전 필수 실행

```
완료를 주장하기 전:
1. 어떤 명령이 이 주장을 증명하는가?
2. 지금 그 명령을 실행한다 (fresh run)
3. 출력 전체를 읽는다
4. 출력이 주장을 확인하는가?
   → NO: 실제 상태를 증거와 함께 보고
   → YES: 증거와 함께 주장
명령을 실행하지 않고 완료를 주장하는 것은 오류다.
```

<!-- Pattern from: superpowers/verification-before-completion -->
T-review, T-security 결과를 구조적으로 검증:
- review-code `decision` 필드 == `ACCEPT` 인가?
- review-code `critical_count` == 0, `high_count` == 0 인가?
- security-scan 결과에 CRITICAL/HIGH == 0 인가?

→ 모두 충족 시에만 `T-merge` 실행 ("이슈 없음" 판정)
→ 하나라도 미충족 시 이슈 목록과 권고사항을 사용자에게 보고, 파이프라인 중단

`T-merge` 실행:

0. **[Guard]** 판정 기준 미충족 시: 미충족 항목 + 이슈 목록 + 권고사항을 사용자에게 보고하고 파이프라인을 중단한다. `TaskUpdate(T-merge, status="failed")`. 아래 단계를 실행하지 않는다.
1. **검증 마커 생성** — Stop hook 이중 검증 방지:
   ```bash
   python3 - <<'PY'
   # 지문 계산의 단일 소스 = stop-validator.py의 _worktree_state_hash().
   # 과거엔 이 스니펫이 같은 로직을 복제했고(MUST MATCH 산문 계약), 예외절·타임아웃이
   # 침묵 드리프트했다(재감사 R2/ATK-002) — 이제 훅 모듈을 직접 로드해 호출한다.
   import importlib.util, os, subprocess, tempfile
   root = subprocess.run(["git","rev-parse","--show-toplevel"], capture_output=True,
                         text=True, timeout=10).stdout.strip() or os.getcwd()
   sv_path = os.path.join(root, "plugins/common/hooks/stop-validator.py")
   if not os.path.isfile(sv_path):  # 플러그인 설치 환경 폴백
       sv_path = os.path.join(os.environ.get("CLAUDE_PLUGIN_ROOT",""), "hooks/stop-validator.py")
   spec = importlib.util.spec_from_file_location("stop_validator", sv_path)
   sv = importlib.util.module_from_spec(spec); spec.loader.exec_module(sv)
   state = sv._worktree_state_hash()
   marker = str(sv.VALIDATED_MARKER)  # 경로·키 계산도 훅과 단일 소스
   d = os.path.dirname(marker)
   os.makedirs(d, mode=0o700, exist_ok=True)
   fd, tmp = tempfile.mkstemp(dir=d)
   with os.fdopen(fd, "w") as fh:
       fh.write(state)
   os.replace(tmp, marker)  # rename은 심링크 자체를 교체(CWE-59)
   PY
   ```
   > 마커에는 **검증 스코프 지문**(HEAD + 검증 대상 .py들의 내용 sha256)을 기록하고
   > 사용자별 `$TMPDIR/claude-{uid}`(0700)에 둔다. Stop hook은 이름이 아니라 이
   > 내용으로 판정한다. 지문/마커명 계산은 stop-validator 모듈 호출로 **물리적으로
   > 단일 소스** — 복제 로직 드리프트가 원천 차단된다.
2. T-review, T-security 결과를 `review-results.md`에 통합 기록
3. `TaskUpdate(T-merge, status="completed")` + `TaskList`로 이번 Work의 잔존
   in_progress/pending 태스크가 없는지 확인해 정리한다.
   (T-merge = 검증 **결과 통합** 태스크 — 브랜치 머지가 아니다. 머지 여부는 옵션
   선택 후 Work status가 추적한다.)
   **반드시 사용자 보고(다음 단계)보다 먼저** — 단발 실행에선 보고 후 턴이 사용자
   입력 대기로 끝나 마킹이 증발한다(태스크 잔존 버그의 근원). 배치 모드(Step 5)에선
   턴이 안 끝나지만 마킹-우선 순서는 동일하게 적용한다.
   마킹 규율의 SSOT는 `rules/definition-of-done.md#task-마감-규율`.
4. 사용자에게 완료 보고 후 브랜치 처리 옵션 제시:

   ```
   W-XXX Validation 통과. 다음 단계를 선택하세요:
   1. 로컬 머지 (현재 브랜치 → main)
   2. PR 생성
   3. 코드 리뷰 먼저 (`/review`)
   4. 브랜치 유지 (나중에 처리)
   ```

   옵션별 Work 상태 처리:
   - **옵션 1 (로컬 머지):** 머지 완료 후 `./scripts/work.sh complete W-XXX` 실행
   - **옵션 2 (PR 생성):** `gh pr create` 후 Work 상태 active 유지 — PR 머지 확인 후 `work.sh complete`
   - **옵션 3 (코드 리뷰):** `/review` 실행 후 결과에 따라 옵션 1 또는 2 선택
   - **옵션 4 (브랜치 유지):** Work 상태 active 유지, progress.md에 "Validation 통과" 메모 기록

---

## Step 5: 배치 모드 — 자율 완주 (Spec 5 / W-009) [opt-in]

여러 Work가 계획되어 배치로 실행 요청된 경우(예: `/auto-dev W-005 W-006 W-007`,
또는 "계획한 Work 전부 진행"), **설계 게이트 통과 후에는 P0·완료·가드 전까지 멈추지
않고** 자율 완주합니다. (Loop Engineering — `rules/loop-engineering.md`)

```
배치 드라이버 (검증된 Task 시스템 + 스킬 루프, 자체 데몬 없음):
  while (미완료 Work 존재):
    1. 의존성(Depends on) 충족된 unblocked Work 선택
    2. 해당 Work에 Step 0~3 (Development → Validation) 실행
    3. validation 통과 → progress.md 래칫 → work.sh complete
    4. 종료 가드 점검 → 다음 Work로 사람 확인 없이 전진
  → 배치 완료 보고
```

**종료 가드 (필수):**
- P0 모호함 → 즉시 `AskUserQuestion`, 루프 탈출
- validation 실패가 continueOnBlock 재시도 후에도 잔존 → 보고 후 해당 Work 정지
- 동일 Work에서 진전 없는 반복(2회+) → 에스컬레이션
- 배치 전체 완료 → 종합 보고

**단발 실행**(`/auto-dev W-XXX` 단일)은 기존 동작 유지 — 배치 드라이버 미발동.

---

## Fallback: Work 시스템 없는 경우

`docs/works/` 폴더가 없거나 Work ID 없이 요청된 경우:

Work 관련 작업(상태 전환, progress.md, decisions.md) 전부 생략하고 파이프라인만 실행:

1. **탐색**: 코드베이스 파악 (직접 탐색)
2. **계획**: 구현 계획 수립 (`plan-implementation` 에이전트)
3. **구현**: 코드 작성 (`implement-code` 에이전트, isolation: worktree)
4. **테스트**: 테스트 작성 (`write-tests` 에이전트)
5. **검증**: 코드 리뷰 + 보안 스캔 (병렬)
6. **보고**: 결과를 대화창에 출력

---

## 참고 문서

| 문서              | 경로                                              |
| ----------------- | ------------------------------------------------- |
| Work 시스템 전체  | `plugins/common/skills/plan-task/references/work-system.md` |
| Planning 프로토콜 | `plugins/common/rules/planning-protocol.md`       |
