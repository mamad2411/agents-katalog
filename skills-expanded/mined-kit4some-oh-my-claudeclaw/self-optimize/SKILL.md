---
name: self-optimize
description: >
  Self-optimization loop that analyzes system performance, identifies failure
  patterns, and improves skill prompts autonomously. Triggers on "자기 최적화",
  "self-optimize", "시스템 개선", "성능 분석", "optimize yourself", "improve yourself",
  "evolve", "자가 개선", "스스로 개선해" and similar requests. Also runs weekly via
  cron. Reads error/success logs from memory, identifies weak skills, rewrites
  prompts, commits changes, and tracks improvement over time. Includes automatic
  rollback if metrics worsen.
---

# Self-Optimize — Autonomous System Evolution Engine

## Role

Continuously improve the OpenClaw-CC system by analyzing its own performance,
identifying failure patterns, and modifying skill prompts, hooks, and workflows
to reduce errors and increase success rates. This is a closed-loop optimization
cycle: measure → analyze → modify → verify → commit or rollback.

## Safety Boundaries

### NEVER modify:
- `mcp-servers/` — MCP 서버 코드는 손대지 않음 (테스트 깨짐 위험)
- `.mcp.json` — 서버 설정 변경 금지
- `memory-store/_memory.db` — DB 직접 조작 금지

### CAN modify:
- `skills/*/SKILL.md` — 스킬 프롬프트 개선
- `scripts/hooks/*.mjs` — 훅 로직 개선
- `.claude/agents/*.md` — 에이전트 프롬프트 개선
- `CLAUDE.md` — 시스템 지시문 미세 조정 (구조 변경 금지, 문구 개선만)

### Guardrails:
- 한 사이클에 최대 **3개 파일**만 수정
- 수정 전 반드시 **git stash or branch** 생성 (롤백 포인트)
- 수정 후 **기존 테스트 실행** — 1개라도 실패 시 즉시 롤백
- 메신저로 변경 사항 보고 — 사용자 확인 후 main에 반영
- 1주일 후 성과 비교 — 개선 없으면 자동 롤백

## 7-Step Optimization Cycle

### Step 1 — Performance Data Collection

```
memory_search(tag: "error", limit: 50)       → 최근 에러 로그
memory_search(tag: "done", limit: 50)         → 최근 성공 로그
memory_search(tag: "bug", limit: 20)          → 버그 이력
memory_search_date(start_date: "{7d_ago}")    → 이번 주 전체 활동
memory_stats                                  → 전체 시스템 통계
```

### Step 2 — Failure Pattern Analysis

각 실패를 분류:

| 실패 유형 | 원인 분석 | 개선 대상 |
|----------|----------|----------|
| Skill 실행 실패 | 프롬프트 불명확, 도구 매핑 오류 | SKILL.md |
| 에이전트 위임 실패 | 컨텍스트 부족, 잘못된 에이전트 선택 | agent .md 또는 SKILL.md |
| 메모리 검색 미스 | 태그/카테고리 불일치, 인덱스 부재 | hook 또는 memory-ops |
| Hook 타임아웃 | 처리 시간 초과, 무거운 로직 | hook .mjs |
| 잘못된 결과 | 프롬프트 모호성, 검증 부재 | SKILL.md |

결과를 구조화:
```markdown
## Failure Report — Week of {date}

### Top Failure Patterns
1. **{skill_name}**: {failure_count}회 실패
   - 공통 원인: {root_cause}
   - 영향받은 워크플로우: {workflows}
   - 제안 수정: {proposed_fix}

2. **{skill_name}**: ...
```

### Step 3 — Improvement Hypothesis

각 실패 패턴에 대해 구체적 가설 수립:

```markdown
### Hypothesis #{n}
- **문제**: {skill}이 {situation}에서 {failure_mode}
- **원인**: 프롬프트의 {section}이 {reason}
- **수정안**: "{old_text}" → "{new_text}"
- **예상 효과**: {failure_type} {X}% 감소
- **검증 방법**: {how_to_measure}
```

**우선순위**: 실패 빈도 × 영향도 순으로 정렬. 상위 3개만 수정.

### Step 4 — Safe Modification

```bash
# 1. 롤백 포인트 생성
git checkout -b self-optimize/{date}

# 2. 현재 파일 백업을 메모리에 저장
memory_store(
  category: "knowledge",
  subcategory: "self-optimize",
  title: "Backup: {file} before optimization {date}",
  content: "{original_content}",
  tags: ["self-optimize", "backup", "{cycle_id}"],
  importance: 5
)
```

수정 적용:
```
For each hypothesis (max 3):
  1. Read target file
  2. Apply minimal, focused edit
  3. Document change reason in commit message
```

### Step 5 — Verification

```bash
# MCP 서버 테스트 (변경하지 않았지만 사이드이펙트 확인)
cd mcp-servers/memory-manager && npx vitest run
cd mcp-servers/knowledge-engine && npx vitest run
```

| 결과 | 액션 |
|------|------|
| 모든 테스트 통과 | Step 6으로 진행 |
| 1개라도 실패 | 즉시 `git checkout .` 롤백, 실패 원인 기록 |

### Step 6 — Commit & Report

```bash
git add {modified_files}
git commit -m "self-optimize: {summary}

Cycle: {cycle_id}
Changes:
- {file1}: {what_changed}
- {file2}: {what_changed}

Metrics before:
- Error rate: {before}%
- Top failure: {before_top}

Expected improvement: {prediction}

Constraint: Only skill/hook/agent prompts modified
Confidence: medium
Scope-risk: narrow
Not-tested: Long-term effectiveness (measured next cycle)"
```

메신저 알림:
```
messenger_send(platform: "telegram", message: "
🔧 **Self-Optimize Cycle #{n}**
📅 {date}

수정 사항:
{change_list}

예상 개선: {prediction}
브랜치: self-optimize/{date}

⚠️ 1주 후 자동 성과 비교 예정
확인 후 main 머지: `git merge self-optimize/{date}`
")
```

### Step 7 — Retrospective (다음 사이클에서 실행)

다음 주 사이클 시작 시 이전 사이클 성과 측정:

```
memory_search(tag: "error", date_range: "this_week")  → 이번 주 에러
memory_search(tag: "self-optimize", limit: 1)          → 지난 사이클 예측

Compare:
  before_error_rate vs after_error_rate
  before_top_failure vs after_top_failure
```

| 결과 | 액션 |
|------|------|
| 에러율 감소 | 성공 기록, main 머지 권고 |
| 변화 없음 | 수정 유지, 다른 접근 시도 |
| 에러율 증가 | 자동 롤백: `git revert`, 원인 분석 |

성과 기록:
```
memory_store(
  category: "knowledge",
  subcategory: "self-optimize",
  title: "Optimization Result: Cycle #{n}",
  tags: ["self-optimize", "metrics", "{cycle_id}"],
  importance: 7,
  content: "
    ## Cycle #{n} Results
    - Error rate: {before}% → {after}%
    - Changes: {file_list}
    - Verdict: {SUCCESS|NEUTRAL|ROLLBACK}
    - Lessons: {what_worked_or_didnt}
  "
)
memory_link(source: result_id, target: previous_cycle_id, relation: "derived")
```

## Optimization Targets by Priority

| 우선순위 | 대상 | 최적화 방법 |
|---------|------|-----------|
| 1 | Skill 프롬프트 | 실패 원인에 맞게 지시문 명확화, 예시 추가, 제약조건 강화 |
| 2 | Agent 프롬프트 | 컨텍스트 로딩 개선, 도구 사용 가이드 강화 |
| 3 | Hook 로직 | 타임아웃 최적화, 에러 핸들링 강화 |
| 4 | CLAUDE.md 라우팅 | 에이전트-태스크 매핑 정확도 개선 |

## Memory Integration

모든 최적화 사이클의 결과는 영구 기록:
```
memory_store(category: "knowledge", subcategory: "self-optimize")
memory_link(relation: "derived") → 이전 사이클과 연결
memory_daily_log(type: "done", entry: "Self-optimize cycle #{n}: {verdict}")
```

시간이 지나면 `memory_graph(depth: 4)`로 최적화 이력 전체를 순회하여
어떤 변경이 효과적이었는지 메타 분석 가능.

## Completion Codes

| Code | Meaning |
|------|---------|
| OPTIMIZED | 수정 적용 + 테스트 통과 + 커밋 완료 |
| NO_ACTION | 분석 결과 개선 필요 없음 (에러율 충분히 낮음) |
| ROLLED_BACK | 이전 사이클 수정이 악화 → 롤백 완료 |
| BLOCKED | 테스트 실패 → 수정 취소, 수동 검토 필요 |
