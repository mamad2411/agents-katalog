---
name: track-status
effort: low
description: |
  Track 작업 추적 현황을 조회하고 6단계 워크플로우 가이드를 제공한다.
  환경 점검(setup-til-skills), 제품 검증(product-review), 작업 명세(work-plan), 구현(work-plan-start), 검증, 마무리 단계 시각화.
  "/track-status", "트랙 상태", "작업 추적", "track 확인", "진행 상태" 요청에 트리거된다.
  같은 Jira 번호에 여러 sub-track이 있으면 목록을 표시하고 선택할 수 있다.
---

# Track Status Skill

`.claude/tracks/` 하위의 Track 상태를 조회하고, 6단계 워크플로우 가이드를 제공한다.

> **첫 응답 맨 위에 항상 한 줄 표시**:
> `📖 워크플로우 헷갈리면: .claude/docs/WORKFLOW-GUIDELINE.md (단일 진실 출처)`

---

## 실행 방법

```
/track-status                    # 전체 Track 목록 + 환경 점검 요약
/track-status TECH-22386         # 해당 Jira 번호의 모든 sub-track 표시
/track-status TECH-22386-shipment  # 특정 Track 상세 조회 + 워크플로우 다이어그램
```

---

## 작업 절차

### 1. Track 목록 조회

`.claude/tracks/index.md`를 읽어 전체 Track 목록을 파악한다.

### 2. 환경 점검 (모든 모드 공통, 첫 5줄 출력)

`.claude/docs/setup-state.json`을 읽어 다음을 표시:

```
🔍 환경: ✅ ATLASSIAN_API_TOKEN | ❌ Slack MCP | ✅ Codex
   (마지막 setup: 2026-04-22, 7일 경과 → /setup-til-skills 권장)
```

파일 부재 시:
```
⚠️ 환경 점검 미실행 — /setup-til-skills 한 번 실행하세요.
```

### 3. 인자 분석

- **인자 없음**: 전체 Track 목록 표시 (Active / Completed / Archived)
- **Jira 번호만** (예: `TECH-22386`): 해당 Jira의 모든 sub-track을 필터링하여 표시
- **전체 Track ID** (예: `TECH-22386-shipment`): 해당 Track의 상세 정보 표시

### 4. Jira 번호로 조회 시 — 다중 Track 선택

같은 Jira 번호에 여러 Track이 있으면 AskUserQuestion으로 선택을 요청한다.

### 5. Track 상세 조회

선택된 Track의 `metadata.json`을 읽고, `references/workflow-stages.md`를 참조하여 다음을 출력한다:

#### 5-1. 기본 정보 + 인프라 체크

```markdown
## Track: {track_id}

| 항목 | 값 |
|------|------|
| 설명 | {description} |
| 상태 | {status} |
| 브랜치 | {branch} |
| 제품 검증 | {product_review_decision 또는 "(미실행)"} |
| Phase | {current_phase} / {total_phases} |
| 상위 Track | {parent_track 또는 "—"} |

### 인프라 점검
- {.claude/CONTEXT.md ✅/⚠️}
- {.claude/docs/adr/0001-... ✅/⚠️}
- {Hard dependency 충족도 한 줄 요약}
```

#### 5-2. 워크플로우 단계 다이어그램 (★ 핵심)

`{DOC_DIR}` 내 파일 존재 여부 + setup-state.json + metadata.json 으로 현재 위치 추론:

```
[✓] Step 0  환경 점검          (setup-state.json 정상)
[✓] Step 0.5 제품 검증           (Go)
[✓] Step 1  작업 명세            (WORK-SPEC + 3-1 Agent Brief ✅)
[▶] Step 2  구현 (Phase 2/5)    ← 현재 위치
[ ] Step 3  검증
[ ] Step 4  마무리
```

마커 규칙:
- `[✓]` 완료 (산출물 파일 존재 + 품질 체크 통과)
- `[▶]` 진행 중 (현재 단계)
- `[ ]` 미진입
- `[⚠️]` 보강 필요 (예: WORK-SPEC 있는데 3-1 섹션 누락)
- `[—]` 건너뜀 (예: product-review 미실행, Step 0.5는 선택)

#### 5-3. 문서 현황 + 품질 체크

`{DOC_DIR}` 내 번호별 파일 + WORK-SPEC.html 의 3-1 섹션 검증:

```markdown
### 문서 현황
- [x] 1_REQ-SNAPSHOT.html
- [x] 2_WORK-SPEC.html
  └ 3-1. 변경 인터페이스 (Agent Brief): ✅ (또는 ⚠️ 누락 → 보강 권장)
- [x] 3_FEATURE-CHECKLIST.html
- [▶] 4_PLAN.html (Phase 2/5)
- [ ] 5_ARCHITECTURE.html
- ...
```

**WORK-SPEC.html 3-1 섹션 검증 방법**: Read 도구로 WORK-SPEC.html 읽고 `^## 3-1\.` 패턴 또는 "변경 인터페이스" / "Agent Brief" 키워드 검색. 누락 시 `[⚠️]` 표시.

**0_INDEX.html 생성 시**: 산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 문서 관계도를 인라인 SVG 다이어그램으로 포함한다.

#### 5-4. 다음 추천 명령

`references/workflow-stages.md`의 단계별 가이드 메시지 양식 참조:

```markdown
### 다음 추천 명령
1. **/work-plan-start** — Phase 3 진행
   └ 에러 발생 시: debugger 에이전트 (Phase 1 재현 loop 우선)
   └ 코드 영역 모를 때: /zoom-out
   └ 응답 길어질 때: /caveman 토글
```

#### 5-5. 사용 가능한 도구 모드 (footer)

```markdown
### 도구 모드 (단계 무관)
- `/caveman` — 토큰 75% 절약 모드
- `/zoom-out` — 한 단계 추상화 맵
- debugger 에이전트 — 5-phase 진단

### 더 알아보기
📖 .claude/docs/WORKFLOW-GUIDELINE.md (전체 6단계 + 7가지 패턴 + 결정 트리)
```

### 6. Track 상태 변경 (선택적)

사용자가 Track 상태를 변경하고 싶으면:
- `in_progress` → `completed`: metadata.json 업데이트 + index.md에서 Active → Completed로 이동
- `completed` → `archived`: metadata.json 업데이트 + index.md에서 Completed → Archived로 이동

---

## metadata.json 호환성

새 필드 (`product_review_decision`, `grilling_completed`, `agent_brief_complete`, `hard_dependencies`, `tools_used`)는 모두 **optional**.
누락 시 graceful 처리:
- `product_review_decision` 없음 → "(미실행)"
- `agent_brief_complete` 없음 → WORK-SPEC.html을 직접 grep으로 검사
- `hard_dependencies` 없음 → 환경 점검 결과로부터 추론
- `tools_used` 없음 → footer에 표시 안 함

기존 Track의 metadata.json에 강제 마이그레이션 X.

---

## 출력 형식 (요약)

### 전체 목록 모드
```
🔍 환경: ✅ X / ❌ Y
📖 워크플로우 가이드: .claude/docs/WORKFLOW-GUIDELINE.md

## Track 현황
### Active (N개) / Completed (N개) / Archived (N개)
{표 형식}
```

### 상세 조회 모드
```
🔍 환경: ...
📖 가이드: ...

## Track: {track_id}
{기본 정보 표}
### 인프라 점검
### 워크플로우 단계 (다이어그램)
### 문서 현황 (품질 체크 포함)
### 다음 추천 명령
### 도구 모드
### 더 알아보기
```

---

## 참고

- 단계별 상세 가이드: [`references/workflow-stages.md`](./references/workflow-stages.md)
- 단일 진실 출처: [`.claude/docs/WORKFLOW-GUIDELINE.md`](../../docs/WORKFLOW-GUIDELINE.md)
- 의존성 분류: [`.claude/docs/adr/0001-skill-dependency-classification.md`](../../docs/adr/0001-skill-dependency-classification.md)
